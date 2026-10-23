from pathlib import Path
import subprocess,json,re,time
D=Path(__file__).resolve().parent;R=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261022-cache-release/baseline-root/local/BUILD-ROOTS/scratch.x86_64.0');E=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/bolt-on-hybrid-20261024/five-parse');E.mkdir(exist_ok=True)
P=R/'home/abuild/bolt-on-hybrid-parse-20261024';P.mkdir(exist_ok=True)
spec=(D/'export/llvm.spec').read_text();(P/'llvm.spec').write_text(spec);(P/'rollback.spec').write_text(spec.replace('%bcond_without clang_bolt','%bcond_with clang_bolt',1))
prefix=['sudo','-n','/usr/sbin/chroot','--userspec=1000:1000',str(R),'/usr/bin/env','-i','HOME=/home/abuild','USER=abuild','LOGNAME=abuild','SHELL=/bin/sh','PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin','LC_ALL=C','LANG=C']
def run(name,args):
    start=time.monotonic();p=subprocess.run(prefix+args,capture_output=True,text=True)
    (E/(name+'.stdout')).write_text(p.stdout);(E/(name+'.stderr')).write_text(p.stderr)
    row={'argv':prefix+args,'rc':p.returncode,'seconds':time.monotonic()-start};(E/(name+'.json')).write_text(json.dumps(row,indent=2));return row,p.stdout
v,out=run('version',['/usr/bin/rpm','-q','--qf','%{NAME} %{VERSION}-%{RELEASE}\n','rpm','rpm-build']);assert v['rc']==0 and all(x.split()[1].startswith('4.14.1.1-') for x in out.splitlines())
rows=[]
for name,target,off,rollback in [('x86-on','x86_64-tizen-linux',False,False),('x86-off','x86_64-tizen-linux',True,False),('x86-rollback','x86_64-tizen-linux',False,True),('armv7l','armv7l-tizen-linux',False,False),('aarch64','aarch64-tizen-linux',False,False)]:
    path='/home/abuild/bolt-on-hybrid-parse-20261024/'+('rollback.spec' if rollback else 'llvm.spec')
    common=['--target',target,'--define','_sourcedir /home/abuild/bolt-on-hybrid-parse-20261024/SOURCES','--define','_builddir /home/abuild/bolt-on-hybrid-parse-20261024/BUILD','--define','_buildrootdir /home/abuild/bolt-on-hybrid-parse-20261024/BUILDROOT','--define','_tmppath /home/abuild/bolt-on-hybrid-parse-20261024/tmp','--define','_toolchain clang']
    row,_=run(name,['/usr/bin/rpmbuild','-bp','--nodeps','--nobuild']+common+(['--without','clang_bolt'] if off else [])+[path])
    expanded,text=run(name+'-expanded',['/usr/bin/rpmspec','-P']+common+(['--define','_without_clang_bolt 1'] if off else [])+[path])
    row.update(case=name,expanded=expanded,sources_patches=[x for x in text.splitlines() if re.match(r'^(Source|Patch)\d*:',x)])
    row['PASS']=row['rc']==0 and expanded['rc']==0 and sum(x.startswith('Patch') for x in row['sources_patches'])==8
    rows.append(row);(E/'matrix.json').write_text(json.dumps(rows,indent=2))
    assert row['PASS'],row
print('five Tizen RPM parses PASS')
