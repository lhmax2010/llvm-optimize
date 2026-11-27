"""Audit the retained QB package payloads and package-worker logs."""
from collections import Counter, defaultdict, deque
import hashlib
import json
from pathlib import Path
import re
import subprocess

A = Path(__file__).resolve().parent
W = A.parents[1]
B = W.with_name(W.name+"-bolt")
E = A/"evidence"
PS7 = ("1241534","1241535")
PGO = ("1241584","1241585")
ARCH = ("x86_64","aarch64","armv7l")
PACK = ("llvm","clang","llvm-devel")
TARGETS = ("/usr/bin/scan-view","/usr/share/clang/run-find-all-symbols.py",
           "/usr/share/opt-viewer/opt-diff.py","/usr/share/opt-viewer/opt-stats.py",
           "/usr/share/opt-viewer/opt-viewer.py","/usr/share/opt-viewer/optrecord.py")
OLD = B/"tools/bolt/results/task154"
RPM = "/usr/bin/rpm"
EXPECTED = b"#!/usr/bin/env python3"


def read(p):
    return json.loads(p.read_text())


def save(p,data):
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")


def text(*cmd):
    return subprocess.check_output(list(map(str,cmd)),text=True,errors="strict")


def receipt(path):
    with path.open("rb") as f:
        sha=hashlib.file_digest(f,"sha256").hexdigest()
    return {"path":str(path),"bytes":path.stat().st_size,"sha256":sha}


def relevant(path):
    return (path in ("/usr/bin/scan-build","/usr/bin/scan-build-py","/usr/bin/scan-view") or
            re.match(r"^/usr/share/man/man1/scan-build\.1(?:\.gz)?$",path) is not None or
            re.match(r"^/(?:usr/share/(?:scan-build|scan-view)|usr/lib(?:64)?/(?:libscanbuild|libear))(?:/|$)",path) is not None)


def extract(rpm, root, paths):
    root.mkdir(parents=True,exist_ok=True)
    argv=["/usr/bin/cpio","-idmu","--quiet","--no-absolute-filenames","--",*("." + p for p in paths)]
    with subprocess.Popen(["/usr/bin/rpm2cpio",str(rpm)],stdout=subprocess.PIPE) as source:
        subprocess.run(argv,stdin=source.stdout,cwd=root,check=True)
        source.stdout.close()
        if source.wait():
            raise RuntimeError(f"rpm2cpio failed: {rpm}")


def args_diff(a,b):
    return {"added":sorted((b-a).elements()),"removed":sorted((a-b).elements())}


def normal_requires(rows):
    return Counter(re.sub(r"^llvm = 22\.1\.8-[\d.]+$","llvm = 22.1.8-<release>",r) for r in rows)


def audit_ps7(downloads):
    items={(r["build"],r["arch"],r["package"]):r for r in downloads}
    expected={p:{x for x in r if relevant(x)} for p,r in read(OLD/"expected-rpm-paths.json").items()}
    baseline=(OLD/"attempt-1/evidence/clang-requires-new.txt").read_text().splitlines()
    results={}
    for build in PS7:
        results[build]={}
        for arch in ARCH:
            out=E/build/arch
            out.mkdir(parents=True,exist_ok=True)
            chosen={p:Path(items[build,arch,p]["path"]) for p in PACK}
            source={}
            paths={}
            for name,path in chosen.items():
                info=text(RPM,"-qp","--qf","%{NAME}\n%{VERSION}-%{RELEASE}\n%{ARCH}\n%{SOURCERPM}\n%{VCS}\n",path)
                (out/(name+"-rpm-header.txt")).write_text(info)
                row=info.splitlines()
                if row[0]!=name or row[2]!=arch:
                    raise RuntimeError(f"RPM identity mismatch {path}: {info}")
                source[name]={"name":row[0],"version_release":row[1],"arch":row[2],"srpm":row[3],"vcs":row[4]}
                listing=text(RPM,"-qpl",path)
                (out/(name+"-rpm-qlp.txt")).write_text(listing)
                paths[name]=set(listing.splitlines())
            gist={k:sorted(x for x in v if relevant(x)) for k,v in paths.items()}
            reference={p:expected[p+":x86_64"] for p in PACK}
            ownership={}
            for name in PACK:
                ownership[name]={"added":sorted(set(gist[name])-reference[name]),
                                 "missing":sorted(reference[name]-set(gist[name]))}
            clash=set()
            for i,left in enumerate(PACK):
                for right in PACK[i+1:]:
                    clash|=set(gist[left])&set(gist[right])
            shebangs={}
            for name in PACK:
                expected_targets=[p for p in TARGETS if p in paths[name]]
                extract_root=A/build/"extract"/arch/name
                if expected_targets:
                    extract(chosen[name],extract_root,expected_targets)
                for path in expected_targets:
                    f=extract_root/path.lstrip("/")
                    with f.open("rb") as stream:
                        first=stream.readline().removesuffix(b"\n")
                    shebangs.setdefault(path,[]).append({"owner":name,"first_line":first.decode("ascii",errors="replace"),
                                                          "pass":first==EXPECTED})
            all_shebangs=all(len(shebangs.get(path,[]))==1 and shebangs[path][0]["pass"] for path in TARGETS)
            req=text(RPM,"-qp","--requires",chosen["clang"])
            (out/"clang-requires.txt").write_text(req)
            rows=req.splitlines()
            requires={"python_entries":[row for row in rows if re.search("python",row,re.I)],
                      "reference":str(OLD/"attempt-1/evidence/clang-requires-new.txt"),
                      "same_arch_available":arch=="x86_64"}
            if arch=="x86_64":
                requires.update(exact_diff=args_diff(Counter(baseline),Counter(rows)),
                                after_llvm_release_normalization=args_diff(normal_requires(baseline),
                                                                           normal_requires(rows)))
            log=read(E/build/(arch+"-log-audit.json"))
            result={"headers":source,"relevant_paths":gist,"relative_to_154B_relevant_set":ownership,
                    "duplicate_paths":sorted(clash),"ownership_pass":not clash and not any(
                         row["added"] or row["missing"] for row in ownership.values()),
                    "shebangs":shebangs,"shebang_pass":all_shebangs,"requires":requires,"log":log}
            save(out/"audit.json",result)
            results[build][arch]=result
    save(E/"ps7-audit.json",results)


