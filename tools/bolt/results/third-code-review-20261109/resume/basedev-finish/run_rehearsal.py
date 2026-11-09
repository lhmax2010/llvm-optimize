from pathlib import Path
import subprocess,os,time,datetime,json,gzip,re,shutil,sys,hashlib,shlex
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.with_name('llvm-optimize-bolt');E=Path(__file__).parent
tag=sys.argv[1];assert tag in ('toolchain','basedev')
bid={'toolchain':'1221204','basedev':'1221207'}[tag]
D=W/'temp/rebase-359934-20261106-r2/rehearsal'/tag/'retry-02'
O=E/('rehearsal-'+tag);O.mkdir()
head='fa4f9978c9162d3c6cd2113d0cfe1173f04881c8'
argv=['/bin/sh',str(B/'tools/bolt/rebase-launch-20261106-r2'/tag/'launch.sh'),head,'rehearsal-02']
argv.append('basedev')
command=shlex.join(argv)
expected=(B/'docs/bolt/72_third_code_review_fixes.md').read_text().splitlines()[233]
print('FULL ARGV:',command,flush=True)
print('DOC LINE 234:',expected,flush=True)
assert command==expected,'argv differs from doc line 234'
(O/'launch-command.json').write_text(json.dumps(argv,indent=2)+'\n')
status='failed';reason='launch-or-audit-failed'
def stamp():return datetime.datetime.now().astimezone().isoformat()
def flags(lines):
 out={}
 for n,line in enumerate(lines,1):
  text=re.sub(r'^\[\s*\d+s\]\s*','',line).strip()
  if text.startswith(('TIZEN_LLVM_NORMALIZED_FLAGS ','TIZEN_LLVM_DROPPED_FLAGS ','TIZEN_LLVM_FLAGS_WARNING ')):
   out.setdefault(text.split()[0],[]).append(dict(line=n,text=text))
 return out
try:
 assert not D.exists()
 p=subprocess.run(argv,text=True,capture_output=True)
 (O/'launch.stdout').write_text(p.stdout);(O/'launch.stderr').write_text(p.stderr)
 print(p.stdout,end='',flush=True);print(p.stderr,end='',flush=True)
 assert p.returncode==0,p.returncode
 unit=json.loads((D/'controller-command.json').read_text())
 unit=next(x.split('=',1)[1] for x in unit if x.startswith('--unit='))
 start=time.monotonic()
 while True:
  state=subprocess.check_output(['systemctl','--user','show',unit,'-p','ActiveState','--value'],text=True).strip()
  if state in ('inactive','failed'):break
  assert time.monotonic()-start<3600,'rehearsal exceeded one hour; no manual retry'
  tail=(D/'controller.stdout').read_text(errors='replace').splitlines()
  print('REHEARSAL_PROGRESS',stamp(),tag,state,tail[-1] if tail else '(no controller output)',flush=True)
  time.sleep(30)
 # Snapshot the completed attempt's evidence; never execute historical scripts.
 for name in ('plan.json','controller-command.json','controller.stdout','controller.stderr'):
  shutil.copyfile(D/name,O/name)
 for p in sorted((D/'evidence').iterdir()):
  if p.is_file():
   if p.stat().st_size>1024**2:
    with p.open('rb') as src,gzip.open(O/(p.name+'.gz'),'wb') as dst:shutil.copyfileobj(src,dst)
   else:shutil.copyfile(p,O/p.name)
 result=json.loads((D/'evidence/result.json').read_text());assert result['status']=='ok',result
 audit=json.loads((D/'evidence/final-audit.json').read_text())
 assert not audit['mounts']['stdout'] and not audit['remaining_build_processes'],audit
 assert audit['source']['commit']==head and not audit['source']['status'],audit['source']
 copy=json.loads((D/'evidence/log-copy-audit.json').read_text())
 assert copy['PASS'] and copy['log_restarts']==0 and copy['source_bytes']==copy['evidence_bytes'],copy
 local=(D/'evidence/rpm-build-final.log').read_text(errors='replace')
 with gzip.open(B/'tools/bolt/results/qb-1221204-1221207'/bid/'x86_64/llvm.buildlog.txt.gz','rt',errors='replace') as f:qb=flags(f)
 got=flags(local.splitlines(True))
 for key in ('TIZEN_LLVM_NORMALIZED_FLAGS','TIZEN_LLVM_DROPPED_FLAGS'):
  assert len(got.get(key,[]))==1 and len(qb.get(key,[]))==1,(key,got,qb)
  assert [r['text'] for r in got[key]]==[r['text'] for r in qb[key]],(key,got,qb)
 assert not got.get('TIZEN_LLVM_FLAGS_WARNING') and not qb.get('TIZEN_LLVM_FLAGS_WARNING')
 resources=list(D.rglob('resource-table.md'));assert len(resources)==1,resources
 shutil.copyfile(resources[0],O/'resource-table.md')
 assert '+ cmake -G Ninja' in local and '+ ninja ' not in local
 checks=dict(PASS=True,project=tag,qb=bid,local=got,reference=qb,log_copy=copy,resource_table=str(resources[0]),final_audit=audit,result=result)
 (O/'comparison-audit.json').write_text(json.dumps(checks,indent=2)+'\n')
 status='ok';reason='CMake_stop_flags_log_resources_cleanup_pass'
 print(json.dumps(checks,indent=2),flush=True)
finally:
 line='REHEARSAL 已结束 '+stamp()+' project='+tag+' status='+status+' reason='+reason
 (O/'end.txt').write_text(line+'\n');print(line,flush=True)
if status!='ok':sys.exit(1)
