from pathlib import Path
import json,os,re,subprocess,sys
A=Path("/home/linhao/Toolchain/development/llvm-optimize/archive/task153")
W=A.parents[1]
E=A/"evidence"
T=A/"transactions"
R=W/"temp/rebase-359934-20261111-r6/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0"
L=[str(R/"usr/lib64/ld-linux-x86-64.so.2"),"--library-path",str(R/"usr/lib64")]
env={**os.environ,"LC_ALL":"C","RPM_CONFIGDIR":str(R/"usr/lib/rpm"),"HOME":str(T)}
rpm=[*L,str(R/"usr/bin/rpm")]
builder=[*L,str(R/"usr/bin/rpmbuild")]
macro=(E/"rpm-macro-path.txt").read_text().strip()
argv_records=[]
T.mkdir(exist_ok=False)
for name in ("BUILD","BUILDROOT","RPMS","SOURCES","SPECS","SRPMS","tmp"):
    (T/name).mkdir()

def run(name,argv):
    p=subprocess.run(list(map(str,argv)),cwd=T,text=True,capture_output=True,env=env)
    (T/(name+".stdout.txt")).write_text(p.stdout)
    (T/(name+".stderr.txt")).write_text(p.stderr)
    argv_records.append({"check":name,"argv":list(map(str,argv)),"rc":p.returncode,"stdout":p.stdout,"stderr":p.stderr})
    print(name,p.returncode,flush=True)
    return p

def need(name,argv):
    p=run(name,argv)
    if p.returncode:
        raise RuntimeError(f"{name}: {p.stderr}")
    return p

def make(key,name,version,release,epoch="0",header=""):
    assert all(re.fullmatch(r"[A-Za-z0-9.+_~^]+",x) for x in (version,release,epoch))
    spec=T/"SPECS"/(key+".spec")
    spec.write_text(f"""Name: {name}
Version: {version}
Release: {release}
Epoch: {epoch}
Summary: RPM transaction fixture
License: MIT
BuildArch: noarch
AutoReqProv: no
{header}
%description
Header-only package for checking rename semantics.

%files
""")
    need("build-"+key,[*builder,"-bb","--macros",macro,"--target","x86_64-tizen-linux",
        "--define","_topdir "+str(T),"--define","_tmppath "+str(T/"tmp"),
        "--define","_build_id_links none","--define","__os_install_post %{nil}",str(spec)])
    p=T/"RPMS/noarch"/(f"{name}-{version}-{release}.noarch.rpm")
    assert p.is_file(),p
    assert not need("verify-empty-"+key,[*rpm,"-qlp",str(p)]).stdout.replace("(contains no files)","").strip()
    for arg in ("provides","obsoletes","requires"):
        need(key+"-"+arg,[*rpm,"-qp","--"+arg,str(p)])
    return p

def controls(key,use_root):
    root=T/("root-"+key)
    root.mkdir()
    db=root/"var/lib/rpm"
    db.mkdir(parents=True)
    cmd=[*rpm,"--macros",macro]
    if use_root:
        cmd += ["--root",str(root),"--dbpath","/var/lib/rpm"]
    else:
        cmd += ["--dbpath",str(db)]
    need("init-"+key,[*cmd,"--initdb"])
    return cmd

def query(key,cmd):
    return need(key,[*cmd,"-qa","--qf","%{NAME}\t%{EPOCHNUM}\t%{VERSION}\t%{RELEASE}\n"]).stdout.splitlines()

def transact(key,cmd,argv,verbose=False):
    return run(key,[*cmd,*(["-vv"] if verbose else []),"-U","--noscripts","--notriggers",
         "--noplugins","--nosignature","--nodigest",*argv])

