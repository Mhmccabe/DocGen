from typing import Dict, List, TypedDict, Callable, Union
from langgraph.graph import Graph, StateGraph
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import sys
import re
import time

# Load environment variables
load_dotenv()

class DocumentState(TypedDict):
    """The state of the document generation workflow"""
    sections: List[Dict[str, str]]  # List of sections with title and content
    current_section: int            # Index of current section being processed
    generated_content: str          # Generated content for current section
    review_feedback: List[str]      # Feedback from review agent
    improvements: List[str]         # Suggested improvements
    final_content: str             # Final improved content
    error: str                     # Error messages

def parse_markdown_file(file_path: str) -> List[Dict[str, str]]:
    """Parse markdown file into sections"""
    sections = []
    current_section = None
    
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            
        # Split content by headers
        parts = re.split(r'^(#+ .*?)$', content, flags=re.MULTILINE)
        
        for i in range(1, len(parts), 2):
            header = parts[i].strip()
            content = parts[i + 1].strip() if i + 1 < len(parts) else ""
            sections.append({
                "title": header,
                "prompt": content,
                "content": ""
            })
        
        return sections
    except Exception as e:
        raise ValueError(f"Error parsing markdown file: {str(e)}")

def create_initial_state(sections: List[Dict[str, str]]) -> DocumentState:
    """Create initial document state"""
    return DocumentState(
        sections=sections,
        current_section=0,
        generated_content="",
        review_feedback=[],
        improvements=[],
        final_content="",
        error=""
    )

