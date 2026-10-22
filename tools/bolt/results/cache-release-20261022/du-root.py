import time,json,subprocess
from pathlib import Path
D=Path(__file__).resolve().parent;R=D/'baseline-root/local/BUILD-ROOTS/scratch.x86_64.0';E=D/'baseline-segment2'
while True:
    start=time.monotonic();stamp=time.time_ns()
    argv=['sudo','-n','/usr/sbin/chroot',str(R),'/bin/du','-sx','-B1','/']
    p=subprocess.run(argv,capture_output=True,text=True)
    with (E/'du-root-complete.jsonl').open('a') as f:f.write(json.dumps({'time_ns':stamp,'argv':argv,'stdout':p.stdout,'stderr':p.stderr,'rc':p.returncode,'seconds':time.monotonic()-start})+'\n')
    if p.returncode:break
    for n in range(max(0,int(60-(time.monotonic()-start)))):
        state=subprocess.run(['systemctl','--user','is-active','bolt-cache-baseline-20261022-2.service'],capture_output=True,text=True).stdout.strip()
        if state not in ['active','activating','deactivating']:raise SystemExit(0)
        time.sleep(1)
