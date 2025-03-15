# review_documentation.py
import os
import argparse
from langchain_openai import OpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from config import API_KEY, ANTHROPIC_API_KEY, LLM_PROVIDER


def load_agent_prompts(prompts_dir="agent_prompts"):
    """
    Loads prompt files from the specified directory and returns a dictionary mapping
    the perspective (filename without extension) to the prompt content.
    """
    agent_prompts = {}
    for filename in os.listdir(prompts_dir):
        if filename.endswith(".txt") and filename != "consolidate_prompt.txt":
            perspective = os.path.splitext(filename)[0]
            with open(os.path.join(prompts_dir, filename), "r", encoding="utf-8") as f:
                prompt_text = f.read()
            agent_prompts[perspective] = prompt_text
    return agent_prompts


def get_llm(model_provider=None):
    """
    Initialize the language model based on the provider.
    
    Args:
        model_provider (str, optional): The model provider to use ('openai' or 'anthropic').
                                      If None, uses the LLM_PROVIDER from environment.
        
    Returns:
        LLM: The language model instance
        
    Raises:
        ValueError: If the model provider is not supported
    """
    # Use environment variable if no provider is specified
    provider = (model_provider or LLM_PROVIDER).lower()
    
    if provider == "openai":
        if not API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in the environment")
        return OpenAI(temperature=0, openai_api_key=API_KEY)
    elif provider == "anthropic":
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is not set in the environment")
        return ChatAnthropic(temperature=0, anthropic_api_key=ANTHROPIC_API_KEY, model="claude-2")
    else:
        raise ValueError(f"Unsupported model provider: {provider}. Use 'openai' or 'anthropic'.")


def review_document(markdown_text, model_provider=None):
    """
    Uses LangChain to review the markdown document from various perspectives
    and consolidates the reviews into actionable improvement suggestions.
    
    Args:
        markdown_text (str): The text to review
        model_provider (str, optional): The model provider to use ('openai' or 'anthropic').
                                      If None, uses the LLM_PROVIDER from environment.
    """
    # Initialize the LLM
    try:
        llm = get_llm(model_provider)
    except ValueError as e:
        print(f"Error: {e}")
        return None, None
    except Exception as e:
        print(f"Error initializing model: {e}")
        return None, None

    # Load the agent-specific prompts
    agent_prompts = load_agent_prompts()

    reviews = {}
    for perspective, prompt_text in agent_prompts.items():
        # Create a prompt template. The prompt text should include a placeholder {document}
        prompt = PromptTemplate(template=prompt_text, input_variables=["document"])
        
        # Use the new invoke method instead of run
        provider_name = model_provider or LLM_PROVIDER
        print(f"Running review for {perspective} using {provider_name} ...")
        review = llm.invoke(prompt.format(document=markdown_text))
        reviews[perspective] = review

    # Load consolidation prompt from a file for combining the reviews
    consolidation_prompt_file = os.path.join("agent_prompts", "consolidate_prompt.txt")
    if os.path.exists(consolidation_prompt_file):
        with open(consolidation_prompt_file, "r", encoding="utf-8") as f:
            consolidation_prompt_text = f.read()
    else:
        consolidation_prompt_text = """Based on the following reviews, please provide a consolidated summary that includes constructive, actionable improvements for the document:

{reviews}

Please provide a clear, organized summary of the key improvements needed."""

    # Combine the various reviews into one string
    consolidated_reviews = "\n\n".join([f"{k} Review:\n{v}" for k, v in reviews.items()])

    # Create and invoke the consolidation prompt
    consolidation_prompt = PromptTemplate(template=consolidation_prompt_text, input_variables=["reviews"])
    final_improvements = llm.invoke(consolidation_prompt.format(reviews=consolidated_reviews))

    return reviews, final_improvements
