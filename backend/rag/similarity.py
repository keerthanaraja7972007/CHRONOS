from __future__ import annotations
from datetime import date
from backend.analysis.structured_diff import StructuredDiff
from backend.incidents.models import IncidentRecord
from backend.rag.vector_store import VectorMatch
def rank(diff:StructuredDiff, incidents:dict[str,IncidentRecord], matches:list[VectorMatch])->list[dict]:
    changed=set(diff.modified_files+diff.added_files+diff.removed_files); service=set(diff.impact.services_affected); results=[]
    severity={"critical":1.0,"high":.8,"medium":.5,"low":.2}
    for match in matches:
        incident=incidents.get(match.id)
        if not incident:continue
        file_overlap=len(changed&set(incident.affected_files))/max(1,len(changed|set(incident.affected_files))); service_overlap=len(service&set(incident.affected_services))/max(1,len(service|set(incident.affected_services))) if service or incident.affected_services else 0
        root_overlap=sum(token in (diff.pull_request.title+" "+diff.pull_request.description).lower() for token in incident.root_cause.lower().split())/max(1,len(incident.root_cause.split()))
        recency=max(0,1-(date.today()-incident.occurred_on).days/730); score=.5*match.score+.2*file_overlap+.1*service_overlap+.08*root_overlap+.07*recency+.05*severity.get(incident.severity,.2)
        results.append({"incident":incident,"score":round(score,4),"signals":{"semantic":match.score,"files":round(file_overlap,3),"services":round(service_overlap,3),"root_cause":round(root_overlap,3),"recency":round(recency,3)}})
    return sorted(results,key=lambda result:result["score"],reverse=True)
