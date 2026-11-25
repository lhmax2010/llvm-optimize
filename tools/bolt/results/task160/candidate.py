from datetime import datetime
from pathlib import Path
import hashlib, json, os, re, shutil, subprocess, sys
from zoneinfo import ZoneInfo

A=Path(__file__).resolve().parent
W=A.parents[2]
B=W.with_name(W.name+"-bolt")
IR_RUN=W/"archive/task151"
OLD=A.parent/"run"
PROFILES=OLD/"G-profiles"
IR_PROFILES=IR_RUN/"G-profiles"
SRC=W/"temp/task131/pgo-dev"
REPO=W/"archive/task157/llvm.git"
E=A/"evidence"
PS5="7b05a13744d1cf81a5e9cff22a27eb037bf1b6a8"
RECIPE=(A.parent/"recipe.sha").read_text().strip()
PROFILE_SHA="39171c4a5fcb6166ac86d6d47ad16c7890527a73e66c26f035fb910288f496aa"
PROFDATA={"bytes":52_530_416,"sha256":PROFILE_SHA}
REMOTE="ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm"
SPEC="packaging/llvm.spec"
HELPER="packaging/clang-bolt-helper.py"
SKILL=B/"tools/skills/tizen-llvm-offline-profile/scripts"
sys.path.insert(0,str(SKILL))
from manifest import file_identity, pack
ENV={**os.environ,"LC_ALL":"C","GIT_TERMINAL_PROMPT":"0",
     "GIT_SSH_COMMAND":"/usr/bin/ssh -o BatchMode=yes -o ConnectTimeout=20",
     "GIT_AUTHOR_NAME":"Hao Lin","GIT_AUTHOR_EMAIL":"hao.lin@samsung.com",
     "GIT_COMMITTER_NAME":"Hao Lin","GIT_COMMITTER_EMAIL":"hao.lin@samsung.com"}
GIT=["/usr/bin/git","-C",str(REPO)]
TIMEZONE=ZoneInfo("America/Los_Angeles")
R=W/"temp/rebase-359934-20261111-r6/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0"
RPM=[str(R/"usr/lib64/ld-linux-x86-64.so.2"),"--library-path",str(R/"usr/lib64"),str(R/"usr/bin/rpmspec")]
MACROS=B/"tools/bolt/results/fifth-review-20261111/rerun4/parse"
ASCII=r'[^\x00-\x7F]'
STATUS=r'github|lhmax|raw\.githubusercontent|bolt-v4|sandbox|/home/|docs/bolt|tools/bolt|\bmaster\b|\bmain\b|号'
EXTRAS=r'llvm-optimize|(^|[^[:alnum:]_])(ai|codex|claude|cline|openai|chatgpt|copilot)([^[:alnum:]_]|$)|task[[:space:]_-]*[0-9]+|docs/[0-9]+|/var/tmp/'
SIGN="Signed-off-by: Hao Lin <hao.lin@samsung.com>"

def require(p,msg):
    if not p:
        raise RuntimeError(msg)
def read(p):
    return json.loads(p.read_text())
def save(p,data):
    tmp=p.with_suffix(p.suffix+".tmp")
    tmp.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n")
    tmp.replace(p)
def command(args, *, env=ENV, data=None, timeout=180, check=True):
    p=subprocess.run(list(map(str,args)),text=True,input=data,capture_output=True,env=env,timeout=timeout)
    if check and p.returncode:
        raise RuntimeError(f"{args[0]} rc={p.returncode}\n{p.stdout}{p.stderr}")
    return p
def git(*args,env=ENV,data=None):
    return command([*GIT,*args],env=env,data=data).stdout
def show(rev,path):
    return git("show",rev+":"+path)
def replace(s,before,after):
    require(s.count(before)==1,"recipe literal is missing or ambiguous: "+before)
    return s.replace(before,after,1)
def receipt(path):
    return {"path":str(path),**file_identity(path)}
def logged(d,name,argv,*,env=ENV,expect=(0,),timeout=180):
    p=command(argv,env=env,check=False,timeout=timeout)
    (d/(name+".stdout.txt")).write_text(p.stdout)
    (d/(name+".stderr.txt")).write_text(p.stderr)
    save(d/(name+".json"),{"argv":list(map(str,argv)),"rc":p.returncode,
                          "stdout":name+".stdout.txt","stderr":name+".stderr.txt"})
    require(p.returncode in expect,f"{name} rc={p.returncode}\n{p.stdout}{p.stderr}")
    return p

