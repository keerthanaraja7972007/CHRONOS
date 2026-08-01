from fastapi import APIRouter, HTTPException
from backend.demo.catalog import pull_requests
from backend.models.analysis_context import AgentAnalysisContext
from backend.orchestrator.orchestrator import AgentOrchestrator
from backend.services.intelligence import service
router=APIRouter(prefix="/swarm",tags=["AI swarm"])
@router.post("/runs/{number}")
async def run_demo(number:int):
    pr=next((item for item in pull_requests() if item["number"]==number),None)
    if not pr:raise HTTPException(404,"Demo pull request not found")
    intelligence=service.analyze_diff(pr["diff"],title=pr["title"],author=pr["author"],number=number)
    return await AgentOrchestrator().run(AgentAnalysisContext(intelligence=intelligence))
