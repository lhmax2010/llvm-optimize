#!/usr/bin/env bash
# Read-only ELF inspection; an optional explicit loader handles non-host PT_INTERP.
set -euo pipefail
exec python3 - "$@" <<'PY'
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys

p = argparse.ArgumentParser(description="Verify extracted native x86_64 LLVM tools without installing RPMs.",
    epilog="Pass ROOT containing bin/, or the extraction root containing usr/bin/. "
    "Nonzero exit means missing tool, non-x86_64 ELF, version failure, or LLVM shared-library dependency. "
    "Extraction is separate: rpm2cpio PACKAGE.rpm | (cd DEST && cpio -idm --no-absolute-filenames).")
p.add_argument("--root", required=True, type=Path)
p.add_argument("--loader", type=Path, help="explicit native ELF loader if PT_INTERP is absent on this host")
p.add_argument("--library-path", help="colon-separated runtime directories, used only with --loader")
p.add_argument("--output", required=True, type=Path, help="new JSON file; raw output uses the same stem with .log")
a = p.parse_args()
root = a.root.resolve()
bindir = root / "bin" if (root / "bin/clang").exists() else root / "usr/bin"
if a.library_path and not a.loader:
    p.error("--library-path requires --loader")
if a.output.exists() or a.output.with_suffix(".log").exists():
    p.error("output already exists; choose a new path to preserve earlier evidence")
a.output.parent.mkdir(parents=True, exist_ok=True)
rows = []
failed = False
with a.output.with_suffix(".log").open("w", buffering=1) as log:
    def run(cmd):
        log.write("$ " + shlex.join(map(str, cmd)) + "\n")
        try:
            r = subprocess.run(list(map(str, cmd)), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               text=True, timeout=60)
            log.write(r.stdout + "[exit=" + str(r.returncode) + "]\n")
            return r.returncode, r.stdout
        except (OSError, subprocess.TimeoutExpired) as error:
            log.write(repr(error) + "\n")
            return 125, str(error)
    for name in ("clang", "clang++", "ld.lld", "llvm-ar", "llvm-ranlib"):
        tool = bindir / name
        row = dict(tool=name, path=str(tool), errors=[])
        if not tool.exists():
            row["errors"].append("MISSING (including a broken symlink)")
            rows.append(row)
            failed = True
            continue
        resolved = tool.resolve()
        if not resolved.is_relative_to(root):
            row["errors"].append("symlink escapes the extraction root; refusing to inspect/execute host tool")
            rows.append(row)
            failed = True
            continue
        with resolved.open("rb") as binary:
            digest = hashlib.file_digest(binary, "sha256").hexdigest()
        row.update(resolved=str(resolved), bytes=resolved.stat().st_size, sha256=digest)
        outputs = {}
        for key, cmd in (("ls", ["ls", "-la", tool, resolved]), ("file", ["file", "-L", tool]),
                         ("elf_header", ["readelf", "-h", tool]), ("dynamic", ["readelf", "-d", tool])):
            rc, out = run(cmd)
            outputs[key] = out
            if rc:
                row["errors"].append(key + " failed")
        if not re.search(r"Machine:\s+Advanced Micro Devices X86-64", outputs["elf_header"]):
            row["errors"].append("not a native x86_64 ELF")
        needed = re.findall(r"\(NEEDED\).*\[([^\]]+)\]", outputs["dynamic"])
        row.update(needed=needed, raw=outputs)
        row["llvm_shared"] = [x for x in needed if re.search(r"libLLVM|libclang-cpp", x)]
        if row["llvm_shared"]:
            row["errors"].append("BLOCKER: LLVM shared-library link is still present")
        if not row["errors"] or row["errors"] == ["BLOCKER: LLVM shared-library link is still present"]:
            cmd = [str(tool), "--version"]
            if a.loader:
                cmd = [str(a.loader)] + (["--library-path", a.library_path] if a.library_path else []) + cmd
            rc, version = run(cmd)
            row["version"] = version.strip()
            if rc:
                row["errors"].append("--version failed")
        failed |= bool(row["errors"])
        rows.append(row)
result = dict(timestamp=datetime.datetime.now().astimezone().isoformat(), root=str(root),
              loader=str(a.loader) if a.loader else None, library_path=a.library_path,
              status="BLOCKER" if failed else "PASS", tools=rows)
a.output.write_text(json.dumps(result, indent=2) + "\n")
print("| Tool | Bytes (resolved ELF) | NEEDED | Status |")
print("| --- | ---: | --- | --- |")
for row in rows:
    print("| {} | {} | {} | {} |".format(row["tool"], row.get("bytes", "UNKNOWN"),
          ", ".join(row.get("needed", [])), "; ".join(row["errors"]) or "PASS"))
print("Raw output:", a.output.with_suffix(".log"))
sys.exit(2 if failed else 0)
PY
