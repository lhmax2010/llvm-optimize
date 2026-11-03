from pathlib import Path
import os,json,subprocess,time,hashlib,datetime,fcntl
E=Path(__file__).parent.resolve();plan=json.loads((E/'plan.json').read_text())
assert len(plan['items'])==10
assert 'PREPARATION FINISHED' in (E/'prepare.stdout').read_text()
assert not (E/'sudo-result.json').exists() and not (E/'askpass-count').exists()
manifest=json.loads((E/'script-hashes.json').read_text())
for name,sha in manifest.items():assert hashlib.sha256((E/name).read_bytes()).hexdigest()==sha
assert any(r.get('root_owned_probe',{}).get('stdout') for r in plan['items']), 'no root-owned target recorded'
lock=Path('/home/linhao/Toolchain/development/heavy-stage.lock').open('r')
fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
env=dict(os.environ,SUDO_ASKPASS=str(E/'askpass.sh'))
argv=['sudo','-A','-k','/bin/sh',str(E/'root-delete.sh')]
start=time.monotonic()
with (E/'sudo.stdout').open('w') as out,(E/'sudo.stderr').open('w') as err:
 p=subprocess.run(argv,env=env,stdout=out,stderr=err)
r={'argv':argv,'rc':p.returncode,'seconds':time.monotonic()-start,'one_invocation':True,'attempts':int((E/'askpass-count').read_text()) if (E/'askpass-count').exists() else 0,'root_entered':(E/'root-entry.json').exists(),'cancelled_or_dialog_error':(E/'askpass-cancelled').exists(),'time':datetime.datetime.now().astimezone().isoformat()}
(E/'sudo-result.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2),flush=True)
