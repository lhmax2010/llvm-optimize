from collections import Counter
import json
from pathlib import Path
import re
import sys
import zlib

A=Path("/home/linhao/Toolchain/development/llvm-optimize/archive/task152")
E=A/"evidence"
sources={
 "llvm::X86::getOpcodeForShortImmediateForm":"X86BoltMnemonicTables.cpp:37–46",
 "llvm::getX86SubSuperRegister":"X86BoltMnemonicTables.cpp:48–50; X86GenSubSuperRegisterBody.inc",
 "llvm::X86_MC::isMemOperand":"X86BoltMnemonicTables.cpp:54–61",
 "llvm::X86_MC::is16BitMemOperand":"X86BoltMnemonicTables.cpp:63–72",
 "llvm::X86_MC::is32BitMemOperand":"X86BoltMnemonicTables.cpp:74–84",
 "llvm::X86_MC::is64BitMemOperand":"X86BoltMnemonicTables.cpp:86–88",
 "llvm::X86_MC::needsAddressSizeOverride":"X86BoltMnemonicTables.cpp:90–93; X86GenNeedsAddressSizeOverrideBody.inc",
 "llvm::InitX86MCRegisterInfo":"X86BoltMnemonicTables.cpp:29–30; RegisterInfoEmitter.cpp:914–916,1124–1142"
}
mnemonics={}
for line,text in enumerate((E/"X86GenMnemonicTables.inc").read_text().splitlines(),1):
    m=re.fullmatch(r"bool (is[A-Za-z0-9_]+)\(unsigned Opcode\) \{",text)
    if m:
        key="llvm::X86::"+m[1]
        assert key not in mnemonics,key
        mnemonics[key]=f"X86GenMnemonicTables.inc:{line}"
assert "llvm::X86::isNOP" in mnemonics and "llvm::X86::isADD" in mnemonics
assert not sources.keys() & mnemonics.keys()
sources.update(mnemonics)
for file in ("X86BoltMnemonicTables.cpp","X86GenSubSuperRegisterBody.inc","X86GenNeedsAddressSizeOverrideBody.inc"):
    actual=E/file
    assert actual.read_bytes()==(E/("PS6-"+file)).read_bytes(),file
note=lambda f:re.findall(r"Build ID:\s+([a-f0-9]+)",(E/f).read_text())
build_id=note("bolt-notes.txt")
assert len(build_id)==1 and build_id==note("bolt-debug-notes.txt")
debuglink=[]
for line in (E/"bolt-debuglink.txt").read_text().splitlines():
    m=re.match(r"^\s+0x[0-9a-f]+ ((?:[0-9a-f]{8} ){0,3}[0-9a-f]{8})(?:\s|$)",line)
    if m: debuglink.append(m[1])
blob=bytes.fromhex(" ".join(debuglink))
filename,_,rest=blob.partition(b"\0")
crc_offset=(len(filename)+4)//4*4
crc=int.from_bytes(blob[crc_offset:crc_offset+4],"little")
debug=A/"payload/bolt-debug/usr/lib/debug/usr/bin/llvm-bolt.debug"
computed=0
with debug.open("rb") as stream:
    for chunk in iter(lambda:stream.read(1<<20),b""):computed=zlib.crc32(chunk,computed)
assert filename.decode()==debug.name and computed==crc,(filename,computed,crc)

tables={"export":"libllvm-defined","import":"bolt-undefined","internal":"bolt-debug-defined"}
evidence={k:{} for k in tables}
counts={}
pattern=re.compile(r"^\s*(?:[0-9a-f]+\s+)?[A-Za-z?]\s+(llvm::[^ (]+)\(")
for field,file in tables.items():
    n=0
    with (E/(file+".txt")).open() as stream:
        for n,line in enumerate(stream,1):
            m=pattern.match(line)
            if m and m[1] in sources:
                evidence[field].setdefault(m[1],[]).append({"line":n,"raw":line.rstrip("\n")})
    counts[field]=n
    with (E/(file+".mirror-matches.txt")).open("w") as f:
        for rows in evidence[field].values():
            for r in rows:f.write(f"{r['line']}: {r['raw']}\n")
rows=[]
for name,src in sorted(sources.items()):
    rows.append(dict(name=name,source=src,**{f:v.get(name,[]) for f,v in evidence.items()}))
(E/"mirror-symbols.json").write_text(json.dumps(rows,indent=2)+"\n")
with (E/"mirror-symbols.tsv").open("w") as f:
    f.write("function\tsource\tlibLLVM_export\tllvm_bolt_import\tllvm_bolt_internal\n")
    for row in rows:
        fields=[row["name"],row["source"]]
        for key in tables:
            fields.append(" | ".join(v["raw"].strip() for v in row[key]) or "-")
        f.write("\t".join(fields)+"\n")
summary={"source_functions":len(rows),"mnemonic_functions":len(mnemonics),"nm_rows":counts,
         "exported":[r["name"] for r in rows if r["export"]],
         "imported":[r["name"] for r in rows if r["import"]],
         "defined_in_bolt_count":sum(bool(r["internal"]) for r in rows),
         "no_internal_nm_definition_count":sum(not r["internal"] for r in rows),
         "named_functions":[r for r in rows if r["name"] in {
             "llvm::X86::isNOP","llvm::X86::isADD",*(x for x in sources if x not in mnemonics)}],
         "bolt_build_id":build_id[0],"debuglink":filename.decode(),"debuglink_crc32":f"{crc:08x}"}
(E/"symbol-summary.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps({k:v for k,v in summary.items() if k!="named_functions"},indent=2))