rows=[]
try:
    clang=make("clang-new","clang","22.1.8","1",header=
        "Requires: llvm = 22.1.8-1\nProvides: clang-analyzer = 22.1.8-1\nObsoletes: clang-analyzer < 22.1.8-1")
    llvm=make("llvm-new","llvm","22.1.8","1",header=
        "Provides: llvm-xray = 22.1.8-1\nObsoletes: llvm-xray < 22.1.8-1\nProvides: llvm-prof-tools = 22.1.8-1\nObsoletes: llvm-prof-tools < 22.1.8-1")
    consumer=make("consumer","needs-clang-analyzer","1","1",header="Requires: clang-analyzer")
    history=json.loads((E/"historical-evr.json").read_text())
    evrs={(h["epoch"],h["version"],h["release"]) for h in history["hits"] if h["name"]=="clang-analyzer"}
    if not evrs:
        evrs={("0","22.1.8","0"),("0","22.1.8","2")}
    cases=[]
    fallback=not any(h["name"]=="clang-analyzer" for h in history["hits"])
    for i,(epoch,version,release) in enumerate(sorted(evrs)):
        key=f"old-{i}"
        pkg=make(key,"clang-analyzer",version,release,epoch)
        cases.append((key,pkg,{"epoch":epoch,"version":version,"release":release}))
    try:
        cmd=controls("probe",True)
        use_root=transact("root-transaction-probe",cmd,["--test",llvm]).returncode==0
    except RuntimeError:
        # The same empty, script-free fixtures can be tested against a private
        # database when a non-root process cannot initialize a chroot RPM DB.
        use_root=False
    for key,old,evr in cases:
        cmd=controls(key,use_root)
        assert transact(key+"-install",cmd,[old]).returncode==0
        before=query(key+"-before",cmd)
        planned=transact(key+"-upgrade-test",cmd,["--test",llvm,clang],verbose=True)
        after_test=query(key+"-after-test",cmd)
        assert before==after_test
        after=None
        if planned.returncode==0:
            done=transact(key+"-upgrade-disposable-db",cmd,[llvm,clang])
            assert done.returncode==0
            after=query(key+"-after",cmd)
        retained=after is not None and any(x.startswith("clang-analyzer\t") for x in after)
        expected=evr["release"]=="2" if fallback else None
        if expected is None:
            verdict="PASS" if planned.returncode==0 else "FAIL"
        else:
            verdict="PASS" if planned.returncode==0 and retained==expected else "FAIL"
        rows.append({"check":"old-analyzer-upgrade","evr":evr,"test_rc":planned.returncode,
                     "old_package_retained":None if after is None else retained,"status":verdict,
                     "expected_old_package_retained":expected,
                     "before":before,"after_test":after_test,"after":after})
    cmd=controls("consumer",use_root)
    missing=transact("consumer-without-provider",cmd,["--test",consumer],verbose=True)
    p=transact("new-clang-satisfies-consumer",cmd,["--test",llvm,clang,consumer],verbose=True)
    rows.append({"check":"requires-clang-analyzer","rc":p.returncode,"missing_provider_rc":missing.returncode,
                 "status":"PASS" if missing.returncode!=0 and "clang-analyzer" in missing.stderr and p.returncode==0 else "FAIL"})
    cmd=controls("self",use_root)
    installed=transact("new-clang-first-install",cmd,[llvm,clang])
    assert installed.returncode==0
    before=query("self-before",cmd)
    planned=transact("new-clang-self-test",cmd,["--test","--replacepkgs",llvm,clang],verbose=True)
    after=query("self-after",cmd)
    rows.append({"check":"no-self-obsoletion","rc":planned.returncode,
                 "status":"PASS" if planned.returncode==0 and before==after else "FAIL","before":before,"after":after})
    result={"state":"PASS" if all(r.get("status","PASS")=="PASS" for r in rows) else "FAIL",
            "rpm":need("version",[*rpm,"--version"]).stdout.strip(),"used_private_root":use_root,"cases":rows,
            "testsolv":{"state":"SKIPPED","path":history.get("testsolv",[]),"reason":"No retained testsolv executable found"}}
except (OSError,ValueError,AssertionError,RuntimeError) as exc:
    result={"state":"FAIL","reason":str(exc),"cases":rows}
finally:
    (T/"result.json").write_text(json.dumps(result,indent=2)+"\n")
    (T/"commands.json").write_text(json.dumps(argv_records,indent=2)+"\n")
    print(json.dumps(result,indent=2))
raise SystemExit(result["state"]!="PASS")
