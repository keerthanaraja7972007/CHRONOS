from __future__ import annotations
import asyncio,uuid
from backend.debate.debate_log import DebateLog
from backend.debate.event_bus import EventBus
from backend.models.analysis_context import AgentAnalysisContext
from backend.models.schemas import WorkflowProgress
from backend.orchestrator.workflow import Workflow
class AgentOrchestrator:
    def __init__(self,workflow:Workflow|None=None,bus:EventBus|None=None):self.workflow=workflow or Workflow();self.bus=bus or EventBus()
    async def run(self,context:AgentAnalysisContext)->dict:
        run_id=str(uuid.uuid4()); debate=DebateLog(); results={}
        async def execute(agent):
            await self.bus.publish(WorkflowProgress(run_id=run_id,stage="agent",agent_name=agent.name,state="running")); result=await agent.run(context.model_copy(update={"previous_results":results}),debate); results[agent.name]=result.model_dump(mode="json"); await self.bus.publish(WorkflowProgress(run_id=run_id,stage="agent",agent_name=agent.name,state="completed",payload=results[agent.name]))
        await asyncio.gather(*(execute(agent) for agent in self.workflow.parallel)); await execute(self.workflow.risk); await execute(self.workflow.simulation); await asyncio.gather(*(execute(agent) for agent in self.workflow.artifacts)); await execute(self.workflow.final)
        return {"run_id":run_id,"results":results,"debate_log":[entry.model_dump(mode="json") for entry in debate.entries()],"verdict":results["Final Decision"]["data"]}
