from pathlib import Path
import json,hashlib,subprocess,datetime,re
B=Path.cwd();E=B/'tools/bolt/results/night-82-84-20261113'
def digest(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
report={'historical_resource_inputs':[],'entry_unchanged':[],'doc_links':[]}
for x in json.load(open(E/'84/read-inputs.json')):
 actual=digest(x['path']);assert actual==x['sha256'],x['path']
 report['historical_resource_inputs'].append({'path':x['path'],'sha256':actual,'unchanged':True})
entry=B/'tools/bolt/rebase-launch-20261111-r6'
for rel in ('toolchain/launcher.py','toolchain/SHA256SUMS'):
 assert (entry/rel).read_bytes()==(E/'82/before'/rel).read_bytes()
 report['entry_unchanged'].append(rel)
docs=['82_entry_fixes.md','83_td_function_diff.md','84_resource_breakdown.md']
for name in docs:
 p=B/'docs/bolt'/name
 for label,target in re.findall(r'\[([^\]]*)\]\(([^)]+)\)',p.read_text()):
  if '://' in target or target.startswith('#'):continue
  q=p.parent/target.split('#')[0]
  assert q.exists(),(p,target)
  report['doc_links'].append({'document':name,'target':target,'exists':True})
assert subprocess.check_output(['git','branch','--show-current'],text=True).strip()=='bolt-v4'
allowed=[
'tools/bolt/rebase-launch-20261111-r6/README.md','tools/bolt/rebase-launch-20261111-r6/SHA256SUMS',
'tools/bolt/rebase-launch-20261111-r6/basedev/SHA256SUMS','tools/bolt/rebase-launch-20261111-r6/basedev/launcher.py',
'tools/bolt/rebase-launch-20261111-r6/basedev/provenance.json','tools/bolt/rebase-launch-20261111-r6/run-night.sh',
'tools/bolt/rebase-launch-20261111-r6/test_serial.py','docs/bolt/STATUS.md']
changed=subprocess.check_output(['git','diff','--name-only'],text=True).splitlines()
assert set(changed)<=set(allowed),changed
report['tracked_changes']=changed
files=[p for p in E.rglob('*') if p.is_file()]
assert not any(p.stat().st_size>=100*1024**2 for p in files)
assert not any('__pycache__' in p.parts for p in files)
report['evidence_file_count']=len(files);report['evidence_bytes']=sum(p.stat().st_size for p in files)
report['statuses']={k:json.load(open(E/k/'result.json'))['status'] for k in ('82','83','84')}
report['timestamp']=datetime.datetime.now().astimezone().isoformat()
(E/'final-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS',len(report['historical_resource_inputs']),'historical input SHA checks;',
      len(report['doc_links']),'document links;',report['statuses'])
