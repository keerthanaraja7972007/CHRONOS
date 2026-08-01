"""Provider-agnostic orchestration entry point. Future workers call this module."""
from backend.orchestrator.contracts import AnalysisContext, AnalysisAgent
async def run_agents(context: AnalysisContext, agents: list[AnalysisAgent]):
    return [await agent.analyze(context) for agent in agents]
