from langchain.tools import tool
from app.github_client import GitHubClient
from app.config import settings

@tool
def read_file(repo_path: str, file_path: str) -> str:
    """Read a file from the target GitHub repository."""
    client = GitHubClient()
    repo = client.get_repo()
    try:
        content = repo.get_contents(file_path, ref=repo_path)
        return content.decoded_content.decode("utf-8")
    except Exception as e:
        return f"Error reading file: {str(e)}"

@tool
def create_pull_request(branch_name: str, title: str, body: str) -> str:
    """Create a pull request from a branch."""
    client = GitHubClient()
    repo = client.get_repo()
    try:
        pr = repo.create_pull(
            title=title,
            body=body,
            head=branch_name,
            base="main"
        )
        return f"PR created: {pr.html_url}"
    except Exception as e:
        return f"Error creating PR: {str(e)}"

@tool
def write_file_and_commit(branch: str, path: str, content: str, commit_msg: str) -> str:
    """Write content to a file and commit it to a branch."""
    client = GitHubClient()
    repo = client.get_repo()
    
    try:
        # Check if branch exists, if not create it
        try:
            repo.get_branch(branch)
        except:
            # Create branch from main
            main_ref = repo.get_branch("main")
            repo.create_git_ref(
                ref=f"refs/heads/{branch}",
                sha=main_ref.commit.sha
            )
        
        # Try to update existing file or create new one
        try:
            file = repo.get_contents(path, ref=branch)
            repo.update_file(path, commit_msg, content, file.sha, branch=branch)
        except:
            repo.create_file(path, commit_msg, content, branch=branch)
        
        return f"File {path} updated on branch {branch}"
    except Exception as e:
        return f"Error writing file: {str(e)}"