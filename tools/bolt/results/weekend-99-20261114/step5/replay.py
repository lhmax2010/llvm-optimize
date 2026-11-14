from pathlib import Path
import os,sys,json,hashlib,importlib.util,subprocess,shlex,time,datetime,threading,traceback,collections
E=Path(__file__).parent; B=E.parents[4]; W=Path('/home/linhao/Toolchain/development/llvm-optimize')
X=W/'temp/weekend99-replay-20261114'; X.mkdir(exist_ok=False)
UNIT='weekend99-step5-20261114.service'; started=time.monotonic(); done=threading.Event(); stage='preflight'
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def load(name,p):
 spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
def dump(name,obj): (E/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def now():return datetime.datetime.now().astimezone().isoformat()
cg=Path('/sys/fs/cgroup'+subprocess.check_output(['systemctl','--user','show',UNIT,'-p','ControlGroup','--value'],text=True).strip())
def guard():
 with (E/'runtime-samples.jsonl').open('a') as f:
  while not done.is_set():
   mem=int(next(l.split()[1] for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemAvailable:')))*1024
   disk=os.statvfs('/home');free=disk.f_bavail*disk.f_frsize
   size=0
   for root,dirs,files in os.walk(X):
    for name in files:
     try:size+=(Path(root)/name).stat().st_size
     except FileNotFoundError:pass
   procs=[]
   for pid in (cg/'cgroup.procs').read_text().split():
    try:
     p=Path('/proc')/pid;status=(p/'status').read_text();hwm=next((l for l in status.splitlines() if l.startswith('VmHWM:')),None)
     procs.append({'pid':int(pid),'hwm':hwm,'argv':(p/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace')})
    except (FileNotFoundError,ProcessLookupError,PermissionError):pass
   heavy=[]
   for p in Path('/proc').iterdir():
    if p.name.isdigit():
     try:
      comm=(p/'comm').read_text().strip()
      if comm in ('gbs','rpmbuild','ninja','llvm-bolt'):heavy.append({'pid':int(p.name),'comm':comm})
     except (FileNotFoundError,ProcessLookupError,PermissionError):pass
   reasons=[]
   if mem<6*2**30:reasons.append('MemAvailable-below-6GiB')
   if free<30*2**30:reasons.append('home-below-30GiB')
   if size>5*2**30:reasons.append('output-over-5GiB')
   if time.monotonic()-started>=7200:reasons.append('runtime-120min')
   if heavy:reasons.append('another-heavy-process-started')
   row={'time':now(),'stage':stage,'elapsed':time.monotonic()-started,'MemAvailable':mem,'home_available':free,'output_bytes':size,'memory_peak':(cg/'memory.peak').read_text().strip(),'memory_events':(cg/'memory.events').read_text(),'processes':procs,'heavy':heavy,'stop_reasons':reasons}
   f.write(json.dumps(row)+'\n');f.flush()
   if reasons:
    dump('watchdog-stop.json',row);print('99步骤5 已结束',now(),'status=STOP',reasons,flush=True)
    subprocess.run(['systemctl','--user','stop','--no-block',UNIT],check=False);return
   done.wait(30)
thread=threading.Thread(target=guard,daemon=True);thread.start()
result={'status':'STOP','source':'b0c1732c08c5a81382f9eeef27ffe1e40c6c47d1','shipping':{},'debug':{},'start':now()}
try:
 old=load('old_converter',E/'old-converter.py');new=load('new_converter',E/'new-converter.py')
 # The product startup logger is exercised without rewriting it.
 new.log_startup_context()
 R=W/'temp/night-20261105/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';BUILD=R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build'
 assert (BUILD/'CMakeCache.txt').is_file()
 build=X/'build';build.mkdir();(build/'CMakeCache.txt').write_bytes((BUILD/'CMakeCache.txt').read_bytes())
 tools=X/'tools';tools.mkdir();paths={};ident={}
 for name in ('clang-22','llvm-dis','llvm-nm'):
  binary=R/'usr/bin'/name;assert binary.is_file()
  argv=[str(R/'lib64/ld-linux-x86-64.so.2'),'--library-path',str(R/'lib64')+':'+str(R/'usr/lib64'),str(binary)]
  wrapper=tools/name;wrapper.write_text('#!/bin/sh\nexec '+shlex.join(argv)+' "$@"\n');wrapper.chmod(0o755);paths[name]=wrapper;ident[name]={'path':str(binary),'sha256':sha(binary),'argv':argv}
 dump('tool-identities.json',ident)
 assets=json.loads((B/'tools/bolt/results/disk-cleanup-20261114/replay-assets-current.json').read_text())
 for project in ('toolchain','basedev'):
  stage='shipping-'+project;root=Path(assets[project]['path']);archives=sorted(root.rglob('*.a'));assert len(archives)==225
  rows=[];members=checked=0
  with (E/('shipping-'+project+'-members.jsonl')).open('w') as evidence:
   for i,path in enumerate(archives):
    a=old.validate_archive(path);b=new.validate_archive(path);assert a==b,(path,'inspect changed');assert b['bitcode']==0 and b['other']==0
    with path.open('rb') as f:
     for member in b['members']:
      f.seek(member['offset']);data=f.read(member['size']);assert hashlib.sha256(data).hexdigest()==member['sha256']
      assert old.elf_details(data)==new.elf_details(data),(path,member['name'],'elf_details')
      prior=old.pic_relocations(data);current=new.pic_relocations(data);assert prior==current,(path,member['name'],'pic_relocations',prior,current)
      assert not current['forbidden'],(path,member['name'],current)
      members+=1;checked+=current['checked']
      evidence.write(json.dumps({'archive':str(path.relative_to(root)),'ordinal':member['ordinal'],'name':member['name'],'sha256':member['sha256'],'new_old_equal':True,'checked':current['checked']})+'\n')
    rows.append({'path':str(path),'sha256':b['sha256'],'bytes':b['bytes'],'members':b['member_count'],'same_inspect':True})
    if i%25==0:print('SHIPPING_CHECK',project,i+1,'members',members,now(),flush=True)
  assert members==3864
  # Preserve the product's already-native behavior: convert scans/skips, does not rewrite inputs.
  summary=new.convert(root,X/('native-'+project),paths['clang-22'],paths['llvm-dis'],paths['llvm-nm'],build,jobs=2,debug_info='yes' if project=='toolchain' else 'no')
  assert summary['status']=='CONVERTED' and summary['native_archives_skipped']==225 and summary['native_members_preserved']==3864 and not summary['archives']
  for r in rows:assert sha(r['path'])==r['sha256'],r['path']
  result['shipping'][project]={'archives':225,'members':members,'historical_converted':3853,'historical_native':11,'checked_relocations':checked,'byte_unchanged':True,'newly_codegen_members':0,'native_skip_summary':str(X/('native-'+project)/'summary.json')}
  dump('shipping-'+project+'-archives.json',rows);dump('progress.json',result)
 stage='debug-conversion'
 inputs=json.loads((B/'tools/bolt/results/fifth-review-20261111/rerun3/debug-inputs.json').read_text());root=Path(assets['debug_inputs']['path']);assert len(list(root.glob('*.a')))==10
 for r in inputs:assert sha(r['copy'])==r['sha256'] and Path(r['copy']).stat().st_size==r['bytes']
 summary=new.convert(root,X/'debug',paths['clang-22'],paths['llvm-dis'],paths['llvm-nm'],build,jobs=2,debug_info='yes')
 assert summary['status']=='CONVERTED';assert sum(r['converted'] for r in summary['archives'])==1093;assert sum(r['preserved'] for r in summary['archives'])==7
 stage='debug-comparison';rows=[]
 references={Path(r['path']).name:Path(r['path']) for r in assets['outputs'] if r['side']=='new'}
 for r in summary['archives']:
  out=X/'debug/archives'/r['path'];prior=references[out.name];a=new.inspect(out);b=new.inspect(prior)
  assert a['sha256']==b['sha256'] and a['bytes']==b['bytes'],(out,prior,a['sha256'],b['sha256'])
  assert {k:v for k,v in a.items() if k!='path'}=={k:v for k,v in b.items() if k!='path'},out
  assert all(x['sha256']==y['sha256'] for x,y in zip(a['members'],b['members']))
  rows.append({'archive':out.name,'input':str(root/out.name),'input_sha256':sha(root/out.name),'output':str(out),'reference':str(prior),'sha256':a['sha256'],'bytes':a['bytes'],'converted':r['converted'],'preserved':r['preserved'],'members':a['member_count'],'byte_identical':True})
  print('DEBUG_IDENTICAL',out.name,a['sha256'],flush=True)
 dump('debug-output-comparison.json',rows)
 result['debug']={'archives':10,'members':1100,'converted':1093,'preserved':7,'byte_identical':True,'reference':'78 rerun3/rerun4 retained new outputs (fea0fe46)'}
 result['status']='PASS';result['coverage_note']='450 shipping archives cover 3853 previously converted +11 native members per project; they are already ELF, so convert preserves/skips them. All ELF members rerun both PIC/detail checks. The 10 genuine bitcode archives regenerate 1093 converted members, not 3853.'
except BaseException:
 result['failure']=traceback.format_exc();print(result['failure'],flush=True)
finally:
 done.set();thread.join();result['end']=now();result['seconds']=time.monotonic()-started;result['memory_peak']=(cg/'memory.peak').read_text().strip();result['memory_events']=(cg/'memory.events').read_text();dump('result.json',result)
 print('99步骤5 已结束',result['end'],'status='+result['status'],flush=True)
sys.exit(0 if result['status']=='PASS' else 1)
