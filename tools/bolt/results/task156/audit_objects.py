from pathlib import Path
import json
import re
import subprocess

A=Path(__file__).resolve().parent
E=A/"evidence"
result=json.loads((A/"pilot/results.json").read_text())
variants=json.loads((E/"variants.json").read_text())
section_re=re.compile(r"(?m)^\s*\[\s*\d+\]\s+\.GCC\.command\.line\s+\S+\s+[0-9a-f]+\s+([0-9a-f]+)\s+([0-9a-f]+)\s")
old,new=(variants[k]["loader"].encode() for k in ("V0","V1"))

def span(obj):
    rs=subprocess.check_output(["/usr/bin/readelf","-W","-S",str(obj)],text=True)
    match=section_re.search(rs)
    return tuple(int(x,16) for x in match.groups()) if match else None

def equal_stream(a,b,length=None):
    while length is None or length:
        n=1024*1024 if length is None else min(1024*1024,length)
        lhs,rhs=a.read(n),b.read(n)
        if lhs!=rhs:
            return False
        if not lhs:
            return length in (None,0)
        if length is not None:
            length-=len(lhs)
    return True

rows=[]
for pair in result["rounds"][0]["comparisons"]:
    if pair["status"]!="DIFFERENT":
        continue
    a=Path(pair["baseline"]["path"])
    b=Path(pair["candidate"]["path"])
    sa,sb=span(a),span(b)
    row={"tu":pair["tu"],"raw_status":pair["status"],"loader_path_only":False,"section_span":sa}
    if sa and sa==sb:
        off,size=sa
        with a.open("rb") as x,b.open("rb") as y:
            before=equal_stream(x,y,off)
            x.seek(off)
            y.seek(off)
            before_path,after_path=x.read(size),y.read(size)
            replaced=(before_path.count(old)==1 and after_path.count(new)==1
                      and before_path.replace(old,new,1)==after_path)
            after=equal_stream(x,y)
        row.update(loader_path_only=bool(before and after and replaced),
                   equal_before_section=before,equal_after_section=after,
                   encoded_loader_paths_match=replaced)
    rows.append(row)
out={"method":"Compare all bytes, with exactly one replacement of the V0 loader path by the V1 loader path inside .GCC.command.line. Read-only diagnostic.",
     "raw_different":len(rows),"loader_path_only":sum(r["loader_path_only"] for r in rows),"rows":rows}
(E/"pilot-object-attribution.json").write_text(json.dumps(out,indent=2)+"\n")
print(out["raw_different"],out["loader_path_only"])
