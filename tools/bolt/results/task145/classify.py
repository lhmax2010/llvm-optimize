from collections import Counter, defaultdict
from datetime import datetime
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import traceback

from elf_analysis import Elf, compared, disassemble, is_elf, symbols, unit_names

root=Path("/home/linhao/Toolchain/development/llvm-optimize/archive/task144")
evidence=root.parents[1].with_name("llvm-optimize-bolt")/"tools/bolt/results/task144"
work=Path(sys.argv[1])
result_path=work/"result.json"
raw=root/"b1-audit/rpm-unclassified.json"
source=root/"b1-audit/comparison"
toolroot=root/"b1-a1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr"
base=[toolroot/"lib64/ld-linux-x86-64.so.2","--library-path",toolroot/"lib64"]
objdump=[*base,toolroot/"bin/llvm-objdump"]
dwarfdump=[*base,toolroot/"bin/llvm-dwarfdump"]
errors=work/"llvm-tools-stderr.txt"
errors.touch()
start=datetime.now().astimezone().isoformat(timespec="seconds")

def save(name,value):
    (work/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+"\n")

def sha(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f,"sha256").hexdigest()

def pkgpath(package,side,path):
    pkg="-".join(package)
    prefix=source/side/pkg
    name=path.removeprefix("/")
    if "-RELEASE." in name:
        name=name.replace("-RELEASE.","-2.1." if side=="old" else "-1.")
    return prefix/name

def fingerprint_pair(left,right):
    with Elf(left) as l, Elf(right) as r:
        a,b=l.fingerprints(),r.fingerprints()
        return {"build_id_before":l.id(),"build_id_after":r.id(),
                "section_differences":sorted(k for k in a.keys()|b.keys() if a.get(k)!=b.get(k))}

def verify_file(p,record):
    if not p.is_file() or p.is_symlink() or sha(p)!=record["sha256"]:
        raise RuntimeError(f"RPM member / extracted file identity mismatch: {p}")

def existing_debug(path,side,package):
    sibling=pkgpath((package[0]+"-debuginfo",package[1]),side,"/usr/lib/debug"+path+".debug")
    return sibling if sibling.is_file() and not sibling.is_symlink() else None

def text_delta(old,new):
    if old.stat().st_size>2**20 or new.stat().st_size>2**20:
        return None
    try:
        a=old.read_text()
        b=new.read_text()
    except UnicodeError:
        return None
    return list(difflib.unified_diff(a.splitlines(),b.splitlines(),fromfile=str(old),tofile=str(new),lineterm=""))[:60]

def compare_code(old,new,package,path,unit,cold=False):
    data=work/unit
    data.mkdir()
    reports={}
    outputs=[]
    for side,p in (("old",old),("new",new)):
        debug=existing_debug(path,side,package)
        image=data/(side+".with-symbols")
        result=data/(side+".disassembly.txt")
        funcs={}
        if debug:
            with Elf(p) as before,Elf(debug) as after:
                if before.id()!=after.id():
                    raise RuntimeError(f"detached debug build-id mismatch: {p}, {debug}")
            funcs=symbols(p,debug,image)
        else:
            if cold:
                raise RuntimeError(f"missing matching detached debug file: {p}")
            image=p
        rows,report=disassemble(objdump,image,funcs,result,errors)
        report.update(image_sha256=sha(p),debug_sha256=sha(debug) if debug else None)
        outputs.append((rows,result))
        reports[side]=report
    (al,ar),(bl,br)=outputs
    details=compared(al,bl,ar,br,cold)
    details.update(coverage=reports,disassembler=list(map(str,objdump)),
                   options=["-d","--no-show-raw-insn","--no-leading-addr","--symbolize-operands"])
    save(unit+".json",details)
    return details

def debug_proof(old,new):
    diffs=fingerprint_pair(old,new)
    a,an=unit_names(dwarfdump,old,errors)
    b,bn=unit_names(dwarfdump,new,errors)
    diffs.update(cu_count_before=an,cu_count_after=bn,cu_unique_before=len(a),cu_unique_after=len(b),
                 cu_missing_names_before=sorted(a-b),cu_added_names_after=sorted(b-a),
                 cu_set_equal=bool(an and bn and a and a==b),
                 cu_set_sha256_before=hashlib.sha256("\n".join(sorted(a)).encode()).hexdigest(),
                 cu_set_sha256_after=hashlib.sha256("\n".join(sorted(b)).encode()).hexdigest())
    outside=[n for n in diffs["section_differences"] if n!=".note.gnu.build-id"]
    # Text stored in a DWARF string table is not an encoded ELF address.
    for s in (".debug_str",".debug_line_str",".strtab"):
        if s in outside:
            with Elf(old) as l,Elf(new) as r:
                aa=l.section(s)
                bb=r.section(s)
                if aa is not None and bb is not None:
                    al=set(aa.split(b"\0"))
                    bl=set(bb.split(b"\0"))
                    diffs.setdefault("string_table_values",{})[s]={
                        "only_before":len(al-bl),"only_after":len(bl-al),
                        "examples_before":[v.decode("utf-8","replace")[:350] for v in sorted(al-bl)[:4]],
                        "examples_after":[v.decode("utf-8","replace")[:350] for v in sorted(bl-al)[:4]]}
    diffs["unproven_address_only_sections"]=outside
    return diffs

