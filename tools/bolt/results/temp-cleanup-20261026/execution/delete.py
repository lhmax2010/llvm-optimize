"""Execute only the ten user-approved paths; fail closed on path/use checks."""
from pathlib import Path
import datetime, json, os, re, shlex, signal, subprocess, threading, time, traceback
import preserve as p

E=p.E; phase='prechecks'; stop=threading.Event(); results=[]
ASKPASS=E/'askpass-cleanup.sh'

def command(argv,label,timeout=900,env=None):
 p.log('COMMAND '+shlex.join(argv))
 start=time.monotonic()
 with (E/(label+'.stdout')).open('w') as out,(E/(label+'.stderr')).open('w') as err:
  try:
   c=subprocess.run(argv,stdout=out,stderr=err,timeout=timeout,env=env)
   result={'argv':argv,'rc':c.returncode,'seconds':time.monotonic()-start}
  except subprocess.TimeoutExpired:result={'argv':argv,'rc':None,'seconds':time.monotonic()-start,'error':'timeout'}
 p.log(f'COMMAND END label={label} rc={result["rc"]} seconds={result["seconds"]:.3f}')
 result.update(stdout=str(E/(label+'.stdout')),stderr=str(E/(label+'.stderr')))
 return result

def df(label):
 r=command(['df','-B1','/home','/var/tmp'],label,60)
 assert r['rc']==0
 values={}
 for line in Path(r['stdout']).read_text().splitlines()[1:]:
  x=line.split();values[x[-1]]={'device':x[0],'available':int(x[3]),'used':int(x[2])}
 return values

def unescape(s):return re.sub(r'\\([0-7]{3})',lambda m:chr(int(m[1],8)),s)
def mounts(root):
 matches={}; errors=[]
 for f in Path('/proc').glob('[0-9]*/mountinfo'):
  try:lines=f.read_text().splitlines()
  except FileNotFoundError:continue
  except PermissionError as e:errors.append(str(e));continue
  for line in lines:
   a=line.split();mid=a.index('-');target=Path(unescape(a[4]));kind=a[mid+1];hits=[]
   if p.inside(target,root):hits.append('mountpoint')
   if kind=='overlay':
    for opt in a[mid+3].split(','):
     if opt.startswith(('lowerdir=','upperdir=','workdir=')):
      for q in opt.split('=',1)[1].split(':'):
       q=Path(unescape(q))
       if p.inside(root,q) or p.inside(q,root):hits.append(opt.split('=')[0])
   # mount root can also expose a bind-mounted part of the requested directory.
   fsroot=unescape(a[3])
   if str(root) in fsroot or str(root).removeprefix('/home')==fsroot: hits.append('mount-root')
   if hits:matches[line]={'target':str(target),'fstype':kind,'hits':hits,'pids':matches.get(line,{}).get('pids',[])+[f.parent.name]}
 return {'references':[dict(raw=k,**v) for k,v in matches.items()],'unreadable_mountinfo':errors}

def processes(root,label):
 a=command(['lsof','-nP','+D',str(root)],label+'-lsof',900)
 b=command(['fuser','-v',str(root)],label+'-fuser',120)
 # +D cannot traverse a few root-only system directories; supplement it with
 # the full visible process list, retaining only lines inside this exact root.
 c=subprocess.run(['lsof','-nP'],capture_output=True,text=True,timeout=120)
 hits=[s for s in c.stdout.splitlines() if str(root) in s]
 (E/(label+'-lsof-global-project.txt')).write_text('\n'.join(hits)+('\n' if hits else ''))
 (E/(label+'-lsof-global.stderr')).write_text(c.stderr)
 aout=Path(a['stdout']).read_text();bout=Path(b['stdout']).read_text();berr=Path(b['stderr']).read_text()
 warnings=Path(a['stderr']).read_text()
 badwarn=[s for s in warnings.splitlines() if not (s.startswith('lsof: WARNING: can\'t opendir(') and s.endswith('Permission denied'))]
 ok=a['rc']==1 and not aout.strip() and b['rc']==1 and not bout.strip() and not berr.strip() and not hits and c.returncode in (0,1) and not badwarn
 return {'pass':ok,'lsof':a,'fuser':b,'global_matches':hits,'permission_visibility_warnings':warnings,'unexpected_warnings':badwarn,'global_lsof_rc':c.returncode}

def sudo_env(i):
 env=os.environ.copy();env['SUDO_ASKPASS']=str(ASKPASS);env['CLEANUP_ASKPASS_MARKER']=str(E/f'askpass-used-{i}')
 return env

def check(root,i):
 r={'path':str(root),'number':i}
 assert root in p.PATHS and root.is_dir() and not root.is_symlink() and not root.parent.is_symlink()
 assert root.resolve()==root,'realpath mismatch'
 expected='/dev/sda1' if i in (1,2,3,4,6,7,8,9) else '/dev/nvme0n1p1'
 device=subprocess.check_output(['df','--output=source',str(root)],text=True).splitlines()[-1].strip()
 assert device==expected,f'device mismatch {device} != {expected}'
 r.update(realpath=str(root.resolve()),device=device,root_inode=root.stat().st_ino)
 r['processes']=processes(root,f'item-{i}-before')
 assert r['processes']['pass'],'process use/error; see lsof/fuser'
 r['mounts']=mounts(root);p.save(f'item-{i}-mounts.json',r['mounts'])
 if r['mounts']['references']:
  # Never unmount overlays or anything outside the approved new build roots.
  assert i<=4,'mount/overlay reference'
  refs=r['mounts']['references'];own={x.split()[4] for x in Path('/proc/self/mountinfo').read_text().splitlines()}
  for x in refs:
   assert x['hits']==['mountpoint'] and x['fstype'] in ('proc','devpts','tmpfs','devtmpfs'),'unexpected mount/overlay reference'
   assert x['target'] in own,'mount exists in another namespace'
   assert x['target'].endswith(('/proc','/dev','/dev/pts','/dev/shm')),'unexpected mount target'
  for j,target in enumerate(sorted({x['target'] for x in refs},key=len,reverse=True)):
   u=command(['umount','--',target],f'item-{i}-umount-{j}',120)
   if u['rc']!=0:
    u=command(['sudo','-A','--','/usr/bin/umount','--',target],f'item-{i}-sudo-umount-{j}',300,sudo_env(i))
   assert u['rc']==0,'normal umount failed or busy'
  r['mounts_after']=mounts(root);assert not r['mounts_after']['references'],'residual mount references'
 r['pass']=True
 return r

