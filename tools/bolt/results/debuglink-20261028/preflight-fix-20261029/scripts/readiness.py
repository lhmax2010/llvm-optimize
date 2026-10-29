from pathlib import Path
import hashlib,json,subprocess,shutil,configparser,difflib,os
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=W/'temp/debuglink-20261028';F=D/'preflight-fix-20261029';E=B/'tools/bolt/results/debuglink-20261028/preflight-fix-20261029';R=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';SOURCES=R/'home/abuild/rpmbuild/SOURCES';plan=json.loads((F/'plan.json').read_text())
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def save(n,o):(E/n).write_text(json.dumps(o,indent=2)+'\n')
assert json.loads((E/'export-result.json').read_text())['rc']==0
assert all(x['PASS'] for x in json.loads((E/'five-parse/matrix.json').read_text()))
assert (E/'five-parse/off-comparison.json').exists() and (E/'five-parse/mode-check.json').exists()
config=configparser.ConfigParser();config.read(plan['config']);p=config[config['general']['profile']];assert p['repos']=='repo.base_0,repo.base_debug_0';assert sha(Path(p['buildconf']))=='e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945'
assert all('tizen-base-toolchain_20261013.024319' in config[k]['url'] for k in ('repo.base_0','repo.base_debug_0'))
a={p.name:p for p in (D/'export').iterdir() if p.is_file()};b={p.name:p for p in (F/'export').iterdir() if p.is_file()};assert a.keys()==b.keys()
rows=[]
for name in sorted(a):
 row={'file':name,'previous_sha256':sha(a[name]),'new_sha256':sha(b[name]),'root_SOURCE_sha256':sha(SOURCES/name)}
 row['unchanged']=row['previous_sha256']==row['new_sha256'];row['prepared_source_matches']=row['root_SOURCE_sha256']==row['previous_sha256'];assert row['prepared_source_matches']
 if name=='libcxx-runtimes.spec':
  assert a[name].read_text().replace('69807d06b89f5d14140854e99485182bdef9546b',plan['commit'])==b[name].read_text()
  row['difference']='GBS VCS line only; not a Source/Patch of llvm.spec'
 elif name!='llvm.spec':assert row['unchanged'],row
 rows.append(row)
save('export-input-comparison.json',rows)
(E/'export-spec.diff').write_text(''.join(difflib.unified_diff(a['llvm.spec'].read_text().splitlines(True),b['llvm.spec'].read_text().splitlines(True),fromfile='previous-export/llvm.spec',tofile='new-export/llvm.spec')))
# The prep body itself is identical. No rerun may delete/recreate its existing tree.
def prep(text):return text.split('\n%prep\n',1)[1].split('\n%build\n',1)[0]
assert prep(a['llvm.spec'].read_text())==prep(b['llvm.spec'].read_text())
(E/'unchanged-prep.txt').write_text(prep(b['llvm.spec'].read_text()))
# Fresh SPECS entry, retain SOURCES/llvm.spec as the previous preparation evidence.
ready=R/'home/abuild/rpmbuild/SPECS/llvm.spec';
if not ready.exists():shutil.copy2(b['llvm.spec'],ready)
assert sha(ready)==sha(b['llvm.spec'])
# Read-only expansion checks with the actual prepared RPM macros and original three job macros.
prefix=['sudo','-n','/usr/sbin/chroot','--userspec=1000:1000',str(R),'/usr/bin/env','-i','HOME=/home/abuild','USER=abuild','LOGNAME=abuild','SHELL=/bin/sh','PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin','LC_ALL=C','LANG=C']
args=['--define','jobs 8','--define','_smp_mflags -j8','--define','_costomized_smp_mflags -j20','--define','_srcdefattr (-,root,root)','--target=x86_64-tizen-linux','--define','_build_create_debug 1']
for label,argv in [('dependencies',['/usr/bin/rpmbuild','-bc','--short-circuit','--nobuild',*args,'/home/abuild/rpmbuild/SPECS/llvm.spec']),('expanded',['/usr/bin/rpmspec','-P',*args,'/home/abuild/rpmbuild/SPECS/llvm.spec']),('elfutils',['/usr/bin/rpm','-qf','/usr/bin/eu-strip'])]:
 run=subprocess.run(prefix+argv,capture_output=True);(E/('ready-'+label+'.stdout')).write_bytes(run.stdout);(E/('ready-'+label+'.stderr')).write_bytes(run.stderr);save('ready-'+label+'.json',{'argv':prefix+argv,'rc':run.returncode});assert run.returncode==0,(label,run.stderr)
text=(E/'ready-expanded.stdout').read_text();assert '--debug-symbols' in text and 'RELCFLAGS=$(echo $CFLAGS' not in text
# rpmspec -P does not create automatic debuginfo subpackage headers here.
# Prove debug mode via explicit pipeline flag and absence of release -g removal above.
build=R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8';assert (build/'llvm/CMakeLists.txt').is_file();assert (build/'mlgo_verify_assets').is_dir();assert not (build/'build/CMakeCache.txt').exists()
assert json.loads((E.parent/'prep-result.json').read_text())['rc']==0
# Do not alter the old controller/plan which references the old export. Record a separate ready plan.
resume={'source_commit':plan['commit'],'tree':plan['tree'],'root':str(R),'spec':str(ready),'spec_sha256':sha(ready),'export':str(F/'export'),'prep_required':False,'prep_reason':'all Source/Patch files identical (other unused spec only changes GBS VCS line), old SOURCES identical, prep body identical; dependencies satisfy new spec','ready_for_build':True,'build_started':False,'build_argv_not_executed':prefix+['/usr/bin/rpmbuild','-bc','--short-circuit',*args,'/home/abuild/rpmbuild/SPECS/llvm.spec'],'warning':'This is the build-only command, not a full packaging command; run later only under authorized resource/proc supervision, followed by install/package stages. Original D/run.py points to old commit/export; do not run it unchanged.'}
save('readiness.json',resume);(F/'ready-plan.json').write_text(json.dumps(resume,indent=2)+'\n');print('READY: unchanged prep inputs; dependency --nobuild check PASS; no build started')
