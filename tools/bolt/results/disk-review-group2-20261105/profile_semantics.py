from pathlib import Path
import json,lzma,collections,subprocess,hashlib,time
E=Path(__file__).resolve().parent;d=json.loads((E/'profile-correspondence.json').read_text())
with lzma.open(d['source'],'rb') as f:c=collections.Counter(f)
expected_count=sum(c.values());h=hashlib.sha256();count=0;bad=[];start=time.monotonic()
with (E/'profile-semantic-remerge.stderr').open('wb') as err:
 p=subprocess.Popen(d['remerge_argv'],stdout=subprocess.PIPE,stderr=err)
 for line in p.stdout:
  h.update(line);count+=1
  if c[line]>0:
   c[line]-=1
   if c[line]==0:del c[line]
  elif len(bad)<20:bad.append(line.decode(errors='replace'))
 rc=p.wait()
r={'rc':rc,'seconds':time.monotonic()-start,'expected_lines':expected_count,'actual_lines':count,'sha256':h.hexdigest(),'missing_line_count':sum(c.values()),'extra_sample':bad,'same_lines_and_counts':rc==0 and not c and not bad and count==expected_count,'explanation':'merge-fdata legacy output iterates thread-id DenseMap then StringMap without sorting; physical line order is not canonical; all complete lines including counts compared as multiset.'}
(E/'profile-semantic-comparison.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
src=Path(d['remerge_argv'][9]).parents[2]/'bolt/tools/merge-fdata/merge-fdata.cpp'
# Preserve source excerpt from the verified tool source location.
src=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/bolt/tools/merge-fdata/merge-fdata.cpp')
lines=src.read_text().splitlines();(E/'merge-fdata-ordering.txt').write_text(str(src)+'\n'+'\n'.join(f'{i+1}: {lines[i]}' for i in range(340,376))+'\n')
