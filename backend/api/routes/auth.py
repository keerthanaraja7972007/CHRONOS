from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from backend.api.deps import get_current_user
from backend.core.config import get_settings
from backend.db.session import get_db
from backend.github.oauth import authorization_url
from backend.models import User
from backend.schemas.resources import UserOut

router = APIRouter(prefix="/auth", tags=["auth"])
FALLBACK_DEMO_USER = {
    "id": UUID("11111111-1111-1111-1111-111111111111"),
    "email": "demo@chronos.dev",
    "name": "Alex Morgan",
    "avatar_url": "https://avatars.githubusercontent.com/u/1?v=4",
}


@router.get("/github")
def github_login():
    settings = get_settings()
    if not settings.github_client_id or not settings.github_callback_url:
        raise HTTPException(501, "GitHub OAuth is not configured for this deployment. Use Demo Mode instead.")

    return RedirectResponse(authorization_url(str(uuid4())), status_code=302)


@router.get("/github/callback")
def github_callback(code: str | None = None, state: str | None = None, error: str | None = None):
    if error:
        raise HTTPException(400, f"GitHub OAuth error: {error}")
    if not code:
        raise HTTPException(400, "GitHub OAuth callback did not receive a code")

    return {
        "provider": "github",
        "status": "callback-received",
        "message": "OAuth callback received; exchange the authorization code with your GitHub app to complete sign-in.",
        "state": state,
    }


@router.post("/demo", response_model=UserOut)
def demo_login(db: Session = Depends(get_db)):
    if not get_settings().enable_demo_auth:
        raise HTTPException(404, "Demo authentication is disabled")

    try:
        user = db.query(User).filter(User.email == "demo@chronos.dev").first()
    except Exception:
        return FALLBACK_DEMO_USER

    if not user:
        return FALLBACK_DEMO_USER

    return user


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
