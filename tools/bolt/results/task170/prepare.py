"""Prepare and validate the exact one-line recipe repair and QB candidate."""
from pathlib import Path
import re
import shutil
import sys

A=Path(__file__).resolve().parent
W=A.parents[1]
B=W.with_name(W.name+"-bolt")
S=W/"archive/task160/candidates"
sys.path.insert(0,str(S))
import candidate as c

BASE="070c94c9263e8b003a899e6c31bcee34f6a64640"
PREVIOUS="4080f55abfc7c48097c9bd7fdbf9334e37c661af"
R_PARENT="ce627fa087233d9da415887222009155fe8b5029"
BRANCH="sandbox/lhmax2025/llvm-pgo-bolt-20261127-2"
D=A/"candidate"
BROKEN='"%{SOURCE1202}"%{?llvm_pgo_bolt_source}'
FIXED='"%{SOURCE1202}" %{?llvm_pgo_bolt_source}'
MESSAGE=("packaging: separate the BOLT profile argument\n\n"
         "Keep the PGO profile Source and the optional BOLT profile switch\n"
         "as separate shell words after RPM macro expansion.")
TEST=("packaging: enable clang PGO with BOLT for build verification (test only, not for merge)")
PROFILE="T-clang.profdata.xz"
FDATA="T-clang.fdata.xz"


def patch_spec(source):
    return c.replace(source,BROKEN,FIXED)


def argv_cli(spec,helper,output,profile,bolt_profile):
    return [sys.executable,"-B",c.SKILL/"check_helper_argv.py","--spec",spec,"--helper",helper,
            "--rpm-config",A/"rpm.json","--output",output,"--profile-name",profile,
            "--bolt-profile-name",bolt_profile]


def prove_negative():
    source=S/"B/assets"
    assert (source/"llvm.spec").read_text()==c.show(PREVIOUS,c.SPEC)
    assert (source/"clang-bolt-helper.py").read_text()==c.show(PREVIOUS,c.HELPER)
    log=c.logged(A,"argv-before-final",
        argv_cli(source/"llvm.spec",source/"clang-bolt-helper.py",A/"argv-original",PROFILE,FDATA),expect=(1,))
    r=c.read(A/"argv-original/result.json")
    failed={key for key,case in r["matrix"].items() if case["errors"]}
    assert failed=={"T-pgo1-bolt1","D-pgo1-bolt1"} and log.stdout.count("unrecognized arguments")==2


def diff_one_line(git,old,new,file):
    patch=git("diff",old,new,"--")
    assert git("diff","--name-only",old,new).splitlines()==[c.SPEC]
    assert git("diff","--numstat",old,new).strip()=="1\t1\t"+c.SPEC
    assert patch.count("-python3 ")==patch.count("+python3 ")==1
    assert BROKEN in patch and FIXED in patch
    file.write_text(patch)


def prepare_recipe():
    def git(*args):
        return c.command(["/usr/bin/git","-C",c.SRC,*args]).stdout
    assert git("branch","--show-current").strip()=="pgo-dev"
    assert git("rev-parse","HEAD").strip()==R_PARENT
    assert not git("status","--short","--untracked-files=no").strip()
    spec=c.SRC/c.SPEC
    spec.write_text(patch_spec(spec.read_text()))
    git("commit","-s","--only","-m",MESSAGE,"--",c.SPEC)
    recipe=git("rev-parse","HEAD").strip()
    diff_one_line(git,R_PARENT,recipe,A/"r-spec.diff")
    m=re.search(r"Source1203:\s+(\S+)",spec.read_text())
    assert m and m[1]=="clang-pgo.fdata.xz"
    c.logged(A,"r-argv",argv_cli(spec,c.SRC/c.HELPER,A/"argv-recipe",
                                 "clang-pgo.profdata.xz","clang-pgo.fdata.xz"))
    return recipe


