"""Local measurement only. Never imported by the packaged helper/spec."""
from pathlib import Path
import hashlib,json,os,subprocess,time
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt')
W=B.parent/'llvm-optimize'; T=Path(__file__).resolve().parent
P=W/'temp/pgo-resource-20261102'; E=P/'preflight'
S=W/'temp/debuglink-tb20261026/source'; COMMIT='3ee2d84719e4bd358c0b2366161f70f2eb788313'
H=W/'temp/debuglink-20261028/full-20261030'
CONFIG=W/'temp/bolt-v4-20261021-disk-footprint/gbs_llvm_qb1202084.conf'
BUILD_SHA='e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945'
INNER='/home/abuild/rpmbuild/BUILD/llvm-22.1.8'
PROFDATA='/home/abuild/pgo-resource/clang.profdata'
MACROS=['--define','jobs 8','--define','_smp_mflags -j8','--define','_costomized_smp_mflags -j20']
def save(p,obj):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def call(argv,out,cwd=None,env=None):
 out.parent.mkdir(parents=True,exist_ok=True);save(Path(str(out)+'.argv.json'),argv);t=time.time_ns()
 with out.open('wb') as o,Path(str(out)+'.stderr').open('wb') as e:r=subprocess.run(argv,cwd=cwd,env=env,stdout=o,stderr=e)
 save(Path(str(out)+'.result.json'),{'rc':r.returncode,'start_ns':t,'end_ns':time.time_ns()})
 if r.returncode:raise RuntimeError(f'{out}: rc={r.returncode}')
def props():
 total=int(next(l.split()[1] for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemTotal:')))*1024
 return ['-p','MemoryMax='+str(total-8*1024**3),'-p','MemorySwapMax=0','-p','CPUQuota=1200%','-p','Nice=10','-p','IOSchedulingClass=best-effort','-p','IOSchedulingPriority=7','-p','OOMPolicy=stop','-p','KillMode=control-group','-p','TimeoutStopSec=120']
def root(d):return d/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
def prefix(r):return ['sudo','-n','/usr/sbin/chroot','--userspec=1000:1000',str(r),'/usr/bin/env','-i','HOME=/home/abuild','USER=abuild','LOGNAME=abuild','SHELL=/bin/sh','PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin','LC_ALL=C','LANG=C']
def disk_budget():
 s=os.statvfs('/home');free=s.f_bavail*s.f_frsize;peak=68252237824
 # Two roots at 1.5x the observed full build peak, plus 20 GiB headroom.
 required=3*peak+20*1024**3
 return dict(available_bytes=free,historical_peak_bytes=peak,root_count=2,multiplier=1.5,reserve_bytes=20*1024**3,required_bytes=required,PASS=free>=required)
