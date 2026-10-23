"""Correct probe selection; no product/source changes, retain first attempts."""
import collections,json,re,shutil,subprocess,time
from validate import W,D,E,R,V,INNER,run,root,save
import check_hybrid_link_needed as needed
# Complete targets not executed because initial optional Ninja stopped at four failures.
failed={'lib64/libomp_testing.so','projects/openmp/runtime/unittests/String/StringTests','bin/clang-fuzzer','bin/clang-objc-fuzzer'}
original=json.loads((E/'optional-build-result.json').read_text());targets=[t for t in original['targets'] if t not in failed];assert len(targets)==18
env=json.loads((E/'rpm-environment-allowlist.json').read_text())['env'];prefix=['sudo','-n','/usr/sbin/chroot','--userspec=1000:1000',str(R),'/usr/bin/env','-i',*[k+'='+v for k,v in sorted(env.items())],'/usr/bin/ninja','-C','/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build']
from validate import sha,BUILD
before={n:sha(BUILD/n) for n in ['CMakeCache.txt','build.ninja','CMakeFiles/rules.ninja']}
dry=run('optional-remaining-dry-run',prefix+['-n',*targets],300)
result={'targets':targets,'excluded_previously_failed':sorted(failed),'compiler_now_installed_hybrid':sha(R/'usr/bin/clang-22'),'config_before':before,'dry_run_rc':dry['rc'],'scope':'Supplemental nondefault/noninstalled targets only; primary root peak already sealed'}
if dry['rc']==0 and not re.search(r're-running cmake|regenerating|cmake --regenerate-during-build',dry['stdout']+dry['stderr'],re.I):
 argv=prefix+['-j6',*targets];start=time.time_ns()
 with (E/'optional-remaining-build.log').open('wb') as out:rc=subprocess.run(argv,stdout=out,stderr=subprocess.STDOUT).returncode
 result.update(argv=argv,rc=rc,start_ns=start,end_ns=time.time_ns(),status='PASS' if rc==0 else 'FAIL')
else:result.update(status='NOT_RUN',reason='dry-run failed or would reconfigure')
result['config_after']={n:sha(BUILD/n) for n in before};result['config_unchanged']=before==result['config_after'];save('optional-remaining-result.json',result)
rows=[]
for t in json.loads((W/'docs/52_hybrid_link_evidence/needed-expectations-v2.json').read_text())['targets']:
 p=BUILD/t['build_output'];r=run('linkage-supplemental/raw-'+str(len(rows)),['readelf','-dW',str(p)])
 libs=re.findall(r'\(NEEDED\).*?\[([^]]+)\]',r['stdout']);state=needed.needed_status(t['expected_needed'],libs)
 rows.append({**t,'exists':p.exists(),'needed':libs,'status':state['status'] if r['rc']==0 else 'INSPECTION_ERROR','needed_comparison':state,'rc':r['rc']})
save('linkage-188-supplemental.json',{'total':188,'counts':dict(collections.Counter(r['status'] for r in rows)),'rows':rows})

# Separate debug-only files accidentally included by broad /sdk_tools/ regex.
table=json.loads((W/'docs/52_hybrid_link_evidence/needed-expectations-v2.json').read_text())
paths=(E/'rpm-paths.txt').read_text().splitlines()
paths=[p for p in paths if not p.startswith('/usr/lib/debug/') and (p.startswith('/usr/bin/') or re.match(r'/usr/lib64/.*\.so',p) or re.search(r'/sdk_tools/lldb/(bin|lib64)/',p))]
j=needed.inspect_paths(table,R,paths,require_declared=True);save('installed-needed-corrected.json',j)
save('probe-corrections.json',{'installed_needed':'Exclude four /usr/lib/debug/.../sdk_tools/*.debug files from executable/DSO selection; initial evidence retained','runtime':'Eight tools need equivalent subcommand or MS-style help; use actual upstream options/tests, do not change product files'})
p=V/'equivalent';p.mkdir(exist_ok=True);inner=INNER+'/equivalent'
(p/'basic_inputs.json').write_text('{"headers":[],"version":"3"}\n');(p/'example.def').write_text('LIBRARY example.dll\nEXPORTS\nanswer\n')
probes={
 '/usr/bin/clang-installapi':['-x','objective-c','-target','arm64-apple-ios13.0.0','-fapplication-extension','-current_version','1','-compatibility_version','1','-install_name','/usr/lib/basic.dylib','-dynamiclib',inner+'/basic_inputs.json','-o',inner+'/basic.tbd'],
 '/usr/bin/diagtool':['list-warnings'],
 '/usr/bin/hmaptool':['dump','--help'],
 '/usr/bin/llvm-c-test':['--targets-list'],
 '/usr/bin/llvm-cvtres':['/HELP'],
 '/usr/bin/llvm-dlltool':['-m','i386:x86-64','-d',inner+'/example.def','-l',inner+'/example.lib'],
 '/usr/bin/llvm-mt':['/?'],
 '/usr/bin/llvm-rc':['/?']}
runtime=json.loads((E/'runtime-result.json').read_text());rows=runtime['rows']
for row in rows:
 if row['path'] not in probes:continue
 q=root('runtime-equivalent/'+row['path'].split('/')[-1],[row['path'],*probes[row['path']]],60);row['equivalent_probe']=q
 row['status']='PASS' if q['rc']==0 and not row.get('missing_libraries') and row.get('ldd_rc',0)==0 else 'REVIEW_REQUIRED'
save('runtime-final.json',{'counts':dict(collections.Counter(r['status'] for r in rows)),'rows':rows,'missing_shared_library_paths':[r['path'] for r in rows if r.get('missing_libraries')]})
# Runtime dependency inventory, no dependency installation or script editing.
root('runtime-environment',['/bin/sh','-c','command -v python; command -v python3; command -v git; rpm -q python python3 git; python3 -c "import sys; print(sys.version); print(sys.path)"'],60)
root('rpm-installed-verify',['rpm','-V','llvm','clang','lldb','llvm-devel','clang-devel','llvm-static-devel','libllvm'],120)
# Supplemental target attempt footprint is excluded from full-build peak.
for name,path in [('root','/'),('cache','/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache')]:root('post-validation-size-'+name,['/bin/du','-sx','-B1',path],600)
print('FOLLOWUP_DONE',j['status'],json.loads((E/'runtime-final.json').read_text())['counts'],flush=True)
