from pathlib import Path
import re,json,collections
E=Path(__file__).resolve().parent
P=E.parent/'bolt-v4-20261014-fallback'
def parse(path):
 text=path.read_text().replace('$\n','')
 rows=[];rules={};globals={};active=None
 for line in text.splitlines():
  if line.startswith('build '):
   m=re.match(r'build (.*?)(?<!\$): (\S+)(.*)',line);assert m,line
   row={'outputs':m[1].split(),'rule':m[2],'dependencies':[v for v in m[3].split() if v not in ('|','||','|@')],'bindings':{}}
   rows.append(row);active=row['bindings']
  elif line.startswith('rule '):active={};rules[line[5:]]=active
  elif line.startswith('  ') and active is not None:
   m=re.match(r'  (\w+) = (.*)',line)
   if m:active[m[1]]=m[2]
  else:
   active=None;m=re.match(r'(\w+) = (.*)',line)
   if m:globals[m[1]]=m[2]
 return rows,rules,globals
before,_,_=parse(P/'config-before/build.ninja')
after,_,g=parse(P/'config-after/build.ninja')
_,rules,rg=parse(P/'config-after/CMakeFiles/rules.ninja');g.update(rg)
old={x for r in before for x in r['outputs']};byout={x:i for i,r in enumerate(after) for x in r['outputs']}
seen=set();external=set()
def visit(x):
 if x not in byout:external.add(x);return
 i=byout[x]
 if i in seen:return
 seen.add(i)
 for dep in after[i]['dependencies']:visit(dep)
visit('llvm-bolt')
def expand(s,env,stack=()):
 def sub(m):
  name=m[1] or m[2]
  if name is None:return {'$':'$',':':':',' ':' '}[m[3]]
  assert name not in stack,(name,stack)
  return expand(env.get(name,''),env,stack+(name,))
 return re.sub(r'\$\{(\w+)\}|\$(\w+)|\$([$: ])',sub,s)
rows=[]
for i in sorted(seen):
 r=after[i];new=all(x not in old for x in r['outputs']);env={**g,**rules.get(r['rule'],{}),**r['bindings'],'out':' '.join(r['outputs']),'in':' '.join(r['dependencies'])}
 desc=expand(env.get('description',''),env)
 rows.append({**r,'new':new,'description':desc,'command_present':'command' in env})
new=[r for r in rows if r['new'] and r['rule']!='phony']
assert all(any('tools/bolt/' in x or 'LLVMBOLT' in x or x=='bin/llvm-bolt' for x in r['outputs']) for r in new)
assert all(r['description'] and '$' not in r['description'] for r in new)
result={'status':'PASS','method':'Offline recursive traversal of every explicit/implicit/order-only input; recursive rule+edge variable expansion; no Ninja execution','closure_edges':len(rows),'ordinary_edges':sum(not r['new'] for r in rows),'ordinary_command_edges':sum(not r['new'] and r['command_present'] for r in rows),'new_phony_edges':sum(r['new'] and r['rule']=='phony' for r in rows),'new_task_edges':len(new),'categories':dict(collections.Counter(r['description'].split(' tools/bolt/')[0] if ' tools/bolt/' in r['description'] else r['description'] for r in new)),'bolt_tasks':new,'closure':rows,'external_inputs':sorted(external)}
(E/'closure.json').write_text(json.dumps(result,indent=2)+'\n')
(E/'descriptions.json').write_text(json.dumps(sorted(set(r['description'] for r in new)),indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('bolt_tasks','closure','external_inputs')},indent=2))
