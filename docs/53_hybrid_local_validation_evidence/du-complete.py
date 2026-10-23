"""Read-only sampler: root lacks timeout(1); Python timeout reaps direct du child."""
import json,subprocess,time
from pathlib import Path
W=Path('/home/linhao/Toolchain/development/llvm-optimize');D=Path(__file__).resolve().parent;E=W/'docs/53_hybrid_local_validation_evidence';R=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
code='''import subprocess,sys
try:
 p=subprocess.run(['/usr/bin/du','-sx','-B1','/'],capture_output=True,text=True,timeout=50)
 sys.stdout.write(p.stdout);sys.stderr.write(p.stderr);sys.exit(p.returncode)
except subprocess.TimeoutExpired:
 print('DU_TIMEOUT_50_SECONDS',file=sys.stderr);sys.exit(124)
'''
while True:
 active=subprocess.run(['systemctl','--user','is-active','hybrid-local-20261023.service'],capture_output=True,text=True).stdout.strip()
 if active not in ('active','activating','deactivating'):break
 stamp=time.time_ns();start=time.monotonic();argv=['sudo','-n','/usr/sbin/chroot',str(R),'/usr/bin/python3','-B','-c',code]
 p=subprocess.run(argv,capture_output=True,text=True)
 with (E/'du-root-complete.jsonl').open('a') as f:f.write(json.dumps({'time_ns':stamp,'argv':argv,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'seconds':time.monotonic()-start})+'\n')
 time.sleep(max(0,60-(time.monotonic()-start)))
print('SAMPLER_DONE')
