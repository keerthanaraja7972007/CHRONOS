from fastapi import APIRouter
from backend.demo.catalog import incidents, pull_requests, repository_files
router=APIRouter(prefix="/demo",tags=["demo"])
@router.get("/repository")
def repository():return {"name":"acme/checkout-service","files":sorted(repository_files()),"file_count":len(repository_files())}
@router.get("/incidents")
def demo_incidents():return incidents()
@router.get("/pull-requests")
def demo_pull_requests():return pull_requests()
