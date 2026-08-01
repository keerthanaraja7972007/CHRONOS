from datetime import datetime
from pydantic import BaseModel, Field
class DebateEntry(BaseModel): sequence:int; agent_name:str; timestamp:datetime; category:str; severity:str; confidence:float; evidence:list[str]=Field(default_factory=list); historical_references:list[str]=Field(default_factory=list); response_to:str|None=None; message:str
