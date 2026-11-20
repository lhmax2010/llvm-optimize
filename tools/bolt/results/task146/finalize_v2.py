from collections import Counter
from pathlib import Path
import json

d=Path(__file__).resolve().parent
p=Path("/home/linhao/Toolchain/development/llvm-optimize/archive/task145")
prior=json.loads((p/"unclassified-final.json").read_text())
assert len(prior)==269
read=lambda f:json.loads((d/f).read_text())
def write(name,data):
    (d/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")

rpm=read("rpm-v2-results.json")
empty_proof=read("clang-debug-empty-cu-proof.json")
for item in rpm:
    if item["rule"]!="R-ID3b" or item["original"]["path"]!="/usr/lib/debug/usr/bin/clang-22.debug":
        continue
    assert item["proof"]["cu"]["before_cus"]==item["proof"]["cu"]["after_cus"]==0
    assert all(not x["dwarf_sections"] and not x["compile_unit_names"] for x in empty_proof.values())
    assert all(r["equal"] for r in item["proof"]["strings"].values())
    item["proof"]["initial_nonempty_check"]=item["proof"]["cu"]["equal"]
    item["proof"]["cu"]["equal"]=True
    item["proof"]["empty_sets_verified_in"]="clang-debug-empty-cu-proof.json"
    item["result"]="PASS"
for item in rpm:
    if item["rule"]!="R-ID1b" or item["index"] not in (190,217):
        continue
    result=read(f'id1b-{item["index"]}-exact.json')
    preliminary=item["proof"]["instruction_comparison"]
    assert item["proof"]["filenames_equal"] and item["proof"]["c2_crc_match"]
    assert item["proof"]["build_id_after"] and not item["proof"]["build_id_before"]
    assert not item["proof"]["unapproved_or_unproven_sections"]
    item["proof"]["instruction_comparison_preliminary_labels"]=preliminary
    item["proof"]["instruction_comparison"]={k:result[k] for k in ("compared","equal","different","coverage")}
    item["proof"]["instruction_comparison_file"]=f'id1b-{item["index"]}-exact.json'
    item["result"]="PASS" if result["status"]=="PASS" else "UNCLASSIFIED"
clang=read("clang-v2-disassembly.json")
driver=read("driver-v2.json")
source={x["index"]:x for x in prior}
object_row,=[x for x in prior if x["original"]["path"].endswith("/libclangDriver.a")]
clang_row,=[x for x in prior if x["rule"]=="R-ID2"]
def row(item,proof,passed):
    return {"index":item["index"],"rule":item["rule"]+"b","result":"PASS" if passed else "UNCLASSIFIED",
            "original":item["original"],"proof":proof}
clang_proof=read("clang-v2-interpretation.json")
raw_notes=["# R-ID2b clang-22 normalized differences",""]
for v in clang["difference_details"]:
    raw_notes.extend([f'{v["section"]} {v["function"]}',v["demangled"],""])
    for c in v["changes"]:
        raw_notes.append(f'@@ PS5 instruction {c["before_at"]+1}, C2 instruction {c["after_at"]+1} @@')
        raw_notes.extend("- "+line for line in c["before_raw"])
        raw_notes.extend("+ "+line for line in c["after_raw"])
        raw_notes.append("")
(d/"clang-v2-raw-differences.txt").write_text("\n".join(raw_notes)+"\n")
status=all(v["driver_function"] for v in clang["difference_details"]) and clang_proof["only_default_linker_literal_or_length"]
rpm.append(row(clang_row,{"evidence":"clang-v2-disassembly.json","raw_differences":"clang-v2-raw-differences.txt",
                         **{k:clang[k] for k in ("compared","equal","different","old_only","new_only","non_driver")},
                         **clang_proof},status))
rpm.append(row(object_row,{"evidence":"driver-v2.json","source_flag_line":24,
                          "exec_sections_compared":driver["exec_sections_compared"],
                          "allocated_relocation_sections_compared":driver["allocated_relocation_sections_compared"]},
               driver["status"]=="PASS"))
rpm.sort(key=lambda x:x["index"])
assert len(rpm)==269 and {x["index"] for x in rpm}==source.keys()
assert all(x["original"]==source[x["index"]]["original"] for x in rpm)
bad=[r for r in rpm if r["result"]!="PASS"]
stop=None
if bad:
    stop=f"STOP 146: {len(bad)} of 269 RPM differences do not satisfy the frozen v2 rules; see unclassified-v2.json"
    (d/"STOP.txt").write_text(stop+"\n")
    print(stop,flush=True)
summary={"status":"STOP" if bad else "PASS","input":269,"passed":269-len(bad),"unclassified":len(bad),
         "rules":{k:dict(Counter(x["result"] for x in rpm if x["rule"]==k)) for k in
                  ("R-ID1b","R-ID3b","R-PS4b","R-ID2b")},
         "id1b":{"name_equal":sum(x["proof"]["filenames_equal"] for x in rpm if x["rule"]=="R-ID1b"),
                 "crc_equal":sum(x["proof"]["c2_crc_match"] for x in rpm if x["rule"]=="R-ID1b"),
                 "outside_sections":dict(Counter(s for x in rpm if x["rule"]=="R-ID1b"
                                          for s in x["proof"]["unapproved_or_unproven_sections"]))},
         "id3b":{"cu_set_equal":sum(x["proof"]["cu"]["equal"] for x in rpm if x["rule"]=="R-ID3b"),
                 "all_string_sets_equal":sum(all(v["equal"] for v in x["proof"]["strings"].values())
                                             for x in rpm if x["rule"]=="R-ID3b"),
                 "string_entry_totals":{name:{key:sum(x["proof"]["strings"][name][key] for x in rpm if x["rule"]=="R-ID3b")
                                           for key in ("before_entries","after_entries","before_prefixed_entries","after_prefixed_entries")}
                                           for name in (".debug_str",".debug_line_str")}},
         "clang":{k:clang[k] for k in ("compared","equal","different","old_only","new_only","non_driver")},
         "original_stop":stop}
write("entries-v2.json",rpm)
write("unclassified-v2.json",bad)
write("classification-v2-summary.json",summary)
print(summary)
