from __future__ import annotations
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
class GitHubClientError(RuntimeError): pass
class GitHubClient:
    def __init__(self,token:str,base_url:str="https://api.github.com"):self.token=token;self.base_url=base_url.rstrip("/")
    def _request(self,path:str):
        request=Request(f"{self.base_url}{path}",headers={"Accept":"application/vnd.github+json","Authorization":f"Bearer {self.token}","X-GitHub-Api-Version":"2022-11-28"})
        try:
            with urlopen(request,timeout=20) as response:return json.loads(response.read())
        except (HTTPError,URLError,json.JSONDecodeError) as exc:raise GitHubClientError("GitHub API request failed") from exc
    def repositories(self):return self._request("/user/repos?"+urlencode({"per_page":100,"sort":"updated"}))
    def pull_requests(self,owner:str,repo:str):return self._request(f"/repos/{owner}/{repo}/pulls?state=open&per_page=100")
    def pull_request(self,owner:str,repo:str,number:int):return self._request(f"/repos/{owner}/{repo}/pulls/{number}")
    def diff(self,owner:str,repo:str,number:int)->str:
        request=Request(f"{self.base_url}/repos/{owner}/{repo}/pulls/{number}",headers={"Accept":"application/vnd.github.v3.diff","Authorization":f"Bearer {self.token}"})
        try:
            with urlopen(request,timeout=20) as response:return response.read().decode()
        except (HTTPError,URLError) as exc:raise GitHubClientError("GitHub diff request failed") from exc
    def file_content(self,owner:str,repo:str,path:str,ref:str):return self._request(f"/repos/{owner}/{repo}/contents/{path}?"+urlencode({"ref":ref}))
    def commits(self,owner:str,repo:str):return self._request(f"/repos/{owner}/{repo}/commits?per_page=100")
