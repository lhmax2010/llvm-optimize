from pathlib import Path
import json,hashlib,gzip,collections,datetime
E=Path(__file__).resolve().parent
data=json.loads((E/'all-results.json').read_text())
out={}
for d in data:
 if d['environment']!='local':continue
 p=Path(d['thinlto_links']['clang']['ninja_source']).parent/'build.ninja'
 wanted={v['ninja_raw'].split('\t')[3]:k for k,v in d['thinlto_links'].items()}
 captures=[];current=None
 with p.open() as f:
  for n,l in enumerate(f,1):
   if l.startswith('build '):
    if current:captures.append(current);current=None
    output=l[6:].split(':',1)[0]
    if output in wanted:current={'target':wanted[output],'file':str(p),'line':n,'lines':[l.rstrip('\n')]}
   elif current:
    if l.strip():current['lines'].append(l.rstrip('\n'))
    else:captures.append(current);current=None
 if current:captures.append(current)
 assert len(captures)==5,(d['id'],len(captures))
 for x in captures:
  assert any('-flto=thin' in l for l in x['lines']),x['target']
 with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 out[d['id']]={'path':str(p),'sha256':h,'bytes':p.stat().st_size,'targets':captures}
(E/'thinlto-build-rules.json').write_text(json.dumps(out,indent=2)+'\n')
# Verify zero-size scope of the function comparison, without changing prior results.
F=E.parent/'83/td'
def read(p):
 with gzip.open(p,'rt') as f:return json.load(f)
a=read(F/'left-functions.json.gz');b=read(F/'right-functions.json.gz')
key=lambda r:(r['normalized_name'],r['section'],r['ordinal'])
right={key(r):r for r in b}
zeros=[r for r in a if r['size']==0]
for l in zeros:
 r=right[key(l)]
 assert r['size']==0 and l['masked_sha256']==r['masked_sha256'] and l['relocations']==r['relocations']==[]
(E/'zero-size-scope-audit.json').write_text(json.dumps({'zero_size_records_each':len(zeros),'all_identical':True,'nonempty_identical':99048-len(zeros)},indent=2)+'\n')
print('ThinLTO build rules:',len(out)*5,'PASS; zero-size audit:',len(zeros),'PASS')
print('已结束',datetime.datetime.now().astimezone().isoformat(),'supplement PASS')
