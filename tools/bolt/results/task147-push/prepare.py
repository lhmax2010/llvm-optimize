from datetime import datetime
from pathlib import Path
import difflib
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import traceback

WORK=Path(__file__).resolve().parent
GIT=["/usr/bin/git","--git-dir=/home/linhao/Toolchain/development/llvm-optimize/archive/task144/objects.git"]
REMOTE="ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm"
SSH=["/usr/bin/ssh","-o","BatchMode=yes","-o","ConnectTimeout=15","-p","29418","lhmax2025@review.tizen.org"]
ENV={**os.environ,"GIT_SSH_COMMAND":"/usr/bin/ssh -o BatchMode=yes -o ConnectTimeout=15","GIT_TERMINAL_PROMPT":"0","LC_ALL":"C"}
F2="636ef90aa1ff75ca8731b84b1526e6a557cffcd6"
PS4="1ddecbe8729f832b5ef565092d039f68df647a43"
TREE="ef1ab363fa8e9be29eb930916e86c6e8f10f11af"
PARENT="f346dd75e87de324dc2abe61454ca1c49969d12d"
CID=b"Change-Id: Ie2c1d45cea6703a0caef72187397275a03e66468"
SIGNED=b"Signed-off-by: Hao Lin <hao.lin@samsung.com>\n"
A=b"""Keep in-tree BOLT on component libraries by setting BOLT_LLVM_LINK_MODE
before its consumers. List the X86 mirror in LLVM_OPTIONAL_SOURCES, as
only standalone dylib builds compile it. Clear the inherited runtime C
and C++ flags only for standalone builds."""
B=b"""Bind the LLVM provider build requirements to the LLVM version and check
that the installed providers share one version and release. Require
libllvm = %{version} at runtime for bolt and drop its explicit
compiler-rt runtime requirement. Derive LLVM_LIBDIR_SUFFIX from %{_lib},
retain distribution LDFLAGS, correct the debug packaging comments, and
let CMake install merge-fdata once."""
C=b"""The --build-id=sha1 flag is added to the executable and shared-library
linker flags; module linker flags keep their existing settings."""

class Stop(RuntimeError):
    pass
def require(yes, raw):
    if not yes:
        raise Stop(str(raw))
def now():
    return datetime.now().astimezone().isoformat(timespec="seconds")
