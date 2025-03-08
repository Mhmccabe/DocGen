import re
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

load_dotenv()

def parse_markdown_sections(file_path: str):
    """Parse a markdown file into sections starting with '##'."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = r"(## .+?)(?=\n## |$)"
    matches = re.finditer(pattern, content, flags=re.DOTALL)
    sections = [(m.group(0).splitlines()[0].strip(), "\n".join(m.group(0).splitlines()[1:]).strip()) for m in matches]
    return sections

# Use ChatGPT via LangChain
llm = ChatOpenAI(
    model="gpt-4",  # Change to "gpt-3.5-turbo" if needed
    temperature=0.5,
    #openai_api_key=os.getenv("OPENAI_API_KEY")  # Ensure your API key is set
)

# Prompt template
prompt_template = ChatPromptTemplate.from_template(
    """{header}

Original content:
{instruction}

Ensure your content is in a professional tone and clear
Ensure the content is focused toward architecture

Please update this section with more detailed, architecture-focused documentation in markdown format.
"""
)

def generate_section_content(header: str, instruction: str) -> str:
    """Generates updated content for one section using ChatGPT."""

    chain = prompt_template | llm
    response =  chain.invoke({"header": header, "instruction": instruction})
    return response.content

def main():
    input_md = "OpenDocGen/sections.md"
    output_md = "GeneratedDocs/updated_documentation.md"

    sections = parse_markdown_sections(input_md)
    updated_document = "# Updated Architecture Documentation\n\n"

    for header, instruction in sections:
        print(f"Processing section: {header}")
        updated_document += generate_section_content(header, instruction) + "\n\n"

    with open(output_md, "w", encoding="utf-8") as f:
        f.write(updated_document)

    print(f"Updated documentation saved to '{output_md}'")

if __name__ == "__main__":
    main()

