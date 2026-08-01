from __future__ import annotations
from backend.analysis.blast_radius import BlastRadiusEstimator
from backend.analysis.dependency_graph import DependencyGraphBuilder
from backend.analysis.pr_analysis_agent import PRAnalysisAgent
from backend.analysis.repository_parser import RepositoryParser
from backend.demo.catalog import incidents, repository_files
from backend.rag.context_builder import ContextBuilder
from backend.rag.embeddings import HashEmbeddingProvider
from backend.rag.retriever import SemanticRetriever
from backend.rag.vector_store import InMemoryVectorStore
class IntelligenceService:
    def __init__(self):
        self.files=repository_files(); self.incidents={item.id:item for item in incidents()}; self.embedding=HashEmbeddingProvider(); self.store=InMemoryVectorStore(); self.graph=DependencyGraphBuilder().build(self.files); self.metadata=RepositoryParser().parse(list(self.files))
        for incident in self.incidents.values():self.store.upsert(incident.repository,incident.id,self.embedding.embed(incident.content),incident.model_dump())
    def analyze_diff(self,diff:str,*,title:str,author:str="demo",description:str="",number:int|None=None):
        structured=PRAnalysisAgent().analyze(repository_name="checkout-service",owner="acme",branch="main",commit_hash="demo-head",diff=diff,title=title,description=description,author=author,number=number)
        blast=BlastRadiusEstimator().estimate(structured.modified_files+structured.added_files,self.graph,self.metadata.services); structured.impact.services_affected=blast.services_affected; structured.impact.downstream_modules=blast.downstream_consumers; structured.impact.dependency_depth=blast.dependency_depth; structured.impact.classification=blast.classification
        relevant=SemanticRetriever(self.store,self.embedding).retrieve("acme/checkout-service",structured,self.incidents)
        return ContextBuilder().build(structured,self.metadata,self.graph,blast,relevant)
service=IntelligenceService()
