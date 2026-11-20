from collections import Counter
from pathlib import Path
import hashlib
import json
import re
import struct
import subprocess
import sys
import traceback
import zlib

root=Path("/home/linhao/Toolchain/development/llvm-optimize/archive")
prior=root/"task145"
historic=root/"task144"
out=Path(__file__).resolve().parent
sys.path.insert(0,str(prior))
from elf_analysis import Elf, compared, disassemble, is_elf, symbols, unit_names

toolroot=historic/"b1-a1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr"
base=[toolroot/"lib64/ld-linux-x86-64.so.2","--library-path",toolroot/"lib64"]
objdump=[*base,toolroot/"bin/llvm-objdump"]
dwarfdump=[*base,toolroot/"bin/llvm-dwarfdump"]
err=out/"rpm-llvm-stderr.txt"
err.touch()
source=historic/"b1-audit/comparison"
PREFIXES=(b"/usr/src/debug/llvm-22.1.8-2.1.x86_64",b"/usr/src/debug/llvm-22.1.8-1.x86_64")
PREFIX=b"/usr/src/debug/llvm-22.1.8-RELEASE.x86_64"
ALLOW={".note.gnu.build-id",".dynamic",".dynsym",".dynstr",".got",".got.plt",".rela.dyn",".rela.plt",
       ".shstrtab",".gnu.hash",".hash"}
def dump(name,r):
    (out/name).write_text(json.dumps(r,indent=2,ensure_ascii=False)+"\n")
def prefix(value):
    for text in PREFIXES:
        value=value.replace(text,PREFIX)
    return value
def digest(p):
    with p.open("rb") as f:
        return hashlib.file_digest(f,"sha256").hexdigest()
def pkgpath(package,side,path):
    return source/side/"-".join(package)/path.removeprefix("/")
def debug_image(pkg,side,path):
    return pkgpath((pkg[0]+"-debuginfo",pkg[1]),side,"/usr/lib/debug"+path+".debug")
def normhash(items):
    h=hashlib.sha256()
    for k in sorted(items):
        h.update(struct.pack("<Q",len(k)))
        h.update(k)
    return h.hexdigest()
def values_pair(a,b):
    return {"before_count":len(a),"after_count":len(b),"before_sha256":normhash(a),"after_sha256":normhash(b),
            "only_before":len(a-b),"only_after":len(b-a),
            "before_raw_examples":[x.decode("utf-8","replace") for x in sorted(a-b)[:12]],
            "after_raw_examples":[x.decode("utf-8","replace") for x in sorted(b-a)[:12]]}
def section_strings(elf,name):
    if name not in elf.names:
        if name.replace(".debug_",".zdebug_",1) in elf.names:
            name=name.replace(".debug_",".zdebug_",1)
        else:
            return b"",False
    idx=elf.names.index(name)
    data=elf.payload(idx)
    if elf.raw[idx][2]&0x800:
        kind,zero,size,align=struct.unpack_from("<IIQQ",data)
        if kind!=1 or zero:
            raise RuntimeError(f"unexpected compressed string table {elf.path}:{name}")
        data=zlib.decompress(data[24:])
        if len(data)!=size: raise RuntimeError(f"size mismatch {elf.path}:{name}")
    elif name.startswith(".zdebug_"):
        if not data.startswith(b"ZLIB"): raise RuntimeError(f"bad GNU debug compression {elf.path}:{name}")
        size=int.from_bytes(data[4:12],"big"); data=zlib.decompress(data[12:])
        if len(data)!=size: raise RuntimeError(f"size mismatch {elf.path}:{name}")
    return data,True
def strings_pair(l,r,name):
    a,ap=section_strings(l,name); b,bp=section_strings(r,name)
    x=a.split(b"\0") if ap else []
    y=b.split(b"\0") if bp else []
    if ap and x[-1]!=b"" or bp and y[-1]!=b"":
        raise RuntimeError(f"unterminated string table {name}")
    if ap: x.pop()
    if bp: y.pop()
    xx=set(map(prefix,x))
    yy=set(map(prefix,y))
    return {**values_pair(xx,yy),"before_entries":len(x),"after_entries":len(y),
            "before_prefixed_entries":sum(any(v in row for v in PREFIXES) for row in x),
            "after_prefixed_entries":sum(any(v in row for v in PREFIXES) for row in y),
            "section_present_before":ap,"section_present_after":bp,
            "equal":xx==yy}
def id3b(l,r):
    a,an=unit_names(dwarfdump,l,err)
    b,bn=unit_names(dwarfdump,r,err)
    na={prefix(row.encode()) for row in a}
    nb={prefix(row.encode()) for row in b}
    cu={**values_pair(na,nb),"before_cus":an,"after_cus":bn,
        "raw_unique_before":len(a),"raw_unique_after":len(b),"equal":bool(na and nb and na==nb)}
    with Elf(l) as left,Elf(r) as right:
        tables={name:strings_pair(left,right,name) for name in (".debug_str",".debug_line_str")}
    return cu["equal"] and all(x["equal"] for x in tables.values()),{"cu":cu,"strings":tables}
def debuglink(e):
    raw=e.section(".gnu_debuglink")
    if not raw: return None,None
    name,_,tail=raw.partition(b"\0")
    pos=(len(name)+4)//4*4
    if not name or len(raw)!=pos+4 or any(raw[len(name):pos]):
        raise RuntimeError(f"bad .gnu_debuglink: {e.path}")
    return name,int.from_bytes(raw[pos:pos+4],"little")
