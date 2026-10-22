"""Local controller: freeze all build processes before releasing each lease."""
import fcntl,json,os,subprocess,sys,time,shutil
from pathlib import Path
D=Path(__file__).resolve().parent;label=sys.argv[1];command_file=Path(sys.argv[2]);cfg=json.loads(command_file.read_text());E=D/label;E.mkdir(exist_ok=False)
root=Path(cfg['root']);unit='bolt-cache-'+label+'.service';lock=open('/home/linhao/Toolchain/development/heavy-stage.lock','a+');held=False;started=None;child=None;frozen=False
G=1024**3

def save(name,v):(E/name).write_text(json.dumps(v,indent=2)+'\n')
def event(v):
    with (E/'leases.jsonl').open('a') as f:f.write(json.dumps(dict(time_ns=time.time_ns(),**v))+'\n')
def avail():return int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))*1024
def acquire():
    global held,started
    t=time.monotonic();memory_wait=None
    while True:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:
            if time.monotonic()-t>=7200:raise RuntimeError('shared lock timeout')
            time.sleep(5);continue
        held=True;started=time.monotonic()
        free=shutil.disk_usage(root.parent).free
        if free<(30*G if child is not None else cfg.get('required_free_bytes',30*G)):raise RuntimeError('local disk admission unavailable')
        event({'acquired':True,'memory_available':avail(),'disk_free':free});return

def release():
    global held
    if held:
        event({'released':True,'held_seconds':time.monotonic()-started})
        fcntl.flock(lock,fcntl.LOCK_UN);held=False

def ctl(*args):
    p=subprocess.run(['systemctl','--user',*args],capture_output=True,text=True,timeout=60)
    event({'control':args,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr});p.check_returncode();return p.stdout
try:
    acquire()
    argv=['systemd-run','--user','--wait','--pipe','--unit='+unit,'-p','MemoryMax=infinity','-p','MemorySwapMax=0','-p','Nice=15','-p','IOSchedulingClass=idle','-p','RuntimeMaxSec=24h','-p','TimeoutStopSec=20','--setenv=TMPDIR='+str(D/'baseline-tmp'),'python3','-B',str(D/'measure-unlimited.py'),str(E),str(root),unit]+cfg['argv']
    save('controller-command.json',{'argv':argv,'source_config':cfg,'lease_seconds':3200,'pause_before_unlock':True})
    with (E/'service.stdout').open('w') as out,(E/'service.stderr').open('w') as err:
        child=subprocess.Popen(argv,stdout=out,stderr=err)
        subprocess.run(['systemd-run','--user','--unit=bolt-cache-guard-'+label,'-p','MemoryMax=4G','-p','MemorySwapMax=0','-p','Nice=19','-p','IOSchedulingClass=idle','python3','-B',str(D/'guard-unlimited.py'),label],check=True)
        subprocess.run(['systemd-run','--user','--unit=bolt-cache-diskfree-'+label,'-p','MemoryMax=4G','-p','MemorySwapMax=0','-p','Nice=19','-p','IOSchedulingClass=idle','python3','-B',str(D/'diskfree-watch.py'),label],check=True)
        while child.poll() is None:
            if time.monotonic()-started>=3200:
                ctl('freeze',unit);frozen=True
                state=ctl('show',unit,'-p','FreezerState','--value').strip()
                if state!='frozen':raise RuntimeError('failed to confirm frozen build')
                release();time.sleep(1);acquire()
                ctl('thaw',unit);frozen=False
            time.sleep(1)
    save('controller-result.json',{'rc':child.returncode,'time_ns':time.time_ns()})
finally:
    if child is not None and child.poll() is None:
        try:ctl('stop',unit)
        finally:child.wait(timeout=60)
    release();lock.close()
