from backend.agents.base_agent import BaseAgent
class CounterPRAgent(BaseAgent):
    name="Counter PR";system_prompt="Recommend minimal risk-reducing alternative changes."
    async def evaluate(self,c):
        paths=c.intelligence.structured_diff.modified_files; return [],{"alternative_diff":"Add bounded retry count, timeout, and idempotency guard before publishing retry events.","risk_delta":"Reduces retry amplification and duplicate-processing risk.","adoption_recommendation":"Adopt before merge when retry or queue behavior changes.","target_files":paths}
