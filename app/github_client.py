```python
# app/github_client.py

from github import Github
from app.config import settings
import pytest

class GitHubClient:
    """
    A client for interacting with the GitHub API.

    Attributes:
        client (Github): The GitHub client instance.
    """

    def __init__(self):
        """
        Initializes the GitHub client with a token from the settings.

        Raises:
            ValueError: If the GITHUB_TOKEN is not set in the settings.
        """
        if not settings.GITHUB_TOKEN:
            raise ValueError("GITHUB_TOKEN must be set in the settings")
        self.client = Github(settings.GITHUB_TOKEN)

    def get_repo(self, repo_path: str = None) -> 'Repository':
        """
        Retrieves a GitHub repository.

        Args:
            repo_path (str, optional): The path to the repository. Defaults to TARGET_REPO from the settings.

        Returns:
            Repository: The retrieved repository.
        """
        return self.client.get_repo(repo_path or settings.TARGET_REPO)

    def create_branch(self, repo, branch_name: str, base: str = "main") -> 'GitRef':
        """
        Creates a new branch in a repository.

        Args:
            repo (Repository): The repository to create the branch in.
            branch_name (str): The name of the new branch.
            base (str, optional): The base branch to create the new branch from. Defaults to "main".

        Returns:
            GitRef: The created branch reference.
        """
        base_ref = repo.get_branch(base)
        return repo.create_git_ref(
            ref=f"refs/heads/{branch_name}",
            sha=base_ref.commit.sha
        )

    def create_pull_request(self, repo, title: str, body: str, head: str, base: str = "main") -> 'PullRequest':
        """
        Creates a new pull request in a repository.

        Args:
            repo (Repository): The repository to create the pull request in.
            title (str): The title of the pull request.
            body (str): The body of the pull request.
            head (str): The head of the pull request.
            base (str, optional): The base branch to create the pull request from. Defaults to "main".

        Returns:
            PullRequest: The created pull request.
        """

def test_github_client_init():
    """Tests that the GitHub client can be initialized with a token."""
    settings.GITHUB_TOKEN = "test_token"
    client = GitHubClient()
    assert client.client.login == "test_token"

def test_github_client_get_repo():
    """Tests that the GitHub client can retrieve a repository."""
    settings.GITHUB_TOKEN = "test_token"
    client = GitHubClient()
    repo = client.get_repo()
    assert isinstance(repo, type(client.client.get_repo("test_repo")))

def test_github_client_create_branch():
    """Tests that the GitHub client can create a new branch."""
    settings.GITHUB_TOKEN = "test_token"
    client = GitHubClient()
    repo = client.get_repo()
    branch = client.create_branch(repo, "test_branch")
    assert isinstance(branch, type(client.client.get_repo("test_repo").create_git_ref()))

def test_github_client_create_pull_request():
    """Tests that the GitHub client can create a new pull request."""
    settings.GITHUB_TOKEN = "test_token"
    client = GitHubClient()
    repo = client.get_repo()
    pull_request = client.create_pull_request(repo, "test_title", "test_body", "test_head")
    assert isinstance(pull_request, type(client.client.get_repo("test_repo").create_pull()))
```