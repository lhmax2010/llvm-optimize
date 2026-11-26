"""Recover the artifacts produced by the first G5 tools and relink commands."""
import json
import sys
from pathlib import Path

A = Path(__file__).resolve().parent
RUN = A.parent / "task160/run"
sys.path.insert(0, str(A / "orchestration"))
from handoff import confined, g4_scratch, receipt, retain_runtime


def require_receipt(path, expected):
    confined(path, RUN)
    current = receipt(path)
    if current != expected:
        raise RuntimeError(f"G5 recovery artifact differs from its receipt: {path}")
    print(f"REUSED {current['sha256']} {current['bytes']} {path}", flush=True)
    return current


def tools():
    records = json.loads((RUN / "G5/tool-artifacts.json").read_text())
    expected = {str(RUN / "G-config/bolt-artifacts" / name) for name in
                ("llvm-bolt", "merge-fdata", "libbolt_rt_instr.a")}
    if len(records) != len(expected) or {row["path"] for row in records} != expected:
        raise RuntimeError("G5 recovery tool receipt set differs from the expected outputs")
    for row in records:
        require_receipt(Path(row["path"]), row)


def relink():
    root = g4_scratch(RUN)
    target = RUN / "G-profiles/clang-with-relocs"
    current = require_receipt(target, json.loads((RUN / "G5/relink-artifacts.json").read_text()))
    original = root / "home/abuild/133n-bolt/clang-with-relocs"
    confined(original, RUN)
    require_receipt(original, {**current, "path": str(original)})
    runtime = RUN / "G-config/bolt-runtime-libs"
    if runtime.exists():
        confined(runtime, RUN)
        runtime.rmdir()
    retain_runtime(RUN, root, target)


if __name__ == "__main__":
    {"bolt-tools": tools, "relink-strip-debug": relink}[sys.argv[1]]()
