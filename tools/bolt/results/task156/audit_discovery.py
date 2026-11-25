from collections import Counter
from pathlib import Path
import json, sys

A=Path(__file__).resolve().parent
E=A/"evidence"
from corpus import canon_source,parse_source
sys.path.insert(0,str(A/"bench"))
from bench import memory_guard,write_json

scan=json.loads((E/"input-discovery.json").read_text())
training=set(json.loads((E/"training-overlap-policy.json").read_text())["excluded_source_stems"])
admitted=json.loads((E/"corpus.json").read_text())["inputs"]
known={canon_source(r["source_tu"]) for r in admitted}
root_paths={r["path"] for r in admitted}
rows=[]
for path in scan["candidates"]:
    memory_guard()
    status="not admitted"
    try:
        source=parse_source(Path(path))
        stem=canon_source(source)
        if path in root_paths:
            reason="selected input in corpus.json"
        elif stem in training:
            reason="training source identity"
        elif stem in known:
            reason="duplicate source identity or other preprocessing target"
        else:
            reason="no verified package, target and saved compile-flag receipt"
    except (OSError,ValueError) as error:
        source=None
        reason="no readable source marker"
    rows.append({"path":path,"source_marker":source,"reason":reason,"status":"included" if path in root_paths else status})
out={"discovered_candidates":len(rows),"discovery_errors":scan["errors"],
     "reasons":dict(Counter(r["reason"] for r in rows)),"rows":rows}
write_json(E/"input-eligibility.json",out)
print(out["reasons"])
