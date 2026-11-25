from pathlib import Path
import difflib, json, os, re, shlex, shutil, subprocess, sys
from buildsteps import (
 GIT,GBS,PY,PS5,T_ROOT,checked,sha,receipt,save,read,prepare_source,
 gbs_config,export,macros,prep,run_gbs,settle_root,delete_intermediate,
 chroot,rpm_meta,unpack,log_lines,INNER,
)

R=(Path(__file__).resolve().parent.parent/"recipe.sha").read_text().strip()
WORK="temp/task134-offline-profile"
SKILL="tools/skills/tizen-llvm-offline-profile/scripts"
BUILD_DIR=INNER+"/llvm-22.1.8/build"
BOOTSTRAP_REL="temp/night-20261105/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0"+BUILD_DIR+"/lib64/clang/22/lib/linux/libclang_rt.profile-x86_64.a"
G_STAGES=("instrumented-build","ir-train","merge-profdata","pgo-build","bolt-tools-relink","bolt-instrument-train-merge","bolt-match","write-manifest")

def scratch(d):
 return d/"gbs-root/local/BUILD-ROOTS/scratch.x86_64.0"
def setup(a,w,b):
 d=a/"G-config"
 d.mkdir()
 old=w/WORK/"local-config.json"
 shutil.copyfile(old,d/"134-local-config.original.json")
 s=read(old)
 assert s["source_commit"]==R and s["project"]=="T" and s["snapshot"]=="tizen-base-toolchain_20261030.061318",s
 rows=read(Path(s["training"]))
 verified={x["sha256"]:Path(x["source"]) for x in read(w/"archive/server-kit-136/verified-inputs.json")}
 for row in rows:
  p=Path(row["file"])
  if not p.is_file(): p=verified[row["sha256"]]
  if p.stat().st_size!=row["bytes"] or sha(p)!=row["sha256"]:
   raise RuntimeError("training input identity mismatch: "+row["name"])
  row["file"]=str(p)
 save(d/"training.json",rows)
 s["training"]=str(d/"training.json")
 ir=a/"G1"
 pg=a/"G4"
 pgr=scratch(pg)
 ir_root=scratch(ir)
 ir_asset=d/"ir-artifacts"
 bt_asset=d/"bolt-artifacts"
 s["paths"].update(gbs_config=str(gbs_config(w)),instrumented_source=str(ir/"source"),
                   instrumented_root=str(ir/"gbs-root"),pgo_source=str(pg/"source"),
                   pgo_root=str(pg/"gbs-root"),pgo_build=str(pgr/BUILD_DIR.lstrip("/")),
                   package_root=str(pg/"shipping-payload"))
 s["tools"].update(instrumented_clang=str(ir_asset/"clang-22"),llvm_bolt=str(bt_asset/"llvm-bolt"),
                   merge_fdata=str(bt_asset/"merge-fdata"),readelf=str(w/T_ROOT/"usr/bin/llvm-readelf"))
 s["profile_path_in_build"]=BUILD_DIR+"/pgo-profiles/clang.profdata"
 s["ninja_roots"]=["{pgo_build}"]
 s["bolt_runtime"]=str(bt_asset/"libbolt_rt_instr.a")
 s["environment"]={}
 platform=w/T_ROOT
 s["tool_environment"]={}
 for tool,value in s["tools"].items():
  if tool=="git": continue
  base=ir_root if tool=="instrumented_clang" else pgr if tool in ("llvm_bolt","merge_fdata") else platform
  dirs=[base/"usr/lib64",base/"lib64"]
  if tool=="instrumented_clang": dirs.insert(0,ir_asset/"lib64")
  s["tool_environment"][tool]={"LD_LIBRARY_PATH":":".join(map(str,dirs))}
 s["tool_environment"]["bolt-instrumented-clang"]=s["tool_environment"]["instrumented_clang"]
 s["tool_launchers"]={"instrumented_clang":{
   "loader":str(ir_root/"usr/lib64/ld-linux-x86-64.so.2"),
   "library_path":s["tool_environment"]["instrumented_clang"]["LD_LIBRARY_PATH"].split(":"),
 }}
 s["tool_launchers"]["llvm_profdata"] = {
   "loader":str(platform/"usr/lib64/ld-linux-x86-64.so.2"),
   "library_path":s["tool_environment"]["llvm_profdata"]["LD_LIBRARY_PATH"].split(":"),
 }
 s["training_extra_args"]={"ir":["-fintegrated-cc1"]}
 for stage in ("instrumented-build","pgo-build","bolt-tools","relink-strip-debug"):
  s["commands"][stage]=[{"argv":[PY,"-B",str(Path(__file__).resolve()),"adapter",str(a),stage],"cwd":str(d)}]
 # Actual spool resources are set by the systemd scheduler. Keep the checkpoint
 # description stable across stages and any per-stage tier changes.
 s["resources"].update(stage_admission=True,tier="managed",tiers={"managed":{"admission_memory_bytes":7*2**30,"admission_disk_bytes":16*2**30,
             "memory_max_bytes":0,"jobs":6}},stop_memory_bytes=3*2**30,stop_disk_bytes=15*2**30,defer_seconds=0,
             max_seconds=86400,lock_path=str(d/"generation.lock"))
 for key in ("sysroot_armv7l","sysroot_aarch64","resource_dir"):
  assert Path(s["paths"][key]).is_dir(),(key,s["paths"][key])
 src=Path(s["paths"]["llvm"])
 assert checked(GIT,"-C",src,"rev-parse","HEAD").strip().decode()==R
 assert not checked(GIT,"-C",src,"status","--porcelain","--untracked-files=no")
 save(d/"config.json",s)
 diff="".join(difflib.unified_diff(old.read_text().splitlines(True),(d/"config.json").read_text().splitlines(True),
                                 str(old),str(d/"config.json")))
 (d/"134-config-to-live.diff").write_text(diff)
 return d/"config.json"
