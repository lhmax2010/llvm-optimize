from pathlib import Path
import subprocess,json,datetime,shlex,hashlib,sys,re
E=Path(__file__).resolve().parent
SSH=['ssh','-o','BatchMode=yes','-p','29418','lhmax2025@review.tizen.org']
REVISIONS={'1':'c5244e13258bb541458dcd4a08254217d7c556a9','2':'d0b2e82aa90b11251a13b67d890642bf2fa6f66c','3':'ecb2dec72ec5afde9c6c70f166e2ac12b47c093e'}
def now():return datetime.datetime.now().astimezone().isoformat(timespec='seconds')
def run(tag,args):
 assert not (E/(tag+'.json')).exists(),('duplicate operation refused',tag)
 p=subprocess.run(args,capture_output=True)
 (E/(tag+'.stdout')).write_bytes(p.stdout);(E/(tag+'.stderr')).write_bytes(p.stderr)
 (E/(tag+'.json')).write_text(json.dumps({'argv':args,'rc':p.returncode,'time':now()},indent=2)+'\n')
 if p.returncode:raise RuntimeError(tag+': rc='+str(p.returncode)+' '+p.stderr.decode(errors='replace'))
 return p.stdout

def query(tag,number):
 out=run(tag,SSH+['gerrit','query','--format=JSON','--current-patch-set','--patch-sets','--comments','--all-approvals','change:'+str(number)])
 rows=[r for r in map(json.loads,out.splitlines()) if 'project' in r]
 assert len(rows)==1,rows
 c=rows[0];assert c['project']=='platform/upstream/llvm' and c['branch']=='tizen_base',c
 return c

def verify_main(c):
 assert c['status']=='NEW' and str(c['currentPatchSet']['number'])=='3' and c['currentPatchSet']['revision']==REVISIONS['3'],c
 assert {str(x['number']):x['revision'] for x in c['patchSets']}==REVISIONS,c

def matches(c,n,body):
 prefix='Patch Set '+str(n)+':\n\n'
 return [x for x in c.get('comments',[]) if x.get('message')==prefix+body]

def message_action(tag,number,ps,body,abandon=False):
 # ssh joins remote arguments before the remote shell parses them.
 # Pass a single shell-quoted remote command; message remains one argv.
 words=['gerrit','review',str(number)+','+str(ps)]
 if abandon:words+=['--abandon']
 words+=['--message',body]
 command=shlex.join(words)
 assert shlex.split(command)==words
 (E/(tag+'-remote-command.txt')).write_text(command+'\n')
 (E/(tag+'-remote-argv.json')).write_text(json.dumps(words,indent=2)+'\n')
 print('EXECUTE',tag,str(number)+','+str(ps),'message_sha256='+hashlib.sha256(body.encode()).hexdigest(),flush=True)
 return run(tag,SSH+[command])

if __name__=='__main__':
 mode=sys.argv[1]
 try:
  assert json.loads((E/'text-gates.json').read_text())['PASS']
  if mode=='preflight':
   data={}
   for number in [361395,361396,361397]:
    c=query(str(number)+'-before',number);data[str(number)]=c
    if number==361395:verify_main(c)
    else:assert c['status']=='NEW' and str(c['currentPatchSet']['number'])=='1',c
   for n in [1,2,3]:assert not matches(data['361395'],n,(E/f'PS{n}-note.txt').read_text()),('note already present',n)
   (E/'preflight-PASS.json').write_text(json.dumps(data,indent=2)+'\n')
  elif mode.startswith('note'):
   n=int(mode[4:]);assert n in [1,2,3]
   assert (E/('preflight-PASS.json' if n==1 else f'note{n-1}-PASS.json')).exists()
   before=json.loads((E/('preflight-PASS.json' if n==1 else f'note{n-1}-PASS.json')).read_text())
   before=before['361395'] if n==1 else before['change']
   body=(E/f'PS{n}-note.txt').read_text()
   message_action(f'post-note{n}',361395,n,body)
   c=query(f'361395-after-note{n}',361395);verify_main(c)
   found=matches(c,n,body)
   # Exactly one new exact comment; the query itself is preserved on failure.
   assert len(found)==1 and len(matches(before,n,body))==0,('published text mismatch or duplicate',n,c.get('comments',[]))
   (E/f'note{n}-actual-message.txt').write_text(found[0]['message'])
   actual=found[0]['message'].removeprefix(f'Patch Set {n}:\n\n')
   assert actual.encode()==(E/f'PS{n}-note.txt').read_bytes()
   (E/f'note{n}-PASS.json').write_text(json.dumps({'PASS':True,'body_byte_equal':True,'only_removed_prefix':f'Patch Set {n}:\n\n','comment':found[0],'change':c},indent=2)+'\n')
  elif mode.startswith('abandon'):
   number=int(mode[7:]);assert number in [361396,361397]
   assert (E/'note3-PASS.json').exists()
   if number==361397:assert (E/'abandon361396-PASS.json').exists()
   body=(E/f'abandon-{number}.txt').read_text().removesuffix('\n')
   message_action('abandon-'+str(number),number,1,body,True)
   c=query(str(number)+'-after-abandon',number)
   assert c['status']=='ABANDONED' and str(c['currentPatchSet']['number'])=='1',c
   found=[x for x in c.get('comments',[]) if x.get('message')=='Abandoned\n\n'+body]
   assert len(found)==1,('abandon message mismatch',c.get('comments',[]))
   main=query('361395-after-abandon-'+str(number),361395);verify_main(main)
   (E/f'abandon{number}-PASS.json').write_text(json.dumps({'PASS':True,'change':c,'abandon_comment':found[0],'main_change':main},indent=2)+'\n')
  else:raise ValueError(mode)
  print('91 '+mode+' 已结束 '+now()+' status=PASS',flush=True)
 except Exception:
  print('91 '+mode+' 已结束 '+now()+' status=STOP',flush=True)
  raise