class DocumentAgent:
    def __init__(self, temperature=0.7, verbose=True):
        # Initialize different LLMs for different tasks
        self.writer = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=temperature
        )
        self.reviewer = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.3
        )
        self.improver = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.5
        )
        
        self.verbose = verbose
        
        # Create the workflow graph
        self.workflow = self._create_workflow()
    
    def _create_workflow(self) -> Graph:
        workflow = StateGraph(DocumentState)
        
        # Add nodes
        workflow.add_node("generate_content", self._generate_content)
        workflow.add_node("review_content", self._review_content)
        workflow.add_node("improve_content", self._improve_content)
        workflow.add_node("finalize_section", self._finalize_section)
        
        # Define edges
        workflow.add_edge("generate_content", "review_content")
        workflow.add_edge("review_content", "improve_content")
        workflow.add_edge("improve_content", "finalize_section")
        
        # Define conditional routing
        def router(state: DocumentState) -> Dict[str, str]:
            if state["current_section"] < len(state["sections"]) - 1:
                return {"next": "generate_content"}
            return {"next": "end"}
        
        workflow.add_node("router", router)
        workflow.add_edge("finalize_section", "router")
        workflow.add_conditional_edges(
            "router",
            lambda x: x["next"]
        )
        
        # Set entry point
        workflow.set_entry_point("generate_content")
        
        return workflow.compile()
    
    def _generate_content(self, state: DocumentState) -> Dict:
        """Generate content for current section"""
        try:
            current = state["sections"][state["current_section"]]
            if self.verbose:
                print(f"\nProcessing section {state['current_section'] + 1}/{len(state['sections'])}: {current['title']}")
                print("Generating content...")
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are an expert content writer. Generate comprehensive and engaging content based on the section title and prompt.
                Use proper formatting, clear structure, and relevant examples."""),
                ("user", "Title: {title}\nPrompt: {prompt}\n\nGenerate detailed content for this section.")
            ])
            
            response = self.writer.invoke(
                prompt.format_messages(
                    title=current["title"],
                    prompt=current["prompt"]
                )
            )
            
            return {"generated_content": response.content}
        except Exception as e:
            return {"error": f"Content generation error: {str(e)}"}
    
    def _review_content(self, state: DocumentState) -> Dict:
        """Review the generated content"""
        try:
            if self.verbose:
                print("Reviewing content...")
            
            current = state["sections"][state["current_section"]]
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are a critical reviewer. Analyze the content for:
                1. Accuracy and completeness
                2. Structure and flow
                3. Clarity and readability
                4. Technical correctness
                Provide specific feedback for improvements."""),
                ("user", "Title: {title}\nContent: {content}\n\nReview this content and provide detailed feedback.")
            ])
            
            response = self.reviewer.invoke(
                prompt.format_messages(
                    title=current["title"],
                    content=state["generated_content"]
                )
            )
            
            feedback = response.content.split("\n")
            if self.verbose:
                print("\nReview feedback:")
                #for item in feedback[:3]:  # Show first 3 feedback items
                #    print(f"- {item}")
            
            return {"review_feedback": feedback}
        except Exception as e:
            return {"error": f"Review error: {str(e)}"}
    
    def _improve_content(self, state: DocumentState) -> Dict:
        """Improve content based on review feedback"""
        try:
            if self.verbose:
                print("Improving content based on feedback...")
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are an expert editor. Improve the content based on the review feedback.
                Maintain the original message while enhancing clarity, structure, and completeness."""),
                ("user", """Original Content: {content}
                Review Feedback: {feedback}
                
                Provide improved version of the content.""")
            ])
            
            response = self.improver.invoke(
                prompt.format_messages(
                    content=state["generated_content"],
                    feedback="\n".join(state["review_feedback"])
                )
            )
            
            return {"final_content": response.content}
        except Exception as e:
            return {"error": f"Improvement error: {str(e)}"}
    
    def _finalize_section(self, state: DocumentState) -> Dict:
        """Finalize the current section and prepare for the next"""
        try:
            # Update the current section's content
            state["sections"][state["current_section"]]["content"] = state["final_content"]
            
            if self.verbose:
                print(f"Completed section: {state['sections'][state['current_section']]['title']}")
                print("-" * 50)
            
            # Move to next section if available
            if state["current_section"] < len(state["sections"]) - 1:
                return {
                    "current_section": state["current_section"] + 1,
                    "generated_content": "",
                    "review_feedback": [],
                    "final_content": ""
                }
            return {}
        except Exception as e:
            return {"error": f"Finalization error: {str(e)}"}
    
    def generate_document(self, markdown_file: str) -> str:
        """Process markdown file and generate complete document"""
        try:
            # Parse markdown file
            if self.verbose:
                print(f"Loading markdown file: {markdown_file}")
            sections = parse_markdown_file(markdown_file)
            
            if self.verbose:
                print(f"\nFound {len(sections)} sections:")
                for section in sections:
                    print(f"- {section['title']}")
                print("\nStarting document generation...")
            
            # Create initial state
            initial_state = create_initial_state(sections)
            
            # Run the workflow
            final_state = self.workflow.invoke(initial_state)
            
            # Combine all sections into final document
            if self.verbose:
                print("\nGenerating final document...")
            
            document = []
            for section in final_state["sections"]:
                document.append(f"{section['title']}\n\n{section['content']}\n\n")
            
            return "\n".join(document)
        except Exception as e:
            return f"Document generation failed: {str(e)}"

def main():
    print("Document Generation Agent")
    print("-" * 50)
    print("This agent will generate content based on markdown headers and prompts.")
    print("Format your markdown file with headers and prompts like:")
    print("""
# Introduction
Write an introduction about AI and its impact

# Current Applications
Discuss the main applications of AI in industry

# Future Trends
Explore upcoming trends in AI development
    """)
    print("-" * 50)
    
    while True:
        # Get markdown file path
        file_path = input("\nEnter markdown file path (or 'quit' to exit): ").strip()
        
        if file_path.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye!")
            sys.exit(0)
        
        if not file_path:
            print("Please enter a valid file path.")
            continue
        
        # Process document
        print("\nStarting document generation process...")
        try:
            agent = DocumentAgent(verbose=True)
            document = agent.generate_document(file_path)
            
            # Save the generated document
            output_file = "generated_document.md"
            with open(output_file, 'w') as f:
                f.write(document)
            
            print(f"\nDocument generated successfully! Saved as: {output_file}")
            print("-" * 50)
            print(document)
            print("-" * 50)
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 