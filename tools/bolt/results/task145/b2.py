from pathlib import Path
from datetime import datetime
import configparser,hashlib,importlib.util,json,os,re,shlex,shutil,subprocess,sys,time,traceback

A=Path("/home/linhao/Toolchain/development/llvm-optimize/archive/task144")
W=A.parents[1]
B=W.with_name(W.name+"-bolt")
OLD=W/"archive/task138-n-20261119/orchestration"
joblib=B/"tools/skills/tizen-llvm-offline-profile/scripts"
sys.path[:0]=[str(A),str(joblib),str(OLD)]
import buildsteps as bs
import pkg_audit as pa

G="/usr/bin/git"
GBS="/usr/bin/gbs"
identity=json.loads((A/"candidate.json").read_text())
C2=identity["c2"]
job="B2"
D=Path(sys.argv[1])
workers=int(sys.argv[2])
counts=(workers,workers,1)
S=A/"source-c2"
E=D/"evidence"
E.mkdir()
root=D/"gbs-root/local/BUILD-ROOTS/scratch.x86_64.0"
stage="preparation"
t=time.monotonic()
summary={"status":"STOP","kind":"preparation","start":datetime.now().astimezone().isoformat(timespec="seconds"),
         "commit":C2,"parallel":{"ninja":workers,"compile":workers,"thinlto":workers,"links":1}}
os.environ["NIGHT_SOURCE_SHA"]=C2
os.environ["FINAL_PROJECT"]="toolchain"
os.environ["TASK133_WORKSPACE"]=str(W)
for n in ("tmp","cache"): (D/n).mkdir()
env={**bs.CLEAN_ENV,"TMPDIR":str(D/"tmp"),"XDG_CACHE_HOME":str(D/"cache"),
     "NIGHT_SOURCE_SHA":C2,"FINAL_PROJECT":"toolchain","TASK133_WORKSPACE":str(W)}
bs.CLEAN_ENV=env
pa.I=C2
entry=B/"tools/bolt/rebase-launch-20261111-r6/toolchain/launcher.py"
sys.path.insert(0,str(entry.parent))

def checked(argv, name, cwd=D):
    argv=list(map(str,argv))
    assert argv[0].startswith("/"),argv
    print(shlex.join(argv),flush=True)
    bs.save(E/(name+"-argv.json"),argv)
    log=E/(name+".txt")
    with log.open("wb") as out:
        p=subprocess.run(argv,cwd=cwd,env=env,stdout=out,stderr=subprocess.STDOUT)
    if p.returncode:
        with log.open("rb") as out:
            out.seek(max(0,log.stat().st_size-10000))
            print(out.read().decode(errors="replace"),flush=True)
        raise RuntimeError(f"{name} failed rc={p.returncode}, raw={log}")
def query(argv):
    return subprocess.check_output(list(map(str,argv)),env=env,text=True,stderr=subprocess.PIPE)
def need(value,data):
    if not value: raise RuntimeError(str(data))
def stamp():
    return datetime.now().astimezone().isoformat(timespec="seconds")
def read(p):
    return json.loads(p.read_text())

def prepare_driver():
    path=bs.gbs_config(W)
    cfg=configparser.ConfigParser()
    cfg.read(path)
    drv=D/"gbs-driver/local"
    for key in ("sources","repos"): (drv/key).mkdir(parents=True,exist_ok=True)
    root.parent.mkdir(parents=True)
    (drv/"BUILD-ROOTS").symlink_to(root.parent,target_is_directory=True)
    return cfg

def set_provider_overlay(cfg):
    b1=A/"b1-a1"
    raw=read(b1/"evidence/rpms.json")
    names={"llvm","llvm-devel","llvm-static-devel","libomp","clang","libllvm","compiler-rt","liblldb","lldb","lld","libclang"}
    must={"llvm","llvm-devel","llvm-static-devel","libomp","clang","libllvm","compiler-rt"}
    local={}
    repo=D/"providers"
    repo.mkdir()
    for row in raw:
        p=Path(row["path"])
        if p.name.endswith((".src.rpm",".nosrc.rpm")): continue
        n,v,rel,arch=bs.rpm_meta(p)
        if n not in names or arch!="x86_64": continue
        need(bs.sha(p)==row["sha256"],p)
        os.link(p,repo/p.name)
        local[n]={"path":str(p),"evr":v+"-"+rel,
                  "header":query(["/usr/bin/rpm","-qp","--qf","%{VERSION}-%{RELEASE}\t%{VCS}\t%{SIGMD5}\n",p]).strip()}
    need(must<=set(local),("provider closure",sorted(must-set(local))))
    need(len({local[n]["evr"] for n in must})==1,local)
    checked(["/usr/bin/createrepo_c",repo],"provider-repo")
    cfg["repo.b1_provider"]={"url":repo.as_uri()}
    profile=cfg[cfg["general"]["profile"]]
    profile["repos"]="repo.b1_provider,"+profile["repos"]
    bs.save(E/"local-providers.json",local)
    return local

