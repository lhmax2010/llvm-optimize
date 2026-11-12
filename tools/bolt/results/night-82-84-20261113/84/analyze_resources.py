from pathlib import Path
import re,json,gzip,hashlib,datetime,collections
B=Path(__file__).resolve().parents[5];E=Path(__file__).resolve().parent
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
T_SNAP='tizen-base-toolchain_20261030.061318';D_SNAP='tizen-base-dev_20261030.061217'
sources=[
 ('63-T','local','Toolchain','9e39fa8a61392652bb28b75fc26216675bcad1d5',T_SNAP,B/'tools/bolt/results/qb-snapshot-rebuild-20261105/completed/gbs-original-0.log.gz',W/'temp/night-20261105/toolchain',B/'tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence'),
 ('74-T','local','Toolchain','fea0fe464d56e17f2c7588c557bfffd9f6ac352b',T_SNAP,B/'tools/bolt/results/local-full-r6-20261111/toolchain/original-build.log.gz',W/'temp/rebase-359934-20261111-r6/toolchain',B/'tools/bolt/results/local-full-r6-20261111/toolchain'),
 ('74-D','local','Base-Dev','fea0fe464d56e17f2c7588c557bfffd9f6ac352b',D_SNAP,B/'tools/bolt/results/local-full-r6-20261111/basedev/original-build.log.gz',W/'temp/rebase-359934-20261111-r6/basedev',B/'tools/bolt/results/local-full-r6-20261111/basedev')]
for folder,ids,commit in [('qb-1216409-1216410',[1216409,1216410],'9e39fa8a61392652bb28b75fc26216675bcad1d5'),('qb-1225393-1225395',[1225393,1225395],'60fabc723f30c5cc04146a9dd83487ebed63f259'),('qb-1226850-1226851',[1226850,1226851],'fea0fe464d56e17f2c7588c557bfffd9f6ac352b')]:
 for i,q in enumerate(ids):sources.append((str(q),'QB','Toolchain' if i==0 else 'Base-Dev',commit,T_SNAP if i==0 else D_SNAP,B/'tools/bolt/results'/folder/str(q)/'x86_64/llvm.buildlog.txt.gz',None,None))
seen={}
def opening(p):return gzip.open(p,'rt',errors='replace') if p.suffix=='.gz' else p.open(errors='replace')
def provenance(p):
 p=Path(p);key=str(p)
 if key not in seen:
  with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
  seen[key]={'path':key,'bytes':p.stat().st_size,'sha256':h}
 return key
def rows(p):
 provenance(p)
 with opening(p) as f:
  for i,line in enumerate(f,1):yield i,json.loads(line)
def loc(p,n,record=None):
 return {'file':str(p),'line':n,**({'time_ns':record['time_ns']} if record and 'time_ns' in record else {})}
