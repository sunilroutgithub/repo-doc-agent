from github import Github
from app.config import settings

class GitHubClient:
    def __init__(self):
        self.client = Github(settings.GITHUB_TOKEN)
    
    def get_repo(self):
        return self.client.get_repo(settings.TARGET_REPO)
    
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