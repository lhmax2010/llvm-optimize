import os,json,subprocess,hashlib,shutil,time
from pathlib import Path
E=Path(__file__).resolve().parent;W=E.parents[1];S=W/'temp/bolt-v4-20261013/v41/llvm-source';L=W/'temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0';P=L/'home/abuild/rpmbuild/BUILD/llvm-22.1.8';G=1024**3
sha='506dc25c86e4e2154150796d10b77b71d71ad6bb'
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024**2),b''):h.update(b)
 return h.hexdigest()
def measure(root):
 n=sz=blocks=0
 for d,ds,fs in os.walk(root,onerror=lambda e:(_ for _ in ()).throw(e)):
  for name in fs:
   p=Path(d)/name;s=p.lstat()
   if p.is_file() and not p.is_symlink():n+=1;sz+=s.st_size;blocks+=s.st_blocks*512
 return {'files':n,'bytes':sz,'allocated':blocks}
(E/'inputs').mkdir();rows=[]
for name in ['llvm.spec','clang-bolt-helper.py','clang-bolt-v2.fdata.xz','llvm-static-archives-native.py']:
 data=subprocess.check_output(['git','-C',str(S),'show',sha+':packaging/'+name]);p=E/'inputs'/name;p.write_bytes(data);rows.append({'source':'git:'+sha+':packaging/'+name,'name':name,'bytes':len(data),'sha256':digest(p)})
for name in ['llvm-22.1.8.tar.gz','llvm.manifest','mlgo_arm_model.tar.gz','mlgo_aarch_model.tar.gz','mlgo_x86_model.tar.gz']:
 p=L/'home/abuild/rpmbuild/SOURCES'/name
 assert p.is_file(),str(p)
 rows.append({'source':str(p),'name':name,'bytes':p.stat().st_size,'sha256':digest(p),'reuse_existing_lower':True})
(E/'source-inputs.json').write_text(json.dumps(rows,indent=2)+'\n')
# docs38 installed payload bounds from the completed BUILDROOT, and measured cache.
baseline=measure(L/'home/abuild/rpmbuild/BUILDROOT');cache=measure(P/'build/lto.cache');archives=measure(P/'build/lib64')
# Ordinary reinstall + a full extra debuginfo copy (conservative); archive copy-up
# and converter intermediates; 110 GiB cold ThinLTO allowance; 24 GiB BOLT work.
parts={'ordinary_buildroot':baseline['bytes'],'debuginfo_additional_bound':baseline['bytes'],'archive_copyup_and_conversion':2*archives['bytes'],'thinlto_new_and_copyup':110*G+cache['bytes'],'bolt_build_rewrite_logs':24*G}
free=shutil.disk_usage(E).free;budget=sum(parts.values());r={'time':time.time(),'baseline_buildroot':baseline,'build_lib64':archives,'cache':cache,'parts_bytes':parts,'planned_write_bytes':budget,'free_before':free,'floor':30*G,'free_after_budget':free-budget,'pass':free-budget>=30*G,'caveat':'Conservative measured bound, not a reservation; runtime abort if filesystem free <30 GiB. No lower files are removed.'}
(E/'disk-plan.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
assert r['pass'],'disk admission failed; skip B'
