"""Produce held-out Tizen inputs from package commands, writing only .i/.ii."""
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
from datetime import datetime

from configure_corpus import A, W, B, CONF, LAUNCHER, TARGET, ENV, pause, source

E = A / "evidence"
OUT = A / "corpus"
OUTPUT = {".c": "c", ".cpp": "c++", ".cc": "c++", ".cxx": "c++"}
EXTERNAL_PACKAGES = ("bzip2", "expat", "icu", "jsoncpp", "libwebp", "sqlite", "tinyxml2")
BASE_URL = ("http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Dev/"
            "tizen-base-dev_20261030.061217/repos/standard/source/")


def read(path):
    return json.loads(path.read_text())


def save(path, doc):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    tmp.replace(path)


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def band(size):
    return "small" if size < 262144 else "medium" if size < 8388608 else "large"


def input_receipt(path, sha=None):
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha or digest(path)}


def source_identity(path):
    # Translation units with the same package/path across targets are still
    # the same source. Basenames are independently checked conservatively.
    parts = Path(path).parts
    for index, name in enumerate(parts):
        if re.fullmatch(r"llvm-22\.1\.8|source-c2", name):
            return "llvm/" + "/".join(parts[index + 1:])
    return str(path)


def training_index():
    config = read(W / "archive/task151/G-config/config.json")
    receipt = Path(config["training"])
    rows = read(receipt)
    assert len(rows) == 23
    kit = W / "archive/server-kit-136/server-kit-remote/skill/references/training-set.json"
    keys = ("name", "target", "bytes", "sha256")
    identity = lambda data: sorted(tuple(row[key] for key in keys) for row in data)
    assert identity(rows) == identity(read(kit)), "server-kit and the runnable training input identities disagree"
    entries = []
    for row in rows:
        path = (receipt.parent / row["file"]).resolve(strict=True)
        with path.open("rb") as stream:
            first = stream.readline().decode(errors="replace")
        marker = re.match(r'^#\s+\d+\s+"([^"]+)"', first)
        src = marker[1] if marker else str(path)
        assert (path.stat().st_size, digest(path)) == (row["bytes"], row["sha256"])
        entries.append({"name": row["name"], "target": row["target"], "sha256": row["sha256"],
                        "source": src, "source_identity": source_identity(src), "source_basename": Path(src).name})
    return {"manifest": input_receipt(receipt), "server_kit": input_receipt(kit), "entries": entries}


def cdb(pkg):
    f = CONF / pkg / "compile_commands.json"
    if not f.is_file():
        return []
    rows = []
    for entry in read(f):
        cmd = entry.get("arguments") or shlex.split(entry["command"])
        cwd = Path(entry["directory"])
        unit = (cwd / entry["file"]).resolve()
        if unit.suffix in OUTPUT:
            rows.append((unit, cwd, cmd[1:]))
    return rows


def make_dry(pkg):
    f = CONF / pkg / "make-dry.txt"
    if not f.is_file():
        return []
    options = {str(CONF / name) for name in ("cc", "cxx", "cc-configure", "cxx-configure")}
    build = CONF / pkg
    cwd = {"icu": build / "common", "bzip2": source("bzip2")}.get(pkg, build)
    rows = []
    directories = [cwd]
    for line in f.read_text().replace("\\\n", " ").splitlines():
        event = re.search(r" (Entering|Leaving) directory '([^']+)'$", line)
        if event:
            if event[1] == "Entering":
                directories.append(Path(event[2]))
            elif len(directories) > 1:
                directories.pop()
            continue
        cwd = directories[-1]
        if " -c " not in line or not any(name in line for name in options):
            continue
        try:
            cmd = shlex.split(line)
        except ValueError:
            continue
        start = next((i for i, option in enumerate(cmd) if option in options), None)
        if start is None:
            continue
        end = cmd.index("||", start) if "||" in cmd[start:] else len(cmd)
        args = cmd[start + 1:end]
        paths = [(cwd / option).resolve() for option in args if not option.startswith("-")
                 and Path(option).suffix in OUTPUT and (cwd / option).is_file()]
        if len(paths) == 1:
            rows.append((paths[0], cwd, args))
    return rows


def args_for(unit, cwd, args):
    flags = []
    consume = {"-o", "-MF", "-MT", "-MQ"}
    skip_value = False
    for opt in args:
        if skip_value:
            skip_value = False
            continue
        if opt in consume:
            skip_value = True
        elif opt in {"-c", "-MD", "-MMD", "-M", "-MP"} or re.fullmatch(r"-O(?:\d+|s|z|fast|g)", opt):
            continue
        elif opt.startswith("-Wl,") or (Path(opt).suffix in OUTPUT and (cwd / opt).resolve() == unit):
            continue
        else:
            flags.append(opt)
    return ["-O2", *flags]


def compile_flags(input_flags):
    flags = ["--target=" + TARGET]
    skip_value = False
    for flag in input_flags:
        if skip_value:
            skip_value = False
            continue
        if flag in ("-I", "-isystem", "-iquote", "-include", "-imacros"):
            skip_value = True
        elif not flag.startswith(("-I", "-isystem", "-iquote", "-include", "-imacros")):
            flags.append(flag)
    return flags


