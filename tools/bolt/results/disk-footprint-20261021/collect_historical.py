#!/usr/bin/env python3
"""Read-only historical footprint audit; writes evidence beside this script only.
No cmake/ninja, privileged action, build or cleanup is performed.
"""
import datetime, gzip, hashlib, json, os, re, shutil, subprocess, time
import xml.etree.ElementTree as ET
from pathlib import Path
D=Path(__file__).resolve().parent
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
B=W.parent/'llvm-optimize-bolt'
E=W/'temp/bolt-v4-20261021-disk-footprint'
OLD=W/'temp/release-x86-full-build-20261013/round2-eight-output-proof'
R25=W/'temp/bolt-v4-20261015-install-rehearsal'
S=W/'temp/bolt-v4-20261013/v41/llvm-source'
G=2**30
stamp=lambda:datetime.datetime.now().astimezone().isoformat()
def digest(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def save(n,x): (D/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def git(*args):return subprocess.check_output(['git','--no-optional-locks','-C',str(S),*args],text=True).strip()
meta=ET.fromstring((D/'repomd.xml').read_bytes())
ns={'r':'http://linux.duke.edu/metadata/repo'}
data=next(x for x in meta.findall('r:data',ns) if 'build.conf' in x.find('r:location',ns).get('href'))
verification={
 'compressed_sha256':digest(D/'build.conf.gz'),
 'expected_compressed_sha256':data.find('r:checksum',ns).text,
 'uncompressed_sha256':digest(D/'build.conf'),
 'expected_uncompressed_sha256':data.find('r:open-checksum',ns).text,
 'compressed_bytes':(D/'build.conf.gz').stat().st_size,
 'uncompressed_bytes':(D/'build.conf').stat().st_size,
 'local_copy_identical':(E/'build.conf').read_bytes()==(D/'build.conf').read_bytes(),
 'gzip_content_identical':gzip.decompress((D/'build.conf.gz').read_bytes())==(D/'build.conf').read_bytes(),
}
assert verification['compressed_sha256']==verification['expected_compressed_sha256']
assert verification['uncompressed_sha256']==verification['expected_uncompressed_sha256']
assert verification['local_copy_identical'] and verification['gzip_content_identical']
verification['status']='PASS';save('build-conf-verification.json',verification)
raw=(OLD/'root-space-samples.jsonl').read_bytes()
with (D/'historical-off-root-space-samples.jsonl.gz').open('wb') as f:
 with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z:z.write(raw)
rows=[json.loads(x) for x in raw.splitlines()]
valid=[]
for n,row in enumerate(rows,1):
 m=re.match(r'^(\d+)\t(.+)\n?$',row.get('stdout',''))
 if m: valid.append({'source_line':n,'allocated_bytes':int(m[1]),'path':m[2],**row})
assert len(valid)==len(rows)
maximum=max(valid,key=lambda x:x['allocated_bytes'])
summary={'kind':'historical OFF sampled lower bound, not same-condition ON/OFF comparison',
 'source_path':str(OLD/'root-space-samples.jsonl'),'source_sha256':hashlib.sha256(raw).hexdigest(),
 'rows':len(rows),'first':valid[0],'observed_maximum':maximum,'last':valid[-1],
 'error_rows':sum(x['exit']!=0 for x in valid),'permission_error_examples':rows[0]['stderr'].splitlines(),
 'watch_end':json.loads((OLD/'root-space-watch-reaped.json').read_text()),
 'coverage_limit':'Three permission blind spots in every du sample; observer timed out after last sample, before post and packaging finished. du target is the enclosing GBS buildroot, not just scratch chroot.',
 'install_start':'2026-10-14T05:48:16+08:00','post_start':'2026-10-14T06:24:22+08:00',
 'packaging_start':'2026-10-14T06:35:39+08:00','normal_build_end':'2026-10-14T06:49:10+08:00',
 'independent_install_later':'2026-10-14T12:13:03+08:00; not included in sample maximum',
 'environment':'Base 20261010.120615, Unified 20260814.092727; cb679968 plus archive patches; not 9e5675f with Base 20261013.024319'}
save('historical-off-summary.json',summary)
with (D/'historical-off-samples.tsv').open('w') as f:
 f.write('source_line\ttime\tallocated_bytes\tdu_exit\tstage\n')
 for x in valid:
  t=x['time'];stage='ordinary-build' if t<summary['install_start'] else ('ordinary-install-and-native-archive-conversion' if t<summary['post_start'] else 'platform-post')
  f.write(f"{x['source_line']}\t{t}\t{x['allocated_bytes']}\t{x['exit']}\t{stage}\n")
# Read-only endpoint measurements of the retained BOLT rehearsal upper layer.
upper=R25/'upper'; rb=upper/'home/abuild/rpmbuild';build=rb/'BUILD/llvm-22.1.8/build'
groups=[('ordinary_build_overlay_changes',build),('bolt_tool_objects',build/'tools/bolt'),
 ('bolt_tool_executable',build/'bin/llvm-bolt'),('pipeline_work',build/'clang-bolt'),
 ('thinlto_cache_overlay_entries',build/'lto.cache'),('ordinary_BUILDROOT',rb/'BUILDROOT'),
 ('RPM_overlay_entries',rb/'RPMS'),('static_archive_conversion',build/'native-archive-conversion')]
groups += [('bolt_tool_library',p) for p in sorted((build/'lib64').glob('libLLVMBOLT*.a'))]
du_rows=[]
for label,p in groups:
 if not p.exists():
  du_rows.append({'category':label,'path':str(p),'exists':False});continue
 command=['du','-sx','-B1','--',str(p)]
 t=time.monotonic();r=subprocess.run(command,capture_output=True,text=True,timeout=50)
 du_rows.append({'time':stamp(),'category':label,'path':str(p),'exists':True,
  'argv':command,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'wall_seconds':time.monotonic()-t,
  'allocated_bytes':int(r.stdout.split()[0]) if r.stdout else None})
# Do not sum the parent build and its BOLT/cache children: they overlap.
save('historical-rehearsal-current-du.json',{'kind':'current retained endpoint, NOT peak, NOT full merged buildroot',
 'time':stamp(),'rows':du_rows,'overlap_note':'ordinary_build_overlay_changes contains the BOLT and cache child categories. The old upper also contains baseline installation; it is not BOLT-only.',
 'on_source':'506dc25, historical docs38 lower; install-only aborted during relink at local 55-minute compute limit'})
snap=json.loads((R25/'actual/install-before.json').read_text())
files=snap['files'];ordinary=files['usr/bin/clang-22']
work_entries=[]
for p in sorted((build/'clang-bolt').rglob('*')):
 s=p.lstat()
 if p.is_file() and not p.is_symlink():work_entries.append({'path':str(p.relative_to(build/'clang-bolt')),'bytes':s.st_size,'allocated_bytes':s.st_blocks*512,'mtime_ns':s.st_mtime_ns})
save('historical-rehearsal-endpoint.json',{'time':stamp(),'ordinary_install_snapshot_sha256':digest(R25/'actual/install-before.json'),
 'paths':len(files),'regular_file_logical_bytes':sum(v.get('bytes',0) for v in files.values() if v.get('type')=='file'),
 'ordinary_installed_clang':ordinary,'work_files':work_entries,
 'retention_original_record':json.loads((R25/'upper-retained.json').read_text()),
 'mtimes_are_not_birth_or_last_use':'mtime is the last content modification only. No access-time trace or complete stage lifetime trace exists.'})
# Show only directly documented historical relink facts, not the enormous command.
x=json.loads((B/'tools/bolt/results/relink-first-relink.json').read_text())
save('historical-relink-summary.json',{k:x[k] for k in ['status','link_wall_s','strip_debug_wall_s','before_strip_bytes','before_strip_sha256','after_strip_bytes','after_strip_sha256','cache_after_files','cache_after_bytes','cache_policy']})
# Input/config evidence from the existing raw child log, no network/QB actions.
log=gzip.decompress((B/'tools/bolt/results/qb-timeout-20261021/child/1202084-full-log.txt.gz').read_bytes()).decode().splitlines()
selection=set([130,316,523]); selection.update(range(324,349))
(D/'qb-config-excerpts.txt').write_text(''.join(f'C:L{n}: {log[n-1]}\n' for n in sorted(selection)))
# A historical footprint cannot certify this snapshot, but is a conservative local admission reference.
space=[]
for p in [W,Path('/var/tmp')]:
 s=os.statvfs(p);free=s.f_bavail*s.f_frsize
 space.append({'path':str(p),'device':p.stat().st_dev,'available_bytes':free,'required_local_reserve_bytes':30*G,
 'available_for_new_writes_after_reserve':max(0,free-30*G),
 'historical_OFF_lower_bound_bytes':maximum['allocated_bytes'],
 'historical_OFF_lower_bound_plus_reserve_bytes':maximum['allocated_bytes']+30*G,
 'shortfall_against_historical_OFF_reference_bytes':max(0,maximum['allocated_bytes']+30*G-free)})
mem=Path('/proc/meminfo').read_text();avail=int(re.search(r'^MemAvailable:\s+(\d+)',mem,re.M)[1])*1024
save('local-admission.json',{'time':stamp(),'status':'NOT_STARTED_DISK_CAPACITY_REFERENCE_UNMET',
 'memory_available_bytes':avail,'heavy_entry_required_bytes':12*G,'memory_entry_pass':avail>=12*G,
 'filesystems':space,'source_HEAD':git('rev-parse','HEAD'),'source_status_porcelain':git('status','--porcelain'),
 'source_spec_sha256':digest(S/'packaging/llvm.spec'),'source_helper_sha256':digest(S/'packaging/clang-bolt-helper.py'),
 'original_W_config_sha256':digest(W/'gbs_llvm.conf'),
 'why_not_started':'The destination cannot accommodate even the known historical OFF sampled lower bound plus the local reserve. This is not a measured requirement of the new snapshot, and excludes additional BOLT/export costs. No protected assets were removed to make room.',
 'additional_rule':'Full-build scheduling must also preserve shared-lock holds of at most 60 minutes; no long-lived build or lock started.',
 'shared_lock_acquired':False,'full_build_started':False,'source_changes':False,'cleanup_performed':False,
 'five_parse_checks':'NOT RUN: no new source commit/export produced'})
save('collection-result.json',{'time':stamp(),'status':'HISTORICAL_INVENTORY_AND_INPUTS_READY_FULL_MEASUREMENT_BLOCKED',
 'measured_ON_peak_bytes':None,'measured_same_condition_OFF_peak_bytes':None,'BOLT_extra_peak_bytes':None,
 'cleanup_reduction_bytes':None,'new_candidate_SHA':None,'original_candidate_untouched':True,
 'filesystems':space,'no_production_or_Gerrit_changes':True})
print(json.dumps({'status':'INVENTORY_READY_BUILD_NOT_STARTED','historical_OFF_sampled_lower_bound_bytes':maximum['allocated_bytes'],
 'filesystem_admission':space,'rehearsal_endpoint_du':[(x['category'],x.get('allocated_bytes')) for x in du_rows]},indent=2))
