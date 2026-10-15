#!/usr/bin/env python3
"""Strict offline saved Ninja graph traversal; no depfile or dirty-state inference."""
import argparse, hashlib, json, lzma, re, sys
from pathlib import Path

class GraphError(RuntimeError): pass

def need(ok, text):
    if not ok: raise GraphError(text)

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def parse(path):
    rows=[]; rules={}; glob={}; active=None
    text=Path(path).read_text().replace('$\n','')
    for line in text.splitlines():
        if line.startswith('subninja '): raise GraphError('subninja unsupported: '+line)
        if line.startswith('include '):
            need(line.split(None,1)[1]=='CMakeFiles/rules.ninja','unapproved include: '+line)
        if line.startswith('build '):
            m=re.fullmatch(r'build (.*?)(?<!\$): (\S+)(.*)',line);need(m is not None,'malformed build: '+line)
            def tokens(part):
                need(not re.search(r'\$[: $]',part),'escaped path unsupported: '+part)
                out=[]
                for token in part.split():
                    if token in ('|','||','|@'):continue
                    for prefix in ('${cmake_ninja_workdir}','$cmake_ninja_workdir'):
                        if token.startswith(prefix):token=token[len(prefix):]
                    need('$' not in token,'unexpanded path variable: '+token)
                    out.append(token)
                return list(dict.fromkeys(out))
            row={'outputs':tokens(m[1]),'rule':m[2],'dependencies':tokens(m[3]),'bindings':{}}
            need(bool(row['outputs']),'empty output set');rows.append(row);active=row['bindings']
        elif line.startswith('rule '):active={};rules[line[5:]]=active
        elif line.startswith('  ') and active is not None:
            m=re.fullmatch(r'  (\w+) = (.*)',line)
            if m:active[m[1]]=m[2]
        else:
            active=None;m=re.fullmatch(r'(\w+) = (.*)',line)
            if m:glob[m[1]]=m[2]
    prefix=glob.get('cmake_ninja_workdir','')
    for row in rows:
        for key in ('outputs','dependencies'):
            row[key]=list(dict.fromkeys(v[len(prefix):] if prefix and v.startswith(prefix) else v for v in row[key]))
    return rows,rules,glob

def expand(text,env,stack=()):
    def sub(m):
        name=m[1] or m[2]
        if name is None:return {'$':'$',':':':',' ':' '}[m[3]]
        need(name in env,'unexpanded description variable: '+name)
        need(name not in stack,'recursive variable: '+name)
        return expand(env[name],env,stack+(name,))
    result=re.sub(r'\$\{(\w+)\}|\$(\w+)|\$([$: ])',sub,text)
    need(not re.search(r'\$(?![$: ])',result),'unexpanded description: '+result)
    return result

def analyze(before,after,rules,expect_tasks,old_result=None):
    old,_,_=parse(before);new,_,glob=parse(after);_,definitions,rg=parse(rules);glob.update(rg)
    oldout={v for row in old for v in row['outputs']};byout={}
    for i,row in enumerate(new):
        for v in row['outputs']:
            need(v not in byout,'duplicate normalized output: '+v);byout[v]=i
    seen=set();external=set()
    def visit(node):
        if node not in byout:external.add(node);return
        i=byout[node]
        if i in seen:return
        seen.add(i)
        for v in new[i]['dependencies']:visit(v)
    need('llvm-bolt' in byout,'missing llvm-bolt target');visit('llvm-bolt');rows=[];used={}
    for i in sorted(seen):
        row=new[i];rule=definitions.get(row['rule'],{})
        need(row['rule']=='phony' or bool(rule),'missing rule: '+row['rule'])
        env={**glob,**rule,**row['bindings'],'out':' '.join(row['outputs']),'in':' '.join(row['dependencies'])}
        description=expand(rule.get('description',''),env)
        rows.append({**row,'new':all(v not in oldout for v in row['outputs']),'description':description})
        if description:used[row['rule']]={**rule}
    tasks=[r for r in rows if r['new'] and r['rule']!='phony'];descriptions=sorted({r['description'] for r in tasks})
    need(len(tasks)==expect_tasks and len(descriptions)==expect_tasks,'task count actual=%d/%d expected=%d'%(len(tasks),len(descriptions),expect_tasks))
    result={'status':'PASS','method':'saved static graph only; no .ninja_deps/depfiles or complete dirty evaluation; unknown real tasks fail closed','closure_edges':len(rows),'ordinary_edges':sum(not r['new'] for r in rows),'new_phony_edges':sum(r['new'] and r['rule']=='phony' for r in rows),'new_task_edges':len(tasks),'closure':rows,'bolt_tasks':tasks,'descriptions':descriptions,'external_inputs':sorted(external),'rules_subset':used}
    if old_result:
        data=lzma.open(old_result,'rt') if str(old_result).endswith('.xz') else open(old_result)
        with data:previous=json.load(data)
        prior={tuple(r['outputs']):r['new'] for r in previous['closure']}
        result['classification_changes']=[r['outputs'] for r in rows if prior.get(tuple(r['outputs']))!=r['new']]
        need(not result['classification_changes'],'classification changed from supplied previous result')
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ('before','after','rules'):p.add_argument('--'+key,required=True,type=Path)
    p.add_argument('--old-result',type=Path);p.add_argument('--expect-tasks',required=True,type=int)
    a=p.parse_args();r=analyze(a.before,a.after,a.rules,a.expect_tasks,a.old_result)
    r['invocation']=[sys.executable,*sys.argv];r['inputs']={str(v.resolve()):sha(v) for v in (a.before,a.after,a.rules,a.old_result) if v}
    print(json.dumps(r,indent=2))
if __name__=='__main__':
    try:main()
    except (GraphError,OSError,ValueError) as e:print('CLOSURE_FAILED: '+str(e),file=sys.stderr);sys.exit(1)
