from pathlib import Path
import json,hashlib,collections,re,xml.etree.ElementTree as X
W=Path('/home/linhao/Toolchain/development/llvm-optimize');E=W.parent/'llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028';D=E/'second-ruling'
projects={p.get('name'):p.get('revision') for p in X.parse(D/'unified-standard.xml').iter('project')};rows=json.loads((D/'spec-acquisition.json').read_text())
assert len(rows)==1030 and len({r['project'] for r in rows})==1030
assert all(r.get('rc')==0 and r['specs'] and r['revision']==projects[r['project']] for r in rows)
extras=[];spec_count=0
for r in rows:
 for ent in r['specs']:
  p=D/ent['path'];b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==ent['sha256'];spec_count+=1
  for i,l in enumerate(b.decode(errors='replace').splitlines(),1):
   if re.match(r'\s*%(?:include|generate_buildrequires)\b',l):extras.append(dict(project=r['project'],spec=ent['path'],line=i,text=l))
assert set(json.loads((D/'scanned-specs.json').read_text()))=={e['path'] for r in rows for e in r['specs']}
br=json.loads((D/'buildrequires-lines.json').read_text());hits=json.loads((D/'buildrequires-hits.json').read_text());raw=json.loads((D/'removed-capability-text-hits.json').read_text());unresolved=[r for r in br if re.search(r'%\{|%\([^)]+\)',r['expanded'])]
old=json.loads((E/'repos/unified-toolchain/packages-all.json').read_text());removed=json.loads((E/'unified-fixed-source-comparison.json').read_text())['missing_from_new'];removed_rows=[]
for repo in removed:
 pk=[p for p in old if p.get('vcs','').split('#')[0]==repo];caps=sorted({c for p in pk for c in [p['name']]+[x['name'] for x in p['provides']]+p['files']});removed_rows.append(dict(project=repo,packages=sorted({p['name'] for p in pk}),capability_count=len(caps),capabilities=caps,buildrequires_hits=[r for r in hits if r['capability'] in caps]))
(D/'removed-repository-providers.json').write_text(json.dumps(removed_rows,indent=2)+'\n')
summary=dict(repositories=len(rows),specs=spec_count,buildrequires_lines=len(br),removed_repositories=len(removed),capabilities=len({c for r in removed_rows for c in r['capabilities']}),matched_buildrequires=len(hits),literal_text_hits=len(raw),unresolved_buildrequires=unresolved,external_or_dynamic_dependencies=extras,status='PASS' if not hits and not unresolved and not extras else 'REVIEW_REQUIRED',scope='Static BuildRequires closure for outputs of the 17 removed repositories, preserving conditional branches; not a general package-build certification.')
(D/'closure-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2)[:5000])
