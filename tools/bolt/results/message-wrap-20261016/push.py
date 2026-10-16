from pathlib import Path
import subprocess,json,re,time,sys
E=Path(__file__).resolve().parent;S=E.parents[1]/'temp/bolt-v4-20261013/v41/llvm-source';v=json.loads((E/'verification.json').read_text());old=v['old'];new=v['new'];branch='refs/heads/sandbox/lhmax2025/bolt_pgo'
def git(*a):return subprocess.check_output(['git','-C',str(S),*a])
assert v['status']=='PASS' and git('rev-parse','HEAD').decode().strip()==new
before=git('ls-remote','origin',branch).decode();(E/'remote-before.txt').write_text(before);r={'old':old,'new':new,'before':before,'started':time.time()}
if before.split()!=[old,branch]:
 r.update(status='STOP_LEASE_MISMATCH');(E/'push-result.json').write_text(json.dumps(r,indent=2)+'\n');sys.exit('STOP: '+before)
argv=['git','-C',str(S),'push','--force-with-lease='+branch+':'+old,'origin',new+':'+branch];r['argv']=argv;p=subprocess.run(argv,capture_output=True,text=True);(E/'push.stdout').write_text(p.stdout);(E/'push.stderr').write_text(p.stderr);r['rc']=p.returncode;r['warnings']=re.findall(r'^.*warning:.*$',p.stdout+p.stderr,re.M|re.I)
if p.returncode:
 r.update(status='REJECTED');(E/'push-result.json').write_text(json.dumps(r,indent=2)+'\n');print(p.stdout+p.stderr);sys.exit(p.returncode)
after=git('ls-remote','origin',branch).decode();(E/'remote-after.txt').write_text(after);r['after']=after;r['status']='PASS' if after.split()==[new,branch] else 'STOP_REMOTE_MISMATCH';(E/'push-result.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));print(p.stdout+p.stderr);assert r['status']=='PASS'
