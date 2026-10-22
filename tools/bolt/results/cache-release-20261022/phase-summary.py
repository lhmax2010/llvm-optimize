"""Summarize observed phase anchors and complete du samples; never interpolate a peak."""
import json,re,sys
from pathlib import Path
D=Path(__file__).resolve().parent; E=D/sys.argv[1]
launch=json.loads((E/'launch.json').read_text()); epoch=launch['time_ns']
log=E/'rpm-build.log'
if not log.exists():log=E/'build.log'
origin='launcher time'
observed=E/'rpm-phase-observed.jsonl'
if observed.exists():
 first=json.loads(observed.read_text().splitlines()[0]);m=re.match(r'\[\s*([0-9.]+)s\]',first['text'])
 if m:epoch=first['observed_ns']-int(float(m[1])*1e9);origin='first phase observed time minus native log seconds; polling uncertainty about 1-2s'

patterns=[('install-start',r'Executing\(%install\)'),('disk-report',r'BOLT_DISK_REPORT \{'),('pipeline-pass',r'\] BOLT_PIPELINE_PASS$'),('compare-root-pass',r'\] BOLT_COMPARE_ROOT_PASS$'),('cache-release',r'\] BOLT_CACHE_RELEASE '),('post-pass',r'\] BOLT_POST_GATE_PASS$'),('static-conversion',r'\] \+ (?:python3 |python3 -B ).*llvm-static-archives-native.py'),('candidate-install',r'\] \+ python3 -B .*clang-bolt-helper.py install '),('find-debuginfo',r'\] \+ .*find-debuginfo.sh'),('packaging',r'Processing files:|Wrote:'),('failure',r'BOLT_GATE_FAILED|Bad exit status')]
samples=[]
for line in (E/'du-root-complete.jsonl').read_text().splitlines():
 try:r=json.loads(line)
 except ValueError:continue
 if r['rc']==0 and r['stdout'].split():samples.append(r)
anchors=[];install_seen=False
for n,line in enumerate(log.read_text(errors='replace').splitlines(),1):
 m=re.match(r'\[\s*([0-9.]+)s\]',line)
 if not m:continue
 if 'Executing(%install)' in line:install_seen=True
 task=re.search(r'\[(\d+)/(\d+)\]',line)
 if task and task[1]==task[2] and not install_seen:anchors.append({'line':n,'kind':'ordinary-build-end','elapsed_seconds':float(m[1]),'time_ns':epoch+int(float(m[1])*1e9),'text':line})
 for kind,pat in patterns:
  if re.search(pat,line):
   stamp=epoch+int(float(m[1])*1e9);prior=[r for r in samples if r['time_ns']<=stamp]
   anchors.append({'line':n,'kind':kind,'elapsed_seconds':float(m[1]),'time_ns':stamp,'text':line,'nearest_prior_complete_du':prior[-1] if prior else None})
peak=max(samples,key=lambda r:int(r['stdout'].split()[0])) if samples else None
out={'launch':launch,'time_origin':origin,'anchors':anchors,'sampled_peak':peak,'complete_sample_count':len(samples),'warning':'Discrete samples; scan start and duration are retained. No interpolation. Not a continuous exact peak.'}
(E/'phase-summary.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'anchors':len(anchors),'complete_samples':len(samples),'peak_bytes':int(peak['stdout'].split()[0]) if peak else None}))
