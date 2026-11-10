from pathlib import Path
import json,urllib.request,hashlib,subprocess,datetime,sys,stat,difflib,re,traceback
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.parent/'llvm-optimize';E=Path(__file__).parent;S=W/'temp/rebase-359934-20261106/source';Q=B/'tools/bolt/results/qb-1223601-1223602'
X=W/'temp/fourth-review-20261110/resume/arm';X.mkdir()
sys.path.insert(0,str(B/'tools/bolt/night-launch-20261103'))
from rpm_io import manifest
from rpm_extract import extract_selected
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def blob(rev,path):return subprocess.check_output(['git','show',rev+':'+path],cwd=S)
orig=json.loads((Q/'rpm-downloads.json').read_text());archs=json.loads((Q/'arch-status.json').read_text())
rows=[];checks=[];status='failed'
try:
 for row in archs:
  if row['arch']=='x86_64':continue
  bid=row['build'];arch=row['arch'];d=X/bid/arch;d.mkdir(parents=True);dest=d/'payload'
  base=next(x['url'].split('/repos/')[0] for x in orig if x['build']==bid)
  selected=[r['name'] for r in row['rpms'] if re.match(r'^(llvm-devel|clang|lld|lld-devel)-[0-9]',r['name'])]
  assert len(selected)>=2,(bid,arch,selected)
  all_names=[]
  for name in selected:
   url=base+'/repos/standard/packages/'+arch+'/'+name;p=d/name
   with urllib.request.urlopen(url,timeout=120) as response,p.open('xb') as f:
    for b in iter(lambda:response.read(1048576),b''):f.write(b)
   query=subprocess.run(['rpm','-qp','--qf','%{NAME}\t%{VERSION}\t%{RELEASE}\t%{ARCH}\t%{VCS}\n',str(p)],capture_output=True,text=True)
   assert query.returncode==0,query.stderr
   assert 'fa4f9978c9162d3c6cd2113d0cfe1173f04881c8' in query.stdout,query.stdout
   m=manifest(p)
   out=E/'arm'/bid/arch;out.mkdir(parents=True,exist_ok=True)
   (out/(name+'.manifest.json')).write_text(json.dumps(m,indent=2)+'\n')
   names={n for n,v in m.items() if stat.S_ISREG(v['mode']) and re.search(r'/cmake/(llvm|clang|lld)/',n)}
   if names:extract_selected(p,names,dest)
   all_names+=list(names)
   rec=dict(build=bid,arch=arch,name=name,url=url,path=str(p),bytes=p.stat().st_size,sha256=sha(p),rpm_query=query.stdout,rpm_stderr=query.stderr,cmake_files=sorted(names))
   rows.append(rec);(E/'arm-downloads.json').write_text(json.dumps(rows,indent=2)+'\n')
   print('ARM_DOWNLOADED',bid,arch,name,rec['bytes'],flush=True)
  for filename,source in [('AddLLVM.cmake','llvm/cmake/modules/AddLLVM.cmake'),('AddClang.cmake','clang/cmake/modules/AddClang.cmake')]:
   installed=[n for n in all_names if Path(n).name==filename];assert len(installed)==1,(bid,arch,filename,installed)
   data=(dest/installed[0]).read_bytes();final=blob('fa4f9978',source);before=blob('13c3e223',source);hybrid=blob('8a50d712',source)
   check=dict(build=bid,arch=arch,file=installed[0],source=source,installed_sha256=hashlib.sha256(data).hexdigest(),fa4f9978_sha256=hashlib.sha256(final).hexdigest(),baseline_sha256=hashlib.sha256(before).hexdigest(),equals_fa4f9978=data==final,equals_hybrid=data==hybrid,diff_equal=data==final==hybrid)
   (out/filename).write_bytes(data)
   delta=''.join(difflib.unified_diff(before.decode().splitlines(True),data.decode().splitlines(True),fromfile='13c3e223/'+source,tofile=bid+'/'+installed[0]))
   (out/(filename+'.diff')).write_text(delta)
   assert check['equals_fa4f9978'] and check['equals_hybrid'] and check['diff_equal'],check
   checks.append(check)
  checks.append(dict(build=bid,arch=arch,AddLLD_installed=any(Path(n).name=='AddLLD.cmake' for n in all_names),lld_cmake_files=sorted(n for n in all_names if '/cmake/lld/' in n),packages=selected))
 status='ok'
except BaseException:
 (E/'arm-failure.txt').write_text(traceback.format_exc());raise
finally:
 (E/'arm-result.json').write_text(json.dumps(dict(status=status,checks=checks),indent=2)+'\n')
 print('ARM_CHECK 已结束',datetime.datetime.now().astimezone().isoformat(),'status='+status,flush=True)
