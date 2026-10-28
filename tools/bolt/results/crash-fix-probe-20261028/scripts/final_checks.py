from common import *
import re,struct
run('platform-objcopy-version',[*LD,R/'usr/bin/objcopy','--version'])
run('platform-gnu-keep',['/usr/bin/time','-v',*LD,R/'usr/bin/objcopy','--only-keep-debug',WORK/'clang.bolt',D/'platform-gnu.debug'])
run('clang-rpm-files',['rpm','-qpl',W/'temp/oldtext-final-20261027/products/RPMS/clang-22.1.8-1.x86_64.rpm'])
# Exact list enumeration from platform find-debuginfo.sh, on the NEW temporary chroot only.
C=D/'scratch.debug-probe'
script=D/'enumerate-debug.sh';script.write_text('#!/bin/sh\nset -e\ncd "$1/usr"\n(test ! -d lib/debug || find lib/debug ! -type d) | sed "s,^,/usr/,"\n')
run('platform-debug-list',['/bin/sh',script,C])
assert '/usr/lib/debug/usr/bin/clang-22.debug' in (E/'platform-debug-list.stdout').read_text().splitlines()
assert '/usr/bin/clang-22' in (E/'clang-rpm-files.stdout').read_text().splitlines()
save('package-list-analysis.json',{'enumerated_debug_path':'/usr/lib/debug/usr/bin/clang-22.debug','main_file_in_clang_package':True,'platform_macro_debuginfo_subpackages':1,'rule':'debug path = /usr/lib/debug + binary path + .debug','expected_package':'clang-debuginfo','scope':'Read-only scripts/macros + existing RPM file list + exact enumeration on temporary root. No new RPM built; upstream 4.14 files.c supports mapping but exact Tizen binary not rebuilt.'})
# Record file containment as well as virtual address containment; non-ALLOC sections may be outside LOAD.
analysis={}
for role,p in [('bolt39',WORK/'clang.bolt'),('bolt37',OLD/'clang.bolt'),('ordinary',WORK/'ordinary-clang-22')]:
 a=h.ELF(p);alloc=[]
 for name,s in a.by_name.items():
  if s[2]&2 and s[1]!=8 and s[5]:
   match=[i for i,q in enumerate(a.phdrs) if q[0]==1 and q[2]<=s[4] and s[4]+s[5]<=q[2]+q[5] and q[3]<=s[3] and s[3]+s[5]<=q[3]+q[6] and s[4]-q[2]==s[3]-q[3]]
   alloc.append({'name':name,'containing_LOAD':match});assert match,(role,name)
 phdr=a.phdrs[0];analysis[role]={'all_alloc_file_sections_contained':True,'sections':alloc,'PT_PHDR':phdr,'program_header_offset':struct.unpack_from('<Q',a.mm,32)[0],'phdr_contained_by_load':[i for i,q in enumerate(a.phdrs) if q[0]==1 and q[2]<=phdr[2] and phdr[2]+phdr[5]<=q[2]+q[5]],'gnu_build_id_present':'.note.gnu.build-id' in a.names};a.close()
save('elf-containment.json',analysis)
# Summarize actual debugger frames, not just exit status.
text=(E/'chroot-lldb-with-proc.stdout').read_text().split('(lldb) bt all\n',1)[1].split('(lldb) quit',1)[0]
frames=[x for x in text.splitlines() if re.search(r'frame #\d+:',x)]
clang=[x for x in frames if 'clang-22`' in x]
sym={}
for role in ['debug','auto-debuglink','gnu-direct','eu-direct']:
 blocks=(E/('symbolizer-'+role+'.stdout')).read_text().strip().split('\n\n');sym[role]={'total':len(blocks),'named':sum(not x.startswith('??') for x in blocks),'source_lines':sum(not x.splitlines()[-1].startswith('??:0') for x in blocks)}
save('symbolization-summary.json',{'lldb_auto_loaded_standard_debug_file':True,'lldb_total_frames':len(frames),'lldb_named_clang_frames':len(clang),'lldb_other_frames':len(frames)-len(clang),'symbolizer':sym,'crash_signal':'SIGILL (pragma emits ud2)','core_files_generated':0,'RLIMIT_CORE':0})
# Existing inputs still have original identities.
ids=json.loads((E/'input-identities.json').read_text());save('input-recheck.json',{k:{'sha256':sha(v['path']),'unchanged':sha(v['path'])==v['sha256']} for k,v in ids.items()})
run('end-source-status',['git','-C',S,'status','--porcelain'])
run('end-mount-check',['findmnt','-R',C])
print('final checks complete',flush=True)
