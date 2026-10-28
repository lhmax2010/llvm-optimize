from common import *
import re,lzma
# Preserve platform scripts and source excerpts with original line numbers.
P=E/'sources';P.mkdir(exist_ok=True)
sources={
 'find-debuginfo.sh':R/'usr/lib/rpm/find-debuginfo.sh',
 'rpm-macros':R/'usr/lib/rpm/macros',
 'brp-strip':R/'usr/lib/rpm/brp-strip',
 'brp-strip-comment-note':R/'usr/lib/rpm/brp-strip-comment-note',
 'ELFObject.cpp':S/'llvm/lib/ObjCopy/ELF/ELFObject.cpp',
 'Symbolize.cpp':S/'llvm/lib/DebugInfo/Symbolize/Symbolize.cpp',
 'llvm.spec':S/'packaging/llvm.spec',
 'clang-bolt-helper.py':S/'packaging/clang-bolt-helper.py',
 'rpm-files-upstream-4.14.x.c':D/'rpm-files-upstream.c'}
meta={}
for name,p in sources.items():
 if p.exists():
  txt=p.read_text();(P/name).write_text(txt);(P/(name+'.numbered.txt')).write_text(''.join(f'{i}: {l}\n' for i,l in enumerate(txt.splitlines(),1)));meta[name]={'source':str(p),'sha256':sha(p)}
meta['rpm-files-upstream-4.14.x.c']['url']='https://raw.githubusercontent.com/rpm-software-management/rpm/rpm-4.14.x/build/files.c';meta['rpm-files-upstream-4.14.x.c']['limit']='Upstream 4.14 branch supplementary source, not proof of exact Tizen patchset; local installed macros and actual package names are primary.'
save('sources/provenance.json',meta)
log=B/'tools/bolt/results/oldtext-final-20261027/rpm-build.log';lines=log.read_text().splitlines();hits=[]
for i,l in enumerate(lines):
 if re.search(r'find-debuginfo.sh|clang-22 is already stripped|Processing files: clang-debuginfo|BOLT_POST_GATE_PASS|brp-strip',l):
  hits.extend(f'{j+1}: {lines[j]}' for j in range(max(0,i-2),min(len(lines),i+3)))
(E/'platform-log-anchors.txt').write_text('\n'.join(hits)+'\n')
inv=[]
for root,dirs,files in os.walk(WORK):
 for n in files:
  p=Path(root)/n;inv.append({'path':str(p.relative_to(WORK)),'bytes':p.stat().st_size})
save('work-file-inventory.json',inv)
# Measure successful symbol separation, output in a fresh temporary file.
for role,argv in [('gnu',['/usr/bin/objcopy','--only-keep-debug',WORK/'clang.bolt',D/'timed-gnu.debug']),('eu',[*LD,R/'usr/bin/eu-strip','-f',D/'timed-eu.debug','-o',D/'timed-eu.stripped',WORK/'clang.bolt'])]:
 x=run('timed-'+role,['/usr/bin/time','-v',*argv]);assert x['rc']==0
 p=D/('timed-'+role+'.debug');run('debug-elf-'+role,['readelf','-h','-l','-S','-W',p])
 addresses=json.loads((E/'offline-addresses.json').read_text())['addresses'];run('symbolizer-'+role+'-direct',tool('llvm-symbolizer')+['--obj='+str(p),'--inlining=false'],stdin='\n'.join(x['module_offset'] for x in addresses)+'\n')
rows={}
for role in ['gnu','eu']:
 p=D/('timed-'+role+'.debug');c=lzma.LZMACompressor(preset=5);n=0
 with p.open('rb') as f:
  while x:=f.read(1048576):n+=len(c.compress(x))
 n+=len(c.flush());rows[role]={'bytes':p.stat().st_size,'sha256':sha(p),'xz5_bytes_estimate':n}
save('debug-sizes.json',rows)
# Collection input remains unchanged.
save('source-worktree-status.json',run('source-git-status',['git','-C',S,'status','--porcelain']))
print('collected',flush=True)
