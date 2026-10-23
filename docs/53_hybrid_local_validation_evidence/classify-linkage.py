"""Classify frozen expectations against the actual Ninja default closure; no Ninja invocation."""
import json,re
from pathlib import Path
from validate import E,BUILD,save
text=(E/'build-metadata/build.ninja').read_text();logical=[];pending='';first=0
for number,line in enumerate(text.splitlines(),1):
 if not pending:first=number
 pending+=line
 if pending.endswith('$'):pending=pending[:-1];continue
 logical.append((first,pending));pending=''
assert not pending
edges={};defaults=[]
def tokens(s):
 assert '$ ' not in s and '$:' not in s, 'unexpected escaped whitespace or colon requires explicit handling'
 s=s.replace('${cmake_ninja_workdir}','').replace('$cmake_ninja_workdir','')
 return [x for x in s.split() if x not in ('|','||','|@')]
for number,line in logical:
 if line.startswith('default '):defaults+=tokens(line[8:])
 if not line.startswith('build '):continue
 outputs,tail=line[6:].split(': ',1);parts=tokens(tail);rule=parts[0];inputs=parts[1:]
 row={'line':number,'raw':line,'rule':rule,'inputs':inputs,'outputs':tokens(outputs)}
 for output in row['outputs']:
  assert output not in edges or edges[output]==row,output
  edges[output]=row
assert defaults==['all'],defaults
closure=set();todo=list(defaults)
while todo:
 n=todo.pop()
 if n in closure:continue
 closure.add(n)
 if n in edges:todo.extend(edges[n]['inputs'])
j=json.loads((E/'linkage-188.json').read_text());rows=[]
for r in j['rows']:
 n=r['build_output'];edge=edges.get(n);row={**r,'edge_exists':edge is not None,'default_all_reachable':n in closure,'edge':edge}
 if r['status']=='INSPECTION_ERROR' and not r['exists'] and edge and n not in closure and not r['install_paths']:row['classification']='NOT_BUILT_NONDEFAULT_NONINSTALLED'
 else:row['classification']=r['status']
 rows.append(row)
counts={k:sum(r['classification']==k for r in rows) for k in sorted({r['classification'] for r in rows})}
save('linkage-188-classification.json',{'default':defaults,'default_closure_nodes':len(closure),'counts':counts,'total':len(rows),'physical_pass':counts.get('PASS',0),'note':'No absent ELF is counted as physical PASS. No optional target was built. The source, default target, and expected table are unchanged.','rows':rows})
print(counts)
