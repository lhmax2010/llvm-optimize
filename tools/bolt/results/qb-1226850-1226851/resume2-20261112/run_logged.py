from pathlib import Path
import subprocess,sys
dest=Path(sys.argv[1])
with dest.open('x') as f:
 p=subprocess.Popen(sys.argv[2:],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 for line in p.stdout:
  f.write(line);f.flush();print(line,end='',flush=True)
 sys.exit(p.wait())
