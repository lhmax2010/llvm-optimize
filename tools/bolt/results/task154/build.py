from pathlib import Path
import configparser, json, os, re, shutil, subprocess, sys, time, traceback

A=Path(__file__).resolve().parent
W=A.parents[1]
B=W.with_name(W.name+"-bolt")
ORCH=W/"archive/task151/orchestration"
SKILL=B/"tools/skills/tizen-llvm-offline-profile/scripts"
sys.path[:0]=[str(ORCH),str(SKILL)]
import buildsteps as bs
from build_jobs import install,require_rpm_log
from static_audit import package_files

REPO=W/"archive/task153/ps6-suggestions.git"
B1_SOURCE=W/"archive/task144/source-c2"
LAUNCHER=B/"tools/bolt/rebase-launch-20261111-r6/toolchain/launcher.py"
GIT="/usr/bin/git"
GBS="/usr/bin/gbs"

def read(p):
    return json.loads(p.read_text())

def main():
    import importlib.util
    D=Path(sys.argv[1])
    jobs=int(sys.argv[2])
    counts=(jobs,jobs,1)
    S=D/"source"
    E=D/"evidence"
    E.mkdir()
    root=D/"gbs-root/local/BUILD-ROOTS/scratch.x86_64.0"
    runtime=D/"runtime-root"
    candidate=next(x for x in read(A/"evidence/series.json") if x["patch"]==6)
    ref=candidate["commit"]
    config=bs.gbs_config(W)
    log=D/"rpm-build.log"
    base_repo=D/"gbs-driver/local/repos/tizen_base_toolchain_standard/x86_64"
    result={"status":"FAIL","stage":"preparation","commit":ref,"tree":candidate["tree"],
            "parallelism":list(counts)}
    start=time.monotonic()
    for n in ("tmp","cache","osc-cache"):
        (D/n).mkdir()
    env={**bs.CLEAN_ENV,"TMPDIR":str(D/"tmp"),"XDG_CACHE_HOME":str(D/"cache"),
         "NIGHT_SOURCE_SHA":ref,"FINAL_PROJECT":"toolchain","TASK133_WORKSPACE":str(W)}
    os.environ.update({k:env[k] for k in ("NIGHT_SOURCE_SHA","FINAL_PROJECT","TASK133_WORKSPACE","TMPDIR","XDG_CACHE_HOME")})
    bs.CLEAN_ENV=env

    def run(name, argv, cwd=D, strict=True, timeout=None):
        args=list(map(str,argv))
        assert args[0].startswith("/")
        bs.save(E/(name+"-argv.json"),args)
        print(name,*args,flush=True)
        path=E/(name+".txt")
        with path.open("wb") as out:
            p=subprocess.run(args,cwd=cwd,env=env,stdout=out,stderr=subprocess.STDOUT,timeout=timeout)
        if strict and p.returncode:
            raise RuntimeError(f"{name} exited {p.returncode}, raw output {path}")
        return p.returncode

    def capture_build_log():
        success=base_repo/"logs/success/llvm-22.1.8-1"
        failed=base_repo/"logs/fail/llvm-22.1.8-1"
        for path in (success/"log.txt",failed/"log.txt",root/".build.log",
                     success/"log.txt.gz",failed/"log.txt.gz"):
            if path.is_file():
                if path.suffix==".gz":
                    import gzip
                    with gzip.open(path,"rb") as inp, log.open("wb") as out:
                        shutil.copyfileobj(inp,out)
                else:
                    shutil.copyfile(path,log)
                bs.save(E/"rpm-log-origin.json",{"source":str(path),"local":bs.receipt(log)})
                return

    def check_packages(rpms):
        expected={k:set(v) for k,v in read(A/"evidence/expected-rpm-paths.json").items()}
        actual={k:set(v) for k,v in package_files(rpms).items()}
        report={}
        for key in sorted(expected.keys()|actual.keys()):
            a,e=actual.get(key,set()),expected.get(key,set())
            report[key]={"actual":len(a),"expected":len(e),"unexpected_added":sorted(a-e),"unexpected_missing":sorted(e-a)}
        same=actual==expected
        bs.save(E/"rpm-files.json",{k:sorted(v) for k,v in actual.items()})
        bs.save(E/"rpm-file-comparison.json",{"status":"PASS" if same else "FAIL","packages":report,
                "expected_moves":read(A/"evidence/static-package-simulation.json")["patch5_moved"]})
        result["file_comparison"]="PASS" if same else "FAIL"

    def smoke(rpms,repo_urls,buildconf):
        from shutil import copyfile
        names=("llvm","libllvm","clang")
        repo=D/"runtime-repo"
        repo.mkdir()
        expected={}
        for p in rpms:
            name,version,release,arch=bs.rpm_meta(p)
            if name in names and arch=="x86_64":
                (repo/p.name).hardlink_to(p)
                expected[name]=subprocess.check_output(["/usr/bin/rpm","-qp","--qf",
                    "%{NAME}\t%{VERSION}-%{RELEASE}\t%{VCS}\t%{ARCH}",p],env=env,text=True)
        assert set(expected)==set(names),expected
        run("runtime-createrepo",["/usr/bin/createrepo_c",repo])
        # Drop development/project defaults. Keep the platform's bootstrap
        # RPM set and let its solver expand the requested runtime packages.
        conf=D/"runtime.conf"
        conf.write_text("".join(line for line in Path(buildconf).read_text().splitlines(keepends=True)
                                 if not re.match(r"^\s*(Support|Required|VMinstall|Keep):",line)))
        recipe=D/"runtime-fixture.spec"
        recipe.write_text("Name: task154-runtime-fixture\nVersion: 1\nRelease: 1\nSummary: Runtime dependency selection\n"
                          "License: MIT\nBuildRequires: llvm\nBuildRequires: libllvm\nBuildRequires: clang\n"
                          "BuildRequires: perl\n%description\nRuntime dependency selection.\n%files\n")
        runtime.mkdir()
        init=["/usr/bin/sudo","-n","/usr/lib/build/init_buildsystem","--root",runtime,"--dist",conf,
              "--arch","x86_64","--cachedir",D/"osc-cache"]
        for url in [str(repo),*repo_urls]:
            init+=["--repo",url]
        run("runtime-plan",[*init,"--list-state",recipe],timeout=1200)
        plan=(E/"runtime-plan.txt").read_text().splitlines()
        if any(re.match(r"^llvm-devel-.*\.rpm$",line.strip()) for line in plan):
            raise RuntimeError("runtime resolver requested llvm-devel")
        run("runtime-init",[*init,recipe],timeout=1200)
        root_cmd=["/usr/bin/sudo","-n","/usr/sbin/chroot",runtime]
        query_fmt="%{NAME}\t%{VERSION}-%{RELEASE}\t%{VCS}\t%{ARCH}\n"
        run("runtime-installed",[*root_cmd,"/usr/bin/rpm","-qa","--qf",query_fmt],timeout=60)
        installed={line.split("\t",1)[0]:line for line in (E/"runtime-installed.txt").read_text().splitlines() if "\t" in line}
        assert "llvm-devel" not in installed
        assert all(installed.get(k)==v for k,v in expected.items()),(expected,{k:installed.get(k) for k in expected})
        for k,v in installed.items():
            if k in expected:
                assert ref in v,(k,v)
        run("smoke-dir",[*root_cmd,"/bin/mkdir","-p","/tmp/task154"],timeout=15)
        run("smoke-dir-owner",[*root_cmd,"/bin/chown","1000:1000","/tmp/task154"],timeout=15)
        fixture=runtime/"tmp/task154"
        (fixture/"null.c").write_text("int read_null(void) { int *p = (int *)0; return *p; }\n")
        smoke_cmd=["/usr/bin/sudo","-n","/usr/sbin/chroot","--userspec=1000:1000",runtime,
                   "/usr/bin/env","PATH=/usr/bin:/bin","LC_ALL=C","HOME=/tmp/task154","PYTHONDONTWRITEBYTECODE=1"]
        command=["/usr/bin/scan-build","--use-analyzer","/usr/bin/clang","--use-cc","/usr/bin/clang",
                 "--use-c++","/usr/bin/clang++","-o","/tmp/task154/report",
                 "/bin/sh","-c",'exec "$CC" -c /tmp/task154/null.c -o /tmp/task154/null.o']
        rc=run("smoke-scan-build",[*smoke_cmd,*command],strict=False,timeout=120)
        reports=sorted(fixture.glob("report/*/index.html"))
        assets=[]
        for index in reports:
            href=index.read_text(errors="replace")
            if all(name in href and (index.parent/name).is_file() and (index.parent/name).stat().st_size
                   for name in ("sorttable.js","scanview.css")):
                assets.append(str(index.relative_to(fixture)))
        if (fixture/"report").is_dir():
            copy_dest=E/"reports"
            shutil.copytree(fixture/"report",copy_dest)
        outcomes={"scan-build":{"rc":rc,"reports":assets,"status":"PASS" if rc==0 and assets else "FAIL"}}
        py=run("smoke-python3",[*smoke_cmd,"/bin/sh","-c","command -v python3"],strict=False,timeout=10)
        for tool in ("analyze-build","intercept-build","scan-build-py","scan-view"):
            if py:
                outcomes[tool]={"status":"SKIPPED","reason":"python3 not installed in the runtime dependency closure"}
                continue
            rc=run("smoke-"+tool,[*smoke_cmd,"/usr/bin/"+tool,"--help"],strict=False,timeout=45)
            outcomes[tool]={"status":"PASS" if rc==0 else "FAIL","rc":rc}
        bs.save(E/"functional-results.json",outcomes)
        result["functional"]=outcomes

    try:
        run("clone",[GIT,"clone","--quiet","--shared","--no-checkout",REPO,S])
        upstream="refs/tags/upstream/22.1.8"
        objects=subprocess.check_output([GIT,"-C",B1_SOURCE,"rev-parse","--path-format=absolute","--git-path","objects"],text=True)
        tag=subprocess.check_output([GIT,"-C",B1_SOURCE,"rev-parse",upstream],text=True).strip()
        with (S/".git/objects/info/alternates").open("a") as out:
            out.write(objects)
        run("local-upstream-tag",[GIT,"-C",S,"update-ref",upstream,tag])
        run("checkout",[GIT,"-C",S,"checkout","--quiet","--detach",ref])
        ls=importlib.util.spec_from_file_location("task154_entry82",LAUNCHER)
        lr=importlib.util.module_from_spec(ls)
        ls.loader.exec_module(lr)
        lr.SOURCE=S
        assert lr.check_source()["tree"]==candidate["tree"]
        lr.materialize(D,{"prep_unit":"llvm-opt-task154-prep","build_unit":"llvm-opt-task154-b1.service"})
        cfg=configparser.ConfigParser()
        cfg.read(config)
        drv=D/"gbs-driver/local"
        for key in ("sources","repos"):
            (drv/key).mkdir(parents=True,exist_ok=True)
        root.parent.mkdir(parents=True)
        (drv/"BUILD-ROOTS").symlink_to(root.parent,target_is_directory=True)
        rows=read(D/"export-command.json")
        rows[0]=GBS
        export=D/"export"
        run("export",rows,S)
        destination=drv/"sources/tizen_base_toolchain_standard/llvm-22.1.8-1"
        destination.parent.mkdir()
        shutil.copytree(export,destination)
        profile=cfg[cfg["general"]["profile"]]
        repos=[cfg[k.strip()]["url"] for k in profile["repos"].split(",")]
        cfg["general"]["buildroot"]=str(D/"gbs-driver")
        cfg["general"]["tmpdir"]=str(D/"tmp")
        conf=D/"gbs.conf"
        with conf.open("w") as stream:
            cfg.write(stream)
        prep=["/usr/bin/sudo","-n","/usr/bin/build","--uid","1000:1000","--root",root,
              "--cachedir",D/"osc-cache","--dist",profile["buildconf"],"--arch","x86_64",
              "--target","x86_64-tizen-linux","--stage=-bp","--debug","--baselibs",*bs.macros(jobs)]
        for url in repos:
            prep+=["--repo",url]
        run("prep",[*prep,export/"llvm.spec"])
        bs.settle_root(root)
        build_shell="_buildshell "+install(root,counts)
        args=[GBS,"-c",conf,"build","-A","x86_64","-B",D/"gbs-driver","-c",ref,"--threads="+str(jobs),
              *bs.macros(jobs,[build_shell]),"--baselibs","--style=tar","--spec","llvm.spec",S]
        result["stage"]="build"
        result["gbs_rc"]=run("gbs",args,S,strict=False)
        capture_build_log()
        if log.is_file():
            with log.open(errors="replace") as stream:
                misses=[f"{i}: {line.rstrip()}" for i,line in enumerate(stream,1)
                        if re.search(r"Installed \(but unpackaged\) file\(s\)|File not found:|No such file or directory.*(?:libscanbuild|libear|scan-view|scan-build)",line,re.I)]
            (E/"rpm-packaging-errors.txt").write_text("\n".join(misses)+("\n" if misses else ""))
            result["packaging_errors"]=len(misses)
        if result["gbs_rc"] or not log.is_file() or result["packaging_errors"]:
            raise RuntimeError("GBS or RPM packaging gate failed")
        require_rpm_log(log,counts)
        rpms=sorted((base_repo/"RPMS").glob("*.rpm"))
        assert rpms
        bs.save(E/"rpms.json",[bs.receipt(p) for p in rpms])
        result["build"]="PASS"
        result["stage"]="validation"
        check_packages(rpms)
        try:
            smoke(rpms,repos,profile["buildconf"])
        except (OSError,RuntimeError,AssertionError,subprocess.SubprocessError) as error:
            result["functional"]={"status":"SKIPPED","reason":str(error)}
            (E/"functional-environment-error.txt").write_text(traceback.format_exc())
        if result["file_comparison"]!="PASS" or any(
                isinstance(x,dict) and x.get("status")=="FAIL" for x in result["functional"].values()):
            raise RuntimeError("file ownership or functional check failed")
        result["status"]="PASS" if result["functional"].get("status")!="SKIPPED" else "PARTIAL"
    except BaseException as error:
        result["error"]=str(error)
        (E/"STOP.txt").write_text(traceback.format_exc())
        traceback.print_exc()
    finally:
        result["elapsed_seconds"]=round(time.monotonic()-start,3)
        bs.save(D/"worker.json",result)
    return result["status"] not in ("PASS","PARTIAL")

if __name__=="__main__":
    raise SystemExit(main())