def adapt_instrumented(a,w,b,jobs):
 d=a/"G1"
 source=prepare_source(w,d,R)
 exp=export(w,b,d,source,R,"llvm.spec")
 sp=exp/"llvm.spec"
 raw=sp.read_text()
 marker="cmake " + chr(92) + "\n    -G Ninja " + chr(92) + "\n"
 start,marker_build,body=raw.partition("\n%build\n")
 assert marker_build and body.count(marker)==1
 instrument=marker+"    -DLLVM_BUILD_INSTRUMENTED=IR "+chr(92)+"\n"
 body=body.replace(marker,instrument,1)
 target="# Full build using ninja (already in build/ directory after cd build)"
 assert body.count(target)==1
 body=body.replace(target,f"ninja -j {jobs} clang_rt.profile-x86_64 || exit 1\nninja -j {jobs} clang || exit 1\necho PGO_INSTRUMENTED_BUILD_PASS\nexit 0\n\n"+target,1)
 revised=start+marker_build+body
 sp.write_text(revised)
 (d/"instrumented-recipe.diff").write_text("".join(difflib.unified_diff(raw.splitlines(True),revised.splitlines(True),"R export","instrumented-only recipe")))
 root=prep(w,d,exp,"llvm.spec",jobs,("_without_clang_bolt 1",))
 try:
  settle_root(root)
  boot=w/BOOTSTRAP_REL
  expected=root/"usr/lib64/clang/22/lib/linux/libclang_rt.profile-x86_64.a"
  if not expected.exists():
   grant=root/"home/abuild/133n-bootstrap"
   grant.mkdir()
   src=grant/boot.name
   shutil.copyfile(boot,src)
   assert sha(src)==sha(boot)
   checked(*chroot(root,"/usr/bin/install","-D","-m","0644","/home/abuild/133n-bootstrap/"+boot.name,
                   "/usr/lib64/clang/22/lib/linux/"+boot.name))
  assert expected.is_file()
  save(d/"bootstrap-runtime.json",receipt(expected))
  temp=root/"home/abuild/133n-instrumented.spec"
  shutil.copyfile(sp,temp)
  assert sha(temp)==sha(sp)
  from build_jobs import from_environment, install
  build_shell=install(root,from_environment())
  cmd=[*chroot(root,"/usr/bin/rpmbuild","-bc","--short-circuit",
        "--define","_topdir /home/abuild/rpmbuild","--define","_toolchain clang"),
        *macros(jobs,("_without_clang_bolt 1","_buildshell "+build_shell)),
        "/home/abuild/133n-instrumented.spec"]
  # Use build's configured uid to keep outputs readable and use the same RPM
  # macros that extracted the unchanged R source tree in the previous step.
  cmd[3:3]=["--userspec=1000:1000"]
  print(shlex.join(cmd),flush=True)
  subprocess.run(cmd,check=True)
  gpath=root/BUILD_DIR.lstrip("/")
  out=a/"G-config/ir-artifacts"
  out.mkdir()
  p=gpath/"bin/clang-22"
  shutil.copyfile(p,out/p.name)
  (out/p.name).chmod(0o755)
  assert sha(p)==sha(out/p.name)
  lib=out/"lib64"
  lib.mkdir()
  for src in sorted((gpath/"lib64").glob("*.so*")):
   if src.is_file():
    dest=lib/src.name
    if src.is_symlink():
     dest.symlink_to(os.readlink(src))
    else:
     shutil.copyfile(src,dest)
     assert sha(src)==sha(dest)
  assert "LLVM_BUILD_INSTRUMENTED:STRING=IR" in (gpath/"CMakeCache.txt").read_text()
  shutil.copyfile(gpath/"CMakeCache.txt",d/"CMakeCache.instrumented.txt")
  save(d/"artifacts.json",[receipt(out/p.name),*[receipt(x) for x in lib.iterdir() if x.is_file()]])
 finally:
  settle_root(root)
 delete_intermediate(d,root)