def rowout(d, rule, why, accepted=False):
    return {"rule":rule,"result":"PASS" if accepted else "UNCLASSIFIED","basis":why,"original":d}

def link(d):
    package=d["rpm"]
    path=d["path"]
    p=pkgpath(package,"new",path)
    target=d["after"].get("target","")
    if not p.is_symlink() or os.readlink(p)!=target:
        return rowout(d,"R-ID3",{"reason":"missing RPM link or target mismatch","extracted":str(p)})
    original=os.path.normpath(os.path.join(os.path.dirname(path),target))
    match=re.fullmatch(r"/usr/lib/debug/\.build-id/([\da-f]{2})/([\da-f]+)(?:\.debug)?",path)
    if not match or not package[0].endswith("-debuginfo"):
        return rowout(d,"R-ID3",{"reason":"link pattern or package mismatch","target":original})
    expected="".join(match.groups())
    paired=(package[0].removesuffix("-debuginfo"),package[1])
    bin_pkg=package if original.endswith(".debug") else paired
    value=pkgpath(bin_pkg,"new",original)
    debug_value=value if original.endswith(".debug") else existing_debug(original,"new",paired)
    if not value.is_file() or value.is_symlink() or not is_elf(value) or not debug_value or not is_elf(debug_value):
        return rowout(d,"R-ID3",{"reason":"missing corresponding extracted ELF or debug file in the paired RPMs",
                                 "target":original,"target_package":bin_pkg})
    with Elf(value) as exe,Elf(debug_value) as debug:
        output={"target":original,"target_package":bin_pkg,"debug_path":str(debug_value),
                "expected_build_id":expected,"target_build_id":exe.id(),"debug_build_id":debug.id()}
        return rowout(d,"R-ID3",output,exe.id()==expected and debug.id()==expected)

def allowed(section):
    return section in {".note.gnu.build-id",".dynamic",".dynsym",".dynstr",".got",".got.plt",".rela.dyn",
                       ".rela.plt",".shstrtab",".gnu.hash",".hash"} or section.startswith(".gnu.version")

