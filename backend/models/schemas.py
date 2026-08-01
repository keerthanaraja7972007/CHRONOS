from enum import Enum
from pydantic import BaseModel
class Verdict(str,Enum): merge="Merge"; caution="Merge with Caution"; changes="Request Changes"; block="Block Merge"
class WorkflowProgress(BaseModel): run_id:str; stage:str; agent_name:str|None=None; state:str; payload:dict={}
