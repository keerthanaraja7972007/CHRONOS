from __future__ import annotations
import re
from collections import defaultdict, deque
from pydantic import BaseModel, Field
class GraphNode(BaseModel): id:str; type:str="module"; external:bool=False
class GraphEdge(BaseModel): source:str; target:str; relation:str="imports"
class DependencyGraph(BaseModel): nodes:list[GraphNode]=Field(default_factory=list); edges:list[GraphEdge]=Field(default_factory=list); circular_dependencies:list[list[str]]=Field(default_factory=list); statistics:dict[str,int]=Field(default_factory=dict)
    
class DependencyGraphBuilder:
    def build(self, files:dict[str,str])->DependencyGraph:
        nodes={path:GraphNode(id=path) for path in files}; edges=[]
        for path,content in files.items():
            for target in self._imports(content):
                resolved=self._resolve(path,target,files); external=resolved not in files
                if resolved not in nodes:nodes[resolved]=GraphNode(id=resolved,type="package" if external else "module",external=external)
                edges.append(GraphEdge(source=path,target=resolved))
        cycles=self._cycles(edges); return DependencyGraph(nodes=list(nodes.values()),edges=edges,circular_dependencies=cycles,statistics={"nodes":len(nodes),"edges":len(edges),"cycles":len(cycles)})
    def _imports(self,text:str)->list[str]: return [x for match in re.finditer(r"(?:from\s+|import\s+)([\w./@-]+)|from\s+['\"]([^'\"]+)",text) for x in match.groups() if x]
    def _resolve(self,path:str,target:str,files:dict[str,str])->str:
        if not target.startswith("."):
            internal=target.replace(".","/")
            for candidate in (internal+".py",internal+".ts",internal+".tsx",internal+"/index.ts"):
                if candidate in files:return candidate
            return target
        base=path.rsplit("/",1)[0] if "/" in path else ""; raw=(base+"/"+target).replace("/./","/")
        while "/../" in raw: raw=re.sub(r"[^/]+/\.\./","",raw)
        for candidate in (raw,raw+".py",raw+".ts",raw+".tsx",raw+"/index.ts"): 
            if candidate in files:return candidate
        return raw
    def _cycles(self,edges:list[GraphEdge])->list[list[str]]:
        graph=defaultdict(list); [graph[e.source].append(e.target) for e in edges]; found=[]; visiting=set(); visited=set()
        def walk(node,path):
            if node in visiting: found.append(path[path.index(node):]+[node]); return
            if node in visited:return
            visiting.add(node)
            for target in graph[node]:walk(target,path+[target])
            visiting.remove(node);visited.add(node)
        for node in list(graph):walk(node,[node])
        return found
    def descendants(self, graph:DependencyGraph, starts:list[str])->dict[str,int]:
        reverse=defaultdict(list)
        for edge in graph.edges: reverse[edge.target].append(edge.source)
        result={}; queue=deque((item,0) for item in starts)
        while queue:
            current,depth=queue.popleft()
            if current in result and result[current]<=depth:continue
            result[current]=depth; queue.extend((next_node,depth+1) for next_node in reverse[current])
        return result
