from collections import Counter,defaultdict
import bisect
import difflib
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys

work=Path(__file__).resolve().parent
archive=Path("/home/linhao/Toolchain/development/llvm-optimize/archive")
historical=archive/"task145"
source=archive/"task144/source-c2/clang/lib/Driver/Driver.cpp"
sys.path.insert(0,str(historical))
from elf_analysis import Elf,SY,normalize

d=work/"driver"
pc_rx=re.compile(r"^\s+([0-9a-f]+):\s+(\S.*)")
section_rx=re.compile(r"^Disassembly of section (.*):$")
constructor_prefix=".text._ZN5clang6driver6DriverC2EN4llvm"
literal_symbol=re.compile(rb"\.L\.str(?:\.\d+)?$")
RA=struct.Struct("<QQq")
string_sections=[".rodata.str1.1",".rodata.str1.8",".debug_str",".debug_line_str",".strtab"]

def parse(raw):
    result=defaultdict(list)
    sec=None
    for line in raw.read_text().splitlines():
        if m:=section_rx.fullmatch(line):
            sec=m[1]
        elif sec and line.startswith((" ","\t")):
            result[sec].append(line.strip())
    return result
def addressed(p):
    rows=[]
    for line in p.read_text().splitlines():
        if m:=pc_rx.fullmatch(line):
            if not m[2].startswith("R_X86_64_"):
                rows.append((int(m[1],16),m[2].strip()))
    return rows
def changes(before,after):
    l=[normalize(s) for s in before]
    r=[normalize(s) for s in after]
    return [{"kind":kind,"old_pos":i,"new_pos":j,"old":before[i:x],"new":after[j:y],
             "old_normalized":l[i:x],"new_normalized":r[j:y]}
            for kind,i,x,j,y in difflib.SequenceMatcher(None,l,r,autojunk=False).get_opcodes() if kind!="equal"]
def ar_record(p):
    with p.open("rb") as f:
        return {"path":str(p),"sha256":hashlib.file_digest(f,"sha256").hexdigest(),"bytes":p.stat().st_size}
def str_values(elf,table):
    v=elf.section(table)
    return Counter(v[:-1].split(b"\0")) if v else Counter()
def strdiff(elfs):
    result={}
    for table in string_sections:
        a,b=(str_values(e,table) for e in elfs)
        diff_a=a-b; diff_b=b-a
        result[table]={"old_entries":sum(a.values()),"new_entries":sum(b.values()),"values_removed":sum(diff_a.values()),
                       "values_added":sum(diff_b.values()),"old_only":[x.decode(errors="replace") for x in diff_a.elements()],
                       "new_only":[x.decode(errors="replace") for x in diff_b.elements()],
                       "all_changed_values_are_local_string_numbers":bool(diff_a or diff_b) and
                       all(literal_symbol.fullmatch(x) for x in diff_a.keys()|diff_b.keys())}
    return result
def read_syms(elf):
    sec=elf.raw[elf.names.index(".symtab")]
    names=elf.payload(sec[6])
    data=elf.section(".symtab")
    return [(Elf.string(names,p[0]),*p[1:]) for p in SY.iter_unpack(data)]
def offset_in_insns(addresses,offset):
    if addresses is None:
        return offset
    i=bisect.bisect_right(addresses,offset)-1
    if i<0: raise RuntimeError(f"cannot map relocation offset {offset}")
    return [i,offset-addresses[i]]