def preflight():
    if not REPO.exists():
        command(["/usr/bin/git","clone","--bare","--shared",SRC,REPO])
    require(git("rev-parse",RECIPE).strip()==RECIPE,"recipe not found")
    git("merge-base","--is-ancestor",PS5,RECIPE)
    revs=git("rev-list","--reverse","--topo-order",PS5+".."+RECIPE).splitlines()
    baseline={"recipe":RECIPE,"tree":git("rev-parse",RECIPE+"^{tree}").strip(),
              "immediate_parent":git("rev-parse",RECIPE+"^").strip(),"ps5":PS5,"ps5_is_ancestor":True,
              "unpublished_recipe_commits":revs}
    save(E/"baseline.json",baseline)
    return baseline

def message_gate(d,revs):
    folder=d/"messages"
    folder.mkdir(exist_ok=True)
    outcomes=[]
    good=True
    for rev in revs:
        path=folder/(rev+".txt")
        path.write_text(git("cat-file","commit",rev).split("\n\n",1)[1])
        for switch,regex,env in (("-nP",ASCII,ENV),("-niE",STATUS,{**ENV,"LC_ALL":"C.UTF-8"}),
                                 ("-niE",EXTRAS,{**ENV,"LC_ALL":"C.UTF-8"})):
            cmd=["/usr/bin/grep",switch,regex,path]
            p=command(cmd,env=env,check=False)
            outcomes.append({"commit":rev,"argv":list(map(str,cmd)),"rc":p.returncode,
                             "stdout":p.stdout,"stderr":p.stderr})
            good &= p.returncode==1 and not p.stdout and not p.stderr
    save(d/"outward-text-gate.json",outcomes)
    require(good,"external text gate STOP; see "+str(d/"outward-text-gate.json"))

def local_commit(parent,d,files,message,change_id=False):
    now=datetime.now(TIMEZONE).isoformat(timespec="seconds")
    env={**ENV,"GIT_AUTHOR_DATE":now,"GIT_COMMITTER_DATE":now}
    def entries(tree):
        rows={}
        for row in git("ls-tree","-z",tree).split("\0"):
            if row:
                info,name=row.split("\t",1)
                rows[name]=info
        return rows
    def make_tree(rows):
        return git("mktree","-z",data="".join(info+"\t"+name+"\0" for name,info in rows.items())).strip()
    package=entries(parent+":packaging")
    for path,source in files.items():
        subdir,name=path.split("/",1)
        require(subdir=="packaging" and Path(name).name==name,"candidate path is outside packaging: "+path)
        if source is None:
            package.pop(name,None)
        else:
            blob=git("hash-object","-w",str(source),env=env).strip()
            package[name]="100644 blob "+blob
    root=entries(parent)
    root["packaging"]="040000 tree "+make_tree(package)
    tree=make_tree(root)
    msg=message.rstrip()+"\n\n"+SIGN+"\n"
    if change_id:
        ident1=git("var","GIT_AUTHOR_IDENT",env=env).strip()
        ident2=git("var","GIT_COMMITTER_IDENT",env=env).strip()
        virtual=f"tree {tree}\nparent {parent}\nauthor {ident1}\ncommitter {ident2}\n\n{msg}"
        change=git("hash-object","-t","commit","--stdin",env=env,data=virtual).strip()
        msg+="Change-Id: I"+change+"\n"
    return git("commit-tree",tree,"-p",parent,env=env,data=msg).strip()

def shared_provenance():
    ir=read(IR_PROFILES/"ir-tools.json")
    source=read(IR_PROFILES/"ir-source-identity.json")
    train_path=Path(read(IR_RUN/"G-config/config.json")["training"])
    rows=[{k:r[k] for k in ("name","target","sha256","bytes")} for r in read(train_path)]
    require(len(rows)==23 and len({r["name"] for r in rows})==23,"training set has unexpected cardinality")
    model=ir["instrumented_clang"]
    tool={k:model[k] for k in ("sha256","bytes")}
    tool["version"]=model["version"].splitlines()[0]
    return {"source_identity":source,"instrumented_clang":tool,"training":rows,
            "training_sha256":hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(",",":")).encode()).hexdigest(),
            "recipe":RECIPE}

