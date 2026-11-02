from pathlib import Path
import shlex,gzip,json,hashlib
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.parent/'llvm-optimize';D=W/'temp/final-20261103';E=D/'evidence'
rows={}
for name,bid,start,end in [('toolchain',1215143,391,427),('basedev',1214821,380,425)]:
 p=B/f'tools/bolt/results/qb-20261102/{bid}/x86_64-llvm.log.gz';ls=gzip.decompress(p.read_bytes()).decode().splitlines()
 row={'source':str(p),'raw':{},'effective':{},'lines':{}}
 for kind in ['CFLAGS','CXXFLAGS','LDFLAGS']:
  for i in range(start-1,start+7):
   parts=shlex.split(ls[i].split('] ',1)[1].removeprefix('+ '))
   if len(parts)==1 and parts[0].startswith(kind+'='):row['raw'][kind]=parts[0].split('=',1)[1];row['lines']['raw_'+kind]=i+1
  for i in range(end-1,end+5):
   parts=shlex.split(ls[i].split('] ',1)[1].removeprefix('+ '))
   if len(parts)==1 and parts[0].startswith(kind+'='):row['effective'][kind]=parts[0].split('=',1)[1];row['lines']['effective_'+kind]=i+1
 row['effective']['LDFLAGS']=row['raw']['LDFLAGS'];rows[name]=row
# Read the old build log only; do not run anything in its root.
p=W/'temp/debuglink-20261028/full-20261030/evidence/rpm-build.log'
for i,l in enumerate(p.open(errors='replace'),1):
 if '+ cmake -G Ninja ' in l:
  argv=shlex.split(l[l.index('+ cmake ')+2:]);row={'file':str(p),'line':i,'argv':argv,'flags':{}}
  for a in argv:
   for k in ['CMAKE_C_FLAGS','CMAKE_CXX_FLAGS','CMAKE_EXE_LINKER_FLAGS','CMAKE_SHARED_LINKER_FLAGS']:
    if a.startswith('-D'+k+'='):row['flags'][k]=a.split('=',1)[1]
  (E/'local-configure.json').write_text(json.dumps(row,indent=2)+'\n');break
comparison = {k: {'local': row['flags'][cm], 'qb': rows['toolchain']['effective'][k], 'byte_equal': row['flags'][cm] == rows['toolchain']['effective'][k]} for k,cm in [('CFLAGS','CMAKE_C_FLAGS'),('CXXFLAGS','CMAKE_CXX_FLAGS')]}
(E/'configure-source-differences.json').write_text(json.dumps(comparison,indent=2)+'\n')
(E/'flags-inputs.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Saved both source argv; QB has explicit function/data-sections absent from local CMake flags. QB is the required exact output oracle.')
