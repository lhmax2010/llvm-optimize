from common import *
import time,re
out=D/'old-text';out.mkdir();inp=WORK/'reference-relocs-clang-22';assert inp.is_file(),'relink input absent; do not relink'
ids=json.loads((E/'input-identities.json').read_text());assert sha(inp)==ids[str(inp)]
argv=loader(BUILD/'bin/llvm-bolt')+[str(inp),'-o',str(out/'clang.bolt'),'-data='+str(WORK/'profile.fdata'),*h.OPTIONS,'-use-old-text'];h.profile_identity(WORK/'profile.fdata')
version=subprocess.check_output(loader(BUILD/'bin/llvm-bolt')+['--version'],text=True);h.certified_version(version);(E/'oldtext-tool-version.txt').write_text(version)
start=time.monotonic()
with (E/'oldtext-bolt.log').open('wb') as log:p=subprocess.run(['/usr/bin/time','-v','-o',str(E/'oldtext-bolt.time'),*argv],stdout=log,stderr=subprocess.STDOUT,env={**os.environ,'LC_ALL':'C'})
row={'argv':argv,'rc':p.returncode,'seconds':time.monotonic()-start};save(E/'oldtext-result.json',row);assert p.returncode==0
counts=h.match_counts((E/'oldtext-bolt.log').read_text(),argv,True,True);row['counts']=counts;save(E/'oldtext-result.json',row);assert counts['R']<=0.05 and counts['S']==0,counts
e=h.ELF(out/'clang.bolt');row['elf_before']=e.audit();e.close()
shutil.copy2(out/'clang.bolt',out/'clang.candidate');p=subprocess.run(loader(BUILD/'bin/llvm-strip')+['--strip-all',str(out/'clang.candidate')],capture_output=True,text=True);(E/'oldtext-strip.stderr').write_text(p.stderr);assert p.returncode==0,p.stderr
e=h.ELF(out/'clang.candidate');row['elf_after']=e.audit(final=True);e.close()
m=re.search(r'Maximum resident set size \(kbytes\): (\d+)',(E/'oldtext-bolt.time').read_text());assert m
row.update(PASS=True,max_rss_KiB=int(m[1]),candidate_sha256=sha(out/'clang.candidate'),candidate_bytes=(out/'clang.candidate').stat().st_size,input_sha256=sha(inp),tool_sha256=sha(BUILD/'bin/llvm-bolt'),current_candidate_sha256=sha(WORK/'clang.candidate'),current_bytes=(WORK/'clang.candidate').stat().st_size,profile_sha256=h.PROFILE_SHA,experiment_only=True)
save(E/'oldtext-result.json',row);print('OLDTEXT_REWRITE_PASS',row['candidate_bytes'],counts,flush=True)
