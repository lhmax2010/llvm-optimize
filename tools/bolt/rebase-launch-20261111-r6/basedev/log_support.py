"""Bounded original-GBS-log reader. Never fall back to the accumulated copy."""
from pathlib import Path
import hashlib,re,datetime
LIMIT=1024**3

def canonical_log(D):
 paths=sorted((Path(D)/'gbs-driver/local/repos').glob('*/x86_64/logs/success/llvm-*/log.txt'))
 assert len(paths)==1,('exactly one original successful GBS log required',list(map(str,paths)))
 assert paths[0].stat().st_size<=LIMIT,('GBS log exceeds 1 GiB',str(paths[0]))
 return paths[0]

def log_summary(path):
 path=Path(path);assert path.stat().st_size<=LIMIT,'GBS log exceeds 1 GiB'
 selected={};count=0;h=hashlib.sha256();phases={};origin=None;last=0
 patterns=[('ordinary-build','Executing(%build)'),('ordinary-install','Executing(%install)'),('BOLT','BOLT_DISK_REPORT'),('cache-release',' cache-release '),('archive-conversion','NATIVE_ARCHIVES_BEGIN'),('platform-post','find-debuginfo'),('packaging','Processing files:')]
 with path.open('rb') as f:
  for count,raw in enumerate(f,1):
   h.update(raw);line=raw.decode(errors='replace').rstrip('\n');m=re.match(r'\[\s*(\d+)s\]',line)
   seconds=int(m[1]) if m else None
   if seconds is not None:last=seconds
   if 'started "build llvm.spec" at ' in line:
    stamp=line.split('started "build llvm.spec" at ',1)[1].rstrip('.')
    origin=datetime.datetime.strptime(stamp,'%a %b %d %H:%M:%S UTC %Y').replace(tzinfo=datetime.timezone.utc).timestamp()-(seconds or 0)
   if re.search(r'BOLT|TIZEN_LLVM|TIZEN_HYBRID|NATIVE_ARCHIVES|find-debuginfo|profile|mismatch|unmatched|clang-22.*(?:extract|strip)|(?:extract|strip).*clang-22',line,re.I):selected[count]=line
   if seconds is None or '+ echo ' in line or '+ printf ' in line:continue
   for phase,token in patterns:
    if token in line:phases.setdefault(phase,dict(line=count,text=line,seconds=seconds))
   if 'BOLT_COMPARE_ROOT_PASS' in line:phases.setdefault('BOLT-end',dict(line=count,text=line,seconds=seconds))
   if 'BOLT_CACHE_RELEASE removed' in line or 'BOLT_CACHE_RELEASE skipped' in line:phases.setdefault('cache-release-end',dict(line=count,text=line,seconds=seconds))
   if 'NATIVE_ARCHIVES_END' in line:phases.setdefault('archive-conversion-end',dict(line=count,text=line,seconds=seconds))
 return dict(path=str(path),bytes=path.stat().st_size,lines=count,sha256=h.hexdigest(),selected=selected,phases=phases,epoch_zero=origin,last_seconds=last)

def audit_log_copy(D):
 D=Path(D);E=D/'evidence';rp=E/'log-restarts.jsonl';restarts=sum(1 for _ in rp.open()) if rp.exists() else 0
 source=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/.build.log'
 # During rehearsal there is no success log. .build.log is the GBS original.
 copy=E/'rpm-build.log';assert restarts==0,('log-restarts',restarts)
 assert source.stat().st_size==copy.stat().st_size,('copied log size mismatch',source.stat().st_size,copy.stat().st_size)
 return dict(log_restarts=restarts,source=str(source),source_bytes=source.stat().st_size,evidence_bytes=copy.stat().st_size,PASS=True)
