"""New-root validation only; run after successful build, with resource wrapper."""
import json,subprocess,time
from pathlib import Path
from validate import D,E,R,save
stages=[('sizes','validate.py'),('optional_targets','validate.py'),('linkage','validate.py'),('install','validate.py'),('installed_linkage','validate.py'),('native_smoke','runtime-validation.py'),('sdk','runtime-validation.py'),('executables','runtime-validation.py'),('objects','validate.py'),('archives','runtime-validation.py')]
rows=[]
for name,script in stages:
 argv=['python3','-B',str(D/script),name];start=time.time_ns()
 with (E/('verification-'+name+'.stdout')).open('wb') as out,(E/('verification-'+name+'.stderr')).open('wb') as err:
  rc=subprocess.run(argv,stdout=out,stderr=err).returncode
 rows.append({'stage':name,'argv':argv,'rc':rc,'start_ns':start,'end_ns':time.time_ns()});save('verification-stages.json',rows)
 print('VERIFICATION',name,'EXIT',rc,flush=True)
 if name=='install' and rc:break
cg=Path('/proc/self/cgroup').read_text().strip().split(':')[-1];c=Path('/sys/fs/cgroup')/cg.lstrip('/')
save('verification-resources-final.json',{n:(c/n).read_text() for n in ['memory.peak','memory.events','memory.swap.current','cpu.stat']})
