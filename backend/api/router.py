from fastapi import APIRouter
from backend.api.routes import analyses, auth, demo, demo_mode, github, intelligence, pull_requests, repositories, settings, swarm
api_router=APIRouter(prefix="/api/v1")
for route in (auth.router,repositories.router,pull_requests.router,analyses.router,settings.router,intelligence.router,demo.router,demo_mode.router,github.router,swarm.router): api_router.include_router(route)
