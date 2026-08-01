from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException
from backend.demo.catalog import incidents, pull_requests, repository_files
from backend.services.intelligence import service
router=APIRouter(prefix="/intelligence",tags=["repository intelligence"])
class DiffRequest(BaseModel): diff:str=Field(min_length=1,max_length=2_000_000); title:str=Field(min_length=1,max_length=500); author:str="manual"; description:str=""; number:int|None=None
@router.post("/structured-diff")
def structured_diff(payload:DiffRequest): return service.analyze_diff(payload.diff,title=payload.title,author=payload.author,description=payload.description,number=payload.number).structured_diff
@router.get("/repository-metadata")
def repository_metadata():return service.metadata
@router.get("/dependency-graph")
def dependency_graph():return service.graph
@router.get("/blast-radius/{number}")
def blast_radius(number:int):return _context(number).blast_radius
@router.get("/incidents")
def list_incidents():return incidents()
@router.get("/semantic-search/{number}")
def semantic_search(number:int):return _context(number).relevant_historical_incidents
@router.get("/similarity-rankings/{number}")
def similarity_rankings(number:int):return _context(number).relevant_historical_incidents
@router.get("/analysis-context/{number}")
def analysis_context(number:int):return _context(number)
def _context(number:int):
    pr=next((item for item in pull_requests() if item["number"]==number),None)
    if not pr:raise HTTPException(404,"Demo pull request not found")
    return service.analyze_diff(pr["diff"],title=pr["title"],author=pr["author"],number=number)
