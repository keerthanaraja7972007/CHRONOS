from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.models import AnalysisHistory, RiskScore
from backend.schemas.resources import AnalysisCreate, AnalysisOut, RiskScoreOut
from backend.services.analysis import queue_analysis
router=APIRouter(prefix="/analyses",tags=["analyses"])
@router.post("",response_model=AnalysisOut,status_code=202)
def create(payload: AnalysisCreate, db: Session=Depends(get_db)): return queue_analysis(db,payload.pull_request_id)
@router.get("/{analysis_id}",response_model=AnalysisOut)
def get_one(analysis_id: UUID, db: Session=Depends(get_db)):
    value=db.get(AnalysisHistory,analysis_id)
    if not value: raise HTTPException(404,"Analysis not found")
    return value
@router.get("/{analysis_id}/risk",response_model=RiskScoreOut)
def risk(analysis_id: UUID, db: Session=Depends(get_db)):
    value=db.query(RiskScore).filter_by(analysis_id=analysis_id).first()
    if not value: raise HTTPException(404,"Risk score unavailable")
    return value
