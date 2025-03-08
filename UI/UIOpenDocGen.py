import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
import markdown
import io

# Load environment variables
load_dotenv()

# Initialize OpenAI
llm = ChatOpenAI(
    model="gpt-4-turbo-preview",
    temperature=0.3
)

class DocumentSection(BaseModel):
    title: str = Field(description="The title of the section")
    content: str = Field(description="The generated content for the section")
    improvements: List[str] = Field(description="List of suggested improvements")

parser = PydanticOutputParser(pydantic_object=DocumentSection)

def generate_markdown_download(sections):
    """Generate a markdown string from the sections."""
    content = []
    for section in sections:
        # Add the title with appropriate header level
        content.append(f"# {section['title']}\n")
        # Add the content
        content.append(section.get('content', '').strip())
        content.append("\n")  # Add spacing between sections
    return "\n".join(content)

def extract_sections(markdown_text):
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

def generate_content(section, context):
    """Generate content for a section using OpenAI."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "{context}"),
        ("user", "Title: {title}\nOutline: {content}\n\nGenerate comprehensive content for this section, keeping in mind the context and guidelines provided.")
    ])
    
    chain = prompt | llm
    response = chain.invoke({
        "title": section["title"], 
        "content": section["content"],
        "context": context if context else "Generate detailed, engaging content based on the given title and outline."
    })
    return response.content

def improve_content(content, context):
    """Review and suggest improvements for the content."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional editor. {context}"),
        ("user", "Content:\n{content}\n\nReview this content and suggest specific improvements, keeping in mind the context and guidelines provided.")
    ])
    
    chain = prompt | llm
    response = chain.invoke({
        "content": content,
        "context": context if context else "Review the content and suggest specific improvements."
    })
    return response.content

def main():
    st.set_page_config(layout="wide")
    
    
    
    # Add the download button to the toolbar using session state to ensure it's always at the top
    if 'generated_content' in st.session_state:
        # Create markdown content from the edited sections
        sections = [
            {
                'title': section['title'],
                'content': st.session_state.edited_content.get(i, section['content'])
            }
            for i, section in enumerate(st.session_state.generated_content)
        ]
        markdown_content = generate_markdown_download(sections)
        
        # Position the download button in the top-right corner
        col1, col2 = st.columns([6, 1])
        with col2:
            st.download_button(
                label="Download MD",
                data=markdown_content,
                file_name="generated_document.md",
                mime="text/markdown",
                help="Download the generated content as a markdown file"
            )

    # Initialize session state for edit mode and content
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = {}
    if 'edited_content' not in st.session_state:
        st.session_state.edited_content = {}

    # Create two columns for split screen
    left_col, right_col = st.columns(2)

    with left_col:
        st.header("Content Context")
        context_input = st.text_area(
            "Enter context or guidelines for the AI to consider while generating content:",
            height=150,
            placeholder="""Example:
- Write in a professional but accessible tone
- Use concrete examples to illustrate points
- Focus on practical applications
- Include relevant statistics when possible
- Maintain consistency with company style guide""",
            help="This context will guide the AI in generating and improving content. It acts like a system prompt or set of guidelines."
        )

        st.header("Document Outline")
        markdown_input = st.text_area(
            "Enter your document outline in markdown format (use # for headers):",
            height=500,
            placeholder="""# Introduction
Brief overview of the topic

# Main Points
Key points to cover

# Conclusion
Summary and next steps"""
        )

        if st.button("Generate Content"):
            if not markdown_input:
                st.warning("Please enter a document outline first.")
            else:
                with st.spinner("Generating content..."):
                    sections = extract_sections(markdown_input)
                    generated_content = []
                    
                    for section in sections:
                        if section["is_empty"]:
                            # For empty sections, keep the original content without generation
                            generated_content.append({
                                "title": section["title"],
                                "content": section["content"].strip(),
                                "improvements": [],
                                "is_empty": True
                            })
                        else:
                            # Generate content only for non-empty sections
                            content = generate_content(section, context_input)
                            improvements = improve_content(content, context_input)
                            
                            generated_content.append({
                                "title": section["title"],
                                "content": content,
                                "improvements": improvements.split('\n'),
                                "is_empty": False
                            })
                    
                    st.session_state.generated_content = generated_content
                    # Initialize edit mode and edited content for new sections
                    for i, section in enumerate(generated_content):
                        if i not in st.session_state.edit_mode:
                            st.session_state.edit_mode[i] = False
                        if i not in st.session_state.edited_content:
                            st.session_state.edited_content[i] = section['content']

    with right_col:
        st.header("Generated Content")
        if 'generated_content' in st.session_state:
            for i, section in enumerate(st.session_state.generated_content):
                st.markdown(f"## {section['title']}")
                
                # Toggle edit mode button
                edit_button_label = "Switch to Read Mode" if st.session_state.edit_mode.get(i, False) else "Switch to Edit Mode"
                if st.button(edit_button_label, key=f"edit_button_{i}"):
                    st.session_state.edit_mode[i] = not st.session_state.edit_mode.get(i, False)
                
                # Edit mode or display mode based on state
                if st.session_state.edit_mode.get(i, False):
                    # Edit mode
                    edited_text = st.text_area(
                        "Edit content:",
                        value=st.session_state.edited_content.get(i, section['content']),
                        height=300,
                        key=f"editor_{i}"
                    )
                    st.session_state.edited_content[i] = edited_text
                else:
                    # Display mode
                    st.markdown(st.session_state.edited_content.get(i, section['content']))
                
                # Only show improvements for non-empty sections
                if not section.get('is_empty', False) and section['improvements']:
                    with st.expander("Suggested Improvements"):
                        for improvement in section['improvements']:
                            if improvement.strip():
                                st.markdown(f"- {improvement}")
                st.markdown("---")
    
    # Close the main-content div

if __name__ == "__main__":
    main() 