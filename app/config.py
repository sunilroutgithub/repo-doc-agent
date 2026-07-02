import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    HUGGINGFACE_TOKEN: str = os.getenv("HUGGINGFACE_TOKEN")
    TARGET_REPO: str = os.getenv("TARGET_REPO")

settings = Settings()
