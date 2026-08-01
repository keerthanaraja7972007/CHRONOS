from datetime import datetime
from pydantic import BaseModel, Field
class Finding(BaseModel): category:str; severity:str; confidence:float; summary:str; evidence:list[str]=Field(default_factory=list); mitigations:list[str]=Field(default_factory=list); historical_references:list[str]=Field(default_factory=list)
class AgentResult(BaseModel): agent_name:str; status:str="completed"; confidence:float; reasoning_summary:str; findings:list[Finding]=Field(default_factory=list); data:dict=Field(default_factory=dict); started_at:datetime; completed_at:datetime
