from collections import defaultdict
from itertools import zip_longest
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import traceback

from elf_analysis import COLD, Elf, SY, normalize, compared, run

A=Path("/home/linhao/Toolchain/development/llvm-optimize/archive/task144")
BASE=Path(__file__).resolve().parent
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

try:
    d=BASE/"classify-first-a1/r-id2-clang-22"
    left=d/"old.disassembly.txt"
    right=d/"new.disassembly.txt"
    for p in (d/"old.with-symbols",d/"new.with-symbols",left,right):
        if not p.is_file():
            raise RuntimeError(f"missing first-pass data {p}")
    a,ac=get_rows(d/"old.with-symbols",left)
    print("PS5 mapped",ac,flush=True)
    b,bc=get_rows(d/"new.with-symbols",right)
    print("C2 mapped",bc,flush=True)
    result=compared(a,b,left,right,True)
    result["coverage"]={"old":ac,"new":bc}
    result["input_required_option"]="--no-leading-addr"
    result["cross_check_option"]="--full-leading-addr"
    result["verification"]="the two streams match instruction for instruction after removing the cross-check address field"
    status="STOP" if result["different"] or ac["unrepresented_ranges"] or bc["unrepresented_ranges"] else "PASS"
    if status=="STOP":
        stop=f"STOP R-ID2: {result['different']} of {result['compared']} function keys differ after address normalization and cold-fragment merging"
        (OUT/"STOP.txt").write_text(stop+"\n")
        print(stop,flush=True)
    result["status"]=status
    (OUT/"r-id2-symbol-ranges.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    (OUT/"result.json").write_text(json.dumps({k:result[k] for k in
        ("status","compared","different","equal","old_only","new_only","coverage")},indent=2)+"\n")
    sys.exit(status!="PASS")
except Exception:
    (OUT/"preparation-STOP.txt").write_text(traceback.format_exc())
    (OUT/"result.json").write_text(json.dumps({"status":"STOP","kind":"preparation","error":traceback.format_exc()})+"\n")
    raise
