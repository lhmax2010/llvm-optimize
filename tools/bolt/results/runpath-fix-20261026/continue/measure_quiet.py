# Environmental repeat: full balanced rounds, retaining every original sample.
"""One compile at a time, fixed CPU/ASLR, unchanged preprocessed inputs."""
from pathlib import Path
import os,sys,json,hashlib,shutil,subprocess,time,threading,signal,statistics,math,re,datetime,traceback
from common import *
OLD=BASE.parent/'perf-c-o2-os-20261025';mode=sys.argv[1];assert mode in ('threeway','rss');label=mode+'-quiet-repeat';O=E/label;O.mkdir(exist_ok=True);P=X/label;P.mkdir(exist_ok=True);CPU=2
assert json.loads((BASE/'build-result.json').read_text())['exit_code']==0
assert json.loads((E/'objects-current/result.json').read_text())['passed']==90
if mode=='threeway':assert json.loads((E/'objects-oldtext/result.json').read_text())['passed']==90
roles={'ordinary':WORK/'ordinary-clang-22','candidate':WORK/'clang.candidate'}
if mode=='threeway':roles['oldtext']=D/'old-text/clang.candidate'

def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def save(p,v):
 tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(v,indent=2)+'\n');tmp.replace(p)
def read(p):
 try:return Path(p).read_text().strip()
 except OSError:return 'unavailable'
def condition():return {'time_ns':time.time_ns(),'loadavg':read('/proc/loadavg'),'frequency_kHz':read(f'/sys/devices/system/cpu/cpu{CPU}/cpufreq/scaling_cur_freq'),'home_free':shutil.disk_usage('/home').free}

