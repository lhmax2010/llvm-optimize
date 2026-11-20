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
from elf_analysis import COLD, Elf, SY, normalize as original_normalize, merge, run
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

def main():
    d=BASE/"classify-first-a1/r-id2-clang-22"
    old=d/"old.disassembly.txt"
    new=d/"new.disassembly.txt"
    a,ac=get_rows(d/"old.with-symbols",old)
    print("PS5 mapped",ac,flush=True)
    b,bc=get_rows(d/"new.with-symbols",new)
    print("C2 mapped",bc,flush=True)
    left,right=merge(a,True),merge(b,True)
    old_data=old.read_bytes()
    new_data=new.read_bytes()
    different=[]
    for section,name in sorted(left.keys()|right.keys()):
        key=section,name
        ls=left.get(key,())
        rs=right.get(key,())
        if signature(old_data,ls)==signature(new_data,rs):
            continue
        a1,b1=insns(old_data,ls),insns(new_data,rs)
        rows=diff_lines(a1,b1)
        if not rows:
            raise RuntimeError(f"hash compare differs without an instruction change {key}")
        different.append({"section":section,"function":name,"before_count":len(a1),"after_count":len(b1),
                          "old_spans":ls,"new_spans":rs,"changes":rows})
    # Names and function identities are kept intact. Only instruction operands change.
    proc=subprocess.run(["/usr/bin/c++filt"],input="".join(d["function"]+"\n" for d in different),
                        text=True,capture_output=True,check=True)
    for d,pretty in zip(different,proc.stdout.splitlines(),strict=True):
        d["demangled"]=pretty
        d["driver_function"]=(pretty.startswith("clang::driver::") or pretty.startswith("clang_main(") or
                              pretty.startswith("non-virtual thunk to clang::driver::"))
    counted=len(left.keys()|right.keys())
    universe=json.loads((BASE/"exact-first-a1/result.json").read_text())
    if counted!=universe["compared"] or any(s["unrepresented_ranges"] for s in (ac,bc)):
        raise RuntimeError(f"v2 function coverage changed: {counted}, {ac}, {bc}")
    report={"coverage":{"old":ac,"new":bc},"compared":counted,"equal":counted-len(different),
            "different":len(different),"old_only":len(left.keys()-right.keys()),"new_only":len(right.keys()-left.keys()),
            "non_driver":sum(not x["driver_function"] for x in different),"difference_details":different,
            "normalization":["145 address and offset substitutions","local literal symbols","ThinLTO local symbol suffixes",
                             "nearest-symbol plus hexadecimal or decimal offset annotations"]}
    (OUT/"clang-v2-disassembly.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
    print({k:v for k,v in report.items() if k not in ("coverage","difference_details")},flush=True)

try:
    main()
except Exception:
    (OUT/"clang-v2-preparation-STOP.txt").write_text(traceback.format_exc())
    raise
