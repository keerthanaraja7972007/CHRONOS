from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.github.github_client import GitHubClient, GitHubClientError
from backend.github.pull_requests import fetch_structured_diff
router=APIRouter(prefix="/github",tags=["github"])
class GitHubRequest(BaseModel): token:str=Field(min_length=1); owner:str; repository:str; number:int|None=None
@router.post("/repositories")
def repositories(payload:GitHubRequest):
    try:return GitHubClient(payload.token).repositories()
    except GitHubClientError as exc:raise HTTPException(502,str(exc)) from exc
@router.post("/pull-requests")
def pull_requests(payload:GitHubRequest):
    try:return GitHubClient(payload.token).pull_requests(payload.owner,payload.repository)
    except GitHubClientError as exc:raise HTTPException(502,str(exc)) from exc
@router.post("/pull-request")
def pull_request(payload:GitHubRequest):
    if payload.number is None:raise HTTPException(422,"number is required")
    try:return GitHubClient(payload.token).pull_request(payload.owner,payload.repository,payload.number)
    except GitHubClientError as exc:raise HTTPException(502,str(exc)) from exc
@router.post("/diff")
def diff(payload:GitHubRequest):
    if payload.number is None:raise HTTPException(422,"number is required")
    try:return {"diff":GitHubClient(payload.token).diff(payload.owner,payload.repository,payload.number)}
    except GitHubClientError as exc:raise HTTPException(502,str(exc)) from exc
@router.post("/structured-diff")
def github_structured_diff(payload:GitHubRequest):
    if payload.number is None:raise HTTPException(422,"number is required")
    try:return fetch_structured_diff(GitHubClient(payload.token),payload.owner,payload.repository,payload.number)
    except GitHubClientError as exc:raise HTTPException(502,str(exc)) from exc