def verify_installed(providers):
    installed={}
    for n,r in providers.items():
        tag="%{VERSION}-%{RELEASE}\t%{VCS}\t%{SIGMD5}\n"
        command=[*bs.chroot(root,"/usr/bin/rpm","-q","--qf",tag,n)]
        p=subprocess.run(command,env=env,text=True,capture_output=True)
        if n not in ("llvm","llvm-devel","llvm-static-devel","libomp","clang","libllvm","compiler-rt") and p.returncode:
            continue
        actual=p.stdout.strip()
        want=r["header"].split("\t")
        got=actual.split("\t")
        installed[n]={"want":want,"installed":got,"rc":p.returncode,"stderr":p.stderr}
        bs.save(E/"installed-providers.json",installed)
        need(p.returncode==0 and len(want)==len(got)==3 and want[:2]==got[:2] and C2 in got[1] and
             (want[2]=="(none)" or got[2]=="(none)" or want[2]==got[2]),("B1 provider mismatch",n,installed[n]))

def shim():
    target=root/"var/tmp/llvm-task145"
    need(target.parent.resolve().is_relative_to(root.resolve()),target)
    target.mkdir()
    n=target/"ninja"
    n.write_text(f'#!/bin/sh\nprintf "LLVM_145_STANDALONE_NINJA jobs={workers}\\n" >&2\nexec /usr/bin/ninja -j{workers} "$@"\n')
    s=target/"build-shell"
    s.write_text('#!/bin/sh\nexport PATH="/var/tmp/llvm-task145:$PATH"\nexec /bin/sh "$@"\n')
    for p in (s,n): p.chmod(0o755)
    return "_buildshell /var/tmp/llvm-task145/build-shell"

def rpm_log():
    p=root/".build.log"
    target=D/"rpm-build.log"
    if p.is_file():
        shutil.copyfile(p,target)
    else:
        import gzip
        rows=sorted((D/"gbs-driver/local/repos").rglob("log.txt.gz"))
        if rows:
            with gzip.open(rows[-1],"rb") as f,target.open("wb") as out: shutil.copyfileobj(f,out)
        else:
            rows=sorted((D/"gbs-driver/local/repos").rglob("log.txt"))
            if rows: shutil.copyfile(rows[-1],target)
    return target

def compare_tools(rpms):
    logs=bs.log_lines(D,lambda l:any(t in l for t in ("provider Version-Release","LLVM_145_STANDALONE_NINJA","aarch64","x86-64","stddef.h")))
    filtered=[l for l in logs if "provider Version-Release" in l or "LLVM_145_STANDALONE_NINJA" in l
              or re.search(r"\]\s*(aarch64|x86-64)\s+-",l)]
    bs.save(E/"key-lines.json",filtered)
    need(any("consistency check passed" in l for l in filtered),("provider gate",filtered))
    need(any("LLVM_145_STANDALONE_NINJA jobs="+str(workers) in l for l in filtered),("ninja shim",filtered))
    rp=pa.get_versions(p for p in rpms if not p.name.endswith((".src.rpm",".nosrc.rpm")) and bs.rpm_meta(p)[3] in ("noarch","x86_64"))
    payload=D/"installed"
    bs.unpack([rp[("bolt","x86_64")],rp[("bolt-debuginfo","x86_64")]],payload)
    bins={p.name:p for p in (payload/"usr/bin").iterdir()}
    arcs={p.name for p in (payload/"usr/lib64").glob("*.a")}
    need(set(bins)==pa.NEW_TOOLS and arcs==pa.RUNTIMES,(list(bins),sorted(arcs)))
    req=query(["/usr/bin/rpm","-qpR",rp[("bolt","x86_64")]]).splitlines()
    need("libllvm = 22.1.8" in req and not any("compiler-rt" in l for l in req),req)
    files={}
    for n,p in bins.items():
        exe=p.resolve()
        need(exe.is_relative_to(payload) and "GNU_RELRO" in bs.elf(exe,"-l"),("GNU_RELRO",n))
        files[n]={"GNU_RELRO":True,"build_id":pa.validate_debug(exe,payload)}
    caches=sorted((root/"home/abuild/rpmbuild/BUILD").glob("*/bolt-build/CMakeCache.txt"))
    need(len(caches)==1,("standalone build cache",caches))
    build=caches[0].parent
    shutil.copyfile(caches[0],E/"standalone-CMakeCache.txt")
    bs.save(E/"bolt-package.json",{"bins":files,"archives":sorted(arcs),"requires":req})
    binary=build/"bin/llvm-bolt"
    need(re.search(r"(?m)^LLVM_LINK_LLVM_DYLIB:[^=]+=ON$", (build/"CMakeCache.txt").read_text()),"standalone LLVM dylib cache disabled")
    need(re.search(r"NEEDED.*libLLVM\.so",bs.elf(binary,"-d")),"standalone missing libLLVM.so")
    mirror=list(build.rglob("X86BoltMnemonicTables.cpp.o"))
    need(len(mirror)==1 and mirror[0].stat().st_size,("standalone X86 mirror object",mirror))
    caches=sorted(build.glob("**/bolt_rt-bins/CMakeCache.txt"))
    need(len(caches)==1,("standalone runtime cache",caches))
    shutil.copyfile(caches[0],E/"runtime-CMakeCache.txt")
    cache=caches[0].read_text()
    flags=[l for l in cache.splitlines() if re.match(r"^CMAKE_(C|CXX)_FLAGS:[^=]+=",l)]
    need(len(flags)==2 and all(s.endswith("=") for s in flags),("runtime flags",flags))
    version=query([*bs.chroot(root,"/"+str(binary.relative_to(root)),"--version")])
    (E/"llvm-bolt-version.txt").write_text(version)
    targets=["x86-64","aarch64"]
    need(all(re.search(rf"(?m)^\s+{n}\s+-",version) for n in targets),version)
    sys.path.insert(0,str(W/"archive/task142"))
    from common import runtime,smoke
    result=smoke(E,runtime(payload/"usr/bin/llvm-bolt",root),["x86_64","aarch64"])
    summary["audit"]={"files":files,"archives":sorted(arcs),"requires":req,"targets":targets,
                      "smoke":result,"runtime_flags":flags,"mirror":str(mirror[0]),"dylib":True}

