from pathlib import Path
import json,re,collections,gzip,xml.etree.ElementTree as X
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';E=B/'tools/bolt/results/qb-fail-20261028/meta/buildconf'
records=json.loads((E/'spec-macro-usage.json').read_text());manifest=json.loads((E/'manifest-projects.json').read_text());qb=json.loads((E/'1211018-package-lists.json').read_text())[0]['packages'];mapping=collections.defaultdict(list)
for row in records:
 text=(E/row['file']).read_text(errors='replace');v=re.search(r'^VCS:\s+(\S+)',text,re.M)
 if v:
  vcs=v[1];repo,_,commit=vcs.partition('#');repo=repo.removesuffix('.git');mapping[repo].append(dict(file=row['file'],vcs=vcs,source=row['source'],version=row['version'],package=row['package']))
 if row['source'] in ('Gerrit tizen_base fallback','Gerrit exact QB commit'):mapping[row['package']].append(dict(file=row['file'],vcs=row.get('archive_commit') or row['version'],source=row['source'],version=row['version'],package=row['package']))
 if row['source']=='local immutable Git object':mapping['platform/upstream/llvm'].append(dict(file=row['file'],vcs=row['version'],source=row['source'],version=row['version'],package=row['package']))
rows=[]
for project in sorted(set(qb)|{p['name'] for p in manifest}):
 candidates=mapping[project];expected=qb.get(project);exact=[r for r in candidates if r['vcs'].endswith('#'+str(expected)) or r['vcs']==expected]
 rows.append(dict(project=project,manifest=next((p['revision'] for p in manifest if p['name']==project),None),qb_commit=expected,exact_qb_commit_specs=exact,available_specs=candidates,status='exact QB commit available' if exact else ('snapshot or branch evidence only' if candidates else 'not acquired')))
(E/'project-spec-coverage.json').write_text(json.dumps(rows,indent=2)+'\n')
print('project union',len(rows),'counts',dict(collections.Counter(r['status'] for r in rows)));print('missing',[r['project'] for r in rows if r['status']=='not acquired'])