def prepare_pgo_source(a,d,w,b):
 src=prepare_source(w,d,R)
 asset=src/"packaging/clang-pgo.profdata.xz"
 sdir=b/SKILL
 sys.path.insert(0,str(sdir))
 from manifest import pack
 local=d/"offline-assets"
 local.mkdir()
 metadata=pack(a/"G-profiles/clang.profdata",local/asset.name)
 shutil.copyfile(local/asset.name,asset)
 assert sha(asset)==metadata["xz_sha256"]
 manifest=src/"packaging/llvm-profiles.manifest"
 save(manifest,{"format":1,"status":"READY","llvm_version":"22.1.8",
                "provenance":{"purpose":"local generation precursor for a PGO-only build","recipe":R},
                "profiles":[{"project":"T","pgo":True,"bolt":False,"profdata":metadata}]})
 checked(GIT,"-C",src,"add","--",asset,manifest)
 delta=checked(GIT,"-C",src,"diff","--cached","--name-only").decode().splitlines()
 assert delta==["packaging/clang-pgo.profdata.xz","packaging/llvm-profiles.manifest"],delta
 checked(GIT,"-C",src,"-c","user.name=Hao Lin","-c","user.email=hao.lin@samsung.com","commit","-m","Stage locally generated IR profile for offline pairing")
 derived=checked(GIT,"-C",src,"rev-parse","HEAD").decode().strip()
 save(d/"profile-input.json",{"commit":derived,"recipe":R,"changes":delta,"profile":metadata,"manifest":receipt(manifest)})
 exp=export(w,b,d,src,derived,"llvm.spec")
 # Default export parses with PGO disabled. Explicitly carry the two
 # enabled-only Source files beside the spec for the offline build driver.
 for source in (asset,manifest):
  dest=exp/source.name
  if not dest.exists():
   shutil.copyfile(source,dest)
  if sha(dest)!=sha(source):
   raise RuntimeError("exported PGO source identity mismatch: "+str(dest))
 return src,derived,exp

def adapt_pgo(a,w,b,jobs):
 d=a/"G4"
 src,derived,exp=prepare_pgo_source(a,d,w,b)
 extra=("_with_clang_pgo 1","_without_clang_bolt 1")
 root=prep(w,d,exp,"llvm.spec",jobs,extra)
 try:
  settle_root(root)
  rpms=run_gbs(w,d,src,derived,"llvm.spec",jobs,exp,extra)
  lines=log_lines(d,lambda s:any(x in s for x in ("ARCHIVE_MEMBER_RETRY","NATIVE_ARCHIVES_END","PGO_NINJA_CHECK","PGO_MATCH","PGO_RUNTIME_CHECK")))
  save(d/"pgo-evidence.json",lines)
  assert any("NATIVE_ARCHIVES_END" in x and "PASS" in x for x in lines),lines
  checks=[json.loads(x.split("PGO_NINJA_CHECK ",1)[1]) for x in lines
          if re.match(r"^\d+: \[\s*\d+s\] PGO_NINJA_CHECK ",x)]
  assert len(checks)==1 and checks[0]["violation_count"]==0,checks
  save(d/"pgo-configure-gate.json",checks[0])
  regs=[p for p in rpms if rpm_meta(p)[3] in ("x86_64","noarch") and not re.search("debuginfo|debugsource",rpm_meta(p)[0])]
  assert regs
  unpack(regs,d/"shipping-payload")
  assert (d/"shipping-payload/usr/bin/clang-22").is_file()
  p=root/BUILD_DIR.lstrip("/")/"bin/clang-22"
  save(d/"pgo-clang.json",receipt(p))
  shipped=d/"shipping-payload/usr/lib64"
  libs=[p for p in shipped.iterdir()
        if not p.is_symlink() and p.is_file() and
        p.name.startswith(("libLLVM.so","libclang-cpp.so"))]
  save(d/"pgo-shipped-libraries.json",[receipt(p) for p in sorted(libs)])
 finally:
  settle_root(root)
 # The next stage consumes the live Ninja graph, archives and link command.
 # It releases BUILD once the relinked ELF and BOLT tools are checked out.
