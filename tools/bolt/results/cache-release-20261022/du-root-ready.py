"""Wait for package %prep before invoking du in a newly bootstrapped root."""
import os,subprocess,sys,time
from pathlib import Path
D=Path(__file__).resolve().parent;label=sys.argv[1];rootname=sys.argv[2];unit='bolt-cache-'+label+'.service';R=D/rootname/'local/BUILD-ROOTS/scratch.x86_64.0'
while True:
 p=R/'.build.log'
 if p.exists() and 'Executing(%prep)' in p.read_text(errors='replace'):
  os.execv(sys.executable,[sys.executable,'-B',str(D/'du-root2.py'),unit,label,rootname])
 state=subprocess.run(['systemctl','--user','is-active',unit],capture_output=True,text=True).stdout.strip()
 if state not in ('active','activating','deactivating'):raise SystemExit('build ended before complete-root sampler readiness')
 time.sleep(2)
