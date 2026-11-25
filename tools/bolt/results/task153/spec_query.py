import json,os,subprocess
from pathlib import Path
A=Path("/home/linhao/Toolchain/development/llvm-optimize/archive/task153")
W=A.parents[1]
B=W.with_name(W.name+"-bolt")
E=A/"evidence"
R=W/"temp/rebase-359934-20261111-r6/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0"
MACROS=B/"tools/bolt/results/fifth-review-20261111/rerun4/parse"
BASE=[str(R/"usr/lib64/ld-linux-x86-64.so.2"),"--library-path",str(R/"usr/lib64"),str(R/"usr/bin/rpmspec")]
env={**os.environ,"RPM_CONFIGDIR":str(R/"usr/lib/rpm"),"LC_ALL":"C"}
def read(*args):
    return subprocess.check_output([*BASE,*args],env=env,text=True)
version=read("--version")
assert "4.14.1" in version,version
(E/"rpm-version.txt").write_text(version)
showrc=read("--showrc")
path=next(line.split(": ",1)[1] for line in showrc.splitlines() if line.startswith("Macro path:"))
rpmmacros=":".join(p for p in path.split(":") if p.startswith(str(R)))
(E/"rpm-macro-path.txt").write_text(rpmmacros+"\n")
evrs={"llvm":{"llvm-xray","llvm-prof-tools"},"clang":{"clang-analyzer"}}
wanted={n:p for p,ns in evrs.items() for n in ns}
argsfile=[]
report=[]
def run(arch,name,args):
    cmd=[*BASE,*args]
    p=subprocess.run(cmd,env=env,text=True,capture_output=True)
    (E/(arch+"-"+name+".txt")).write_text(p.stdout)
    (E/(arch+"-"+name+".stderr")).write_text(p.stderr)
    argsfile.append({"argv":cmd,"returncode":p.returncode,"output":arch+"-"+name+".txt"})
    return p
for arch in ("x86_64","aarch64","armv7l"):
    macro_name="x86-debug" if arch=="x86_64" else arch
    macro=MACROS/f"toolchain-{macro_name}.macros"
    assert macro.exists()
    opts=["--macros",rpmmacros+":"+str(macro),"--target",arch+"-tizen-linux",
          "--define","_toolchain clang","--define","_topdir "+str(A/"rpm-query"),"--define","_sourcedir "+str(E)]
    row={"arch":arch,"status":"PASS","data":{}}
    for command in ("provides","obsoletes"):
        prefix=command[:-1].upper()
        tags="[%{=NAME}\t%{=ARCH}\t%{"+prefix+"NAME}\t%{"+prefix+"FLAGS:depflags}\t%{"+prefix+"VERSION}\n]"
        raw=run(arch,command,["-q","--"+command,*opts,str(E/"patch1-llvm.spec")])
        selected=run(arch,command+"-with-package",["-q","--qf",tags,*opts,str(E/"patch1-llvm.spec")])
        matches=[]
        for line in selected.stdout.splitlines():
            parts=line.split("\t")
            if len(parts)==5 and parts[2] in wanted:
                pkg,target,name,op,evr=parts
                matches.append({"package":pkg,"arch":target,"dependency":name,"op":op,"evr":evr,"raw":line})
        op="=" if command=="provides" else "<"
        expected=True if len(matches)==3 else False
        for r in matches:
            expected &= (r["package"]==wanted[r["dependency"]] and r["arch"]==arch and r["op"]==op and r["evr"]=="22.1.8-1")
        if raw.returncode or selected.returncode or not expected:
            row["status"]="FAIL"
        row["data"][command]=matches
    report.append(row)
(E/"rpmspec-command-records.json").write_text(json.dumps(argsfile,indent=2)+"\n")
(E/"rpmspec-results.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
raise SystemExit(any(x["status"]!="PASS" for x in report))