def inner_exec(root,argv):
 return (*chroot(root,"/usr/bin/env","-i","LC_ALL=C","PATH=/usr/bin:/bin","HOME=/home/abuild",
                 *(key+"="+os.environ[key] for key in ("PROFILE_JOBS","PROFILE_THINLTO_JOBS","PROFILE_LINK_JOBS") if key in os.environ),
                 "/bin/sh","-c","cd \"$1\"; shift; exec \"$@\"","/bin/sh",BUILD_DIR),*map(str,argv))
def adapt_tools(a,w,b,jobs):
 root=scratch(a/"G5")
 g=root/BUILD_DIR.lstrip("/")
 iv=("/usr/bin/sudo","-n","/usr/sbin/chroot","--userspec=1000:1000")
 def call(*argv,**kwargs):
  full=inner_exec(root,argv)
  return checked(*iv,*full[3:],**kwargs)
 d=a/"G5"
 # Capture the clang relink command after applying this stage's pools and backend cap.
 local=root/"home/abuild/133n-bolt"
 local.mkdir()
 scheduler=local/"build_jobs.py"
 shutil.copyfile(b/SKILL/scheduler.name,scheduler)
 args=(PY,"-B","/home/abuild/133n-bolt/build_jobs.py","reconfigure",BUILD_DIR,"/usr/bin/cmake",
       "-S","../llvm","-B",".","-DLLVM_ENABLE_PROJECTS=clang;lldb;clang-tools-extra;lld;compiler-rt;openmp;bolt",
       "-DBOLT_BUILD_TOOLS=ON","-DBOLT_ENABLE_RUNTIME=ON","-DBOLT_INCLUDE_TESTS=OFF","-DBOLT_TARGETS_TO_BUILD=X86")
 call(*args,output=d/"bolt-configure.log")
 line=call("/usr/bin/ninja","-t","commands","-s","bin/clang-22")
 (d/"link.original").write_bytes(line)
 (local/"link.original").write_bytes(line)
 call("/usr/bin/ninja","-j",str(jobs),"llvm-bolt","merge-fdata","bolt_rt",output=d/"bolt-tools.log")
 assets=a/"G-config/bolt-artifacts"
 assets.mkdir()
 for n in ("llvm-bolt","merge-fdata"):
  p=g/"bin"/n
  shutil.copyfile(p,assets/n)
  (assets/n).chmod(0o755)
  assert sha(p)==sha(assets/n)
 runtime=sorted(g.rglob("libbolt_rt_instr.a"))
 assert len(runtime)==1 or all(sha(p)==sha(runtime[0]) for p in runtime),runtime
 shutil.copyfile(runtime[0],assets/"libbolt_rt_instr.a")
 assert sha(runtime[0])==sha(assets/"libbolt_rt_instr.a")
 save(d/"tool-artifacts.json",[receipt(p) for p in assets.iterdir()])
