#!/usr/bin/env python3
"""Create and verify a paired profile manifest without loading profiles into memory."""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import re
import shutil


def file_identity(path):
    path = Path(path)
    with path.open("rb") as stream:
        return {"bytes": path.stat().st_size, "sha256": hashlib.file_digest(stream, "sha256").hexdigest()}


def verify_asset(info, root):
    root = Path(root).resolve(strict=True)
    name = info["file"]
    if Path(name).name != name or not name.endswith(".xz"):
        raise ValueError("asset must be an xz basename")
    source = root / name
    if source.is_symlink():
        raise ValueError(f"asset is a symbolic link: {name}")
    for key in ("sha256", "xz_sha256"):
        if not re.fullmatch(r"[0-9a-f]{64}", info[key]):
            raise ValueError(f"invalid asset digest: {key}")
    for key in ("bytes", "xz_bytes"):
        if type(info[key]) is not int or info[key] <= 0:
            raise ValueError(f"invalid asset size: {key}")
    if file_identity(source) != {"bytes": info["xz_bytes"], "sha256": info["xz_sha256"]}:
        raise ValueError(f"compressed profile identity mismatch: {name}")
    total = 0
    sha = hashlib.sha256()
    with lzma.open(source, "rb") as stream:
        while block := stream.read(1 << 20):
            if total == 0 and block.lstrip().upper().startswith(b"PLACEHOLDER"):
                raise ValueError(f"placeholder profile: {name}")
            total += len(block)
            if total > info["bytes"]:
                raise ValueError(f"uncompressed profile exceeds declared size: {name}")
            sha.update(block)
    if (total, sha.hexdigest()) != (info["bytes"], info["sha256"]):
        raise ValueError(f"uncompressed profile identity mismatch: {name}")


def select(doc, project, pgo, bolt, *, allow_unqualified=False):
    statuses = ("READY", "UNQUALIFIED") if allow_unqualified else ("READY",)
    if doc.get("format") != 1 or doc.get("status") not in statuses:
        raise ValueError("unsupported, unqualified or PLACEHOLDER manifest")
    if project not in ("T", "D") or type(pgo) is not bool or type(bolt) is not bool:
        raise ValueError("invalid project or switch value")
    if not re.fullmatch(r"\d+\.\d+\.\d+", doc["llvm_version"]):
        raise ValueError("invalid LLVM version")
    rows = {}
    for row in doc["profiles"]:
        key = row["project"], row["pgo"], row["bolt"]
        if key[0] not in ("T", "D") or key[1] is not True or type(key[2]) is not bool:
            raise ValueError("invalid mapping key")
        if key in rows:
            raise ValueError("duplicate profile mapping")
        if not row.get("profdata") or bool(row.get("bolt_profile")) != key[2]:
            raise ValueError("invalid mapping assets")
        rows[key] = row
    if not pgo:
        return {"baseline": True} if bolt else None
    if (project, pgo, bolt) not in rows:
        raise ValueError("missing profile mapping")
    return rows[project, pgo, bolt]


def validate(doc, root, project, pgo, bolt, *, allow_unqualified=False):
    row = select(doc, project, pgo, bolt, allow_unqualified=allow_unqualified)
    if pgo:
        for field in ("profdata", "bolt_profile"):
            if field in row:
                verify_asset(row[field], root)
    return row


def pack(source, dest):
    original = file_identity(source)
    with source.open("rb") as stream, dest.open("xb") as raw_output:
        with lzma.LZMAFile(raw_output, "w", format=lzma.FORMAT_XZ, preset=6) as output:
            shutil.copyfileobj(stream, output, length=1 << 20)
    compressed = file_identity(dest)
    result = {"file": dest.name, **original, "xz_bytes": compressed["bytes"],
              "xz_sha256": compressed["sha256"]}
    verify_asset(result, dest.parent)
    return result


def generate(root, project, llvm_version, profdata, fdata, provenance):
    if project not in ("T", "D"):
        raise ValueError("invalid project")
    pg = pack(Path(profdata), root / (project + "-clang.profdata.xz"))
    bolt = pack(Path(fdata), root / (project + "-clang.fdata.xz"))
    doc = {
        "format": 1, "status": "UNQUALIFIED", "llvm_version": llvm_version,
        "provenance": provenance,
        "profiles": [
            {"project": project, "pgo": True, "bolt": False, "profdata": pg},
            {"project": project, "pgo": True, "bolt": True, "profdata": pg, "bolt_profile": bolt},
        ],
    }
    validate(doc, root, project, True, True, allow_unqualified=True)
    with (root / "llvm-profiles.manifest").open("x", encoding="utf-8") as stream:
        json.dump(doc, stream, indent=2)
        stream.write("\n")
    return doc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    check = sub.add_parser("check")
    check.add_argument("--manifest", type=Path, required=True)
    check.add_argument("--project", choices=["T", "D"], required=True)
    for switch in ("pgo", "bolt"):
        check.add_argument("--" + switch, choices=["on", "off"], required=True)
    check.add_argument("--allow-unqualified", action="store_true")
    create = sub.add_parser("generate")
    create.add_argument("--output", type=Path, required=True)
    create.add_argument("--project", choices=["T", "D"], required=True)
    create.add_argument("--llvm-version", required=True)
    for field in ("profdata", "fdata", "provenance"):
        create.add_argument("--" + field, type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.action == "generate":
            doc = generate(args.output, args.project, args.llvm_version, args.profdata,
                           args.fdata, json.loads(args.provenance.read_text(encoding="utf-8")))
        else:
            doc = validate(json.loads(args.manifest.read_text(encoding="utf-8")),
                           args.manifest.parent, args.project, args.pgo == "on", args.bolt == "on",
                           allow_unqualified=args.allow_unqualified)
        print(json.dumps(doc, indent=2))
    except (KeyError, TypeError, ValueError, OSError, lzma.LZMAError) as error:
        parser.exit(1, f"STOP: {error}\n")


if __name__ == "__main__":
    main()
