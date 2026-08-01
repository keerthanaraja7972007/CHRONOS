import enum
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, JSON, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.db.base import Base

class Timestamped(Base):
    __abstract__=True
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
class AnalysisStatus(str, enum.Enum): queued="queued"; running="running"; completed="completed"; failed="failed"
class User(Timestamped):
    __tablename__="users"; email: Mapped[str]=mapped_column(String(320),unique=True,index=True); name: Mapped[str]=mapped_column(String(120)); avatar_url: Mapped[str|None]=mapped_column(String(2048)); github_id: Mapped[str|None]=mapped_column(String(64),unique=True); is_active: Mapped[bool]=mapped_column(Boolean,default=True)
class Repository(Timestamped):
    __tablename__="repositories"; owner_id: Mapped[UUID]=mapped_column(ForeignKey("users.id"),index=True); provider: Mapped[str]=mapped_column(String(30),default="github"); external_id: Mapped[str]=mapped_column(String(100)); full_name: Mapped[str]=mapped_column(String(300),unique=True); default_branch: Mapped[str]=mapped_column(String(255),default="main"); is_active: Mapped[bool]=mapped_column(Boolean,default=True)
class PullRequest(Timestamped):
    __tablename__="pull_requests"; repository_id: Mapped[UUID]=mapped_column(ForeignKey("repositories.id"),index=True); number: Mapped[int]=mapped_column(Integer); title: Mapped[str]=mapped_column(String(500)); author: Mapped[str]=mapped_column(String(120)); head_sha: Mapped[str]=mapped_column(String(64)); base_branch: Mapped[str]=mapped_column(String(255)); status: Mapped[str]=mapped_column(String(40),default="open"); diff: Mapped[str|None]=mapped_column(Text); __table_args__=(UniqueConstraint("repository_id","number",name="uq_pr_repo_number"),)
class AnalysisHistory(Timestamped):
    __tablename__="analysis_history"; pull_request_id: Mapped[UUID]=mapped_column(ForeignKey("pull_requests.id"),index=True); status: Mapped[AnalysisStatus]=mapped_column(Enum(AnalysisStatus),default=AnalysisStatus.queued); pre_mortem: Mapped[str|None]=mapped_column(Text); completed_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
class AgentResult(Timestamped):
    __tablename__="agent_results"; analysis_id: Mapped[UUID]=mapped_column(ForeignKey("analysis_history.id"),index=True); agent_name: Mapped[str]=mapped_column(String(100)); status: Mapped[str]=mapped_column(String(30)); result: Mapped[dict]=mapped_column(JSON,default=dict); confidence: Mapped[float|None]=mapped_column(Float)
class RiskScore(Timestamped):
    __tablename__="risk_scores"; analysis_id: Mapped[UUID]=mapped_column(ForeignKey("analysis_history.id"),unique=True); score: Mapped[int]=mapped_column(Integer); level: Mapped[str]=mapped_column(String(20)); factors: Mapped[dict]=mapped_column(JSON,default=dict)
class SimulationResult(Timestamped):
    __tablename__="simulation_results"; analysis_id: Mapped[UUID]=mapped_column(ForeignKey("analysis_history.id"),index=True); scenario: Mapped[str]=mapped_column(String(255)); outcome: Mapped[dict]=mapped_column(JSON,default=dict)
class Feedback(Timestamped):
    __tablename__="feedback"; analysis_id: Mapped[UUID]=mapped_column(ForeignKey("analysis_history.id"),index=True); user_id: Mapped[UUID]=mapped_column(ForeignKey("users.id")); rating: Mapped[int]=mapped_column(Integer); comment: Mapped[str|None]=mapped_column(Text)
class IncidentReport(Timestamped):
    __tablename__="incident_reports"; analysis_id: Mapped[UUID]=mapped_column(ForeignKey("analysis_history.id"),unique=True); title: Mapped[str]=mapped_column(String(500)); report: Mapped[str]=mapped_column(Text); rollback_plan: Mapped[str|None]=mapped_column(Text); counter_pr: Mapped[dict]=mapped_column(JSON,default=dict)
class Setting(Timestamped):
    __tablename__="settings"; user_id: Mapped[UUID]=mapped_column(ForeignKey("users.id"),index=True); key: Mapped[str]=mapped_column(String(100)); value: Mapped[dict]=mapped_column(JSON,default=dict); __table_args__=(UniqueConstraint("user_id","key",name="uq_setting_user_key"),)
