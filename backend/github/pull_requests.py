from backend.analysis.pr_analysis_agent import PRAnalysisAgent
from backend.github.github_client import GitHubClient
def fetch_structured_diff(client:GitHubClient,owner:str,repository:str,number:int):
    pr=client.pull_request(owner,repository,number); diff=client.diff(owner,repository,number)
    return PRAnalysisAgent().analyze(repository_name=repository,owner=owner,branch=pr["base"]["ref"],commit_hash=pr["head"]["sha"],diff=diff,title=pr["title"],description=pr.get("body") or "",author=pr["user"]["login"],number=number)
