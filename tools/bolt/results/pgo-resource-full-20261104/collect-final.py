"""Collect finished experiment evidence; never restart, stop, or change products."""
from pathlib import Path
import json,subprocess,hashlib,gzip,shutil,datetime,os
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');E=Path(__file__).parent
D=B.parent/'llvm-optimize/temp/pgo-resource-20261102/full'
with (D/'controller.stdout').open() as f:ends=[l.rstrip('\n') for l in f if l.startswith('PGO_RESOURCE 已结束 ')]
assert ends,'no controller end marker; do not summarize unfinished run'
cmd=['python3','-B',str(B/'tools/bolt/pgo-resource-20261102/report.py'),str(D)]
with (E/'report.stdout').open('xb') as o,(E/'report.stderr').open('xb') as e:p=subprocess.run(cmd,stdout=o,stderr=e)
(E/'report-command.json').write_text(json.dumps(dict(argv=cmd,rc=p.returncode),indent=2)+'\n');assert p.returncode==0
out=E/'full';out.mkdir(exist_ok=False);rows=[]
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
files=[p for p in D.iterdir() if p.is_file()]
for directory in D.glob('stage-*/evidence'):
 files.extend(p for p in directory.rglob('*') if p.is_file() and not p.is_symlink())
files.extend(D.glob('stage-*/training-commands.json'))
files.extend(D.glob('stage-D/gbs-driver/local/repos/*/x86_64/logs/fail/*/log.txt'))
work=D/'stage-D/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt'
if work.exists():
 files.extend(p for p in work.rglob('*') if p.is_file() and not p.is_symlink() and p.suffix in ('.json','.log','.txt','.sh'))
for src in sorted(files):
 dest=out/src.relative_to(D);dest.parent.mkdir(parents=True,exist_ok=True);compressed=src.stat().st_size>1048576
 if compressed:
  dest=Path(str(dest)+'.gz')
  with src.open('rb') as i,dest.open('xb') as raw,gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as o:shutil.copyfileobj(i,o)
 else:
  with src.open('rb') as i,dest.open('xb') as o:shutil.copyfileobj(i,o)
 rows.append(dict(source=str(src),source_bytes=src.stat().st_size,source_sha256=sha(src),evidence=str(dest.relative_to(E)),evidence_bytes=dest.stat().st_size,evidence_sha256=sha(dest),gzip=compressed))
(E/'full-provenance.json').write_text(json.dumps(rows,indent=2)+'\n')
profiles=[]
for src in sorted(D.glob('stage-A/profiles/*')):
 if src.is_file():profiles.append(dict(path=str(src),bytes=src.stat().st_size,allocated_bytes=src.stat().st_blocks*512,sha256=sha(src)))
(E/'profile-final-inventory.json').write_text(json.dumps(profiles,indent=2)+'\n')
dus=[]
for path in [D,*D.glob('stage-*/gbs-root')]:
 cmd=['timeout','90','nice','-n','19','ionice','-c3','du','-sx','-B1',str(path)];p=subprocess.run(cmd,capture_output=True,text=True);dus.append(dict(time=datetime.datetime.now().astimezone().isoformat(),argv=cmd,rc=p.returncode,stdout=p.stdout,stderr=p.stderr))
(E/'final-du.json').write_text(json.dumps(dus,indent=2)+'\n');(E/'final-df.txt').write_text(subprocess.check_output(['df','-B1','/home'],text=True))
print('FINISHED_EVIDENCE',ends[-1],len(rows),'files',flush=True)
