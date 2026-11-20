from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

a=Path("/home/linhao/Toolchain/development/llvm-optimize/archive/task144")
o=Path(sys.argv[1])
database=json.loads((a/"b1-audit/rpm-unclassified.json").read_text())
kinds={"build-id":re.compile(r"--build-id|build.id",re.I),"Obsoletes":re.compile(r"Obsoletes"),
       "DESTDIR":re.compile("DESTDIR"),"OpenMP compatibility links":re.compile(r"libgomp|libiomp5"),
       "%files":re.compile(r"^[-+]%files"),"clang.cfg/default linker":re.compile(r"clang\.cfg|CLANG_DEFAULT_LINKER|nostart-stop-gc")}
matches={}
for name in ("ps1-ps4.diff","ps4-parent-vs-ps5.diff"):
    file=a/name
    entries=[]
    current=None
    for nr,line in enumerate(file.open(errors="replace"),1):
        if line.startswith("diff --git "): current=line.split()[-1].removeprefix("b/")
        if not current or not current.startswith("packaging/") or not line.startswith(("+","-")) or line.startswith(("+++","---")):
            continue
        found=[k for k,rx in kinds.items() if rx.search(line)]
        if found: entries.append({"line":nr,"file":current,"categories":found,"text":line.rstrip()})
    matches[name]=entries
paths=[r for r in database if r["rpm"]!=["llvm-debugsource","x86_64"]]
unilateral=[r for r in paths if not r["before"] or not r["after"]]
result={"diff_line_index":matches,"removed_or_new_outside_build_id":[r for r in unilateral if "/.build-id" not in r["path"]],
        "r_ps4_clang_cfg_already_excluded_from_509": {
          "file":"/usr/bin/clang.cfg","lines":{"ps4-parent-vs-ps5.diff":[33,34,35,36,37,38,39],
                                            "ps1-ps4.diff":[3424,3426]}}}
old=a/"b1-audit/comparison/old/llvm-static-devel-x86_64/usr/lib64/libclangDriver.a"
new=a/"b1-audit/comparison/new/llvm-static-devel-x86_64/usr/lib64/libclangDriver.a"
def members(p):
    rows=[]
    f=p.open("rb")
    with f:
        if f.read(8)!=b"!<arch>\n": raise RuntimeError(f"unexpected ar format: {p}")
        names=b""
        while h:=f.read(60):
            if len(h)!=60 or h[58:60]!=b"`\n": raise RuntimeError(f"invalid member header {p}")
            size=int(h[48:58])
            name=h[:16].decode().rstrip()
            data=f.read(size)
            if len(data)!=size: raise RuntimeError(f"truncated member {p}")
            if size%2: f.read(1)
            if name=="//":
                names=data
                continue
            if name in ("/","/SYM64/"):
                continue
            if name.startswith("/") and name[1:].isdigit():
                pos=int(name[1:])
                end=names.index(b"/\n",pos)
                name=names[pos:end].decode()
            else:
                name=name.removesuffix("/")
            rows.append({"name":name,"bytes":size,"sha256":hashlib.sha256(data).hexdigest()})
    return rows
l,r=members(old),members(new)
from collections import defaultdict
ma,mb=defaultdict(list),defaultdict(list)
for x in l: ma[x["name"]].append(x)
for x in r: mb[x["name"]].append(x)
result["archive"]={"path":"/usr/lib64/libclangDriver.a","members_before":len(l),"members_after":len(r),
 "diff":[{"name":k,"old":ma[k],"new":mb[k]} for k in sorted(ma.keys()|mb.keys()) if ma[k]!=mb[k]]}
o.write_text(json.dumps(result,indent=2)+"\n")
