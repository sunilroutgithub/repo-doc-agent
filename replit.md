# Repo Doc Agent

An AI-powered FastAPI agent that automatically generates Google-style docstrings, pytest unit tests, and opens GitHub pull requests for Python code.

## Stack

- **FastAPI** — REST API server
- **LangChain + LangGraph** — ReAct agent framework
- **Groq LLM** (`llama-3.1-8b-instant`) — code analysis and generation
- **PyGithub** — GitHub API integration
- **uvicorn** — ASGI server

## How to run

The app starts automatically via the **Start application** workflow:

```
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

## Required secrets (set in Replit Secrets)

| Secret | Description |
|--------|-------------|
| `GITHUB_TOKEN` | Personal access token with `repo` scope |
| `GROQ_API_KEY` | From console.groq.com |
| `HUGGINGFACE_TOKEN` | From huggingface.co/settings/tokens |

## Required environment variables

| Variable | Description |
|----------|-------------|
| `TARGET_REPO` | GitHub repo to document, in `owner/repo` format |

## API endpoints

### `POST /generate-docs`

Generates docstrings and tests for a file in the target repo, then opens a PR.

```json
{
  "repo_path": "owner/repo",
  "file_path": "path/to/file.py"
}
```

Returns:
```json
{
  "pull_request_url": "https://github.com/...",
  "message": "✅ PR with docstrings and tests created!"
}
```

### `GET /health`

Returns service health status and the configured `TARGET_REPO`.

## User preferences

- Keep the project's existing structure and stack
