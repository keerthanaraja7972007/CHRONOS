from datetime import datetime
from uuid import UUID
from pydantic import Field
from backend.schemas.common import APIModel
class UserOut(APIModel): id: UUID; email: str; name: str; avatar_url: str|None=None
class RepositoryOut(APIModel): id: UUID; full_name: str; default_branch: str; is_active: bool
class PullRequestCreate(APIModel): repository_id: UUID; number: int=Field(gt=0); title: str; author: str; head_sha: str; base_branch: str="main"; diff: str|None=None
class PullRequestOut(PullRequestCreate): id: UUID; status: str; created_at: datetime
class AnalysisCreate(APIModel): pull_request_id: UUID
class AnalysisOut(APIModel): id: UUID; pull_request_id: UUID; status: str; pre_mortem: str|None=None; created_at: datetime
class RiskScoreOut(APIModel): score: int; level: str; factors: dict
class FeedbackCreate(APIModel): rating: int=Field(ge=1,le=5); comment: str|None=None
class SettingUpdate(APIModel): value: dict
class SettingOut(APIModel): key: str; value: dict
