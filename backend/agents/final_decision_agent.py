from backend.agents.base_agent import BaseAgent
class FinalDecisionAgent(BaseAgent):
    name="Final Decision";system_prompt="Resolve evidence with critical-security override rules."
    async def evaluate(self,c):
        results=c.previous_results; security=results.get("Security",{}).get("findings",[]); risk=results.get("Risk Prediction",{}).get("data",{}).get("composite_score",0); critical=any(item["severity"]=="critical" for item in security)
        verdict="Block Merge" if critical or risk>=c.risk_thresholds["block"] else "Request Changes" if risk>=c.risk_thresholds["request_changes"] else "Merge with Caution" if risk>=30 else "Merge"
        return [],{"verdict":verdict,"final_risk_score":risk,"override_applied":critical,"executive_summary":"Critical security evidence overrides the composite score." if critical else "Decision balances weighted agent evidence and historical grounding."}
