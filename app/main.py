"""
FastAPI application for automatically generating documentation and unit tests
for a specified file in a GitHub repository.

The application exposes three endpoints:

* ``/generate-docs`` – Creates a pull request that adds docstrings and
  pytest unit tests to a file.
* ``/health`` – Health check endpoint that reports the status of the
  service and the target repository.
* ``/`` – Root endpoint that returns a simple status message.

The module also contains a minimal set of pytest unit tests that exercise
the public API.  The tests use the :class:`fastapi.testclient.TestClient`
to make requests against the application and monkeypatch the external
dependencies so that no real network calls are performed.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agent.react_agent import create_doc_agent
from app.agent.prompts import SYSTEM_PROMPT
from app.github_client import GitHubClient
from app.config import settings
import time
import random

app = FastAPI(title="Repo Doc Agent")


class DocRequest(BaseModel):
    """
    Request model for the ``/generate-docs`` endpoint.

    Attributes
    ----------
    repo_path : str
        The path to the repository on GitHub.  This is currently unused
        because the :class:`GitHubClient` is configured globally via
        :mod:`app.config`, but the field is kept for future extensibility.
    file_path : str
        The path to the file within the repository that should be
        processed by the documentation agent.
    """

    repo_path: str
    file_path: str


class DocResponse(BaseModel):
    """
    Response model for the ``/generate-docs`` endpoint.

    Attributes
    ----------
    pull_request_url : str
        The URL of the created pull request on GitHub.
    message : str
        A human‑readable confirmation message.
    """

    pull_request_url: str
    message: str


@app.post("/generate-docs", response_model=DocResponse)
def generate_docs(request: DocRequest) -> DocResponse:
    """
    Generate documentation and unit tests for a file in a GitHub repository.

    The function performs the following steps:

    1. Creates a new branch from ``main`` with a unique name.
    2. Invokes the documentation agent to read the