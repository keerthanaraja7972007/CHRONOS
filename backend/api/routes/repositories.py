from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api.deps import get_current_user
from backend.db.session import get_db
from backend.models import Repository, User
from backend.schemas.resources import RepositoryOut
from backend.services.repositories import list_repositories
router=APIRouter(prefix="/repositories",tags=["repositories"])
@router.get("",response_model=list[RepositoryOut])
def list_all(db: Session=Depends(get_db), user: User=Depends(get_current_user)): return list_repositories(db,user)
@router.get("/{repository_id}",response_model=RepositoryOut)
def get_one(repository_id: UUID, db: Session=Depends(get_db), user: User=Depends(get_current_user)):
    repo=db.get(Repository,repository_id)
    if not repo or repo.owner_id != user.id: raise HTTPException(404,"Repository not found")
    return repo
