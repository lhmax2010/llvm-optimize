from pathlib import Path
import json,re,shlex,sys,subprocess
W=Path('/home/linhao/Toolchain/development/llvm-optimize');D=W/'temp/night-20261103/rehearsal';E=Path(__file__).parents[1]/'results/night-prep-20261103'
project=sys.argv[1];root=D/project;root=root/'retry-02' if len(sys.argv)>2 and sys.argv[2]=='retry-02' else root;e=root/'evidence'
r=json.loads((e/'result.json').read_text());assert r['status']=='ok',r
audit=json.loads((e/'final-audit.json').read_text());assert not audit['mounts']['stdout'] and not audit['remaining_build_processes']
logfile=e/'rpm-build-final.log' if (e/'rpm-build-final.log').exists() else e/'rpm-build.log';log=logfile.read_text();lines=log.splitlines();rows={'root':str(root),'logfile':str(logfile)}
for name in ['TIZEN_LLVM_NORMALIZED_FLAGS','TIZEN_LLVM_DROPPED_FLAGS']:
 matches=[{'line':i,'text':t,'payload':t[t.index(name):]} for i,t in enumerate(lines,1) if name+' CFLAGS=[' in t and not re.search(r'\+ printf ',t)]
 assert len(matches)==1,(name,matches);rows[name]=matches[0]
c=[(i,t) for i,t in enumerate(lines,1) if '+ cmake -G Ninja ' in t];assert len(c)==1,c
lineno,text=c[0];argv=shlex.split(text.split('+ ',1)[1]);keys=['CMAKE_C_FLAGS','CMAKE_CXX_FLAGS','CMAKE_EXE_LINKER_FLAGS','CMAKE_SHARED_LINKER_FLAGS']
cm={k:next(a.split('=',1)[1] for a in argv if a.startswith('-D'+k+'=')) for k in keys}
# LDFLAGS is exported into CMake's environment; it is not an invented -DCMAKE flag.
ld=[(i,t) for i,t in enumerate(lines,1) if re.search(r'\+ (?:export )?LDFLAGS=',t)]
if ld:
 ll,lt=ld[-1];args=shlex.split(lt.split('+ ',1)[1]);ldval=next(a.split('=',1)[1] for a in args if a.startswith('LDFLAGS='))
else:raise AssertionError('LDFLAGS assignment missing')
inputs=json.loads((W.parent/'llvm-optimize-bolt/tools/bolt/results/final-20261103/flags-inputs.json').read_text())
expected=dict(inputs['toolchain']['effective'])
if project=='basedev':
 for k in ['CFLAGS','CXXFLAGS']:expected[k]=expected[k].replace('-g2 -gdwarf-4','').replace(' -g ','  ')
assert cm['CMAKE_C_FLAGS']==expected['CFLAGS'],('CFLAGS',cm['CMAKE_C_FLAGS'],expected['CFLAGS'])
assert cm['CMAKE_CXX_FLAGS']==expected['CXXFLAGS']
assert ldval==expected['LDFLAGS'],(ldval,expected['LDFLAGS'])
previous=json.loads((W.parent/'llvm-optimize-bolt/tools/bolt/results/second-review-20261104'/(project+'-rehearsal-audit.json')).read_text())
assert rows['TIZEN_LLVM_NORMALIZED_FLAGS']['payload']==previous['TIZEN_LLVM_NORMALIZED_FLAGS']['payload']
assert cm==previous['cmake']['flags']
assert ldval==previous['LDFLAGS']['value']
assert not re.search(r'\+ ninja ',log)
expected_drop='' if project=='toolchain' else '-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4'
assert rows['TIZEN_LLVM_DROPPED_FLAGS']['payload']=='TIZEN_LLVM_DROPPED_FLAGS CFLAGS=['+expected_drop+'] CXXFLAGS=['+expected_drop+'] LDFLAGS=[]'
assert 'TIZEN_LLVM_FIXED_FLAGS_FAILED' not in log
rows.update(project=project,result=r,cmake={'line':lineno,'text':text,'argv':argv,'flags':cm},LDFLAGS={'line':ll,'text':lt,'value':ldval},PASS=True)
assert not re.search(r'(?:^|\] )TIZEN_LLVM_FLAGS_WARNING ',log,re.M)
(E/(project+'-rehearsal-audit.json')).write_text(json.dumps(rows,indent=2)+'\n')
print(project,'PARAMETERS_AND_CLEANUP_PASS');print(rows['TIZEN_LLVM_NORMALIZED_FLAGS']['text']);print(rows['TIZEN_LLVM_DROPPED_FLAGS']['text']);print(cm);print('LDFLAGS=',ldval)
