from pathlib import Path
import hashlib,json,subprocess,os,stat,shutil,datetime,difflib
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.parent/'llvm-optimize';E=Path(__file__).parent/'entry';E.mkdir()
rel=Path('tools/bolt/rebase-launch-20261111-r6');src=B/rel;dst=W/rel

def run(tag,args,cwd,env=None):
 p=subprocess.run(args,cwd=cwd,env=env,capture_output=True)
 (E/(tag+'.stdout')).write_bytes(p.stdout);(E/(tag+'.stderr')).write_bytes(p.stderr)
 (E/(tag+'.json')).write_text(json.dumps({'argv':args,'cwd':str(cwd),'rc':p.returncode},indent=2)+'\n')
 assert p.returncode==0,(tag,p.returncode,p.stderr.decode(errors='replace'))
 return p.stdout

def inventory(root):
 result={}
 for p in sorted(root.rglob('*')):
  key=str(p.relative_to(root));st=p.lstat()
  row={'kind':'symlink' if p.is_symlink() else 'dir' if p.is_dir() else 'file','mode':stat.S_IMODE(st.st_mode)}
  if p.is_symlink():row['link']=os.readlink(p)
  elif p.is_file():row.update(bytes=st.st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
  result[key]=row
 return result
try:
 a=inventory(src);b=inventory(dst);differences=[{'path':n,'B':a.get(n),'W':b.get(n)} for n in sorted(set(a)|set(b)) if a.get(n)!=b.get(n)]
 (E/'all-differences-before.json').write_text(json.dumps(differences,indent=2)+'\n')
 allowed=set()
 for name,prefix in [('SHA256SUMS',''),('basedev/SHA256SUMS','basedev/')]:
  for line in (src/name).read_text().splitlines():
   sha,namepart=line.split(None,1);namepart=namepart.lstrip('*');p=Path(prefix+namepart)
   assert not p.is_absolute() and '..' not in p.parts
   assert hashlib.sha256((src/p).read_bytes()).hexdigest()==sha
   allowed.add(str(p))
 unexpected=[r for r in differences if r['path'] not in allowed or r['path'].startswith('toolchain/') or r['B'] is None or r['B']['kind']!='file' or (r['W'] and r['W']['kind']!='file')]
 print('ALL DIFFERENCES',json.dumps(differences,indent=2),flush=True)
 assert not unexpected,('STOP: differences outside authorized scope',unexpected)
 run('B-top-check',['sha256sum','-c','SHA256SUMS'],src)
 run('B-basedev-check',['sha256sum','-c','SHA256SUMS'],src/'basedev')
 backup=[]
 for row in differences:
  n=row['path'];p=dst/n;q=E/'before'/n
  if p.exists():q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);assert hashlib.sha256(q.read_bytes()).hexdigest()==row['W']['sha256']
  backup.append({'path':n,'before':row['W'],'backup':str(q) if p.exists() else None})
 (E/'backup-manifest.json').write_text(json.dumps(backup,indent=2)+'\n')
 for row in differences:
  n=row['path'];shutil.copy2(src/n,dst/n)
  assert hashlib.sha256((dst/n).read_bytes()).hexdigest()==row['B']['sha256']
 run('W-top-check',['sha256sum','-c','SHA256SUMS'],dst)
 run('W-basedev-check',['sha256sum','-c','SHA256SUMS'],dst/'basedev')
 env=dict(os.environ,SERIAL_ENTRY=str(dst),SERIAL_TEST_ROOT=str(E/'fixtures'))
 run('30-tests',['python3','-B',str(dst/'test_serial.py')],dst,env)
 stderr=(E/'30-tests.stderr').read_text();assert 'Ran 30 tests' in stderr and '\nOK\n' in stderr,stderr
 run('dry-run',['/bin/sh',str(dst/'run-night.sh'),'fea0fe464d56e17f2c7588c557bfffd9f6ac352b','--dry-run'],dst)
 assert inventory(src)==inventory(dst),'post-sync inventory differs'
 (E/'result.json').write_text(json.dumps({'status':'PASS','copied':[r['path'] for r in differences],'tests':30,'sha_checks':'both PASS','dry_run':'PASS'},indent=2)+'\n')
 print('88步骤1 已结束',datetime.datetime.now().astimezone().isoformat(),'status=PASS',flush=True)
except Exception as e:
 (E/'result.json').write_text(json.dumps({'status':'STOP','error':str(e)},indent=2)+'\n')
 print('88步骤1 已结束',datetime.datetime.now().astimezone().isoformat(),'status=STOP',flush=True)
 raise
