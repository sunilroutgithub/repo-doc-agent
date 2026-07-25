from langchain.tools import tool
from app.github_client import GitHubClient


def make_write_file_tool(repo_path: str):
    """Return a write_file_and_commit tool with repo_path hardcoded via closure."""

    @tool
    def write_file_and_commit(branch: str, path: str, content: str, commit_msg: str) -> str:
        """Write content to a file and commit it to a branch. Arguments: branch (the branch name to write to), path (file path in the repo), content (full file content), commit_msg (commit message)."""
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
