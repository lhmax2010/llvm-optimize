from pathlib import Path
import subprocess,json,hashlib,urllib.request,xml.etree.ElementTree as X
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';E=B/'tools/bolt/results/qb-meta-switch-20261028';D=E/'second-ruling';R=W/'temp/qb-meta-20261028/repo'
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def save(n,d): (D/n).write_text(json.dumps(d,indent=2)+'\n')
prov=[]
for n,url in [('unified-standard.xml','https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified/tizen-unified_20261027.231956/builddata/manifest/tizen-unified_20261027.231956_standard.xml'),('base-standard.xml','https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base/tizen-base_20261026.005418/builddata/manifest/tizen-base_20261026.005418_standard.xml')]:
 with urllib.request.urlopen(url,timeout=60) as r:b=r.read();prov.append(dict(url=url,status=r.status,final_url=r.url,file=n,size=len(b),sha256=hashlib.sha256(b).hexdigest()))
 (D/n).write_bytes(b)
save('snapshot-url-provenance.json',prov)
f='TIZEN/Tizen/Tizen-Base-Toolchain/manifest.xml'
a=git('show','3c78318b^:'+f);b=git('show','3c78318b:'+f);assert a==b
(D/'3c78318b.diff').write_bytes(git('show','--format=fuller','3c78318b'))
(D/'meta-manifest-before.xml').write_bytes(a);(D/'meta-manifest-after.xml').write_bytes(b)
def repos(b):return {x.get('name'):x.get('revision') for x in X.fromstring(b).iter('project')}
m=repos(a);snap=repos((D/'base-standard.xml').read_bytes());q=json.loads((B/'tools/bolt/results/qb-fail-20261028/meta/buildconf/1211018-package-lists.json').read_text())[0]['packages']
save('source-mechanism.json',dict(meta_before_sha256=hashlib.sha256(a).hexdigest(),meta_after_sha256=hashlib.sha256(b).hexdigest(),meta_git_blob_before=git('rev-parse','3c78318b^:'+f).decode().strip(),meta_git_blob_after=git('rev-parse','3c78318b:'+f).decode().strip(),meta_count=len(m),qb_count=len(q),snapshot_count=len(snap),added=[dict(repo=n,qb=q[n],snapshot=snap.get(n)) for n in sorted(q.keys()-m.keys())],removed=sorted(m.keys()-q.keys()),changed=[dict(repo=n,meta=m[n],qb=q[n],snapshot=snap.get(n)) for n in sorted(q.keys()&m.keys()) if q[n]!=m[n]],snapshot_differences=[dict(repo=n,snapshot=snap.get(n),qb=q.get(n)) for n in sorted(snap.keys()|q.keys()) if q.get(n)!=snap.get(n)]))
print((D/'source-mechanism.json').read_text())
