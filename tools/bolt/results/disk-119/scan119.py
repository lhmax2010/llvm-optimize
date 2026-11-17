from pathlib import Path
import subprocess,json,datetime,sys
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
OUT=Path(sys.argv[1])
assert OUT.is_absolute() and not OUT.exists()
OUT.mkdir(parents=True)
for p in sorted((W/'temp').iterdir()):
 if not p.is_dir() and not p.is_symlink():continue
 row={'path':str(p),'symlink':p.is_symlink(),'realpath':str(p.resolve()),'entry_mtime':datetime.datetime.fromtimestamp(p.lstat().st_mtime).astimezone().isoformat()}
 try:
  r=subprocess.run(['/usr/bin/du','-s','-x','-B1','--time','--time-style=full-iso','--',str(p)],text=True,capture_output=True,timeout=60)
  row.update(rc=r.returncode,stdout=r.stdout,stderr=r.stderr)
  fields=r.stdout.rstrip('\n').split('\t')
  if len(fields)>=3:row.update(bytes=int(fields[0]),latest_mtime=fields[1])
 except subprocess.TimeoutExpired:row.update(status='UNKNOWN timeout 60s',bytes=None)
 with (OUT/'inventory-raw.jsonl').open('a') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
# Deliberately no inherited inventory classification or deletion here.
# Classification requires the current protection-rules, report evidence,
# Git checks and per-item pre-delete checks recorded for task 119.
