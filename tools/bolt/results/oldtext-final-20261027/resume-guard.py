from pathlib import Path
import json,time,subprocess,shutil,datetime,traceback
D=Path(__file__).resolve().parent;E=D.parent.parent.parent/'llvm-optimize-bolt/tools/bolt/results/oldtext-final-20261027';R=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';WORK=R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt';C=R/'home/abuild/oldtext-resume-20261027';unit='oldtext-final-resume-20261027.service';reason=None
while True:
 q=subprocess.run(['systemctl','--user','show',unit,'-p','ActiveState','-p','ControlGroup'],capture_output=True,text=True);v=dict(l.split('=',1) for l in q.stdout.splitlines() if '=' in l)
 if v.get('ActiveState') not in ('active','activating','deactivating'):break
 cg=Path('/sys/fs/cgroup')/v.get('ControlGroup','').lstrip('/');row={'time_ns':time.time_ns(),'home_available_bytes':shutil.disk_usage('/home').free,'meminfo':Path('/proc/meminfo').read_text(),'loadavg':Path('/proc/loadavg').read_text()}
 for n in ['memory.current','memory.peak','memory.events','memory.swap.current','cpu.stat','io.stat']:
  try:row[n]=(cg/n).read_text()
  except OSError as ex:row[n]={'unavailable':str(ex)}
 with (E/'resume-guard-resources.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
 if row['home_available_bytes']<20*1024**3:reason='home-below-20GiB'
 events=row.get('memory.events')
 if isinstance(events,str) and any(int(l.split()[1])>0 for l in events.splitlines() if l.split()[0] in ['oom','oom_kill']):reason='cgroup-OOM'
 for file,field in [(WORK/'rewrite/rewrite-result.json','counts'),(WORK/'identity.json','identity')]:
  if file.exists():
   try:data=json.loads(file.read_text())
   except (OSError,json.JSONDecodeError):continue
   expected={'N':23592,'M':144032,'S':0,'U':1,'Q':383,'R':4.238545331242318e-05,'S_over_N':0.0}
   mismatch=data['counts']!=expected if field=='counts' else data.get('strip_all_sha256',data.get('after_sha256'))!='13a07cb7f84bd1ceda4d851c8bd71bddf7ef0c2d4864892eba64cbbb9a0350b8'
   if mismatch:reason='identity-or-profile-mismatch';(E/'identity-stop.json').write_text(json.dumps({'file':str(file),'data':data},indent=2)+'\n')
 if reason:
  (C/'STOP').write_text(reason);(E/'resume-guard-stop.json').write_text(json.dumps({'reason':reason,'time_ns':time.time_ns()},indent=2)+'\n')
  subprocess.run(['systemctl','--user','stop',unit]);break
 time.sleep(3)
print('GUARD_FINISHED '+str(reason),flush=True)
