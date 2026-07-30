import pytest

def test_Settings_class():
    # Test that the Settings class is defined
    assert Settings is not None

def test_Settings_attributes():
    # Test that the Settings class has the correct attributes
    settings = Settings()
    assert hasattr(settings, 'GITHUB_TOKEN')
    assert hasattr(settings, 'GROQ_API_KEY')
    assert hasattr(settings, 'HUGGINGFACE_TOKEN')
    assert hasattr(settings, 'TARGET_REPO')

def test_load_dotenv():
    # Test that load_dotenv function loads environment variables correctly
    assert os.getenv('GITHUB_TOKEN') is not None
    assert os.getenv('GROQ_API_KEY') is not None
    assert os.getenv('HUGGINGFACE_TOKEN') is not None
    assert os.getenv('TARGET_REPO') is not None
