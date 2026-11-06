"""Release-only checks. Real release inputs do not exist until D finishes."""
from pathlib import Path
import importlib.util,json,subprocess,re,os,shlex,hashlib,ctypes
from unittest.mock import patch
from checks import *
from rpm_io import manifest
from rpm_extract import extract_selected

def library_links(man,payload):
 # Resolve package absolute links inside this scratch payload, never against
 # the host filesystem. Keep soname aliases needed by RTLD_NOW.
 rows=[]
 for files in man.values():
  for name,v in files.items():
   if not stat.S_ISLNK(v['mode']) or Path(name).parent.as_posix() not in ('usr/lib64','lib64','usr/lib','lib'):continue
   p=payload/name;target=v['target'];p.parent.mkdir(parents=True,exist_ok=True)
   if target.startswith('/'):target=os.path.relpath(payload/target.lstrip('/'),p.parent)
   assert (p.parent/target).resolve().is_relative_to(payload.resolve()),('library symlink escapes payload',name,target)
   if p.is_symlink():assert os.readlink(p)==target
   else:assert not p.exists();p.symlink_to(target)
   rows.append(dict(path=name,rpm_target=v['target'],scratch_target=target))
 return rows

def extract_package_payload(rpm,chosen,payload,files):
 # Multiple RPMs can legitimately own identical headers. Never overwrite a
 # previous payload: reuse only a regular file with the exact expected SHA.
 existing=[];missing=set()
 for name in chosen:
  p=payload/name
  if p.exists() or p.is_symlink():
   assert p.is_file() and not p.is_symlink(),('payload overlap is not regular',name)
   actual=sha(p);assert actual==files[name]['sha256'],('conflicting RPM payload',name,actual,files[name]['sha256'])
   existing.append(dict(path=name,sha256=actual,rpm=str(rpm)))
  else:missing.add(name)
 if missing:extract_selected(rpm,missing,payload)
 return existing

def check_native_archive(data,record):
 ms=[m for m in members(data) if m['name'] not in ('/','//','/SYM64/')];assert len(ms)==record['members']
 results={r['ordinal']:r for r in record['results']};converted=preserved=0
 for i,m in enumerate(ms):
  r=results[i];assert r['name']==m['name']
  if r['preserved']:preserved+=1;continue
  ss=sections(m['body']);bad=[n for n in ss if n.startswith(('.debug','.zdebug'))];assert not bad,(m['name'],'release conversion unexpectedly emitted debug sections',bad);converted+=1
  assert hashlib.sha256(m['body']).hexdigest()==r['sha256']
 return dict(converted=converted,preserved=preserved)

def ninja_modules(BUILD):
 # Read Ninja's emitted graph only; never invoke ninja in an existing tree.
 def logical(p):return p.read_text().replace('$\n','').splitlines()
 rules={};name=None
 for line in logical(BUILD/'CMakeFiles/rules.ninja'):
  if line.startswith('rule '):name=line[5:];rules[name]={}
  elif name and line.startswith('  ') and ' = ' in line:
   k,v=line.strip().split(' = ',1);rules[name][k]=v
 edges=[];current=None
 for line in logical(BUILD/'build.ninja'):
  if line.startswith('build '):
   current=None
   left,right=line[6:].split(': ',1);xs=right.split();rule=xs[0]
   if '_MODULE_LIBRARY_LINKER_' not in rule:continue
   inputs=xs[1:];inputs=inputs[:inputs.index('|')] if '|' in inputs else inputs;inputs=inputs[:inputs.index('||')] if '||' in inputs else inputs
   current=dict(output=left.split()[0],rule=rule,variables={'in':' '.join(inputs),'out':left.split()[0]});edges.append(current)
  elif current and line.startswith('  ') and ' = ' in line:
   k,v=line.strip().split(' = ',1);current['variables'][k]=v
 for e in edges:
  env=e['variables'];command=rules[e['rule']]['command'];e['rule_command']=command
  # One Ninja expansion, not repeated shell-variable expansion. In particular
  # escaped $$ORIGIN in a variable value must survive as the shell's $ORIGIN.
  def unescape(value):return value.replace('$$','$').replace('$ ', ' ').replace('$:', ':')
  e['command']=re.sub(r'\$\$|\$\{(\w+)\}|\$(\w+)|\$([ :])',lambda m:'$' if m[0]=='$$' else m[3] if m[3] else unescape(env.get(m[1] or m[2],'')),command)
 return edges

