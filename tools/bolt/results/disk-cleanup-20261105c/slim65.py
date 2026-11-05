from pathlib import Path
import json,gzip,os,stat,subprocess,time,hashlib
from checks import command,stamp,process_snapshot,mount_snapshot
E=Path(__file__).resolve().parent;OLD=E.parent/'disk-review-group2-20261105';W=Path('/home/linhao/Toolchain/development/llvm-optimize/temp')
names=['arm-source-root-probes-20261010','arm-archive-stage1-20261010','bolt-v4-20261022-cache-release','crash-probe-20261028','llvm-optimize-intranet-20261020','qb-meta-switch-20261028']
expected={}
for p in [*OLD.glob('*/hashes.json'),OLD/'probe-binary-hashes.json',OLD/'additional-tool-hashes.json',OLD/'identity-hashes.json',OLD/'handoff-assets.json']:
 if p.exists():
  for x in json.loads(p.read_text()):
   h=x.get('hash',{}).get('sha256')
   if h:expected[x['path']]=h
for r in json.loads((OLD/'archive-copy-comparison.json').read_text()):
 for x in r['files']:
  if x['equal']:expected[x['path']]=x['hash']['sha256']
results=[]
for n in names:
 root=W/n;rec={'name':n,'time_start':stamp(),'df_before':command(['df','-B1','/home']),'candidates':[],'deleted':[],'skipped':[]}
 plan=json.loads((OLD/n/'recommendation.json').read_text());files=[]
 for line in gzip.open(OLD/n/'suggested-files.tsv.gz','rt'):
  if line.startswith('path\t'):continue
  files.append(line.rstrip('\n').split('\t')[0])
 assert all(p.startswith(str(root)+'/') for p in files)
 # An unverified directory candidate is kept intact rather than partially damaging a checkout/runtime.
 omitted=set()
 for c in plan['candidate_paths']:
  p=Path(c['path']);members=[s for s in files if s==str(p) or s.startswith(str(p)+'/')]
  missing=[s for s in members if s not in expected]
  if missing:
   omitted.update(members);rec['skipped'].append({'path':str(p),'reason':'65 evidence has no historical SHA for every member; keep this candidate intact','missing_sha_files':missing,'retained_files':len(members)})
 proc=process_snapshot([str(root)]);mnt=mount_snapshot([str(root)]);rec['occupancy']=proc;rec['mounts']=mnt
 if proc['matches'] or mnt['matches'] or mnt['rc']:
  rec['skipped'].append({'path':str(root),'reason':'visible process or mount; entire item retained'});omitted.update(files)
 for path in files:
  if path in omitted:continue
  p=Path(path);row={'path':path,'expected_sha256':expected.get(path)}
  try:
   s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink() and str(p.resolve())==path,'not a real regular file'
   assert s.st_uid==os.getuid() and os.access(p.parent,os.W_OK),'not ordinary-user removable'
   q=command(['timeout','120','nice','-n','19','ionice','-c3','sha256sum','--',path],130);row['hash_query']=q
   assert q['rc']==0 and q['stdout'].split()[0]==row['expected_sha256'],'SHA mismatch or UNKNOWN'
   s2=p.stat();assert (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns)==(s2.st_dev,s2.st_ino,s2.st_size,s2.st_mtime_ns),'changed during hashing'
   q=command(['rm','-f','--',path],60);row['remove']=q;assert q['rc']==0 and not p.exists(),'rm failed'
   rec['deleted'].append(row)
  except Exception as ex:row['reason']=str(ex);rec['skipped'].append(row)
  (E/('slim-'+n+'.json')).write_text(json.dumps(rec,ensure_ascii=False,indent=2))
 rec['df_after']=command(['df','-B1','/home']);rec['time_end']=stamp();rec['remaining_candidate_paths']=[p for p in files if os.path.lexists(p)]
 rec['end_line']='SLIM65 已结束 '+rec['time_end']+' status='+('partial' if rec['skipped'] else 'ok')+' path='+n+' deleted='+str(len(rec['deleted']))+' retained='+str(len(rec['remaining_candidate_paths']))
 (E/('slim-'+n+'.json')).write_text(json.dumps(rec,ensure_ascii=False,indent=2));results.append({'name':n,'deleted':len(rec['deleted']),'retained':len(rec['remaining_candidate_paths']),'end_line':rec['end_line']});(E/'slim-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2));print(rec['end_line'],flush=True)
print('SLIM65_ALL 已结束 '+stamp()+' status=partial reason=historical-SHA-missing-candidates-preserved',flush=True)
