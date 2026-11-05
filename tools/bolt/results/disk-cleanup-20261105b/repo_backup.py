"""Non-mutating Git inspection; standalone bundles and readable patch evidence."""
from pathlib import Path
import os,json,subprocess,hashlib,re,gzip
W=Path('/home/linhao/Toolchain/development/llvm-optimize');BACKUP=W/'temp/deleted-repo-backup-20261105'
def run(repo,args,**kw):
 return subprocess.run(['git','-c','pack.threads=2','-c','pack.windowMemory=64m','-c','safe.directory='+str(repo),'-c','core.fsmonitor=false','-C',str(repo),*args],env={**os.environ,'GIT_OPTIONAL_LOCKS':'0','GIT_TERMINAL_PROMPT':'0'},capture_output=True,**kw)
def inspect_backup(repo,number,target,approved):
 repo=Path(repo);r=dict(path=str(repo));queries={
 'git_dir':['rev-parse','--absolute-git-dir'], 'common_dir':['rev-parse','--path-format=absolute','--git-common-dir'],
 'head':['rev-parse','--verify','HEAD'], 'requested_unpublished':['log','--format=%H %s','--branches','--tags','--not','--remotes'],
 'all_unpublished':['rev-list','--branches','--tags','HEAD','--not','--remotes'],
 'stash':['stash','list','--format=%H%x09%gd%x09%gs'], 'status':['status','--porcelain=v1','--untracked-files=no'],
 'worktrees':['worktree','list','--porcelain']}
 for name,args in queries.items():
  p=run(repo,args);r[name]=dict(argv=args,rc=p.returncode,stdout=p.stdout.decode(errors='replace'),stderr=p.stderr.decode(errors='replace'))
  assert p.returncode==0,(repo,name,r[name])
  if name in ('requested_unpublished','all_unpublished'):
   raw=Path(__file__).parent/'git-inspection'/hashlib.sha256(str(repo).encode()).hexdigest()[:16];raw.mkdir(parents=True,exist_ok=True)
   dest=raw/(name+'.stdout.gz')
   with gzip.open(dest,'wb') as f:f.write(p.stdout)
   r[name].pop('stdout');r[name].update(stdout_gzip=str(dest),stdout_bytes=len(p.stdout),stdout_lines=len(p.stdout.splitlines()),stdout_sha256=hashlib.sha256(p.stdout).hexdigest())
 common=Path(r['common_dir']['stdout'].strip());external=[]
 if common==Path(target) or common.is_relative_to(target):
  for l in r['worktrees']['stdout'].splitlines():
   if l.startswith('worktree '):
    q=Path(l[9:]);inside=(q==Path(target) or q.is_relative_to(target))
    if q.exists() and not inside:external.append(str(q))
 r['external_worktrees_depending_on_target']=external
 if external:r['safe_to_delete']=False;r['reason']='external live worktree uses common git directory';return r
 published=Path(__file__).parent/'published-llvm-refs.stdout'
 exclusions=[]
 if published.exists():
  tips=sorted({l.split()[0] for l in published.read_text().splitlines() if l.split()})
  p=run(repo,['cat-file','--batch-check=%(objectname) %(objecttype)'],input=('\n'.join(tips)+'\n').encode());assert p.returncode==0,p.stderr
  exclusions=[l.split()[0] for l in p.stdout.decode().splitlines() if l.split()[-1] in ('commit','tag')]
 effective=['rev-list','--branches','--tags','HEAD','--not','--remotes',*exclusions]
 p=run(repo,effective);assert p.returncode==0,p.stderr;r['verified_published_tips_present']=exclusions;r['effective_unpublished']=p.stdout.decode().splitlines()
 shas=r['effective_unpublished'];assert len(shas)<1000,'too many commits to safely export as patches; preserve directory'
 stashes=[l.split('\t',2) for l in r['stash']['stdout'].splitlines()];dirty=bool(r['status']['stdout'])
 if not shas and not stashes and not dirty:r.update(safe_to_delete=True,backup=None,conclusion='无未发布内容');return r
 name=f'{number:02d}-'+Path(target).name;rel=str(repo.relative_to(target)) if repo!=Path(target) else 'root';slug=re.sub('[^A-Za-z0-9_.-]+','_',rel)[:100]+'-'+hashlib.sha256(str(repo).encode()).hexdigest()[:8];out=BACKUP/name/slug;out.mkdir(parents=True,exist_ok=False);r['backup']=str(out)
 (out/'inspection-before.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
 for name,args in [('worktree.patch',['diff','--no-ext-diff','--no-textconv','--binary','--full-index']),('index.patch',['diff','--cached','--no-ext-diff','--no-textconv','--binary','--full-index']),('unpublished.patch',['format-patch','--stdout','--binary','--full-index','--root','--branches','--tags','HEAD','--not','--remotes',*exclusions])]:
  p=run(repo,args);assert p.returncode==0,(repo,args,p.stderr.decode(errors='replace'));(out/name).write_bytes(p.stdout)
  if p.stdout:
   check=run(repo,['apply','--numstat','--allow-empty',str(out/name)]);(out/(name+'.readcheck')).write_bytes(check.stdout+check.stderr);assert check.returncode==0,(name,check.stderr)
 for i,(sha,ref,title) in enumerate(stashes):
  p=run(repo,['stash','show','--include-untracked','--binary','--patch',sha]);assert p.returncode==0,p.stderr;(out/f'stash-{i:03d}.patch').write_bytes(p.stdout)
  check=run(repo,['apply','--numstat','--allow-empty',str(out/f'stash-{i:03d}.patch')]);assert check.returncode==0,check.stderr
  p=run(repo,['show','--format=raw','--no-patch',sha]);(out/f'stash-{i:03d}.commit.txt').write_bytes(p.stdout)
 bundle=out/'repository.bundle';args=['bundle','create',str(bundle),'--all','HEAD']+[v[0] for v in stashes];p=run(repo,args);(out/'bundle-create.txt').write_bytes(p.stdout+p.stderr);assert p.returncode==0,p.stderr
 # Verify against an empty object database: no deleted source repository prerequisite.
 verify=out/'verified.git';p=subprocess.run(['git','init','--bare',str(verify)],capture_output=True);assert p.returncode==0,p.stderr
 p=run(verify,['bundle','verify',str(bundle)]);(out/'bundle-verify.txt').write_bytes(p.stdout+p.stderr);assert p.returncode==0,p.stderr
 p=run(verify,['bundle','unbundle',str(bundle)]);(out/'bundle-unbundle.txt').write_bytes(p.stdout+p.stderr);assert p.returncode==0,p.stderr
 for sha in set(shas+[r['head']['stdout'].strip()]+[x[0] for x in stashes]):
  p=run(verify,['cat-file','-e',sha+'^{commit}']);assert p.returncode==0,(sha,p.stderr)
 after=run(repo,['status','--porcelain=v1','--untracked-files=no']);assert after.stdout.decode(errors='replace')==r['status']['stdout'],'source status changed during export'
 manifest=[]
 for p in sorted(out.iterdir()):
  if p.is_file():
   with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
   manifest.append(dict(path=p.name,bytes=p.stat().st_size,sha256=h))
 (out/'SHA256SUMS').write_text(''.join(x['sha256']+'  '+x['path']+'\n' for x in manifest))
 r.update(safe_to_delete=True,unpublished_commits=len(shas),stashes=len(stashes),tracked_dirty=dirty,files=manifest,conclusion='已保全；bundle在空仓库读取并逐个确认commit，diff已解析')
 return r
