from pathlib import Path
import json,xml.etree.ElementTree as X,collections,re,subprocess,hashlib,urllib.request
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';E=B/'tools/bolt/results/qb-meta-switch-20261028';D=Path(__file__).resolve().parent;R=W/'temp/qb-meta-20261028/repo'
def repos(p):return {x.get('name'):x.get('revision') for x in X.parse(p).getroot().iter('project') if x.get('name')}
a=repos(E/'metadata/Tizen-Unified-Toolchain/manifest.xml');p=next((E/'repos/unified').glob('*_standard.xml'));b=repos(p);qb=json.loads((E/'qb/1209727-packages.json').read_text())[0]['packages']
result=dict(current_manifest_count=len(a),qb_count=len(qb),fixed_new_count=len(b),new_snapshot_manifest=str(p.relative_to(E)),missing_from_new=sorted(a.keys()-b.keys()),added_in_new=sorted(b.keys()-a.keys()),changed=[dict(project=k,old=a[k],new=b[k]) for k in sorted(a.keys()&b.keys()) if a[k]!=b[k]],qb_missing_from_new=sorted(qb.keys()-b.keys()),qb_vs_current_names_equal=qb.keys()==a.keys(),qb_vs_current_revision_changes=[k for k in a.keys()&qb.keys() if a[k]!=qb[k]])
(E/'unified-fixed-source-comparison.json').write_text(json.dumps(result,indent=2)+'\n')
with (E/'unified-repository-changes.tsv').open('w') as f:
 f.write('change\tproject\told_revision\tnew_revision\n')
 for k in result['missing_from_new']:f.write(f'missing\t{k}\t{a[k]}\t\n')
 for k in result['added_in_new']:f.write(f'added\t{k}\t\t{b[k]}\n')
 for r in result['changed']:f.write('changed\t'+r['project']+'\t'+str(r['old'])+'\t'+str(r['new'])+'\n')
# Index all config checks and missing packages with original config line references.
for side,project in [('base','Tizen-Base-Toolchain'),('unified','Tizen-Unified-Toolchain')]:
 rows=json.loads((E/f'{side}-config-providers.json').read_text());lines=(E/'metadata'/project/'project_config').read_text().splitlines()
 for r in rows:
  needle=(r.get('substitute_trigger') or r['name']).replace('x86_64','%{build_hostarch}')
  r['config_lines']=[i+1 for i,l in enumerate(lines) if l.lower().startswith(r['directive']+':') and (needle in l or r['name'] in l)]
 (E/f'{side}-config-providers.json').write_text(json.dumps(rows,indent=2)+'\n')
 with (E/f'{side}-config-providers.tsv').open('w') as f:
  f.write('arch\tdirective\tlines\ttrigger\tname\tproviders\told_providers\tother_arch_providers\n')
  for r in rows:f.write('\t'.join([r['arch'],r['directive'],','.join(map(str,r['config_lines'])),r.get('substitute_trigger') or '',r['name'],','.join(r['providers']),','.join(r.get('old_same_arch_providers',[])),','.join(r.get('other_arch_providers',[]))])+'\n')
for side in ['base','unified']:
 rows=json.loads((E/f'{side}-missing-dependencies.json').read_text());key='missing_packages' if side=='base' else 'missing_even_with_base';names=sorted({n for r in rows.values() for n in r[key]})
 with (E/f'{side}-missing-packages.tsv').open('w') as f:
  f.write('package\tx86_64\tarmv7l\taarch64\n')
  for n in names:f.write(n+'\t'+'\t'.join('missing' if n in rows[a][key] else 'present/not-old' for a in ['x86_64','armv7l','aarch64'])+'\n')
# Explicit proof of scope and absence of second-layer declarations in the two Unified project directories.
summary=[]
for project in ['Tizen-Unified','Tizen-Unified-Toolchain']:
 path=E/'metadata'/project;meta=X.parse(path/'project_meta');snap=X.parse(path/'snapshot_info');summary.append(dict(project=project,files=sorted(x.name for x in path.iterdir()),repository_arches={r.get('name'):[x.get('name') for x in r.findall('arch')] for r in meta.findall('repository')},explicit_paths=[dict(x.attrib) for x in meta.findall('.//path')],snapshot_info=[dict(x.attrib) for x in snap.getroot()],project_config_sha256=hashlib.sha256((path/'project_config').read_bytes()).hexdigest(),mlgo_parameter_lines=[i+1 for i,l in enumerate((path/'project_config').read_text().splitlines()) if 'regalloc-enable-advisor' in l or 'enable-ml-inliner' in l]))
(E/'unified-topology.json').write_text(json.dumps(summary,indent=2)+'\n')
proof=[]
for n in [1209720,1209725,1209726,1209727]:
 lines=(D/f'{n}-full-log.txt').read_text().splitlines();hits=[]
 for i,l in enumerate(lines):
  if re.search(r'dod create project|DOD:|timeout 8h gbs build|repo_url :|get_build_conf_text|USE_NGBS',l):hits.append(dict(line=i+1,text=l))
 proof.append(dict(build=n,total_lines=len(lines),dod_create_count=sum('dod create project' in l for l in lines),hits=hits))
(E/'qb/mechanism-summary.json').write_text(json.dumps(proof,indent=2)+'\n')
(E/'base-existing.diff').write_bytes(subprocess.check_output(['git','-C',str(R),'show','--format=','fd60db96806a372404bd4f04e68d4ba586290147']))
(E/'meta-local-state.txt').write_bytes(subprocess.check_output(['git','-C',str(R),'log','-1','--format=fuller']))
# Snapshot/source URLs and files have no cookies/headers. Existing preview page was saved only after login.
prov=json.loads((E/'qb/provenance.json').read_text())
for ext in ['txt','png']:
 p=E/'qb'/('1209720-overview.'+ext);prov.append(dict(file=str(p.relative_to(E)),url='https://quickbuild.tizen.org/build/1209720',bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(E/'qb/provenance.json').write_text(json.dumps(prov,indent=2)+'\n')
print('source comparison',len(result['missing_from_new']),len(result['added_in_new']),len(result['changed']),'QB/currentsame',result['qb_vs_current_names_equal'])
print('topology',[{k:v for k,v in x.items() if k not in ['snapshot_info']} for x in summary])