def code_section_comparison(l,r,dl,dr,idx):
    d=out/f"id1b-{idx}"
    d.mkdir()
    sides=[]
    for side,p,dbg in (("old",l,dl),("new",r,dr)):
        raw=d/(side+".disassembly.txt")
        image=d/(side+".symbols")
        if not dbg.is_file():
            return False,{"error":"matching debug symbol table missing"}
        funcs=symbols(p,dbg,image)
        rows,cov=disassemble(objdump,image,funcs,raw,err)
        sides.append((rows,cov,raw))
    (ls,lc,lf),(rs,rc,rf)=sides
    q=compared(ls,rs,lf,rf,False)
    q["coverage"]={"old":lc,"new":rc}
    ok=q["compared"]>0 and not q["different"] and all(
        x["function_symbols"] and not x["function_addresses_without_matching_named_block"] for x in (lc,rc))
    dump(f"id1b-{idx}-disassembly.json",q)
    return ok,q
def id1b(row,l,r):
    a=row["original"]; path=a["path"]; pkg=a["rpm"]; idx=row["index"]
    dl=debug_image(pkg,"old",path)
    dr=debug_image(pkg,"new",path)
    with Elf(l) as left,Elf(r) as right:
        ln,lc=debuglink(left)
        rn,rc=debuglink(right)
        pair=(left.id(),right.id())
        lf,rf=left.fingerprints(),right.fingerprints()
    member=dr.with_name(rn.decode("utf-8","surrogateescape")) if rn else dr
    if member!=dr and member.is_file() and not member.is_symlink(): dr=member
    computed=None
    if dr.is_file() and not dr.is_symlink():
        computed=0
        with dr.open("rb") as f:
            while chunk:=f.read(1024**2):
                computed=zlib.crc32(chunk,computed)
    diffs=sorted(name for name in lf.keys()|rf.keys() if lf.get(name)!=rf.get(name))
    excluded=[s for s in diffs if s!=".gnu_debuglink" and s not in ALLOW and not s.startswith(".gnu.version")]
    # In earlier rows with frame differences an independent outside-whitelist
    # difference is always recorded before making a decision about frame fields.
    basis={"before_debuglink":ln.decode(errors="replace") if ln else None,"after_debuglink":rn.decode(errors="replace") if rn else None,
           "before_crc":f"{lc:08x}" if lc is not None else None,"after_crc":f"{rc:08x}" if rc is not None else None,
           "recomputed_c2_debug_file":str(dr),"recomputed_c2_crc":f"{computed:08x}" if computed is not None else None,
           "filenames_equal":bool(ln and rn and ln==rn),
           "c2_crc_match":computed is not None and rc==computed,
           "build_id_before":pair[0],"build_id_after":pair[1],
           "section_differences":diffs,"unapproved_or_unproven_sections":excluded}
    passed=basis["filenames_equal"] and basis["c2_crc_match"] and not pair[0] and bool(pair[1]) and not excluded
    if passed:
        passed,proof=code_section_comparison(l,r,dl,dr,idx)
        basis["instruction_comparison"]={k:proof[k] for k in ("compared","different","equal","coverage","error") if k in proof}
        if "compared" in proof: basis["instruction_comparison_file"]=f"id1b-{idx}-disassembly.json"
    else:
        basis["instruction_comparison"]="not entered: at least one frozen prerequisite failed"
    return passed,basis
def config(row,l,r):
    a,b=l.read_bytes(),r.read_bytes()
    variants=[(b'set(CLANG_DEFAULT_LINKER "")',b'set(CLANG_DEFAULT_LINKER "lld")'),
              (b'#define CLANG_DEFAULT_LINKER ""',b'#define CLANG_DEFAULT_LINKER "lld"')]
    src=historic/"ps4-parent-vs-ps5.diff"
    matches=[(i,x.rstrip()) for i,x in enumerate(src.open(),1) if x.startswith("+") and "-DCLANG_DEFAULT_LINKER=lld" in x]
    valid=any(a.count(old)==1 and a.replace(old,new,1)==b for old,new in variants) and len(matches)==1
    return valid,{"source_diff":str(src),"added_lines":matches,"raw_diff":row["basis"]["raw_diff"],
                  "literal_substitution_reproduces_full_file":bool(valid)}
def main():
    rows=json.loads((prior/"unclassified-final.json").read_text())
    assert len(rows)==269
    results=[]
    for item in rows:
        if item["rule"]=="R-ID2" or item["original"]["path"].endswith("/libclangDriver.a"):
            continue
        original=item["original"]; path=original["path"]; package=original["rpm"]
        left=pkgpath(package,"old",path); right=pkgpath(package,"new",path)
        if digest(left)!=original["before"]["sha256"] or digest(right)!=original["after"]["sha256"]:
            raise RuntimeError(f"RPM member identity mismatch: {left}, {right}")
        source_rule=item["rule"]
        passed,evidence={"R-ID1":lambda:id1b(item,left,right),"R-ID3":lambda:id3b(left,right),
                         "R-PS4":lambda:config(item,left,right)}[source_rule]()
        result={"index":item["index"],"rule":source_rule+"b","result":"PASS" if passed else "UNCLASSIFIED",
                "proof":evidence,"original":original}
        with (out/"rpm-v2-in-progress.jsonl").open("a") as f:
            f.write(json.dumps(result,ensure_ascii=False)+"\n")
        results.append(result)
        if len(results)%20==0:
            print("Completed",len(results),flush=True)
    dump("rpm-v2-results.json",results)
    print(Counter((d["rule"],d["result"]) for d in results),flush=True)
try:
    main()
except Exception:
    (out/"rpm-v2-preparation-STOP.txt").write_text(traceback.format_exc())
    raise