def verification_helper(original):
    text=replace(original, "def select_pgo_profile(manifest, project, pgo, bolt):",
                 "def select_pgo_profile(manifest, project, pgo, bolt, *, allow_unqualified=False):")
    text=replace(text, "require(doc['status'] == 'READY', 'profile manifest is not READY (PLACEHOLDER is not usable)')",
                 "require(doc['status'] == 'READY' or (allow_unqualified and doc['status'] == 'UNQUALIFIED'),\n"
                 "            'profile manifest is not READY (PLACEHOLDER is not usable)')")
    return replace(text, "select_pgo_profile(manifest, project, True, bolt_profile is not None)",
                   "select_pgo_profile(manifest, project, True, bolt_profile is not None, allow_unqualified=True)")


def verification_commit(integration,d,assets,message):
    helper=assets/"clang-bolt-helper.py"
    helper.write_text(verification_helper(show(integration,HELPER)))
    return local_commit(integration,d,{SPEC:assets/"llvm.spec",HELPER:helper},
           message+"\n\nExplicitly accept the unqualified manifest for build verification.")


def make_a(d):
    profile=IR_PROFILES/"clang.profdata"
    require(file_identity(profile)==PROFDATA,"G3 profdata does not match authorized size and SHA")
    check=read(IR_PROFILES/"merge-profdata.done.json")
    require(any({k:r[k] for k in ("bytes","sha256")}==PROFDATA for r in check["artifacts"]),"G3 checkpoint identity mismatch")
    assets=d/"assets"
    assets.mkdir()
    asset=assets/"clang-pgo.profdata.xz"
    asset_info=pack(profile,asset)
    manifest=assets/"llvm-profiles.manifest"
    save(manifest,{"format":1,"llvm_version":"22.1.8","status":"UNQUALIFIED",
                   "provenance":shared_provenance(),
                   "profiles":[{"project":"T","pgo":True,"bolt":False,"profdata":asset_info}]})
    # A PGO-only build must not declare the unused placeholder fdata.
    default=assets/"llvm.spec"
    src=show(RECIPE,SPEC)
    src=replace(src,"Source1203: clang-pgo.fdata.xz \\\n","")
    src=replace(src,'%define llvm_pgo_bolt_source --bolt-profile "%{SOURCE1203}"',
               '%define llvm_pgo_bolt_asset Source1203: clang-pgo.fdata.xz\n'
               '%define llvm_pgo_bolt_source --bolt-profile "%{SOURCE1203}"')
    src=replace(src,"%{?llvm_pgo_sources}\n","%{?llvm_pgo_sources}\n%{?llvm_pgo_bolt_asset}\n")
    default.write_text(src)
    integration=local_commit(RECIPE,d,{"packaging/"+p.name:p for p in (asset,manifest,default)},
              "packaging: add a profile for clang PGO\n\n"
              "Include the offline-generated instrumentation profile and its\n"
              "manifest for x86-64 Toolchain builds. Keep PGO off by default.",True)
    s=replace(show(integration,SPEC),"%bcond_with clang_pgo\n","%bcond_without clang_pgo\n")
    s=replace(s,"%bcond_without clang_bolt\n","%bcond_with clang_bolt\n")
    test_spec=assets/"llvm.spec"
    test_spec.write_text(s)
    test=verification_commit(integration,d,assets,
           "packaging: enable clang PGO without BOLT for build verification (test only, not for merge)")
    return integration,test,assets

