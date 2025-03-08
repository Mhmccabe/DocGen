from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DocumentSection(BaseModel):
    title: str = Field(description="The title of the section")
    content: str = Field(description="The generated content for the section")
    improvements: List[str] = Field(description="List of suggested improvements")

class LangChainHandler:
    def __init__(self, temperature=0.3):
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=temperature
        )
        self.parser = PydanticOutputParser(pydantic_object=DocumentSection)

    def generate_content(self, section: dict, context: str) -> str:
        """Generate content for a section using OpenAI."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "{context}"),
            ("user", "Title: {title}\nOutline: {content}\n\nGenerate comprehensive content for this section, keeping in mind the context and guidelines provided.")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "title": section["title"], 
            "content": section["content"],
            "context": context if context else "Generate detailed, engaging content based on the given title and outline."
        })
        return response.content

    def improve_content(self, content: str, context: str) -> str:
        """Review and suggest improvements for the content."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a professional editor. {context}"),
            ("user", "Content:\n{content}\n\nReview this content and suggest specific improvements, keeping in mind the context and guidelines provided.")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "content": content,
            "context": context if context else "Review the content and suggest specific improvements."
        })
        return response.content

def extract_sections(markdown_text: str) -> List[dict]:
    """Extract sections from markdown text based on headers."""
    sections = []
    current_section = {"title": "", "content": "", "is_empty": True}
    
    for line in markdown_text.split('\n'):
        if line.startswith('#'):
            if current_section["title"]:  # Don't add the initial empty section
                sections.append(current_section)
            current_section = {
                "title": line.lstrip('#').strip(),
                "content": "",
                "is_empty": True
            }
        else:
            content_line = line.strip()
            if content_line:  # If there's any non-empty content
                current_section["is_empty"] = False
            current_section["content"] += line + "\n"
    
    if current_section["title"]:  # Add the last section if it exists
        sections.append(current_section)
    
    return sections

def generate_markdown_download(sections: List[dict]) -> str:
    """Generate a markdown string from the sections."""
    content = []
    for section in sections:
        # Add the title with appropriate header level
        content.append(f"# {section['title']}\n")
        # Add the content
        content.append(section.get('content', '').strip())
        content.append("\n")  # Add spacing between sections
    return "\n".join(content) 