from common import *
import sys,re,shutil
r=root(Path(sys.argv[1]));p=r/'home/abuild/pgo-parse';p.mkdir();shutil.copytree(P/'export-PGO',p/'SOURCES')
spec=(P/'export-PGO/llvm.spec').read_text();(p/'llvm.spec').write_text(spec);(p/'rollback.spec').write_text(spec.replace('%bcond_without clang_bolt','%bcond_with clang_bolt',1))
out=E/'five-parse';out.mkdir();call(prefix(r)+['/usr/bin/rpm','-q','--qf','%{NAME} %{VERSION}-%{RELEASE}\n','rpm','rpm-build'],out/'version.stdout')
assert all('4.14.1.1-' in l for l in (out/'version.stdout').read_text().splitlines())
rows=[]
for name,arch,off,rollback in [('x86-on','x86_64',False,False),('x86-off','x86_64',True,False),('x86-rollback','x86_64',False,True),('armv7l','armv7l',False,False),('aarch64','aarch64',False,False)]:
 common=['--target',arch+'-tizen-linux','--define','_toolchain clang','--define','_sourcedir /home/abuild/pgo-parse/SOURCES','--define','_builddir /home/abuild/pgo-parse/BUILD','--define','_buildrootdir /home/abuild/pgo-parse/BUILDROOT','--define','_tmppath /home/abuild/pgo-parse/tmp']
 f='/home/abuild/pgo-parse/'+('rollback.spec' if rollback else 'llvm.spec')
 call(prefix(r)+['/usr/bin/rpmbuild','-bp','--nodeps','--nobuild',*common,*(['--without','clang_bolt'] if off else []),f],out/(name+'.stdout'))
 call(prefix(r)+['/usr/bin/rpmspec','-P',*common,*(['--define','_without_clang_bolt 1'] if off else []),f],out/(name+'-expanded.stdout'))
 expanded=(out/(name+'-expanded.stdout')).read_text();patches=re.findall(r'^Patch\d+:.*$',expanded,re.M)
 assert len(patches)==8 and '-DLLVM_PROFDATA_FILE='+PROFDATA in expanded
 rows.append({'case':name,'PASS':True,'patches':patches});save(out/'matrix.json',rows)
print('Tizen RPM five parses PASS')
