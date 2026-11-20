from datetime import datetime
from pathlib import Path
import json
import os
import re
import subprocess
import sys
import traceback

work=Path("/home/linhao/Toolchain/development/llvm-optimize/archive/task147-fix")
repo=Path("/home/linhao/Toolchain/development/llvm-optimize/archive/task144/objects.git")
git=["/usr/bin/git","--git-dir="+str(repo)]
remote="ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm"
ssh=["/usr/bin/ssh","-o","BatchMode=yes","-o","ConnectTimeout=15","-p","29418","lhmax2025@review.tizen.org"]
env=dict(os.environ,GIT_SSH_COMMAND="/usr/bin/ssh -o BatchMode=yes -o ConnectTimeout=15",
         GIT_TERMINAL_PROMPT="0",LC_ALL="C")
c2="5e58d65678e2d936b28eb4458bbd73a51abe5e06"
ps4="1ddecbe8729f832b5ef565092d039f68df647a43"
tree="ef1ab363fa8e9be29eb930916e86c6e8f10f11af"
change="Ie2c1d45cea6703a0caef72187397275a03e66468"
name="Hao Lin"
email="hao.lin@samsung.com"
ref="refs/heads/361624-ps5"
signoff=b"Signed-off-by: Hao Lin <hao.lin@samsung.com>\n"
ident=["-c","user.name="+name,"-c","user.email="+email]
for key in ("GIT_AUTHOR_NAME","GIT_AUTHOR_EMAIL","GIT_AUTHOR_DATE","GIT_COMMITTER_NAME","GIT_COMMITTER_EMAIL","GIT_COMMITTER_DATE"):
    env.pop(key,None)

class Stop(RuntimeError):
    """A task gate stopped the preparation."""

def stamp():
    return datetime.now().astimezone().isoformat(timespec="seconds")
def require(ok,message):
    if not ok: raise Stop(str(message))
def save(filename,value):
    (work/filename).write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n")
