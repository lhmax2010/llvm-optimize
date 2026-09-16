#!/usr/bin/env python3
"""Query installed LLVM tools without executing them or changing the RPM root.

Supply an existing GBS root discovered separately. Raw query output goes to
stdout; package lists and tool_inventory.json go to --output-dir (use temp/).
Absolute symlinks are resolved inside the supplied root, not on the host.
"""

import argparse
import json
import os
from pathlib import Path
import re
import shlex
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--extra-package", action="append", default=[])
    args = parser.parse_args()
    root = args.root.resolve(strict=True)
    outdir = args.output_dir.resolve()
    if root == outdir or root in outdir.parents:
        parser.error("output-dir must be outside the queried RPM root")
    outdir.mkdir(parents=True, exist_ok=True)

    def run(command):
        print("$ " + shlex.join(map(str, command)), flush=True)
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            env=dict(os.environ, LC_ALL="C"),
        )
        print(result.stdout, end="", flush=True)
        print(result.stderr, end="", flush=True)
        print(f"[command_exit={result.returncode}]", flush=True)
        return result

    def resolve(guest):
        parts, resolved, links = guest.split("/"), [], 0
        while parts:
            part = parts.pop(0)
            if part in ("", "."):
                continue
            if part == "..":
                if resolved:
                    resolved.pop()
                continue
            candidate = root.joinpath(*resolved, part)
            if candidate.is_symlink():
                links += 1
                if links > 40:
                    raise RuntimeError(f"Symlink loop: {guest}")
                target = os.readlink(candidate)
                if target.startswith("/"):
                    resolved = []
                parts = target.split("/") + parts
            else:
                resolved.append(part)
        return root.joinpath(*resolved)

    rpm = ["rpm", "--root", str(root), "--dbpath", "/var/lib/rpm"]
    query = run(rpm + ["-qa", "--qf", "%{NAME}\t%{VERSION}-%{RELEASE}\t%{ARCH}\t%{SOURCERPM}\n"])
    query.check_returncode()
    packages = [
        line.split("\t")[0] for line in query.stdout.splitlines()
        if line.split("\t")[-1].startswith("llvm-")
    ]
    packages = list(dict.fromkeys(packages + args.extra_package))
    records = []
    for package in packages:
        listed = run(rpm + ["-ql", package])
        listed.check_returncode()
        (outdir / f"rpm-ql-{package}.txt").write_text(listed.stdout)
        for guest in listed.stdout.splitlines():
            target = resolve(guest)
            if not target.is_file() or not target.stat().st_mode & 0o111:
                continue
            with target.open("rb") as stream:
                head = stream.read(4)
            if "/bin/" not in guest and "/libexec/" not in guest and not head.startswith(b"#!"):
                continue
            original = root / guest.lstrip("/")
            run(["ls", "-la", str(original)]).check_returncode()
            if target != original:
                run(["ls", "-la", str(target)]).check_returncode()
            dynamic = run(["readelf", "-d", str(target)])
            is_elf = head == b"\x7fELF"
            if is_elf:
                dynamic.check_returncode()
            needed = re.findall(r"Shared library: \[(.*?)\]", dynamic.stdout)
            info = run(["file", "-L", str(target)])
            info.check_returncode()
            records.append({
                "package": package, "path": guest,
                "resolved": str(target.relative_to(root)),
                "size": target.stat().st_size, "elf": is_elf,
                "needed": needed,
                "llvm_shared": any(re.match(r"lib(LLVM|clang-cpp).*\.so", name) for name in needed),
                "file": info.stdout.strip(),
            })
    (outdir / "tool_inventory.json").write_text(json.dumps(records, indent=2) + "\n")
    print("INVENTORY SUMMARY")
    for package in packages:
        rows = [row for row in records if row["package"] == package]
        print(package, "paths=" + str(len(rows)),
              "ELF=" + str(sum(row["elf"] for row in rows)),
              "LLVM_shared=" + str(sum(row["llvm_shared"] for row in rows)))


if __name__ == "__main__":
    main()