def main():
 assert not (O/'samples.jsonl').exists(),'new run only'
 assert CPU in os.sched_getaffinity(0)
 assert subprocess.check_output(['setarch','x86_64','-R','cat','/proc/self/personality'],text=True).strip()=='00040000'
 cases=[u for u in json.loads((OLD/'cases.json').read_text()) if u['language']=='C++' and u['option']=='-O2']+[u for u in json.loads((OLD/'clean-c/cases.json').read_text()) if u['option']=='-O2']
 if mode=='threeway':cases=[u for u in cases if u['target']!='aarch64-tizen-linux-gnu']
 assert len(cases)==(80 if mode=='threeway' else 120),len(cases)
 oldroot=json.loads((OLD/'config.json').read_text())['root']
 for u in cases:
  assert sha(u['input'])==u['input_sha256']
  u['argv']=[('-resource-dir='+str(BUILD/'lib64/clang/22') if a.startswith('-resource-dir=') else a.replace(oldroot,str(R)) if a.startswith('--sysroot=') else a) for a in u['argv']]
  u['argv'][u['argv'].index('-o')+1]=str(P/'same.o')
 save(O/'cases.json',cases)
 compiler_sha={r:sha(p) for r,p in roles.items()}
 loader=[str(R/'lib64/ld-linux-x86-64.so.2'),'--library-path',str(R/'lib64')+':'+str(R/'usr/lib64')]
 conditions={'start':datetime.datetime.now().astimezone().isoformat(),'mode':mode,'cpu':CPU,'parallel_compiles':1,'ASLR':'setarch x86_64 -R; personality=00040000','governor':read(f'/sys/devices/system/cpu/cpu{CPU}/cpufreq/scaling_governor'),'driver':read(f'/sys/devices/system/cpu/cpu{CPU}/cpufreq/scaling_driver'),'cpuinfo':read('/proc/cpuinfo'),'roles':{r:{'path':str(p),'sha256':compiler_sha[r]} for r,p in roles.items()},'loader':loader,'outliers_removed':False,'order':'per-round roles ordinary/candidate/oldtext (reverse on odd rounds); same ordered cases per role','timer':'monotonic_ns around blocking Popen.wait, watchdog separate; copies/fsync/hashes outside timer','RSS':'host /usr/bin/time -v per invocation, maximum resident set size in KiB' if mode=='rss' else 'not collected in timing experiment'}
 save(O/'conditions.json',conditions);(O/'processes-before.txt').write_text(subprocess.check_output(['ps','-eo','pid,pcpu,comm,args','--sort=-pcpu'],text=True))
 slot=P/'clang-22';slot.touch();inode=slot.stat().st_ino;refs={};rows=[];(O/'logs').mkdir(exist_ok=True);(P/'objects').mkdir(exist_ok=True)
 for iteration in ([3,4] if mode=='threeway' else [0]):
  order=list(roles) if iteration%2==0 else list(reversed(roles))
  for role in order:
   shutil.copyfile(roles[role],slot);slot.chmod(0o755)
   with slot.open('rb') as f:os.fsync(f.fileno())
   assert sha(slot)==compiler_sha[role] and slot.stat().st_ino==inode
   for index,u in enumerate(cases):
    if shutil.disk_usage('/home').free<20*1024**3:raise RuntimeError('home free below 20 GiB')
    tag=f'{iteration}-{role}-{index:03d}';out=P/'same.o';out.unlink(missing_ok=True)
    argv=['taskset','-c',str(CPU),'setarch','x86_64','-R',*loader,str(slot),*u['argv']]
    if mode=='rss':argv=['/usr/bin/time','-v','-o',str(O/'logs'/f'{tag}.time'),*argv]
    before=condition()
    with (O/'logs'/f'{tag}.log').open('wb') as log:
     start=time.monotonic_ns();p=subprocess.Popen(argv,cwd=P,stdout=log,stderr=subprocess.STDOUT,start_new_session=True,env={**os.environ,'LC_ALL':'C'})
     def kill():
      try:os.killpg(p.pid,signal.SIGKILL)
      except ProcessLookupError:pass
     watchdog=threading.Timer(900,kill);watchdog.daemon=True;watchdog.start();rc=p.wait();end=time.monotonic_ns();watchdog.cancel()
    after=condition();actual=sha(out) if out.is_file() else None
    rss=None
    if mode=='rss':
     text=(O/'logs'/f'{tag}.time').read_text();m=re.search(r'Maximum resident set size \(kbytes\): (\d+)',text);rss=int(m[1]) if m else None
    if index not in refs:
     assert rc==0 and actual # First role is reference; all roles including ordinary are compared.
     shutil.copyfile(out,P/'objects'/f'{index:03d}.o');refs[index]=actual
    equal=actual==refs[index] and out.is_file() and out.read_bytes()==(P/'objects'/f'{index:03d}.o').read_bytes()
    row={'round':iteration,'role':role,'index':index,'language':u['language'],'target':u['target'],'name':u['name'],'wall_s':(end-start)/1e9,'max_rss_KiB':rss,'rc':rc,'byte_equal':equal,'object_sha256':actual,'compiler_inode':inode,'compiler_sha256':compiler_sha[role],'before':before,'after':after,'argv':argv,'log':'logs/'+tag+'.log'}
    with (O/'samples.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
    rows.append(row);save(O/'progress.json',{'completed':len(rows),'total':len(cases)*(2 if mode=='threeway' else 1)*len(roles),'last':row});print(mode,tag,round(row['wall_s'],5),'RSS',rss,'equal',equal,flush=True)
    assert rc==0 and equal and (rss is not None if mode=='rss' else True),(tag,rc,'object/RSS gate failed')
 metric='max_rss_KiB' if mode=='rss' else 'wall_s';per=[]
 for i,u in enumerate(cases):
  values={r:statistics.median(x[metric] for x in rows if x['index']==i and x['role']==r) for r in roles}
  per.append({'index':i,'language':u['language'],'target':u['target'],'name':u['name'],'medians':values,'ratios':{r:values[r]/values['ordinary'] for r in roles if r!='ordinary'}})
 summary=[]
 for language,target in sorted({(u['language'],u['target']) for u in cases}):
  selected=[x for x in per if (x['language'],x['target'])==(language,target)]
  summary.append({'language':language,'target':target,'files':len(selected),'metric':metric,'ratios':{r:math.exp(statistics.mean(math.log(x['ratios'][r]) for x in selected)) for r in roles if r!='ordinary'}})
 save(O/'per-file.json',per);save(O/'summary.json',summary);save(O/'result.json',{'PASS':True,'compiles':len(rows),'end':datetime.datetime.now().astimezone().isoformat(),'summary':summary});(O/'processes-after.txt').write_text(subprocess.check_output(['ps','-eo','pid,pcpu,comm,args','--sort=-pcpu'],text=True))
if __name__=='__main__':
 try:main()
 except BaseException:
  (O/'failure.txt').write_text(traceback.format_exc());raise
