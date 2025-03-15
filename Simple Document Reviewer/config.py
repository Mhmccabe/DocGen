# config.py
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Make sure to set your API keys and provider in your .env file:
# OPENAI_API_KEY=your-openai-key
# ANTHROPIC_API_KEY=your-anthropic-key
# LLM_PROVIDER=openai (or anthropic)

API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()  # Default to OpenAI if not set

if LLM_PROVIDER not in ["openai", "anthropic"]:
    raise ValueError("LLM_PROVIDER must be either 'openai' or 'anthropic'")

if LLM_PROVIDER == "openai" and not API_KEY:
    raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER is set to 'openai'")
elif LLM_PROVIDER == "anthropic" and not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY is required when LLM_PROVIDER is set to 'anthropic'")