def main():
    rows=json.loads(raw.read_text())
    assert len(rows)==24793,"expected 144 gate record count"
    left,right={},{}
    detail=[]
    for row in rows:
        if row["rpm"]!=["llvm-debugsource","x86_64"]:
            detail.append(row)
            continue
        old=bool(row["before"])
        prefix="/usr/src/debug/llvm-22.1.8-"+("2.1" if old else "1")+".x86_64"
        relative=row["path"].removeprefix(prefix)
        assert row["path"].startswith(prefix) and (relative=="" or relative.startswith("/")),row
        side=left if old else right
        assert relative not in side,row
        side[relative]=row["before"] if old else row["after"]
    assert len(detail)==509 and len(left)==len(right)==12142
    assert left==right,"R-B records differ in data or presence after prefix replacement"
    save("r-b-proof.json",{"rule":"R-B","pairs":len(left),"raw_entries":len(left)+len(right),
         "checked":["path","mode","uid","gid","bytes","sha256"],"raw_evidence":str(raw),"raw_sha256":sha(raw)})
    packaged=json.loads((root/"b1-audit/rpm-package-comparison.json").read_text())
    already_passed=defaultdict(set)
    for pkg in packaged:
        for c in pkg["changes"]:
            if c["reason"]=="validated build-id link" and c["after"]:
                already_passed[tuple(pkg["rpm"])].add(c["path"])
    linked={}
    for d in detail:
        if d["before"] is None and ".build-id" in d["path"] and stat.S_ISLNK(d["after"]["mode"]):
            linked[(tuple(d["rpm"]),d["path"])]=link(d)
    ordered=sorted(enumerate(detail,1),key=lambda i:i[1]["path"]!="/usr/bin/clang-22")
    results={}
    for number,d in ordered:
        p=d["path"]
        pkg=d["rpm"]
        before,after=d["before"],d["after"]
        li=linked.get((tuple(pkg),p))
        if li:
            result=li
        elif before is None and pkg[0].endswith("-debuginfo") and stat.S_ISDIR(after["mode"]) and re.fullmatch(r"/usr/lib/debug/\.build-id(?:/[0-9a-f]{2})?",p):
            candidates=[r for (k,n),r in linked.items() if k==tuple(pkg) and n.startswith(p+"/")]
            prechecked=sorted(n for n in already_passed[tuple(pkg)] if n.startswith(p+"/"))
            passed=sorted(r["original"]["path"] for r in candidates if r["result"]=="PASS")
            rejected=sorted(r["original"]["path"] for r in candidates if r["result"]!="PASS")
            backing={"new_directory":str(pkgpath(pkg,"new",p)),"passed_links":passed,
                     "links_verified_in_144":prechecked,"unverified_links":rejected}
            # The directory record and each child link retain independent results.
            result=rowout(d,"R-ID3",backing,pkgpath(pkg,"new",p).is_dir()
                        and not pkgpath(pkg,"new",p).is_symlink() and bool(passed or prechecked))
        elif before is not None and after is not None and stat.S_ISREG(before["mode"]) and stat.S_ISREG(after["mode"]):
            l,r=pkgpath(pkg,"old",p),pkgpath(pkg,"new",p)
            verify_file(l,before)
            verify_file(r,after)
            if is_elf(l) and is_elf(r):
                if p=="/usr/bin/clang-22":
                    code=compare_code(l,r,pkg,p,"r-id2-clang-22",True)
                    base={k:code[k] for k in ("compared","different","equal","old_only","new_only","coverage")}
                    base["full_disassembly_comparison"]="r-id2-clang-22.json"
                    valid=code["different"]==0 and all(
                        x["function_symbols"] and not x["function_addresses_without_matching_named_block"]
                        for x in code["coverage"].values())
                    result=rowout(d,"R-ID2",base,valid)
                elif pkg[0].endswith("-debuginfo") and p.endswith(".debug"):
                    base=debug_proof(l,r)
                    result=rowout(d,"R-ID3",base,
                         base["cu_set_equal"] and not base["unproven_address_only_sections"])
                else:
                    base=fingerprint_pair(l,r)
                    excluded=[n for n in base["section_differences"] if not allowed(n)]
                    base["outside_layout_whitelist_or_unproven_address_fields"]=excluded
                    valid=not base["build_id_before"] and bool(base["build_id_after"]) and not excluded
                    if valid:
                        code=compare_code(l,r,pkg,p,f"r-id1-{number}")
                        base["disassembly"]={k:code[k] for k in ("compared","different","equal","coverage")}
                        valid=code["compared"]>0 and not code["different"] and all(
                            x["function_symbols"] and not x["function_addresses_without_matching_named_block"]
                            for x in code["coverage"].values())
                    else:
                        base["disassembly"]="short-circuited by independently failing ELF note/section gate"
                    result=rowout(d,"R-ID1",base,valid)
            else:
                base={"reason":"same-path non-ELF content change, not a proven R-PS4 file operation"}
                rawdiff=text_delta(l,r)
                if rawdiff is not None:
                    base["raw_diff"]=rawdiff
                result=rowout(d,"R-PS4",base)
        else:
            result=rowout(d,None,{"reason":"no exact corresponding rule evidence"})
        results[number]=result
        if number%20==0 or p=="/usr/bin/clang-22":
            print(datetime.now().astimezone().isoformat(timespec="seconds"),"classified",len(results),flush=True)
        with (work/"entries.partial.jsonl").open("a") as out:
            out.write(json.dumps({"index":number,**result},ensure_ascii=False)+"\n")
    final=[{"index":i,**results[i]} for i in sorted(results)]
    pending=[d for d in final if d["result"]!="PASS"]
    save("entries-509.json",final)
    save("unclassified.json",pending)
    totals={}
    for rule in ("R-ID1","R-ID2","R-ID3","R-PS4",None):
        totals[rule or "OTHER"]=dict(Counter(r["result"] for r in final if r["rule"]==rule))
    save("result.json",{"start":start,"end":datetime.now().astimezone().isoformat(timespec="seconds"),
        "status":"STOP" if pending else "PASS","pending":len(pending),"totals":totals,"R-B":{"passed_pairs":len(left)}})
    if pending:
        stop=f"STOP: {len(pending)} of 509 RPM differences do not satisfy the frozen rules; see {work/'unclassified.json'}"
        print(stop,flush=True)
        (work/"STOP.txt").write_text(stop+"\n")
    return bool(pending)

try:
    rc=main()
except Exception:
    (work/"preparation-STOP.txt").write_text(traceback.format_exc())
    traceback.print_exc()
    save("result.json",{"status":"STOP","kind":"preparation","error":traceback.format_exc()})
    rc=1
sys.exit(rc)
