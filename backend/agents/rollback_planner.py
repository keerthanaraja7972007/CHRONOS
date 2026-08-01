from backend.agents.base_agent import BaseAgent
class RollbackPlanner(BaseAgent):
    name="Rollback";system_prompt="Create safe, verifiable rollback instructions."
    async def evaluate(self,c):
        files=c.intelligence.structured_diff.modified_files; return [],{"trigger_conditions":["Error rate exceeds baseline","Payment or dependency timeout alert fires"],"steps":["Pause deployment","Disable affected feature flag","Redeploy previous stable revision","Verify key workflow"],"validation_steps":["Check dashboards","Run checkout smoke test"],"affected_files":files,"escalation":"Page the owning service team if recovery exceeds 15 minutes."}
