from pathlib import Path
import json,gzip,collections,subprocess,re
E=Path(__file__).resolve().parent;B=E.parents[3];N=json.loads((E/'targets.json').read_text());allrows=[]
for n in N:
 p=E/n/'hashes.json'
 if p.exists():allrows+=json.loads(p.read_text())
extra=json.loads((E/'probe-binary-hashes.json').read_text()) if (E/'probe-binary-hashes.json').exists() else []
allrows+=extra
p=E/'additional-tool-hashes.json'
if p.exists():allrows+=json.loads(p.read_text())
p=E/'identity-hashes.json'
if p.exists():allrows+=json.loads(p.read_text())
p=E/'handoff-assets.json'
if p.exists():
 extra+=json.loads(p.read_text());allrows+=json.loads(p.read_text())
byhash=collections.defaultdict(set)
for x in allrows:
 h=x['hash'].get('sha256')
 if h:
  byhash[h].add(x['path'])
  byhash[h].update(q['path'] for q in x.get('duplicates',[]))
p=E/'probe-external-duplicates.json'
if p.exists():
 for x in json.loads(p.read_text()):
  h=x['hash'].get('sha256')
  if h:byhash[h].update(x['same_sha_retained_products'])
for l in (E/'retained-tool-copies.sha256').read_text().splitlines():
 h,path=l.split(None,1);byhash[h].add(path.strip())
# Check QB retained RPM candidates by size first; an unequal size cannot have equal file bytes.
qbs=json.loads((E/'qb-rpm-metadata.json').read_text());qs=collections.defaultdict(list)
for x in qbs:qs[x['bytes']].append(x)
comp=[];cache={}
for x in allrows:
 if not x['path'].endswith('.rpm'):continue
 h=x['hash'].get('sha256')
 if not h:continue
 for q in qs[x['size']]:
  if q['path'] not in cache:
   r=subprocess.run(['timeout','120','nice','-n','19','ionice','-c3','sha256sum','--',q['path']],capture_output=True,text=True)
   cache[q['path']]={'rc':r.returncode,'sha256':r.stdout.split()[0] if r.returncode==0 else None,'stderr':r.stderr}
  z=cache[q['path']];equal=h==z['sha256'];comp.append({'file':x['path'],'qb':q['path'],'equal':equal,'qb_hash':z})
  if equal:byhash[h].add(q['path'])
(E/'qb-size-candidate-check.json').write_text(json.dumps({'qb_rpm_paths':len(qbs),'same_size_checks':comp,'note':'unequal-size files excluded; no public-download availability inferred'},indent=2))
refs=json.loads((E/'reference-locations.json').read_text())
stats=[]
for n in N:
 inv=json.loads((E/n/'inventory.json').read_text());hashmap={x['path']:x for x in allrows if '/'+n+'/' in x['path']};rpm_rows=[];asset_rows=[]
 for x in inv['rpms']:
  z=hashmap.get(x['path'],{});hh=z.get('hash',{});h=hh.get('sha256');copies=sorted(byhash[h]-{x['path']}) if h else []
  rpm_rows.append({'path':x['path'],'bytes':x['size'],'sha256':h or 'UNKNOWN','status':hh.get('status','OK' if h else 'UNKNOWN'),'copies':copies,'hash_rc':hh.get('rc')})
 for x in inv['special']+extra:
  if not x['path'].startswith(inv['path']+'/'):continue
  if x['path'] in {a['path'] for a in asset_rows}:continue
  z=hashmap.get(x['path'],{});h=z.get('hash',{}).get('sha256');copies=sorted(byhash[h]-{x['path']}) if h else []
  asset_rows.append({'path':x['path'],'bytes':x['size'],'sha256':h or ('symlink -> '+x['link'] if x.get('link') else 'not hashed: metadata/evidence or UNKNOWN'),'copies':copies})
 for filename,rows in [('rpm.tsv',rpm_rows),('assets.tsv',asset_rows)]:
  with (E/n/filename).open('w') as f:
   f.write('path\tbytes\tsha256\tverified_same_sha_copies\n')
   for x in rows:f.write(f"{x['path']}\t{x['bytes']}\t{x['sha256']}\t"+(' | '.join(x['copies']) if x['copies'] else '未证实其他位置同SHA；保留/UNKNOWN')+'\n')
 (E/n/'rpm-catalog.json').write_text(json.dumps(rpm_rows,indent=2))
 doc=['# 引用逐条索引：'+n,'','本页逐条列工具脚本及55–63号文档引用。其他用途来源的完整命中在main-docs/bolt-docs-references-v3.txt.gz。路径命中不等于当前执行依赖；历史render/报告脚本仍按原文列出。','']
 for cat in ('main-scripts','bolt-scripts','main-config','bolt-config','recent-docs'):
  hits=[]
  if cat.endswith('config'):
   p=E/n/(cat+'-references.txt.gz')
   if p.exists():
    for l in gzip.open(p,'rt'):
     if not l.strip():continue
     parts=l.rstrip().split(':',2);hits.append({'file':parts[0],'line':int(parts[1]),'text':parts[2]})
  else:
   for r in refs:
    if r['directory']!=n:continue
    if r['category']==cat:hits+=r['hits']
    if cat=='recent-docs' and r['category'].endswith('docs'):
     hits += [x for x in r['hits'] if re.search(r'/docs/bolt/(55|56|57|58|59|60|61|62|63)[^/]*\.md$',x['file'])]
  doc+=['## '+cat,'']
  if not hits:doc+=['无。',''];continue
  for x in hits:
   doc+=['- `'+x['file']+':'+str(x['line'])+'`', '  ```text', '  '+x['text'].replace('\n','\n  '),'  ```']
  doc+=['']
 (E/n/'reference-index.md').write_text('\n'.join(doc).rstrip()+'\n')
 stats.append({'directory':n,'RPM_paths':len(rpm_rows),'hash_known':sum(x['sha256']!='UNKNOWN' for x in rpm_rows),'hash_unknown':sum(x['sha256']=='UNKNOWN' for x in rpm_rows),'verified_copy_paths':sum(bool(x['copies']) for x in rpm_rows),'assets':len(asset_rows)})
(E/'catalog-summary.json').write_text(json.dumps(stats,indent=2));print(json.dumps(stats,indent=2))
