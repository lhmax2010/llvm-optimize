"""One-path cleanup authorized by the user; never recurse into sibling scopes."""
from pathlib import Path
import datetime, hashlib, json, os, re, shlex, subprocess, threading, time, traceback

E=Path(__file__).resolve().parent
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
ROOT=W/'temp/bolt-v4-20261022-cache-release/revised-root'
BACKUP=ROOT.parent/'preserved-before-delete/revised-root'
LOG=W/'temp/cleanup-20261026.log'
phase='initial'; stop=threading.Event(); result={'path':str(ROOT),'status':'skipped','sudo':False}
def stamp():return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(timespec='seconds')
def log(s):
 with LOG.open('a') as f:f.write(stamp()+' '+s+'\n')
 print(s,flush=True)
def save(): (E/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
def run(argv,label,timeout=900,env=None,cwd=None):
 log('COMMAND '+shlex.join(argv));start=time.monotonic()
 with (E/(label+'.stdout')).open('w') as out,(E/(label+'.stderr')).open('w') as err:
  try:r=subprocess.run(argv,stdout=out,stderr=err,timeout=timeout,env=env,cwd=cwd);rc=r.returncode
  except subprocess.TimeoutExpired:rc=None
 data={'argv':argv,'cwd':str(cwd) if cwd else None,'rc':rc,'seconds':time.monotonic()-start}
 log(f'COMMAND END {label} rc={rc} seconds={data["seconds"]:.3f}');return data
def df(label):
 r=run(['df','-B1','/home'],label,60);assert r['rc']==0
 a=(E/(label+'.stdout')).read_text().splitlines()[-1].split()
 return {'device':a[0],'available':int(a[3]),'used':int(a[2])}
def inside(p,r):return p==r or r in p.parents
def mount_refs():
 matches={};errors=[]
 dec=lambda s:re.sub(r'\\([0-7]{3})',lambda m:chr(int(m[1],8)),s)
 for f in Path('/proc').glob('[0-9]*/mountinfo'):
  try:lines=f.read_text().splitlines()
  except FileNotFoundError:continue
  except PermissionError as e:errors.append(str(e));continue
  for line in lines:
   a=line.split();ix=a.index('-');target=Path(dec(a[4]));hits=[]
   if inside(target,ROOT):hits.append('mountpoint')
   fsroot=dec(a[3])
   if str(ROOT) in fsroot or str(ROOT).removeprefix('/home')==fsroot:hits.append('mount-root')
   if a[ix+1]=='overlay':
    for opt in a[ix+3].split(','):
     if opt.startswith(('lowerdir=','upperdir=','workdir=')):
      for v in opt.split('=',1)[1].split(':'):
       q=Path(dec(v))
       if inside(q,ROOT) or inside(ROOT,q):hits.append(opt.split('=')[0])
   if hits:matches[line]=hits
 return {'references':matches,'unreadable':errors}
def process_check(label):
 a=run(['lsof','-nP','+D',str(ROOT)],label+'-lsof')
 b=run(['fuser','-v',str(ROOT)],label+'-fuser',120)
 out=(E/(label+'-lsof.stdout')).read_text();err=(E/(label+'-lsof.stderr')).read_text()
 fout=(E/(label+'-fuser.stdout')).read_text();ferr=(E/(label+'-fuser.stderr')).read_text()
 # Preserve the same permission-visibility limitation as the previous run;
 # supplement recursive lsof with all visible processes, without publishing
 # unrelated host file names.
 c=subprocess.run(['lsof','-nP'],capture_output=True,text=True,timeout=120)
 hits=[s for s in c.stdout.splitlines() if str(ROOT) in s]
 (E/(label+'-global-project.txt')).write_text('\n'.join(hits)+('\n' if hits else ''))
 (E/(label+'-global.stderr')).write_text(c.stderr)
 unexpected=[s for s in err.splitlines() if not (s.startswith("lsof: WARNING: can't opendir(") and s.endswith('Permission denied'))]
 passed=a['rc']==1 and b['rc']==1 and not out.strip() and not fout.strip() and not ferr.strip() and not hits and not unexpected and c.returncode in (0,1)
 return {'pass':passed,'lsof':a,'fuser':b,'recursive_visibility_warnings':err,'global_matches':hits,'fuser_stdout':fout,'fuser_stderr':ferr}
def invariant():
 assert ROOT.is_dir() and ROOT.resolve()==ROOT,'missing/path realpath mismatch'
 assert not ROOT.is_symlink() and not ROOT.parent.is_symlink(),'root/parent symlink'
 device=subprocess.check_output(['df','--output=source',str(ROOT)],text=True).splitlines()[-1].strip()
 assert device=='/dev/sda1','wrong filesystem '+device
 return {'realpath':str(ROOT.resolve()),'root_symlink':False,'parent_symlink':False,'device':device,'inode':ROOT.stat().st_ino}
def main():
 global phase
 log('REVISED-ROOT FOLLOWUP START only this one path is authorized')
 result['df_initial']=df('df-initial')
 phase='verify preserved SHA256SUMS'
 old=json.loads((E.parent/'execution/preservation.json').read_text())['roots']['2']
 sums=BACKUP/'SHA256SUMS'
 assert BACKUP.resolve()==BACKUP and not BACKUP.is_symlink()
 digest=hashlib.sha256(sums.read_bytes()).hexdigest();assert digest==old['checksums']['sha256sums_sha256'],'SHA256SUMS changed'
 names=[]
 for line in sums.read_text().splitlines():
  sha,name=line.split('  ',1);p=Path(name)
  assert re.fullmatch('[0-9a-f]{64}',sha) and not p.is_absolute() and '..' not in p.parts
  assert inside((BACKUP/p).resolve(),BACKUP),'backup entry escapes directory'
  names.append(name)
 result['sha256sums']=run(['sha256sum','--check','--strict','SHA256SUMS'],'sha256sums-check',1800,cwd=BACKUP)
 result['sha256sums'].update(count=len(names),list_sha256=digest)
 assert result['sha256sums']['rc']==0,'preserved SHA256SUMS verification failed'
 for a in old['entries']:
  p=Path(a['destination']);assert p.is_file() and p.stat().st_size==a['bytes'],'missing preserved file '+str(p)
 result['preservation_entries_present']=len(old['entries']);save();log('PRESERVATION VERIFIED; no copies made')
 phase='realpath / symlink / device'
 result['path_checks']=invariant();save()
 phase='lsof +D / fuser'
 result['process_check']=process_check('before');save()
 assert result['process_check']['pass'],'process occupied or process check failed; stop without removal'
 phase='mountinfo'
 result['mount_check']=mount_refs();save();assert not result['mount_check']['references'],'mount/overlay reference; no unmount attempted'
 result['df_before_delete']=df('df-before-delete')
 result['du_before']=run(['du','-sx','-B1',str(ROOT)],'du-before')
 assert invariant()['inode']==result['path_checks']['inode'] and not mount_refs()['references']
 phase='ordinary rm'
 result['rm']=run(['rm','-rf','--one-file-system','--',str(ROOT)],'rm',3600);save()
 if ROOT.exists() or ROOT.is_symlink():
  err=(E/'rm.stderr').read_text()
  assert result['rm']['rc'] is not None and 'Permission denied' in err,'incomplete deletion not attributable to permissions'
  assert invariant()['inode']==result['path_checks']['inode'] and not mount_refs()['references']
  result['sudo_process_check']=process_check('sudo-before');save();assert result['sudo_process_check']['pass'],'occupied before sudo; stop'
  root_owned=[];walk_errors=[]
  for base,dirs,files in os.walk(ROOT,onerror=lambda e:walk_errors.append(str(e))):
   for name in dirs+files:
    q=Path(base)/name
    if q.lstat().st_uid==0:root_owned.append(str(q))
  result['root_owned_residual_count']=len(root_owned);result['residual_walk_errors']=walk_errors;save()
  assert root_owned,'permission residuals not confirmed root-owned'
  assert os.environ.get('DISPLAY') or os.environ.get('WAYLAND_DISPLAY'),'no graphical display'
  script=E/'askpass.sh'
  with os.fdopen(os.open(script,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o700),'w') as f:
   f.write('''#!/bin/sh
set -eu
unset LD_LIBRARY_PATH LD_PRELOAD GTK_PATH GIO_MODULE_DIR GDK_PIXBUF_MODULE_FILE GI_TYPELIB_PATH
set -C
if ! ( : > "$CLEANUP_ASKPASS_MARKER" ) 2>/dev/null; then exit 1; fi
exec /usr/bin/zenity --password --title='LLVM 清理：仅 revised-root'
''')
  env=os.environ.copy();env['SUDO_ASKPASS']=str(script);env['CLEANUP_ASKPASS_MARKER']=str(E/'askpass-used')
  phase='graphical sudo rm';result['sudo']=True;log('GRAPHICAL AUTH only revised-root; cancel/failure will stop')
  result['sudo_rm']=run(['sudo','-A','--','/usr/bin/rm','-rf','--one-file-system','--',str(ROOT)],'sudo-rm',3600,env=env);save()
  assert result['sudo_rm']['rc']==0,'sudo canceled/failed'
 assert not ROOT.exists() and not ROOT.is_symlink(),'path still exists'
 result['status']='ok';log('REMOVED revised-root; no sibling or parent deletion command executed')
def heartbeat():
 while not stop.wait(30):log('RUNNING phase='+phase)
if __name__=='__main__':
 assert os.geteuid()!=0
 thread=threading.Thread(target=heartbeat,daemon=True);thread.start()
 start=time.monotonic()
 try:main()
 except BaseException as e:result['reason']=repr(e);log('STOP '+repr(e));(E/'exception.txt').write_text(traceback.format_exc())
 finally:
  try:result['df_after']=df('df-after')
  finally:
   stop.set();thread.join(timeout=2);result['seconds']=time.monotonic()-start;result['path_exists']=ROOT.exists() or ROOT.is_symlink();save()
   final='CLEANUP FINISHED '+stamp()+' status='+result['status']+' path=revised-root'
   with LOG.open('a') as f:f.write(final+'\n')
   (E/'cleanup-log.txt').write_text(LOG.read_text());print(final,flush=True)
