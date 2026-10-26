"""Authorized preservation only. No removal or changes to source files."""
from pathlib import Path
import collections, datetime, hashlib, json, os, shutil, subprocess, threading, time, traceback

E = Path(__file__).resolve().parent
I = E.parent
W = Path('/home/linhao/Toolchain/development/llvm-optimize')
T = W / 'temp'
LOG = T / 'cleanup-20261026.log'
PATHS = [
 T/'bolt-v4-20261022-cache-release/baseline-root',
 T/'bolt-v4-20261022-cache-release/revised-root',
 T/'hybrid-local-20261023/gbs-root',
 T/'bolt-on-hybrid-20261024/gbs-root',
 Path('/var/tmp/llvm-optimize-x86-archivefix-20261013/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache'),
 T/'bolt-v4-20261016-source-order/upper-parse',
 T/'toolchain-archivefix-v2-final', T/'toolchain-llvm-strip', T/'toolchain-release-x86-20261013',
 Path('/var/tmp/llvm-optimize-archivefix-v2-final-20261009/independent-install')]
phase = 'initial'; stop = threading.Event(); cache = {}; result = {'roots':{}, 'runtime':{}, 'rpm_sets':{}}

def stamp(): return datetime.datetime.now().astimezone().isoformat(timespec='seconds')
def log(message):
 with LOG.open('a') as f: f.write(stamp()+' '+message+'\n'); f.flush()
 print(message, flush=True)
