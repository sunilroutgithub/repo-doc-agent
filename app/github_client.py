from github import Auth, Github
from app.config import settings


class GitHubClient:
    def __init__(self):
        if not settings.GITHUB_TOKEN:
            raise RuntimeError(
                "GITHUB_TOKEN is not configured in Replit Secrets. "
                "Add it to the Shared or Production environment and republish."
            )
        self.client = Github(auth=Auth.Token(settings.GITHUB_TOKEN))

    def get_repo(self, repo_path: str = None):
        path = (repo_path or settings.TARGET_REPO or "").strip().strip("/")
        if not path or path.count("/") != 1:
            raise ValueError(
                "repo_path must use the GitHub owner/repository format, "
                f"for example 'sunilroutgithub/repo-doc-agent'; received {path!r}."
            )
        return self.client.get_repo(path)

    def create_branch(self, repo, branch_name, base="main"):
        base_ref = repo.get_branch(base)
        return repo.create_git_ref(
            ref=f"refs/heads/{branch_name}",
            sha=base_ref.commit.sha
        )
    
    def create_pull_request(self, repo, title, body, head, base="main"):
        return repo.create_pull(
            title=title,
            body=body,
            head=head,
            base=base
        )