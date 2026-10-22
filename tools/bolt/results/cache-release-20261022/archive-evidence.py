"""Archive only this task's small logs/scripts, never the build trees or RPMs."""
from pathlib import Path
import gzip, hashlib, json, shutil, time
D=Path(__file__).resolve().parent
E=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/cache-release-20261022')
folders=['baseline-segment1','baseline-segment2','baseline-resume1','baseline-resume2','baseline-resume2-evidence','resume2-preflight','baseline-preserve','baseline-space-recovery','baseline-evidence','baseline-export','revised-export','five-parse','revised-run']
files=[D/'timeline.tsv',D/'baseline-products/preserved.json']+list(D.glob('*.py'))+list(D.glob('*command.json'))+list(D.glob('*measurement.json'))+list(D.glob('*selfcheck.json'))
for folder in folders:
 p=D/folder
 if p.is_dir(): files += [x for x in p.rglob('*') if x.is_file() and not x.is_symlink()]
rows=[]
for src in sorted(set(files)):
 rel=src.relative_to(D)
 if src.stat().st_size>100*1024**2:
  rows.append({'source':str(src),'omitted':'over 100 MiB uncompressed'});continue
 out=E/rel
 out.parent.mkdir(parents=True,exist_ok=True)
 if src.suffix=='.log':
  out=out.with_name(out.name+'.gz')
  with src.open('rb') as a,out.open('wb') as raw,gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as b:shutil.copyfileobj(a,b)
 else:shutil.copyfile(src,out)
 rows.append({'source':str(src),'artifact':str(out.relative_to(E)),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
(E/'build-evidence-provenance.json').write_text(json.dumps({'captured_at_ns':time.time_ns(),'files':rows},indent=2)+'\n')
print('Archived',len(rows),'files')
