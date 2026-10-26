from pathlib import Path
import json,subprocess,os,time
E=Path(__file__).resolve().parent;W='/home/linhao/Toolchain/development/llvm-optimize'
units=json.loads((E/'units.json').read_text());paths=[u['path'] for u in units if u['group']!='W']
plans=json.loads((E/'scenarios.json').read_text());scopes=sorted(set(p for fs in plans.values() for v in fs.values() for p in v['paths']))
r=subprocess.run(['lsof','-nP'],text=True,capture_output=True);(E/'lsof-final.stdout').write_text(r.stdout);(E/'lsof-final.stderr').write_text(r.stderr)
lines=[x for x in r.stdout.splitlines() if W in x or '/var/tmp/llvm' in x]
(E/'lsof-final-project.txt').write_text('\n'.join(lines)+'\n')
(E/'lsof-final-visibility.txt').write_text('\n'.join(x for x in r.stdout.splitlines() if 'NOFD' in x)+'\n')
active={p:[l for l in lines if p+'/' in l or l.endswith(p)] for p in paths+scopes};active={p:v for p,v in active.items() if v}
f=subprocess.run(['fuser','-v']+paths+scopes,text=True,capture_output=True);(E/'fuser-final.stdout').write_text(f.stdout);(E/'fuser-final.stderr').write_text(f.stderr)
mounts={};errors=[]
for p in Path('/proc').glob('[0-9]*'):
 try:
  for l in (p/'mountinfo').read_text().splitlines():
   if W in l or '/var/tmp/llvm' in l:mounts.setdefault(l,[]).append(int(p.name))
 except OSError as x:errors.append(str(x))
d=subprocess.run(['df','-B1','/home','/var/tmp'],text=True,capture_output=True);(E/'df-final.stdout').write_text(d.stdout);(E/'df-final.stderr').write_text(d.stderr)
missing={p:not Path(p).exists() for p in [W+'/temp/runpath-fix-20261026',W+'/temp/bolt-v4-20261015-review3/payload-merged',W+'/temp/bolt-v4-20261015-review4b/payload-merged',W+'/temp/bolt-v4-20261015-validation/baseline-extract',W+'/temp/bolt-v4-20261015-install-rehearsal/upper']}
locks=[]
for p in list(Path(W).glob('*.lock'))+list(Path(W+'/temp').glob('*/*.lock'))+[Path('/home/linhao/Toolchain/development/heavy-stage.lock')]:
 if p.exists():
  s=p.stat();locks.append(dict(path=str(p),bytes=s.st_size,mtime=s.st_mtime,uid=s.st_uid))
result=dict(time=time.time(),lsof_rc=r.returncode,active_paths=active,fuser_argv=['fuser','-v']+paths+scopes,fuser_rc=f.returncode,fuser_stdout=f.stdout,fuser_stderr=f.stderr,mounts=mounts,mountinfo_errors=errors,absent=missing,locks=locks)
(E/'final-activity.json').write_text(json.dumps(result,indent=2)+'\n');print('active paths',list(active),'fuser',f.returncode,'mounts',len(mounts),'missing',missing)
