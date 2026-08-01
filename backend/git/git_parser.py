from __future__ import annotations
import subprocess
from dataclasses import dataclass
from pathlib import Path
class GitParserError(RuntimeError): pass
@dataclass(frozen=True)
class CommitMetadata: sha:str; author:str; timestamp:str; message:str
class GitParser:
    def __init__(self,repository_path:Path): self.path=repository_path.resolve()
    def _run(self,*args:str)->str:
        try:return subprocess.run(["git","-C",str(self.path),*args],capture_output=True,text=True,check=True,timeout=30).stdout
        except (subprocess.CalledProcessError,subprocess.TimeoutExpired) as exc: raise GitParserError("Unable to read local git repository") from exc
    def tree(self,branch:str="HEAD")->list[str]: return self._run("ls-tree","-r","--name-only",branch).splitlines()
    def branches(self)->list[str]: return self._run("branch","--format=%(refname:short)").splitlines()
    def commits(self,limit:int=50)->list[CommitMetadata]: return [CommitMetadata(*line.split("\x1f",3)) for line in self._run("log",f"-{limit}","--format=%H%x1f%an%x1f%aI%x1f%s").splitlines()]
    def diff(self,base:str,head:str="HEAD")->str: return self._run("diff",f"{base}...{head}")
