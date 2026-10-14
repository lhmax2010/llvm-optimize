from pathlib import Path
import json,re,hashlib,collections,sys
E=Path(__file__).parent; prev=E.parent/'bolt-v4-20261014-no-reinstall';snap=E.parent/'bolt-v4-20261014-fallback';B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
def records(lines):
 rows={};owners={}
 for i,line in enumerate(lines):
  if not line.startswith(('build ','rule ')):continue
  typ='build' if line.startswith('build ') else 'rule';key=line.split(': ',1)[0][6:] if typ=='build' else line[5:].strip();end=i+1
  while end<len(lines) and lines[end].startswith((' ','\t')):end+=1
  assert (typ,key) not in rows,('duplicate',typ,key)
  rows[(typ,key)]=lines[i:end]
  for idx in range(i,end):owners[idx]=(typ,key)
 return rows,owners
binding=re.compile(r'^  ([A-Za-z_][A-Za-z0-9_]*) = (.*)\n?$')
def variables(lines):
 result={}
 for line in lines[1:]:
  m=binding.match(line);assert m,('unknown variable syntax',line)
  assert m[1] not in result,('duplicate variable',m[1]);result[m[1]]=m[2]
 return result
j=json.loads((prev/'edge-compare-result.json').read_text());prior=json.loads((prev/'edge-report.json').read_text())
parsed={};identity=[];rule_sources=[]
for name,v in j['files'].items():
 parsed[name]={}
 for mode in ['before','after']:
  path=snap/('config-'+mode)/name;sha=digest(path);assert sha==v[mode+'_sha256']
  lines=path.read_text().splitlines(True);rows,owners=records(lines);parsed[name][mode]=(lines,rows,owners)
  identity.append({'file':name,'snapshot':mode,'sha256':sha,'bytes':path.stat().st_size})
  for key,body in rows.items():
   if key[0]=='rule':rule_sources.append({'file':name,'snapshot':mode,'rule':key[1],'text':''.join(body)})
pdb_rows=[];changed_names=set();pdb_keys=set()
for row in j['files']['build.ninja']['changes']:
 if row['kind']!='build' or not row['before'] or not row['after']:continue
 a=row['before'].splitlines(True);b=row['after'].splitlines(True)
 if ''.join(x for x in a if not x.startswith(('  TARGET_COMPILE_PDB =','  TARGET_PDB ='))) != ''.join(x for x in b if not x.startswith(('  TARGET_COMPILE_PDB =','  TARGET_PDB ='))):continue
 av,bv=variables(a),variables(b);names={n for n in av.keys()|bv.keys() if av.get(n)!=bv.get(n)}
 assert names and names<= {'TARGET_COMPILE_PDB','TARGET_PDB'}
 assert a[0]==b[0]
 assert {n:v for n,v in av.items() if n not in names}=={n:v for n,v in bv.items() if n not in names}
 stripped_a=''.join(x for x in a if not (binding.match(x) and binding.match(x)[1] in names))
 stripped_b=''.join(x for x in b if not (binding.match(x) and binding.match(x)[1] in names))
 assert stripped_a==stripped_b
 changed_names.update(names);pdb_keys.add(('build',row['key']))
 pdb_rows.append({'output':row['key'],'kind':'link' if 'TARGET_FILE' in av else 'object','changed_variables':{n:{'before':av.get(n),'after':bv.get(n)} for n in sorted(names)},'identical_head_sha256':hashlib.sha256(a[0].encode()).hexdigest(),'remaining_statement_sha256':hashlib.sha256(stripped_a.encode()).hexdigest(),'PASS':True})
assert len(pdb_rows)==6838
references={}
for n in sorted(changed_names):
 # Conservative raw-token search: all fields, both files, both snapshots; no exclusion of $$.
 pattern=re.compile(r'\$(?:'+re.escape(n)+r'(?![A-Za-z0-9_])|\{'+re.escape(n)+r'\})')
 hits=[]
 for source in rule_sources:
  for line in source['text'].splitlines():
   if pattern.search(line):hits.append({k:v for k,v in source.items() if k!='text'}|{'line':line})
 assert not hits,(n,hits)
 references[n]={'pattern':pattern.pattern,'rule_definitions_searched':len(rule_sources),'all_rule_fields_searched':True,'hits':hits,'PASS':True}
