from pathlib import Path
import sys,json,gzip,re,hashlib,subprocess,os,datetime,shutil
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.parent/'llvm-optimize'
E=Path(__file__).parent
project=sys.argv[1];qb={'toolchain':'1225393','basedev':'1225395'}[project]
D=W/'temp/rebase-359934-20261111-r6/rehearsal'/project/'retry-02';e=D/'evidence'
out=E/('rehearsal-'+project);out.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def flags(lines):
 result=[];warning=[]
 for n,t in enumerate(lines,1):
  x=re.match(r'^(?:\[\s*\d+s\]\s*)?(TIZEN_LLVM_(?:NORMALIZED_FLAGS|DROPPED_FLAGS) CFLAGS=.*)$',t.rstrip())
  if x:result.append(dict(line=n,text=t.rstrip(),payload=x[1]))
  if re.match(r'^(?:\[\s*\d+s\]\s*)?TIZEN_LLVM_FLAGS_WARNING ',t):warning.append(dict(line=n,text=t.rstrip()))
 return result,warning
result=json.loads((e/'result.json').read_text());assert result['status']=='ok',result
lines=(e/'rpm-build-final.log').read_text().splitlines()
actual,warn=flags(lines)
qbpath=B/'tools/bolt/results/qb-1225393-1225395'/qb/'x86_64/llvm.buildlog.txt.gz'
with gzip.open(qbpath,'rt') as f:expected,qwarn=flags(f)
assert len(actual)==len(expected)==2
assert [x['payload'] for x in actual]==[x['payload'] for x in expected],(actual,expected)
assert len(warn)==len(qwarn)==0
assert sum('+ cmake -G Ninja ' in x for x in lines)==1
assert not any(re.search(r'\+\s*(?:[^\s]*/)?ninja(?:\s|$)',x) for x in lines)
restarts=e/'log-restarts.jsonl';restart_count=sum(bool(x.strip()) for x in restarts.read_text().splitlines()) if restarts.exists() else 0
assert restart_count==0
original=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/.build.log';copy=e/'rpm-build.log'
assert original.stat().st_size==copy.stat().st_size
assert sha(original)==sha(copy)
audit=json.loads((e/'final-audit.json').read_text())
assert not audit['mounts']['stdout'] and not audit['remaining_build_processes'],audit
assert (e/'resource-table.md').stat().st_size>0
assert (e/'resource-table.json').stat().st_size>0
resource=json.loads((e/'resource-table.json').read_text())
units={}
for unit in [f'rebase359934r6-{project}-rehearsal-controller-20261111-02.service',f'rebase359934r6-{project}-rehearsal-prep-20261111-02.service',f'rebase359934r6-{project}-rehearsal-20261111-02.service']:
 p=subprocess.run(['systemctl','--user','show',unit,'-p','ActiveState','-p','SubState','-p','Result'],capture_output=True,text=True)
 units[unit]=dict(returncode=p.returncode,stdout=p.stdout,stderr=p.stderr)
 assert not any(x in p.stdout for x in ('ActiveState=active\n','ActiveState=activating\n','ActiveState=deactivating\n')),units
mounts=subprocess.run(['findmnt','-rn','-o','TARGET'],capture_output=True,text=True)
assert mounts.returncode==0,mounts.stderr
roots={str(D),str(D.resolve())}
remaining_mounts=[x for x in mounts.stdout.splitlines() if any(x==r or x.startswith(r+'/') for r in roots)]
assert not remaining_mounts,remaining_mounts
users=[];blind=[];excluded={os.getpid()};pid=os.getppid()
while pid>0 and pid not in excluded:
 excluded.add(pid)
 try:pid=int((Path('/proc')/str(pid)/'status').read_text().split('PPid:')[1].splitlines()[0])
 except (OSError,IndexError):break
for p in Path('/proc').iterdir():
 if not p.name.isdigit() or int(p.name) in excluded:continue
 for key in ('cwd','root'):
  try:target=os.readlink(p/key)
  except PermissionError:blind.append(str(p/key));continue
  except OSError:continue
  if any(target==r or target.startswith(r+'/') for r in roots):users.append(dict(pid=p.name,kind=key,target=target))
 try:fds=list((p/'fd').iterdir())
 except PermissionError:blind.append(str(p/'fd'));continue
 except OSError:continue
 for f in fds:
  try:target=os.readlink(f)
  except OSError:continue
  if any(target==r or target.startswith(r+'/') for r in roots):users.append(dict(pid=p.name,kind='fd',target=target))
assert not users,users
records=dict(PASS=True,project=project,qb=qb,result=result,log_restarts=restart_count,flags=actual,qb_flags=expected,warning_count=len(warn),qb_warning_count=len(qwarn),
 original_log=str(original),original_bytes=original.stat().st_size,copied_bytes=copy.stat().st_size,log_sha256=sha(original),no_ninja=True,
 final_audit=audit,current_units=units,findmnt=dict(returncode=mounts.returncode,remaining=remaining_mounts),
 process_check=dict(remaining=users,permission_blind_count=len(blind),note='ordinary-user current scan; root-level final cleanup evidence preserved from the authorized entry'),
 resource_table=resource,cmake=[x for x in lines if '+ cmake -G Ninja ' in x],time=datetime.datetime.now().astimezone().isoformat())
(out/'audit.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
(out/'process-permission-blind.txt').write_text('\n'.join(blind)+'\n')
(out/'findmnt-all.txt').write_text(mounts.stdout)
for rel in ('controller.stdout','controller.stderr','plan.json','controller-command.json'):
 shutil.copyfile(D/rel,out/rel)
for rel in ('result.json','final-audit.json','final-cleanup-mounts.json','final-cleanup-root-processes.json','log-copy-audit.json','log-source-handoff.jsonl','resource-table.md','resource-table.json','rpm-build-final.log','launcher-used.py','build-command.json','cmake-stop.jsonl'):
 if (e/rel).exists():shutil.copyfile(e/rel,out/rel)
print(json.dumps({k:records[k] for k in ('PASS','project','result','log_restarts','flags','warning_count','original_bytes','copied_bytes','no_ninja')},ensure_ascii=False,indent=2))
print('REHEARSAL 已结束',records['time'],'project='+project,'status=ok reason=CMake_flags_log_resources_cleanup_pass')
(out/'end.txt').write_text('REHEARSAL 已结束 '+records['time']+' project='+project+' status=ok reason=CMake_flags_log_resources_cleanup_pass\n')
