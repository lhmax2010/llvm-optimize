from pathlib import Path
import os,json,re,hashlib,subprocess
from checks import command,stamp
E=Path(__file__).resolve().parent;R=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105')
P=E.parent/'disk-cleanup-20261105b/published-llvm-refs.stdout';tips=sorted({l.split()[0] for l in P.read_text().splitlines() if l.split()})
out=[]
def git(repo,args,data=None):
 p=subprocess.run(['git','--no-optional-locks','-c','safe.directory='+str(repo),'-C',str(repo),*args],input=data,capture_output=True,text=True,timeout=120)
 return {'args':args,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
for f in sorted(R.rglob('inspection-before.json')):
 d=f.parent;v=d/'verified.git';j=json.loads(f.read_text());m={'directory':str(d),'time':stamp(),'original_repository':j['path'],'head':j['head']['stdout'].strip(),'reasons':[],'patches':[],'base_source':str(P)}
 try:
  assert v.is_dir() and not v.is_symlink(),'missing/non-real readback repository'
  expected={}
  for l in (d/'SHA256SUMS').read_text().splitlines():
   h,n=l.split(None,1);expected[n.lstrip('*')]=h
  for p in [f,*sorted(d.glob('*.patch'))]:
   h=hashlib.sha256(p.read_bytes()).hexdigest();assert expected.get(p.name)==h,'SHA differs/missing '+p.name
  patches=sorted(d.glob('*.patch'));assert {p.name for p in patches}>={'unpublished.patch','index.patch','worktree.patch'},'missing required patch'
  stashes=j['stash']['stdout'].splitlines();assert len(list(d.glob('stash-*.patch')))==len(stashes),'stash export count mismatch'
  for p in patches:
   q=git(v,['apply','--numstat','--allow-empty',str(p)]);m['patches'].append({'file':p.name,'bytes':p.stat().st_size,'sha256':expected[p.name],'readcheck':q});assert q['rc']==0,'unreadable '+p.name
  seq=re.findall(r'^From ([0-9a-f]{40}) Mon Sep 17 00:00:00 2001$',(d/'unpublished.patch').read_text(),re.M);m['patch_commit_order']=seq
  assert set(seq)==set(j['effective_unpublished']),'format-patch commit coverage differs (possibly merge commit)'
  parents={}
  for sha in seq:
   q=git(v,['show','-s','--format=%P',sha]);assert q['rc']==0,'unreadable commit';parents[sha]=q['stdout'].split();assert len(parents[sha])==1,'root/merge commit: no single published base'
  base=parents[seq[0]][0] if seq else m['head'];m['series_base']=base
  for prev,sha in zip(seq,seq[1:]):assert parents[sha]==[prev],'non-linear patch history'
  if seq:assert m['head']==seq[-1],'patch series does not reconstruct original HEAD'
  q=git(v,['cat-file','--batch-check=%(objectname) %(objecttype)'],'\n'.join(tips)+'\n');assert q['rc']==0,'tip object query failed'
  present=[l.split()[0] for l in q['stdout'].splitlines() if l.split()[-1] in ('commit','tag')]
  m['published_tips_present']=present
  if not present:raise RuntimeError('no published LLVM ref object available; base availability not proven')
  q=git(v,['rev-list','--count',base,'--not',*present]);m['published_base_reachability']=q
  assert q['rc']==0 and q['stdout'].strip()=='0','base not proven reachable from 64 published LLVM refs'
  m['patch_bases']={'unpublished.patch':base,'index.patch':m['head'],'worktree.patch':m['head']+' plus index.patch'}
  if stashes:raise RuntimeError('stash parents require separate published-base proof; keep bundle conservatively')
  m['eligible']=True;m['delete_candidates']=[str(d/'repository.bundle'),str(v)]
 except Exception as ex:m['eligible']=False;m['reasons'].append(str(ex));m['delete_candidates']=[]
 out.append(m);(E/'backup-plan.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(d.relative_to(R),m['eligible'],m['reasons'],flush=True)
print('eligible',sum(x['eligible'] for x in out),'total',len(out),flush=True)
