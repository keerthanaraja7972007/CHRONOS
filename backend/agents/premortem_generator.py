from backend.agents.base_agent import BaseAgent
class PreMortemGenerator(BaseAgent):
    name="Pre-Mortem";system_prompt="Generate an actionable pre-incident engineering report."
    async def evaluate(self,c):
        risk=c.previous_results.get("Risk Prediction",{}).get("data",{}); references=[item["incident"].id if hasattr(item["incident"],"id") else item["incident"]["id"] for item in c.intelligence.relevant_historical_incidents]; return [],{"markdown":f"# Pre-Mortem\n\n## Risk overview\nComposite risk: {risk.get('composite_score','pending')}\n\n## Blast radius\n{c.intelligence.blast_radius.classification.title()} across {', '.join(c.intelligence.blast_radius.services_affected) or 'changed modules'}.\n\n## Recommended actions\nValidate rollback, add regression tests, and monitor error rates.","historical_references":references}
