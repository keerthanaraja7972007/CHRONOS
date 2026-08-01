from pydantic import BaseModel, Field
from backend.analysis.blast_radius import BlastRadius
from backend.analysis.dependency_graph import DependencyGraph
from backend.analysis.repository_parser import RepositoryMetadata
from backend.analysis.structured_diff import StructuredDiff
class AnalysisContext(BaseModel): structured_diff:StructuredDiff; repository_metadata:RepositoryMetadata; dependency_graph:DependencyGraph; blast_radius:BlastRadius; relevant_historical_incidents:list[dict]=Field(default_factory=list); repository_statistics:dict[str,int]=Field(default_factory=dict); project_metadata:dict[str,str]=Field(default_factory=dict)
class ContextBuilder:
    def build(self,diff,metadata,graph,blast,relevant):return AnalysisContext(structured_diff=diff,repository_metadata=metadata,dependency_graph=graph,blast_radius=blast,relevant_historical_incidents=relevant,repository_statistics=metadata.statistics,project_metadata={"project_types":", ".join(metadata.project_types)})
