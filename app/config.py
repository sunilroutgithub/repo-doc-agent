import os
from dotenv import load_dotenv
import pytest

load_dotenv()

class Settings:
    """
    A class to hold application settings.

    Attributes:
        GITHUB_TOKEN (str): The GitHub token for API access.
        GROQ_API_KEY (str): The GROQ API key for data access.
        HUGGINGFACE_TOKEN (str): The Hugging Face token for API access.
        TARGET_REPO (str): The target repository for GitHub API access.
    """

    def __init__(self):
        """
        Initializes the Settings class.

        Raises:
            ValueError: If any environment variable is not set.
        """
        self.GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        self.HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
        self.TARGET_REPO = os.getenv("TARGET_REPO")

        if not all([self.GITHUB_TOKEN, self.GROQ_API_KEY, self.HUGGINGFACE_TOKEN, self.TARGET_REPO]):
            raise ValueError("One or more environment variables are not set.")


def test_settings_init():
    """
    Tests the Settings class initialization.

    Raises:
        ValueError: If the test fails.
    """
    try:
        settings = Settings()
    except ValueError as e:
        pytest.fail(str(e))


def test_settings_attributes():
    """
    Tests the Settings class attributes.

    Raises:
        AssertionError: If any attribute is not set correctly.
    """
    settings = Settings()
    assert settings.GITHUB_TOKEN
    assert settings.GROQ_API_KEY
    assert settings.HUGGINGFACE_TOKEN
    assert settings.TARGET_REPO


def test_settings_env_vars():
    """
    Tests the Settings class environment variables.

    Raises:
        AssertionError: If any environment variable is not set correctly.
    """
    settings = Settings()
    assert os.getenv("GITHUB_TOKEN") == settings.GITHUB_TOKEN
    assert os.getenv("GROQ_API_KEY") == settings.GROQ_API_KEY
    assert os.getenv("HUGGINGFACE_TOKEN") == settings.HUGGINGFACE_TOKEN
    assert os.getenv("TARGET_REPO") == settings.TARGET_REPO

settings = Settings()