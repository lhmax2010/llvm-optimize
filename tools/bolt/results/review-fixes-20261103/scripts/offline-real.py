from pathlib import Path
import importlib.util,json,subprocess,shutil,time,hashlib
W=Path('/home/linhao/Toolchain/development/llvm-optimize');D=W/'temp/review-20261103';E=D/'evidence';S=W/'temp/review-20261102/source';H=W/'temp/debuglink-20261028/full-20261030';R=H/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';B=R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build'
s=importlib.util.spec_from_file_location('h',S/'packaging/clang-bolt-helper.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
(D/'real-files').mkdir(exist_ok=True);before=B/'clang-bolt/clang.bolt';strip=D/'real-files/clang.stripped';assert not strip.exists();shutil.copy2(before,strip)
argv=[str(R/'usr/lib64/ld-linux-x86-64.so.2'),'--library-path',str(B/'lib64')+':'+str(R/'usr/lib64'),str(B/'bin/llvm-strip'),'--strip-all',str(strip)]
t=time.monotonic();p=subprocess.run(argv,capture_output=True,text=True);(E/'real-strip.stdout').write_text(p.stdout);(E/'real-strip.stderr').write_text(p.stderr);assert p.returncode==0
r={'argv':argv,'rc':p.returncode,'seconds':time.monotonic()-t,'before_sha256':h.digest(before),'strip_tool_sha256':h.digest(B/'bin/llvm-strip'),'after_sha256':h.digest(strip)};assert r['after_sha256']=='13a07cb7f84bd1ceda4d851c8bd71bddf7ef0c2d4864892eba64cbbb9a0350b8'
after=W/'temp/oldtext-final-20261027/products/binaries/clang.candidate';assert h.digest(after)=='8c2429d870f421a29a9914458bc4d4ff2ce359a15e0bdd20f39bfb4580c40bdf'
identity=json.loads((B/'clang-bolt/identity.json').read_text());assert identity['strip_all_sha256']==r['after_sha256'] and identity['rpath_adjusted_sha256']==h.digest(after)
layout=h.rpath_layout(strip);new=h.rpath_layout(after,layout['allowed_ranges']);r.update(runpath_before=str(strip),runpath_after=str(after),runpath_after_sha256=h.digest(after),allowed_ranges=layout['allowed_ranges'],rpath_gate_pass=layout==new,full_20261030_identity_sha=h.digest(B/'clang-bolt/identity.json'));assert r['rpath_gate_pass']
r['debugfiles_gate']=h.debugfiles_gate(B/'clang-bolt/ordinary-clang-22',identity);(E/'real-offline-gates.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
shutil.copyfile(B.parent/'debugfiles.list',E/'full-20261030-debugfiles.list')
log=H/'evidence/rpm-build.log';lines=log.read_text(errors='replace').splitlines();hits=[(i,l) for i,l in enumerate(lines,1) if 'find-debuginfo.sh' in l or 'Processing files: clang-debuginfo' in l];(E/'debugfiles-log-excerpts.txt').write_text(''.join(f'{log}:{i}:{l}\n' for i,l in hits))
