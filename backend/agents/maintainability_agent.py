from backend.agents.base_agent import BaseAgent
from backend.models.agent_result import Finding
class MaintainabilityAgent(BaseAgent):
    name="Maintainability";system_prompt="Assess coupling, readability, testability and technical debt."
    async def evaluate(self,c):
        d=c.intelligence.structured_diff; test_changed=any("test" in f.path for f in d.files); debt=min(100,len(d.files)*8+len(c.intelligence.dependency_graph.circular_dependencies)*15); findings=[]
        if not test_changed:findings=[Finding(category="maintainability",severity="medium",confidence=.78,summary="No test change accompanies the implementation change.",evidence=d.modified_files,mitigations=["Add focused regression tests for affected services."],historical_references=[])]
        return findings,{"technical_debt_estimate":debt,"future_maintenance_risk":"high" if debt>60 else "moderate"}
