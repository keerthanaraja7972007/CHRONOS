from __future__ import annotations
from datetime import datetime, timezone
from threading import Lock
from backend.models.debate_entry import DebateEntry
class DebateLog:
    def __init__(self):self._entries:list[DebateEntry]=[];self._lock=Lock()
    def append(self,*,agent_name:str,category:str,severity:str,confidence:float,message:str,evidence:list[str]|None=None,historical_references:list[str]|None=None,response_to:str|None=None)->DebateEntry:
        with self._lock:
            entry=DebateEntry(sequence=len(self._entries)+1,agent_name=agent_name,timestamp=datetime.now(timezone.utc),category=category,severity=severity,confidence=confidence,message=message,evidence=evidence or [],historical_references=historical_references or [],response_to=response_to);self._entries.append(entry);return entry
    def entries(self)->tuple[DebateEntry,...]:return tuple(self._entries)