def make_b(d,a):
    source=PROFILES/"llvm-profiles.manifest"
    body=read(source)
    match=read(PROFILES/"bolt-match.json")
    save(d/"G7-match.json",match)
    require(body.get("status")=="UNQUALIFIED",
            "G8 did not deliver the expected unqualified manifest; original kept unchanged")
    require(body.get("provenance",{}).get("bolt_match")==match,"G8 match identity differs from G7")
    pair=next((w for w in body["profiles"] if w["project"]=="T" and w["pgo"] is True and w["bolt"] is True),None)
    require(pair is not None,"G8 is missing the paired T profile")
    require({k:pair["profdata"][k] for k in PROFDATA}==PROFDATA,"G8 PGO asset differs from G3")
    assets=d/"assets"; assets.mkdir()
    for field in ("profdata","bolt_profile"):
        name=pair[field]["file"]
        require(Path(name).name==name and name.endswith(".xz"),"invalid G8 asset filename")
        shutil.copyfile(PROFILES/name,assets/name)
    manifest=assets/source.name
    shutil.copyfile(source,manifest)
    parent=a["integration"]
    files={"packaging/llvm-profiles.manifest":manifest}
    s=show(parent,SPEC)
    for field,old in (("profdata","clang-pgo.profdata.xz"),("bolt_profile","clang-pgo.fdata.xz")):
        name=pair[field]["file"]
        if name!=old:
            s=replace(s,old,name)
            files["packaging/"+old]=None
        files["packaging/"+name]=assets/name
    old_unpack='python3 -B %{SOURCE1201} unpack %{SOURCE1200} "$BOLT_WORK/profile.fdata" || bolt_status_exit $?'
    s=replace(s,old_unpack,'%if %{llvm_pgo_enabled}\n'
              'cp "$PWD/pgo-profiles/clang.fdata" "$BOLT_WORK/profile.fdata" || bolt_status_exit $?\n'
              '%else\n'+old_unpack+'\n%endif')
    test_spec=assets/"llvm.spec"
    test_spec.write_text(s)
    files[SPEC]=test_spec
    integration=local_commit(parent,d,files,
        "packaging: add the paired profile for clang BOLT\n\n"
        "Ship the profile matched to the PGO build. Use the validated\n"
        "paired profile when both optimizations are enabled.",True)
    test_spec.write_text(replace(s,"%bcond_with clang_pgo\n","%bcond_without clang_pgo\n"))
    test=verification_commit(integration,d,assets,
          "packaging: enable clang PGO with BOLT for build verification (test only, not for merge)")
    return integration,test,assets

def expand(d,name,arch,spec):
    e={**ENV,"RPM_CONFIGDIR":str(R/"usr/lib/rpm")}
    ver=command([*RPM,"--version"],env=e).stdout
    require("4.14.1" in ver,"RPM parser is not the designated version")
    (d/"rpm-version.txt").write_text(ver)
    showrc=command([*RPM,"--showrc"],env=e).stdout
    macro=next(x.split(": ",1)[1] for x in showrc.splitlines() if x.startswith("Macro path:"))
    macro=":".join(p for p in macro.split(":") if p.startswith(str(R)))
    profile="x86-debug" if arch=="x86_64" else arch
    opts=["--macros",macro+":"+str(MACROS/f"toolchain-{profile}.macros"),
          "--target",arch+"-tizen-linux","--define","_toolchain clang",
          "--define","_topdir "+str(d/"rpmdir"),"--define","_sourcedir "+str(spec.parent)]
    return logged(d,f"{name}-{arch}",[*RPM,"-P",*opts,spec],env=e).stdout

def build_flags_probe(d,unpacked,test):
    cmake=show(test,"llvm/cmake/modules/HandleLLVMOptions.cmake")
    block="if(LLVM_PROFDATA_FILE AND EXISTS "+cmake.split("if(LLVM_PROFDATA_FILE AND EXISTS ",1)[1].split("\n\nif(LLVM_SPROFDATA_FILE",1)[0]
    (d/"llvm-cmake-profdata-block.txt").write_text(block+"\n")
    script=d/"flags-probe.cmake"
    script.write_text(f'set(LLVM_PROFDATA_FILE "{unpacked}")\n'
        'set(CMAKE_CXX_COMPILER_ID Clang)\n'
        'function(append value)\n'
        '  foreach(variable IN LISTS ARGN)\n'
        '    set(${variable} "${${variable}} ${value}" PARENT_SCOPE)\n'
        '  endforeach()\n'
        'endfunction()\n'+block+'\n'
        'message("C_FLAGS=${CMAKE_C_FLAGS}")\nmessage("CXX_FLAGS=${CMAKE_CXX_FLAGS}")\n')
    p=logged(d,"cmake-script-flags",[*RPM[:-1],R/"usr/bin/cmake","-P",script])
    both=p.stdout+p.stderr
    flag=f'-fprofile-instr-use="{unpacked}"'
    require(all(f"{kind}_FLAGS= {flag}" in both for kind in ("C","CXX")),
            "CMake script did not produce the required profile-use flags")
    return flag

