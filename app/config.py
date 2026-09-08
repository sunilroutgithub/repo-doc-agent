"""Application configuration module.

This module loads environment variables using :func:`dotenv.load_dotenv` and
provides a :class:`Settings` class that exposes the required configuration
values as attributes.  The module also contains a small test suite that can be
run with ``pytest`` to verify that the settings are loaded correctly.

The tests are intentionally lightweight and only check that the environment
variables are present and that the :class:`Settings` constructor raises a
:class:`ValueError` when any required variable is missing.
"""

import os
from dotenv import load_dotenv
import pytest

# Load environment variables from a .env file if present.
load_dotenv()


class Settings:
    """Container for application configuration.

    The class reads the following environment variables on instantiation:

    ``GITHUB_TOKEN``
        GitHub personal access token used for API requests.

    ``GROQ_API_KEY``
        API key for the GROQ service.

    ``HUGGINGFACE_TOKEN``
        Hugging Face authentication token.

    ``TARGET_REPO``
        The GitHub repository (``owner/repo``) that the application will
        interact with.

    Raises
    ------
    ValueError
        If any of the required environment variables are missing.
    """

    def __init__(self) -> None:
        """Read required environment variables.

        The constructor pulls the values from :mod:`os.environ`.  If any of
        the variables are not set, a :class:`ValueError` is raised.
        """
        self.GITHUB_TOKEN: str | None = os.getenv("GITHUB_TOKEN")
        self.GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")
        self.HUGGINGFACE_TOKEN: str | None = os.getenv("HUGGINGFACE_TOKEN")
        self.TARGET_REPO: str | None = os.getenv("TARGET_REPO")

        if not all([
            self.GITHUB_TOKEN,
            self.GROQ_API_KEY,
            self.HUGGINGFACE_TOKEN,
            self.TARGET_REPO,
        ]):
            raise ValueError("One or more environment variables are not set.")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_settings_init() -> None:
    """Verify that :class:`Settings` can be instantiated when all env vars are set.

    The test simply constructs a :class:`Settings` instance and ensures that no
    exception is raised.
    """
    try:
        Settings()
    except ValueError as e:
        pytest.fail(str(e))


def test_settings_attributes() -> None:
    """Check that the attributes of :class:`Settings` are truthy.

    The test asserts that each attribute is set to a non‑empty string.
    """
    settings = Settings()
    assert settings.GITHUB_TOKEN
    assert settings.GROQ_API_KEY
    assert settings.HUGGINGFACE_TOKEN
    assert settings.TARGET_REPO


def test_settings_env_vars() -> None:
    """Ensure that the attributes match the values in :mod:`os.environ`.

    This test compares each attribute to the corresponding environment
    variable to confirm that the values are read correctly.
    """
    settings = Settings()
    assert os.getenv("GITHUB_TOKEN") == settings.GITHUB_TOKEN
    assert os.getenv("GROQ_API_KEY") == settings.GROQ_API_KEY
    assert os.getenv("HUGGINGFACE_TOKEN") == settings.HUGGINGFACE_TOKEN
    assert os.getenv("TARGET_REPO") == settings.TARGET_REPO


def test_settings_missing_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that a missing environment variable triggers a :class:`ValueError`.

    The test temporarily removes ``GITHUB_TOKEN`` from the environment and
    asserts that constructing :class:`Settings` raises a :class:`ValueError`.
    """
    # Preserve original value
    original_token = os.getenv("GITHUB_TOKEN")
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    with pytest.raises(ValueError):
        Settings()
    # Restore original value for any subsequent tests
    if original_token is not None:
        monkeypatch.setenv("GITHUB_TOKEN", original_token)

# Instantiate a Settings object for potential use in other modules.
settings = Settings()
