import os,json,time,shutil,math
from pathlib import Path
E=Path(__file__).resolve().parent;G=1024**3
p=E.parent/'bolt-v4-20261015-review4b/payload-merged';assert p.is_dir()
n=sz=0
for d,ds,fs in os.walk(p,onerror=lambda e:(_ for _ in ()).throw(e)):
 for f in fs:
  s=(Path(d)/f).lstat()
  if not (Path(d)/f).is_symlink():n+=1;sz+=s.st_size
old=json.loads((E/'disk-plan.json').read_text());(E/'disk-plan-provisional.json').write_text(json.dumps(old,indent=2)+'\n')
# The lower BUILDROOT was removed by prior packaging. Use the complete verified
# docs35 payload instead, rounded up, then count that entire bound twice.
bound=math.ceil(sz/G)*G;old['baseline_buildroot']={'source':str(p),'files':n,'bytes':sz,'rounded_bound':bound,'reason':'lower BUILDROOT empty; verified 22-RPM merged payload provides the bound'}
old['parts_bytes']['ordinary_buildroot']=bound;old['parts_bytes']['debuginfo_additional_bound']=bound
old['planned_write_bytes']=sum(old['parts_bytes'].values());old['free_before']=shutil.disk_usage(E).free;old['free_after_budget']=old['free_before']-old['planned_write_bytes'];old['pass']=old['free_after_budget']>=30*G
(E/'disk-plan.json').write_text(json.dumps(old,indent=2)+'\n');print(json.dumps(old,indent=2));assert old['pass']
