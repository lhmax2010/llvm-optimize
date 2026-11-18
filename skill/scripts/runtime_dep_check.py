#!/usr/bin/env python3
"""Inspect shipped ELF files and every member of ordinary static archives."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess

ARCHIVE = b"!<arch>\n"
THIN = b"!<thin>\n"
ELF = b"\x7fELF"


def findings(lines):
    issues = []
    for line in lines:
        if (re.search(r"\b__llvm_(?:prf|profile)_[A-Za-z0-9_.]+", line)
                or re.search(r"\(NEEDED\).*\[libclang_rt\.profile[^\]]*\]", line)):
            issues.append(line.strip())
        elif re.search(r"\b(?:error|warning):", line, re.I):
            issues.append(line.strip())
    return issues


def audit(root, readelf):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("payload root must be a directory")
    readelf = Path(readelf)
    if not readelf.is_absolute():
        raise ValueError("an absolute readelf path is required")
    counts = {"elf": 0, "archives": 0}
    issues = []
    def walk_error(error):
        raise error

    for directory, dirs, names in os.walk(root, onerror=walk_error):
        dirs.sort()
        for name in sorted(names):
            path = Path(directory) / name
            if path.is_symlink() or not path.is_file():
                continue
            with path.open("rb") as stream:
                ident = stream.read(20)
            if ident.startswith(THIN):
                issues.append({"file": str(path.relative_to(root)), "diagnostic": "external members in thin archive"})
                continue
            if ident.startswith(ARCHIVE):
                counts["archives"] += 1
            elif ident.startswith(ELF):
                if len(ident) < 20 or ident[5] not in (1, 2):
                    issues.append({"file": str(path.relative_to(root)), "diagnostic": "invalid ELF identification"})
                    continue
                elf_type = int.from_bytes(ident[16:18], "little" if ident[5] == 1 else "big")
                if elf_type not in (2, 3):
                    continue
                counts["elf"] += 1
            elif path.suffix == ".a":
                issues.append({"file": str(path.relative_to(root)), "diagnostic": "invalid archive magic"})
                continue
            else:
                continue
            argv = [str(readelf), "--wide", "--section-headers", "--symbols", "--dynamic", str(path)]
            with subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  text=True, errors="replace", env={**os.environ, "LC_ALL": "C"}) as process:
                for finding in findings(process.stdout):
                    issues.append({"file": str(path.relative_to(root)), "diagnostic": finding})
                if process.wait():
                    issues.append({"file": str(path.relative_to(root)), "diagnostic": "readelf failed"})
    if not any(counts.values()):
        issues.append({"file": ".", "diagnostic": "no shipped ELF or archive inspected"})
    return {"status": "FAIL" if issues else "PASS", **counts, "findings": issues}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--readelf", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = audit(args.root, args.readelf)
        print(json.dumps(result, indent=2))
    except (OSError, ValueError) as error:
        parser.exit(1, f"STOP: {error}\n")
    return int(result["status"] != "PASS")


if __name__ == "__main__":
    raise SystemExit(main())
