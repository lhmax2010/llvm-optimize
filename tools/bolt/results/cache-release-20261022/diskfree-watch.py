"""Local filesystem safety sampling independent of du; not build-root attribution."""
import json,shutil,subprocess,sys,time
from pathlib import Path
D=Path(__file__).resolve().parent;label=sys.argv[1];E=D/label;unit='bolt-cache-'+label+'.service'
while True:
 state=subprocess.run(['systemctl','--user','is-active',unit],capture_output=True,text=True).stdout.strip()
 if state not in ('active','activating','deactivating'):break
 u=shutil.disk_usage(D);r={'time_ns':time.time_ns(),'path':str(D),'filesystem_device':D.stat().st_dev,'total':u.total,'used':u.used,'free':u.free,'scope':'filesystem; includes unrelated writers, not root du'}
 with (E/'filesystem-independent.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
 if u.free<30*1024**3:
  (E/'diskfree-emergency-stop.json').write_text(json.dumps(r)+'\n');subprocess.run(['systemctl','--user','stop',unit]);break
 time.sleep(5)
