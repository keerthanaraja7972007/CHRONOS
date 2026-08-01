from datetime import date
from pydantic import BaseModel, Field
class IncidentRecord(BaseModel): id:str; repository:str; title:str; root_cause:str; affected_files:list[str]=Field(default_factory=list); affected_services:list[str]=Field(default_factory=list); severity:str; occurred_on:date; resolution:str; tags:list[str]=Field(default_factory=list); source_type:str="manual"; content:str=""