def inspect_log(build,arch):
    p=A/build/(arch+".buildlog.txt")
    out=E/build
    out.mkdir(parents=True,exist_ok=True)
    status=read(A/build/"public-log-locations.json")[arch]["result"]["status"]
    starts, ends, architecture, unpackaged, gates, check_raw = [],[],[],[],[],[]
    post_checks, current_path, context_before= {},None,deque(maxlen=40)
    first_error, context_after, arg_lines = None, [], []
    with p.open("rb") as stream:
        for i,raw in enumerate(stream,1):
            line=raw.decode("utf-8",errors="replace").rstrip("\n")
            if "started \"build llvm.spec\"" in line:
                starts.append({"line":i,"text":line})
            if ('finished "build llvm.spec"' in line or 'failed "build llvm.spec"' in line):
                ends.append({"line":i,"text":line})
            if "Building llvm for project" in line:
                architecture.append(line)
            if re.search(r"Installed \(but unpackaged\) file\(s\)",line,re.I):
                unpackaged.append({"line":i,"text":line})
            if re.search(r"PGO_NINJA_CHECK|PGO_MATCH|PGO_RUNTIME_CHECK|ARCHIVE_MEMBER_RETRY|BOLT_(?:REAL_GATE_PASS|POST_GATE_PASS|PIPELINE_PASS)|stale-threshold",line):
                gates.append({"line":i,"text":line})
            if "pgo-prepare" in line and line.find("+ python3")!=-1:
                arg_lines.append({"line":i,"text":line})
            if re.search(r"\+\+ head -n 1\s+",line):
                current_path=next((t for t in TARGETS if line.endswith(t)),None)
                if current_path:
                    check_raw.append(f"{i}: {line}\n")
            if current_path and re.search(r"\+ test ",line):
                post_checks[current_path]={"line":i,"original":line,
                    "matched":line.endswith("test '#!/usr/bin/env python3' = '#!/usr/bin/env python3'")}
                check_raw.append(f"{i}: {line}\n")
                current_path=None
            if status=="failed":
                if not first_error and "clang-bolt-helper.py: error: unrecognized arguments:" in line:
                    first_error={"line":i,"text":line,"from_line":i-len(context_before)}
                    context_after=[*context_before,raw]
                elif first_error and i <= first_error["line"]+40:
                    context_after.append(raw)
                context_before.append(raw)
    if first_error:
        first_error["to_line"]=first_error["from_line"]+len(context_after)-1
        (out/(arch+"-first-error-40x40.txt")).write_bytes(b"".join(context_after))
    if check_raw:
        (out/(arch+"-shebang-log.txt")).write_text("".join(check_raw))
    result={"artifact":receipt(p),"publication_bucket":status,"worker_start":starts,"worker_end":ends,
            "project_and_arch":architecture,"first_error":first_error,"pgo_prepare":arg_lines,
            "unpackaged":unpackaged,"gate_lines":gates,"post_checks":post_checks,
            "post_checks_pass":all(post_checks.get(t,{}).get("matched") for t in TARGETS)}
    save(out/(arch+"-log-audit.json"),result)
    return result


if __name__ == "__main__":
    for b in (*PS7,*PGO):
        for arch in ARCH:
            item=inspect_log(b,arch)
            print(b,arch,item["publication_bucket"],item["post_checks_pass"],
                   bool(item["unpackaged"]), item["first_error"],flush=True)
    downloads=A/"ps7-downloads.json"
    if downloads.is_file():
        audit_ps7(read(downloads))
