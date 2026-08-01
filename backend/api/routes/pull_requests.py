from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api.deps import get_current_user
from backend.db.session import get_db
from backend.models import PullRequest, Repository, User
from backend.schemas.resources import PullRequestCreate, PullRequestOut
router=APIRouter(prefix="/pull-requests",tags=["pull requests"])
@router.post("",response_model=PullRequestOut,status_code=201)
def create(payload: PullRequestCreate, db: Session=Depends(get_db), user: User=Depends(get_current_user)):
    repo=db.get(Repository,payload.repository_id)
    if not repo or repo.owner_id != user.id: raise HTTPException(404,"Repository not found")
    pr=PullRequest(**payload.model_dump()); db.add(pr); db.commit(); db.refresh(pr); return pr
@router.get("/{pull_request_id}",response_model=PullRequestOut)
def get_one(pull_request_id: str, db: Session=Depends(get_db)):
    pr=db.get(PullRequest,pull_request_id)
    if not pr: raise HTTPException(404,"Pull request not found")
    return pr
