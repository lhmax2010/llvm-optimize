import bz2
import gzip
import hashlib
import json
import lzma
import os
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
from xml.parsers import expat

W=Path("/home/linhao/Toolchain/development/llvm-optimize")
A=W/"archive/task152"
E=A/"evidence"
NAMES={"clang-analyzer","llvm-xray","llvm-prof-tools"}
RICH=re.compile(r"(?<![\w.+-])(?:clang-analyzer|llvm-xray|llvm-prof-tools)(?![\w.+-])")
ROOTS=(W/"archive/task144/b1-a1", W/"archive/task145/b2-first-a1", W/"archive/task145/b2-corrected-a1")
SEARCH=[]
for stage in ROOTS:
    SEARCH.extend((stage/"gbs-driver/local/repos",stage/"gbs-driver/local/cache",
                   stage/"providers",stage/"cache",stage/"gbs-root/local/BUILD-ROOTS"))

def sha(p):
    with p.open("rb") as f:
        return hashlib.file_digest(f,"sha256").hexdigest()

def op(p):
    return {".gz":gzip.open,".bz2":bz2.open,".xz":lzma.open}.get(p.suffix,open)

hits=[]
seen=set()
inventory=[]
def scan_xml(path):
    state={"package":{}, "count":0, "source_count":0, "pending":[], "requires_count":0}
    stack=[]
    def start(name,attr):
        name=name.rsplit("|",1)[-1]
        stack.append(name)
        if name=="package":
            state["package"]={}
            state["pending"]=[]
            state["count"]+=1
        elif name in ("name","arch") and stack[-2:]==["package",name]:
            state["package"][name]=""
        elif name=="version" and stack[-2:]==["package","version"]:
            state["package"]["version"]=attr
        elif name=="entry" and stack[-3:]==["format","requires","entry"]:
            state["requires_count"]+=1
            dep=attr["name"]
            if dep in NAMES or (dep.startswith("(") and RICH.search(dep)):
                state["pending"].append({"line":parser.CurrentLineNumber,"dependency":attr})
    def data(text):
        if len(stack)>1 and stack[-2]=="package" and stack[-1] in ("name","arch"):
            state["package"][stack[-1]]+=text
    def end(name):
        if stack.pop()=="package":
            p=state["package"]
            if p.get("arch") in ("src","nosrc"):
                state["source_count"]+=1
            for row in state["pending"]:
                hits.append({"file":str(path), "package":p,
                             "kind":"BuildRequires" if p.get("arch") in ("src","nosrc") else "Requires", **row})
    parser=expat.ParserCreate(namespace_separator="|")
    parser.StartElementHandler=start
    parser.EndElementHandler=end
    parser.CharacterDataHandler=data
    with op(path)(path,"rb") as stream:
        parser.ParseFile(stream)
    rows=[h for h in hits if h["file"]==str(path)]
    if rows:
        numbers={item["line"] for item in rows}
        with op(path)(path,"rt",encoding="utf-8") as stream:
            raw={i:line.rstrip("\n") for i,line in enumerate(stream,1) if i in numbers}
        for item in rows: item["raw"]=raw[item["line"]]
    return {k:v for k,v in state.items() if k.endswith("count")}

searched=[]
errors=[]
for root in SEARCH:
    found=[]
    if root.is_dir() and root.resolve().is_relative_to(W):
        for directory, dirs, files in os.walk(root,followlinks=False,onerror=lambda e:errors.append(str(e))):
            where=Path(directory)
            dirs[:]=[n for n in dirs if n not in {"BUILD","BUILDROOT","RPMS","SRPMS","SOURCES","usr","proc","sys","dev","home","tmp","lib","lib64","run","root"}]
            if "repomd.xml" not in files or where.name!="repodata":
                continue
            repomd=where/"repomd.xml"
            found.append(str(repomd))
            if repomd in seen: continue
            seen.add(repomd)
            for item in ET.parse(repomd).getroot().findall("{*}data"):
                if item.get("type")!="primary":
                    continue
                href=item.find("{*}location").get("href")
                path=repomd.parent.parent/href
                if not path.is_file() or not path.resolve().is_relative_to(W):
                    errors.append("Primary unavailable: "+str(path))
                    continue
                inventory.append({"repomd":str(repomd),"primary":str(path),"sha256":sha(path),**scan_xml(path)})
    searched.append({"directory":str(root),"exists":root.is_dir(),"repomd":sorted(found)})
src_data=[]
srpms={p for stage in ROOTS for p in stage.glob("gbs-driver/local/repos/*/*/SRPMS/*.rpm")
       if p.resolve().is_relative_to(W)}
for path in sorted(srpms):
    raw=subprocess.check_output(["/usr/bin/rpm","-qp","--requires",str(path)],text=True)
    lines=raw.splitlines()
    match=[line for line in lines if line.split() and (line.split()[0] in NAMES or
           (line.startswith("(") and RICH.search(line)))]
    src_data.append({"path":str(path),"kind":"BuildRequires (source RPM header)", "matches":match,
                     "output":raw})
report={"target_names":sorted(NAMES),"search_roots":searched,"primary_files":inventory,
        "sources":src_data,"hits":hits,"errors":errors}
(E/"dependency-scan.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
print(json.dumps({"files":len(inventory),"unique_primary_hashes":len({i["sha256"] for i in inventory}),
                  "packages":sum(r["count"] for r in inventory),"source_rpms":len(src_data),
                  "hits":hits,"errors":errors},indent=2))
