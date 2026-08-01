from __future__ import annotations
import asyncio, logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from backend.debate.debate_log import DebateLog
from backend.models.agent_result import AgentResult, Finding
from backend.models.analysis_context import AgentAnalysisContext
logger=logging.getLogger(__name__)
class AgentExecutionError(RuntimeError):pass
class BaseAgent(ABC):
    name:str; system_prompt:str; timeout_seconds:float=20
    async def run(self,context:AgentAnalysisContext,debate:DebateLog)->AgentResult:
        started=datetime.now(timezone.utc)
        try:
            findings,data=await asyncio.wait_for(self.evaluate(context),timeout=self.timeout_seconds); confidence=round(sum(f.confidence for f in findings)/len(findings),2) if findings else .75
            for finding in findings:debate.append(agent_name=self.name,category=finding.category,severity=finding.severity,confidence=finding.confidence,message=finding.summary,evidence=finding.evidence,historical_references=finding.historical_references)
            return AgentResult(agent_name=self.name,confidence=confidence,reasoning_summary=self.summary(findings),findings=findings,data=data,started_at=started,completed_at=datetime.now(timezone.utc))
        except Exception as exc:
            logger.exception("agent_failed",extra={"agent":self.name});raise AgentExecutionError(f"{self.name} failed") from exc
    @abstractmethod
    async def evaluate(self,context:AgentAnalysisContext)->tuple[list[Finding],dict]:...
    def summary(self,findings:list[Finding])->str:return "No material concerns identified." if not findings else "; ".join(item.summary for item in findings)
    def finding(self,category,severity,confidence,summary,evidence,mitigations=()):
        refs=[item["incident"]["id"] for item in context_references] if False else []
        return Finding(category=category,severity=severity,confidence=confidence,summary=summary,evidence=list(evidence),mitigations=list(mitigations))
