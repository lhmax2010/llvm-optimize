import os,time,json,subprocess,gzip,hashlib
from pathlib import Path
E=Path(__file__).resolve().parent;N=json.loads((E/'targets.json').read_text());env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_TERMINAL_PROMPT='0',GIT_SSH_COMMAND='ssh -o BatchMode=yes -o ConnectTimeout=15')
remote_cache={}
def run(repo,args,seconds=90):
 a=['timeout',str(seconds),'nice','-n','19','ionice','-c3','git','--no-optional-locks','-c','safe.directory='+repo,'-C',repo]+args
 r=subprocess.run(a,capture_output=True,text=True,env=env);return {'argv':a,'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
def log(repo,args,path):
 r=run(repo,args,180)
 with gzip.open(path,'wt') as f:f.write(r['stdout'])
 r['count']=len(r['stdout'].splitlines());r['sample']=r['stdout'].splitlines()[:30];r.pop('stdout');r['file']=str(path.relative_to(E));return r
for n in N:
 out=E/n
 while not (out/'inventory.json').exists():time.sleep(2)
 inv=json.loads((out/'inventory.json').read_text());results=[]
 for repo in inv.get('repositories',[]):
  key=hashlib.sha256(repo.encode()).hexdigest()[:12];d=out/('git-'+key);d.mkdir(exist_ok=True);rec={'repo':repo}
  for k,args in [('head',['show','-s','--format=fuller','HEAD']),('bare',['rev-parse','--is-bare-repository']),('worktrees',['worktree','list','--porcelain']),('remotes',['remote','-v']),('remote_refs',['for-each-ref','--format=%(objectname) %(refname)','refs/remotes']),('stash',['reflog','show','--format=%H %gd %gs','refs/stash'])]:rec[k]=run(repo,args)
  if rec['bare']['stdout'].strip()!='true':
   rec['status']=run(repo,['status','--porcelain=v1','--untracked-files=no']);rec['diff_stat']=run(repo,['diff','HEAD','--stat']);rec['diff']=log(repo,['diff','HEAD','--binary'],d/'tracked-diff.patch.gz')
  rec['requested_unpublished']=log(repo,['log','--format=%H %s','--branches','--tags','--not','--remotes'],d/'requested-log.txt.gz')
  rec['with_detached']=log(repo,['log','--format=%H %s','HEAD','--branches','--tags','--not','--remotes'],d/'detached-log.txt.gz')
  urls=sorted(set(line.split()[1] for line in rec['remotes']['stdout'].splitlines() if '(fetch)' in line));rec['remote_live']=[];tips=[]
  for url in urls:
   if not url.startswith(('ssh://','https://','git@')):rec['remote_live'].append({'url':url,'status':'local remote, not publication proof'});continue
   if url not in remote_cache:
    rr=subprocess.run(['timeout','45','git','ls-remote','--heads','--tags',url],capture_output=True,text=True,env=env)
    remote_cache[url]={'url':url,'rc':rr.returncode,'stdout':rr.stdout,'stderr':rr.stderr}
   rr=remote_cache[url];rec['remote_live'].append(rr)
   if rr['rc']==0:tips+=sorted({l.split()[0] for l in rr['stdout'].splitlines() if l.strip()})
  if tips:
   rr=run(repo,['cat-file','--batch-check'],90) if False else None
   a=['git','--no-optional-locks','-c','safe.directory='+repo,'-C',repo,'cat-file','--batch-check=%(objectname) %(objecttype)']
   rr=subprocess.run(a,input='\n'.join(tips)+'\n',capture_output=True,text=True,env=env,timeout=90)
   present=[l.split()[0] for l in rr.stdout.splitlines() if l.endswith(' commit')]
   rec['present_live_tip_count']=len(present)
   if present:rec['live_unpublished']=log(repo,['log','--format=%H %s','HEAD','--branches','--tags','--not','--remotes']+present,d/'live-unpublished.txt.gz')
  # Direct read of alternates, including bare/common-git directories; do not change config.
  gd=run(repo,['rev-parse','--path-format=absolute','--git-common-dir']);rec['git_common_dir']=gd
  if gd['rc']==0:
   alt=Path(gd['stdout'].strip())/'objects/info/alternates'
   if alt.exists():rec['alternates']={'path':str(alt),'text':alt.read_text()}
  results.append(rec);(out/'git-review.json').write_text(json.dumps(results,indent=2)+'\n')
  print(n,repo,'local candidates',rec['with_detached'].get('count'),'live',rec.get('live_unpublished',{}).get('count'),flush=True)
 if not results:(out/'git-review.json').write_text('[]\n')
(E/'remote-queries.json').write_text(json.dumps(remote_cache,indent=2))
