from backend.agents.base_agent import BaseAgent
from backend.models.agent_result import Finding
class PRAnalysisAgent(BaseAgent):
    name="PR Analysis";system_prompt="Summarize engineering impact from structured changes."
    async def evaluate(self,c):
        d=c.intelligence.structured_diff; b=c.intelligence.blast_radius
        return [Finding(category="change_summary",severity=b.classification,confidence=.9,summary=f"{len(d.files)} files changed across {', '.join(b.services_affected) or 'shared components'}.",evidence=d.modified_files+d.added_files,mitigations=[],historical_references=[])],{"components":d.methods_modified,"complexity":"high" if len(d.files)>8 else "moderate","blast_radius":b.model_dump()}
