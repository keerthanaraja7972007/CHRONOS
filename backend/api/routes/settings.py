from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.deps import get_current_user
from backend.db.session import get_db
from backend.models import Setting, User
from backend.schemas.resources import SettingOut, SettingUpdate
router=APIRouter(prefix="/settings",tags=["settings"])
@router.get("",response_model=list[SettingOut])
def list_all(db: Session=Depends(get_db), user: User=Depends(get_current_user)): return db.query(Setting).filter_by(user_id=user.id).all()
@router.put("/{key}",response_model=SettingOut)
def update(key: str,payload: SettingUpdate,db: Session=Depends(get_db),user: User=Depends(get_current_user)):
    setting=db.query(Setting).filter_by(user_id=user.id,key=key).first() or Setting(user_id=user.id,key=key)
    setting.value=payload.value; db.add(setting); db.commit(); db.refresh(setting); return setting
