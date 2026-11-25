import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

W=Path("/home/linhao/Toolchain/development/llvm-optimize")
B=W.with_name(W.name+"-bolt")
A=W/"archive/task152"
E=A/"evidence"
R1=B/"tools/bolt/results/task144/b1-audit-rpms.json"
R2=W/"archive/task145/b2-corrected-a1/evidence/rpms.json"

def run(args, file=None):
    print(" ".join(map(str,args)),flush=True)
    if file:
        with (E/file).open("wb") as out:
            subprocess.run(args,stdout=out,check=True)
        return
    return subprocess.check_output(args).decode()

def sha(path):
    with path.open("rb") as f: return hashlib.file_digest(f,"sha256").hexdigest()

def unpack(path, names, sub):
    directory=A/"payload"/sub
    directory.mkdir()
    with subprocess.Popen(["/usr/bin/rpm2cpio",str(path)],stdout=subprocess.PIPE) as p:
        try:
            subprocess.run(["/usr/bin/cpio","--extract","--make-directories","--no-absolute-filenames","--quiet",
                            "--",*["."+name for name in names]],cwd=directory,stdin=p.stdout,check=True)
        finally:
            p.stdout.close()
        if p.wait()!=0:
            raise RuntimeError("rpm2cpio failed: "+str(path))
    for n in names:
        assert (directory/n.lstrip("/")).is_file(),n
    return [directory/n.lstrip("/") for n in names]

def nm(file, flags, out):
    args=["/usr/bin/nm",*flags,str(file)]
    with (E/(out+".mangled.txt")).open("wb") as f:
        subprocess.run(args,stdout=f,check=True)
    with (E/(out+".mangled.txt")).open("rb") as src,(E/(out+".txt")).open("wb") as dst:
        subprocess.run(["/usr/bin/c++filt"],stdin=src,stdout=dst,check=True)

b1,b2=(json.loads(p.read_text()) for p in (R1,R2))
pkgs={}
audit=[]
for src,names in ((b1,("libllvm","llvm","clang")),(b2,("bolt","bolt-debuginfo","llvm-tools-subpkgs-debugsource"))):
    for name in names:
        row=next(x for x in src if Path(x["path"]).name==name+"-22.1.8-1.x86_64.rpm")
        path=Path(row["path"])
        assert path.resolve().is_relative_to(W) and path.stat().st_size==row["bytes"]
        assert sha(path)==row["sha256"],path
        audit.append({**row,"package":name,"receipt_matches":True})
        pkgs[name]=path
        run(["/usr/bin/rpm","-qlp",str(path)],name+"-rpm-qlp.txt")
        run(["/usr/bin/rpm","-qp","--requires",str(path)],name+"-rpm-requires.txt")
(E/"rpm-identities.json").write_text(json.dumps(audit,indent=2)+"\n")

[lib]=unpack(pkgs["libllvm"],["/usr/lib64/libLLVM.so.22.1"],"libllvm")
[exe]=unpack(pkgs["bolt"],["/usr/bin/llvm-bolt"],"bolt")
[debug]=unpack(pkgs["bolt-debuginfo"],["/usr/lib/debug/usr/bin/llvm-bolt.debug"],"bolt-debug")
ds=(E/"llvm-tools-subpkgs-debugsource-rpm-qlp.txt").read_text().splitlines()
source=[p for p in ds if p.endswith(("/X86GenMnemonicTables.inc","/X86BoltMnemonicTables.cpp",
                                     "/X86GenSubSuperRegisterBody.inc","/X86GenNeedsAddressSizeOverrideBody.inc"))]
for p in unpack(pkgs["llvm-tools-subpkgs-debugsource"],source,"bolt-debugsource"):
    (E/p.name).write_bytes(p.read_bytes())
nm(lib,["-D","--defined-only"],"libllvm-defined")
nm(exe,["-D","--undefined-only"],"bolt-undefined")
nm(debug,["--defined-only"],"bolt-debug-defined")
for name,path in (("bolt",exe),("bolt-debug",debug)):
    run(["/usr/bin/readelf","--wide","--notes",str(path)],name+"-notes.txt")
run(["/usr/bin/readelf","--wide","--dynamic",str(exe)],"bolt-dynamic.txt")
run(["/usr/bin/readelf","--wide","--hex-dump=.gnu_debuglink",str(exe)],"bolt-debuglink.txt")

package_owners={}
needle=re.compile(r"/usr/(?:lib(?:64)?/(?:libscanbuild|libear)(?:/|$)|share/(?:scan-build(?:-py)?|scan-view)(?:/|$)|share/man/[^/]+/scan-(?:build|view)[^/]*|libexec/(?:ccc-analyzer|c\+\+-analyzer|intercept-c(?:c|\+\+))$|bin/(?:analyze-build|intercept-build|scan-build|scan-build-py|scan-view)$)")
for row in b1:
    path=Path(row["path"])
    if "/RPMS/" not in str(path):
        continue
    checked=run(["/usr/bin/rpm","-qlp",str(path)]).splitlines()
    package_owners[path.name]={"file_count":len(checked),
                              "matches":[line for line in checked if needle.fullmatch(line) or needle.search(line)]}
(E/"b1-analyzer-package-owners.json").write_text(json.dumps(package_owners,indent=2)+"\n")
for n,prefixes in (("llvm",("/usr/bin/analyze-build","/usr/bin/intercept-build","/usr/bin/scan-build","/usr/bin/scan-build-py","/usr/bin/scan-view")),
                   ("clang",("/usr/libexec/ccc-analyzer","/usr/libexec/c++-analyzer","/usr/libexec/intercept-cc","/usr/libexec/intercept-c++"))):
    unpack(pkgs[n],prefixes,n+"-analyzer")
