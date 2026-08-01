from __future__ import annotations
from backend.demo.state import state
from backend.models.analysis_context import AgentAnalysisContext
from backend.orchestrator.orchestrator import AgentOrchestrator
from backend.services.intelligence import service
class DemoService:
    async def analyze(self,number:int):
        pr=next((item for item in state.pull_requests if item["number"]==number),None)
        if not pr:raise KeyError(number)
        intelligence=service.analyze_diff(pr["diff"],title=pr["title"],author=pr["author"],number=number)
        result=await AgentOrchestrator().run(AgentAnalysisContext(intelligence=intelligence))
        record={"id":result["run_id"],"number":number,"title":pr["title"],"author":pr["author"],"risk_score":result["verdict"]["final_risk_score"],"decision":result["verdict"]["verdict"],"created_at":state.created_at.isoformat(),"result":result}
        state.history=[item for item in state.history if item["number"]!=number]+[record];return record
    def dashboard(self):
        history=state.history; return {"repository":state.repository,"statistics":{"repositories":1,"indexed_files":state.repository["file_count"],"incidents":len(state.incidents),"analyses":len(history),"high_risk":sum(x["risk_score"]>=80 for x in history)},"risk_trend":[{"week":f"Week {i+1}","score":value} for i,value in enumerate([22,31,28,47,39,54,43,61])],"recent_analyses":history[-8:],"high_risk_prs":[pr for pr in state.pull_requests if pr["risk"] in {"high","critical"}]}
demo_service=DemoService()
