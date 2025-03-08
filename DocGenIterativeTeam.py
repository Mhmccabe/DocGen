import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI 
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory  
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Load API key from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the LLM (using OpenAI's GPT-4)
llm = ChatOpenAI(model_name="gpt-4", temperature=0.7, api_key=openai_api_key)

# ----------------------------
# Architect Chain: Initial Document Generation
# ----------------------------
architect_template = """
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
architect_prompt = ChatPromptTemplate(
    input_variables=["project_details"],
    template=architect_template
)
architect_chain = LLMChain(llm=llm, prompt=architect_prompt)

# ----------------------------
# Reviewer Chains: Each returns feedback ending with a quality marker
# ----------------------------
general_review_template = """
You are a seasoned architectural reviewer.
Review the following document for overall technical accuracy, best practices, and clarity.
Document:
{document}

Provide detailed feedback and end with exactly:
"General Quality: HIGH" if the document is satisfactory, or "General Quality: LOW" if improvements are needed.
"""
general_review_prompt = ChatPromptTemplate(
    input_variables=["document"],
    template=general_review_template
)
general_review_chain = LLMChain(llm=llm, prompt=general_review_prompt)

security_review_template = """
You are a security architect.
Review the following document for security vulnerabilities and secure design best practices.
Document:
{document}

Provide detailed feedback and conclude with exactly:
"Security Quality: HIGH" if the document meets security standards, or "Security Quality: LOW" otherwise.
"""
security_review_prompt = ChatPromptTemplate(
    input_variables=["document"],
    template=security_review_template
)
security_review_chain = LLMChain(llm=llm, prompt=security_review_prompt)

infrastructure_review_template = """
You are an infrastructure architect.
Review the following document for deployment strategies, scalability, and infrastructure best practices.
Document:
{document}

Provide detailed feedback and conclude with exactly:
"Infrastructure Quality: HIGH" if the document is well-designed for infrastructure, or "Infrastructure Quality: LOW" if improvements are necessary.
"""
infrastructure_review_prompt = ChatPromptTemplate(
    input_variables=["document"],
    template=infrastructure_review_template
)
infrastructure_review_chain = LLMChain(llm=llm, prompt=infrastructure_review_prompt)

data_review_template = """
You are a data architect.
Review the following document for data architecture, database design, and data flow best practices.
Document:
{document}

Provide detailed feedback and conclude with exactly:
"Data Quality: HIGH" if the document meets data architecture standards, or "Data Quality: LOW" otherwise.
"""
data_review_prompt = ChatPromptTemplate(
    input_variables=["document"],
    template=data_review_template
)
data_review_chain = LLMChain(llm=llm, prompt=data_review_prompt)

compliance_review_template = """
You are a compliance officer.
Review the following document for regulatory compliance, risk management, and adherence to industry standards.
Document:
{document}

Provide detailed feedback and conclude with exactly:
"Compliance Quality: HIGH" if the document meets compliance standards, or "Compliance Quality: LOW" if not.
"""
compliance_review_prompt = ChatPromptTemplate(
    input_variables=["document"],
    template=compliance_review_template
)
compliance_review_chain = LLMChain(llm=llm, prompt=compliance_review_prompt)

# ----------------------------
# Editor Chain: Revise the document based on aggregated feedback
# ----------------------------
editor_template = """
You are a technical editor.
Original Document:
{document}

Aggregated Review Feedback:
{aggregated_feedback}

Revise the document to address all the feedback. Provide a revised version that improves clarity, technical accuracy, security, infrastructure design, data architecture, and compliance.
"""
editor_prompt = ChatPromptTemplate(
    input_variables=["document", "aggregated_feedback"],
    template=editor_template
)
editor_chain = LLMChain(llm=llm, prompt=editor_prompt)

# ----------------------------
# Publisher Chain: Final formatting
# ----------------------------
publisher_template = """
You are responsible for formatting and finalizing the architectural document for publication.
Document:
{document}

Convert the document into a professionally formatted version ready for distribution.
"""
publisher_prompt = ChatPromptTemplate(
    input_variables=["document"],
    template=publisher_template
)
publisher_chain = LLMChain(llm=llm, prompt=publisher_prompt)

# ----------------------------
# Iterative Review Process
# ----------------------------
def iterative_review(project_details: str, max_iterations: int = 5):
    # Step 1: Generate the initial document
    state = {}
    state["project_details"] = project_details
    state["document"] = architect_chain.run(project_details=project_details)
    iteration = 1
    print(f"Initial document generated:\n{state['document']}\n{'-'*60}\n")
    
    # Iteratively review and edit until all feedback is high quality
    while iteration <= max_iterations:
        print(f"Iteration {iteration}:")
        
        # Run each reviewer chain
        general_feedback = general_review_chain.run(document=state["document"])
        security_feedback = security_review_chain.run(document=state["document"])
        infrastructure_feedback = infrastructure_review_chain.run(document=state["document"])
        data_feedback = data_review_chain.run(document=state["document"])
        compliance_feedback = compliance_review_chain.run(document=state["document"])
        
        print("General Review:", general_feedback)
        print("Security Review:", security_feedback)
        print("Infrastructure Review:", infrastructure_feedback)
        print("Data Review:", data_feedback)
        print("Compliance Review:", compliance_feedback)
        
        # Check if all reviews indicate HIGH quality
        if (
            "General Quality: HIGH" in general_feedback and
            "Security Quality: HIGH" in security_feedback and
            "Infrastructure Quality: HIGH" in infrastructure_feedback and
            "Data Quality: HIGH" in data_feedback and
            "Compliance Quality: HIGH" in compliance_feedback
        ):
            print("All reviews are high quality. Proceeding to publish.\n")
            state["document"] = publisher_chain.run(document=state["document"])
            break
        else:
            # Aggregate all feedback for editing
            aggregated_feedback = "\n".join([
                general_feedback,
                security_feedback,
                infrastructure_feedback,
                data_feedback,
                compliance_feedback
            ])
            # Edit the document based on aggregated feedback
            state["document"] = editor_chain.run(document=state["document"], aggregated_feedback=aggregated_feedback)
            iteration += 1
            print("Document edited. Re-reviewing...\n" + "-"*60 + "\n")
    
    state["iteration"] = iteration
    return state

# ----------------------------
# Run the iterative process
# ----------------------------
if __name__ == "__main__":
    project_info = (
        "Project Name: AI-Powered Building Design\n"
        "Scope: A cloud-based system for architects to design buildings using AI.\n"
        "Technology Stack: Python, AWS, LangChain, OpenAI, React\n"
        "Requirements: Scalable, Secure, Multi-user collaboration, AI-based recommendations\n"
        "Industry Standards: TOGAF, Microservices Best Practices"
    )
    final_state = iterative_review(project_info)
    print("✅ Multi-Reviewer Documentation Process Completed!")
    print("\nFinal Document Output:\n")
    print(final_state["document"])
    print("\nTotal Iterations:", final_state["iteration"])
