from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agent.react_agent import create_doc_agent
from app.config import settings

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
        
        result = agent.invoke({
            "input": f"Read {request.file_path} from {request.repo_path}, add docstrings, create PR"
        })
        
        return DocResponse(
            pull_request_url=result.get("output", ""),
            message="Docstrings generated and PR created"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "healthy", "target_repo": settings.TARGET_REPO}