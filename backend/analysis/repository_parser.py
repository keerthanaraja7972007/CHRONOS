from __future__ import annotations
from collections import Counter
from pathlib import PurePosixPath
from pydantic import BaseModel, Field
class RepositoryMetadata(BaseModel): project_types:list[str]=Field(default_factory=list); areas:dict[str,list[str]]=Field(default_factory=dict); languages:dict[str,int]=Field(default_factory=dict); services:list[str]=Field(default_factory=list); statistics:dict[str,int]=Field(default_factory=dict)
class RepositoryParser:
    def parse(self, paths:list[str])->RepositoryMetadata:
        areas={key:[] for key in ("backend","frontend","microservices","shared_libraries","configuration","tests","infrastructure","documentation")}; languages=Counter(); services=[]
        extensions={".py":"Python",".ts":"TypeScript",".tsx":"TypeScript",".js":"JavaScript",".java":"Java",".go":"Go",".rs":"Rust"}
        for raw in paths:
            path=PurePosixPath(raw); lower=raw.lower(); extension=path.suffix; languages[extensions.get(extension,"Other")]+=1
            category="documentation" if lower.startswith("docs/") or extension in {".md",".rst"} else "tests" if any(x in lower for x in ("/test","/tests",".spec.",".test.")) else "infrastructure" if any(x in lower for x in ("terraform","k8s","kubernetes","helm","docker")) else "configuration" if path.name.startswith(".") or extension in {".yml",".yaml",".toml"} else "frontend" if any(x in lower for x in ("frontend/","web/","client/","ui/")) else "backend" if any(x in lower for x in ("backend/","server/","api/")) else "shared_libraries" if any(x in lower for x in ("shared/","common/","lib/")) else "microservices" if "services/" in lower else None
            if category: areas[category].append(raw)
            if category=="microservices" and len(path.parts)>1: services.append(path.parts[path.parts.index("services")+1])
        types=[]
        markers={"Node":"package.json","Python":"pyproject.toml","Java":"pom.xml","Go":"go.mod","Rust":"Cargo.toml"}
        for name,marker in markers.items():
            if marker in paths: types.append(name)
        return RepositoryMetadata(project_types=types,areas={k:v for k,v in areas.items() if v},languages=dict(languages),services=sorted(set(services)),statistics={"files":len(paths),"services":len(set(services))})