def adapt_link(a,w,b,jobs):
 root=scratch(a/"G5")
 local=root/"home/abuild/133n-bolt"
 base="/home/abuild/133n-bolt/"
 d=a/"G5"
 iv=("/usr/bin/sudo","-n","/usr/sbin/chroot","--userspec=1000:1000")
 def call(*argv,**kwargs):
  full=inner_exec(root,argv)
  return checked(*iv,*full[3:],**kwargs)
 helper="/home/abuild/rpmbuild/SOURCES/clang-bolt-helper.py"
 call(PY,"-B",helper,"replay",base+"link.original",base+"clang-relinked",base+"clang-relinked.d",base+"relink.sh",
      output=d/"relink-plan.log")
 call("/bin/sh",base+"relink.sh",output=d/"relink.log")
 call("/usr/bin/llvm-strip","--strip-debug","-o",base+"clang-with-relocs",base+"clang-relinked")
 dest=a/"G-profiles/clang-with-relocs"
 shutil.copyfile(local/"clang-with-relocs",dest)
 dest.chmod(0o755)
 assert sha(dest)==sha(local/"clang-with-relocs")
 save(d/"relink-artifacts.json",receipt(dest))
 from handoff import retain_runtime
 retain_runtime(a, root, dest)
def generation_log_files(root):
 for p in root.iterdir():
  if p.is_dir() and any(p.name.startswith(x+"-") for x in G_STAGES):
   yield from (f for f in p.iterdir() if f.is_file())
def generate(a,d,w,b,task,tier,jobs,mem,cpu):
 from __main__ import locked
 from datetime import datetime
 idx=int(task[1:])-1
 stage=G_STAGES[idx]
 with locked():
  c=a/"G-config/config.json"
  if idx==0 and not c.exists(): c=setup(a,w,b)
  skill=Path(__file__).with_name("profile_stage.py")
  root=a/"G-profiles"
  args=[PY,"-B",str(skill),"--config",str(c),"--output",str(root),"--stages",stage]
  args += ["--memory-available-bytes",os.environ["TASK133_ADMISSION_MEMORY"]]
  if idx: args += ["--resume"]
  if task=="G2": args += ["--recover-instrumented",str(a/"G-config/recovery-receipt.json")]
  elif not root.exists():
   with (d/"skill-dry-run.json").open("xb") as out:
    subprocess.run([*args,"--dry-run"],check=True,stdout=out)
  env={**os.environ,"TASK133_JOBS":str(jobs)}
  print(shlex.join(args),flush=True)
  proc=subprocess.run(args,env=env)
  if proc.returncode:
   err=read(root/"summary.json") if (root/"summary.json").is_file() else {}
   if err.get("status")=="INTERRUPTED":
    return {"_step_status":"INTERRUPTED","watchdog":err["watchdog"],"reason":err["reason"]}
   raise RuntimeError(f"profile skill exited {proc.returncode}: {err}")
  status=read(root/"summary.json")
  if status["status"]=="SKIPPED":
   return {"_step_status":"SKIPPED","stage":stage,"reason":status["reason"],"admission":status["admission"]}
  check=read(root/(stage+".done.json"))
  assert check["stage"]==stage
  counts=None
  details={}
  if task=="G2":
   profiles=check["artifacts"]
   assert len(profiles)==23 and all(row["bytes"]>0 and row["sha256"]==sha(Path(row["path"])) for row in profiles)
   old=Path(read(a/"G-config/config.json")["paths"]["instrumented_root"]).parent
   archived=Path(w/"archive/task133-n-20261118/G1")
   assert old==archived, (str(old),str(archived))
   root_old=scratch(archived)
   details["G1_cleanup"]=delete_intermediate(d,root_old,build_owner=archived)
  if task=="G8":
   manifest=read(root/"llvm-profiles.manifest")
   return {"stage":stage,"manifest":manifest,"artifacts":check["artifacts"]}
  if task=="G7":
   counts=read(root/"bolt-match.json")
   from weekend import runtime_gate
   details["runtime_dependency_gate"]=runtime_gate(a,b,d)
  if task=="G4":
   details["pgo_clang"]=read(d/"pgo-clang.json")
   details["merged_profdata"]=receipt(root/"clang.profdata")
   details["rpm_identities_file"]=str(d/"rpm-identities.json")
  return {"stage":stage,"artifacts":check["artifacts"],"bolt_match":counts, **details}
if __name__=="__main__":
 _,mode,d,stage=sys.argv
 assert mode=="adapter"
 a=Path(d)
 w=Path(os.environ["TASK133_WORKSPACE"])
 b=w.with_name(w.name+"-bolt")
 sys.path.insert(0,str(b/SKILL))
 actions={"instrumented-build":adapt_instrumented,"pgo-build":adapt_pgo,"bolt-tools":adapt_tools,"relink-strip-debug":adapt_link}
 actions[stage](a,w,b,int(os.environ["TASK133_JOBS"]))