flat=[(name,block) for name,v in j['files'].items() for block in v['blocks']];assert len(flat)==len(prior['blocks'])==7439
classes=collections.Counter();blocks=[];failures=[];rerun=None;paired=None
allowed={'BOLT_build_edges','BOLT_rules','aggregate_BOLT_dependencies','BOLT_build_edges+aggregate_BOLT_dependencies'}
for index,((name,raw),old) in enumerate(zip(flat,prior['blocks']),1):
 assert name==old['file'] and raw['before_lines']==old['before_lines'] and raw['after_lines']==old['after_lines']
 category=old['category'];status='PASS';detail={}
 owners=set()
 for mode,coord,field in [('before',raw['before_lines'],'before'),('after',raw['after_lines'],'after')]:
  lines,rows,mapping=parsed[name][mode];start,end=coord;assert ''.join(lines[start-1:end])==raw[field]
  for n in range(start-1,end):
   if n in mapping:owners.add(mapping[n])
 if category=='ordinary_PDB_metadata_change':
  assert owners and owners<=pdb_keys
  for field in ['before','after']:
   for line in raw[field].splitlines(True):
    m=binding.match(line);assert m and m[1] in changed_names,(index,line)
  category='A_unreferenced_variable';detail={'owning_statements':[x[1] for x in sorted(owners)],'variables':sorted({binding.match(x)[1] for f in ['before','after'] for x in raw[f].splitlines(True)})}
 elif category=='ordinary_CMake_dependency_removal':
  before_rows=parsed[name]['before'][1];after_rows=parsed[name]['after'][1]
  if owners=={('build','build.ninja')}:
   a=before_rows[('build','build.ninja')];b=after_rows[('build','build.ninja')]
   lefta,righta=a[0].split(': ',1);leftb,rightb=b[0].split(': ',1)
   ta,tb=righta.split(),rightb.split()
   assert lefta==leftb=='build build.ninja' and ta[0]==tb[0]=='RERUN_CMAKE'
   assert a[1:]==b[1:]
   assert ta[1]==tb[1]=='|' and '||' not in ta[2:] and '||' not in tb[2:]
   removed=sorted(set(ta[2:])-set(tb[2:]));added=sorted(set(tb[2:])-set(ta[2:]));assert len(removed)==88 and len(added)==20
   rerun={'block':index,'removed':removed,'added':added,'rule':'RERUN_CMAKE','output':'build.ninja','other_bindings_identical':True,'PASS':True}
   detail=rerun;category='B_RERUN_CMAKE_dependencies'
  else:
   assert len(owners)==2 and all(x[0]=='build' for x in owners)
   before_key=next(x for x in owners if x in before_rows and x not in after_rows);after_key=next(x for x in owners if x in after_rows and x not in before_rows)
   a=before_rows[before_key];b=after_rows[after_key]
   assert a[0].split(': ',1)[1].strip()==b[0].split(': ',1)[1].strip()=='phony'
   old_outputs=a[0].split(': ',1)[0][6:].split();new_outputs=b[0].split(': ',1)[0][6:].split()
   removed=sorted(set(old_outputs)-set(new_outputs));added=sorted(set(new_outputs)-set(old_outputs))
   assert a[1:]==b[1:] and not variables(a) and not variables(b)
   paired={'block':index,'rule':'phony','removed_outputs':removed,'added_outputs':added,'before_output_count':len(old_outputs),'after_output_count':len(new_outputs),'not_A':'Build outputs changed; no variable bindings changed.','not_B':'Rule is phony, not RERUN_CMAKE; output is a multioutput CMake input-file fallback list, not build.ninja.','not_aggregate_allowance':'Changes are outputs and include 88 removals; allowance permits added BOLT dependencies in aggregate targets.','PASS':False}
   detail=paired;category='FAIL_CMake_input_phony_outputs';status='FAIL'
   (E/'phony-failure-before.ninja.txt').write_text(''.join(a));(E/'phony-failure-after.ninja.txt').write_text(''.join(b))
   (E/'phony-failure-diff.txt').write_text('--- before\n+++ after\n-'+''.join(a)+'+'+''.join(b))
 else:assert category in allowed,(index,category)
 classes[category]+=1
 result={'index':index,'file':name,'category':category,'status':status,'before_lines':raw['before_lines'],'after_lines':raw['after_lines'],'detail':detail};blocks.append(result)
 if status=='FAIL':failures.append(result)
assert classes['A_unreferenced_variable']==7421 and classes['B_RERUN_CMAKE_dependencies']==1 and len(failures)==1
assert paired['removed_outputs']==rerun['removed'] and paired['added_outputs']==rerun['added']
result={'status':'STOP_CMAKE_PHONY_OUTPUTS_OUTSIDE_ALLOWED_CLASSES','total_blocks':len(blocks),'block_class_counts':dict(classes),'passed_blocks':len(blocks)-len(failures),'failed_blocks':len(failures),'snapshot_identity':identity,'changed_variable_names':sorted(changed_names),'rule_reference_search':references,'rule_definitions_by_file_snapshot':dict(collections.Counter(x['snapshot']+'/'+x['file'] for x in rule_sources)),'ordinary_statements_certified':len(pdb_rows),'ordinary_statement_kinds':dict(collections.Counter(x['kind'] for x in pdb_rows)),'ordinary_statement_conditions':'Exact head equality proves outputs, inputs, implicit/order-only dependencies and rule name unchanged; all other variable bindings and remaining statement bytes unchanged.','rerun_dependencies':rerun,'phony_failure':paired,'blocks':blocks,'statements':pdb_rows,'control_experiment':'NOT_RUN after product text gate FAIL','expansion':'NOT_RUN','objects_30_90':'NOT_RUN','dual_mode_smoke':'NOT_RUN','expected_RPM_DWARF_diff':'NOT_RUN','performance':'NOT_RUN; geometric mean unknown','sandbox_push':'NOT_ATTEMPTED','candidate_route':'historical tool fallback; retained previous candidate','candidate_sha256':'4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9','source_commit':'a1410e3d14b8836e3f9be5a1b4380f914dc2e705','preparatory_corrections':[{'class':'documentation path','first_error':'Guessed 17_no_reinstall_and_text_edges.md does not exist.','correction':'rg --files found and read 17_no_reinstall_and_text_gate.md.','count':1,'product_gate_impact':False}]}
save(E/'certification.json',result)
public=B/'tools/bolt/results/text-proof-certification.json';save(public,result)
for n in ['phony-failure-before.ninja.txt','phony-failure-after.ninja.txt','phony-failure-diff.txt']:(B/'tools/bolt/results'/('text-proof-'+n)).write_bytes((E/n).read_bytes())
print(json.dumps({k:result[k] for k in ['status','total_blocks','block_class_counts','changed_variable_names','rule_definitions_by_file_snapshot','ordinary_statements_certified','ordinary_statement_kinds','passed_blocks','failed_blocks']},indent=2),flush=True)
print('RERUN removals',len(rerun['removed']),'additions',len(rerun['added']),'phony_block',paired['block'],flush=True)
# Nonzero for product certification failure; detailed proof already retained.
sys.exit(1 if failures else 0)
