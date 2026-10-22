"""Post-measurement cleanup of only this task's first-root cache, after preservation."""
import json,os,subprocess,time,shutil,stat
from pathlib import Path
D=Path(__file__).resolve().parent;R=D/'baseline-root/local/BUILD-ROOTS/scratch.x86_64.0';C=R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache';E=D/'baseline-space-recovery'
assert D==Path('/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261022-cache-release')
assert C.resolve()==C and not C.is_symlink() and not C.parent.is_symlink() and C.is_dir()
assert C.stat().st_dev==os.stat('/home').st_dev and C.stat().st_uid==os.getuid()
assert json.loads((D/'baseline-resume2/result.json').read_text())['exit_code']==0
assert json.loads((D/'baseline-preserve/result.json').read_text())['rc']==0
saved=json.loads((D/'baseline-products/preserved.json').read_text());files=saved['files']
assert sum('/RPMS/' in x['retained'] for x in files)==22
assert sum('/SRPMS/' in x['retained'] for x in files)==1
assert saved['candidate_sha256']=='4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9'
for name in ('identity.json','disk-begin.json','disk-tool-built.json','disk-pipeline.json','disk-post.json'):assert (D/'baseline-products/work'/name).is_file(),name
checks=[]
for argv in (['lsof','-nP','+D',str(C)],['fuser','-v',str(C)]):
 p=subprocess.run(argv,capture_output=True,text=True);checks.append({'argv':argv,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==1 and not p.stdout.strip() and not p.stderr.strip(),checks[-1]
mi=Path('/proc/self/mountinfo').read_text();assert not [l for l in mi.splitlines() if l.split()[4]==str(C) or l.split()[4].startswith(str(C)+'/')]
p=subprocess.run(['df','-B1','--output=source,target',str(C)],capture_output=True,text=True,check=True);assert p.stdout.splitlines()[-1].split()==['/dev/sda1','/home'],p.stdout
u=subprocess.run(['du','-sx','-B1',str(C)],capture_output=True,text=True,check=True);size=int(u.stdout.split()[0]);before=shutil.disk_usage(D);n=sum(len(names) for _,_,names in os.walk(C))
record={'started_ns':time.time_ns(),'scope':'Only cache inside user-approved first new build root, after completed baseline and verified preservation; not production cache-release execution.','path':str(C),'file_count_before':n,'du_before':u.stdout,'allocated_bytes_before':size,'df_device':p.stdout,'filesystem_free_before':before.free,'checks':checks,'preservation_file_count':len(files),'preservation_bytes':saved['bytes'],'retained_proc':'VS Code holds proc; leave mount and rest of first root untouched.'}
(E/'preflight.json').write_text(json.dumps(record,indent=2)+'\n')
argv=['rm','-rf','--one-file-system','--',str(C)];start=time.monotonic();p=subprocess.run(argv,capture_output=True,text=True)
record.update(argv=argv,rc=p.returncode,stdout=p.stdout,stderr=p.stderr,seconds=time.monotonic()-start,remaining=C.exists(),filesystem_free_after=shutil.disk_usage(D).free)
(E/'cleanup.json').write_text(json.dumps(record,indent=2)+'\n');assert p.returncode==0 and not C.exists(),record
print(json.dumps(record,indent=2))