def analyze(src):
 id,env,project,commit,snapshot,path,base,sampledir=src
 out=E/id;out.mkdir(exist_ok=False)
 provenance(path)
 records=[]
 with opening(path) as f:
  for no,line in enumerate(f,1):
   m=re.match(r'^\[\s*(\d+)s\]\s?(.*)',line.rstrip('\n'))
   if m:records.append({'line':no,'seconds':int(m[1]),'text':m[2],'raw':line.rstrip('\n')})
 def first(pattern,after=0):
  return next((r for r in records if r['line']>after and re.search(pattern,r['text'])),None)
 def last(pattern,after=0):
  found=[r for r in records if r['line']>after and re.search(pattern,r['text'])]
  return found[-1] if found else None
 phases={};anchors={}
 def interval(name,start,end,why='explicit GBS boundaries'):
  if not start or not end:
   phases[name]={'seconds':'UNKNOWN','reason':'missing explicit start/end timestamp'};return
  assert end['seconds']>=start['seconds'],(id,name,start,end)
  phases[name]={'seconds':end['seconds']-start['seconds'],'start':start,'end':end,'source':str(path),'basis':why}
  anchors[str(start['line'])]=start;anchors[str(end['line'])]=end
 cmake=first(r'^\+ cmake -G Ninja');cmake_end=first(r'^-- Build files have been written',cmake['line'] if cmake else 0)
 ninja=first(r'^\+ ninja .* -j|^\+ ninja -')
 nend=None
 if ninja:
  initial=first(r'^\[\d+/\d+\]',ninja['line'])
  total=re.match(r'^\[\d+/(\d+)\]',initial['text'])[1] if initial else None
  if total:nend=first(r'^\['+total+'/'+total+r'\]',ninja['line'])
 install=first(r'^Executing\(%install\)')
 begin=first(r'^BOLT_DISK_REPORT .*"stage": "begin"')
 configure=first(r'^\+ bolt_step configure ')
 confend=first(r'^-- Build files have been written',configure['line'] if configure else 999999)
 tool=first(r'^\+ bolt_checked tool-build ')
 toolend=first(r'^BOLT_NINJA_EXIT_0$')
 pipeline=first(r'^\+ python3 .*clang-bolt-helper.py pipeline ')
 pipeend=first(r'^BOLT_PIPELINE_PASS$')
 compare=first(r'^\+ python3 .*clang-bolt-helper.py compare-root ')
 compareend=first(r'^BOLT_COMPARE_ROOT_PASS$')
 cache=first(r'^\+ .*clang-bolt-helper.py cache-release ')
 cacheend=first(r'^BOLT_CACHE_RELEASE ')
 conversion=first(r'^NATIVE_ARCHIVES_BEGIN ')
 convend=first(r'^NATIVE_ARCHIVES_END ')
 post=first(r'^\+ /usr/lib/rpm/find-debuginfo.sh ')
 postgate=first(r'^\+ python3 .*clang-bolt-helper.py post ')
 postgateend=first(r'^BOLT_POST_GATE_PASS$')
 packaging=first(r'^Processing files:')
 wrote=last(r'^Wrote:')
 interval('cmake',cmake,cmake_end)
 interval('ordinary_ninja_including_links',ninja,nend)
 interval('ordinary_install',install,begin)
 interval('BOLT_total',begin,compareend)
 interval('BOLT_reconfigure',configure,confend)
 interval('BOLT_tool_build',tool,toolend)
 interval('BOLT_pipeline',pipeline,pipeend)
 interval('BOLT_compare_root',compare,compareend)
 interval('cache_release',cache,cacheend)
 interval('archive_conversion',conversion,convend)
 interval('platform_post_before_BOLT_post_gate',post,postgate)
 interval('BOLT_post_gate',postgate,postgateend)
 interval('packaging',packaging,wrote)
 for name in ['BOLT_relink','BOLT_reference_strip','BOLT_candidate_strip','BOLT_rewrite','BOLT_RUNPATH','BOLT_tiny_gate','BOLT_security_gate']:
  phases[name]={'seconds':'UNKNOWN','reason':'no isolated start/end in preserved command logs; no inference from adjacent stdout gaps'}
 # Individual helper monotonic durations, distinct from whole command duration.
 for r in records:
  text=r['text'];values=[]
  if text.startswith('BOLT_REAL_GATE_PASS '):
   d=json.loads(text.split(' ',1)[1]);tag='prestrip' if 'prestrip' in d['work'] else 'preinstall' if 'preinstall' in d['work'] else 'post'
   values.append(('BOLT_real_gate_'+tag,d['seconds'],'BOLT_REAL_GATE_PASS.seconds'))
  elif text.startswith('{"BOLT_DEBUG_SYMBOLS_PASS":'):
   d=json.loads(text)['BOLT_DEBUG_SYMBOLS_PASS'];values.append(('BOLT_debug_symbols',d['seconds'],'BOLT_DEBUG_SYMBOLS_PASS.seconds'))
  elif text.startswith('{"BOLT_DEBUGLINK_PASS":'):
   d=json.loads(text)['BOLT_DEBUGLINK_PASS']
   if 'debuglink_seconds' in d:values.append(('BOLT_debuglink',d['debuglink_seconds'],'BOLT_DEBUGLINK_PASS.debuglink_seconds'))
  for name,seconds,field in values:
   phases[name]={'seconds':seconds,'source':str(path),'line':r['line'],'sample':r,'basis':field}
   anchors[str(r['line'])]=r
 target_patterns={'clang':r'^Linking CXX executable bin/clang-22$','libLLVM.so':r'^Linking CXX shared library lib64/libLLVM\.so\.', 'libclang-cpp.so':r'^Linking CXX shared library lib64/libclang-cpp\.so\.', 'lld':r'^Linking CXX executable bin/lld$', 'liblldb':r'^Linking CXX shared library lib64/liblldb\.so\.'}
 links={}
 for name,pat in target_patterns.items():
  rec=next((r for r in records if re.search(pat,re.sub(r'^\[\d+/\d+\] ','',r['text']))),None)
  links[name]={'seconds':'UNKNOWN','reason':'Ninja stdout provides completion time, not start','completion':rec,'log_source':str(path)}
  if rec:anchors[str(rec['line'])]=rec
 disk_reports=[]
 for r in records:
  if r['text'].startswith('BOLT_DISK_REPORT '):
   d=json.loads(r['text'][17:]);disk_reports.append({'source':str(path),'line':r['line'],'gbs_seconds':r['seconds'],'data':d})
 memory={'memory_peak':'UNKNOWN','events':'UNKNOWN','max_process_VmHWM':'UNKNOWN','anon':'UNKNOWN','file':'UNKNOWN'}
 disk={'root_peak':'UNKNOWN','major_directories':'UNKNOWN'}
 ninjapath=None
 if base:
  root=base/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build'
  ninjapath=root/'.ninja_log'
  if ninjapath.exists():
   provenance(ninjapath)
   with ninjapath.open('rb') as fi,gzip.open(out/'ninja.log.gz','wb') as fo:
    import shutil;shutil.copyfileobj(fi,fo)
   mapping={'bin/clang-22':'clang','bin/lld':'lld','lib64/libLLVM.so.22.1':'libLLVM.so','lib64/libclang-cpp.so.22.1':'libclang-cpp.so','lib64/liblldb.so.22.1.8':'liblldb'}
   with ninjapath.open() as f:
    for no,line in enumerate(f,1):
     fields=line.rstrip('\n').split('\t')
     if len(fields)==5 and fields[3] in mapping:
      name=mapping[fields[3]]
      assert links[name]['seconds']=='UNKNOWN','multiple Ninja log entries: needs disambiguation'
      links[name].update(seconds=(int(fields[1])-int(fields[0]))/1000,ninja_start_ms=int(fields[0]),ninja_end_ms=int(fields[1]),ninja_source=str(ninjapath),ninja_line=no,ninja_raw=line.rstrip(),basis='Ninja task interval, not exclusive wall contribution')
  resource=sampledir/'resources.jsonl.gz'
  if not resource.exists():resource=sampledir/'resources.jsonl'
  samples=list(rows(resource))
  peak=[(int(d['memory.peak']),no,d) for no,d in samples if str(d.get('memory.peak','')).strip().isdigit()]
  best=max(peak,key=lambda x:x[0])
  events={}
  for no,d in samples:
   for line in d.get('memory.events','').splitlines():
    v=line.split()
    if len(v)==2 and v[1].isdigit():events[v[0]]=max(events.get(v[0],0),int(v[1]))
  final=sampledir/'build-result.json'
  if not final.exists():final=base/'evidence/build-result.json'
  memory.update(memory_peak=best[0],peak_source=loc(resource,best[1],best[2]),events=events,resource_samples=len(samples),first_sample=loc(resource,samples[0][0],samples[0][1]),last_sample=loc(resource,samples[-1][0],samples[-1][1]),events_scope='per-key maxima from full raw sample series')
  if final.exists():
   provenance(final);data=json.loads(final.read_text())
   (out/'build-result.json').write_text(json.dumps(data,indent=2)+'\n')
   stats=data.get('stats',{})
   if 'memory.peak' in stats:memory.update(memory_peak=int(stats['memory.peak']),memory_max=int(stats['memory.max']) if stats.get('memory.max','').strip().isdigit() else 'UNKNOWN',peak_final_file=str(final),peak_final_field='stats.memory.peak',events={k:int(v) for k,v in (l.split() for l in stats['memory.events'].splitlines())},build_seconds=data.get('seconds'))
  memory['truncated']=bool(memory['events'].get('max',0)>0 or memory['memory_peak']==memory.get('memory_max'))
  memory['time_note']='受内存回收影响' if memory['truncated'] else '未观测到memory.events max触顶'
  du=sampledir/'du-root.jsonl.gz'
  if not du.exists():du=sampledir/'du-root.jsonl'
  dus=list(rows(du));valid=[]
  for no,d in dus:
   if d.get('rc')==0 and re.match(r'^\d+\s',d.get('stdout','')):valid.append((int(d['stdout'].split()[0]),no,d))
  if valid:
   peakdu=max(valid,key=lambda x:x[0])
   disk={'root_peak':peakdu[0],'source':loc(du,peakdu[1],peakdu[2]),'raw':peakdu[2],'samples':len(dus),'successful_samples':len(valid),'timeouts':sum(d.get('rc')==124 for _,d in dus),'nonzero_or_missing':sum(d.get('rc')!=0 for _,d in dus),'major_directories':'UNKNOWN: du measured / total only; BOLT-owned scopes below are separate measurements','scope':'maximum successful du -sx -B1 / samples, not guaranteed instantaneous peak'}
  proc=sampledir/'bolt-process.jsonl.gz'
  if not proc.exists():proc=sampledir/'bolt-process.jsonl'
  if proc.exists():
   procs=list(rows(proc));argv={d['pid']:d.get('argv') for _,d in procs if d.get('event')=='found'}
   vals=[(int(d['VmHWM'].split()[0])*1024,no,d) for no,d in procs if re.match(r'^\d+ kB$',d.get('VmHWM',''))]
   if vals:
    v=max(vals,key=lambda x:x[0]);memory['llvm_bolt_VmHWM']={'bytes':v[0],'source':loc(proc,v[1],v[2]),'command':argv.get(v[2]['pid']),'scope':'only llvm-bolt sampled; maximum over all build processes UNKNOWN'}
  # Current memory samples in exact phase windows, inclusive one-second GBS precision.
  report=sampledir/'resource-table.json'
  if report.exists():
   provenance(report);rep=json.loads(report.read_text());epoch=rep.get('log_source',{}).get('epoch_zero')
   if epoch is not None:
    def sampled(start,end):
     found=[(int(d['memory.current']),no,d) for no,d in samples if 'memory.current' in d and str(d['memory.current']).strip().isdigit() and start*1e9<=d['time_ns']<=end*1e9]
     if not found:return 'UNKNOWN'
     v=max(found,key=lambda x:x[0]);return {'bytes':v[0],'source':loc(resource,v[1],v[2]),'scope':'whole cgroup in overlapping task window; not exclusive task/process memory'}
    for p in phases.values():
     if 'start' in p:p['cgroup_sampled_window_max']=sampled(epoch+p['start']['seconds'],epoch+p['end']['seconds'])
    if ninja:
     for p in links.values():
      if 'ninja_start_ms' in p:p['cgroup_sampled_window_max']=sampled(epoch+ninja['seconds']+p['ninja_start_ms']/1000,epoch+ninja['seconds']+p['ninja_end_ms']/1000)
 # selected complete raw log anchors, not truncated
 with (out/'anchors.txt').open('w') as f:
  for _,a in sorted(anchors.items(),key=lambda x:int(x[0])):f.write(str(a['line'])+': '+a['raw']+'\n')
 result={'id':id,'environment':env,'project':project,'commit':commit,'snapshot':snapshot,'log':str(path),'log_last_seconds':records[-1]['seconds'],'phases':phases,'thinlto_links':links,'memory':memory,'disk':disk,'BOLT_disk_reports':disk_reports}
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 print(id,'done; cmake',phases['cmake']['seconds'],'ninja',phases['ordinary_ninja_including_links']['seconds'],'convert',phases['archive_conversion']['seconds'],'peak',memory['memory_peak'],flush=True)
 return result
if __name__=='__main__':
 results=[]
 try:
  for s in sources:results.append(analyze(s))
  (E/'all-results.json').write_text(json.dumps(results,indent=2)+'\n')
 finally:
  (E/'read-inputs.json').write_text(json.dumps(list(seen.values()),indent=2)+'\n')
 print('已结束',datetime.datetime.now().astimezone().isoformat(),'resource-analysis PASS')
