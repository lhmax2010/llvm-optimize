"""Measurement only: immutable inputs, one compiler slot/inode, no package build."""
from pathlib import Path
import os,json,hashlib,shutil,subprocess,time,statistics,math,traceback,datetime,threading,signal
E=Path(__file__).resolve().parent
C=json.loads((E/'config.json').read_text());D=Path(C['work'])
CASES=json.loads((E/'cases.json').read_text());CPU=C['cpu']
def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def save(p,x):
    tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(x,indent=2)+'\n');tmp.replace(p)
def read(p):
    try:return Path(p).read_text().strip()
    except OSError:return 'unavailable'
def condition():
    return dict(time_ns=time.time_ns(),loadavg=read('/proc/loadavg'),frequency_kHz=read(f'/sys/devices/system/cpu/cpu{CPU}/cpufreq/scaling_cur_freq'),free_bytes=shutil.disk_usage(D).free)
def process_snapshot():return subprocess.check_output(['ps','-eo','pid,comm,pcpu,args','--sort=-pcpu'],text=True)
def main():
    assert CPU in os.sched_getaffinity(0)
    assert not (E/'samples.jsonl').exists(),'Do not append a different run to measurements'
    assert subprocess.check_output(['setarch','x86_64','-R','/bin/cat','/proc/self/personality'],text=True).strip()=='00040000'
    meta=dict(start=datetime.datetime.now().astimezone().isoformat(),parallel_compiles=1,fixed_cpu=CPU,affinity=sorted(os.sched_getaffinity(0)),ASLR='ADDR_NO_RANDOMIZE via setarch x86_64 -R; 00040000',governor=read(f'/sys/devices/system/cpu/cpu{CPU}/cpufreq/scaling_governor'),driver=read(f'/sys/devices/system/cpu/cpu{CPU}/cpufreq/scaling_driver'),siblings=read(f'/sys/devices/system/cpu/cpu{CPU}/topology/thread_siblings_list'),cpuinfo=read('/proc/cpuinfo'),order='group static then hybrid; each round A/B on even rounds, B/A on odd rounds; each role runs identical ordered 300 cases',timer='monotonic_ns around taskset + setarch + Tizen loader + clang subprocess; copy/hash/condition sampling outside timer',runtime='Tizen dynamic loader/libraries from preserved hybrid build root; host namespace; explicit per-target sysroot and common resource-dir',outliers_removed=False)
    save(E/'conditions.json',meta);(E/'processes-before.txt').write_text(process_snapshot())
    slot=D/'compiler/clang-22';slot.parent.mkdir(exist_ok=True);slot.touch(exist_ok=True);inode=slot.stat().st_ino
    objects=D/'objects';objects.mkdir(exist_ok=True);logs=E/'compile-logs';logs.mkdir(exist_ok=True)
    for u in CASES:assert sha(u['input'])==u['input_sha256']
    for group,roles in C['groups'].items():
        reference={};rows=[]
        for round_no in range(5):
            for role in (['ordinary','candidate'] if round_no%2==0 else ['candidate','ordinary']):
                source=roles[role];shutil.copyfile(source['path'],slot);slot.chmod(0o755)
                assert sha(slot)==source['sha256'] and slot.stat().st_ino==inode
                # Every timed call has an identical compiler path, argv, cwd, input and output across roles.
                for idx,u in enumerate(CASES):
                    tag=f'{group}-{round_no}-{role}-{idx:03d}';output=D/'same.o';output.unlink(missing_ok=True)
                    argv=['/usr/bin/taskset','-c',str(CPU),'/usr/bin/setarch','x86_64','-R']+C['loader']+[str(slot)]+u['argv']
                    before=condition()
                    with (logs/(tag+'.txt')).open('wb') as log:
                        start=time.monotonic_ns()
                        r=subprocess.Popen(argv,cwd=D,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
                        def timeout_child():
                            try:os.killpg(r.pid,signal.SIGKILL)
                            except ProcessLookupError:pass
                        watchdog=threading.Timer(900,timeout_child);watchdog.daemon=True;watchdog.start()
                        r.wait();end=time.monotonic_ns();watchdog.cancel()
                    after=condition();h=sha(output) if output.is_file() else None
                    ref=objects/(group+'-'+str(idx)+'.o')
                    if idx not in reference:
                        assert role=='ordinary';shutil.copyfile(output,ref);reference[idx]=h
                    equal=h==reference[idx] and output.read_bytes()==ref.read_bytes()
                    row=dict(group=group,round=round_no,role=role,case=idx,language=u['language'],option=u['option'],target=u['target'],name=u['name'],wall_s=(end-start)/1e9,returncode=r.returncode,object_sha256=h,object_bytes=output.stat().st_size if output.exists() else None,byte_equal=equal,before=before,after=after,argv=argv,compiler_sha256=source['sha256'],compiler_inode=inode,log='compile-logs/'+tag+'.txt')
                    with (E/'samples.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
                    rows.append(row)
                    save(E/'progress.json',dict(group=group,round=round_no,role=role,case=idx,completed_total=len(rows)+(3000 if group=='hybrid' else 0),last=row))
                    print(tag,round(row['wall_s'],4),'rc',r.returncode,'equal',equal,flush=True)
                    assert r.returncode==0 and h and output.stat().st_size>0,(tag,'compile failure')
                    # Differences must be listed; do not discard timing or silently filter sections.
        assert len(rows)==3000
        save(E/(group+'-finished.json'),dict(compiles=len(rows),byte_equal=sum(x['byte_equal'] for x in rows),end=datetime.datetime.now().astimezone().isoformat()))
    (E/'processes-after.txt').write_text(process_snapshot())
    save(E/'finished.json',dict(status='COMPLETE',compiles=6000,end=datetime.datetime.now().astimezone().isoformat(),inputs_unchanged=all(sha(u['input'])==u['input_sha256'] for u in CASES)))
if __name__=='__main__':
    try:main()
    except BaseException:
        (E/'failure.txt').write_text(traceback.format_exc());raise
