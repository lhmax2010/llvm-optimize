import fcntl,subprocess,time,json,os,sys,hashlib,shutil
from pathlib import Path
W=Path('/home/linhao/Toolchain/development/llvm-optimize');D=W/'temp/bolt-v4-20261022-cache-release';E=D/'baseline-segment1';E.mkdir(exist_ok=False)
source=W/'temp/bolt-v4-20261013/v41/llvm-source';config=W/'temp/bolt-v4-20261021-disk-footprint/gbs_llvm_qb1202084.conf';conf=config.parent/'build.conf'
assert hashlib.sha256(conf.read_bytes()).hexdigest()=='e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945'
root=D/'baseline-root';assert not root.exists()
lock=open('/home/linhao/Toolchain/development/heavy-stage.lock','a+')
wait=time.monotonic()
while True:
    try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);break
    except BlockingIOError:
        if time.monotonic()-wait>=7200:raise RuntimeError('shared lock timeout')
        time.sleep(10)
acquired=time.monotonic()
try:
    mem=int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))*1024
    free=shutil.disk_usage(D).free
    # Local admission estimate: historical lower bound + 15 GiB BOLT + 20 GiB export/retention + 30 GiB reserve.
    required=236149145600+(15+20+30)*1024**3
    admission={'mem_available':mem,'free':free,'reference_required':required,'time_ns':time.time_ns()}
    (E/'admission.json').write_text(json.dumps(admission,indent=2))
    assert mem>=12*1024**3 and free>=required,admission
    root.mkdir();tmp=D/'baseline-tmp';tmp.mkdir()
    cmd=['gbs','-c',str(config),'build','-A','x86_64','-B',str(root),'-c','9e5675f57d122549997caffa39b655dfefc46fee','--threads=30','--define','jobs 8','--define','_smp_mflags -j8','--define','_costomized_smp_mflags -j20','--baselibs','--clean-once','--style=tar',str(source)]
    unit='bolt-cache-baseline-20261022-1.service'
    argv=['systemd-run','--user','--wait','--pipe','--unit='+unit,'-p','MemoryMax=16G','-p','MemorySwapMax=0','-p','Nice=15','-p','IOSchedulingClass=idle','-p','RuntimeMaxSec=3400','-p','TimeoutStopSec=20','-p','WorkingDirectory='+str(source),'--setenv=TMPDIR='+str(tmp),'python3','-B',str(D/'measure.py'),str(E),str(root),unit]+cmd
    (E/'command.json').write_text(json.dumps(argv,indent=2))
    with (E/'service.stdout').open('w') as out,(E/'service.stderr').open('w') as err:r=subprocess.run(argv,stdout=out,stderr=err)
    (E/'service-exit.json').write_text(json.dumps({'rc':r.returncode,'held_seconds':time.monotonic()-acquired}))
finally:
    fcntl.flock(lock,fcntl.LOCK_UN);lock.close()
    (E/'lock-released.json').write_text(json.dumps({'time_ns':time.time_ns(),'held_seconds':time.monotonic()-acquired}))
