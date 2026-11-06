from pathlib import Path
import subprocess,gzip,json,hashlib,re,shutil,datetime,os,sys
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt')
E=Path(__file__).resolve().parent/('rehearsal-'+sys.argv[1]);E.mkdir()
project=sys.argv[1]
D=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106-r2/rehearsal')/project
R=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
O=E/'rehearsal';O.mkdir()
plan=json.loads((D/'plan.json').read_text())
result=json.loads((D/'evidence/result.json').read_text())
assert result['status']=='ok',result
assert plan['commit']=='5a27edb4265366781f07049ad17a3796f2e05301'
assert plan['buildconf_sha256']=={'toolchain':'8f201a0d58eb634e60a1f213f47fc09dfa953d9869cdc5724f326a76203587bf','basedev':'8ace286a5f98f2e02a79be275a64c22a86ea2b0034174c1e293381e181ce3f6a'}[project]
rp=D/'evidence/log-restarts.jsonl'
restarts=sum(1 for _ in rp.open()) if rp.exists() else 0
original=R/'.build.log';copy=D/'evidence/rpm-build.log'
a=original.read_bytes();b=copy.read_bytes()
assert restarts==0 and a==b
log=a.decode(errors='strict');lines=log.splitlines()
cmake=[{'line':i,'text':l} for i,l in enumerate(lines,1) if '+ cmake -G Ninja ' in l]
assert len(cmake)==1
assert not re.search(r'\+ ninja(?: |$)',log,re.M)
assert 'Build files have been written to:' not in log
def flags(iterable):
 rows=[]
 for i,line in enumerate(iterable,1):
  t=re.sub(r'^\[\s*\d+s\]\s*','',line.rstrip('\n'))
  if re.match(r'TIZEN_LLVM_(NORMALIZED_FLAGS|DROPPED_FLAGS|FLAGS_WARNING) ',t):
   rows.append({'line':i,'text':t})
 return rows
local=flags(lines)
qb=B/'tools/bolt/results/qb-1216409-1216410'/('1216409' if project=='toolchain' else '1216410')/'x86_64/llvm.buildlog.txt.gz'
with gzip.open(qb,'rt') as f:qflags=flags(f)
assert [x['text'] for x in local]==[x['text'] for x in qflags]
assert len(local)==2
resource=json.loads((D/'evidence/resource-table.json').read_text())
assert resource['log_source']['path']==str(original)
assert resource['log_source']['sha256']==hashlib.sha256(a).hexdigest()
audit=json.loads((D/'evidence/final-audit.json').read_text())
assert not audit['mounts']['stdout'] and not audit['remaining_build_processes']
units=[plan['prep_unit'],plan['build_unit'],next(x.split('=',1)[1] for x in json.loads((D/'controller-command.json').read_text()) if x.startswith('--unit='))]
commands={}
cmd=['systemctl','--user','show',*units,'-p','Id','-p','ActiveState','-p','SubState','-p','Result','-p','ControlGroup']
r=subprocess.run(cmd,capture_output=True,text=True)
commands['services']={'argv':cmd,'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
assert r.returncode==0 and r.stdout.count('ActiveState=inactive')==3
cmd=['findmnt','-rn','-o','TARGET,SOURCE,FSTYPE']
r=subprocess.run(cmd,capture_output=True,text=True)
own=[l for l in r.stdout.splitlines() if str(D) in l]
commands['mounts']={'argv':cmd,'rc':r.returncode,'filtered_stdout':'\n'.join(own),'filter':str(D)}
assert not own
procs=[];blind=[]
for p in Path('/proc').iterdir():
 if not p.name.isdigit():continue
 try:
  cg=(p/'cgroup').read_text()
  if any('/'+u in cg for u in units):
   procs.append({'pid':int(p.name),'cgroup':cg})
 except (PermissionError,FileNotFoundError,ProcessLookupError) as ex:
  blind.append({'pid':int(p.name),'reason':type(ex).__name__})
assert not procs
commands['process_cgroups']={'method':'read /proc/[0-9]*/cgroup; match exact service names','matches':procs,'unreadable_or_exited':blind}
(O/'cleanup-command-output.json').write_text(json.dumps(commands,indent=2)+'\n')
for p in (D/'evidence').iterdir():
 if p.is_file() and p.suffix in ('.json','.jsonl','.md','.txt','.stdout','.stderr'):
  if p.stat().st_size>1024**2:
   with p.open('rb') as f,gzip.open(O/(p.name+'.gz'),'wb') as out:shutil.copyfileobj(f,out)
  else:shutil.copyfile(p,O/p.name)
for name in ['plan.json','controller.stdout','controller.stderr','controller-command.json']:
 shutil.copyfile(D/name,O/name)
with gzip.open(O/'original-build.log.gz','wb') as f:f.write(a)
with gzip.open(O/'generated-run.py.gz','wb') as f:f.write((D/'run.py').read_bytes())
row={'PASS':True,'root':str(D),'source':plan['commit'],'controller':result,'log_restarts':restarts,
     'source_bytes':len(a),'copy_bytes':len(b),'byte_equal':True,'log_sha256':hashlib.sha256(a).hexdigest(),
     'local_flags':local,'qb_log':str(qb),'qb_flags':qflags,'flags_equal':True,'warning_count':0,
     'cmake_start':cmake,'ninja_ran':False,'resource_report_generated':True,
     'resource_log_source':resource['log_source'],'cleanup_pass':True}
(E/'rehearsal-audit.json').write_text(json.dumps(row,indent=2)+'\n')
print('REHEARSAL_AUDIT PASS')
print('log-restarts=0; original=copy='+str(len(a))+' bytes; byte_equal=true')
for x in local:print('LOCAL L'+str(x['line'])+': '+x['text'])
for x in qflags:print('QB L'+str(x['line'])+': '+x['text'])
print('resource_report=PASS; Ninja=NOT RUN; remaining_mounts=0; remaining_processes=0')
print(r.stdout if False else commands['services']['stdout'])
end=project+' 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status=ok reason=rehearsal-log-restarts-0-and-audit-PASS'
(E/'item-end.txt').write_text(end+'\n');print(end)
