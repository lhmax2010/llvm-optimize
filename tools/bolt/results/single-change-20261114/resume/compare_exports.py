from pathlib import Path
import hashlib,json,difflib,datetime
E=Path(__file__).resolve().parent
root=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/single-change-20261114')
a=root/'export-old';b=root/'export-PS3'
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
 return h.hexdigest()
def manifest(root):
 return {str(p.relative_to(root)):{'bytes':p.stat().st_size,'sha256':digest(p),'mode':oct(p.stat().st_mode&0o7777)} for p in sorted(root.rglob('*')) if p.is_file()}
x=manifest(a);y=manifest(b)
(E/'export-old-manifest.json').write_text(json.dumps(x,indent=2)+'\n');(E/'export-PS3-manifest.json').write_text(json.dumps(y,indent=2)+'\n')
common=set(x)&set(y);changed=[n for n in sorted(common) if x[n]!=y[n]]
report={'status':'STOP','time':datetime.datetime.now().astimezone().isoformat(),'identical':sorted(n for n in common if x[n]==y[n]),'changed':changed,'old_only':sorted(set(x)-set(y)),'PS3_only':sorted(set(y)-set(x)),'reason':'Patch filename, Patch7 references and patch commit message change, beyond VCS/commit-ID-only expectation.'}
for name in changed:
 old=(a/name).read_text();new=(b/name).read_text()
 (E/('export-'+name.replace('/','_')+'.diff')).write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='old/'+name,tofile='PS3/'+name)))
pa=next(a.glob('0008-*.patch'));pb=next(b.glob('0008-*.patch'));aa=pa.read_bytes();bb=pb.read_bytes()
code_a=aa[aa.index(b'diff --git '):];code_b=bb[bb.index(b'diff --git '):]
report['patch0008_code_to_EOF_equal']=code_a==code_b
report['patch0008_code_sha256']={'old':hashlib.sha256(code_a).hexdigest(),'PS3':hashlib.sha256(code_b).hexdigest()}
(E/'export-0008.diff').write_text(''.join(difflib.unified_diff(aa.decode().splitlines(True),bb.decode().splitlines(True),fromfile='old/'+pa.name,tofile='PS3/'+pb.name)))
(E/'export-comparison.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
print('89步骤2 已结束 '+report['time']+' status=STOP')
