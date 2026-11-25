import json, os
from pathlib import Path
a=Path(__file__).resolve().parent
w=a.parents[1]
t=w/"temp"
roots=[w/"tools/bench_inputs",t/"tu-inputs-restored-20261106",t/"bench_results/pilot_sources"]
roots+=sorted(p for p in t.iterdir() if not p.is_symlink() and p.is_dir()
              and p.name.startswith(("baseline-","bolt-holdout-","bolt-final-",
                 "bolt-aarch64-","bolt-on-hybrid-","tu-dwarf-","perf-","pgo-resource-")))
roots=[p for p in roots if p.is_dir() and not p.is_symlink()]
out=[]
errors=[]
skip={".git","BUILDROOT","BUILD-ROOTS","BUILD","node_modules","CMakeFiles","objects","__pycache__",
      "deleted-repo-backup-20261105","foreign-artifacts","debugsource","thinlto-cache","members","source","sources","llvm-project","compile-logs","bench_results","payload","usr","rootfs","tests","fixtures","helper-tests","installed","optimized","instrument","profile-work","collection","toolchains","runtime-libs"}
for root in roots:
    for path,dirs,files in os.walk(root,followlinks=False,onerror=lambda e:errors.append(str(e))):
        here=Path(path)
        git_root=".git" in dirs or ".git" in files
        dirs[:]=[n for n in dirs if n not in skip and "llvm_autofdo_bolt_agent" not in n
                 and not n.endswith((".a",".rpm","-census","-raw","-unpacked","-proof","-tests","-cache")) and not n.startswith(("source-","cmake-","ps5-helper-"))]
        if git_root or ({"llvm","clang","compiler-rt"} <= set(dirs)):
            dirs[:]=[]
        for name in files:
            if Path(name).suffix in (".i",".ii"):
                candidate=here/name
                if not candidate.is_symlink() and candidate.is_file():
                    out.append(str(candidate))
(a/"evidence/input-discovery.json").write_text(json.dumps({"roots":list(map(str,roots)),
   "pruned":sorted(skip),"candidates":sorted(out),"errors":errors},indent=2)+"\n")
print(len(out),"candidate paths")
