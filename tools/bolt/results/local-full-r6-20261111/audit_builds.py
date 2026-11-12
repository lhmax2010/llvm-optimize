from pathlib import Path
import json,gzip,re,hashlib,shutil,datetime,sys,collections,subprocess
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt')
W=B.parent/'llvm-optimize'
E=Path(__file__).resolve().parent
BASE=W/'temp/rebase-359934-20261111-r6'
def now():return datetime.datetime.now().astimezone().isoformat()
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def read(p,default=None):
 try:return json.loads(p.read_text())
 except (OSError,ValueError):return default
def parse(p):
 out=dict(flags=[],warnings=[],anchors=[],tools=[],native=[],profiles=[],errors=[],assignments={},disk_reports=[],post_gate=[],selected=[])
 opener=gzip.open if p.suffix=='.gz' else open
 with opener(p,'rt',errors='replace') as f:
  for n,raw in enumerate(f,1):
   line=raw.rstrip('\n');s=re.sub(r'^\[\s*\d+s\]\s?','',line);rec=dict(line=n,text=line,payload=s)
   if s.startswith(('TIZEN_LLVM_NORMALIZED_FLAGS ','TIZEN_LLVM_DROPPED_FLAGS ')):out['flags'].append(rec)
   if s.startswith('TIZEN_LLVM_FLAGS_WARNING '):out['warnings'].append(rec)
   if re.search(r'(?:^|[ :])(?:/[^ ]*/)?(?:sh|bash|rpm-tmp[^ :]*):.*(?:not found|command not found)',s) or re.search(r'\b(?:NATIVE_ARCHIVES_CANCELLED|BOLT_CANCELLED)\b',s):out['errors'].append(rec)
   for key in ['CFLAGS','CXXFLAGS','LDFLAGS']:
    if s.startswith('+ '+key+'='):out['assignments'][key]=rec
   if s.startswith('NATIVE_ARCHIVES_TOOLS '):
    out['tools'].append({**rec,'data':json.loads(s.split(' ',1)[1])})
   if s.startswith('BOLT_POST_GATE_PASS'):out['post_gate'].append(rec)
   if s.startswith('BOLT_DISK_REPORT '):out['disk_reports'].append({**rec,'data':json.loads(s.split(' ',1)[1])})
   if s.startswith('{'):
    try:z=json.loads(s)
    except ValueError:continue
    if {'N','M','S','U','Q','R'}<=z.keys():out['profiles'].append({**rec,'data':z})
    if 'counts' in z and isinstance(z['counts'],dict):out['profiles'].append({**rec,'data':z['counts']})
    if {'converted','preserved','path'}<=z.keys():out['native'].append({**rec,'data':z})
   if not s.startswith('+') and re.search(r'\b(?:BOLT_\w*PASS|BOLT_PROC_OK|BOLT_PROC_MISSING|BOLT_NINJA_EXIT_0|TIZEN_HYBRID_LINK_OK|NATIVE_ARCHIVES_END)\b',s):out['anchors'].append(rec)
   if not s.startswith('+') and ('BOLT' in s or 'NATIVE_ARCHIVES' in s or 'TIZEN_LLVM_' in s or 'TIZEN_HYBRID' in s):out['selected'].append(rec)
 out['lines']=n if 'n' in locals() else 0
 return out
def jl(p):
 if p.exists():
  with p.open() as f:
   for l in f:
    try:yield json.loads(l)
    except ValueError:pass