def text_gate(d,base,integration,test):
    c.message_gate(d,c.git("rev-list","--reverse","--topo-order",c.PS5+".."+test).splitlines())
    contents=""
    for old,new in ((base,integration),(integration,test)):
        contents+="\n".join(line[1:] for line in c.git("diff","--unified=0",old,new).splitlines()
                             if line.startswith("+") and not line.startswith("+++"))+"\n"
    additions=d/"checked-code-additions.txt"
    additions.write_text(contents)
    for key,switch,regex,env in (("ascii","-nP",c.ASCII,c.ENV),("status","-niE",c.STATUS,{**c.ENV,"LC_ALL":"C.UTF-8"}),
                                ("extra","-niE",c.EXTRAS,{**c.ENV,"LC_ALL":"C.UTF-8"})):
        c.logged(d,"outward-added-"+key,["/usr/bin/grep",switch,regex,additions],env=env,expect=(1,))


def prepare():
    prove_negative()
    recipe=prepare_recipe()
    D.mkdir()
    assets=D/"assets"
    assets.mkdir()
    prior=S/"B/assets"
    for name in (PROFILE,FDATA,"llvm-profiles.manifest"):
        shutil.copyfile(prior/name,assets/name)
        assert c.git("hash-object",assets/name).strip()==c.git("rev-parse",BASE+":packaging/"+name).strip()
    raw=assets/"llvm.spec"
    raw.write_text(patch_spec(c.show(BASE,c.SPEC)))
    integration=c.local_commit(BASE,D,{c.SPEC:raw},MESSAGE,change_id=True)
    diff_one_line(c.git,BASE,integration,A/"integration-spec.diff")
    raw.write_text(c.replace(raw.read_text(),"%bcond_with clang_pgo\n","%bcond_without clang_pgo\n"))
    test=c.verification_commit(integration,D,assets,TEST)
    diff_one_line(c.git,PREVIOUS,test,A/"test-vs-previous.diff")
    (A/"test-only.diff").write_text(c.git("diff",integration,test,"--"))
    for ref,rev in (("integration",integration),("candidate",test)):
        c.git("update-ref","refs/heads/task170/pgo-bolt-"+ref,rev,"0"*40)
    old=c.read(S/"B/result.json")
    c.require(old["status"]=="PASS" and old["test"]==PREVIOUS,"prior qualification receipt changed")
    counts=c.read(c.PROFILES/"bolt-match.json")
    n,s,u=counts["N"],counts["S"],counts["U"]
    assert n>0 and 100*(s+u)<=5*(n+u) and 100*s<=5*n
    c.save(D/"G7-match.json",counts)
    text_gate(D,BASE,integration,test)
    checks=c.validate_candidate(D,"B",integration,test,assets)
    c.require_argv_receipt(D,test)
    tree=c.git("rev-parse",test+"^{tree}").strip()
    for label,rev in (("integration",integration),("test",test)):
        parts=c.git("show","-s","--format=%an <%ae>%n%cn <%ce>",rev).splitlines()
        assert parts==["Hao Lin <hao.lin@samsung.com>"]*2
        (D/(label+"-message.txt")).write_text(c.git("cat-file","commit",rev).split("\n\n",1)[1])
    result={"status":"READY","r_parent":R_PARENT,"recipe":recipe,"integration_parent":BASE,
            "integration":integration,"test":test,"replaces":PREVIOUS,"tree":tree,"branch":BRANCH,
            "checks":checks}
    c.save(A/"result.json",result)
    print(result,flush=True)


def push():
    result=c.read(A/"result.json")
    assert result["status"]=="READY" and result["branch"]==BRANCH
    c.require_argv_receipt(D,result["test"])
    with (A/"push-attempt.json").open("x") as claim:
        import json
        json.dump({"branch":BRANCH,"commit":result["test"]},claim)
        claim.write("\n")
    branch,receipt=c.upload(D,"B",result["test"],branch=BRANCH)
    result.update(status="PASS",ls_remote=receipt)
    c.save(A/"result.json",result)
    print(receipt,flush=True)


if __name__=="__main__":
    {"prepare":prepare,"push":push}[sys.argv[1]]()
