from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from backend.demo.state import state
from backend.services.demo_service import demo_service
router=APIRouter(prefix="/demo-mode",tags=["offline demo"])
@router.get("/dashboard")
def dashboard():return demo_service.dashboard()
@router.get("/repository")
def repository():return state.repository
@router.get("/incidents")
def incident_list():return state.incidents
@router.get("/pull-requests")
def pr_list():return state.pull_requests
@router.post("/analyses/{number}")
async def analyze(number:int):
    try:return await demo_service.analyze(number)
    except KeyError:raise HTTPException(404,"Demo pull request not found")
@router.get("/history")
def history():return state.history
@router.post("/replay/{number}")
async def replay(number:int):
    existing=next((item for item in state.history if item["number"]==number),None)
    return existing or await demo_service.analyze(number)
@router.get("/reports/{number}/{artifact}",response_class=PlainTextResponse)
async def report(number:int,artifact:str):
    record=next((item for item in state.history if item["number"]==number),None) or await demo_service.analyze(number); data=record["result"]["results"]
    values={"premortem":data["Pre-Mortem"]["data"].get("markdown",""),"runbook":"\n".join(data["Rollback"]["data"].get("steps",[])),"counter-pr":data["Counter PR"]["data"].get("alternative_diff","")}
    if artifact not in values:raise HTTPException(404,"Unknown report artifact")
    return values[artifact]
@router.post("/reset")
def reset():state.reset();return {"status":"reset","created_at":state.created_at}
