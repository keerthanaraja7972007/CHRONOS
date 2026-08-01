from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.models import Repository, User
def list_repositories(db: Session, user: User) -> list[Repository]: return list(db.scalars(select(Repository).where(Repository.owner_id == user.id).order_by(Repository.full_name)))
