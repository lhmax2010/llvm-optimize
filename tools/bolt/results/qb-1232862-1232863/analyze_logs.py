from pathlib import Path
import gzip,json,re,collections,datetime,hashlib
E=Path(__file__).resolve().parent;O=E.parent/'qb-1231417-1231418'
def save(name,obj):
 (E/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def striptime(s):return re.sub(r'^\[\s*\d+s\]\s?', '',s)
def norm(s):return re.sub(r'^\[\d+/\d+\]\s*','',striptime(s))
patterns={'WARNING':r'\bWARNING\b','warning_colon':r'warning:','error_colon':r'error:','error_word':r'\berror\b','not_found':r'not found','cancelled':r'cancelled','traceback':r'Traceback','segfault':r'segmentation fault','oom':r'out of memory|cannot allocate memory|killed process'}
regs={k:re.compile(v,re.I) for k,v in patterns.items()}
kw=re.compile('|'.join(patterns.values()),re.I)
cleanup=re.compile(r'live descendants|could not verify|cleanup deadline|drain deadline|session deadline|member read errors|scan incomplete|SESSION_TRANSIENT_ERRORS_RECOVERED|COMMAND_ERROR',re.I)
keys=['SESSION_KILL_MODE','NATIVE_ARCHIVES_STARTUP','BOLT_REAL_GATE_PASS','BOLT_POST_GATE_PASS','NATIVE_ARCHIVES_END','BOLT_DISK_REPORT']
def read(p):
 hits=[];diags=[];clean=[];critical={k:[] for k in keys};counts=collections.Counter();dcounts=collections.Counter()
 with gzip.open(p,'rt',errors='replace') as f:
  for n,s in enumerate(f,1):
   s=s.rstrip('\n');r={'line':n,'raw':s,'normalized':norm(s)}
   isprogress=bool(re.match(r'^\[\d+/\d+\]\s',striptime(s)))
   for k in keys:
    if k in s:critical[k].append(r)
   if cleanup.search(s):clean.append(r)
   if kw.search(s):
    hits.append(r)
    for k,reg in regs.items():
     if reg.search(s):counts[k]+=1
    if not isprogress:
     diags.append(r)
     for k,reg in regs.items():
      if reg.search(s):dcounts[k]+=1
 return {'file':str(p),'critical':critical,'keyword_hits':hits,'diagnostic_hits':diags,'cleanup_hits':clean,'keyword_counts':dict(counts),'diagnostic_counts':dict(dcounts)}
summary={}
for bid,oid in [('1232862','1231418'),('1232863','1231417')]:
 a=read(O/oid/'x86_64/llvm.buildlog.txt.gz');b=read(E/bid/'x86_64/llvm.buildlog.txt.gz')
 result={'baseline':oid,'old':a,'new':b}
 for field in ['keyword_hits','diagnostic_hits']:
  old=collections.Counter(r['normalized'] for r in a[field]);new=collections.Counter(r['normalized'] for r in b[field]);extra=new-old;remaining=extra.copy();rows=[]
  for r in b[field]:
   if remaining[r['normalized']]>0:rows.append(r);remaining[r['normalized']]-=1
  result['new_'+field]=rows;result['removed_'+field]=dict(old-new)
 with gzip.open(E/(bid+'-log-comparison.json.gz'),'wt') as f:json.dump(result,f,ensure_ascii=False,indent=2)
 critical=b['critical'];save(bid+'-critical-lines.json',critical)
 (E/(bid+'-critical-lines.txt')).write_text('\n'.join(k+'\n'+'\n'.join(str(r['line'])+': '+r['raw'] for r in rows) for k,rows in critical.items())+'\n')
 summary[bid]={'baseline':oid,'old_keyword_counts':a['keyword_counts'],'new_keyword_counts':b['keyword_counts'],'old_diagnostic_counts':a['diagnostic_counts'],'new_diagnostic_counts':b['diagnostic_counts'],'new_keyword_hits':result['new_keyword_hits'],'new_diagnostic_hits':result['new_diagnostic_hits'],'cleanup_hits':b['cleanup_hits'],'mode_occurrences':len(critical['SESSION_KILL_MODE']),'mode_values':sorted(set(re.findall(r'SESSION_KILL_MODE=(\w+)', '\n'.join(r['raw'] for r in critical['SESSION_KILL_MODE'])))),'mode_runtime_lines':sum(striptime(r['raw'])=='SESSION_KILL_MODE=pidfd' for r in critical['SESSION_KILL_MODE']),'real_gates':len(critical['BOLT_REAL_GATE_PASS']),'post_runtime_lines':sum(striptime(r['raw'])=='BOLT_POST_GATE_PASS' for r in critical['BOLT_POST_GATE_PASS']),'startup':[r for r in critical['NATIVE_ARCHIVES_STARTUP']]}
 print(bid,json.dumps(summary[bid],ensure_ascii=False),flush=True)
save('log-summary.json',summary)
end='LOGS 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status=COMPLETE';(E/'log-end.txt').write_text(end+'\n');print(end)
