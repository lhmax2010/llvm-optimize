"""One authenticated cleanup; exact whitelist, root rechecks, per-path fail-closed."""
from pathlib import Path
import os,sys,json,stat,hashlib,time,subprocess,traceback,re,pwd
from checks import identity,process_snapshot,mount_snapshot,command,stamp
from repo_backup import inspect_backup
E=Path(__file__).parent;W=Path('/home/linhao/Toolchain/development/llvm-optimize');UID=1000;GID=pwd.getpwuid(UID).pw_gid
rows=json.loads((E/'inventory.json').read_text());allowed=[r['path'] for r in rows];assert sys.argv[1:]==allowed,'printed command must match exact authorized list';assert os.geteuid()==0
os.umask(0o022)
def save(p,x):Path(p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def demote():os.setgroups([]);os.setgid(GID);os.setuid(UID)
def userservices():
 env={**os.environ,'XDG_RUNTIME_DIR':'/run/user/'+str(UID),'DBUS_SESSION_BUS_ADDRESS':'unix:path=/run/user/'+str(UID)+'/bus','HOME':pwd.getpwuid(UID).pw_dir}
 def run(args):
  p=subprocess.run(['systemctl','--user',*args],env=env,preexec_fn=demote,capture_output=True,text=True,timeout=45);return dict(rc=p.returncode,stdout=p.stdout,stderr=p.stderr)
 listing=run(['list-units','--type=service','--state=active,activating,reloading,deactivating','--no-legend','--plain','--no-pager']);assert listing['rc']==0,listing
 units=[l.split()[0] for l in listing['stdout'].splitlines() if l.split()];show=run(['show',*units,'-p','Id','-p','ActiveState','-p','ExecStart','-p','WorkingDirectory','-p','RootDirectory','-p','Environment','-p','EnvironmentFiles','-p','FragmentPath','-p','BindPaths','-p','BindReadOnlyPaths']) if units else dict(rc=0,stdout='',stderr='');assert show['rc']==0,show
 # Only path references are needed from service environment; do not archive values.
 safe=[]
 for line in show['stdout'].splitlines():
  if line.startswith('Environment='):
   safe.extend('EnvironmentPathReference='+p for p in allowed if p in line)
  else:safe.append(line)
 show['stdout']='\n'.join(safe)+'\n'
 return dict(listing=listing,show=show)
def checks(target,number):
 targets=[target]+([str(Path(target).parent)] if number==2 else [])
 mounts=mount_snapshot([target]);proc=process_snapshot(targets);services=userservices();refs=[];errors=[]
 for p in Path('/proc').glob('[0-9]*/mountinfo'):
  try:refs.extend(dict(path=str(p),line=l) for l in p.read_text().splitlines() if target in l)
  except (FileNotFoundError,ProcessLookupError):pass
  except PermissionError as e:errors.append(str(e))
 r=dict(mounts=mounts,processes=proc,services=services,mountinfo_references=refs,mountinfo_errors=errors)
 assert mounts['rc']==0,'findmnt failed'
 reasons=[]
 if mounts['matches'] or refs:reasons.append('mount/overlay reference')
 if proc['matches']:reasons.append('process uses path (for item2, includes entire oldtext parent including VS Code)')
 if proc['errors'] or errors:reasons.append('root process/mountinfo inspection incomplete')
 if any(t in services['show']['stdout'] for t in targets):reasons.append('active user service references path')
 return r,reasons

def complete_inventory(target,original):
 r=dict(repos=list(original['repos']),rpms=list(original['rpms']),root_supplement_paths=[],errors=[])
 # Ordinary scan reached every readable directory. Inspect each permission-denied
 # subtree as root, including hidden repositories/RPMs; do not follow symlinks.
 for error in original.get('errors',[]):
  m=re.search(r"(?:Permission denied|Operation not permitted): '(.+)'",error)
  if not m:raise AssertionError('unclassified inventory error: '+error)
  p=Path(m[1]);assert p==Path(target) or p.is_relative_to(target);assert not p.is_symlink();r['root_supplement_paths'].append(str(p))
  def onerror(e):r['errors'].append(str(e))
  for d,ds,fs in os.walk(p,followlinks=False,onerror=onerror):
   if '.git' in ds or '.git' in fs:r['repos'].append(d)
   if 'HEAD' in fs and 'objects' in ds and 'refs' in ds:r['repos'].append(d)
   ds[:]=[n for n in ds if n!='.git' and not os.path.islink(os.path.join(d,n))]
   for n in fs:
    q=Path(d)/n
    if q.suffix=='.rpm' and not q.is_symlink():
     with q.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
     r['rpms'].append(dict(path=str(q.relative_to(target)),bytes=q.stat().st_size,sha256=h))
 assert not r['errors'],r['errors'];r['repos']=sorted(set(r['repos']));r['rpms']=list({v['path']:v for v in r['rpms']}.values());return r

results=[];save(E/'root-entry.json',dict(time=stamp(),uid=os.geteuid()));print(stamp(),'ROOT_CLEANUP_STARTED',flush=True)
for old in rows:
 n=old['number'];target=old['path'];out=E/('execution-%02d'%n);out.mkdir(exist_ok=False);r=dict(number=n,path=target,status='skipped',reason='not yet checked',time_start=stamp())
 try:
  ident=identity(target);r['identity']=ident
  assert ident.get('directory') and not ident.get('symlink') and ident['realpath']==target and not ident['parent_symlink'],'not a real exact directory'
  assert ident==old['identity'],'directory identity changed since inventory'
  audit,reasons=checks(target,n);save(out/'precheck.json',audit)
  assert not reasons,'; '.join(reasons)
  complete=complete_inventory(target,old);save(out/'complete-inventory.json',complete)
  if old['errors']:save(out/'du-root.json',command(['du','-sx','-B1',target],180))
  repos=[]
  for repo in complete['repos']:
   print(stamp(),'REPOSITORY_BACKUP',n,repo,flush=True);v=inspect_backup(repo,n,target,allowed);repos.append(v);save(out/'repositories.json',repos);assert v['safe_to_delete'],v
  if not repos:save(out/'repositories.json',[])
  r['repositories']=repos
  if n==4:
   keep=W/'temp/pgo-profiles-keep-20261102';before=json.loads((E/'profiles-before.json').read_text());after=[]
   for p in sorted(keep.rglob('*')):
    assert not p.is_symlink()
    if p.is_file():
     with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
     after.append(dict(path=str(p.relative_to(keep)),bytes=p.stat().st_size,sha256=h))
   assert after==before;assert not (Path(target)/'full/stage-A/profiles').exists();save(out/'profiles-recheck.json',dict(PASS=True,files=len(after),bytes=sum(x['bytes'] for x in after)))
  # Recheck after potentially lengthy repository exports; never remove a newly used tree.
  audit,reasons=checks(target,n);save(out/'immediate-predelete.json',audit);assert not reasons,'; '.join(reasons);assert identity(target)==ident
  assert not (W/'temp/night-20261105/toolchain').exists(),'tonight build started unexpectedly'
  before=command(['df','-B1',target]);save(out/'df-before.json',before)
  # Root is needed only for directories the ordinary account cannot traverse/remove.
  privileged=bool(old['not_user_writable_dirs'] or old['errors']);r['uid_for_rm']=0 if privileged else UID
  argv=['rm','-rf','--one-file-system','--',target];print(stamp(),'DELETE_START',n,'uid='+str(r['uid_for_rm']),target,flush=True);start=time.monotonic()
  p=subprocess.run(argv,capture_output=True,text=True,preexec_fn=None if privileged else demote)
  after=command(['df','-B1',str(Path(target).parent)]);save(out/'df-after.json',after)
  r.update(argv=argv,rc=p.returncode,stdout=p.stdout,stderr=p.stderr,seconds=time.monotonic()-start,absent=not os.path.lexists(target))
  if before['rc']==after['rc']==0:r['df_available_delta_bytes']=int(after['stdout'].splitlines()[1].split()[3])-int(before['stdout'].splitlines()[1].split()[3])
  assert p.returncode==0 and r['absent'],'rm incomplete; no retry or permission changes'
  r.update(status='deleted',reason='all checks and repository preservation passed')
 except BaseException as e:
  r['reason']=str(e);r['traceback']=traceback.format_exc();print(stamp(),'SKIP',n,r['reason'],flush=True)
 finally:
  r['time_end']=stamp();save(out/'result.json',r);results.append(r);save(E/'execution-results.json',results);print('CLEANUP_PATH 已结束',stamp(),'number='+str(n),'status='+r['status'],flush=True)
print('CLEANUP 已结束',stamp(),'status='+('ok' if all(x['status']=='deleted' for x in results) else 'partial'),'deleted='+str(sum(x['status']=='deleted' for x in results)),'skipped='+str(sum(x['status']!='deleted' for x in results)),flush=True)
