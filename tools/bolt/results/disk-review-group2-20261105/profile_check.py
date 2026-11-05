import json,subprocess,hashlib,lzma,time
from pathlib import Path
E=Path(__file__).resolve().parent;W=Path('/home/linhao/Toolchain/development/llvm-optimize');R=W/'temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0'
manifest=W/'temp/bolt-aarch64-v2-20260921/profile-work/result.json';m=json.loads(manifest.read_text())
rows=[{'path':p,'expected':h,'target':'armv7l'} for p,h in sorted(m['original_profiles'].items())]+[{'path':x['path'],'expected':x['sha256'],'target':'aarch64'} for x in m['new_profiles']]
def sha(p):
 r=subprocess.run(['timeout','120','nice','-n','19','ionice','-c3','sha256sum','--',str(p)],capture_output=True,text=True)
 return {'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'sha256':r.stdout.split()[0] if r.returncode==0 else None}
for x in rows:
 x['actual']=sha(x['path']);x['size']=Path(x['path']).stat().st_size;x['match']=x['actual']['sha256']==x['expected']
source=W/'temp/review-20261102/source/packaging/clang-bolt-v2.fdata.xz'
result={'manifest':str(manifest),'profiles':rows,'all_match':all(x['match'] for x in rows),'source':str(source),'source_hash':sha(source),'original_merged':m['merged_profile'],'original_merge_hash':sha(m['merged_profile']['path'])}
h=hashlib.sha256();length=0
with lzma.open(source,'rb') as f:
 for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk);length+=len(chunk)
result['source_uncompressed']={'sha256':h.hexdigest(),'bytes':length}
# Analysis-only remerge, stdout streamed to hash; no original files written.
tool=R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/merge-fdata'
loader=R/'lib64/ld-linux-x86-64.so.2'
argv=['timeout','180','nice','-n','19','ionice','-c3',str(loader),'--library-path',str(R/'lib64')+':'+str(R/'usr/lib64'),str(tool)]+[x['path'] for x in rows]
result['remerge_argv']=argv;result['tool_hash']=sha(tool);start=time.monotonic()
with (E/'profile-remerge.stderr').open('wb') as err:
 p=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=err);h=hashlib.sha256();size=0
 for chunk in iter(lambda:p.stdout.read(1024*1024),b''):h.update(chunk);size+=len(chunk)
 rc=p.wait()
result['remerge']={'rc':rc,'seconds':time.monotonic()-start,'bytes':size,'sha256':h.hexdigest(),'matches_Source1200':rc==0 and h.hexdigest()==result['source_uncompressed']['sha256']}
(E/'profile-correspondence.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k in ('all_match','source_uncompressed','remerge')},indent=2))
