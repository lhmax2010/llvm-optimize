from common import *
import re,xml.etree.ElementTree as ET,datetime
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt')
local=json.loads((B/'tools/bolt/results/night-results-20261103/summary.json').read_text())
pat=re.compile(r'^\[\s*(\d+)s\]\s?')
def plain(s):return pat.sub('',s)
markers=['TIZEN_LLVM_NORMALIZED_FLAGS','TIZEN_LLVM_DROPPED_FLAGS','TIZEN_LLVM_FLAGS_WARNING','TIZEN_HYBRID_LINK_OK','BOLT_BUILDROOT_OK','BOLT_PROC_OK','BOLT_PROC_MISSING','BOLT_TOOL_DRY_RUN_BEGIN','BOLT_TOOL_DRY_RUN_END','BOLT_NINJA_EXIT_0','BOLT_REAL_GATE_PASS','BOLT_DEBUG_SYMBOLS_PASS','BOLT_DEBUGLINK_PASS','BOLT_PIPELINE_PASS','BOLT_COMPARE_ROOT_PASS','BOLT_CACHE_RELEASE','BOLT_POST_GATE_PASS','BOLT_DISK_REPORT','NATIVE_ARCHIVES_END']
out={'builds':{},'projects':{}};excerpt=[]
for bid in [1216409,1216410,1216412,1216413]:
 lines=(E/str(bid)/'overview.txt').read_text().splitlines();r=next(l for l in lines if l.startswith(str(bid)+'\t'));c=r.split('\t');secs=sum(int(v)*{'hour':3600,'minute':60,'second':1}[u] for v,u in re.findall(r'(\d+)\s+(hour|minute|second)',c[3]));out['builds'][str(bid)]={'status':c[1],'start':c[2],'duration_seconds':secs,'end_calculated':str(datetime.datetime.fromisoformat(c[2])+datetime.timedelta(seconds=secs)),'line':lines.index(r)+1,'raw':r}
