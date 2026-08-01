from __future__ import annotations
import hashlib, math, re
from typing import Protocol
class EmbeddingProvider(Protocol):
    dimensions:int
    def embed(self,text:str)->list[float]:...
class HashEmbeddingProvider:
    """Deterministic local embedding provider suitable for demo and tests; replace through DI in production."""
    dimensions=192
    def embed(self,text:str)->list[float]:
        vector=[0.0]*self.dimensions
        for token in re.findall(r"[a-zA-Z_]{2,}",text.lower()): vector[int(hashlib.sha256(token.encode()).hexdigest(),16)%self.dimensions]+=1
        magnitude=math.sqrt(sum(x*x for x in vector)); return [x/magnitude for x in vector] if magnitude else vector
def clean_text(value:str)->str:return re.sub(r"\s+"," ",value).strip()
def chunk_text(value:str,size:int=700,overlap:int=100)->list[str]:
    cleaned=clean_text(value); return [cleaned[start:start+size] for start in range(0,max(1,len(cleaned)),max(1,size-overlap))] if cleaned else []