def relocations(elf,ctor_addresses):
    result=defaultdict(list)
    syms=read_syms(elf)
    for num,sh in enumerate(elf.raw):
        n=elf.names[num]
        if sh[1]!=4: continue
        target=elf.raw[sh[7]]
        if not target[2]&2: continue
        name=elf.names[sh[7]]
        positions=ctor_addresses if name.startswith(constructor_prefix) else None
        for addr,info,addend in RA.iter_unpack(elf.payload(num)):
            ni,kind=info>>32,info&0xffffffff
            sym,data,other,section,value,size=syms[ni]
            dest=elf.names[section] if 0<section<len(elf.raw) else None
            if dest and dest.startswith(".rodata.str") and data&0xf in (0,1,3):
                bias=4 if kind in (2,4) else 0
                base=elf.payload(section)
                start=value+addend+bias
                if start<0 or start>=len(base):
                    ref=["outside-string-table",dest,sym,addend]
                else:
                    off=base.find(b"\0",start)
                    if off<0: raise RuntimeError(f"unterminated relocation string {sym}")
                    ref=["literal",base[start:off].decode(errors="replace")]
            else:
                ref=["symbol",sym,dest,addend]
            result[name].append({"at":offset_in_insns(positions,addr),"kind":kind,"target":ref})
    return dict(result)

def main():
    old,new=d/"old.o",d/"new.o"
    expected=json.loads((historical/"r-ps4-source-line-evidence.json").read_text())["archive"]
    obj=[ar_record(old),ar_record(new)]
    assert [r["sha256"] for r in obj]==[expected["diff"][0][k][0]["sha256"] for k in ("old","new")]
    maps=[parse(d/(side+".all.txt")) for side in ("old","new")]
    instructions={}
    for k in sorted(maps[0].keys()|maps[1].keys()):
        a=maps[0].get(k,[]); b=maps[1].get(k,[])
        if [normalize(s) for s in a]!=[normalize(s) for s in b]:
            instructions[k]=changes(a,b)
    addressed_rows=[addressed(d/(side+".constructor.txt")) for side in ("old","new")]
    with Elf(old) as l,Elf(new) as r:
        a,b=l.fingerprints(),r.fingerprints()
        sec=[k for k in sorted(a.keys()|b.keys()) if a.get(k)!=b.get(k)]
        strs=strdiff((l,r))
        rl,rr=(relocations(e,[x[0] for x in insts]) for e,insts in zip((l,r),addressed_rows,strict=True))
    reloc={k:{"old":rl.get(k),"new":rr.get(k)} for k in sorted(rl.keys()|rr.keys()) if rl.get(k)!=rr.get(k)}
    want_a=["movq\t$0x0, 0x4b8(%rbx)","movb\t$0x0, 0x4c0(%rbx)"]
    want_b=["movl\t$0x646c6c, 0x4c0(%rbx)  # imm = 0x646C6C","movq\t$0x3, 0x4b8(%rbx)"]
    ctor_only=len(instructions)==1 and list(instructions)[0].startswith(constructor_prefix)
    delta=next(iter(instructions.values()),[])
    exact_literals=(len(delta)==1 and delta[0]["old"]==want_a and delta[0]["new"]==want_b)
    valid_strings=all((not r["values_removed"] and not r["values_added"]) or
                      k==".strtab" and r["all_changed_values_are_local_string_numbers"] for k,r in strs.items())
    passed=ctor_only and exact_literals and valid_strings and not reloc
    evidence={"status":"PASS" if passed else "UNCLASSIFIED","input_members":obj,
              "other_members_unchanged_in_145":expected["members_before"]-1,
              "exec_sections_compared":len(maps[0].keys()|maps[1].keys()),
              "instruction_diffs":instructions,"changed_elf_sections":sec,
              "allocated_relocation_sections_compared":len(rl.keys()|rr.keys()),
              "semantic_allocated_relocation_differences":reloc,"string_tables":strs,
              "source":str(source),"source_lines":[(i,x.rstrip()) for i,x in enumerate(source.open(),1) if "PreferredLinker(CLANG_DEFAULT_LINKER)" in x],
              "constructor_literal_bytes":struct.pack("<I",0x646c6c).hex(),
              "constructor_literal_length":3}
    (work/"driver-v2.json").write_text(json.dumps(evidence,indent=2,ensure_ascii=False)+"\n")
    print({k:v for k,v in evidence.items() if k not in ("instruction_diffs","semantic_allocated_relocation_differences","string_tables")},flush=True)
main()
