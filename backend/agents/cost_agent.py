from backend.agents.base_agent import BaseAgent
from backend.models.agent_result import Finding
class CostAgent(BaseAgent):
    name="Cost Optimization";system_prompt="Estimate operational cost impact."
    async def evaluate(self,c):
        b=c.intelligence.blast_radius; increase=min(.5,.04*len(b.modules_affected)+.06*b.dependency_depth); findings=[]
        if increase>.12:findings=[Finding(category="cost",severity="medium",confidence=.7,summary="Broad dependency impact may increase compute and request cost.",evidence=b.modules_affected,mitigations=["Instrument retries and cap downstream fan-out."],historical_references=[])]
        return findings,{"relative_cost_increase":increase,"high_cost_components":b.services_affected}
