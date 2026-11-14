from inventory import *
import time
start=time.monotonic()
discovery=json.load(open(E/'discovery.json'))
paths=[Path(p) for p in discovery['directories']]
paths.extend(p for p in (B/'tools/bolt/results').iterdir() if p.is_dir() and p!=E)
# Only known bounded child names, no repeat of repository discovery.
for base in [W/'temp/night-20261103',W/'temp/night-20261105',W/'temp/rebase-359934-20261111-r6',W/'temp/debuglink-20261028/full-20261030']:
 if not base.exists():continue
 if (base/'gbs-root').is_dir():paths.append(base/'gbs-root')
 for name in ('toolchain','basedev','toolchain-rehearsal','basedev-rehearsal'):
  p=base/name/'gbs-root'
  if p.is_dir():paths.append(p)
paths=sorted(set(paths),key=lambda p:(not any(k in str(p) for k in ('night-20261103','night-20261105','rebase-359934-20261111-r6','local-full-r6','pgo-profiles-keep','pgo-bolt-followup','debuglink-20261028','qb-1226850','qb-1225393','tu-inputs-restored')),str(p)))
docs=[]
for p in (B/'docs').rglob('*.md'):
 if p.stat().st_size>2*1024**2:continue
 for no,line in enumerate(p.read_text(errors='replace').splitlines(),1):
  if 'temp/' in line or 'results/' in line:docs.append((str(p.relative_to(B)),no,line))
records=[]
output=E/'directory-inventory.jsonl'
with output.open('x') as f:
 for i,p in enumerate(paths,1):
  rec={'path':str(p),'time':datetime.datetime.now().astimezone().isoformat(),'timeout_seconds':8,'size_bytes':'UNKNOWN'}
  rec['scope']='nested-root' if p.name=='gbs-root' else 'top-level; do not sum with nested-root rows'
  key=str(p.relative_to(W/'temp')) if p.is_relative_to(W/'temp') else p.name
  refs=[{'file':d,'line':n,'excerpt':clean(l[:500])} for d,n,l in docs if key in l]
  rec['references']=refs[:12];rec['reference_count']=len(refs)
  if any(k in str(p) for k in ('local-full-r6','night-20261103','night-20261105','rebase-359934-20261111-r6','pgo-profiles-keep','pgo-bolt-followup','qb-1226850','qb-1225393','tu-inputs-restored','debuglink-20261028')):
   rec['purpose']='当前认证/归因/PGO或输入基线材料；按对应文档查具体内容'
   rec['retain']='需要：85任务表所列归因、身份矩阵、加固真实样本及追溯；不授权删除'
  elif p.is_relative_to(B/'tools/bolt/results'):
   rec['purpose']='历史原始证据（文档引用见references）'
   rec['retain']='建议保留：审计链；是否有GitHub副本不能替代本轮删除授权'
  else:
   rec['purpose']='历史构建/实验目录；具体用途以references为据，未匹配则UNKNOWN'
   rec['retain']='需要用户判断：本轮未做唯一证据和可重建性审计，不建议自动删除'
  if time.monotonic()-start>300:rec['reason']='inventory wall budget exhausted; du NOT RUN'
  else:
   argv=['nice','-n','19','ionice','-c','3','du','-sx','-B1','--',str(p)]
   t=time.monotonic()
   try:
    q=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,errors='replace',timeout=8)
    rec.update(argv=argv,rc=q.returncode,stdout=clean(q.stdout),stderr=clean(q.stderr),elapsed_seconds=time.monotonic()-t)
    if q.returncode==0 and q.stdout.split() and q.stdout.split()[0].isdigit():rec['size_bytes']=int(q.stdout.split()[0])
    else:rec['reason']='du failed; partial size not used'
   except subprocess.TimeoutExpired as ex:
    rec.update(argv=argv,rc='TIMEOUT',elapsed_seconds=time.monotonic()-t,reason='UNKNOWN; only this newly launched du child terminated under explicit user exception')
   except OSError as ex:rec['reason']=str(ex)
  f.write(json.dumps(rec,ensure_ascii=False)+'\n');f.flush();records.append(rec)
  if i%20==0:print('du progress',i,'/',len(paths),flush=True)
write('directory-summary.json',{'count':len(records),'measured':sum(isinstance(r['size_bytes'],int) for r in records),'unknown':sum(not isinstance(r['size_bytes'],int) for r in records),'timeouts':sum(r.get('rc')=='TIMEOUT' for r in records),'over_5_GiB':[r for r in records if isinstance(r['size_bytes'],int) and r['size_bytes']>5*1024**3],'no_additive_total':'parent and nested entries overlap','user_exception':'允许仅终止本次超时 du'})
print('已结束',datetime.datetime.now().astimezone().isoformat(),'directory inventory COMPLETE',len(records),flush=True)
