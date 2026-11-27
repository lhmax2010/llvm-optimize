"""Use task 168's exact single-core corpus and measurement method for V3q."""
from collections import Counter
from itertools import combinations
import os
from pathlib import Path
import subprocess
import sys

from collect import A, W, E, ART, read, record, save, extract

sys.path[:0]=[str(W/"archive/task168"),str(W/"archive/task156")]
import paired
import retest
from variants import elf_closure

PREVIOUS = W/"archive/task168/run/manifest.json"
OUT = A/"benchmark"
NAMES = ("V1","V3","V3q")
BENCH = retest.BENCH


def prepare(qb, comparison, v1):
    root=OUT/"private/V3q"
    root.mkdir(parents=True)
    target=root/"usr/bin/clang-22"
    for runtime in v1["runtime_provider_rpms"]:
        source=Path(runtime["path"])
        proof=record(source)
        if any(proof[k]!=runtime[k] for k in ("bytes","sha256")):
            raise ValueError("fixed Tizen runtime provider changed")
        extract(source,root,("./lib64/*","./usr/lib64/*"))
    for name in ("clang","llvm","libllvm"):
        extract(Path(qb[name]["path"]),root,
                ("./usr/bin/clang-22","./usr/lib64/libLLVM.so*","./usr/lib64/libclang.so*","./usr/lib64/libclang-cpp.so*"))
    identity=record(target)
    if any(identity[k]!=comparison["V3q"][k] for k in ("bytes","sha256")):
        raise ValueError("V3q differs from audited QB compiler")
    loader=root/Path(v1["loader"]).relative_to(v1["root"])
    libs=[str(root/Path(p).relative_to(v1["root"])) for p in v1["library_path"]]
    loader_options=["--inhibit-cache","--library-path",":".join(libs)]
    linked,closure=elf_closure(loader,loader_options,root)
    (E/"v3q-loader.txt").write_text(linked)
    version=subprocess.check_output([loader,*loader_options,target,"--no-default-config","-fintegrated-cc1","--version"],text=True)
    return {"root":str(root),"clang":str(target),"sha256":identity["sha256"],"loader":str(loader),
            "loader_sha256":record(loader)["sha256"],"library_path":libs,"closure":closure,
            "source_rpm":qb["clang"],"version":version.strip(),"status":"PASS"}


def bytes_check(batches, inputs):
    by_name={n:{r["tu"]:r for r in b["measurements"]} for n,b in batches.items()}
    items=[]
    for tu in inputs:
        for a,b in combinations(NAMES,2):
            key=tu["id"]
            items.append({"tu":key,"left":a,"right":b,**BENCH.compare_objects(
                          by_name[a][key].get("object"),by_name[b][key].get("object"))})
    return items


