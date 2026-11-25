from collections import defaultdict
from pathlib import Path
import json, os, re, stat, subprocess

A=Path(__file__).resolve().parent
W=A.parents[1]
B=W.with_name(W.name+"-bolt")
E=A/"evidence"
R=W/"temp/rebase-359934-20261111-r6/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0"
RPM=("/usr/bin/rpm",)
PARSE=(str(R/"usr/lib64/ld-linux-x86-64.so.2"),"--library-path",str(R/"usr/lib64"),str(R/"usr/bin/rpmspec"))
MACROS=B/"tools/bolt/results/fifth-review-20261111/rerun4/parse"
B1=B/"tools/bolt/results/task152/b1-analyzer-package-owners.json"
BINS={"/usr/bin/"+n for n in ("analyze-build","intercept-build","scan-build","scan-build-py")}
WRAPPERS={"/usr/libexec/"+n for n in ("analyze-c++","analyze-cc","c++-analyzer","ccc-analyzer","intercept-c++","intercept-cc")}
SCANBUILD={"/usr/share/scan-build/"+n for n in ("scanview.css","sorttable.js")}
SCANVIEW={"/usr/share/scan-view/"+n for n in ("ScanView.py","Reporter.py","startfile.py","bugcatcher.ico")}
MODULE_DIRS={"/usr/lib/libear","/usr/lib/libscanbuild","/usr/lib/libscanbuild/resources"}
ENV={**os.environ,"LC_ALL":"C","RPM_CONFIGDIR":str(R/"usr/lib/rpm")}

