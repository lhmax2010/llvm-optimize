from pathlib import Path
import bz2,gzip,hashlib,json,lzma,os,re,shutil,subprocess
import xml.etree.ElementTree as ET
A=Path("/home/linhao/Toolchain/development/llvm-optimize/archive/task153")
W=A.parents[1]
E=A/"evidence"
names={"llvm-xray","llvm-prof-tools","clang-analyzer"}
rpm_pattern=re.compile(r"^(?:llvm-xray|llvm-prof-tools|clang-analyzer)-.+\.rpm$")
primary_pattern=re.compile(r"^(?:[0-9a-f]+-)?primary\.xml(?:\.(?:gz|bz2|xz|zst))?$")
pruned={".git",".svn","__pycache__","BUILD","BUILDROOT","proc","sys","dev","node_modules",
        "source","source-c2","sources","packages-unpacked","payload","build","CMakeFiles","installed",
        "thinlto-cache","ThinLTOCache","worktree","usr","home","bench_results",
        "deleted-repo-backup-20261105","foreign-artifacts","sources-old","collect","raw","training",
        "objects","compare","compare-root","source-audit","payloads","unpack","extract"}
# Build/download roots and saved repositories. Independently import the exact
# primary files retained in the prior B1/B2 dependency audit.
selected_prefixes=("qb-","snapshot","rebase-","night-","toolchain-","baseline-","keep-baselines","final-20261103",
                   "local-full-","buildconf-","build-config-","oldtext-final-","hybrid-validation-")
archive_names={"task133-n-20261118","task138-n-20261119","task142","task144","task145","task148","task149-run","task150"}
roots=[p for prefix in ("temp","archive") for p in (W/prefix).iterdir()
       if not p.is_symlink() and p.is_dir() and
       (p.name.startswith(selected_prefixes) if prefix=="temp" else p.name in archive_names)]
prior=W.with_name(W.name+"-bolt")/"tools/bolt/results/task152/dependency-scan.json"
saved=json.loads(prior.read_text()) if prior.is_file() else {}
prior_dirs=[Path(row["directory"]) for row in saved.get("search_roots",[]) if row["exists"]]
# The static rpm tool is in a retained build root. Probe its bin directory and
# those of the 144/145 roots without walking system trees.
binroots=[W/"temp/rebase-359934-20261111-r6/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/bin"]
for stage in (W/"archive/task144/b1-a1",W/"archive/task145/b2-corrected-a1"):
    binroots.extend(p/"usr/bin" for p in stage.glob("gbs-root/local/BUILD-ROOTS/*") if p.is_dir())
testsolv=[str(p/"testsolv") for p in binroots if (p/"testsolv").is_file()]
errors=[]
repodata=[]
rpms=[]
def scoped(p):
    return p.resolve().is_relative_to(W)
for d in prior_dirs:
    if not d.is_symlink() and scoped(d):
        repodata.extend(p for p in d.glob("repodata/*") if primary_pattern.fullmatch(p.name) and scoped(p))
for root in sorted(roots, key=lambda p:(not p.name.startswith(("qb-","task144","task145","snapshot")), p)):
    print("Scanning",root,flush=True)
    for directory,dirs,files in os.walk(root,followlinks=False,onerror=lambda e:errors.append(str(e))):
        where=Path(directory)
        if ".git" in dirs or ".git" in files or len(where.relative_to(root).parts)>=12:
            dirs[:]=[]
        elif where.name.startswith("scratch."):
            dirs[:]=[n for n in dirs if n in ("var","srv","RPMS")]
        elif where.parent.name.startswith("scratch.") and where.name=="var":
            dirs[:]=[n for n in dirs if n=="cache"]
        else:
            dirs[:]=[n for n in dirs if n not in pruned and not n.endswith((".a",".rpm","-census","-raw","-unpacked","-unpack","-proof","-proofs")) and not n.startswith(("llvm_autofdo_bolt_agent","source-","cmake-","install-","calibration-"))]
        if where.name.startswith("scratch.") and (where/"usr/bin/testsolv").is_file():
            testsolv.append(str(where/"usr/bin/testsolv"))
        for n in files:
            p=where/n
            if n=="testsolv" and scoped(p): testsolv.append(str(p))
            if primary_pattern.fullmatch(n) and scoped(p): repodata.append(p)
            if rpm_pattern.fullmatch(n) and scoped(p): rpms.append(p)
receipt={}
hits=[]
def hash_file(p):
    with p.open("rb") as s:return hashlib.file_digest(s,"sha256").hexdigest()
for p in sorted(set(repodata)):
 try:
    digest=hash_file(p)
    if digest in receipt:
        receipt[digest]["paths"].append(str(p))
        continue
    encoding={".gz":gzip.open,".bz2":bz2.open,".xz":lzma.open}
    if p.suffix==".zst":
        spool=subprocess.check_output(["/usr/bin/zstd","-d","-c",str(p)])
        import io
        stream=io.BytesIO(spool)
    else:
        stream=encoding.get(p.suffix,open)(p,"rb")
    count=0
    with stream:
        for _,node in ET.iterparse(stream,events=("end",)):
            if node.tag.rsplit("}",1)[-1] != "package":continue
            count+=1
            name=node.findtext("{*}name")
            if name in names:
                v=node.find("{*}version").attrib
                era={"epoch":v.get("epoch","0"),"version":v["ver"],"release":v["rel"]}
                hits.append({"source":"primary XML","name":name,"arch":node.findtext("{*}arch"),**era,
                             "primary_sha256":digest,"path":str(p),
                             "package_xml":ET.tostring(node,encoding="unicode")})
            node.clear()
    receipt[digest]={"paths":[str(p)],"records":count}
 except (OSError,ValueError,ET.ParseError,subprocess.CalledProcessError) as exc:
    errors.append(str(p)+": "+str(exc))
for p in sorted(set(rpms)):
 try:
    raw=subprocess.check_output(["/usr/bin/rpm","-qp","--qf","%{NAME}\t%{EPOCHNUM}\t%{VERSION}\t%{RELEASE}\t%{ARCH}\n",str(p)],text=True)
    name,epoch,version,release,arch=raw.strip().split("\t")
    if name in names: hits.append(dict(source="retained RPM",name=name,epoch=epoch,version=version,release=release,
                                       arch=arch,path=str(p),header=raw.strip()))
 except (OSError,ValueError,subprocess.CalledProcessError) as exc:
    errors.append(str(p)+": "+str(exc))
result={"roots":[str(r) for r in sorted(roots)],"task152_repository_directories":[str(r) for r in prior_dirs],"pruned":sorted(pruned),"max_depth_below_root":12,
        "metadata":receipt,"file_candidates":[str(p) for p in sorted(set(rpms))],
        "hits":hits,"testsolv":sorted(set(testsolv)),"errors":sorted(set(errors))}
(E/"historical-evr.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
print(json.dumps({"roots":len(roots),"files":len(repodata),"unique":len(receipt),"hits":[{k:r[k] for k in
                       ("name","epoch","version","release","arch","path")} for r in hits],
                  "testsolv":result["testsolv"],"errors":len(errors)},indent=2))
