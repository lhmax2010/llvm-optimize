"""Offline Ninja closure; separators and absolute duplicate outputs are not nodes."""
from pathlib import Path
import re,json,lzma,collections
E=Path(__file__).resolve().parent
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt')
PREFIX=re.search(r'^cmake_ninja_workdir = (.+)$',(E/'config-after/build.ninja').read_text(),re.M)[1]
def norm(value):
    for prefix in ('${cmake_ninja_workdir}','$cmake_ninja_workdir',PREFIX):
        if value.startswith(prefix):value=value[len(prefix):]
    return value
def parse(path):
    text=path.read_text().replace('$\n','');rows=[];rules={};glob={};active=None
    for line in text.splitlines():
        if line.startswith('build '):
            m=re.fullmatch(r'build (.*?)(?<!\$): (\S+)(.*)',line);assert m,line
            output=list(dict.fromkeys(norm(v) for v in m[1].split() if v not in ('|','||','|@')))
            deps=list(dict.fromkeys(norm(v) for v in m[3].split() if v not in ('|','||','|@')))
            assert output
            row={'outputs':output,'rule':m[2],'dependencies':deps,'bindings':{}}
            rows.append(row);active=row['bindings']
        elif line.startswith('rule '):active={};rules[line[5:]]=active
        elif line.startswith('  ') and active is not None:
            m=re.fullmatch(r'  (\w+) = (.*)',line)
            if m:active[m[1]]=m[2]
        else:
            active=None;m=re.fullmatch(r'(\w+) = (.*)',line)
            if m:glob[m[1]]=m[2]
    return rows,rules,glob
def expand(s,env,stack=()):
    def sub(m):
        name=m[1] or m[2]
        if name is None:return {'$':'$',':':':',' ':' '}[m[3]]
        assert name not in stack,(name,stack)
        return expand(env.get(name,''),env,stack+(name,))
    return re.sub(r'\$\{(\w+)\}|\$(\w+)|\$([$: ])',sub,s)
def run():
    before,_,_=parse(E/'config-before/build.ninja');after,_,glob=parse(E/'config-after/build.ninja')
    _,rules,rg=parse(E/'config-after/CMakeFiles/rules.ninja');glob.update(rg)
    old={v for row in before for v in row['outputs']};byout={v:i for i,row in enumerate(after) for v in row['outputs']}
    seen=set();external=set()
    def visit(node):
        if node not in byout:external.add(node);return
        i=byout[node]
        if i in seen:return
        seen.add(i)
        for dep in after[i]['dependencies']:visit(dep)
    visit('llvm-bolt');rows=[]
    for i in sorted(seen):
        row=after[i];env={**glob,**rules.get(row['rule'],{}),**row['bindings'],'out':' '.join(row['outputs']),'in':' '.join(row['dependencies'])}
        rows.append({**row,'new':all(v not in old for v in row['outputs']),'description':expand(env.get('description',''),env),'command_present':'command' in env})
    original=json.loads(lzma.open(B/'tools/bolt/results/review-closure.json.xz','rt').read())
    def key(row):return tuple(sorted(set(norm(v) for v in row['outputs'] if v not in ('|','||','|@'))))
    oldrows={key(row):row for row in original['closure']};changes=[]
    for row in rows:
        previous=oldrows.get(key(row))
        if previous is None or previous['new']!=row['new']:
            changes.append({'outputs':row['outputs'],'old_new':previous['new'] if previous else None,'new_new':row['new'],'description':row['description']})
    missing=[list(k) for k in oldrows if k not in {key(row) for row in rows}]
    tasks=[row for row in rows if row['new'] and row['rule']!='phony'];descs=sorted({row['description'] for row in tasks})
    olddesc=json.loads((B/'tools/bolt/results/review-tool-descriptions.json').read_text())
    result={'status':'RUNNING','method':'offline recursive all-input traversal; strip |/|| delimiters, normalize cmake_ninja_workdir and absolute build aliases; Ninja not executed','closure_edges':len(rows),'ordinary_edges':sum(not r['new'] for r in rows),'new_phony_edges':sum(r['new'] and r['rule']=='phony' for r in rows),'new_task_edges':len(tasks),'classification_changes':changes,'missing_previous_edges':missing,'added_descriptions':sorted(set(descs)-set(olddesc)),'removed_descriptions':sorted(set(olddesc)-set(descs)),'bolt_tasks':tasks,'closure':rows,'external_inputs':sorted(external),'build_directory_external_inputs':sorted(v for v in external if not v.startswith('/'))}
    passed=(len(tasks)==111 and len(descs)==111 and result['added_descriptions']==['Generating VCSVersion.inc'] and not result['removed_descriptions'] and not missing and len(changes)==1 and changes[0]['description']=='Generating VCSVersion.inc' and changes[0]['old_new'] is False and changes[0]['new_new'] is True)
    result['status']='PASS_CLASSIFICATION' if passed else 'FAIL_CLASSIFICATION'
    (E/'closure-v2.json').write_text(json.dumps(result,indent=2)+'\n');(E/'descriptions-v2.json').write_text(json.dumps(descs,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('bolt_tasks','closure','external_inputs')},indent=2),flush=True)
    assert passed,'unexpected closure classification change; STOP'
if __name__=='__main__':run()
