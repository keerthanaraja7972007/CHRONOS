from __future__ import annotations
from datetime import datetime, timezone
from backend.analysis.structured_diff import EstimatedImpact, PRMetadata, RepositoryInfo, StructuredDiff
from backend.git.diff_parser import UnifiedDiffParser
class PRAnalysisAgent:
    """Extraction-only adapter. It never ranks, predicts, or reasons about a change."""
    def __init__(self, parser:UnifiedDiffParser|None=None):self.parser=parser or UnifiedDiffParser()
    def analyze(self,*,repository_name:str,owner:str,branch:str,commit_hash:str,diff:str,title:str,description:str="",author:str="unknown",number:int|None=None,created_at:datetime|None=None)->StructuredDiff:
        files,symbols,imports_added,imports_removed,dependencies,configuration=self.parser.parse(diff)
        classes=[s for s in symbols if s.kind=="class"]; methods=[s for s in symbols if s.kind=="method"]; interfaces=[s for s in symbols if s.kind=="interface"]
        return StructuredDiff(repository=RepositoryInfo(name=repository_name,owner=owner,branch=branch,commit_hash=commit_hash),pull_request=PRMetadata(title=title,description=description,author=author,number=number,created_at=created_at or datetime.now(timezone.utc)),files=files,classes_modified=classes,methods_modified=methods,interfaces_modified=interfaces,imports_added=imports_added,imports_removed=imports_removed,dependency_changes=dependencies,configuration=configuration,impact=EstimatedImpact(classification="low"))
