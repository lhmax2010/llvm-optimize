"""Reclassify existing B6 evidence under PM's independent permission/content rule.
No RPM extraction, tar extraction, patch execution, build, or old-result mutation.
"""
from pathlib import Path
import sys, json, gzip, hashlib, subprocess, datetime, traceback
HERE=Path(__file__).resolve().parent
E=HERE.parent
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
C=W/'temp/rebase-359934-20261111-r6/source'
HEAD='fea0fe464d56e17f2c7588c557bfffd9f6ac352b'
project=sys.argv[1]
O=HERE/project;O.mkdir(exist_ok=False)
old=E/'resume2-20261112'/project/'source'
comp=E/('resume-20261112' if project=='toolchain' else 'resume2-20261112')/project/'comparison'
P=W/('temp/qb79-local-resume-20261112' if project=='toolchain' else 'temp/qb79-local-resume2-20261112')/project/'payload/llvm-src'
X=W/'temp/qb79-source-resume2-20261112'/project
reads={}
def read(p):
 p=Path(p);raw=p.read_bytes();reads[str(p)]=hashlib.sha256(raw).hexdigest();return raw
def js(p):
 raw=read(p)
 if str(p).endswith('.gz'):raw=gzip.decompress(raw)
 return json.loads(raw)
def sha(p):return hashlib.sha256(read(p)).hexdigest()
def save(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def metadata(x,y,tar=False):
 keys=['uid','gid','link','type'] if tar else ['uid','gid','target']
 assert all(x.get(k)==y.get(k) for k in keys),('owner/type/link',x,y)
 same=x['mode']==y['mode']
 group=(x['mode']&0o7777==0o664 and y['mode']&0o7777==0o644 and x['mode']^y['mode']==0o20)
 assert same or group,('unapproved permission',x,y)
 return 'identical' if same else 'R2(a):0664->0644,group-write-only'
def main():
 a=js(comp/'llvm-src-local-manifest.json.gz');b=js(comp/'llvm-src-qb-manifest.json.gz')
 added=sorted(b.keys()-a.keys());assert not a.keys()-b.keys()
 assert len(added)==8 and [n[:4] for n in added]==[f'{i:04}' for i in range(1,9)]
 for n in added:
  assert sha(P/'qb'/n)==b[n]['sha256']
  assert b[n]['mode']==0o100644 and b[n]['uid']==0 and b[n]['gid']==0 and not b[n].get('target')
  text=read(old/('apply-'+n+'.txt')).decode()
  assert text.rstrip().endswith('rc=0'),n
 # Existing tar inventories and already patched target copies establish contents.
 ta=js(old/'tar-local-original-manifest.json.gz')
 tb=js(old/'tar-qb-original-manifest.json.gz')
 patched={r['file']:r for r in js(old/'patched-targets.json')}
 classified={r['file']:r for r in js(old/'tar-classified-differences.json')}
 assert len(patched)==27
 details=[];paired=0;identical=0
 for n in sorted(ta.keys()|tb.keys()):
  x,y=ta.get(n),tb.get(n)
  if y is None:
   assert n=='packaging' or n.startswith('packaging/'),n
   proof=classified[n]['proof'];assert proof['rule']=='R2(c)'
   if n=='packaging':assert x['type']=='5'
   else:
    raw=subprocess.check_output(['git','-C',str(C),'show',HEAD+':'+n])
    assert hashlib.sha256(raw).hexdigest()==x['sha256']==proof['git_sha256']
    assert sha(X/'local'/n)==x['sha256']
   details.append(dict(file=n,permission='PASS:unpaired R2(c) addition; original metadata retained',content='PASS:R2(c)',local=x,qb=None))
   continue
  assert x is not None,n
  perm=metadata(x,y,True);paired+=1
  if x.get('sha256')==y.get('sha256'):
   assert x['size']==y['size'],n
   identical+=1
   continue
  if n in patched:
   proof=patched[n];assert proof['all_tar_metadata_equal']
   assert sha(X/'qb'/n)==sha(X/'local'/n)==x['sha256']==proof['sha256'],n
   assert (X/'qb'/n).stat().st_size==x['size']
   rule='R2(b):eight patch applications succeeded; target content equal'
  elif n=='clang/bindings/python/.git_archival.txt':
   ll=read(X/'local'/n);rr=read(X/'qb'/n)
   assert hashlib.sha256(ll).hexdigest()==x['sha256'] and hashlib.sha256(rr).hexdigest()==y['sha256']
   def clean(raw):
    return [l for l in raw.splitlines(True) if not l.startswith((b'node: ',b'node-date: ',b'describe-name: '))]
   assert clean(ll)==clean(rr)
   assert len(ll.splitlines())-len(clean(ll))==3 and len(rr.splitlines())-len(clean(rr))==3
   rule='R2(d):only node/node-date/describe-name'
  else:raise AssertionError(('tar content outside R2',n))
  details.append(dict(file=n,permission='PASS:'+perm,content='PASS:'+rule,local=x,qb=y))
 save('tar-dimension-evidence.json',details)
 # Recheck exact spec differences using the prior proof's explicit allowed lines.
 specproof=js(old/'spec-content-proof.json')
 canon=[]
 for side,mapping in [('local',a),('qb',b)]:
  raw=read(P/side/'llvm.spec');assert hashlib.sha256(raw).hexdigest()==mapping['llvm.spec']['sha256']
  lines=raw.decode().splitlines(True)
  for line in specproof[side+'_allowed_lines']:
   assert line in lines
   lines.remove(line)
  canonical=''.join(lines).encode()
  assert hashlib.sha256(canonical).hexdigest()==specproof['canonical_sha256']
  canon.append(canonical)
 assert canon[0]==canon[1]
 rows=[]
 for n in sorted(a.keys()&b.keys()):
  x,y=a[n],b[n];perm=metadata(x,y)
  if x.get('sha256')==y.get('sha256'):
   assert x['bytes']==y['bytes'];content='same raw SHA256'
  elif n=='llvm.spec':content='R2(e):exact allowed spec lines; canonical SHA equal'
  elif n=='llvm-22.1.8.tar.gz':content='R2(b/c/d):full tar inventory and file-by-file proofs'
  else:raise AssertionError(('source content outside R2',n))
  rows.append(dict(file=n,local=x,qb=y,permission_verdict='PASS',permission_rule=perm,content_verdict='PASS',content_rule=content,verdict='PASS'))
 for n in added:
  rows.append(dict(file=n,local=None,qb=b[n],permission_verdict='PASS',permission_rule='unpaired R2(b) source addition; mode0644 uid0 gid0 regular file; no changed counterpart',content_verdict='PASS',content_rule='R2(b):patch bytes and successful application evidence verified',verdict='PASS'))
 save('source-files-two-dimensions.json',rows)
 result=dict(project=project,raw_source_status='FAIL',R2_source_status='PASS',files=len(rows),paired_files=len(a),QB_only_patches=len(added),permission_pass=len(rows),content_pass=len(rows),tar_entries_local=len(ta),tar_entries_qb=len(tb),tar_paired=paired,tar_unchanged_content=identical,patched_targets=len(patched),packaging_files=sum(d['file'].startswith('packaging/') for d in details),no_unpack=True,old_results_modified=False)
 save('result.json',result)
 print(json.dumps(result,ensure_ascii=False),flush=True)
try:main()
except BaseException as ex:
 save('result.json',dict(status='UNKNOWN' if isinstance(ex,MemoryError) else 'FAIL',reason=str(ex)))
 (O/'failure.txt').write_text(traceback.format_exc());raise
finally:
 save('input-evidence-sha256.json',reads)
 z=json.loads((O/'result.json').read_text())
 line='B6_R2 已结束 '+datetime.datetime.now().astimezone().isoformat()+' '+project+' status='+z.get('R2_source_status',z.get('status','UNKNOWN'))
 (O/'end.txt').write_text(line+'\n');print(line,flush=True)
