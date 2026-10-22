import os,sys,json,time,subprocess,threading,signal,shutil
from pathlib import Path
E=Path(sys.argv[1]);root=Path(sys.argv[2]);unit=sys.argv[3];command=sys.argv[4:]
E.mkdir(parents=True,exist_ok=True)
start=time.monotonic();stop=threading.Event()
def save(name,value): (E/name).write_text(json.dumps(value,indent=2)+'\n')
def append(name,value):
    with (E/name).open('a') as f:f.write(json.dumps(value)+'\n')
def memory():
    return int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))*1024
cg=Path('/sys/fs/cgroup')/next(x.split(':',2)[2] for x in Path('/proc/self/cgroup').read_text().splitlines() if x.startswith('0:')).lstrip('/')
def sample():
    paths=[root]
    for scratch in (root/'local/BUILD-ROOTS').glob('*'):
        rpm=scratch/'home/abuild/rpmbuild';paths += [rpm/'BUILD',rpm/'BUILDROOT',rpm/'RPMS',rpm/'SRPMS']
        for build in (rpm/'BUILD').glob('llvm-*/build'):
            paths += [build,build/'tools/bolt',build/'clang-bolt',build/'lto.cache',build/'native-archive-conversion']
    for path in paths:
        if not path.exists():continue
        r=subprocess.run(['du','-sx','-B1',str(path)],capture_output=True,text=True)
        append('du.jsonl',{'time_ns':time.time_ns(),'elapsed':time.monotonic()-start,'path':str(path),'stdout':r.stdout,'stderr':r.stderr,'rc':r.returncode})
def watch():
    due=0
    while not stop.is_set():
        now=time.monotonic();record={'time_ns':time.time_ns(),'elapsed':now-start,'mem_available':memory(),'disk_free':shutil.disk_usage(root.parent).free}
        for key in ['memory.current','memory.peak','memory.events','memory.swap.current']:
            try:record[key]=(cg/key).read_text().strip()
            except OSError:pass
        peaks=[]
        try:pids=(cg/'cgroup.procs').read_text().split()
        except OSError:pids=[]
        for pid in pids:
            try:
                lines=Path('/proc',pid,'status').read_text().splitlines()
                hwm=next((x for x in lines if x.startswith('VmHWM:')),None)
                if hwm:peaks.append({'pid':int(pid),'VmHWM_kB':int(hwm.split()[1])})
            except OSError:pass
        record['processes']=peaks;append('resource.jsonl',record)
        if record['disk_free']<30*1024**3:
            save('emergency-stop.json',record)
            subprocess.Popen(['systemctl','--user','stop',unit]);return
        if now>=due:
            sample();due=now+60
        stop.wait(5)
save('launch.json',{'argv':command,'root':str(root),'unit':unit,'cgroup':str(cg),'time_ns':time.time_ns(),'memory_limit':'infinity','swap_limit':0,'nice':15,'ionice':3,'lease_metadata':str(E/'controller-command.json')})
t=threading.Thread(target=watch);t.start()
try:
    with (E/'build.log').open('wb') as log:
        child=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.DEVNULL)
        for line in iter(child.stdout.readline,b''):
            log.write(('[%8.3fs] ' % (time.monotonic()-start)).encode()+line);log.flush()
        child.wait();r=child
    save('result.json',{'exit_code':r.returncode,'seconds':time.monotonic()-start,'time_ns':time.time_ns()})
finally:stop.set();t.join();sample()
sys.exit(r.returncode)
