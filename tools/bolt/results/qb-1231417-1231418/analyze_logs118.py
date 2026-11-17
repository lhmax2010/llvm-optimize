from pathlib import Path
import gzip,json,re,collections,datetime
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=Path(str(W)+'-bolt');E=B/'tools/bolt/results/qb-1231417-1231418';O=B/'tools/bolt/results/qb-1226850-1226851'
def normalized(l):return re.sub(r'^\[\d+/\d+\]\s*','',re.sub(r'^\[\s*\d+s\]\s?','',l))
def read(root,b):
 p=root/b/'x86_64/llvm.buildlog.txt.gz'
 return gzip.open(p,'rt',errors='replace').read().splitlines()
def collect(lines):
 keys=['SESSION_KILL_MODE','NATIVE_ARCHIVES_STARTUP','BOLT_REAL_GATE_PASS','BOLT_POST_GATE_PASS','jump past end','BOLT_DISK_REPORT','NATIVE_ARCHIVES_END','compare-root']
 out={k:[{'line':i+1,'text':l} for i,l in enumerate(lines) if k in l] for k in keys}
 diag=[];allhit=[]
 for i,l in enumerate(lines):
  if re.search(r'warning:|error:|WARNING|CANCELLED|not found',l,re.I):
   ent={'line':i+1,'text':l,'normalized':normalized(l)};allhit.append(ent)
   if not re.match(r'^\[\d+/\d+\]',re.sub(r'^\[\s*\d+s\]\s?','',l)):diag.append(ent)
 out['diagnostics']=diag;out['keyword_hits']=allhit
 disks=[]
 for x in out['BOLT_DISK_REPORT']:
  t=normalized(x['text'])
  if t.startswith('BOLT_DISK_REPORT {'):
   d=json.loads(t[len('BOLT_DISK_REPORT '):]);disks.append({'line':x['line'],'seconds':int(re.search(r'(\d+)s\]',x['text'])[1]),'stage':d['stage'],'used_bytes':d['used_bytes']})
 out['disk_summary']=disks
 out['max_scope_snapshot_bytes']=max((x['used_bytes'] for x in disks),default=None)
 return out
result={}
for n,o in [('1231417','1226850'),('1231418','1226851')]:
 new=collect(read(E,n));old=collect(read(O,o))
 a=collections.Counter(x['normalized'] for x in new['keyword_hits']);b=collections.Counter(x['normalized'] for x in old['keyword_hits'])
 added=a-b;removed=b-a
 result[n]={'baseline':o,'new':new,'old':old,'new_keyword_lines':[{'text':s,'count':c,'originals':[x for x in new['keyword_hits'] if x['normalized']==s]} for s,c in added.items()],'removed_keyword_lines':dict(removed)}
 print(n,'modes',len(new['SESSION_KILL_MODE']),'diag',len(old['diagnostics']),len(new['diagnostics']),'added',sum(added.values()),'jump',len(old['jump past end']),len(new['jump past end']),'disk',new['disk_summary'])
 print('NEWLINES',json.dumps(result[n]['new_keyword_lines'])[:3000])
 # Stage timing explicitly taken from shell invocations, not gate duration floats.
 for key in ['compare-root','post --',' post ','disk-report begin']:
  for tag,ls in [('old',read(O,o)),('new',read(E,n))]:
   found=[{'line':i+1,'text':l} for i,l in enumerate(ls) if key in l]
   result[n].setdefault('timing_lines',{})[tag+' '+key]=found
(E/'log-analysis.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
for n,x in result.items():
 (E/(n+'-critical-lines.txt')).write_text('\n'.join(f"{k} L{r['line']}: {r['text']}" for k in ['SESSION_KILL_MODE','NATIVE_ARCHIVES_STARTUP','BOLT_REAL_GATE_PASS','BOLT_POST_GATE_PASS','jump past end','BOLT_DISK_REPORT'] for r in x['new'][k])+'\n')
print('已结束',datetime.datetime.now().astimezone().isoformat(),'B log-analysis')
