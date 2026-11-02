from pathlib import Path
import shutil,hashlib,json,subprocess,time,os
W=Path('/home/linhao/Toolchain/development/llvm-optimize');D=W/'temp/review-20261102/size-baseline';H=W/'temp/debuglink-20261028/full-20261030';r=H/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';b=r/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build'
source=H/'products/binaries/ordinary-clang-22';out=D/'ordinary-clang-22.stripped';assert not out.exists()
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
identity=json.loads((H/'products/work/identity.json').read_text());tool=b/'bin/llvm-strip';toolsha=sha(tool);assert toolsha==identity['strip_tool_sha256']
original_stat=source.stat();shutil.copy2(source,out);before=sha(out);assert before=='d5090159915657b235b96f1202c058e1efd1647d6a2225ac8fdb2906aeaa501d'
loader=r/'lib64/ld-linux-x86-64.so.2';libs=str(b/'lib64')+':'+str(r/'usr/lib64')+':'+str(r/'lib64')
argv=[str(loader),'--library-path',libs,str(tool),'--strip-all',str(out)]
(D/'argv.json').write_text(json.dumps(argv,indent=2)+'\n')
start=time.time()
with (D/'strip.stdout').open('wb') as o,(D/'strip.stderr').open('wb') as er:p=subprocess.run(argv,cwd=D,stdout=o,stderr=er)
result={'source_path':str(source),'source_sha256':before,'source_bytes':original_stat.st_size,'tool_path':str(tool),'tool_realpath':str(tool.resolve()),'tool_sha256':toolsha,'helper_argv':[str(tool),'--strip-all',str(out)],'actual_argv':argv,'elapsed_seconds':time.time()-start,'rc':p.returncode}
if p.returncode==0:
 size=out.stat().st_size;n=152532400-size;percent=n/size*100
 result.update(output_path=str(out),output_bytes=size,output_sha256=sha(out),candidate_bytes=152532400,N=n,P_raw=percent,P_one_decimal=f'{percent:.1f}')
assert source.stat().st_size==original_stat.st_size and source.stat().st_mtime_ns==original_stat.st_mtime_ns
result['source_size_mtime_unchanged']=True
(D/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(p.returncode)