try:
    # Step 82 gates known historical templates and the working-tree identity.
    ls=importlib.util.spec_from_file_location("task144_entry82",entry)
    lr=importlib.util.module_from_spec(ls)
    ls.loader.exec_module(lr)
    lr.SOURCE=S
    need(lr.check_source()["tree"]==identity["tree"],"source tree mismatch")
    lr.materialize(D,{"prep_unit":"llvm-opt-task145-"+job.lower(),"build_unit":"llvm-opt-task145-"+job.lower()+".service"})
    spec="llvm-tools-subpkgs.spec"
    cfg=prepare_driver()
    rows=read(D/"export-command.json")
    rows[0]=GBS
    rows[rows.index("--spec")+1]=spec
    checked(rows,"export",S)
    export=D/"export"
    need((export/spec).is_file(),"GBS native export missing spec")
    title="llvm-tools-subpkgs"
    dest=D/"gbs-driver/local/sources/tizen_base_toolchain_standard"/(title+"-22.1.8-1")
    dest.parent.mkdir()
    shutil.copytree(export,dest)
    providers=set_provider_overlay(cfg)
    profile=cfg[cfg["general"]["profile"]]
    repos=[cfg[k.strip()]["url"] for k in profile["repos"].split(",")]
    cfg["general"]["buildroot"]=str(D/"gbs-driver")
    cfg["general"]["tmpdir"]=str(D/"tmp")
    newconf=D/"gbs.conf"
    with newconf.open("w") as f: cfg.write(f)
    prep=["/usr/bin/sudo","-n","/usr/bin/build","--uid","1000:1000","--root",root,"--dist",profile["buildconf"],
          "--arch","x86_64","--target","x86_64-tizen-linux","--stage=-bp","--debug","--baselibs",*bs.macros(workers)]
    for url in repos: prep+=["--repo",url]
    checked([*prep,export/spec],"prep")
    if providers:
        verify_installed(providers)
    bs.settle_root(root)
    build_shell=shim()
    buildargs=[GBS,"-c",newconf,"build","-A","x86_64","-B",D/"gbs-driver","-c",C2,"--threads="+str(workers),
               *bs.macros(workers,[build_shell]),"--baselibs","--style=tar","--spec",spec,S]
    stage="product"
    print(stamp(),"GBS_START",job,"workers",workers,flush=True)
    checked(buildargs,"gbs",S)
    summary["gbs_exit"]=0
    log=rpm_log()
    need(log.is_file(),"missing RPM build log")
    rpms=sorted(p for p in (D/"gbs-driver/local/repos").rglob("*.rpm") if p.is_file())
    need(rpms,"GBS success produced no RPMs")
    bs.save(E/"rpms.json",[bs.receipt(p) for p in rpms])
    verify_installed(providers)
    compare_tools(rpms)
    summary["status"]="PASS"
except BaseException as e:
    summary.update(kind=stage,error=str(e))
    (E/"STOP.txt").write_text(traceback.format_exc())
    traceback.print_exc()
finally:
    try:
        rpm_log()
        if root.is_dir():
            bs.settle_root(root)
            target=root/bs.INNER.lstrip("/")
            if target.is_dir():
                summary["retained_build_tree"]=str(target)
    except BaseException as e:
        summary["status"]="STOP"
        summary["cleanup_error"]=str(e)
        (E/"cleanup-STOP.txt").write_text(traceback.format_exc())
        traceback.print_exc()
    summary["end"]=stamp()
    summary["seconds"]=round(time.monotonic()-t,2)
    bs.save(D/"result.json",summary)
sys.exit(summary["status"]!="PASS")
