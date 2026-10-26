from pathlib import Path
import json,hashlib,os,time
E=Path(__file__).resolve().parent;W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=E.parents[3]
found=json.loads((E/'assets-found.json').read_text());selected={}
new=['bolt-v4-20261022-cache-release','hybrid-local-20261023','bolt-on-hybrid-20261024']
for a in found:
 p=Path(a['path']);name=p.name;top=Path(a['top']).name
 reason=None
 if name in ['identity.json','preserved.json','build.conf','gbs_llvm_qb1202084.conf','clang-bolt-v2.fdata.xz'] or name.endswith('.fdata'):reason='identity/profile/config'
 if name in ['clang-22','ordinary-clang-22','llvm-bolt'] and (top in new or p.parent.name=='bin' and '/rpmbuild/BUILD/' in str(p) or 'preserved-from-upper' in str(p)):reason='key compiler/tool'
 if name.endswith('.rpm') and name.startswith('llvm') and ('/rpmbuild/RPMS/' in str(p) or '/rpms-docs35/' in str(p) or '/products/' in str(p) or '-products/' in str(p)):reason='original LLVM RPM / preserved product'
 if reason:selected[str(p)]=reason
# Mandatory preservation assets and current measurement inputs.
for group in json.loads((B/'tools/bolt/results/perf-c-o2-os-20261025/compiler-identities.json').read_text()).values():
 for item in group.values():selected[item['path']]='mandatory compiler product'
for case in json.loads((B/'tools/bolt/results/perf-c-o2-os-20261025/cases.json').read_text()):selected[case['input']]='mandatory C/C++ measurement input'
for p in (W/'temp/hybrid-local-20261023/tu-inputs').glob('*.ii'):selected[str(p)]='mandatory 90-TU asset'
for parent in ['baseline-products','revised-products']:
 for p in (W/'temp/bolt-v4-20261022-cache-release'/parent/'binaries').glob('*'):
  if p.is_file():selected[str(p)]='mandatory preserved binary'
for p in (W/'temp/bolt-on-hybrid-20261024/products/binaries').glob('*'):
 if p.is_file():selected[str(p)]='mandatory preserved binary'
rows=[];cache={};total=0
(E/'hash-selection.json').write_text(json.dumps(selected,indent=2)+'\n')
print('selected',len(selected),'logical GiB',sum(Path(p).stat().st_size for p in selected if Path(p).is_file())/2**30,flush=True)
for i,(raw,reason) in enumerate(sorted(selected.items())):
 p=Path(raw);row=dict(path=raw,reason=reason)
 try:
  st=p.stat();key=(st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns);row.update(bytes=st.st_size,allocated=st.st_blocks*512,uid=st.st_uid,ino=st.st_ino,dev=st.st_dev,mtime_ns=st.st_mtime_ns)
  if key not in cache:
   with p.open('rb') as f:cache[key]=hashlib.file_digest(f,'sha256').hexdigest()
   total+=st.st_size
  row['sha256']=cache[key];row['stable_during_read']=p.stat().st_mtime_ns==st.st_mtime_ns and p.stat().st_size==st.st_size
 except OSError as x:row['error']=str(x)
 rows.append(row)
 if i%10==0:
  (E/'asset-hashes.json').write_text(json.dumps(rows,indent=2)+'\n');print(i,'read GiB',round(total/2**30,2),flush=True)
(E/'asset-hashes.json').write_text(json.dumps(rows,indent=2)+'\n');(E/'hash-complete.json').write_text(json.dumps(dict(time=time.time(),files=len(rows),bytes_read=total))+'\n')
