from pathlib import Path
import json,re,hashlib,subprocess
E=Path(__file__).resolve().parent;B=E.parents[3]
old=json.loads((B/'tools/bolt/results/perf-c-o2-os-20261025/runtime-loader-list.json').read_text())
paths=set(re.findall(r'=> (/[^ ]+) ',old['stdout']));paths.add(old['argv'][0])
root=Path(old['argv'][0]).parent.parent
resource=root/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64/clang/22'
rows=[]
for raw in sorted(paths|{str(p) for p in resource.rglob('*') if p.is_file()}):
 p=Path(raw);s=p.stat()
 with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 rows.append(dict(path=raw,resolved=str(p.resolve()),bytes=s.st_size,allocated=s.st_blocks*512,sha256=h,symlink=p.is_symlink()))
(E/'runtime-preservation.json').write_text(json.dumps(dict(root=str(root),resource=str(resource),files=rows,note='Preserve these runtime libraries and the whole resource directory before deleting hybrid+BOLT gbs-root; no copy performed'),indent=2)+'\n')
print('runtime/resource files',len(rows),'bytes',sum(r['bytes'] for r in rows))
