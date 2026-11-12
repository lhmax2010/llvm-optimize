from pathlib import Path
import gzip,json,re,collections,datetime
E=Path(__file__).resolve().parent
def read(p):
 out={'flags':{},'stages':[],'reports':[],'alerts':[],'raw_profile':[]}
 with gzip.open(p,'rt') as f:
  for n,l in enumerate(f,1):
   raw=l.rstrip('\n');s=re.sub(r'^\[\s*\d+s\] ?','',raw)
   rec=dict(line=n,raw=raw,text=s)
   m=re.match(r'^\+ (CFLAGS|CXXFLAGS|LDFLAGS)=(.*)',s)
   if m:out['flags'][m[1]]=rec
   if re.search(r'WARNING|cancel|not found|BOLT_CANCELLED',s,re.I):out['alerts'].append(rec)
   if s.startswith(('BOLT_DISK_REPORT ','NATIVE_ARCHIVES_END ')):out['reports'].append(rec)
   if s.startswith('BOLT-INFO:') and re.search('profile|stale|invalid|function',s,re.I):out['raw_profile'].append(rec)
   if s.startswith('{'):
    try:j=json.loads(s)
    except ValueError:continue
    ident=j.get('identity',{})
    if 'strip_all_sha256' in ident:
     out['stages'].append(dict(line=n,strip_all=ident['strip_all_sha256'],RUNPATH=ident['rpath_adjusted_sha256'],final=ident['after_sha256']))
 return out
summary={}
for b,o in [('1226850','1225393'),('1226851','1225395')]:
 a=read(E.parent/'qb-1225393-1225395'/o/'x86_64/llvm.buildlog.txt.gz');z=read(E/b/'x86_64/llvm.buildlog.txt.gz')
 assert set(a['flags'])==set(z['flags'])=={'CFLAGS','CXXFLAGS','LDFLAGS'}
 assert {k:v['text'] for k,v in a['flags'].items()}=={k:v['text'] for k,v in z['flags'].items()}
 av=[{k:v for k,v in x.items() if k!='line'} for x in a['stages']]
 zv=[{k:v for k,v in x.items() if k!='line'} for x in z['stages']]
 assert av and av==zv,(av,zv)
 new=collections.Counter(x['text'] for x in z['alerts'])-collections.Counter(x['text'] for x in a['alerts'])
 out=dict(baseline=o,old=a,new=z,new_alerts=dict(new),flags_equal=True,stage_SHA_equal=True)
 (E/b/'log-supplement.json').write_text(json.dumps(out,indent=2)+'\n')
 (E/b/'flags-final.txt').write_text('\n'.join(f"L{v['line']}: {v['raw']}" for v in z['flags'].values())+'\n')
 print(b,'stage_SHA',zv,'new_alerts',dict(new),flush=True)
 assert not new,dict(new)
 summary[b]=dict(flags_equal=True,stage_SHA=zv,new_alert_count=0,existing_alert_lines=len(z['alerts']))
(E/'log-supplement-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
end='B5 已结束 '+datetime.datetime.now().astimezone().isoformat()+' PASS'
(E/'b5-end.txt').write_text(end+'\n');print(end)
