from dataclasses import dataclass
from backend.agents.pr_analysis_agent import PRAnalysisAgent
from backend.agents.security_agent import SecurityAgent
from backend.agents.reliability_agent import ReliabilityAgent
from backend.agents.performance_agent import PerformanceAgent
from backend.agents.cost_agent import CostAgent
from backend.agents.maintainability_agent import MaintainabilityAgent
from backend.agents.risk_prediction_agent import RiskPredictionAgent
from backend.agents.incident_simulation_agent import IncidentSimulationAgent
from backend.agents.premortem_generator import PreMortemGenerator
from backend.agents.rollback_planner import RollbackPlanner
from backend.agents.counter_pr_agent import CounterPRAgent
from backend.agents.final_decision_agent import FinalDecisionAgent
@dataclass(frozen=True)
class Workflow: parallel:tuple= (PRAnalysisAgent(),SecurityAgent(),ReliabilityAgent(),PerformanceAgent(),CostAgent(),MaintainabilityAgent()); risk:object=RiskPredictionAgent(); simulation:object=IncidentSimulationAgent(); artifacts:tuple=(PreMortemGenerator(),RollbackPlanner(),CounterPRAgent()); final:object=FinalDecisionAgent()
