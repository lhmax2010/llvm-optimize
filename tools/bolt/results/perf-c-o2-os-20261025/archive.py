"""Archive this task's raw evidence losslessly; keep originals in its temp directory."""
from pathlib import Path
import json,gzip,hashlib,tarfile,shutil
E=Path(__file__).resolve().parent
D=Path(json.loads((E/'config.json').read_text())['work'])/'raw-uncompressed'
assert json.loads((E/'finished.json').read_text())['status']=='COMPLETE'
assert json.loads((E/'clean-c/finished.json').read_text())['status']=='COMPLETE'
D.mkdir(exist_ok=True)
records=[]
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
for relative in ['.','clean-c','preparation-timer-pilot']:
    root=E/relative;dest=D/relative;dest.mkdir(exist_ok=True,parents=True)
    logs=root/'compile-logs'
    if logs.exists():
        entries=[dict(path=str(p.relative_to(logs)),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(logs.glob('*.txt'))]
        index=dict(files=entries,nonempty=[str((logs/x['path']).relative_to(E)) for x in entries if x['bytes']])
        (root/'compile-log-index.json').write_text(json.dumps(index,indent=2)+'\n')
        archive=root/'compile-logs.tar.gz'
        with tarfile.open(archive,'w:gz') as t:t.add(logs,arcname='compile-logs')
        with tarfile.open(archive,'r:gz') as t:
            for x in entries:
                assert hashlib.sha256(t.extractfile('compile-logs/'+x['path']).read()).hexdigest()==x['sha256']
        assert not (dest/'compile-logs').exists()
        shutil.move(logs,dest/'compile-logs')
        records.append(dict(archive=str(archive.relative_to(E)),sha256=sha(archive),bytes=archive.stat().st_size,files=len(entries),uncompressed_preserved=str(dest/'compile-logs')))
    samples=root/'samples.jsonl'
    if samples.exists():
        data=samples.read_bytes();out=root/'samples.jsonl.gz';out.write_bytes(gzip.compress(data,mtime=0));assert gzip.decompress(out.read_bytes())==data
        assert not (dest/samples.name).exists();shutil.move(samples,dest/samples.name)
        records.append(dict(archive=str(out.relative_to(E)),sha256=sha(out),bytes=out.stat().st_size,raw_bytes=len(data),raw_sha256=hashlib.sha256(data).hexdigest(),uncompressed_preserved=str(dest/samples.name)))
(E/'archive-manifest.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records,indent=2))
