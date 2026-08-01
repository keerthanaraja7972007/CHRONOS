from backend.db.session import SessionLocal
from backend.models import AnalysisHistory, PullRequest, Repository, RiskScore, User
from backend.models.models import AnalysisStatus
def seed():
    db=SessionLocal()
    try:
        user=db.query(User).filter_by(email="demo@chronos.dev").first()
        if not user:
            user=User(email="demo@chronos.dev",name="Alex Morgan",github_id="demo-chronos")
            db.add(user); db.flush()
        repo=db.query(Repository).filter_by(full_name="acme/payments-api").first()
        if not repo:
            repo=Repository(owner_id=user.id,external_id="demo-payments",full_name="acme/payments-api",default_branch="main")
            db.add(repo); db.flush()
        pr=db.query(PullRequest).filter_by(repository_id=repo.id,number=142).first()
        if not pr:
            pr=PullRequest(repository_id=repo.id,number=142,title="Optimize webhook retry worker",author="alexm",head_sha="a1b2c3d4",base_branch="main",status="open",diff="")
            db.add(pr); db.flush()
        if not db.query(AnalysisHistory).filter_by(pull_request_id=pr.id).first():
            analysis=AnalysisHistory(pull_request_id=pr.id,status=AnalysisStatus.completed,pre_mortem="Retry exhaustion may delay payment settlement under provider outages.")
            db.add(analysis); db.flush(); db.add(RiskScore(analysis_id=analysis.id,score=64,level="high",factors={"retry_behavior":0.8,"idempotency":0.5}))
        db.commit()
    finally: db.close()
if __name__ == "__main__": seed()
