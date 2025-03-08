from typing import Dict, List, Tuple, Any, TypedDict
from langgraph.graph import Graph, StateGraph
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

class AgentState(TypedDict):
    """The state of the agent's workflow"""
    query: str
    search_results: str
    final_answer: str
    error: str

def create_initial_state(query: str) -> AgentState:
    """Create initial state dictionary"""
    return AgentState(
        query=query,
        search_results="",
        final_answer="",
        error=""
    )

class GraphSearchAgent:
    def __init__(self, temperature=0.7):
        # Initialize tools and models
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=temperature
        )
        self.search_tool = DuckDuckGoSearchRun()
        
        # Create the workflow graph
        self.workflow = self._create_workflow()
    
    def _create_workflow(self) -> Graph:
        # Create the workflow graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("perform_search", self._perform_search)
        workflow.add_node("generate_response", self._generate_response)
        
        # Define edges
        workflow.add_edge("perform_search", "generate_response")
        
        # Set entry point
        workflow.set_entry_point("perform_search")
        
        return workflow.compile()
    
    def _perform_search(self, state: AgentState) -> Dict:
        """Perform web search"""
        try:
            results = self.search_tool.invoke(state["query"])
            return {"search_results": results}
        except Exception as e:
            return {"error": str(e)}
    
    def _generate_response(self, state: AgentState) -> Dict:
        """Generate final response"""
        if state["error"]:
            return {"final_answer": f"Search error: {state['error']}"}
        
        # Use LLM to format and enhance the search results
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant that provides clear and concise answers based on search results."),
            ("user", "Query: {query}\nSearch Results: {results}\n\nProvide a clear and well-formatted answer.")
        ])
        
        try:
            response = self.llm.invoke(
                prompt.format_messages(
                    query=state["query"],
                    results=state["search_results"]
                )
            )
            return {"final_answer": response.content}
        except Exception as e:
            return {"final_answer": f"Error generating response: {str(e)}"}
    
    def process_query(self, query: str) -> str:
        """Process a query and return the response"""
        initial_state = create_initial_state(query)
        try:
            final_state = self.workflow.invoke(initial_state)
            return final_state["final_answer"] or "No answer was generated."
        except Exception as e:
            return f"Workflow error: {str(e)}"

def main():
    print("Graph-based Search Agent (Type 'quit' to exit)")
    print("-" * 50)
    print("Ask any question and I'll search the web for answers!")
    print("\nExample queries:")
    print("- What's the latest news about AI?")
    print("- Who won the most recent Super Bowl?")
    print("- What are the top programming languages in 2024?")
    print("-" * 50)
    
    # Initialize the agent
    agent = GraphSearchAgent()
    
    while True:
        # Get user input
        query = input("\nEnter your question: ").strip()
        
        # Check for exit command
        if query.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye!")
            sys.exit(0)
        
        # Check for empty input
        if not query:
            print("Please enter a question to search.")
            continue
        
        # Process query
        print("\nSearching and analyzing...")
        try:
            response = agent.process_query(query)
            print("\nAnswer:")
            print("-" * 50)
            print(response)
            print("-" * 50)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 