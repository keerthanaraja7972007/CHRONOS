from backend.agents.base_agent import BaseAgent
from backend.models.agent_result import Finding
class ReliabilityAgent(BaseAgent):
    name="Reliability";system_prompt="Assess retries, timeouts, recovery and operational failure conditions."
    async def evaluate(self,c):
        d=c.intelligence.structured_diff; files=d.modified_files+d.added_files; retry=any(any(x in f.lower() for x in ("retry","queue","payment","timeout")) for f in files); severity="high" if retry else c.intelligence.blast_radius.classification
        findings=[Finding(category="reliability",severity=severity,confidence=.86,summary="Retry or dependency-path changes can amplify failures." if retry else "Blast radius has operational impact.",evidence=files,mitigations=["Set bounded retries, timeouts, and idempotency checks."],historical_references=["payment-retry-loop","dependency-timeout"])] if retry or severity in {"high","critical"} else []
        return findings,{"three_am_page_probability":.62 if retry else .14,"failure_conditions":["upstream dependency degradation"] if retry else []}