def validate_candidate(d,kind,base,test,assets):
    manifest=assets/"llvm-profiles.manifest"
    body=read(manifest)
    require(body["status"]=="UNQUALIFIED","integration must retain UNQUALIFIED")
    original_helper=show(base,HELPER)
    require(original_helper==show(RECIPE,HELPER),"the integration changed the production helper")
    require(show(test,HELPER)==verification_helper(original_helper),
            "verification helper changed more than the status allowance")
    bolt=kind=="B"
    row=next(r for r in body["profiles"] if r["project"]=="T" and r["pgo"] is True and r["bolt"]==bolt)
    asset=assets/row["profdata"]["file"]
    helper=assets/"clang-bolt-helper.py"
    helper.write_text(show(test,HELPER))
    spec=assets/"llvm.spec"
    require(spec.read_text()==show(test,SPEC),"candidate spec working copy differs from Git")
    default=assets/"integration-llvm.spec"
    default.write_text(show(base,SPEC))
    cli=[sys.executable,"-B",SKILL/"manifest.py","check","--manifest",manifest,"--project","T",
         "--pgo","on","--bolt","on" if bolt else "off","--allow-unqualified"]
    logged(d,"skill-manifest-check",cli)
    work=d/"profile-check"
    argv=[sys.executable,"-B",helper,"pgo-prepare",manifest,"T",work,asset]
    tracked=[manifest,asset]
    if bolt:
        paired=assets/row["bolt_profile"]["file"]
        tracked.append(paired)
        argv+=["--bolt-profile",paired]
    for path in tracked:
        require(git("hash-object",str(path)).strip()==git("rev-parse",test+":packaging/"+path.name).strip(),
                "the Git Source blob differs from the validated asset: "+path.name)
    production=d/"integration-helper.py"
    production.write_text(original_helper)
    deny=list(argv)
    deny[2]=production
    deny[6]=d/"integration-rejection-work"
    denied=logged(d,"integration-manifest-rejects-unqualified",deny,expect=(1,))
    require("profile manifest is not READY" in denied.stdout+denied.stderr,
            "production gate did not reject UNQUALIFIED at the status check")
    logged(d,"packaged-manifest-check",argv)
    unpacked=work/"clang.profdata"
    require(file_identity(unpacked)==PROFDATA,"packaged helper emitted different profdata")
    if bolt:
        require(file_identity(work/"clang.fdata")=={key:row["bolt_profile"][key] for key in ("bytes","sha256")},
                "packaged helper emitted different fdata")
    flag=build_flags_probe(d,unpacked,test)
    results={}
    for arch in ("x86_64","aarch64","armv7l"):
        s=expand(d,"test",arch,spec)
        b=expand(d,"integration-default",arch,default)
        if arch=="x86_64":
            require(not re.search(r'(?m)^\s*python.* pgo-prepare ',b),"integration enabled PGO by default")
            require('-DLLVM_PROFDATA_FILE="$PWD/pgo-profiles/clang.profdata"' in s and
                    "-DTIZEN_PGO_EXCLUDE_RUNTIMES=ON" in s and " pgo-check-ninja " in s and
                    "-DTIZEN_HYBRID_LINK=ON" in s,"x86_64 switches or profile-use binding mismatch")
            prepare=[line for line in s.splitlines() if line.startswith("python3 ") and " pgo-prepare " in line]
            require(len(prepare)==1 and f'"{manifest}" T ' in prepare[0] and str(asset) in prepare[0],
                    "expanded build does not use the checked Toolchain mapping and asset")
            require(("echo BOLT_PIPELINE_PASS" in s)==bolt and bool(re.search(r"(?m)^Source1203:",s))==bolt,
                    "expanded BOLT switch or fdata Source differs from request")
            if bolt:
                require("--bolt-profile" in prepare[0] and str(paired) in prepare[0] and
                        'cp "$PWD/pgo-profiles/clang.fdata" "$BOLT_WORK/profile.fdata"' in s and
                        not re.search(r'(?m)^python3 .* unpack .*profile\.fdata',s),
                        "BOLT stage is not bound exclusively to the paired fdata")
                text=helper.read_text()
                require(text.count("'-stale-threshold=5'")==1 and
                        "'-data='+str(profile)" in text and "work/'profile.fdata'" in text,
                        "BOLT gate threshold or pipeline data argument changed")
        else:
            require(s==b,f"{arch} expansion differs from the default integration")
            require(" pgo-prepare " not in s and "-DLLVM_PROFDATA_FILE=" not in s and
                    "echo BOLT_PIPELINE_PASS" not in s,f"{arch} unexpectedly enables a profile path")
        results[arch]="PASS"
    return {"rpmspec":results,"skill_manifest":"PASS","packaged_manifest":"PASS",
            "integration_rejects_unqualified":"PASS","verification_only_status_difference":"PASS",
            "compile_flag_script":flag,"profile":receipt(asset),"manifest":receipt(manifest),
            "variant":"PGO+BOLT" if bolt else "PGO-only","project":"T",
            **({"bolt_profile":receipt(paired),"stale_threshold":5} if bolt else {})}