def save(name, data): (E/name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
def inside(p, root): return p==root or root in p.parents
def hashed(p):
 p=Path(p); s=p.stat(); key=(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
 if key not in cache:
  h=hashlib.sha256()
  with p.open('rb') as f:
   while b:=f.read(4*1024**2): h.update(b)
  z=p.stat(); assert (z.st_dev,z.st_ino,z.st_size,z.st_mtime_ns,z.st_ctime_ns)==key, 'changed while reading '+str(p)
  cache[key]=h.hexdigest()
 return cache[key]
def copy_verify(src,dst,expected=None):
 src=Path(src);dst=Path(dst);sha=hashed(src)
 if expected: assert sha==expected, 'inventory SHA mismatch '+str(src)
 assert not any(inside(dst,r) for r in PATHS)
 assert not dst.is_symlink()
 dst.parent.mkdir(parents=True,exist_ok=True)
 if not dst.exists(): shutil.copy2(src,dst,follow_symlinks=True)
 assert hashed(dst)==sha,'copy SHA mismatch '+str(dst)
 return {'source':str(src),'destination':str(dst),'bytes':src.stat().st_size,'sha256':sha}
def sums(directory):
 rows=[]; links=[]
 for p in sorted(directory.rglob('*')):
  if p.name=='SHA256SUMS':continue
  if p.is_symlink(): links.append({'path':str(p.relative_to(directory)),'target':os.readlink(p)})
  elif p.is_file():rows.append(hashed(p)+'  '+str(p.relative_to(directory)))
 (directory/'SHA256SUMS').write_text('\n'.join(rows)+'\n')
 return {'root':str(directory),'files':len(rows),'symlinks':links,'sha256sums_sha256':hashed(directory/'SHA256SUMS')}
def heartbeat():
 while not stop.wait(30):log('RUNNING phase='+phase)

def main():
 global phase
 save('approved-paths.json',[str(p) for p in PATHS])
 df=subprocess.run(['df','-B1','/home','/var/tmp'],capture_output=True,text=True,check=True)
 (E/'df-before-preservation.txt').write_text(df.stdout)
 entries=json.loads((I/'preserve-before-delete.json').read_text())
 for number,root in enumerate(PATHS[:4],1):
  phase=f'preserve item={number}'
  rows=[];dest=root.parent/'preserved-before-delete'/root.name
  log(phase+' START path='+str(root))
  try:
   assert root.resolve()==root and not root.is_symlink() and not root.parent.is_symlink()
   selected=[a for a in entries if inside(Path(a['path']),root)]
   assert selected,'empty preservation selection'
   for k,a in enumerate(selected,1):
    src=Path(a['path']);sha=hashed(src)
    if a.get('sha256'):assert sha==a['sha256'],'source changed '+str(src)
    existing=None
    if a['action']=='already preserved':
     for candidate in a['same_sha_outside_plan']:
      p=Path(candidate)
      if any(inside(p,r) or inside(p.resolve(),r) for r in PATHS):continue
      if p.is_file() and hashed(p)==sha:existing=str(p);break
     assert existing,'no verified surviving duplicate '+str(src)
    if existing:rows.append({'source':str(src),'destination':existing,'sha256':sha,'bytes':src.stat().st_size,'action':'verified existing copy'})
    else:rows.append(dict(copy_verify(src,dest/src.relative_to(root),sha),action='copied'))
    if k%40==0:log(phase+f' progress={k}/{len(selected)}')
   dest.mkdir(parents=True,exist_ok=True)
   (dest/'preservation-manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
   checksum=sums(dest)
   result['roots'][str(number)]={'status':'PASS','path':str(root),'entries':rows,'checksums':checksum}
   log(phase+f' PASS entries={len(rows)} copied={sum(x["action"]=="copied" for x in rows)}')
  except Exception as e:
   result['roots'][str(number)]={'status':'FAIL','path':str(root),'error':repr(e),'entries':rows}
   log(phase+' FAILED will skip deletion: '+repr(e))
  save('preservation.json',result)
 phase='perf-runtime'
 try:
  manifest=json.loads((I/'runtime-preservation.json').read_text());root=Path(manifest['root']);resource=Path(manifest['resource'])
  dest=T/'bolt-on-hybrid-20261024/perf-runtime';assert not dest.exists(),'runtime destination already exists'
  dest.mkdir();rows=[];links=[]
  # Preserve the usr-merge directory symlink, not just its resolved files.
  lib=root/'lib64';assert lib.is_symlink();target=os.readlink(lib);assert not target.startswith('/') and (root/target).resolve()==(root/'usr/lib64').resolve()
  (dest/'usr/lib64').mkdir(parents=True);(dest/'lib64').symlink_to(target);links.append({'path':'lib64','target':target})
  source_files={str(p) for p in resource.rglob('*') if p.is_file() or p.is_symlink()}
  expected_files={a['path'] for a in manifest['files'] if inside(Path(a['path']),resource)}
  assert source_files==expected_files,'resource file set changed'
  for a in manifest['files']:
   src=Path(a['path']);resolved=Path(a['resolved']);sha=a['sha256']
   assert src.resolve()==resolved and hashed(src)==sha
   if inside(src,resource):
    out=dest/'resource-dir'/src.relative_to(resource)
    assert not src.is_symlink(),'unexpected resource symlink'
    rows.append(copy_verify(src,out,sha))
   else:
    rows.append(copy_verify(resolved,dest/resolved.relative_to(root),sha))
    real_parent=src.parent.resolve();linksrc=real_parent/src.name
    if linksrc.is_symlink():
     target=os.readlink(linksrc);assert not target.startswith('/')
     out=dest/linksrc.relative_to(root)
     if not out.is_symlink():out.symlink_to(target)
     assert os.readlink(out)==target and hashed(out)==sha
     links.append({'path':str(out.relative_to(dest)),'target':target})
    assert hashed(dest/src.relative_to(root))==sha
  (dest/'README.md').write_text('# 34号性能测量运行环境保全\n\n以后重跑34号测量，须把loader、运行库和resource-dir指向本目录：\n\n- loader: `lib64/ld-linux-x86-64.so.2`\n- library path: `lib64`（保留`lib64 -> usr/lib64`及库自身相对符号链接）\n- clang resource-dir: `resource-dir`\n\n源自 hybrid+BOLT gbs-root；8个运行库和完整build/lib64/clang/22已按runtime-preservation.json核对SHA。源码、products与原测量脚本均未修改。\n')
  (dest/'preservation-manifest.json').write_text(json.dumps({'files':rows,'symlinks':links},ensure_ascii=False,indent=2)+'\n')
  result['runtime']={'status':'PASS','files':rows,'symlinks':links,'checksums':sums(dest)}
  log(phase+' PASS files='+str(len(rows)))
 except Exception as e:
  result['runtime']={'status':'FAIL','error':repr(e)};log(phase+' FAILED item=4 will be skipped: '+repr(e))
 save('preservation.json',result)
 original=json.loads((I/'payload-original-rpm-sets.json').read_text())
 for key,group in original.items():
  phase='verify original RPM '+key;log(phase+' START');rows=[]
  try:
   assert len(group['files'])==22
   for a in group['files']:
    p=Path(a['path']);sha=hashed(p);assert sha==a['sha256'],'original RPM changed '+str(p)
    rows.append({'path':str(p),'bytes':p.stat().st_size,'sha256':sha})
    log(phase+f' {len(rows)}/22 '+p.name)
   result['rpm_sets'][key]={'status':'PASS','files':rows};log(phase+' PASS 22/22')
  except Exception as e:
   result['rpm_sets'][key]={'status':'FAIL','files':rows,'error':repr(e)};log(phase+' FAILED '+repr(e))
  save('preservation.json',result)
 phase='preservation complete; deletion checks pending';log('PRESERVATION FINISHED; no deletion yet')

if __name__=='__main__':
 threading.Thread(target=heartbeat,daemon=True).start()
 try:main()
 except BaseException:
  log('PRESERVATION FATAL '+traceback.format_exc());log('CLEANUP FINISHED '+stamp()+' status=failed deleted=0 skipped=10');raise
 finally:stop.set()
