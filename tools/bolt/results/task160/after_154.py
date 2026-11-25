"""Start the new G chain after the documented 154-B handoff."""
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

A=Path(__file__).resolve().parent
W=A.parents[1]
B=W.with_name(W.name+'-bolt')
RUN=A/'run'
sys.path.insert(0,str(RUN/'orchestration'))
from policy import DEADLINE, ZONE
STATUSES={'active','activating','reloading','deactivating'}
ENV={**os.environ,'LC_ALL':'C','GIT_TERMINAL_PROMPT':'0'}


def call(*argv):
    return subprocess.run(argv,env=ENV,text=True,capture_output=True,timeout=100)


def git(*args):
    return call('/usr/bin/git','-C',B,*args)


def ready():
    p=call('/usr/bin/systemctl','--user','list-units','llvm-opt-task154-*.service',
           '--all','--plain','--no-legend','--no-pager')
    if p.returncode:
        return False,'unable to read task 154 service state: '+p.stderr
    active=[parts[0] for line in p.stdout.splitlines()
            if len(parts:=line.split())>=4 and parts[2] in STATUSES]
    if active:
        return False,'active: '+', '.join(active)
    stamp=W/'archive/task154/published-final.sha'
    if not stamp.is_file():
        return False,'154-B published receipt is missing'
    rev=stamp.read_text().strip()
    if git('cat-file','-e',rev+':tools/bolt/results/task154/final.json').returncode:
        return False,'154-B final receipt missing from the stated commit'
    remote=git('ls-remote','--exit-code','origin','refs/heads/bolt-v4')
    if remote.returncode or not remote.stdout.strip():
        return False,'unable to verify the evidence ref: '+remote.stderr
    head=remote.stdout.split()[0]
    if git('cat-file','-e',head+'^{commit}').returncode:
        p=git('fetch','--no-tags','--no-write-fetch-head','origin','refs/heads/bolt-v4')
        if p.returncode:
            return False,'unable to fetch the current evidence head: '+p.stderr
    if git('merge-base','--is-ancestor',rev,head).returncode:
        return False,'154-B final receipt is not published on the evidence branch'
    return True,rev


def save(path,row):
    temporary=path.with_suffix('.tmp')
    temporary.write_text(json.dumps(row,indent=2,ensure_ascii=False)+'\n')
    temporary.replace(path)


def publish_b(result):
    src=A/'candidates/B'
    evidence=B/'tools/bolt/results/task160/candidate-b'
    evidence.mkdir(parents=True,exist_ok=True)
    files=[]
    for p in sorted(src.rglob('*')):
        if not p.is_file() or p.suffix not in ('.txt','.json','.cmake','.patch','.manifest'):
            continue
        dest=evidence/p.relative_to(src)
        dest.parent.mkdir(parents=True,exist_ok=True)
        if p.stat().st_size <= 10_000_000:
            shutil.copyfile(p,dest)
            files.append(str(dest))
    for args in (('add','--',*files),('-c','user.name=Hao Lin','-c','user.email=hao.lin@samsung.com',
                   'commit','-s','-m','docs: record the paired PGO and BOLT candidate','--',*files),
                 ('push','origin','HEAD:refs/heads/bolt-v4')):
        proc=git(*args)
        print(proc.stdout,proc.stderr,flush=True)
        proc.check_returncode()
    head=git('rev-parse','HEAD').stdout.strip()
    check=git('ls-remote','--exit-code','origin','refs/heads/bolt-v4')
    check.check_returncode()
    if check.stdout.split()[0]!=head:
        raise RuntimeError('evidence branch was not verified after push')
    return head


def run_b():
    receipts={n:json.loads((RUN/(n+'.json')).read_text()) for n in ('G6','G7','G8')}
    if any(r['status']!='PASS' for r in receipts.values()):
        return {'status':'SKIPPED','stage_status':{n:r['status'] for n,r in receipts.items()},
                'reason':'G6, G7 and G8 must all pass'}
    sys.path.insert(0,str(A/'candidates'))
    import candidate
    preceding=candidate.read(A/'candidates/A/result.json')
    if preceding['status']!='PASS':
        return {'status':'STOP','reason':'Candidate A integration is unavailable'}
    for step in receipts:
        if not (RUN/('published-'+step+'.sha')).is_file():
            return {'status':'STOP','reason':'No published receipt for '+step}
    result=candidate.finalize('B',preceding)
    result['evidence_commit']=publish_b(result)
    return result


def main():
    while True:
        now=datetime.now(ZONE)
        if now>=DEADLINE:
            row={'admitted':False,'reason':'deadline reached while waiting for 154-B to end and publish'}
            break
        passed,reason=ready()
        if passed and not (RUN/'G-config/recover-g3.json').is_file():
            passed,reason=False,'G1-G3 checkpoint verification is still pending'
        row={'at':now.isoformat(),'admitted':passed,'reason':reason}
        save(RUN/'154-wait.json',row)
        print('154-B handoff',row,flush=True)
        if passed:
            row['publication']=reason
            break
        time.sleep(min(300,max(1,(DEADLINE-datetime.now(ZONE)).total_seconds())))
    save(RUN/'154-gate.json',row)
    subprocess.run(['/usr/bin/python3','-B',RUN/'orchestration/dispatch.py',W,B,RUN],
                   cwd=RUN,env=ENV,check=True)
    result=run_b()
    save(RUN/'paired-candidate.json',result)
    print('Paired candidate',json.dumps(result,ensure_ascii=False),flush=True)
    path=B/'tools/bolt/results/task160/g-chain/paired-candidate.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(RUN/'paired-candidate.json',path)
    for args in (('add','--',str(path)),('-c','user.name=Hao Lin','-c','user.email=hao.lin@samsung.com',
                 'commit','-s','-m','docs: summarize the paired candidate outcome','--',str(path)),
                 ('push','origin','HEAD:refs/heads/bolt-v4')):
        proc=git(*args)
        print(proc.stdout,proc.stderr,flush=True)
        proc.check_returncode()
    head=git('rev-parse','HEAD').stdout.strip()
    check=git('ls-remote','--exit-code','origin','refs/heads/bolt-v4')
    check.check_returncode()
    if check.stdout.split()[0]!=head:
        raise RuntimeError('final evidence branch was not verified after push')
    (RUN/'published-final.sha').write_text(head+'\n')


if __name__=='__main__':
    main()
