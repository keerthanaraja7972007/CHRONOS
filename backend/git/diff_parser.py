from __future__ import annotations
import re
from pathlib import PurePosixPath
from backend.analysis.structured_diff import ChangeKind, ChangedFile, ChangedSymbol, ConfigurationChanges, DependencyChange
_FILE=re.compile(r"^diff --git a/(.+?) b/(.+?)$",re.M); _HUNK=re.compile(r"^@@[^@]*\+([0-9]+)(?:,([0-9]+))?[^@]*@@",re.M)
def language(path:str)->str|None:
    return {".py":"python",".ts":"typescript",".tsx":"typescript",".js":"javascript",".java":"java",".go":"go",".rs":"rust",".yml":"yaml",".yaml":"yaml",".json":"json"}.get(PurePosixPath(path).suffix)
class UnifiedDiffParser:
    def parse(self,text:str)->tuple[list[ChangedFile],list[ChangedSymbol],list[str],list[str],list[DependencyChange],ConfigurationChanges]:
        files=[]; symbols=[]; adds=[]; removes=[]; deps=[]; config=ConfigurationChanges()
        matches=list(_FILE.finditer(text))
        for index,match in enumerate(matches):
            block=text[match.end():matches[index+1].start() if index+1<len(matches) else len(text)]; old,new=match.groups(); path=new if new!="/dev/null" else old
            kind=ChangeKind.renamed if "similarity index" in block and "rename from" in block else ChangeKind.added if "--- /dev/null" in block else ChangeKind.removed if "+++ /dev/null" in block else ChangeKind.modified
            additions=sum(1 for line in block.splitlines() if line.startswith("+") and not line.startswith("+++")); deletions=sum(1 for line in block.splitlines() if line.startswith("-") and not line.startswith("---"))
            files.append(ChangedFile(path=path,previous_path=old if kind is ChangeKind.renamed else None,change=kind,additions=additions,deletions=deletions,patch=block,language=language(path)))
            for line in block.splitlines():
                if line.startswith("+") and not line.startswith("+++"):
                    value=line[1:].strip(); import_match=re.match(r"(?:from\s+([\w.]+)\s+import|import\s+([\w.]+)|import .* from ['\"]([^'\"]+))",value)
                    if import_match: adds.append(next(item for item in import_match.groups() if item))
                    symbol=re.match(r"(?:class|interface|def|function|async function)\s+(\w+)",value)
                    if symbol: symbols.append(ChangedSymbol(name=symbol.group(1),kind="class" if value.startswith("class") else "interface" if value.startswith("interface") else "method",path=path))
                if line.startswith("-") and not line.startswith("---"):
                    value=line[1:].strip(); import_match=re.match(r"(?:from\s+([\w.]+)\s+import|import\s+([\w.]+)|import .* from ['\"]([^'\"]+))",value)
                    if import_match: removes.append(next(item for item in import_match.groups() if item))
            if PurePosixPath(path).name in {"package.json","pyproject.toml","requirements.txt","package-lock.json"}:
                for line in block.splitlines():
                    if line[:1] in "+-" and '"' in line: deps.append(DependencyChange(ecosystem="npm" if "package" in path else "python",package=line.strip("+- ,\"").split('"')[0],change=ChangeKind.added if line.startswith("+") else ChangeKind.removed))
            target=config.docker if "docker" in path.lower() else config.kubernetes if any(x in path.lower() for x in ("k8s","kubernetes","helm")) else config.environment if PurePosixPath(path).name.startswith(".env") else config.ci_cd if any(x in path for x in (".github/",".gitlab-ci","Jenkinsfile")) else None
            if target is not None: target.append(path)
        return files,symbols,adds,removes,deps,config
