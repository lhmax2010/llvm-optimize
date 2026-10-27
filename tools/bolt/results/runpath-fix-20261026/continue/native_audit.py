from common import *
import tarfile,struct
from compare import ar_members
# Also perform literal byte comparisons, beyond the earlier frozen-region SHA comparison.
a=h.ELF(OLD/'binaries/clang.candidate');b=h.ELF(P/'binaries/clang.candidate')
try:
 assert len(a.mm)==len(b.mm) and a.phdrs==b.phdrs and a.sections==b.sections
 spans=sorted((sec[4],sec[4]+sec[5]) for name,sec in a.by_name.items() if name in ('.dynstr','.dynamic'));pos=0;compared=0
 for start,end in spans+[(len(a.mm),len(a.mm))]:
  for at in range(pos,start,1024*1024):
   until=min(at+1024*1024,start);assert a.mm[at:until]==b.mm[at:until],('ELF byte difference',at);compared+=until-at
  pos=end
 save(E/'elf-literal-bytes.json',{'PASS':True,'compared_bytes':compared,'file_bytes':len(a.mm),'excluded_ranges':spans,'method':'literal 1 MiB chunk equality, no hash-only inference','program_headers_equal':True,'section_headers_equal':True})
finally:a.close();b.close()
native=BUILD/'native-archive-conversion';summary=json.loads((native/'summary.json').read_text());assert summary['status']=='PASS',summary['status']
with tarfile.open(BASE/'native-archive-evidence.tar.gz') as tar:
 names=tar.getnames();sums=[n for n in names if n=='summary.json'];assert len(sums)==1
 archived=tar.extractfile(sums[0]).read();assert archived==(native/'summary.json').read_bytes()
save(E/'native-evidence-match.json',{'summary_sha':sha(native/'summary.json'),'tar_sha':sha(BASE/'native-archive-evidence.tar.gz'),'summary_bytes_equal':True,'scanned_archives':summary['scanned_archives'],'native_archives_skipped':summary['native_archives_skipped'],'converted_paths':[x['path'] for x in summary['archives']]})
snapshot=json.loads((WORK/'install-before.json').read_text())['files']
allpaths={name for name in snapshot if name.endswith('.a')};converted={x['path'] for x in summary['archives']};skipped=sorted(allpaths-converted);assert len(allpaths)==summary['scanned_archives']==270;assert len(skipped)==summary['native_archives_skipped']==45
package=json.loads((E/'rpm-comparison/compiler-rt-22.1.8-1.x86_64.rpm.json').read_text());s=package['result'];different={x['path'] for x in s['ar_date_differences']};assert set(skipped)==different
root=X/'rpm-differences/compiler-rt-22.1.8-1.x86_64.rpm/new'
# GBS %clean removed BUILDROOT. The untouched build archives must match the pre-install snapshot;
# inspect retained RPM payload copies too, rather than inventing a missing buildroot.
rows=[]
for path in skipped:
 free();p=root/path;assert sha(p)==package['new_files'][path]['sha256'];original=BUILD/path.removeprefix('usr/');assert sha(original)==snapshot[path]['sha256'];data=p.read_bytes();members=[]
 original_members=[m for m in ar_members(original.read_bytes()) if m['raw_name'] not in ('/','//','/SYM64/')]
 for m in ar_members(data):
  if m['raw_name'] in ('/','//','/SYM64/'):continue
  body=m.pop('body');kind='bitcode' if body[:4] in (b'BC\xc0\xde',b'\xde\xc0\x17\x0b') else 'ELF-relocatable' if len(body)>=20 and body[:6]==b'\x7fELF\x02\x01' and int.from_bytes(body[16:18],'little')==1 else 'other'
  m.update(kind=kind,machine=int.from_bytes(body[18:20],'little') if kind=='ELF-relocatable' else None);members.append(m)
 row={'path':path,'sha256':sha(p),'members':members,'bitcode':sum(m['kind']=='bitcode' for m in members),'other':sum(m['kind']=='other' for m in members),'ELF_relocatable':sum(m['kind']=='ELF-relocatable' for m in members)};rows.append(row);save(E/'native-skipped-members.json',rows)
 assert members and row['bitcode']==0 and row['other']==0 and all(m['machine']==62 for m in members),path
 assert [m['name'] for m in members]==[m['name'] for m in original_members],path
 for m in original_members:
  body=m['body'];assert len(body)>=20 and body[:6]==b'\x7fELF\x02\x01' and int.from_bytes(body[16:18],'little')==1 and int.from_bytes(body[18:20],'little')==62,path
 row['build_original_sha256']=sha(original);row['build_original_matches_preinstall_snapshot']=True;row['original_member_contents_equal_packaged']=[m['sha256'] for m in members]==[m['sha256'] for m in original_members];save(E/'native-skipped-members.json',rows)
for name in ['libclang_rt.builtins-x86_64.a','libclang_rt.asan-x86_64.a']:
 p=root/'usr/lib64/clang/22/lib/linux'/name;cmd=loader(BUILD/'bin/llvm-readelf')+['-h',str(p)];res=subprocess.run(cmd,capture_output=True,text=True);(E/(name+'.readelf.txt')).write_text(res.stdout);(E/(name+'.readelf.stderr')).write_text(res.stderr);assert res.returncode==0
 types=[l.strip() for l in res.stdout.splitlines() if 'Type:' in l];machines=[l.strip() for l in res.stdout.splitlines() if 'Machine:' in l];assert types and all('REL (' in l for l in types) and len(types)==len(machines) and all('X86-64' in l or 'x86-64' in l for l in machines),(types[:2],machines[:2])
save(E/'native-audit.json',{'PASS':True,'skipped_archives':45,'matched_date_difference_files':45,'members':sum(len(x['members']) for x in rows),'bitcode_members':0,'other_members':0,'note':'ar symbol/name tables are metadata, not object members; each object is ELF64 little-endian ET_REL EM_X86_64','paths':skipped,'provenance':'270 pre-install snapshot paths minus 225 converted paths = 45 skipped; build originals match snapshot SHA; RPM member names/order match originals; both originals and packaged members independently ELF ET_REL; original/package content differences separately recorded (platform strip); summary inside evidence tar matches retained conversion summary exactly'});print('NATIVE45_PASS',flush=True)
