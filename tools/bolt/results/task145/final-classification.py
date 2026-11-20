from collections import Counter
from pathlib import Path
import json,re,sys

from elf_analysis import Elf

base=Path(__file__).resolve().parent
historic=Path("/home/linhao/Toolchain/development/llvm-optimize/archive/task144")
checked=historic/"b1-audit/comparison/new"
doc=base/"classify-first-a1/entries-509.json"
rows=json.loads(doc.read_text())
assert len(rows)==509 and sum(x["result"]=="UNCLASSIFIED" for x in rows)==270
ranked=json.loads((base/"exact-first-a1/r-id2-symbol-ranges.json").read_text())
source=json.loads((base/"r-ps4-source-line-evidence.json").read_text())
rb=json.loads((base/"debugsource-first-a1/result.json").read_text())
assert rb["status"]=="PASS" and rb["old_paths"]==rb["new_paths"]==12142
notes=[]
for item in rows:
    original=item["original"]
    p=original["path"]
    if item["rule"]=="R-ID2":
        assert ranked["different"]>0 and item["result"]=="UNCLASSIFIED"
        item["basis"]={k:ranked[k] for k in ("coverage","compared","equal","different","old_only","new_only")}
        item["basis"]["evidence"]="exact-first-a1/r-id2-symbol-ranges.json"
        item["basis"]["pair_link_and_same_text_bytes"]="r-id2-pairing.json"
    elif item["rule"]=="R-PS4" and p.endswith(("/ClangConfig.cmake","/config.h")):
        item["basis"]["source_diff_lines"]={"ps1-ps4.diff":[3253],"ps4-parent-vs-ps5.diff":[24]}
        item["basis"]["observed_correlation"]="CLANG_DEFAULT_LINKER changes from empty to lld in the same installed path"
    elif item["rule"]=="R-PS4" and p.endswith("/libclangDriver.a"):
        item["basis"]["archive_members"]=source["archive"]
        item["basis"]["source_diff_lines"]={"ps1-ps4.diff":[3253],"ps4-parent-vs-ps5.diff":[24]}
        item["basis"]["observed_correlation"]="only Driver.cpp.o differs, source configuration is context rather than a validated file operation"
    elif item["rule"]=="R-ID3" and item["result"]=="UNCLASSIFIED" and not original["before"]:
        # RPM find-debuginfo can add a decimal suffix to distinguish build-id links.
        pkg="-".join(original["rpm"])
        link=checked/pkg/p.removeprefix("/")
        match=re.fullmatch(r"/usr/lib/debug/\.build-id/([0-9a-f]{2})/([0-9a-f]{38})\.([1-9][0-9]*)",p)
        assert match and pkg=="lldb-devel-debuginfo-x86_64",item
        expected=match[1]+match[2]
        target=checked/"lldb-devel-x86_64/usr/lib64/liblldb.so.22.1.8"
        debug=checked/pkg/"usr/lib/debug/usr/lib64/liblldb.so.22.1.8.debug"
        companion=link.with_name(link.name+".debug")
        assert link.is_symlink() and companion.is_symlink()
        assert str(link.readlink())==original["after"]["target"]
        rpmroot=Path("/")
        assert (rpmroot/p.removeprefix("/")).parent.as_posix()=="/usr/lib/debug/.build-id/5f"
        assert target.is_file() and not target.is_symlink() and debug.is_file() and not debug.is_symlink()
        assert str(link.readlink())=="../../../../../usr/lib64/liblldb.so.22.1.8"
        assert str(companion.readlink())=="../../../../../usr/lib/debug/usr/lib64/liblldb.so.22.1.8.debug"
        with Elf(target) as t,Elf(debug) as d:
            assert t.id()==d.id()==expected
            item["basis"]={"target":str(target),"debug":str(debug),"build_id":expected,
                           "rpm_link_suffix":match[3],"link":str(link),"debug_link":str(companion),
                           "debug_link_target":str(companion.readlink()),
                           "previous_matcher_result":item["basis"]}
        item["result"]="PASS"
        notes.append(item)
assert len(notes)==1
rejects=[x for x in rows if x["result"]=="UNCLASSIFIED"]
assert len(rejects)==269
totals={r:dict(Counter(x["result"] for x in rows if x["rule"]==r)) for r in ("R-ID1","R-ID2","R-ID3","R-PS4")}
result={"status":"STOP","scope":509,"unclassified":len(rejects),"by_rule":totals,
        "R-B":{"status":"PASS","pairs":12142,"historical_raw_rows":24284},
        "R-ID2":{"compared":ranked["compared"],"equal":ranked["equal"],"different":ranked["different"]},
        "correction":{"rule":"R-ID3","raw_preparation_reject_indices":[x["index"] for x in notes]},
        "unclassified_by_package":dict(Counter("/".join(x["original"]["rpm"]) for x in rejects))}
for n,data in (("entries-final-509.json",rows),("unclassified-final.json",rejects),("classification-summary.json",result),
               ("r-id3-numbered-link-proof.json",notes)):
    (base/n).write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
stop=f"STOP classification: {len(rejects)} of 509 RPM differences do not satisfy the frozen rules; see unclassified-final.json"
(base/"classification-final-STOP.txt").write_text(stop+"\n")
print(stop)
