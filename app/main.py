from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agent.react_agent import create_doc_agent
from app.agent.prompts import SYSTEM_PROMPT
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
        agent = create_doc_agent()
        
        # Create a unique branch name with timestamp + random number
        branch_name = f"docs-update-{int(time.time())}-{random.randint(1000, 9999)}"
        
        # First, create the branch
        from app.github_client import GitHubClient
        client = GitHubClient()
        repo = client.get_repo()
        
        # Create branch from main
        main_ref = repo.get_branch("main")
        repo.create_git_ref(
            ref=f"refs/heads/{branch_name}",
            sha=main_ref.commit.sha
        )
        
        # Invoke the agent to read and update the file
        result = agent.invoke({
            "messages": [
                ("system", SYSTEM_PROMPT),
                ("user", f"""
Task: 
1. Read file {request.file_path} from branch main
2. Add docstrings to all functions and classes
3. **Generate pytest unit tests** for all functions and classes
4. Write the updated content to branch {branch_name}
5. Create a pull request from {branch_name} to main

File path: {request.file_path}
Branch to write to: {branch_name}
""")
            ]
        })
        
        # Create the PR
        pr = repo.create_pull(
            title=f"Add docstrings and tests to {request.file_path}",
            body=f"Auto-generated documentation and unit tests for {request.file_path}",
            head=branch_name,
            base="main"
        )
        
        return DocResponse(
            pull_request_url=pr.html_url,
            message=f"✅ PR with docstrings and tests created! Check {pr.html_url}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "healthy", "target_repo": settings.TARGET_REPO}