def receipt(name,obj):
    (E/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n")
def read(cmd, *args):
    return subprocess.check_output([*cmd,*map(str,args)],text=True,env=ENV if cmd==PARSE else {**os.environ,"LC_ALL":"C"})
def targets():
    logs=json.loads((E/"module-install-history.json").read_text())
    files=set(logs["B1"]["installed"])
    assert len(files)==14
    return files

def package_files(rpms):
    rows={}
    for file in sorted(rpms):
        pkg=read(RPM,"-qp","--qf","%{NAME}:%{ARCH}",file)
        assert pkg not in rows,pkg
        listing=set(read(RPM,"-qlp",file).splitlines())-{"(contains no files)"}
        modes={p:int(m) for p,m in (ln.rsplit("\t",1) for ln in read(
            RPM,"-qp","--qf","[%{FILENAMES}\t%{FILEMODES}\n]",file).splitlines())}
        assert listing==modes.keys(),(pkg,listing^modes.keys())
        rows[pkg]=modes
    return rows

def file_map(pkgs):
    owners=defaultdict(set)
    for name,files in pkgs.items():
        for path in files:
            owners[path].add(name)
    return owners

def sequence(pkgs):
    b1={pkg:set(paths) for pkg,paths in pkgs.items()}
    post_ps6={pkg:set(paths) for pkg,paths in b1.items()}
    llvm,devel,clang="llvm:x86_64","llvm-devel:x86_64","clang:x86_64"
    base=file_map(b1)
    for path in BINS:
        assert base[path] == {llvm},(path,base[path])
        post_ps6[llvm].remove(path)
        post_ps6[clang].add(path)
    before=file_map(post_ps6)
    p5={pkg:set(paths) for pkg,paths in post_ps6.items()}
    moved={}
    for path in sorted(post_ps6[devel]):
        if path=="/usr/share/scan-view" or path.startswith("/usr/share/scan-view/"):
            want=llvm
        elif path=="/usr/share/scan-build" or path.startswith("/usr/share/scan-build/") or path.startswith("/usr/share/man/man1/scan-build.1"):
            want=clang
        else:
            continue
        assert before[path]=={devel},(path,before[path])
        p5[devel].remove(path)
        p5[want].add(path)
        moved[path]=want
    files=file_map(p5)
    assert files.keys()==before.keys()
    assert {p for p in files if files[p]!=before[p]}==moved.keys()
    assert all(files[p]=={d} for p,d in moved.items())
    assert all(files[p]=={clang} for p in BINS|WRAPPERS|SCANBUILD)
    assert all(files[p]=={llvm} for p in SCANVIEW|{"/usr/bin/scan-view"})
    assert any(p.startswith("/usr/share/man/man1/scan-build.1") and files[p]=={clang} for p in moved)
    duplicate_files=[p for p,s in files.items() if len(s)>1 and any(not stat.S_ISDIR(pkgs[k][p]) for k in s)]
    duplicate_dirs=[p for p,s in files.items() if len(s)>1 and p not in duplicate_files]
    assert all(files[p]==base[p] for p in duplicate_files)
    assert not (set(duplicate_files) & (set(moved)|BINS|WRAPPERS|SCANBUILD|SCANVIEW))
    baseline_duplicates = {p:sorted(files[p]) for p in sorted(duplicate_files)}
    p6={pkg:set(paths) for pkg,paths in p5.items()}
    added=targets()|MODULE_DIRS
    assert not (added & files.keys()),added & files.keys()
    p6[clang].update(added)
    result={"package_count":len(b1),"paths_before":len(base),"paths_after_p5":len(files),
            "paths_after_p6":len(file_map(p6)),"ps6_baseline_moves":sorted(BINS),
            "patch5_move_count":len(moved),"patch5_moved":moved,
            "patch5_lost":[],"patch5_added":[],"duplicate_affected_files":[],"preexisting_duplicate_files":baseline_duplicates,
            "shared_directories":sorted(duplicate_dirs),"patch6_expected_added":sorted(added),
            "patch6_required_files":sorted(targets()),
            "scan_build_direct_resources":sorted(BINS|WRAPPERS|SCANBUILD),
            "scan_view_direct_resources":sorted(SCANVIEW|{"/usr/bin/scan-view"})}
    return result,p6

def expand_and_check():
    version=read(PARSE,"--version")
    assert "4.14.1" in version,version
    (E/"rpm-version.txt").write_text(version)
    macro=next(l.split(": ",1)[1] for l in read(PARSE,"--showrc").splitlines() if l.startswith("Macro path:"))
    macro=":".join(x for x in macro.split(":") if x.startswith(str(R)))
    records=[]
    for arch in ("x86_64","aarch64","armv7l"):
        target=MACROS/f"toolchain-{'x86-debug' if arch=='x86_64' else arch}.macros"
        opts=["--macros",macro+":"+str(target),"--target",arch+"-tizen-linux",
              "--define","_toolchain clang","--define","_topdir "+str(A/"static-rpm"),"--define","_sourcedir "+str(E)]
        for step in ("p5","p6"):
            cmd=[*PARSE,"-P",*opts,str(E/f"{step}-llvm.spec")]
            p=subprocess.run(cmd,capture_output=True,text=True,env=ENV)
            base=f"{arch}-{step}"
            (E/(base+".txt")).write_text(p.stdout)
            (E/(base+".stderr")).write_text(p.stderr)
            assert p.returncode==0,(cmd,p.stderr)
            blocks={}
            for name,content in re.findall(r"(?m)^%files([^\n]*)\n((?:(?!^%files).|\n)*)",p.stdout):
                blocks[name.strip()]=content.splitlines()
            assert "/usr/share/scan-view" in blocks[""]
            assert "/usr/share/scan-build" in blocks["-n clang"]
            for excluded in ("/usr/share/scan-build","/usr/share/scan-view","/usr/share/man/man1/scan-build.1*"):
                assert f"%exclude {excluded}" in blocks["devel"],(arch,step,excluded)
            assert "/usr/share/man/man1/scan-build.1*" in blocks["-n clang"]
            for path in ("/usr/lib/libscanbuild","/usr/lib/libear"):
                assert (path in blocks["-n clang"])==(step=="p6")
                assert bool(re.search(r"(?m)^rm -rf .*"+path+r"/\*",p.stdout))==(step=="p5")
            clang_header=p.stdout.split("%package -n clang\n",1)[1].split("%description",1)[0]
            assert not re.search(r"(?mi)^Requires:\s+.*\bpython3\b",clang_header)
            records.append({"arch":arch,"step":step,"argv":cmd,"status":"PASS"})
    receipt("rpmspec-results.json",records)

if __name__=="__main__":
    old=json.loads(B1.read_text())
    rpms=[Path(r["path"]) for r in old.values()]
    assert len(rpms)==22
    pkgs=package_files(rpms)
    lookup={Path(r["path"]):r for r in old.values()}
    for p in rpms:
        assert p.stat().st_size==lookup[p]["bytes"]
        name=read(RPM,"-qp","--qf","%{NAME}:%{ARCH}",p)
        assert len(pkgs[name])==lookup[p]["file_count"]
    checks,expected=sequence(pkgs)
    receipt("static-package-simulation.json",checks)
    receipt("expected-rpm-paths.json",{n:sorted(v) for n,v in expected.items()})
    expand_and_check()
    print(json.dumps(checks,indent=2))
