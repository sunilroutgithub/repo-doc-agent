from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agent.crew import run_doc_crew
from app.github_client import GitHubClient
from app.config import settings
import time
import random

app = FastAPI(title="Repo Doc Agent")

class DocRequest(BaseModel):
    repo_path: str
    file_path: str

class DocResponse(BaseModel):
    pull_request_url: str
    message: str

@app.post("/generate-docs", response_model=DocResponse)
def generate_docs(request: DocRequest):
    try:
        # All GitHub calls use request.repo_path directly — never passed through the LLM
        client = GitHubClient()
        repo = client.get_repo(request.repo_path)

        # Read the file content here in Python, not via an LLM tool call
        file_content = repo.get_contents(request.file_path).decoded_content.decode("utf-8")

        # Create a unique branch name
        branch_name = f"docs-update-{int(time.time())}-{random.randint(1000, 9999)}"

        # Create the branch from the repo's default branch
        default_ref = repo.get_branch(repo.default_branch)
        repo.create_git_ref(
            ref=f"refs/heads/{branch_name}",
            sha=default_ref.commit.sha,
        )


                       # Multi-agent crew (Writer -> Reviewer -> Editor) generates the final file content
        final_content = run_doc_crew(request.file_path, file_content)

        # Write the crew's final output to the branch — deterministic, not LLM tool call
        from app.agent.tools import make_write_file_tool
        write_tool = make_write_file_tool(request.repo_path)
        write_tool.func(
            branch=branch_name,
            path=request.file_path,
            content=final_content,
            commit_msg=f"Add docstrings and tests to {request.file_path} (multi-agent crew)",
        )


        # Open the PR in Python — not via the LLM
        pr = repo.create_pull(
            title=f"Add docstrings and tests to {request.file_path}",
            body=f"Auto-generated documentation and unit tests for `{request.file_path}`.",
            head=branch_name,
            base=repo.default_branch,
        )

        return DocResponse(
            pull_request_url=pr.html_url,
            message=f"✅ PR created: {pr.html_url}",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"status": "ok", "service": "Repo Doc Agent"}

@app.get("/health")
def health():
    return {"status": "healthy", "target_repo": settings.TARGET_REPO}
