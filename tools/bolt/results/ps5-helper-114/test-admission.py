from pathlib import Path
import os,json,time

def check():
    busy=[];errors=[]
    for p in Path('/proc').iterdir():
        if not p.name.isdecimal():continue
        try:
            state=(p/'stat').read_text().rsplit(')',1)[1].split()[0]
            if state in ('Z','X'):continue
            comm=(p/'comm').read_text().strip()
            argv=(p/'cmdline').read_bytes().split(b'\0')
            names=[os.path.basename(x.decode(errors='replace')) for x in argv[:3]]
            cg=(p/'cgroup').read_text()
            if comm in ('gbs','rpmbuild','ninja','ninja-build') or any(x in ('gbs','rpmbuild','ninja','ninja-build') for x in names) or 'task102' in cg or 'task-102' in cg:
                busy.append({'pid':int(p.name),'comm':comm,'argv':[x.decode(errors='replace') for x in argv[:5]],'cgroup':cg})
        except (FileNotFoundError,ProcessLookupError):pass
        except PermissionError as e:errors.append(str(e))
    record={'time':time.time(),'busy':busy,'inspection_errors':errors,'admitted':not busy and not errors}
    with (Path(__file__).parent/'test-admission.jsonl').open('a') as f:f.write(json.dumps(record)+'\n')
    if not record['admitted']:raise RuntimeError('STOP tests not admitted: '+json.dumps(record))
    return record

if __name__=='__main__':print(json.dumps(check()))
