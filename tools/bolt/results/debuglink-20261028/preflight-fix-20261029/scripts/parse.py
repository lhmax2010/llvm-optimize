from pathlib import Path
import subprocess,json,re,time,shutil
D=Path(__file__).resolve().parent;R=D.parent/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';E=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/debuglink-20261028/preflight-fix-20261029/five-parse');E.mkdir(exist_ok=True)
P=R/'home/abuild/debuglink-parse-fix-20261029';P.mkdir(exist_ok=True)
assert json.loads((E.parent.parent/'prep-result.json').read_text())['rc']==0
shutil.copytree(D/'export',P/'SOURCES')
spec=(D/'export/llvm.spec').read_text();(P/'llvm.spec').write_text(spec);(P/'rollback.spec').write_text(spec.replace('%bcond_without clang_bolt','%bcond_with clang_bolt',1))
prefix=['sudo','-n','/usr/sbin/chroot','--userspec=1000:1000',str(R),'/usr/bin/env','-i','HOME=/home/abuild','USER=abuild','LOGNAME=abuild','SHELL=/bin/sh','PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin','LC_ALL=C','LANG=C']
def run(name,args):
    start=time.monotonic();p=subprocess.run(prefix+args,capture_output=True,text=True)
    (E/(name+'.stdout')).write_text(p.stdout);(E/(name+'.stderr')).write_text(p.stderr)
    row={'argv':prefix+args,'rc':p.returncode,'seconds':time.monotonic()-start};(E/(name+'.json')).write_text(json.dumps(row,indent=2));return row,p.stdout
v,out=run('version',['/usr/bin/rpm','-q','--qf','%{NAME} %{VERSION}-%{RELEASE}\n','rpm','rpm-build']);assert v['rc']==0 and all(x.split()[1].startswith('4.14.1.1-') for x in out.splitlines())
rows=[]
for name,target,off,rollback in [('x86-on','x86_64-tizen-linux',False,False),('x86-off','x86_64-tizen-linux',True,False),('x86-rollback','x86_64-tizen-linux',False,True),('armv7l','armv7l-tizen-linux',False,False),('aarch64','aarch64-tizen-linux',False,False)]:
    path='/home/abuild/debuglink-parse-fix-20261029/'+('rollback.spec' if rollback else 'llvm.spec')
    common=['--target',target,'--define','_sourcedir /home/abuild/debuglink-parse-fix-20261029/SOURCES','--define','_builddir /home/abuild/debuglink-parse-fix-20261029/BUILD','--define','_buildrootdir /home/abuild/debuglink-parse-fix-20261029/BUILDROOT','--define','_tmppath /home/abuild/debuglink-parse-fix-20261029/tmp','--define','_toolchain clang']
    row,_=run(name,['/usr/bin/rpmbuild','-bp','--nodeps','--nobuild']+common+(['--without','clang_bolt'] if off else [])+[path])
    expanded,text=run(name+'-expanded',['/usr/bin/rpmspec','-P']+common+(['--define','_without_clang_bolt 1'] if off else [])+[path])
    row.update(case=name,expanded=expanded,sources_patches=[x for x in text.splitlines() if re.match(r'^(Source|Patch)\d*:',x)])
    row['PASS']=row['rc']==0 and expanded['rc']==0 and sum(x.startswith('Patch') for x in row['sources_patches'])==8
    rows.append(row);(E/'matrix.json').write_text(json.dumps(rows,indent=2))
    assert row['PASS'],row
# OFF must be identical with the baseline under both debug and release macros.
for mode,defines in [('debug',['--define','_toolchain clang']),('release',['--undefine','_toolchain'])]:
    (P/'baseline.spec').write_bytes(subprocess.check_output(['git','-C',json.loads((D/'plan.json').read_text())['source'],'show','f308fe08eeaad4e219f8505449b88bd5f644ea8c:packaging/llvm.spec']))
    (P/'new-source.spec').write_text((Path(json.loads((D/'plan.json').read_text())['source'])/'packaging/llvm.spec').read_text())
    outs=[]
    for label,file in [('baseline','baseline.spec'),('new','new-source.spec')]:
        rr,tt=run('off-'+mode+'-'+label,['/usr/bin/rpmspec','-P','--target','x86_64-tizen-linux','--define','_without_clang_bolt 1',*defines,str(P.relative_to(R)/file) if False else '/home/abuild/debuglink-parse-fix-20261029/'+file])
        assert rr['rc']==0
        # Source specs avoid the unrelated GBS-injected VCS header. No normalization.
        outs.append(tt.encode())
    assert outs[0]==outs[1], 'OFF expansion differs '+mode
(E/'off-comparison.json').write_text(json.dumps({'debug':'byte-identical source-spec expansion, no normalization','release':'byte-identical source-spec expansion, no normalization'}))
print('five Tizen RPM parses and OFF expansion PASS')

for mode,defines in [('debug',['--define','_toolchain clang']),('release',['--undefine','_toolchain'])]:
 rr,tt=run('on-'+mode,['/usr/bin/rpmspec','-P','--target','x86_64-tizen-linux',*defines,'/home/abuild/debuglink-parse-fix-20261029/new-source.spec'])
 assert rr['rc']==0
 lines=[l for l in tt.splitlines() if ' pipeline ' in l and 'python3' in l]
 assert len(lines)==1 and ('--debug-symbols' in lines[0])==(mode=='debug'),lines
 deps=[l for l in tt.splitlines() if l.startswith('BuildRequires:')]
 assert any('elfutils' in l.split() for l in deps),deps
 assert ('RELCFLAGS=$(echo $CFLAGS' in tt)==(mode=='release')
 assert ('--debug-symbols' in tt)==(mode=='debug')
(E/'mode-check.json').write_text(json.dumps({'debug':'elfutils and --debug-symbols present; no release -g removal','release':'elfutils present, --debug-symbols absent; release -g removal present; _toolchain explicitly undefined at entry'}))