def prep_candidates():
    for pkg in EXTERNAL_PACKAGES:
        if pkg in ("jsoncpp", "libwebp"):
            rows = cdb(pkg)
        elif pkg == "tinyxml2":
            # Meson selects only this library source. The target's PIC
            # option and the spec optflags are retained.
            from configure_corpus import FLAGS
            base = source(pkg)
            if not (base / "tinyxml2.cpp").exists():
                continue
            rows = [(base / "tinyxml2.cpp", base, [*FLAGS, "-fPIC", "-I"+str(base)])]
        else:
            rows = make_dry(pkg)
        for unit, cwd, flags in rows:
            if unit.is_file() and unit.is_relative_to(source(pkg)):
                yield pkg, unit, cwd, flags


def verify_holdout(inputs, training):
    source_names = {r["source_basename"] for r in training["entries"]}
    source_ids = {r["source_identity"] for r in training["entries"]}
    hashes = {r["sha256"] for r in training["entries"]}
    seen, seen_hashes, verified, rejected = set(), set(), [], []
    for row in inputs:
        source = row["source_tu"]
        identity = source_identity(source)
        if identity in source_ids or Path(source).name in source_names or row["sha256"] in hashes:
            rejected.append({"id": row["id"], "source": source, "reason": "training source or input identity"})
        elif identity in seen or row["sha256"] in seen_hashes:
            rejected.append({"id": row["id"], "source": source, "reason": "duplicate corpus source or SHA"})
        else:
            verified.append(dict(row, source_identity=identity, training_source_overlap=False,
                                 training_sha256_overlap=False))
            seen.add(identity)
            seen_hashes.add(row["sha256"])
    return verified, rejected


def expand():
    OUT.mkdir(exist_ok=True)
    train = training_index()
    initial = read(W / "archive/task156/evidence/benchmark-config.json")
    old = initial["inputs"]
    for row in old:
        pause()
        path = Path(row["path"])
        assert (path.stat().st_size, digest(path)) == (row["bytes"], row["sha256"])
    source_names = {r["source_basename"] for r in train["entries"]}
    manifest, failed, cmd_rows = [], [], []
    seen = set()
    footprints = Counter(row["language"] for row in old)
    candidates = list(prep_candidates())
    # Prefer breadth. Keep enough C and C++ and give each small package a
    # chance before taking the remaining large-package units.
    for pkg, unit, cwd, args in candidates:
        if unit in seen or unit.name in source_names:
            continue
        seen.add(unit)
        language = OUTPUT[unit.suffix]
        if pkg in ("icu", "libwebp") and footprints[language] >= 86:
            continue
        pause()
        ident = pkg + "-" + re.sub(r"[^A-Za-z0-9_-]", "-", str(unit.relative_to(source(pkg))))
        output = OUT / (ident + (".i" if language == "c" else ".ii"))
        original = args_for(unit, cwd, args)
        command = LAUNCHER + ["-E", "-x", language, *original, str(unit), "-o", str(output)]
        try:
            p = subprocess.run(command, cwd=cwd, env=ENV, text=True, capture_output=True, timeout=90)
            if p.returncode or not output.is_file() or not output.stat().st_size:
                failed.append({"source":str(unit),"command":command,"rc":p.returncode,"stderr":p.stderr})
                continue
        except (OSError, subprocess.TimeoutExpired) as error:
            failed.append({"source":str(unit),"command":command,"error":str(error)})
            continue
        meta = input_receipt(output)
        src_rpm, = (A / "corpus-inputs").glob(pkg + "-*.src.rpm")
        manifest.append({"id":ident,"package":pkg,"language":language,"target":TARGET,"source_tu":str(unit),
                         "package_source":BASE_URL + src_rpm.name,"source_sha256":digest(unit),
                         "size_band":band(meta["bytes"]),"flags":compile_flags(original),**meta})
        cmd_rows.append({"id":ident,"cwd":str(cwd),"source":str(unit),"configured_args":args,"preprocess":command,
                         "stderr":p.stderr})
        footprints[language] += 1
    verified, rejected = verify_holdout(old + manifest, train)
    initial["inputs"] = verified
    stats = {"status":"PASS" if len(verified)>=150 and len({r["package"] for r in verified})>=6 else "PARTIAL",
             "package_build_active":False,"at":datetime.now().astimezone().isoformat(),
             "preprocessing_only":True,"inputs":len(verified),"new":len(manifest),"prepare_failures":len(failed),
             "packages":dict(Counter(r["package"] for r in verified)),
             "languages":dict(Counter(r["language"] for r in verified)),
             "size_bands":dict(Counter(r["size_band"] for r in verified)),
             "size_min":min(r["bytes"] for r in verified),"size_max":max(r["bytes"] for r in verified),
             "total_bytes":sum(r["bytes"] for r in verified)}
    save(E/"corpus-training-identity.json",train)
    save(E/"corpus-config.json",initial)
    save(E/"corpus-preprocessing.json",cmd_rows)
    save(E/"corpus-exclusions.json",{"failed":failed,"training_or_duplicate":rejected})
    save(E/"corpus-summary.json",stats)
    save(A/"corpus-state.json",stats)
    print(json.dumps(stats,ensure_ascii=False))


if __name__ == "__main__":
    expand()
