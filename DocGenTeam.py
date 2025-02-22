import os
from dotenv import load_dotenv
#from langchain.chat_models import ChatOpenAI
#from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI 
from langchain.schema import SystemMessage, HumanMessage, AIMessage
#from langchain.memory import ConversationBufferMemory
#from langchain_community.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferMemory  

# Load API Key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize GPT-4o Model
llm = ChatOpenAI(model="gpt-4o", temperature=0.7, api_key=openai_api_key)

# Shared Memory for Agents
memory = ConversationBufferMemory()

# ===========================
# Define Agent Functions
# ===========================

def architect_agent(project_details):
    """Creates the initial architectural document."""
    prompt = f"""
    You are an experienced architect responsible for generating technical documentation. 
    Based on the following project details:

    {project_details}

    Generate a detailed architectural document with:
    - Introduction & Objectives
    - Architecture Overview (including system diagrams)
    - System Components (APIs, Databases, Services)
    - Design Patterns Used
    - Security & Performance Considerations
    - Deployment Strategy
    - Future Scalability Plans

    Ensure clarity, technical accuracy, and completeness.
    """
    response = llm.invoke([SystemMessage(content=prompt)])
    memory.save_context({"role": "Architect-Agent"}, {"content": response.content})
    return response.content

def reviewer_agent(document):
    """Reviews the document for errors, best practices, and security considerations."""
    prompt = f"""
    You are an expert architectural reviewer. Your task is to analyze the following document for:
    - Technical accuracy
    - Best practice compliance (SOLID principles, microservices, security)
    - Performance optimization
    - Clarity and consistency

    Document:
    {document}

    Provide detailed feedback and necessary corrections.
    """
    response = llm.invoke([SystemMessage(content=prompt)])
    memory.save_context({"role": "Reviewer-Agent"}, {"content": response.content})
    return response.content

def editor_agent(document, review_feedback):
    """Edits the document based on the review feedback."""
    prompt = f"""
    You are a technical editor refining an architectural document. 

    Original Document:
    {document}

    Review Feedback:
    {review_feedback}

    Your tasks:
    - Fix grammatical and stylistic issues
    - Improve readability and structure
    - Ensure consistent formatting
    - Summarize complex sections if needed

    Provide a refined version of the document.
    """
    response = llm.invoke([SystemMessage(content=prompt)])
    memory.save_context({"role": "Editor-Agent"}, {"content": response.content})
    return response.content

def publisher_agent(final_document):
    """Prepares and formats the document for publishing."""
    prompt = f"""
    You are responsible for formatting and publishing the architectural document.

    Document:
    {final_document}

    - Ensure all figures, tables, and diagrams are properly formatted
    - Apply branding if required
    - Provide a final version ready for publishing

    Return the formatted version.
    """
    response = llm.invoke([SystemMessage(content=prompt)])
    memory.save_context({"role": "Publisher-Agent"}, {"content": response.content})
    return response.content

def coordinator_agent(project_details):
    """Manages the workflow between agents."""
    print("📌 Starting Architectural Documentation Process...")

    # 1. Architect Agent Generates the Document
    print("\n📝 Architect-Agent: Generating initial documentation...")
    initial_doc = architect_agent(project_details)
    
    # 2. Reviewer Agent Reviews the Document
    print("\n🔍 Reviewer-Agent: Reviewing the document...")
    review_feedback = reviewer_agent(initial_doc)

    # 3. Editor Agent Refines the Document
    print("\n✍️ Editor-Agent: Editing the document...")
    final_doc = editor_agent(initial_doc, review_feedback)

    # 4. Publisher Agent Publishes the Document
    print("\n📤 Publisher-Agent: Publishing the final document...")
    published_doc = publisher_agent(final_doc)

    print("\n✅ Documentation Process Completed!")
    return published_doc

# ===========================
# Run the Multi-Agent System
# ===========================

if __name__ == "__main__":
    project_info = """
    Project Name: AI-Powered Building Design
    Scope: A cloud-based system for architects to design buildings using AI.
    Technology Stack: Python, AWS, LangChain, OpenAI, React
    Requirements: Scalable, Secure, Multi-user collaboration, AI-based recommendations
    Industry Standards: TOGAF, Microservices Best Practices
    """
    
    final_output = coordinator_agent(project_info)
    with open("GeneratedDocs/AgentTeamDoc.md", "w", encoding="utf-8") as f:
        f.write(final_output)


