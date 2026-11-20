from collections import defaultdict
from itertools import zip_longest
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import traceback

sys.path.insert(0,str(Path("/home/linhao/Toolchain/development/llvm-optimize/archive/task145")))
from elf_analysis import COLD, Elf, SY, normalize as original_normalize, merge, run, symbols
import zlib
import difflib

A=Path("/home/linhao/Toolchain/development/llvm-optimize/archive/task144")
BASE=Path("/home/linhao/Toolchain/development/llvm-optimize/archive/task145")
OUT=Path(sys.argv[1])
toolroot=A/"b1-a1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr"
objdump=[toolroot/"lib64/ld-linux-x86-64.so.2","--library-path",toolroot/"lib64",toolroot/"bin/llvm-objdump"]
options=["-d","--no-show-raw-insn","--symbolize-operands"]
PC=re.compile(rb"^\s+([0-9a-fA-F]+):\s+(\S.*)")
SECTION=b"Disassembly of section "
err=OUT/"llvm-objdump-stderr.txt"

def functions(image):
    by_section=defaultdict(lambda:defaultdict(set))
    with Elf(image) as elf:
        index=elf.names.index(".symtab")
        sym=elf.raw[index]
        st=elf.payload(sym[6])
        for offset in range(0,sym[5],SY.size):
            name,info,_,section,start,size=SY.unpack_from(elf.data,sym[4]+offset)
            if info&15!=2 or not 0<section<len(elf.raw) or not name or not size:
                continue
            if not elf.raw[section][2]&4:
                continue
            value=Elf.string(st,name)
            by_section[elf.names[section]][(start,start+size)].add(value)
    return by_section

def no_pc(path):
    pos=0
    with path.open("rb") as raw:
        for line in raw:
            if line.startswith((b" ",b"\t")) and line.strip():
                yield pos,pos+len(line),line.strip()
            pos+=len(line)

def leading(path):
    current=None
    command=[*objdump,*options,"--full-leading-addr",path]
    for raw in run(command,err):
        if raw.startswith(SECTION):
            current=raw[len(SECTION):].decode().strip().removesuffix(":")
        elif (m:=PC.match(raw)):
            yield current,int(m[1],16),m[2].strip()

def get_rows(image,raw):
    by_section=functions(image)
    rows=defaultdict(list)
    cur=None
    previous=-1
    pending=iter(())
    next_item=None
    active=[]
    counts=defaultdict(int)
    def finish(record):
        start,end,names,h,count,first,last=record
        if not count:
            counts["undecoded_ranges"]+=1
            return
        if first is None or last is None:
            raise RuntimeError("unexpected empty instruction offsets")
        for name in sorted(names):
            rows[(cur,name)].append((h.hexdigest(),count,first,last))
    for p,q in zip_longest(leading(image),no_pc(raw)):
        if p is None or q is None or p[2]!=q[2]:
            raise RuntimeError(f"address-annotated and required disassembly streams diverge: {p!r} {q!r}")
        section,addr,text=p
        first,last,_=q
        if section!=cur:
            for record in active:
                finish(record)
            cur=section
            previous=-1
            pending=iter(sorted(by_section.get(section,{}).items()))
            next_item=next(pending,None)
            active=[]
        if previous>=addr:
            raise RuntimeError(f"non-increasing addresses {section}:{addr:#x} after {previous:#x}")
        previous=addr
        if active and any(rec[1]<=addr for rec in active):
            for rec in active:
                if rec[1]<=addr:
                    finish(rec)
            active=[r for r in active if r[1]>addr]
        while next_item and next_item[0][0]<=addr:
            (start,end),names=next_item
            next_item=next(pending,None)
            if end<=addr:
                counts["undecoded_ranges"]+=1
                continue
            active.append([start,end,names,hashlib.sha256(),0,None,None])
        if not active:
            counts["outside_function_ranges"]+=1
            continue
        norm=(normalize(text.decode("utf-8","replace"))+"\n").encode()
        for rec in active:
            rec[3].update(norm)
            if not rec[4]:
                rec[5]=first
            rec[4]+=1
            rec[6]=last
        counts["within_function_ranges"]+=1
    for rec in active:
        finish(rec)
    counts["distinct_symbol_ranges"]=sum(len(v) for v in by_section.values())
    counts["distinct_symbol_names"]=sum(len(names) for v in by_section.values() for names in v.values())
    counts["named_functions"]=len(rows)
    counts["cold_named_functions"]=sum(bool(COLD.fullmatch(name)) for section,name in rows if section!=".bolt.org.text")
    # Account for overlaps and a trailing zero-filled symbol range as well.
    counts["unrepresented_ranges"]=counts["distinct_symbol_ranges"]-len({(k[0],start,end) for k, spans in rows.items() for _,_,start,end in spans})
    return rows,dict(counts)

