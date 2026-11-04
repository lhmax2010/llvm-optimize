"""Delete only approved validation copies; preserve reports, inputs and all RPMs."""
from pathlib import Path
import os,stat,subprocess,json,hashlib,datetime,sys
W=Path('/home/linhao/Toolchain/development/llvm-optimize');E=Path(__file__).parent
N=W/'temp/night-20261103'
SCOPES=[(N/'toolchain/validation-02/rpm-bytes','payload'),(N/'toolchain/validation-02/objects','objects'),(N/'basedev/validation-02/payload','payload'),(N/'basedev/validation-02/objects','objects'),(N/'basedev/validation-02/release-check-resume/payload','payload'),(W/'temp/night-revalidation-20261104-tests-05','fixture')]
PROTECT=('.json','.txt','.log','.stdout','.stderr','.rpm','.gz','.xz')
def now():return datetime.datetime.now().astimezone().isoformat()
def save(n,x): (E/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def command(argv):
 p=subprocess.run(argv,capture_output=True,text=True);return dict(argv=argv,rc=p.returncode,stdout=p.stdout,stderr=p.stderr)
def digest(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def files(root):
 for base,dirs,names in os.walk(root,followlinks=False):
  for d in list(dirs):
   p=Path(base)/d
   if p.is_symlink():dirs.remove(d);yield p
  for n in names:yield Path(base)/n

def plan():
 rows=[]
 for root,kind in SCOPES:
  assert root.is_dir() and not root.is_symlink() and root.resolve()==root
  du=command(['timeout','60','nice','-n','19','ionice','-c3','du','-sx','-B1',str(root)]);entries=[];kept=[]
  for p in files(root):
   st=p.lstat();assert stat.S_ISREG(st.st_mode) or stat.S_ISLNK(st.st_mode),(p,st.st_mode)
   protected=p.name.endswith(PROTECT)
   selected=not protected and (kind=='payload' or (kind=='objects' and (p.suffix=='.o' or p==root/'clang-22')) or (kind=='fixture' and p.parent==root and p.suffix in ('.debug','.clang')))
   record=dict(path=str(p),bytes=st.st_size,allocated_bytes=st.st_blocks*512,device=st.st_dev,inode=st.st_ino,mtime_ns=st.st_mtime_ns,mode=st.st_mode)
   if selected:entries.append(record)
   else:
    if stat.S_ISREG(st.st_mode):record['sha256']=digest(p)
    else:record['target']=os.readlink(p)
    kept.append(record)
  rows.append(dict(root=str(root),kind=kind,du=du,delete=entries,preserve=kept))
 save('cleanup-plan.json',dict(time=now(),df=command(['df','-B1','/home']),scopes=rows));print('planned',sum(len(x['delete']) for x in rows),'files',sum(v['allocated_bytes'] for x in rows for v in x['delete']),'allocated bytes')

def execute():
 plan=json.loads((E/'cleanup-plan.json').read_text());rows=[]
 mounts=command(['findmnt','-rn','-o','TARGET,FSTYPE,OPTIONS']);save('mounts-before.json',mounts)
 for scope in plan['scopes']:
  root=Path(scope['root']);assert (root,scope['kind']) in SCOPES
  row=dict(root=str(root),start=now(),df_before=command(['df','-B1','/home']),status='skipped')
  check=command(['timeout','90','lsof','-nP','+D',str(root)]);row['lsof']=check
  hits=[];unreadable=0
  for pid in Path('/proc').glob('[0-9]*'):
   for q in [pid/'cwd',pid/'root',*list((pid/'fd').glob('*'))]:
    try:target=os.readlink(q).removesuffix(' (deleted)')
    except OSError:unreadable+=1;continue
    if target==str(root) or target.startswith(str(root)+'/'):hits.append(dict(pid=pid.name,link=str(q),target=target))
  row['proc_hits']=hits;row['unreadable_proc_links']=unreadable
  mounted=any(line.split(' ',1)[0]==str(root) or line.split(' ',1)[0].startswith(str(root)+'/') for line in mounts['stdout'].splitlines());row['mounted']=mounted
  if check['rc']!=1 or check['stdout'].strip() or hits or mounted:
   row['reason']='open files, mount, or inconclusive lsof';rows.append(row);save('cleanup-result.json',rows);continue
  # Recheck every inode/path before deletion; retain all report files and RPMs.
  for f in scope['delete']:
   p=Path(f['path']);s=p.lstat();assert (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns)==(f['device'],f['inode'],f['bytes'],f['mtime_ns']),p
  row['commands']=[]
  try:
   for start in range(0,len(scope['delete']),100):
    paths=[f['path'] for f in scope['delete'][start:start+100]]
    c=command(['rm','--',*paths]);row['commands'].append(c)
    if c['rc']:raise RuntimeError('ordinary-user rm failed; no sudo retry')
   assert all(not os.path.lexists(f['path']) for f in scope['delete'])
   for f in scope['preserve']:
    p=Path(f['path']);s=p.lstat();assert (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns)==(f['device'],f['inode'],f['bytes'],f['mtime_ns']),p
    if 'sha256' in f:assert digest(p)==f['sha256'],p
    else:assert os.readlink(p)==f['target']
   row['status']='deleted-copies-reports-preserved'
  except BaseException as e:
   row['status']='failed';row['reason']=repr(e);rows.append(row);save('cleanup-result.json',rows);raise
  row['df_after']=command(['df','-B1','/home']);row['end']=now();rows.append(row);save('cleanup-result.json',rows)
 save('cleanup-final-df.json',command(['df','-B1','/home']));print('cleanup complete',[(x['root'],x['status']) for x in rows])
if __name__=='__main__':{'plan':plan,'execute':execute}[sys.argv[1]]()
