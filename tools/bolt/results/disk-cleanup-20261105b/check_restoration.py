from pathlib import Path
import os,json,gzip,subprocess,hashlib,datetime
E=Path(__file__).parent;rows=json.loads((E/'inventory.json').read_text());out=[]
for r in rows:
 if r['number'] not in (26,28,32):continue
 for i,repo in enumerate(r['repos']):
  if not Path(repo).exists():continue
  result=dict(number=r['number'],repo=repo,checks=[])
  for label,args in [('commits',['log','--format=%H','--branches','--tags','HEAD','--not','--remotes']),('head-tree',['cat-file','-e','HEAD^{tree}']),('status',['status','--porcelain=v1','--untracked-files=no'])]:
   p=subprocess.run(['git','-c','safe.directory='+repo,'-c','core.fsmonitor=false','-C',repo,*args],env={**os.environ,'GIT_OPTIONAL_LOCKS':'0','GIT_TERMINAL_PROMPT':'0'},capture_output=True)
   file=f'restored-{r["number"]:02d}-{i}-{label}.stdout.gz'
   with gzip.open(E/file,'wb') as f:f.write(p.stdout)
   result['checks'].append(dict(argv=args,rc=p.returncode,stdout=file,lines=len(p.stdout.splitlines()),sha256=hashlib.sha256(p.stdout).hexdigest(),stderr=p.stderr.decode(errors='replace')))
  result['PASS']=all(x['rc']==0 and not x['stderr'] for x in result['checks']);out.append(result);(E/'alternates-restored-readcheck.json').write_text(json.dumps(out,indent=2)+'\n');print(repo,result['PASS'],flush=True)
refs=json.loads((E/'alternates-audit-before-restoration.json').read_text())
for r in refs:
 if 'resolved'in r:r['exists']=Path(r['resolved']).is_dir()
(E/'alternates-audit-after-restoration.json').write_text(json.dumps(refs,indent=2)+'\n')
assert all(x['PASS'] for x in out);assert all(x.get('exists',True) for x in refs)
print('ALTERNATES_READCHECK 已结束',datetime.datetime.now().astimezone().isoformat(),'status=ok',flush=True)
