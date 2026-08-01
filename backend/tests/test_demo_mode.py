import asyncio
from backend.demo.state import state
from backend.services.demo_service import demo_service
def test_demo_seed_is_offline_and_complete():
    state.reset(); assert state.repository["file_count"] >= 80; assert len(state.incidents) == 8; assert len(state.pull_requests) == 4
def test_critical_pull_request_blocks_merge():
    state.reset(); record=asyncio.run(demo_service.analyze(state.pull_requests[-1]["number"])); assert record["decision"] == "Block Merge"; assert record["risk_score"] >= 80
def test_reset_clears_history():
    state.history.append({"number":1}); state.reset(); assert state.history == []
