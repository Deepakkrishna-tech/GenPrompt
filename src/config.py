# File: src/config.py
import os
from dotenv import load_dotenv

# This line correctly finds the .env file in the project's ROOT directory
# by going up two levels from src/config.py
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if not os.path.exists(dotenv_path):
    print(f"[Warning] .env file not found at {dotenv_path}. Make sure it exists in the project root.")
else:
    load_dotenv(dotenv_path=dotenv_path)

class Settings:
    """Manages application-wide configurations and API keys."""
    # Secrets loaded from .env
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    HUGGING_FACE_TOKEN: str = os.getenv("HUGGING_FACE_TOKEN")

    # Public Configurations
    VISION_MODEL_ID: str = "unum-cloud/smol-vlm"
    PARSER_LLM_ID: str = "gpt-4o"
    
settings = Settings()

# Validate that essential secrets are set
if not settings.OPENAI_API_KEY:
    raise ValueError("FATAL: OPENAI_API_KEY environment variable not set in .env file.")

# The HF token is optional for public models but good practice to have.
if not settings.HUGGING_FACE_TOKEN:
    print("[Warning] HUGGING_FACE_TOKEN is not set in the .env file.")