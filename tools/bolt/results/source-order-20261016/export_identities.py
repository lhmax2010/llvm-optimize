from pathlib import Path
import hashlib,json
E=Path(__file__).resolve().parent
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024**2),b''):h.update(b)
 return h.hexdigest()
rows={}
for label in ['before','after']:
 rows[label]=[{'name':p.name,'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted((E/('export-'+label)).iterdir()) if p.is_file()]
left={r['name']:r for r in rows['before']};right={r['name']:r for r in rows['after']};changes=[n for n in left.keys()|right.keys() if left.get(n)!=right.get(n)]
# gbs also exports the sibling libcxx-runtimes spec and its vcs tag; main source inputs and seven generated patches must be identical.
for name in ['llvm-22.1.8.tar.gz','clang-bolt-v2.fdata.xz','clang-bolt-helper.py','llvm-static-archives-native.py']+[p.name for p in (E/'export-before').glob('*.patch')]:assert left[name]==right[name],name
(E/'export-identities.json').write_text(json.dumps({'status':'PASS','files':rows,'changed_export_files':changes},indent=2)+'\n')
print('export main payload and all seven patches identical PASS; changed exported files:',changes)
