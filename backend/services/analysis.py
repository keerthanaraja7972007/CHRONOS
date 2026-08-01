from sqlalchemy.orm import Session
from backend.models import AnalysisHistory, AnalysisStatus, PullRequest
from fastapi import HTTPException
def queue_analysis(db: Session, pull_request_id):
    if not db.get(PullRequest, pull_request_id): raise HTTPException(404, "Pull request not found")
    analysis = AnalysisHistory(pull_request_id=pull_request_id, status=AnalysisStatus.queued)
    db.add(analysis); db.commit(); db.refresh(analysis)
    return analysis
