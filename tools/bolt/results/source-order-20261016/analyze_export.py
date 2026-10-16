from pathlib import Path
import re,json,sys
E=Path(__file__).resolve().parent
label=sys.argv[1];p=E/('export-'+label)/'llvm.spec';lines=p.read_text().splitlines();stack=[];rows=[]
for n,l in enumerate(lines,1):
 if re.match(r'^%if(?:arch|narch|os|nos)?\b',l):stack.append({'line':n,'text':l})
 elif l.startswith('%endif'):stack.pop()
 elif l.startswith('%else'):
  pass
 if re.match(r'^(Patch\d+:|%patch\d*\b)',l):rows.append({'line':n,'text':l,'conditions':stack.copy()})
tags=[r for r in rows if r['text'].startswith('Patch')];cmds=[r for r in rows if r['text'].startswith('%patch')]
assert len(tags)==len(cmds)==7,(tags,cmds)
assert [int(re.match('Patch(\d+):',r['text'])[1]) for r in tags]==list(range(7))
assert all(not r['conditions'] for r in cmds)
if label=='before':assert all([c['text'] for c in r['conditions']]==['%ifarch x86_64','%if %{with clang_bolt}'] for r in tags)
else:
 assert all(not r['conditions'] for r in tags)
 old=json.loads((E/'export-before-analysis.json').read_text())
 assert [r['text'] for r in tags]==[r['text'] for r in old['patch_declarations']]
report={'status':'PASS','patch_declarations':tags,'patch_commands':cmds,'patch_files':[r['text'].split(':',1)[1].strip() for r in tags]}
(E/('export-'+label+'-analysis.json')).write_text(json.dumps(report,indent=2)+'\n')
with (E/('export-'+label+'-excerpts.txt')).open('w') as f:
 for group in [tags,cmds]:
  start=max(1,group[0]['line']-10);end=min(len(lines),group[-1]['line']+10)
  for n in range(start,end+1):f.write(f'{n:4d}: {lines[n-1]}\n')
  f.write('\n')
print(json.dumps(report,indent=2))
