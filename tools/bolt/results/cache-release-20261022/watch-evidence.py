import sys,time,json,hashlib,subprocess,re
from pathlib import Path
D=Path(__file__).resolve().parent;E=D/'baseline-evidence';E.mkdir(exist_ok=True)
R=D/'baseline-root/local/BUILD-ROOTS/scratch.x86_64.0';seen=set();errors=set()
while True:
    for tmp in [R/'tmp',R/'var/tmp',R/'home/abuild/rpmbuild/tmp']:
        for p in tmp.glob('rpm-tmp.*'):
            try:
                data=p.read_bytes();sha=hashlib.sha256(data).hexdigest()
                if sha in seen:continue
                seen.add(sha);(E/('rpm-script-'+sha+'.sh')).write_bytes(data)
                with (E/'scripts.jsonl').open('a') as f:f.write(json.dumps({'time_ns':time.time_ns(),'source':str(p),'sha256':sha,'bytes':len(data)})+'\n')
            except OSError as ex:
                if str(ex) not in errors:
                    errors.add(str(ex))
                    with (E/'read-errors.txt').open('a') as f:f.write(str(ex)+'\n')
    state=subprocess.run(['systemctl','--user','is-active','bolt-cache-baseline-20261022-2.service'],capture_output=True,text=True).stdout.strip()
    if state not in ['active','activating','deactivating']:break
    time.sleep(5)
(E/'watch-finished.json').write_text(json.dumps({'time_ns':time.time_ns(),'scripts':len(seen),'errors':list(errors)}))