def run(argv,label=None,variables=None):
    p=subprocess.run(argv,env=variables or env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if label:
        (work/(label+".stdout")).write_bytes(p.stdout)
        (work/(label+".stderr")).write_bytes(p.stderr)
        save(label+".argv.json",argv)
    if p.returncode:
        raise Stop(f"exit={p.returncode} argv={argv!r}\n"+p.stderr.decode("utf-8","replace").rstrip())
    return p.stdout
def part(rev):
    raw=run([*git,"cat-file","commit",rev])
    header,msg=raw.split(b"\n\n",1)
    return dict(line.split(b" ",1) for line in header.splitlines()),msg
def unique_hash(message, author, parent):
    m=re.fullmatch(rb"(.+) <([^<>]+)> (\d+) ([+-]\d{4})",author)
    require(m,"invalid original author header")
    variables={**env,"GIT_AUTHOR_NAME":m[1].decode(),"GIT_AUTHOR_EMAIL":m[2].decode(),
               "GIT_AUTHOR_DATE":"@"+m[3].decode()+" "+m[4].decode(),
               "GIT_COMMITTER_NAME":name,"GIT_COMMITTER_EMAIL":email}
    file=work/"F2-message.txt"
    file.write_bytes(message)
    attempts=[]
    for i in range(2):
        now=datetime.now().astimezone()
        variables["GIT_COMMITTER_DATE"]=f"@{int(now.timestamp())+i} {now.strftime('%z')}"
        argv=[*git,*ident,"commit-tree",tree,"-p",parent,"-F",str(file)]
        result=run(argv,"commit-tree-"+str(i+1),variables).decode().strip()
        matches=run([*git,"ls-remote","--heads",remote],"gerrit-heads-"+str(i+1)).decode().splitlines()
        require(matches and all(re.fullmatch(r"[a-f0-9]{40}\trefs/heads/[^\s]+",l) for l in matches),
                "Gerrit ls-remote --heads returned an empty or malformed listing")
        found=[line.split()[1] for line in matches if line.split()[0]==result]
        attempts.append({"hash":result,"committer_date":variables["GIT_COMMITTER_DATE"],"remote_head_count":len(matches),
                         "matching_remote_branches":found})
        save("remote-branch-screen.json",attempts)
        if not found:
            return result,attempts
    raise Stop(f"F matches Gerrit branch heads after timestamp regeneration: {attempts!r}")

F="2fdceb61ca6e2309fb4885615dc1f430721d21e9"
addition=b"""Keep in-tree BOLT on component libraries by setting BOLT_LLVM_LINK_MODE
before its consumers. List the unused X86 mirror in LLVM_OPTIONAL_SOURCES
and compile it only for standalone dylib builds. Clear the inherited
runtime C and C++ flags only for standalone builds.

Restore ARM;BPF as the armv7l LLVM target list and drop the explicit
python3 requirement from llvm. Limit the standalone spec to x86_64 and
aarch64, set BOLT_TARGETS_TO_BUILD per architecture, and verify target
registration.

Bind the LLVM provider build requirements to the LLVM version and check
that the installed providers share one version and release. Keep the
libllvm version requirement for bolt and remove its compiler-rt runtime
requirement. Derive LLVM_LIBDIR_SUFFIX from %{_lib}, retain distribution
LDFLAGS, correct the debug packaging comments, and let CMake install
merge-fdata once.
"""

def main():
    import difflib
    old,msg=part(F)
    base,original=part(ps4)
    require(run([*git,"rev-parse",ref]).decode().strip()==F,"local branch is not the expected F")
    require(old[b"tree"]==tree.encode() and old[b"parent"]==base[b"parent"] and old[b"author"]==base[b"author"],
            "F tree/parent/author differs from task identity")
    split=b"\n\nChange-Id: "
    require(original.count(split)==1,"unexpected PS4 message layout")
    prefix,trailers=original.split(split)
    trailers=b"Change-Id: "+trailers
    require(trailers.endswith(b"\n") and not signoff in trailers and trailers.splitlines()[0]==b"Change-Id: "+change.encode(),
            "PS4 trailers or Change-Id differ")
    final=prefix+b"\n\n"+addition+b"\n"+trailers+signoff
    f,heads=unique_hash(final,base[b"author"],base[b"parent"].decode())
    h,body=part(f)
    require(h[b"tree"]==old[b"tree"] and h[b"parent"]==base[b"parent"] and h[b"author"]==base[b"author"],
            "F2 tree, parent or author verification failed")
    require(h[b"committer"].startswith(b"Hao Lin <hao.lin@samsung.com> ") and body==final,
            "F2 committer or message verification failed")
    def history(message):
        return b"".join(l for l in message.splitlines(keepends=True) if re.match(rb"^\* [0-9a-f]+ - ",l))
    a,b=history(original),history(body)
    (work/"ps4-history.txt").write_bytes(a)
    (work/"F2-history.txt").write_bytes(b)
    history_diff=b"".join(difflib.diff_bytes(difflib.unified_diff,a.splitlines(keepends=True),
                    b.splitlines(keepends=True),fromfile=b"PS4",tofile=b"F2"))
    (work/"PS4-to-F2-history.diff").write_bytes(history_diff)
    require(a and a==b and not history_diff,"PS4 history differs from F2")
    diff=b"".join(difflib.diff_bytes(difflib.unified_diff,msg.splitlines(keepends=True),
                body.splitlines(keepends=True),fromfile=b"F",tofile=b"F2"))
    (work/"F-to-F2-message.diff").write_bytes(diff)
    # Restored history and original trailers already appear verbatim in PS4.
    added=addition.splitlines()+[signoff.rstrip()]
    rx=r"github|lhmax|llvm-optimize|sandbox|bolt-v4|codex|claude|openai|\b(?:ai|cline|chatgpt|copilot)\b|\btask[ _-]*\d{1,4}\b|\d{1,4}\s*号|/home/"
    hits=[row.decode() for row in added if re.search(rx,row.decode(),re.I)]
    save("outbound-text-check.json",{"case_insensitive_regex":rx,"added_message_lines":[x.decode() for x in added],"hits":hits})
    require(not hits,f"banned terms: {hits}")
    latest=run([*ssh,"gerrit","query","--format=JSON","--current-patch-set","--patch-sets","change:361624"],"gerrit-361624")
    rows=[json.loads(x) for x in latest.splitlines() if x]
    row,=[x for x in rows if x.get("number") in (361624,"361624") and x.get("project")=="platform/upstream/llvm" and x.get("branch")=="tizen_base"]
    cur=row["currentPatchSet"]
    require(int(cur["number"])==4 and cur["revision"]==ps4,
            f"STOP A: Gerrit 361624 latest PS{cur['number']} revision {cur['revision']}; expected PS4 {ps4}")
    patch=run([*git,"format-patch","--stdout","--no-signature","--full-index","--binary","-1",f])
    require(patch.startswith(("From "+f+" ").encode()),"format-patch identity check failed")
    (work/"0001-361624-ps5-F2.patch").write_bytes(patch)
    run([*git,"update-ref",ref,f,F])
    save("result-a.json",{"status":"PASS","F":F,"F2":f,"tree":tree,"parent":h[b"parent"].decode(),
                         "author":h[b"author"].decode(),"committer":h[b"committer"].decode(),
                         "change_id":change,"history_lines":len(a.splitlines()),"history_equal":True,
                         "retained_ps4_trailers":body.endswith(trailers+signoff),"outbound_hits":hits,
                         "remote_heads":heads[-1],"gerrit_ps":4,"gerrit_revision":ps4,
                         "gerrit_status":row["status"],"at":stamp()})
    print((work/"result-a.json").read_text(),flush=True)
try:
    main()
except Exception:
    (work/"A-STOP.txt").write_text(traceback.format_exc())
    traceback.print_exc()
    sys.exit(1)