def make_patches(d,first,last):
    directory=d/"patches"
    directory.mkdir()
    for index,rev in enumerate((first,last),1):
        path=directory/f"{index:02}-{rev[:8]}.patch"
        p=command([*GIT,"format-patch","--stdout","--full-index","--no-binary","--no-signature","-1",rev])
        path.write_text(p.stdout)
        full=d/f"{index:02}-{rev[:8]}-with-binary.patch"
        with full.open("xb") as out:
            p=subprocess.run([*GIT,"format-patch","--stdout","--full-index","--binary","--no-signature","-1",rev],
                             stdout=out,stderr=subprocess.PIPE,env=ENV,timeout=180)
        require(not p.returncode,p.stderr.decode(errors="replace"))
        info=receipt(full)
        if info["bytes"]<=10_000_000:
            shutil.copyfile(full,directory/full.name)
        else:
            save(directory/(full.name+".json"),info)

def upload(d,kind,tip):
    label="only" if kind=="A" else "bolt"
    branch=f"sandbox/lhmax2025/llvm-pgo-{label}-20261125"
    ref="refs/heads/"+branch
    before=logged(d,"sandbox-before",[*GIT,"ls-remote","--exit-code","--heads",REMOTE,ref],
                  expect=(2,),timeout=45)
    require(not before.stdout,"Gerrit reports an existing ref")
    e={**ENV,"TASK157_REMOTE":REMOTE,"TASK157_EXPECT_OID":tip,"TASK157_EXPECT_REF":ref}
    logged(d,"sandbox-push",[*GIT,"-c",f"core.hooksPath={A/'hooks'}","push","--porcelain",
                           REMOTE,tip+":"+ref],env=e,timeout=240)
    save(d/"remote-write.json",{"branch":branch,"tip":tip,"push_rc":0})
    p=logged(d,"sandbox-after",[*GIT,"ls-remote","--exit-code","--heads",REMOTE,ref],timeout=45)
    require(p.stdout.split()==[tip,ref],"post-push Gerrit ref did not match candidate")
    return branch,p.stdout.strip()

def finalize(kind,previous=None):
    stages=() if kind=="A" else ("G6","G7","G8")
    for name in stages:
        require(read(OLD/(name+".json")).get("status")=="PASS",f"{name} must pass before candidate preparation")
    recipe=preflight()
    d=A/kind
    d.mkdir()
    results={"kind":kind,"status":"STOP","baseline":recipe}
    try:
        if kind=="B":
            raw=PROFILES/"bolt-match.json"
            gate=read(raw)
            shutil.copyfile(raw,d/"G7-match.json")
            n,s,u=gate["N"],gate["S"],gate["U"]
            require(n>0 and 100*(s+u)<=5*(n+u) and 100*s<=5*n,"G7 counters exceed the 5 percent bound")
            # Record what the final stage produced even when its delivered
            # status cannot be consumed by the packaging helper.
            shutil.copyfile(PROFILES/"llvm-profiles.manifest",d/"G8-original-manifest.json")
            integ,test,assets=make_b(d,previous)
        else:
            integ,test,assets=make_a(d)
        results.update(integration=integ,test=test,tree=git("rev-parse",test+"^{tree}").strip())
        git("update-ref",f"refs/heads/task157/{kind.lower()}-integration",integ)
        git("update-ref",f"refs/heads/task157/{kind.lower()}-candidate",test)
        revs=git("rev-list","--reverse","--topo-order",PS5+".."+test).splitlines()
        message_gate(d,revs)
        results["checks"]=validate_candidate(d,kind,integ,test,assets)
        make_patches(d,integ,test)
        branch,actual=upload(d,kind,test)
        results.update(status="PASS",branch=branch,ls_remote=actual)
    except Exception as error:
        results["error"]=str(error)
        (d/"STOP.txt").write_text(str(error)+"\n")
    save(d/"result.json",results)
    return results
