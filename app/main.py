from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.github_client import GitHubClient
from app.config import settings
import time
import random

app = FastAPI(title="Repo Doc Agent")

class DocRequest(BaseModel):
    repo_path: str | None = None
    file_path: str

class DocResponse(BaseModel):
    pull_request_url: str
    message: str


def _github_error_detail(stage: str, repo_path: str, file_path: str, error: Exception) -> str:
    """Return an actionable, secret-safe message for a GitHub API failure."""
    status = getattr(error, "status", None)

    if status == 404:
        if stage == "repository lookup":
            return (
                f"GitHub returned 404 while looking up repository {repo_path!r}. "
                "Check the owner/repository spelling and capitalization. GitHub also "
                "returns 404 when a token cannot access a private repository."
            )
        if stage == "file lookup":
            return (
                f"GitHub found repository {repo_path!r}, but returned 404 for file "
                f"{file_path!r}. Check the path and capitalization; paths are relative "
                "to the repository root and must exist on its default branch."
            )
        return (
            f"GitHub returned 404 during {stage} for repository {repo_path!r}. "
            "Verify that the token has access to the repository and that the requested "
            "resource exists."
        )

    if status in (401, 403):
        permission = {
            "branch creation": "Contents: Read and write",
            "file lookup": "Contents: Read",
            "pull request creation": "Pull requests: Read and write",
        }.get(stage, "access to the selected repository")
        return (
            f"GitHub rejected the {stage} request with HTTP {status}. "
            f"Check that the token has {permission}, is stored in the Replit "
            "Shared or Production Secrets environment, and that organization SSO "
            "authorization is complete if applicable."
        )

    return f"GitHub {stage} failed for repository {repo_path!r}: {error}"


@app.post("/generate-docs", response_model=DocResponse)
def generate_docs(request: DocRequest):
    repo_path = (request.repo_path or settings.TARGET_REPO or "").strip()
    file_path = request.file_path.strip().lstrip("/")

    try:
        # All GitHub calls use request.repo_path directly — never passed through the LLM
        client = GitHubClient()
        try:
            repo = client.get_repo(repo_path)
        except Exception as e:
            raise HTTPException(
                status_code=502,
                detail=_github_error_detail(
                    "repository lookup", repo_path, file_path, e
                ),
            ) from e

        # Read the file content here in Python, not via an LLM tool call
        try:
            file_content = repo.get_contents(file_path).decoded_content.decode("utf-8")
        except Exception as e:
            raise HTTPException(
                status_code=502,
                detail=_github_error_detail("file lookup", repo_path, file_path, e),
            ) from e

        # Create a unique branch name
        branch_name = f"docs-update-{int(time.time())}-{random.randint(1000, 9999)}"

        # Create the branch from the repo's default branch
        try:
            default_ref = repo.get_branch(repo.default_branch)
            repo.create_git_ref(
                ref=f"refs/heads/{branch_name}",
                sha=default_ref.commit.sha,
            )
        except Exception as e:
            raise HTTPException(
                status_code=502,
                detail=_github_error_detail(
                    "branch creation", repo_path, file_path, e
                ),
            ) from e


                       # Lazy import — crewai/torch/sentence-transformers load on first request, not at startup
        from app.agent.crew import run_doc_crew

        # Multi-agent crew (Writer -> Reviewer -> Editor) generates the final file content
        final_content = run_doc_crew(request.file_path, file_content)

        # Write the crew's final output to the branch — deterministic, not LLM tool call
        from app.agent.tools import make_write_file_tool
        write_tool = make_write_file_tool(repo_path)
        write_tool.func(
            branch=branch_name,
            path=file_path,
            content=final_content,
            commit_msg=f"Add docstrings and tests to {file_path} (multi-agent crew)",
        )


        # Open the PR in Python — not via the LLM
        try:
            pr = repo.create_pull(
                title=f"Add docstrings and tests to {file_path}",
                body=f"Auto-generated documentation and unit tests for `{file_path}`.",
                head=branch_name,
                base=repo.default_branch,
            )
        except Exception as e:
            raise HTTPException(
                status_code=502,
                detail=_github_error_detail(
                    "pull request creation", repo_path, file_path, e
                ),
            ) from e

        return DocResponse(
            pull_request_url=pr.html_url,
            message=f"✅ PR created: {pr.html_url}",
        )

    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"status": "ok", "service": "Repo Doc Agent"}

@app.get("/health")
def health():
    return {"status": "healthy", "target_repo": settings.TARGET_REPO}
