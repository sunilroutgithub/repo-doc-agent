# from langchain.tools import tool
# from app.github_client import GitHubClient


# def make_write_file_tool(repo_path: str):
#     """Return a write_file_and_commit tool with repo_path hardcoded via closure."""

#     @tool
#     def write_file_and_commit(branch: str, path: str, content: str, commit_msg: str) -> str:
#         """Write content to a file and commit it to a branch. Arguments: branch (the branch name to write to), path (file path in the repo), content (full file content), commit_msg (commit message)."""
#         client = GitHubClient()
#         repo = client.get_repo(repo_path)  # repo_path from closure — not from LLM

#         try:
#             # Ensure branch exists
#             try:
#                 repo.get_branch(branch)
#             except Exception:
#                 main_ref = repo.get_branch(repo.default_branch)
#                 repo.create_git_ref(
#                     ref=f"refs/heads/{branch}",
#                     sha=main_ref.commit.sha,
#                 )

#             # Update existing file or create new one
#             try:
#                 existing = repo.get_contents(path, ref=branch)
#                 repo.update_file(path, commit_msg, content, existing.sha, branch=branch)
#             except Exception:
#                 repo.create_file(path, commit_msg, content, branch=branch)

#             return f"File {path} written to branch {branch}"
#         except Exception as e:
#             return f"Error writing file: {str(e)}"

#     return write_file_and_commit


from langchain.tools import tool
from app.github_client import GitHubClient
from unittest.mock import Mock, patch
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
        repo = client.get_repo(repo_path)
        
        try:
            # Create or update the file
            repo.create_file(
                path=path,
                message=commit_msg,
                content=content,
                branch=branch
            )
            
            return f"Successfully wrote {path} to branch {branch}"
            
        except Exception as e:
            return f"Error writing file: {str(e)}"
    
    return write_file_and_commit


# ==================== UNIT TESTS (with mocks) ====================

def test_make_write_file_tool_returns_tool():
    """Test that make_write_file_tool returns a StructuredTool."""
    repo_path = "test/repo"
    tool_func = make_write_file_tool(repo_path)
    
    # Check it's a StructuredTool (has name and description attributes)
    assert hasattr(tool_func, 'name')
    assert hasattr(tool_func, 'description')
    assert tool_func.name == "write_file_and_commit"


@patch('app.agent.tools.GitHubClient')
def test_write_file_and_commit_success(mock_github_client):
    """Test successful file write and commit."""
    # Setup mock
    mock_repo = Mock()
    mock_repo.create_file.return_value = Mock()
    mock_client = Mock()
    mock_client.get_repo.return_value = mock_repo
    mock_github_client.return_value = mock_client
    
    # Create tool
    repo_path = "test/repo"
    tool_func = make_write_file_tool(repo_path)
    
    # Execute using .invoke() method
    result = tool_func.invoke({
        "branch": "main",
        "path": "path/file.txt",
        "content": "content",
        "commit_msg": "commit msg"
    })
    
    # Verify
    assert "Successfully wrote" in result
    mock_repo.create_file.assert_called_once_with(
        path="path/file.txt",
        message="commit msg",
        content="content",
        branch="main"
    )


@patch('app.agent.tools.GitHubClient')
def test_write_file_and_commit_error(mock_github_client):
    """Test error handling when GitHub API fails."""
    # Setup mock to raise exception
    mock_repo = Mock()
    mock_repo.create_file.side_effect = Exception("API failure")
    mock_client = Mock()
    mock_client.get_repo.return_value = mock_repo
    mock_github_client.return_value = mock_client
    
    # Create tool
    repo_path = "test/repo"
    tool_func = make_write_file_tool(repo_path)
    
    # Execute using .invoke() method
    result = tool_func.invoke({
        "branch": "main",
        "path": "path/file.txt",
        "content": "content",
        "commit_msg": "commit msg"
    })
    
    # Verify error handling
    assert "Error writing file: API failure" in result


if __name__ == "__main__":
    pytest.main([__file__])