def main():
 global phase
 preservation=json.loads((E/'preservation.json').read_text())
 original=json.loads((p.I/'payload-original-rpm-sets.json').read_text())
 initial=df('df-before-deletion');p.save('filesystem-before-deletion.json',initial)
 for i,root in enumerate(p.PATHS,1):
  phase=f'item={i} precheck';r={'number':i,'path':str(root),'status':'skipped','sudo':False};start=time.monotonic()
  p.log(phase+' START '+str(root))
  try:
   if i<=4:assert preservation['roots'][str(i)]['status']=='PASS','preservation failed'
   if i==4:assert preservation['runtime']['status']=='PASS','perf-runtime preservation failed'
   group={7:'docs35',8:'docs38',9:'docs49',10:'docs35'}.get(i)
   if group:
    assert preservation['rpm_sets'][group]['status']=='PASS','original RPM SHA failed'
    for a in original[group]['files']:assert p.hashed(a['path'])==a['sha256'],'original RPM changed before deletion'
    r['rpm_set']=group
   r['checks']=check(root,i);p.save(f'item-{i}-checks.json',r['checks'])
   r['df_before']=df(f'item-{i}-df-before')
   r['du_before']=command(['du','-sx','-B1',str(root)],f'item-{i}-du-before',900)
   phase=f'item={i} ordinary rm'
   # Recheck path and all mounts after scanning, immediately before mutation.
   assert root.resolve()==root and root.stat().st_ino==r['checks']['root_inode']
   assert not mounts(root)['references'],'mount appeared before removal'
   r['rm']=command(['rm','-rf','--one-file-system','--',str(root)],f'item-{i}-rm',3600)
   if root.exists() or root.is_symlink():
    stderr=Path(r['rm']['stderr']).read_text()
    assert r['rm']['rc'] is not None and 'Permission denied' in stderr,'removal incomplete for a non-permission reason'
    # No chmod, lazy/forced unmount, alternate paths, or broader parent removal.
    assert root.resolve()==root and not root.is_symlink() and not root.parent.is_symlink()
    assert root.stat().st_ino==r['checks']['root_inode'] and not mounts(root)['references']
    r['sudo_process_recheck']=processes(root,f'item-{i}-sudo-before')
    assert r['sudo_process_recheck']['pass'],'new process use before sudo'
    phase=f'item={i} graphical sudo rm';p.log('GRAPHICAL PASSWORD may appear; only authorized exact path '+str(root))
    r['sudo']=True
    r['sudo_rm']=command(['sudo','-A','--','/usr/bin/rm','-rf','--one-file-system','--',str(root)],f'item-{i}-sudo-rm',3600,sudo_env(i))
    assert r['sudo_rm']['rc']==0,'sudo canceled/authentication/removal failed'
   assert not root.exists() and not root.is_symlink(),'path still exists'
   r['status']='deleted';p.log(f'item={i} DELETED '+str(root))
  except Exception as e:
   r['reason']=repr(e);r['remaining']=root.exists() or root.is_symlink();p.log(f'item={i} SKIPPED '+repr(e))
  finally:
   r['seconds']=time.monotonic()-start;r['df_after']=df(f'item-{i}-df-after');results.append(r);p.save('deletion-results.json',results)
 phase='final verification';final=df('df-after-cleanup');p.save('filesystem-after-cleanup.json',final)
 p.log('DELETION LOOP COMPLETE')

def heartbeat():
 while not stop.wait(30):p.log('RUNNING phase='+phase)

if __name__=='__main__':
 assert os.geteuid()!=0,'controller must remain ordinary user'
 assert os.environ.get('DISPLAY') or os.environ.get('WAYLAND_DISPLAY'),'no graphical session'
 # Create a new executable askpass wrapper; no existing file permissions change.
 ask='''#!/bin/sh
set -eu
unset LD_LIBRARY_PATH LD_PRELOAD GTK_PATH GIO_MODULE_DIR GDK_PIXBUF_MODULE_FILE GI_TYPELIB_PATH
set -C
if ! ( : > "$CLEANUP_ASKPASS_MARKER" ) 2>/dev/null; then exit 1; fi
exec /usr/bin/zenity --password --title='LLVM 清理：仅删除用户批准的精确目录'
'''
 with os.fdopen(os.open(ASKPASS,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o700),'w') as f:f.write(ask)
 threading.Thread(target=heartbeat,daemon=True).start();fatal=False
 try:main()
 except BaseException:
  fatal=True;p.log('CLEANUP FATAL '+traceback.format_exc());raise
 finally:
  stop.set();deleted=sum(r['status']=='deleted' for r in results);status='all-done' if deleted==10 else 'partial' if deleted or any('rm' in r for r in results) else 'failed'
  p.save('deletion-results.json',results)
  p.log('CLEANUP FINISHED '+p.stamp()+f' status={status} deleted={deleted} skipped={10-deleted}')
