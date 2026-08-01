from __future__ import annotations
from datetime import datetime, timezone
from backend.demo.catalog import incidents, pull_requests, repository_files
class DemoState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.created_at = datetime.now(timezone.utc)
        self.repository = {
            "name": "acme/checkout-service",
            "owner": "acme",
            "description": "Production e-commerce checkout platform",
            "default_branch": "main",
            "contributors": ["Alex Morgan", "Maya Chen", "Noah Patel"],
            "file_count": len(repository_files()),
            "languages": {"Python": 91, "TypeScript": 4, "YAML": 2, "Markdown": 1},
            "files": sorted(repository_files()),
        }
        self.incidents = incidents()[:8]
        self.pull_requests = pull_requests()
        self.history = []


state = DemoState()
