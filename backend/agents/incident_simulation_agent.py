from backend.agents.base_agent import BaseAgent
class IncidentSimulationAgent(BaseAgent):
    name="Incident Simulation";system_prompt="Produce a grounded operational incident timeline."
    async def evaluate(self,c):
        b=c.intelligence.blast_radius; service=", ".join(b.services_affected) or "the changed service"; return [],{"timeline":[{"minute":0,"event":"Change deployed"},{"minute":5,"event":f"Dependency degradation reaches {service}"},{"minute":15,"event":"User-facing errors trigger alerting"},{"minute":30,"event":"Rollback or feature flag restores service"}],"root_cause_hypothesis":f"Failure propagation across {b.dependency_depth} dependency levels.","narrative":"A bounded failure becomes visible through downstream consumers."}