results={}
try:
 for project,bid in [('toolchain','1225393'),('basedev','1225395')]:
  D=BASE/project;O=E/project;O.mkdir(exist_ok=False);e=D/'evidence'
  if not D.exists():
   result={'status':'NOT RUN','reason':'build root not created'};save(O/'audit.json',result);results[project]=result;continue
  paths=list((D/'gbs-driver/local/repos').glob('*/x86_64/logs/success/llvm-*/log.txt'))
  orig=paths[0] if len(paths)==1 else D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/.build.log'
  result={'controller_result':read(e/'result.json'),'build_result':read(e/'build-result.json'),'original_log':str(orig),'successful_GBS_log':len(paths)==1}
  if orig.exists() and orig.stat().st_size<=1024**3:
   result['original_log_sha256']=sha(orig);result['original_log_bytes']=orig.stat().st_size
   with orig.open('rb') as f,gzip.open(O/'original-build.log.gz','wb') as g:shutil.copyfileobj(f,g)
   local=parse(orig);qb=parse(B/f'tools/bolt/results/qb-1225393-1225395/{bid}/x86_64/llvm.buildlog.txt.gz')
   save(O/'log-audit-raw.json',local);save(O/'qb-log-reference.json',qb)
   result['flags_equal']=len(local['flags'])==2 and [x['payload'] for x in local['flags']]==[x['payload'] for x in qb['flags']]
   result['warning_count']=len(local['warnings']);result['shell_or_cancel_errors']=local['errors']
   result['native_counts']={k:sum(x['data'][k] for x in local['native']) for k in ['converted','preserved']}
   result['native_archive_count']=len(local['native'])
   result['native_end']=[x for x in local['anchors'] if x['payload'].startswith('NATIVE_ARCHIVES_END')]
   result['tools']=local['tools'];result['final_flags']=local['assignments']
   result['profile_records']=local['profiles'];result['qb_profile_records']=qb['profiles']
   result['profiles_equal']=bool(local['profiles']) and [x['data'] for x in local['profiles']]==[x['data'] for x in qb['profiles']]
   result['post_disk_after_gate']=bool(local['post_gate']) and any(x['data'].get('stage')=='post' and x['line']>local['post_gate'][-1]['line'] for x in local['disk_reports'])
  else:result['log_status']='UNKNOWN: missing or over 1GiB original log'
  result['log_restarts']=sum(1 for _ in (e/'log-restarts.jsonl').open()) if (e/'log-restarts.jsonl').exists() else 0
  for name in ['result.json','build-result.json','controller-result.json','final-audit.json','failure.txt','cleanup-failure.txt','resource-table.json','resource-table.md','validation-stage.json','validation.stderr','validation.stdout']:
   if (e/name).exists():shutil.copyfile(e/name,O/name)
  samples=list(jl(e/'resources.jsonl'));du=list(jl(e/'du-root.jsonl'))
  def numeric(v):
   try:return int(v)
   except (TypeError,ValueError):return None
  anon=[];file=[]
  for s in samples:
   st=s.get('memory.stat','')
   if isinstance(st,str):
    st=dict(x.split() for x in st.splitlines() if len(x.split())==2)
   if isinstance(st,dict):
    if numeric(st.get('anon')) is not None:anon.append(int(st['anon']))
    if numeric(st.get('file')) is not None:file.append(int(st['file']))
  result['resource_supplement']={'sample_count':len(samples),'anon_sampled_peak':max(anon) if anon else 'UNKNOWN','file_sampled_peak':max(file) if file else 'UNKNOWN','du_samples':len(du),'du_timeout_count':sum(x.get('rc')==124 or x.get('timeout',False) for x in du),'du_nonzero_count':sum(x.get('rc')!=0 for x in du),'du_first_sample':du[:1]}
  R=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';builds=list((R/'home/abuild/rpmbuild/BUILD').glob('llvm-*/build'))
  mats=[];dest=W/'temp/local-full-r6-20261111-materials'/project
  for build in builds:
   work=build/'clang-bolt'
   if not work.exists():continue
   for p in work.iterdir():
    if p.is_file() and (p.name=='reference-relocs-clang-22' or p.name.endswith('.log') or p.name in ('identity.json','rewrite.json')):
     dest.mkdir(parents=True,exist_ok=True);target=dest/p.name
     if target.exists():raise RuntimeError('refuse existing material '+str(target))
     shutil.copyfile(p,target);s=sha(p);assert sha(target)==s
     mats.append({'source':str(p),'copy':str(target),'bytes':p.stat().st_size,'sha256':s})
  result['materials']=mats;result['BOLT_input_status']='copied' if any(Path(x['source']).name=='reference-relocs-clang-22' for x in mats) else 'UNKNOWN: input no longer present'
  save(O/'audit.json',result);results[project]=result
  print('AUDIT 已结束',now(),project,'status=recorded',flush=True)
 save(E/'audit-summary.json',results)
finally:
 print('AUDIT_ALL 已结束',now(),flush=True)