ANNOTATION = re.compile(r"<([^<>]+)>")
LOCAL_LITERAL = re.compile(r"^(?:\.str|\.L\.str|\.Lstr)")
THIN_LOCAL = re.compile(r"\.llvm\.\d+$")
NEAREST = re.compile(r".+\+(?:0x[0-9a-fA-F]+|\d+)$")

def normalize(line):
    def symbol(match):
        value=match[1]
        if LOCAL_LITERAL.search(value) or THIN_LOCAL.search(value) or NEAREST.fullmatch(value):
            return "<ADDR>"
        return match[0]
    return original_normalize(ANNOTATION.sub(symbol,line))

def insns(data,parts):
    return [raw.decode("utf-8","replace").strip()
            for _,_,start,end in parts for raw in data[start:end].splitlines()
            if raw.startswith((b" ",b"\t")) and raw.strip()]

def signature(data,parts):
    if len(parts)==1:
        return parts[0][:2]
    items=insns(data,parts)
    result=hashlib.sha256()
    for text in items:
        result.update((normalize(text)+"\n").encode())
    return result.hexdigest(),len(items)

def diff_lines(a,b):
    x,y=list(map(normalize,a)),list(map(normalize,b))
    return [{"kind":kind,"before_at":i,"after_at":j,"before_raw":a[i:v],"after_raw":b[j:w],
             "before_normalized":x[i:v],"after_normalized":y[j:w]}
            for kind,i,v,j,w in difflib.SequenceMatcher(None,x,y,autojunk=False).get_opcodes() if kind!="equal"]

def crc(path):
    value=0
    with path.open("rb") as f:
        while chunk:=f.read(2**20):
            value=zlib.crc32(chunk,value)
    return value

def sha(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f,"sha256").hexdigest()

def match_debug(exe,folder):
    with Elf(exe) as elf:
        d=elf.section(".gnu_debuglink")
        label=d.split(b"\0",1)[0]
        offset=(len(label)+4)//4*4
        value=int.from_bytes(d[offset:offset+4],"little")
        expected_id=elf.id()
    choices=[p for p in folder.rglob(label.decode()) if p.is_file() and not p.is_symlink()]
    paired=[q for q in choices if crc(q)==value]
    if len(paired)!=1:
        raise RuntimeError(f"expected one .debug with debuglink crc {value:08x}: {exe}, {paired}, candidates={choices}")
    with Elf(paired[0]) as debug:
        if debug.id()!=expected_id:
            raise RuntimeError(f"GNU build-id identity error {paired[0]}")
    return paired[0],f"{value:08x}"

