from pathlib import Path
import json,hashlib,subprocess,shutil,importlib.util
D=Path(__file__).resolve().parent;W=D.parent.parent;E=W.parent/'llvm-optimize-bolt/tools/bolt/results/oldtext-final-20261027';R=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';BUILD=R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build';WORK=BUILD/'clang-bolt'
s=importlib.util.spec_from_file_location('helper',D/'source/packaging/clang-bolt-helper.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
assert json.loads((E/'build-result.json').read_text())['exit_code']==0
shutil.copyfile(E/'resumed-rpm-build.log' if (E/'resumed-rpm-build.log').exists() else D/'gbs-root/local/repos/tizen_base_toolchain_standard/x86_64/logs/success/llvm-22.1.8-1/log.txt',E/'rpm-build.log');log=(E/'rpm-build.log').read_text(errors='replace')
for marker in ['BOLT_PIPELINE_PASS','BOLT_COMPARE_ROOT_PASS','BOLT_POST_GATE_PASS','BOLT_CACHE_RELEASE removed']:
 assert marker in log,marker
assert 'BOLT_GATE_FAILED:' not in log
for line in log.splitlines():
 if 'BOLT_CACHE_RELEASE removed' in line:print(line)
identity=json.loads((WORK/'identity.json').read_text());assert h.digest(WORK/'clang.candidate')==identity['rpath_adjusted_sha256']==identity['installed_sha256']==identity['after_sha256']
props=h.security_properties(WORK/'clang.candidate');assert props['DT_RPATH'] is None and props['DT_RUNPATH']=='$ORIGIN/../lib64',props
baseline=json.loads((WORK/'installed-baseline.json').read_text());assert props['DT_RUNPATH']==baseline['DT_RUNPATH'];h.installed_security(WORK/'installed-baseline.json',WORK/'clang.candidate')
real=[json.loads((WORK/p).read_text()) for p in ['prestrip-real/real-result.json','preinstall-real/real-result.json','post-gate/real/real-result.json']]
assert all(x['real_pass'] and len(x['cases'])==8 for x in real)
counts=json.loads((WORK/'pipeline-result.json').read_text())['counts'];assert counts=={'N':23592,'M':144032,'S':0,'U':1,'Q':383,'R':4.238545331242318e-05,'S_over_N':0.0}
assert identity['strip_all_sha256']=='13a07cb7f84bd1ceda4d851c8bd71bddf7ef0c2d4864892eba64cbbb9a0350b8'
assert (WORK/'clang.candidate').stat().st_size==152532296
assert len(list((R/'home/abuild/rpmbuild/RPMS/x86_64').glob('*.rpm')))==22
assert len(list((R/'home/abuild/rpmbuild/SRPMS').glob('*.rpm')))==1
for name in ['tool-plan.json','tool-build-verification.json']:
    data=json.loads((WORK/name).read_text());assert data['tasks']==113
    if name=='tool-build-verification.json':assert data['planned_tasks']==data['executed_tasks']==113 and data['tool_build_verified'] and data['executable_produced_by_this_build']
    print(name,'PASS',data['tasks'])
version=subprocess.check_output(['readelf','-dW',str(WORK/'clang.candidate')],text=True);(E/'candidate-readelf.txt').write_text(version)
result={'PASS':True,'candidate_sha256':h.digest(WORK/'clang.candidate'),'ordinary_sha256':h.digest(WORK/'ordinary-clang-22'),'DT_RPATH':props['DT_RPATH'],'DT_RUNPATH':props['DT_RUNPATH'],'identity':identity,'counts':counts,'real_seconds':[x['seconds'] for x in real],'real_total_seconds':sum(x['seconds'] for x in real)}
(E/'qualification.json').write_text(json.dumps(result,indent=2));print('QUALIFICATION_PASS',result['candidate_sha256'],'real seconds',result['real_total_seconds'])
# Independent retained deliverables, no root is deleted.
P=D/'products';P.mkdir(exist_ok=True);rows=[]
files=[(WORK/'clang.candidate','binaries/clang.candidate'),(WORK/'ordinary-clang-22','binaries/ordinary-clang-22'),(BUILD/'bin/llvm-bolt','binaries/llvm-bolt')]
files += [(p,'RPMS/'+p.name) for p in sorted((R/'home/abuild/rpmbuild/RPMS/x86_64').glob('*.rpm'))]
files += [(p,'SRPMS/'+p.name) for p in sorted((R/'home/abuild/rpmbuild/SRPMS').glob('*.rpm'))]
files += [(WORK/n,'work/'+n) for n in ['identity.json','installed-baseline.json','install-state.json','pipeline-result.json','disk-begin.json','disk-tool-built.json','disk-pipeline.json','disk-post.json','cache-release.json']]
for src,rel in files:
 dst=P/rel;dst.parent.mkdir(parents=True,exist_ok=True);assert not dst.exists();shutil.copy2(src,dst);assert h.digest(dst)==h.digest(src);rows.append({'source':str(src),'preserved':str(dst),'sha256':h.digest(dst),'bytes':dst.stat().st_size})
(E/'preserved-products.json').write_text(json.dumps(rows,indent=2));(P/'SHA256SUMS').write_text(''.join(x['sha256']+'  '+str(Path(x['preserved']).relative_to(P))+'\n' for x in rows))
