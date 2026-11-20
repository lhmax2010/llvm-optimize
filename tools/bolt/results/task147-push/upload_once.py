import hashlib
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys
import time
import traceback

from prepare import (WORK,GIT,REMOTE,ENV,PS4,PARENT,Stop,require,now,save,run,raw_query,review_query,ps4_gate)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def upload():
    checked=json.loads((WORK/"checks.json").read_text())
    require(checked["status"]=="PASS","missing PASS preflight")
    f3=checked["F3"]
    require(re.fullmatch("[0-9a-f]{40}",f3),"wrong F3 format")
    evidence=checked["pre_push_evidence"]
    require(sha(WORK/"0001-361624-PS5-F3.patch")==evidence["F3_patch_sha256"]
            and sha(WORK/"F2-to-F3-message.diff")==evidence["message_diff_sha256"],
            "pre-push evidence changed")
    branch=ps4_gate(review_query(raw_query("gerrit-immediately-before")))
    require(branch==checked["preflight"]["target_branch"],"review target branch changed")
    args=[*GIT,"push",REMOTE,f3+":refs/for/"+branch]
    require(args==checked["push_argv"],"push argv differs from preflight")
    # An exclusive marker records the sole authorized push before it runs.
    with (WORK/"push-attempt.json").open("x") as f:
        f.write(json.dumps({"started_at":now(),"argv":args},indent=2)+"\n")
    print(shlex.join(args),flush=True)
    with (WORK/"push-output.txt").open("wb") as f:
        r=subprocess.run(args,env=ENV,stdout=f,stderr=subprocess.STDOUT)
    raw=(WORK/"push-output.txt").read_bytes()
    sys.stdout.buffer.write(raw)
    sys.stdout.flush()
    save("push-result.json",{"finished_at":now(),"exit_code":r.returncode,"argv":args})
    if r.returncode:
        raise Stop(raw.decode("utf-8","replace"))
    raw_ref=run([*GIT,"ls-remote","--exit-code",REMOTE,"refs/changes/24/361624/5"],"gerrit-ps5-ref")
    expected_ref=f"{f3}\trefs/changes/24/361624/5"
    require(raw_ref.decode().rstrip()==expected_ref,raw_ref.decode())
    for attempt in range(1,5):
        data=raw_query(f"gerrit-after-{attempt}")
        post=review_query(data)
        ps=post["currentPatchSet"]
        # The read-only query can trail the ref update briefly.
        if str(ps["number"])=="4" and ps["revision"]==PS4 and attempt<4:
            time.sleep(2)
            continue
        (WORK/"gerrit-after.jsonl").write_bytes(data)
        require(post["status"]=="NEW" and post["branch"]==branch and str(ps["number"])=="5"
               and ps["revision"]==f3 and ps["parents"]==[PARENT],data.decode("utf-8","replace"))
        require(any(str(x.get("number"))=="4" and x.get("revision")==PS4 for x in post.get("patchSets",[])),
                    "PS4 missing after upload\n"+data.decode("utf-8","replace"))
        save("postflight.json",{"status":"PASS","queried_at":now(),"change":361624,"latest_ps":5,
           "revision":f3,"parent":PARENT,"gerrit_status":"NEW","branch":branch,"ps4_preserved":True,
           "ps4_revision":PS4,"ps5_ref":expected_ref})
        print(data.decode("utf-8","replace"),end="",flush=True)
        return

try:
    upload()
except Exception:
    (WORK/"upload-STOP.txt").write_text(traceback.format_exc())
    traceback.print_exc()
    sys.exit(1)