def real_c2(D,O,summary,fixture_bc=None):
 from validate import rootpaths,run,loader,SOURCE
 R,BUILD,WORK=rootpaths(D);spec=importlib.util.spec_from_file_location('night_converter',SOURCE/'packaging/llvm-static-archives-native.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
 X=O/'real-release-c2';X.mkdir();wr=X/'tools';wr.mkdir();tools={}
 for name in ['clang-22','llvm-dis','llvm-as','llvm-nm']:
  original=R/'usr/bin'/name;assert original.is_file();q=wr/name;q.write_text('#!/bin/sh\nexec '+shlex.join([str(x) for x in loader(R,original)])+' "$@"\n');q.chmod(0o755);tools[name]=str(q)
 if fixture_bc is None:
  record=next(r for r in summary['archives'] if r['converted']>0);build_archive=BUILD/'lib64'/Path(record['path']).name;assert build_archive.is_file()
  orig=a.inspect(build_archive);selected=next(m for m in orig['members'] if m['kind']=='bitcode')
  with build_archive.open('rb') as f:f.seek(selected['offset']);data=f.read(selected['size'])
 else:
  build_archive=Path(fixture_bc);data=build_archive.read_bytes();selected={'name':build_archive.name,'sha256':hashlib.sha256(data).hexdigest(),'synthetic_fixture':True}
 assert hashlib.sha256(data).hexdigest()==selected['sha256'];bc=X/'real-release.bc';bc.write_bytes(data)
 ll=run([tools['llvm-dis'],bc,'-o','-'],X/'disassemble');settings=a.ir_settings(ll.splitlines(True),debug_info='no');assert not settings['policy']['dwarf']
 # Inject a compile unit into a COPY of this real release module; keep its
 # real recorded release command. This is the C-2 #6 malformed-input probe.
 ids=[int(x) for x in re.findall(r'^!(\d+) =',ll,re.M)];start=max(ids,default=0)+1
 cu,fi,dv,di=range(start,start+4)
 assert '!llvm.dbg.cu' not in ll
 bad=ll+'\n!llvm.dbg.cu = !{!'+str(cu)+'}\n'
 flags=re.search(r'^!llvm.module.flags = !\{([^\n]*)\}',bad,re.M)
 extra='!'+str(dv)+', !'+str(di)
 if flags:bad=bad[:flags.start()]+flags.group(0)[:-1]+', '+extra+'}'+bad[flags.end():]
 else:bad+='!llvm.module.flags = !{'+extra+'}\n'
 bad+=f'!{cu} = distinct !DICompileUnit(language: DW_LANG_C_plus_plus, file: !{fi}, producer: "night negative fixture", isOptimized: true, runtimeVersion: 0, emissionKind: FullDebug)\n!{fi} = !DIFile(filename: "negative.cpp", directory: "/")\n!{dv} = !{{i32 2, !"Dwarf Version", i32 4}}\n!{di} = !{{i32 2, !"Debug Info Version", i32 3}}\n'
 # A CU alone is optimized away by the backend. Attach a real subprogram
 # and return-instruction location to force debug emission in the malformed copy.
 sp,ty,empty,loc=range(start+4,start+8)
 definition=next((m for m in re.finditer(r'^define .*\{\s*$',bad,re.M) if re.search(r'^  ret .*$',bad[m.end():bad.index('\n}',m.end())],re.M)),None);assert definition,'no returning function in real release member'
 line=definition.group(0);bad=bad[:definition.start()]+line.rstrip()[:-1]+'!dbg !'+str(sp)+' {'+bad[definition.end():]
 end=bad.index('\n}',definition.start());part=bad[definition.start():end]
 ret=re.search(r'^  ret .*$',part,re.M);assert ret,'selected real function has no return for negative fixture'
 at=definition.start()+ret.end();bad=bad[:at]+', !dbg !'+str(loc)+bad[at:]
 bad+=f'!{sp} = distinct !DISubprogram(name: "negative_probe", scope: !{fi}, file: !{fi}, line: 1, type: !{ty}, scopeLine: 1, spFlags: DISPFlagDefinition, unit: !{cu}, retainedNodes: !{empty})\n!{ty} = !DISubroutineType(types: !{empty})\n!{empty} = !{{}}\n!{loc} = !DILocation(line: 1, column: 1, scope: !{sp})\n'
 (X/'negative.ll').write_text(bad);run([tools['llvm-as'],X/'negative.ll','-o',X/'negative.bc'],X/'assemble-negative')
 results=[];retained=[]
 def retain(p,*args,**kwargs):
  assert p.resolve().is_relative_to(X.resolve());retained.append(str(p))
 for label,source in [('positive',bc),('negative',X/'negative.bc')]:
  root=X/(label+'-root');root.mkdir();build=X/(label+'-build');build.mkdir();(build/'CMakeCache.txt').write_text('# fixture, no CMake execution\n');run(['/usr/bin/ar','qcDS',root/'fixture.a',source],X/(label+'-archive'))
  try:
   # Preserve newly generated test evidence, overriding deletion only.
   with patch.object(Path,'unlink',retain):answer=a.convert(root,build/'evidence',tools['clang-22'],tools['llvm-dis'],tools['llvm-nm'],build,jobs=1,debug_info='no')
  except ValueError as e:
   assert label=='negative' and str(e)=='release conversion unexpectedly emitted debug sections',str(e);results.append(dict(case=label,PASS=True,error=str(e)))
  else:
   assert label=='positive' and answer['status']=='CONVERTED';inspected=a.inspect(build/'evidence/archives/fixture.a');assert all(not m['debug_sections'] for m in inspected['members']);results.append(dict(case=label,PASS=True,output=inspected))
 save(X/'result.json',dict(real_input_archive=str(build_archive),member=selected,recorded_command=settings['recorded_command'],converter=str(SOURCE/'packaging/llvm-static-archives-native.py'),converter_sha256=sha(SOURCE/'packaging/llvm-static-archives-native.py'),results=results,synthetic_fixture=fixture_bc is not None,retained_cleanup_files=retained))

def release_checks(D,O,peer,log,identity):
 from validate import packages,rootpaths,run,loader
 R,BUILD,WORK=rootpaths(D);pk=packages(D);man={k:manifest(p) for k,p in pk.items()};save(O/'rpm-manifests.json',man)
 debuginfo={k:v for k,v in man.items() if 'debuginfo' in k or 'debugsource' in k};save(O/'actual-debuginfo-packages.json',debuginfo)
 assert 'debug_file' not in identity and 'debuglink' not in identity,'release identity has debug symbols'
 assert '.gnu_debuglink' not in sections((WORK/'clang.candidate').read_bytes())
 post=WORK/'post-gate/post-result.json';assert post.is_file();save(O/'helper-post-gate.json',json.loads(post.read_text()))
 save(O/'platform-post-excerpts.json',[dict(line=i,text=t) for i,t in log.items() if 'find-debuginfo' in t or ('clang-22' in t and ('extract' in t.lower() or 'strip' in t.lower()))]);assert any('find-debuginfo' in t for t in log.values()),'platform post evidence absent'
 # Extract only fresh copies of payload regular files to scan recorded options,
 # and use those exact module bytes for dlopen. Hardlink aliases are not executables here.
 payload=O/'payload';filemap={};scanned=0;overlaps=[]
 for key,files in man.items():
  if key.endswith('\tsrc'):continue
  chosen={n for n,v in files.items() if stat.S_ISREG(v['mode']) and v['bytes']>0}
  if chosen:overlaps.extend(extract_package_payload(pk[key],chosen,payload,files));save(O/'extraction-overlaps.json',overlaps)
  for name in chosen:
   p=payload/name;assert sha(p)==files[name]['sha256'],('RPM hardlink payload extraction mismatch',name);filemap[name]=p
   with p.open('rb') as f:magic=f.read(8)
   if magic.startswith(b'\x7fELF') or magic==b'!<arch>\n':scanned+=no_dropped(p.read_bytes())
 save(O/'library-links.json',library_links(man,payload))
 save(O/'no-dropped-records.json',dict(PASS=True,command_record_sections_checked=scanned));assert scanned>0,'no command records checked'
 summary=json.loads((BUILD/'native-archive-conversion/summary.json').read_text());assert summary['status']=='PASS' and len(summary['archives'])==225
 checks=[]
 for record in summary['archives']:
  p=payload/record['path'];assert p.is_file();checks.append(dict(path=record['path'],**check_native_archive(p.read_bytes(),record)))
 save(O/'native-release.json',dict(converted_members=sum(x['converted'] for x in checks),preserved_native_members=summary['native_members_preserved'],native_archives_skipped=summary['native_archives_skipped'],archives=checks))
 real_c2(D,O,summary)
 module_rows=[];cache=(BUILD/'CMakeCache.txt').read_text();match=re.search(r'^CMAKE_MODULE_LINKER_FLAGS:STRING=(.*)$',cache,re.M);assert match;expected=shlex.split(match[1])
 for edge in ninja_modules(BUILD):
  paths=[p for name,p in filemap.items() if Path(name).name==Path(edge['output']).name]
  if not paths:continue
  tokens=shlex.split(edge['command']);assert all(t in tokens for t in expected),(edge,expected)
  for p in paths:
   # Python from this root plus its loader, with package libraries taking precedence.
   argv=[R/'lib64/ld-linux-x86-64.so.2','--library-path',str(payload/'usr/lib64')+':'+str(R/'usr/lib64')+':'+str(R/'lib64'),R/'usr/bin/python3','-B','-c','import ctypes,os,sys; ctypes.CDLL(sys.argv[1],mode=os.RTLD_NOW|os.RTLD_GLOBAL); print("DLOPEN_PASS",sys.argv[1])',p]
   env={**os.environ,'PYTHONHOME':str(R/'usr')};run(argv,O/('dlopen-'+p.name),env=env);module_rows.append(dict(**edge,payload=str(p),expected_module_flags=expected,dlopen='PASS'))
 assert module_rows,'no packaged MODULE libraries found';save(O/'module-link-and-dlopen.json',module_rows)
 tp=packages(peer);tm={k:manifest(p) for k,p in tp.items()};differences={}
 for k in sorted(set(man)&set(tm)):
  a,b=tm[k],man[k];differences[k]=dict(only_T=sorted(set(a)-set(b)),only_D=sorted(set(b)-set(a)),different_files=[n for n in sorted(set(a)&set(b)) if a[n]!=b[n]])
 save(O/'T-D-package-file-differences.json',dict(only_T=sorted(set(tp)-set(pk)),only_D=sorted(set(pk)-set(tp)),shared_package_file_differences=differences))
