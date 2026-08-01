from backend.agents.base_agent import BaseAgent
from backend.models.agent_result import Finding
class PerformanceAgent(BaseAgent):
    name="Performance";system_prompt="Detect latency, query, cache, memory and throughput regressions."
    async def evaluate(self,c):
        text=" ".join(f.patch for f in c.intelligence.structured_diff.files).lower(); trigger=any(x in text for x in ("query","loop","cache","list(")); findings=[]
        if trigger: findings=[Finding(category="performance",severity="medium",confidence=.72,summary="Changed code includes a potential data-access or hot-path pattern.",evidence=c.intelligence.structured_diff.modified_files,mitigations=["Benchmark the changed path and inspect query counts."],historical_references=["n-plus-one-query","cache-inconsistency"])]
        return findings,{"estimated_latency_delta_ms":25 if trigger else 0,"throughput_impact":"moderate" if trigger else "none"}
