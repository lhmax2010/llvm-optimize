"""Preserve completed products only; never delete a build root."""
import hashlib,json,shutil,sys,time
from pathlib import Path
D=Path(__file__).resolve().parent;label=sys.argv[1];run=sys.argv[2]
R=D/(label+'-root')/'local/BUILD-ROOTS/scratch.x86_64.0';rpm=R/'home/abuild/rpmbuild';work=rpm/'BUILD/llvm-22.1.8/build/clang-bolt'
out=D/(label+'-products');assert not out.exists(),out
result=json.loads((D/run/'result.json').read_text());assert result['exit_code']==0,result
logpath=D/run/'rpm-build.log'
if not logpath.exists():logpath=D/run/'build.log'
log=logpath.read_text(errors='replace')
for marker in ('BOLT_PIPELINE_PASS','BOLT_COMPARE_ROOT_PASS','BOLT_POST_GATE_PASS'):assert marker in log,marker
identity=json.loads((work/'identity.json').read_text())
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
candidate=work/'clang.candidate';assert sha(candidate)==identity['after_sha256']
items=[(candidate,Path('binaries/clang.candidate')),(work/'ordinary-clang-22',Path('binaries/ordinary-clang-22'))]
items += [(work/'link.original',Path('work/link.original')),(work.parent/'bin/llvm-bolt',Path('binaries/llvm-bolt'))]
for folder in ('RPMS','SRPMS'):
 ps=sorted((rpm/folder).rglob('*.rpm'));assert ps,folder
 for p in ps:items.append((p,Path(folder)/p.relative_to(rpm/folder)))
for stage in ('begin','tool-built','pipeline','post'):json.loads((work/('disk-'+stage+'.json')).read_text())
for p in work.rglob('*'):
 if p.is_file() and not p.is_symlink() and p.suffix in ('.json','.jsonl','.txt','.log','.sh'):
  items.append((p,Path('work')/p.relative_to(work)))
# Source1005 evidence is outside clang-bolt; retain its text and hashes too.
conversion=work.parent/'native-archive-conversion'
if conversion.exists():
 for p in conversion.rglob('*'):
  if p.is_file() and not p.is_symlink() and p.suffix in ('.json','.jsonl','.txt','.log'):
   items.append((p,Path('native-archive-conversion')/p.relative_to(conversion)))
for p in (work.parent/'CMakeCache.txt',work.parent/'build.ninja',work.parent/'CMakeFiles/rules.ninja'):
 items.append((p,Path('build-metadata')/p.relative_to(work.parent)))
size=sum(p.stat().st_size for p,_ in items);free=shutil.disk_usage(D).free
assert size<=10*1024**3 or free-size>=30*1024**3,(size,free)
out.mkdir();rows=[]
for src,rel in items:
 dst=out/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 before=sha(src);after=sha(dst);assert before==after,(src,dst)
 rows.append({'source':str(src),'retained':str(dst),'bytes':dst.stat().st_size,'sha256':after})
(out/'preserved.json').write_text(json.dumps({'time_ns':time.time_ns(),'source_root':str(R),'bytes':size,'candidate_sha256':identity['after_sha256'],'files':rows},indent=2)+'\n')
print(json.dumps({'preserved_files':len(rows),'bytes':size,'candidate_sha256':identity['after_sha256']},indent=2))