def save(name, obj):
    (WORK/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n")
def run(argv,label=None,env=None,returns=(0,)):
    result=subprocess.run(argv,env=ENV if env is None else env,capture_output=True)
    if label:
        (WORK/(label+".stdout")).write_bytes(result.stdout)
        (WORK/(label+".stderr")).write_bytes(result.stderr)
        save(label+".argv.json",argv)
    if result.returncode not in returns:
        raise Stop(f"exit={result.returncode} {shlex.join(argv)}\n"
                   +(result.stdout+result.stderr).decode("utf-8","replace"))
    return result.stdout
def commit(id_):
    header,message=run([*GIT,"cat-file","commit",id_]).split(b"\n\n",1)
    return dict(s.split(b" ",1) for s in header.splitlines()),message
def diff(x,y,old,new):
    return b"".join(difflib.diff_bytes(difflib.unified_diff,x.splitlines(keepends=True),y.splitlines(keepends=True),
                                       fromfile=old,tofile=new))
def history(m):
    return b"".join(l for l in m.splitlines(keepends=True) if re.match(rb"^\* [0-9a-f]+ - ",l))
def review_query(raw):
    rows=[json.loads(x) for x in raw.splitlines() if x.strip()]
    selected=[x for x in rows if x.get("number") in (361624,"361624")]
    require(len(selected)==1 and selected[0].get("project")=="platform/upstream/llvm",
            raw.decode("utf-8","replace"))
    return selected[0]
def ps4_gate(row):
    cur=row.get("currentPatchSet",{})
    require(row.get("status")=="NEW" and str(cur.get("number"))=="4" and cur.get("revision")==PS4,
            json.dumps(row,ensure_ascii=False))
    require(cur.get("parents")==[PARENT],"PS4 parent differs from task expectation: "+json.dumps(cur))
    branch=row["branch"]
    require(isinstance(branch,str) and branch and "%" not in branch and not branch.startswith("refs/"),
            f"rejected branch from Gerrit: {branch!r}")
    run([*GIT,"check-ref-format","refs/heads/"+branch])
    return branch
def raw_query(label):
    return run([*SSH,"gerrit","query","--format=JSON","--current-patch-set","--patch-sets","change:361624"],label)

def prepare():
    before=(WORK/"gerrit-before.jsonl").read_bytes()
    branch=ps4_gate(review_query(before))
    fh,msg=commit(F2)
    ph,pmsg=commit(PS4)
    require(fh[b"tree"].decode()==TREE and fh[b"parent"].decode()==PARENT,
            {k.decode():v.decode() for k,v in fh.items()})
    require(fh[b"author"]==ph[b"author"],"F2 author header differs from PS4")
    checks=[]
    for name in ("packaging/llvm.spec","packaging/llvm-tools-subpkgs.spec"):
        raw=run([*GIT,"show",TREE+":"+name])
        lines=raw.decode().splitlines()
        found=[{"line":j,"text":s} for j,s in enumerate(lines,1) if "--build-id=sha1" in s]
        pattern=re.compile(r'^\s*-DCMAKE_(EXE|SHARED)_LINKER_FLAGS=')
        applicable=[pattern.match(x["text"]) for x in found]
        require(len(found)==2 and all(applicable) and {m[1] for m in applicable}=={"EXE","SHARED"},
                f"build-id linker scope differs in {name}: {found!r}")
        checks.append({"file":name,"sha256":hashlib.sha256(raw).hexdigest(),"build_id_sha1":found,
                       "module_related":[{"line":j,"text":s} for j,s in enumerate(lines,1)
                                         if "MODULE_LINKER_FLAGS" in s],"module_build_id_sha1":False})
    pre={"status":"PASS","gerrit_status":"NEW","gerrit_ps":4,"gerrit_revision":PS4,"target_branch":branch,
         "F2":F2,"tree":TREE,"parent":PARENT,"author":fh[b"author"].decode(),"spec_checks":checks}
    save("preflight.json",pre)
    p=msg.split(b"\n\n")
    require(len(p)==6 and p[2].startswith(b"Keep in-tree BOLT ") and p[4].startswith(b"Bind the LLVM provider "),
            "F2 paragraph layout differs from the requested edit")
    require(p[5].startswith(CID+b"\n") and p[5].endswith(SIGNED),"F2 trailer block mismatch")
    require(history(pmsg)==history(msg) and len(history(msg).splitlines())==9,"F2 does not retain all PS4 history")
    p4_trailer=CID+pmsg.split(b"\n\n"+CID,1)[1]
    require(p[5]==p4_trailer+SIGNED,"F2 does not retain PS4's complete inherited trailer order")
    expected=b"\n\n".join([p[0],p[1],A,p[3],B,C,p[5]])
    require(max(len(x) for para in (A,p[3],B,C) for x in para.splitlines())<=72,"prose exceeds 72 columns")
    rx=re.compile(r'github|lhmax|llvm-optimize|sandbox|bolt-v4|codex|claude|openai|\b(?:chatgpt|cline|copilot|ai)\b|\btask[ _-]*\d{1,4}\b|\d{1,4}\s*号|/home/',re.I)
    edits=[l.decode() for para in (A,B,C) for l in para.splitlines()]
    hits=[l for l in edits if rx.search(l)]
    require(not hits,f"new commit text contains forbidden terms: {hits!r}")
    (WORK/"F3-message.txt").write_bytes(expected)

    author=re.fullmatch(rb"(.+) <([^<>]+)> (\d+) ([+-]\d{4})",fh[b"author"])
    require(author,"F2 author header unparsable")
    clock=datetime.now().astimezone()
    env={**ENV,"GIT_AUTHOR_NAME":author[1].decode(),"GIT_AUTHOR_EMAIL":author[2].decode(),
         "GIT_AUTHOR_DATE":"@"+author[3].decode()+" "+author[4].decode(),"GIT_COMMITTER_NAME":"Hao Lin",
         "GIT_COMMITTER_EMAIL":"hao.lin@samsung.com","GIT_COMMITTER_DATE":f"@{int(clock.timestamp())} {clock.strftime('%z')}"}
    f3=run([*GIT,"-c","user.name=Hao Lin","-c","user.email=hao.lin@samsung.com","-c","commit.gpgSign=false",
            "commit-tree",TREE,"-p",PARENT,"-F",str(WORK/"F3-message.txt")],"commit-tree",env=env).decode().strip()
    require(f3!=F2,"F3 has F2's SHA")
    hh,actual=commit(f3)
    require(all(hh[k]==fh[k] for k in (b"tree",b"parent",b"author")) and actual==expected,
            "F3 tree, parent, author or exact message differs")
    require(hh[b"committer"].startswith(b"Hao Lin <hao.lin@samsung.com> "),"wrong committer identity")
    hdiff=diff(history(pmsg),history(actual),b"PS4",b"F3")
    require(not hdiff,"PS4→F3 history diff is nonempty")
    (WORK/"PS4-to-F3-history.diff").write_bytes(hdiff)
    mdiff=diff(msg,actual,b"F2",b"F3")
    (WORK/"F2-to-F3-message.diff").write_bytes(mdiff)
    branches=run([*GIT,"ls-remote","--heads",REMOTE],"gerrit-heads").decode().splitlines()
    require(branches and all(re.fullmatch(r"[a-f0-9]{40}\trefs/heads/[^\s]+",l) for l in branches),
            "empty or malformed Gerrit --heads output")
    unmatched=[l for l in branches if l.startswith(f3+"\t")]
    require(not unmatched,f"F3 already matches Gerrit branch heads: {unmatched!r}")
    push_options=run([*GIT,"config","--get-all","push.pushOption"],returns=(0,1)).decode().splitlines()
    follow_tags=run([*GIT,"config","--get","--bool","push.followTags"],returns=(0,1)).decode().strip()
    require(not any(push_options) and follow_tags!="true","configured push options or follow tags are active")
    patch=run([*GIT,"format-patch","--stdout","--no-signature","--full-index","--binary","-1",f3])
    require(patch.startswith(("From "+f3+" ").encode()),"format-patch SHA mismatch")
    (WORK/"0001-361624-PS5-F3.patch").write_bytes(patch)
    push=[*GIT,"push",REMOTE,f3+":refs/for/"+branch]
    save("checks.json",{"status":"PASS","preflight":pre,"F3":f3,"tree":TREE,"parent":PARENT,
         "raw_author":hh[b"author"].decode(),"raw_committer":hh[b"committer"].decode(),"change_id":CID.decode().split(" ",1)[1],
         "only_requested_edits":True,"max_prose_columns":72,"ps4_history_diff_bytes":len(hdiff),
         "ps4_trailers_same_in_original_order":True,"hao_signoff_last":True,"outbound_new_lines_checked":len(edits),
         "forbidden_word_hits":hits,"advertised_heads":len(branches),"heads_pointing_at_F3":unmatched,
         "push_argv":push,"pre_push_evidence":{"F3_patch_sha256":hashlib.sha256(patch).hexdigest(),
         "message_diff_sha256":hashlib.sha256(mdiff).hexdigest()},"done_at":now()})
    print((WORK/"checks.json").read_text(),flush=True)

if __name__=="__main__":
    try:
        prepare()
    except Exception:
        (WORK/"preparation-STOP.txt").write_text(traceback.format_exc())
        traceback.print_exc()
        sys.exit(1)
