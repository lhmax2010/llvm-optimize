from pathlib import Path
import json,subprocess
E=Path(__file__).resolve().parent;W=Path('/home/linhao/Toolchain/development/llvm-optimize');root=W/'temp/qb-1216409-1216410';rows=[]
for p in root.rglob('*.rpm'):
 if not p.is_file():continue
 s=p.stat();rows.append({'path':str(p),'bytes':s.st_size,'dev':s.st_dev,'ino':s.st_ino})
(E/'qb-rpm-metadata.json').write_text(json.dumps(rows,indent=2))
print('QB RPM candidate paths',len(rows))
