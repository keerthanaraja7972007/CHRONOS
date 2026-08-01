from pydantic import BaseModel, Field
from backend.analysis.dependency_graph import DependencyGraph, DependencyGraphBuilder
class BlastRadius(BaseModel): classification:str; files_affected:list[str]=Field(default_factory=list); services_affected:list[str]=Field(default_factory=list); modules_affected:list[str]=Field(default_factory=list); downstream_consumers:list[str]=Field(default_factory=list); critical_paths:list[str]=Field(default_factory=list); dependency_depth:int=0
class BlastRadiusEstimator:
    def estimate(self,changed:list[str],graph:DependencyGraph,services:list[str])->BlastRadius:
        downstream=DependencyGraphBuilder().descendants(graph,changed); modules=list(downstream); depth=max(downstream.values(),default=0); matched=[s for s in services if any(f"/{s}/" in path or path.startswith(f"services/{s}/") for path in modules)]
        score=len(modules)+depth*2+len(matched)*3
        level="critical" if score>=20 else "high" if score>=12 else "medium" if score>=5 else "low"
        if matched and level == "low": level="medium"
        if depth > 0 and matched and level in {"low","medium"}: level="high"
        if any(path.startswith("shared/") for path in changed) and depth > 0: level="critical"
        return BlastRadius(classification=level,files_affected=changed,services_affected=matched,modules_affected=modules,downstream_consumers=[m for m in modules if m not in changed],critical_paths=changed if level in {"high","critical"} else [],dependency_depth=depth)
