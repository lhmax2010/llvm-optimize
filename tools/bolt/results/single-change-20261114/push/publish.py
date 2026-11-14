from gates import *
import sys,shlex
URL='ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm'
SSH=['ssh','-o','BatchMode=yes','-p','29418','lhmax2025@review.tizen.org','gerrit','query','--format=JSON','--current-patch-set','--patch-sets']
ps1='c5244e13258bb541458dcd4a08254217d7c556a9';ps2='d0b2e82aa90b11251a13b67d890642bf2fa6f66c';ps3='ecb2dec72ec5afde9c6c70f166e2ac12b47c093e'
def query(name,num):
 raw=run(name,SSH+['change:'+str(num)])
 changes=[r for r in map(json.loads,raw.splitlines()) if 'project' in r]
 assert len(changes)==1,changes
 return changes[0]
def push(name,args):
 assert not (E/(name+'.json')).exists(),'refusing duplicate attempt'
 cmd=shlex.join(args)
 (E/(name+'-command.txt')).write_text('GIT_SSH_COMMAND=\'ssh -o BatchMode=yes\' '+cmd+'\n')
 print(cmd,flush=True)
 try:
  run(name,args)
 finally:
  for ext in ['stdout','stderr']:
   p=E/(name+'.'+ext)
   if p.exists(): print(p.read_text(errors='replace'),end='',flush=True)
try:
 mode=sys.argv[1]
 if mode=='PS2':
  assert json.loads((E/'remote-preflight-PASS.json').read_text())['PASS']
  push('push-PS2',['git','-c','gc.auto=0','push',URL,ps2+':refs/for/tizen_base'])
  c=query('361395-after-PS2',361395)
  assert c['status']=='NEW' and c['branch']=='tizen_base' and c['project']=='platform/upstream/llvm'
  assert str(c['currentPatchSet']['number'])=='2' and c['currentPatchSet']['revision']==ps2,c
  (E/'PS2-remote-PASS.json').write_text(json.dumps(c,indent=2)+'\n')
 elif mode=='PS3':
  assert (E/'PS2-remote-PASS.json').is_file()
  push('push-PS3',['git','-c','gc.auto=0','push',URL,ps3+':refs/for/tizen_base'])
  c=query('361395-after-PS3',361395)
  assert c['status']=='NEW' and c['branch']=='tizen_base' and c['project']=='platform/upstream/llvm'
  assert str(c['currentPatchSet']['number'])=='3' and c['currentPatchSet']['revision']==ps3,c
  assert {str(x['number']):x['revision'] for x in c['patchSets']}=={'1':ps1,'2':ps2,'3':ps3},c
  (E/'PS3-remote-PASS.json').write_text(json.dumps(c,indent=2)+'\n')
 elif mode=='sandbox':
  assert (E/'PS3-remote-PASS.json').is_file()
  old='2cdd37ff747765e99c2befa3e6e8a88663ab77fe'
  before=run('sandbox-before',['git','ls-remote',URL,'refs/heads/sandbox/lhmax2025/bolt_pgo']).decode().split()
  assert before==[old,'refs/heads/sandbox/lhmax2025/bolt_pgo'],before
  push('push-sandbox',['git','-c','gc.auto=0','push','--force-with-lease=refs/heads/sandbox/lhmax2025/bolt_pgo:'+old,URL,ps3+':refs/heads/sandbox/lhmax2025/bolt_pgo'])
  after=run('sandbox-after',['git','ls-remote',URL,'refs/heads/sandbox/lhmax2025/bolt_pgo']).decode().split()
  assert after==[ps3,'refs/heads/sandbox/lhmax2025/bolt_pgo'],after
  other=[]
  for num in [361396,361397]:
   c=query(str(num)+'-unchanged',num);other.append(c)
   assert c['status']=='NEW' and str(c['currentPatchSet']['number'])=='1',c
  (E/'sandbox-PASS.json').write_text(json.dumps({'before':old,'after':ps3,'other_changes':other},indent=2)+'\n')
 else:raise ValueError(mode)
 print('90步骤2 '+mode+' 已结束 '+now()+' status=PASS',flush=True)
except Exception:
 print('90步骤2 已结束 '+now()+' status=STOP',flush=True)
 raise
