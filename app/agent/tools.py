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
        """
        client = GitHubClient()
        repo = client.get_repo(repo_path)
        
        try:
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
    
    assert hasattr(tool_func, 'name')
    assert hasattr(tool_func, 'description')
    assert tool_func.name == "write_file_and_commit"


@patch('app.agent.tools.GitHubClient')
def test_write_file_and_commit_success(mock_github_client):
    """Test successful file write and commit."""
    mock_repo = Mock()
    mock_repo.create_file.return_value = Mock()
    mock_client = Mock()
    mock_client.get_repo.return_value = mock_repo
    mock_github_client.return_value = mock_client
    
    tool_func = make_write_file_tool("test/repo")
    result = tool_func.invoke({
        "branch": "main",
        "path": "path/file.txt",
        "content": "content",
        "commit_msg": "commit msg"
    })
    
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
    mock_repo = Mock()
    mock_repo.create_file.side_effect = Exception("API failure")
    mock_client = Mock()
    mock_client.get_repo.return_value = mock_repo
    mock_github_client.return_value = mock_client
    
    tool_func = make_write_file_tool("test/repo")
    result = tool_func.invoke({
        "branch": "main",
        "path": "path/file.txt",
        "content": "content",
        "commit_msg": "commit msg"
    })
    
    assert "Error writing file: API failure" in result


if __name__ == "__main__":
    pytest.main([__file__])