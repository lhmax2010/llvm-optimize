from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

a=Path("/home/linhao/Toolchain/development/llvm-optimize/archive/task144")
out=Path(sys.argv[1])
rows=json.loads((a/"b1-a1/evidence/rpms.json").read_text())
binary_rows=[]
hits=[]
raw=[]
for row in rows:
    p=Path(row["path"])
    if p.name.endswith((".src.rpm",".nosrc.rpm")):
        continue
    with p.open("rb") as f:
        digest=hashlib.file_digest(f,"sha256").hexdigest()
    if digest!=row["sha256"]:
        raise RuntimeError(f"RPM input SHA256 differs from B1 receipt: {p}")
    names=subprocess.check_output(["/usr/bin/rpm","-qpl",str(p)],text=True).splitlines()
    matched=[path for path in names if re.search(r"/llvm-bolt(?:\.debug)?$",path)]
    hits.extend({"rpm":str(p),"path":path} for path in matched)
    binary_rows.append({"rpm":str(p),"checked_sha256":digest,"paths":len(names),"exact_tool_matches":matched})
    raw.extend([str(p),*matched])
    if matched:
        raise RuntimeError(f"unexpected packaged llvm-bolt requires extraction: {p}, {matched}")
root=a/"b1-a1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0"
tool=root/"home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-bolt"
service=a/"b1-a1/service.txt"
log=a/"b1-a1/rpm-build.log"
b1=a/"b1-a1"
log_refs=[]
for i,line in enumerate(log.open(errors="replace"),1):
    if "Linking CXX executable bin/llvm-bolt" in line or '"executable_after_sha256"' in line and len(line)<500:
        log_refs.append({"line":i,"text":line.rstrip()})
for i,line in enumerate(service.open(errors="replace"),1):
    if line.startswith("/usr/bin/readelf --wide -d ") and line.rstrip().endswith("/bin/llvm-bolt"):
        log_refs.append({"line":i,"file":str(service),"text":line.rstrip()})
spec=a/"source-c2/packaging/llvm.spec"
spec_ref=[{"file":str(spec),"line":i,"text":line.rstrip()} for i,line in enumerate(spec.open(),1)
          if "ninja -j" in line and "llvm-bolt" in line]
raw_text="STOP B1 NEEDED: the in-tree llvm-bolt is absent from the 22 B1 binary RPM manifests, its original executable was in the cleaned BUILD tree, and the readelf invocation did not preserve stdout."
if tool.exists() or len(binary_rows)!=22:
    raise RuntimeError(f"expected 22 RPMs and no retained BUILD executable: {len(binary_rows)}, {tool}")
result={"status":"STOP","needed":None,"rpm_count":len(binary_rows),"receipt_and_inventory":binary_rows,
        "tool_rpm_matches":hits,"original_tool":str(tool),"retained":False,"readelf_source":log_refs,
        "spec_reference":spec_ref,"stop_original":raw_text}
(out/"b1-needed.json").write_text(json.dumps(result,indent=2)+"\n")
(out/"STOP.txt").write_text(raw_text+"\n")
(out/"result.json").write_text(json.dumps({"status":"STOP","error":raw_text})+"\n")
print(raw_text,flush=True)
sys.exit(1)
