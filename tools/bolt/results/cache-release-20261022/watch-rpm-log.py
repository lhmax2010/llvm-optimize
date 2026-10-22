"""Copy GBS's raw package log and record when phase lines are observed."""
import json,re,subprocess,sys,time
from pathlib import Path
D=Path(__file__).resolve().parent;label=sys.argv[1];rootname=sys.argv[2];E=D/label;unit='bolt-cache-'+label+'.service';R=D/rootname/'local/BUILD-ROOTS/scratch.x86_64.0';src=R/'.build.log';offset=0;inode=None;buf=b'';line_no=0
patterns=('Executing(%prep)','Executing(%build)','Executing(%install)','BOLT_DISK_REPORT','BOLT_PIPELINE_PASS','BOLT_COMPARE_ROOT_PASS','BOLT_CACHE_RELEASE','NATIVE_ARCHIVES_BEGIN','NATIVE_ARCHIVES_END','BOLT_POST_GATE_PASS','find-debuginfo.sh','Processing files:','Wrote:','Bad exit status','BOLT_GATE_FAILED')
def read_new():
 global offset,inode,buf,line_no
 if not src.exists():return
 st=src.stat()
 if inode is not None and (inode!=st.st_ino or st.st_size<offset):raise RuntimeError('package log replaced/truncated; preserve and inspect')
 inode=st.st_ino
 with src.open('rb') as f:f.seek(offset);data=f.read()
 if not data:return
 offset+=len(data)
 with (E/'rpm-build.log').open('ab') as f:f.write(data)
 buf+=data;lines=buf.split(b'\n');buf=lines.pop()
 for line in lines:
  line_no+=1;s=line.decode(errors='replace')
  if any(x in s for x in patterns):
   with (E/'rpm-phase-observed.jsonl').open('a') as f:f.write(json.dumps({'observed_ns':time.time_ns(),'line':line_no,'text':s})+'\n')
while True:
 read_new()
 state=subprocess.run(['systemctl','--user','is-active',unit],capture_output=True,text=True).stdout.strip()
 if state not in ('active','activating','deactivating'):read_new();break
 time.sleep(1)
(E/'rpm-log-copy.json').write_text(json.dumps({'time_ns':time.time_ns(),'source':str(src),'bytes_copied':offset,'inode':inode,'lines':line_no},indent=2)+'\n')
