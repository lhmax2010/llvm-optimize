from common import *
assert subprocess.check_output(['git','-C',str(D/'source'),'rev-parse','HEAD'],text=True).strip()=='ac112ebfd6e7983bdfd4c38dd156e6baba72731b'
assert not subprocess.check_output(['git','-C',str(D/'source'),'status','--porcelain'],text=True)
free();X.mkdir();rows=[]
for l in (P/'SHA256SUMS').read_text().splitlines():
 expected,rel=l.split('  ',1);f=P/rel;actual=sha(f);rows.append({'file':str(f),'expected':expected,'sha256':actual,'PASS':actual==expected});assert actual==expected,f
save(E/'new-products-sha.json',rows)
oldrows=[]
for item in json.loads((BASE.parent/'bolt-on-hybrid-20261024/preserved-products.json').read_text()):
 f=Path(item['retained']);actual=sha(f);oldrows.append({'file':str(f),'expected':item['sha256'],'sha256':actual,'PASS':actual==item['sha256']});assert actual==item['sha256'],f
save(E/'old-products-sha.json',oldrows)
checks={};identity=json.loads((WORK/'identity.json').read_text())
for name,expected in [('clang.candidate',identity['after_sha256']),('ordinary-clang-22',sha(P/'binaries/ordinary-clang-22')),('reference-relocs-clang-22',json.loads((WORK/'pipeline-result.json').read_text())['input_sha256'])]:
 f=WORK/name;assert f.is_file(),f;actual=sha(f);assert actual==expected;checks[str(f)]=actual
for f in [BUILD/'bin/llvm-bolt',BUILD/'bin/llvm-strip',WORK/'profile.fdata',D/'source/packaging/llvm.spec',D/'source/packaging/clang-bolt-helper.py',BASE/'native-archive-evidence.tar.gz']:checks[str(f)]=sha(f)
save(E/'input-identities.json',checks)
save(E/'preflight.json',{'PASS':True,'new_sums':len(rows),'old_manifest':len(oldrows),'old_SHA256SUMS_exists':(OLD/'SHA256SUMS').exists(),'free':shutil.disk_usage('/home').free})
print('PREFLIGHT_PASS',len(rows),len(oldrows),flush=True)
