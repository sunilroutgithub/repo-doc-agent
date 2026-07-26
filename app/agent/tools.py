```python
from langchain.tools import tool
from app.github_client import GitHubClient
import pytest

def make_write_file_tool(repo_path: str):
    """
    Return a write_file_and_commit tool with repo_path hardcoded via closure.

    Args:
        repo_path (str): The path to the GitHub repository.

    Returns:
        A write_file_and_commit tool.
    """
    @tool
    def write_file_and_commit(branch: str, path: str, content: str, commit_msg: str) -> str:
        """
        Write content to a file and commit it to a branch.

        Args:
            branch (str): The branch name to write to.
            path (str): The file path in the repository.
            content (str): The full file content.
            commit_msg (str): The commit message.

        Returns:
            A success message if the file is written and committed, or an error message if not.

        Raises:
            Exception: If an error occurs while writing the file or committing the changes.
        """
        client = GitHubClient()
        repo = client.get_repo(repo_path)  # repo_path from closure — not from LLM

        try:
            # Ensure branch exists
            try:
                repo.get_branch(branch)
            except Exception:
                main_ref = repo.get_branch(repo.default_branch)
                repo.create_git_ref(
                    ref=f"refs/heads/{branch}",
                    sha=main_ref.commit.sha,
                )

            # Update existing file or create new one
            try:
                existing = repo.get_contents(path, ref=branch)
                repo.update_file(path, commit_msg, content, existing.sha, branch=branch)
            except Exception:
                repo.create_file(path, commit_msg, content, branch=branch)

            return f"File {path} written to branch {branch}"
        except Exception as e:
            return f"Error writing file: {str(e)}"

    return write_file_and_commit


def test_make_write_file_tool():
    """Test the make_write_file_tool function."""
    repo_path = "https://github.com/user/repo"
    tool = make_write_file_tool(repo_path)
    assert isinstance(tool, tool)


def test_write_file_and_commit():
    """Test the write_file_and_commit function."""
    repo_path = "https://github.com/user/repo"
    tool = make_write_file_tool(repo_path)
    result = tool("main", "path/to/file", "content", "commit message")
    assert isinstance(result, str)


def test_write_file_and_commit_error():
    """Test the write_file_and_commit function with an error."""
    repo_path = "https://github.com/user/repo"
    tool = make_write_file_tool(repo_path)
    result = tool("main", "path/to/file", "content", "commit message")
    assert "Error writing file:" in result


def test_write_file_and_commit_branch_not_found():
    """Test the write_file_and_commit function with a branch not found."""
    repo_path = "https://github.com/user/repo"
    tool = make_write_file_tool(repo_path)
    result = tool("non-existent-branch", "path/to/file", "content", "commit message")
    assert "Error writing file:" in result

if __name__ == "__main__":
    pytest.main([__file__])
```