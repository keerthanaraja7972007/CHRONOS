from backend.analysis.structured_diff import StructuredDiff
from backend.incidents.models import IncidentRecord
from backend.rag.embeddings import EmbeddingProvider, clean_text
from backend.rag.similarity import rank
from backend.rag.vector_store import VectorStore
class SemanticRetriever:
    def __init__(self,store:VectorStore,embeddings:EmbeddingProvider):self.store=store;self.embeddings=embeddings
    def retrieve(self,repository:str,diff:StructuredDiff,incidents:dict[str,IncidentRecord],limit:int=8)->list[dict]:
        query=clean_text(" ".join([diff.pull_request.title,diff.pull_request.description,*diff.modified_files,*diff.imports_added]))
        return rank(diff,incidents,self.store.search(repository,self.embeddings.embed(query),limit))
