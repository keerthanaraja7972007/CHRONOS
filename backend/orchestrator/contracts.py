from dataclasses import dataclass
from typing import Protocol
@dataclass(frozen=True)
class AnalysisContext: pull_request_id: str; repository_name: str; diff: str
@dataclass(frozen=True)
class AgentFinding: agent_name: str; confidence: float; payload: dict
class AnalysisAgent(Protocol):
    name: str
    async def analyze(self, context: AnalysisContext) -> AgentFinding: ...
