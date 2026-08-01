from __future__ import annotations
import json,re
from datetime import date
from pathlib import Path
from backend.incidents.models import IncidentRecord
class IncidentParser:
    def parse(self,source:str,repository:str,source_type:str="markdown")->IncidentRecord:
        if source_type=="json": data=json.loads(source); return IncidentRecord(repository=repository,**data)
        fields={key:re.search(rf"^{key.replace('_',' ')}:\s*(.+)$",source,re.I|re.M) for key in ("title","severity","root_cause","resolution","date","tags","affected_files","affected_services")}
        value=lambda name,default="": fields[name].group(1).strip() if fields[name] else default
        identifier=re.sub(r"[^a-z0-9]+","-",value("title","incident").lower()).strip("-")
        return IncidentRecord(id=identifier,repository=repository,title=value("title","Untitled incident"),root_cause=value("root_cause"),affected_files=[x.strip() for x in value("affected_files").split(",") if x.strip()],affected_services=[x.strip() for x in value("affected_services").split(",") if x.strip()],severity=value("severity","medium").lower(),occurred_on=date.fromisoformat(value("date",date.today().isoformat())),resolution=value("resolution"),tags=[x.strip() for x in value("tags").split(",") if x.strip()],source_type=source_type,content=source)
    def parse_file(self,path:Path,repository:str)->IncidentRecord:
        if path.suffix.lower()==".pdf": raise ValueError("PDF extraction requires a configured document extractor")
        return self.parse(path.read_text(encoding="utf-8"),repository,"json" if path.suffix==".json" else "markdown")
