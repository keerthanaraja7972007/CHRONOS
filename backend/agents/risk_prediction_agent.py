from backend.agents.base_agent import BaseAgent
from backend.models.agent_result import Finding
class RiskPredictionAgent(BaseAgent):
    name="Risk Prediction";system_prompt="Calibrate composite risk from domain findings and repository history."
    async def evaluate(self,c):
        results=c.previous_results; weights={"Security":.3,"Reliability":.28,"Performance":.16,"Cost Optimization":.1,"Maintainability":.16}; values={}
        rank={"low":20,"medium":50,"high":75,"critical":100}
        for agent,weight in weights.items():values[agent]=max([rank.get(item["severity"],0) for item in results.get(agent,{}).get("findings",[])],default=0)
        score=round(sum(values[a]*weights[a] for a in weights)+rank[c.intelligence.blast_radius.classification]*.15+min(10,len(c.intelligence.relevant_historical_incidents)*1.5)); return [],{"composite_score":min(100,score),"domain_scores":values,"confidence_interval":[max(0,score-12),min(100,score+12)],"explanation":"Weighted domain signals, blast radius, and historical incident density."}
