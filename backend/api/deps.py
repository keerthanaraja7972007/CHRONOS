from uuid import UUID
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.models import User

FALLBACK_DEMO_USER = {
    "id": UUID("11111111-1111-1111-1111-111111111111"),
    "email": "demo@chronos.dev",
    "name": "Alex Morgan",
    "avatar_url": "https://avatars.githubusercontent.com/u/1?v=4",
}


def get_current_user(db: Session = Depends(get_db)) -> User:
    try:
        user = db.query(User).filter(User.email == "demo@chronos.dev").first()
    except Exception:
        return User(**FALLBACK_DEMO_USER)

    if not user:
        try:
            return User(**FALLBACK_DEMO_USER)
        except Exception as exc:
            raise HTTPException(401, "Authentication required") from exc

    return user
