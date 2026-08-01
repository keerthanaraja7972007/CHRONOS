from backend.agents.base_agent import BaseAgent
from backend.models.agent_result import Finding
class SecurityAgent(BaseAgent):
    name="Security";system_prompt="Identify security regressions using changed paths, symbols and historical incidents."
    async def evaluate(self,c):
        d=c.intelligence.structured_diff; text=" ".join(f.patch for f in d.files).lower(); sensitive=[f.path for f in d.files if any(x in f.path.lower() for x in ("auth","token","secret",".env","permission"))]; unsafe=any(x in text for x in ("unsafe","eval(","select "))
        findings=[]
        if sensitive or unsafe: findings.append(Finding(category="security",severity="critical" if unsafe else "high",confidence=.9,summary="Sensitive authentication or unsafe execution surface changed.",evidence=sensitive,mitigations=["Require security review and regression tests."],historical_references=["authentication-regression"]))
        return findings,{"blocking":any(x.severity=="critical" for x in findings)}
