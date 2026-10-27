from pathlib import Path
import subprocess,json,hashlib,time,importlib.util,shutil
D=Path(__file__).resolve().parent;W=D.parent.parent;E=W.parent/'llvm-optimize-bolt/tools/bolt/results/runpath-fix-20261026';R=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';build=Path('/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build');work=build/'clang-bolt';X=Path('/home/abuild/runpath-oldtext');out=R/X.relative_to('/');out.mkdir(exist_ok=True)
assert json.loads((E/'build-result.json').read_text())['exit_code']==0
assert all(x['PASS'] for x in json.loads((E/'rpm-comparison/summary.json').read_text()))
s=importlib.util.spec_from_file_location('helper',D/'source/packaging/clang-bolt-helper.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
argv=[str(build/'bin/llvm-bolt'),str(work/'reference-relocs-clang-22'),'-o',str(X/'clang.bolt'),'-data='+str(work/'profile.fdata'),*h.OPTIONS,'-use-old-text']
assert not (out/'clang.bolt').exists()
prefix=['sudo','-n','/usr/sbin/chroot','--userspec=1000:1000',str(R),'/usr/bin/env','PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin','LC_ALL=C']
version=subprocess.check_output(prefix+[str(build/'bin/llvm-bolt'),'--version'],text=True);h.certified_version(version);(E/'oldtext-tool-version.txt').write_text(version)
h.profile_identity(R/(work/'profile.fdata').relative_to('/'))
start=time.monotonic()
with (E/'oldtext-bolt.log').open('wb') as log:p=subprocess.run(['/usr/bin/time','-v','-o',str(E/'oldtext-bolt.time'),*prefix,*argv],stdout=log,stderr=subprocess.STDOUT)
row={'argv':argv,'rc':p.returncode,'seconds':time.monotonic()-start};(E/'oldtext-result.json').write_text(json.dumps(row,indent=2));assert p.returncode==0
row['counts']=h.match_counts((E/'oldtext-bolt.log').read_text(),argv,True,True)
e=h.ELF(out/'clang.bolt');row['elf_before']=e.audit();e.close()
shutil.copy2(out/'clang.bolt',out/'clang.candidate');p=subprocess.run(prefix+[str(build/'bin/llvm-strip'),'--strip-all',str(X/'clang.candidate')],capture_output=True,text=True);assert p.returncode==0,p.stderr
e=h.ELF(out/'clang.candidate');row['elf_after']=e.audit(final=True);e.close()
row.update(candidate_sha256=h.digest(out/'clang.candidate'),candidate_bytes=(out/'clang.candidate').stat().st_size,input_sha256=h.digest(R/(work/'reference-relocs-clang-22').relative_to('/')),tool_sha256=h.digest(R/(build/'bin/llvm-bolt').relative_to('/')),current_candidate_sha256=h.digest(R/(work/'clang.candidate').relative_to('/')),current_bytes=(R/(work/'clang.candidate').relative_to('/')).stat().st_size,profile_sha256=h.PROFILE_SHA,experiment_only=True)
(E/'oldtext-result.json').write_text(json.dumps(row,indent=2));print('OLDTEXT_REWRITE_PASS',row['candidate_bytes'],row['counts'],flush=True)
