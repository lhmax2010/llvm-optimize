from pathlib import Path
import json,gzip,collections,datetime,shutil,subprocess,os
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.parent/'llvm-optimize';E=B/'tools/bolt/results/baseline-attribution-20261105'
c=collections.Counter();exceptions=[]
with gzip.open(E/'all-changed-names.jsonl.gz','rt') as f:
 for l in f:
  x=json.loads(l);kind=x['kind']
  if kind in ('symbol','archive-index'):
   a,b=x['old'],x['new'];c[kind+'_rows']+=1
   if a and b and a[0]!=b[0]:c[kind+'_name_changes']+=1
   if (kind=='symbol' and not x['suffix_only']) or (kind=='archive-index' and not x['suffix_and_target_equal']):exceptions.append(x);c[kind+'_exceptions']+=1
with (E/'symbol-exceptions.tsv').open('w') as f:
 f.write('package\tpath\tmember\tsection\tindex\told\tnew\n')
 for x in exceptions:f.write('\t'.join(str(x.get(k,'')).replace('\t',' ') for k in ['package','path','member','section','index'])+'\t'+json.dumps(x['old'])+'\t'+json.dumps(x['new'])+'\n')
(E/'name-counts.json').write_text(json.dumps(dict(c),indent=2)+'\n')
q=json.loads((E/'qb-rpm-comparison-v2.json').read_text());fail=[]
with (E/'qb-failures.tsv').open('w') as f:
 f.write('project\tpackage\tfile\treason\n')
 for r in q:
  for x in r['content_changes']:
   if x['classification']=='FAIL':f.write('\t'.join([r['project'],r['package'].replace('\t',' '),x['path'],x['error'].replace('\n',' ')])+'\n');fail.append({'project':r['project'],'package':r['package'],'path':x['path'],'error':x['error']})
(E/'qb-failure-catalog.json').write_text(json.dumps(fail,indent=2)+'\n')
for p in (W/'temp/attribution-20261105/probe').glob('*bcanalyzer.*'):shutil.copyfile(p,E/('probe-'+p.name))
df=subprocess.check_output(['df','-B1','/home'],text=True);(E/'df-final.txt').write_text(df)
line='ITEM3 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status=partial reason=449-files-audited-module-byte-causality-unproven';(E/'item3-end.txt').write_text(line+'\n');print(line,flush=True)
