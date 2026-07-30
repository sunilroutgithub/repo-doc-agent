import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    A class to hold application settings.

    Attributes:
        GITHUB_TOKEN (str): The GitHub token.
        GROQ_API_KEY (str): The Groq API key.
        HUGGINGFACE_TOKEN (str): The Hugging Face token.
        TARGET_REPO (str): The target repository.
    """
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    HUGGINGFACE_TOKEN: str = os.getenv("HUGGINGFACE_TOKEN")
    TARGET_REPO: str = os.getenv("TARGET_REPO")

settings = Settings()
