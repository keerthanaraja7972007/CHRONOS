from __future__ import annotations
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

class ChangeKind(str, Enum): added="added"; removed="removed"; modified="modified"; renamed="renamed"
class ChangedFile(BaseModel): path: str; change: ChangeKind; previous_path: str|None=None; additions: int=0; deletions: int=0; patch: str=""; language: str|None=None
class ChangedSymbol(BaseModel): name: str; kind: str; path: str; line_start: int|None=None; line_end: int|None=None
class DependencyChange(BaseModel): ecosystem: str; package: str; old_version: str|None=None; new_version: str|None=None; change: ChangeKind
class ConfigurationChanges(BaseModel): docker: list[str]=Field(default_factory=list); kubernetes: list[str]=Field(default_factory=list); environment: list[str]=Field(default_factory=list); ci_cd: list[str]=Field(default_factory=list)
class RepositoryInfo(BaseModel): name: str; owner: str; branch: str; commit_hash: str; provider: str="manual"
class PRMetadata(BaseModel): title: str; description: str=""; author: str; created_at: datetime; number: int|None=None
class EstimatedImpact(BaseModel): services_affected: list[str]=Field(default_factory=list); downstream_modules: list[str]=Field(default_factory=list); dependency_depth: int=0; classification: str="low"
class StructuredDiff(BaseModel):
    repository: RepositoryInfo; pull_request: PRMetadata; files: list[ChangedFile]=Field(default_factory=list); classes_modified: list[ChangedSymbol]=Field(default_factory=list); methods_modified: list[ChangedSymbol]=Field(default_factory=list); interfaces_modified: list[ChangedSymbol]=Field(default_factory=list); apis_modified: list[ChangedSymbol]=Field(default_factory=list); imports_added: list[str]=Field(default_factory=list); imports_removed: list[str]=Field(default_factory=list); dependency_changes: list[DependencyChange]=Field(default_factory=list); configuration: ConfigurationChanges=Field(default_factory=ConfigurationChanges); impact: EstimatedImpact=Field(default_factory=EstimatedImpact)
    @property
    def added_files(self)->list[str]: return [f.path for f in self.files if f.change is ChangeKind.added]
    @property
    def removed_files(self)->list[str]: return [f.path for f in self.files if f.change is ChangeKind.removed]
    @property
    def renamed_files(self)->list[str]: return [f.path for f in self.files if f.change is ChangeKind.renamed]
    @property
    def modified_files(self)->list[str]: return [f.path for f in self.files if f.change is ChangeKind.modified]