def run():
    old=read(PREVIOUS)
    comparison=read(E/"clang-comparison.json")
    if comparison["same_sha256"]:
        raise ValueError("V3q replay only applies when the compiler SHA256 differs")
    inputs=old["single_inputs"]
    if len(inputs)!=30 or len({t["id"] for t in inputs})!=30:
        raise ValueError("task 168 top-30 corpus is incomplete")
    for row in inputs:
        if record(Path(row["path"]))["sha256"]!=row["sha256"]:
            raise ValueError(f"benchmark input changed: {row['id']}")
    raw,topology=retest.find_cores()
    core=old["topology"]["single_cpu"]
    if core not in topology["p_cpu_ids"] or core not in os.sched_getaffinity(0):
        raise ValueError(f"task 168 performance core {core} is unavailable")
    variants={n:old["variants"][n] for n in NAMES if n!="V3q"}
    for n,v in variants.items():
        for field,sha in (("clang","sha256"),("loader","loader_sha256")):
            if record(Path(v[field]))["sha256"]!=v[sha]:
                raise ValueError(f"{n} benchmark identity changed: {field}")
    OUT.mkdir()
    work=OUT/"work"
    work.mkdir()
    fixed=OUT/"fixed"
    fixed.mkdir()
    variants["V3q"]=prepare(read(E/"rpm-downloads.json"),comparison,variants["V1"])
    (OUT/"cpu-topology.csv").write_text(raw)
    alias=fixed/"root"
    layouts=[BENCH.variant_at(v,alias) for v in variants.values()]
    assert all(all(v[field]==layouts[0][field] for field in ("clang","loader","library_path")) for v in layouts)
    save(OUT/"manifest.json",{"started":retest.prior.now(),"cpu":core,"inputs":inputs,"variants":variants,
          "initial_environment":retest.environment(topology["allowed_cpus"]),"comparison_corpus":str(PREVIOUS),
          "topology":topology,"fixed_root":str(alias)})
    BENCH.measure=retest.measure
    os.sched_setaffinity(0,{topology["reserved_p_cpu"]})
    rows=[]
    warmup=None
    for idx in range(6):
        name="warmup" if idx==0 else f"round-{idx:02}"
        order=BENCH.rotation(NAMES,max(0,idx-1))
        row={"round":idx,"order":order,"environment_start":retest.environment([core]),"variants":{}}
        batches=row["variants"]
        for v in order:
            print(f"BEGIN {retest.prior.now()} V3q {name} {v}",flush=True)
            compiler=BENCH.use_variant(variants[v],alias)
            batch=retest.batch_with_environment(compiler,inputs,[core],work,OUT/name/v)
            batches[v]=batch
            if {m["cpu"] for m in batch["measurements"]}!={core}:
                raise ValueError("benchmark worker affinity changed")
            print(f"END {retest.prior.now()} V3q {name} {v} cpu={batch['tu_cpu_seconds_sum']:.3f} "
                  f"wall={batch['elapsed_seconds']:.3f} pass={batch['all_passed']}",flush=True)
        if idx:
            for v in order:
                batch=batches[v]
                if any(m["anomalous"] for m in batch["measurements"]):
                    compiler=BENCH.use_variant(variants[v],alias)
                    extra=BENCH.repeat_batch(batch,compiler,inputs,[core],work,OUT/name/v,0)
                    batch.update(anomaly_retries=extra["anomaly_retries"],
                                 retry_elapsed_seconds=extra["retry_elapsed_seconds"])
        row["comparisons"]=bytes_check(batches,inputs)
        row["environment_end"]=retest.environment([core])
        save(OUT/(name+".json"),row)
        if idx:
            rows.append(row)
        else:
            warmup=row
        print(name,dict(Counter(x["status"] for x in row["comparisons"])),flush=True)
    paired.PAIRS=(("V3q","V1"),("V3q","V3"))
    analysis=paired.analyze(rows,inputs,"171")
    deltas=[{"round":r["round"],**x} for r in (warmup,*rows) for x in r["comparisons"] if x["status"]!="IDENTICAL"]
    failures=[{"round":r["round"],"variant":n,**m} for r in (warmup,*rows) for n,b in r["variants"].items()
              for m in b["measurements"] if m["status"]!="PASS"]
    retries=[]
    for row in rows:
        for n,b in row["variants"].items():
            retries.extend({"round":row["round"],"variant":n,"tu":item["initial"]["tu"],
                            "rc":item["retry"]["rc"],"objects":item["objects"]} for item in b["anomaly_retries"])
    data={"status":"PASS" if not failures and not deltas and all(
          r["rc"]==0 and r["objects"]["status"]=="IDENTICAL" for r in retries) else "FAIL",
          "ended_at":retest.prior.now(),"cpu":core,"paired":analysis,
          "formal_objects":dict(Counter(x["status"] for r in rows for x in r["comparisons"])),
          "warmup_objects":dict(Counter(x["status"] for x in warmup["comparisons"])),
          "differences":deltas,"failures":failures,"retries":retries}
    save(OUT/"result.json",data)
    print({k:data[k] for k in ("status","cpu","formal_objects","warmup_objects")},flush=True)


if __name__=="__main__":
    run()
