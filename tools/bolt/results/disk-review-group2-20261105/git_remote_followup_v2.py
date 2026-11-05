from pathlib import Path
import subprocess,json,os,gzip
E=Path(__file__).resolve().parent;env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_TERMINAL_PROMPT='0',GIT_SSH_COMMAND='ssh -o BatchMode=yes -o ConnectTimeout=15')
url='ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm'
r=subprocess.run(['timeout','60','git','ls-remote',url],capture_output=True,text=True,env=env)
with gzip.open(E/'llvm-all-remote-refs-v2.txt.gz','wt') as f:f.write(r.stdout)
(E/'llvm-all-remote-query-v2.json').write_text(json.dumps({'url':url,'rc':r.returncode,'stderr':r.stderr,'refs':len(r.stdout.splitlines())},indent=2))
tips=sorted({l.split()[0] for l in r.stdout.splitlines() if l.strip()});out=[]
for p in E.glob('*/git-review.json'):
 for row in json.loads(p.read_text()):
  repo=row['repo'];prefix=['timeout','180','nice','-n','19','ionice','-c3','git','--no-optional-locks','-c','safe.directory='+repo,'-C',repo];o={'repo':repo}
  st=subprocess.run(prefix+['for-each-ref','--format=%(objectname) %(refname)','refs/stash'],capture_output=True,text=True,env=env);o['stash_ref']={'rc':st.returncode,'stdout':st.stdout,'stderr':st.stderr}
  # Canonical LLVM remote includes review refs as well as branches/tags.
  if r.returncode==0:
   c=subprocess.run(prefix+['cat-file','--batch-check=%(objectname) %(objecttype)'],input='\n'.join(tips)+'\n',capture_output=True,text=True,env=env)
   have=[l.split()[0] for l in c.stdout.splitlines() if l.endswith(' commit')];o['remote_tip_commits_present']=len(have)
   if have:
    z=subprocess.run(prefix+['log','--format=%H %s','HEAD','--branches','--tags','--not','--remotes','--stdin'],input='\n'.join('^'+h for h in have)+'\n',capture_output=True,text=True,env=env)
    f=p.parent/('live-all-refs-v2-'+Path(repo).name+'.txt.gz')
    with gzip.open(f,'wt') as g:g.write(z.stdout)
    o['after_live_remote']={'rc':z.returncode,'count':len(z.stdout.splitlines()),'sample':z.stdout.splitlines()[:25],'stderr':z.stderr,'file':str(f.relative_to(E))}
  out.append(o)
(E/'git-remote-followup-v2.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