for bid,proj in [(1216409,'toolchain'),(1216410,'basedev')]:
 r={'project':proj,'arch':{}};out['projects'][str(bid)]=r
 manifest=ET.fromstring((E/str(bid)/'manifest.xml').read_bytes());r['manifest_llvm']=[p.attrib for p in manifest.findall('.//project') if p.get('name')=='platform/upstream/llvm'];assert r['manifest_llvm'][0]['revision']=='9e39fa8a61392652bb28b75fc26216675bcad1d5'
 for arch in ['x86_64','armv7l','aarch64']:
  p=D/f'{bid}-{arch}.log';lines=p.read_text().splitlines();rec={'bytes':p.stat().st_size,'lines':len(lines),'start':[],'end':[],'rpm_files':[],'exit0':[]};r['arch'][arch]=rec
  for i,l in enumerate(lines,1):
   if 'started "build llvm.spec" at' in l:rec['start'].append({'line':i,'raw':l})
   if 'finished "build llvm.spec" at' in l:rec['end'].append({'line':i,'raw':l})
   if re.search(r'^\[\s*\d+s\] \+ exit 0$',l):rec['exit0'].append({'line':i,'raw':l})
   if 'Wrote: ' in l:rec['rpm_files'].append({'line':i,'raw':l,'file':l.rsplit('/',1)[-1]})
  excerpt.append(f'=== {bid}/{arch}/llvm.buildlog.txt ===')
  excerpt.extend(f'L{x["line"]}: {x["raw"]}' for x in rec['start']+rec['end']+rec['exit0'][-2:])
  if arch!='x86_64':continue
  rec['anchors']={m:[] for m in markers};rec['find_debuginfo']=[];rec['pipeline']=None;rec['profile_raw']=[];rec['json_records']=[]
  gaps=[];prev=None
  for i,l in enumerate(lines,1):
   s=plain(l);m=pat.match(l)
   if m:
    sec=int(m[1])
    if prev:gaps.append({'start_line':prev[0],'end_line':i,'seconds':sec-prev[1]})
    prev=(i,sec)
   if s.startswith('+'):continue
   for key in markers:
    if s==key or s.startswith(key+' ') or s.startswith('{"'+key+'"'):
     rec['anchors'][key].append({'line':i,'seconds':int(m[1]) if m else None,'raw':l})
   if s.startswith('{'):
    try:
     j=json.loads(s);rec['json_records'].append({'line':i,'keys':list(j)})
     if 'counts' in j and 'profile_sha256' in j:
      rec['pipeline']=j;rec['pipeline_line']=i;rec['profile_raw'].append({'line':i,'raw':l});save(f'{bid}/pipeline.json',json.dumps(j,indent=2)+'\n')
     if 'planned' in j or 'counts' in j or 'ninja_diagnostics' in j:save(f'{bid}/json-L{i}.json',json.dumps(j,indent=2)+'\n')
    except json.JSONDecodeError:pass
  for i,l in enumerate(lines,1):
   if any(x in l for x in ['find-debuginfo','extracting debug info from','debugfiles.list','debugsourcefiles.list','clang-22.debug']):rec['find_debuginfo'].append({'line':i,'raw':l})
  excerpt.extend(f'L{x["line"]}: {x["raw"]}' for seq in rec['anchors'].values() for x in seq)
  excerpt.extend(f'L{x["line"]}: {x["raw"]}' for x in rec['profile_raw']+rec['find_debuginfo'])
  # Full dry-run original section, including shell trace, unmodified.
  lo=rec['anchors']['BOLT_TOOL_DRY_RUN_BEGIN'][0]['line'];hi=rec['anchors']['BOLT_TOOL_DRY_RUN_END'][0]['line'];save(f'{bid}/tool-dry-run.txt','\n'.join(f'L{i}: {lines[i-1]}' for i in range(lo,hi+1))+'\n')
  rec['top_gaps']=sorted(gaps,key=lambda x:-x['seconds'])[:10]
  for g in rec['top_gaps']:g['start_raw']=lines[g['start_line']-1];g['end_raw']=lines[g['end_line']-1]
  flags=[plain(x['raw']) for key in markers[:3] for x in rec['anchors'][key]]
  lflags=[plain(x['text']) for x in local[proj]['flags']]
  r['flags_compare']={'qb':flags,'local':lflags,'exact_equal':flags==lflags,'qb_warning_count':len(rec['anchors'][markers[2]]),'local_warning_count':local[proj]['warning_count']}
  lp=W/f'temp/night-20261103/{proj}/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt/identity.json';ident=json.loads(lp.read_text())
  # Canonical local log, read-only; avoid huge accumulator.
  lcounts=None
  with Path(local[proj]['log_source']).open() as f:
   for l in f:
    s=plain(l)
    if s.startswith('{"tool_sha256"'):
     j=json.loads(s);lcounts=j['counts']
  r['counts_compare']={'qb':rec['pipeline']['counts'],'local':lcounts,'exact_equal':rec['pipeline']['counts']==lcounts}
  qnames=sorted(re.sub(r'-22\.1\.8-[^-]+\.(x86_64|noarch)\.rpm$','',x['file']) for x in rec['rpm_files'] if not x['file'].endswith('.src.rpm'))
  lnames=sorted(x for x in local[proj]['rpm_names'] if x!='llvm [src]')
  r['rpm_names_compare']={'qb':qnames,'local':lnames,'exact_equal':qnames==lnames,'qb_only':sorted(set(qnames)-set(lnames)),'local_only':sorted(set(lnames)-set(qnames))}
(E/'analysis.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
save('excerpts.txt','\n'.join(excerpt)+'\n')
for b,r in out['projects'].items():print(b,'flags',r['flags_compare'],'counts',r['counts_compare'],'rpms',r['rpm_names_compare'],flush=True)
