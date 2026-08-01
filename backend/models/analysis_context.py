from pydantic import BaseModel, Field
from backend.rag.context_builder import AnalysisContext as IntelligenceContext
class AgentAnalysisContext(BaseModel):
    intelligence: IntelligenceContext; previous_results:dict[str,dict]=Field(default_factory=dict); repository_settings:dict=Field(default_factory=dict); risk_thresholds:dict[str,float]=Field(default_factory=lambda:{"request_changes":55,"block":80})