def compare_file(row):
    orig=row["original"]; idx=row["index"]; actual=orig["path"]
    pkg,arch=orig["rpm"]
    w=OUT/"binaries"/str(idx)
    w.mkdir(parents=True)
    rows=[]
    raw=[]
    proof={}
    for side,key in (("old","before"),("new","after")):
        parent=A/"b1-audit/comparison"/side
        image=parent/(pkg+"-"+arch)/actual.removeprefix("/")
        if sha(image)!=orig[key]["sha256"]:
            raise RuntimeError(f"RPM input SHA mismatch {image}")
        dbg, crc32=match_debug(image,parent/(pkg+"-debuginfo-"+arch))
        if (w/(side+".symbols")).exists():
            raise RuntimeError("output already exists")
        fused=w/(side+".symbols")
        symbols(image,dbg,fused)
        dis=w/(side+".disassembly.txt")
        argv=[*objdump,*options,"--no-leading-addr",fused]
        with dis.open("wb") as out:
            for text in run(argv,err):
                out.write(text)
        current,coverage=get_rows(fused,dis)
        print(idx,side,coverage["distinct_symbol_ranges"],"ranges",coverage["unrepresented_ranges"],"unrepresented",flush=True)
        rows.append(merge(current,False))
        raw.append(dis)
        proof[side]={"elf":str(image),"elf_sha256":orig[key]["sha256"],"debug":str(dbg),
                     "debug_crc32":crc32,"coverage":coverage,"disassembly_argv":list(map(str,argv))}
    left,right=rows
    data=None
    different=[]
    keys=left.keys()|right.keys()
    for section,name in sorted(keys):
        key=section,name
        ls=left.get(key,())
        rs=right.get(key,())
        if [(h,n) for h,n,*_ in ls]==[(h,n) for h,n,*_ in rs]:
            continue
        if data is None:
            data=[q.read_bytes() for q in raw]
        a1,b1=insns(data[0],ls),insns(data[1],rs)
        changes=diff_lines(a1,b1)
        if not changes:
            raise RuntimeError(f"instruction partition mismatch without differing instruction text {idx} {key}")
        different.append({"section":section,"function":name,"before_count":len(a1),"after_count":len(b1),
                          "raw_spans_old":ls,"raw_spans_new":rs,"changes":changes})
    pretty=subprocess.run(["/usr/bin/c++filt"],input="".join(x["function"]+"\n" for x in different),
                         text=True,capture_output=True,check=True).stdout.splitlines()
    for record,human in zip(different,pretty,strict=True): record["display_name"]=human
    result={"index":idx,"path":actual,"compared":len(keys),"same":len(keys)-len(different),
            "different":len(different),"old_only":len(left.keys()-right.keys()),
            "new_only":len(right.keys()-left.keys()),"identity_and_coverage":proof,
            "changed_functions":different}
    if any(x["coverage"]["unrepresented_ranges"] for x in proof.values()):
        result["coverage_warning"]="some sized function ranges have no decoded instruction"
    (w/"comparison.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    return {k:v for k,v in result.items() if k not in ("identity_and_coverage","changed_functions")}

def main():
    source=Path("/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/task146/unclassified-v2.json")
    entries=[x for x in json.loads(source.read_text()) if x["rule"]=="R-ID1b" and
                 {".relro_padding",".text"}<=set(x["proof"]["section_differences"])]
    if len(entries)!=14: raise RuntimeError(f"expected 14 original entries, got {len(entries)}")
    outcomes=[]
    # Small files first, so coverage and provenance checks land early.
    for row in sorted(entries,key=lambda x:x["original"]["after"]["bytes"]):
        idx=row["index"]
        try:
            out=compare_file(row)
        except Exception:
            stop=traceback.format_exc()
            (OUT/"binaries"/str(idx)/"STOP.txt").write_text(stop)
            out={"index":idx,"path":row["original"]["path"],"status":"STOP","error":stop}
        outcomes.append(out)
        with (OUT/"b-progress.jsonl").open("a") as f: f.write(json.dumps(out,ensure_ascii=False)+"\n")
        print(out,flush=True)
    (OUT/"b-summary.json").write_text(json.dumps(sorted(outcomes,key=lambda x:x["index"]),indent=2,ensure_ascii=False)+"\n")
if __name__=="__main__":
    main()
