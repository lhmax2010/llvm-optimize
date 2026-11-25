"""Recover a timed-out create only after checking whether the ref exists."""
import json
import candidate as c

d=c.A/'A'
previous=c.read(d/'result.json')
tip=previous.get('test')
assert previous['status']=='STOP' and 'timed out' in previous['error'] and previous['checks'] and tip
checks=(d/'result.json').read_bytes()
(d/'first-push-result.json').write_bytes(checks)
ref='refs/heads/sandbox/lhmax2025/llvm-pgo-only-20261125'
state=c.logged(d,'timeout-ls-remote',[*c.GIT,'ls-remote','--exit-code','--heads',c.REMOTE,ref],
               expect=(0,2),timeout=60)
if state.returncode==0:
    c.require(state.stdout.split()==[tip,ref],'remote contains a different commit')
    branch=ref.removeprefix('refs/heads/')
    actual=state.stdout.strip()
else:
    c.require(not state.stdout,'unexpected ref from timeout check')
    original=c.logged
    def with_longer_push(*args,**opts):
        if args[1]=='sandbox-push':
            opts['timeout']=900
        return original(*args,**opts)
    c.logged=with_longer_push
    branch,actual=c.upload(d,'A',tip)
previous.pop('error')
previous.update(status='PASS',branch=branch,ls_remote=actual)
c.save(d/'result.json',previous)
print(json.dumps(previous,ensure_ascii=False),flush=True)
