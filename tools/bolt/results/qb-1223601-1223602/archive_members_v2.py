from pathlib import Path
import json,hashlib,struct
E=Path(__file__).resolve().parent;B=E.parents[3];W=B.parent/'llvm-optimize';P=W/'temp/qb-1223601-1223602/payload'
def members(p):
 rows=[];names=b''
 with p.open('rb') as f:
  assert f.read(8)==b'!<arch>\n'
  while True:
   pos=f.tell();h=f.read(60)
   if not h:break
   assert len(h)==60 and h[-2:]==b'`\n'
   size=int(h[48:58]);raw=h[:16].decode().strip();name=raw
   if raw.startswith('/') and raw[1:].isdigit():
    at=int(raw[1:]);end=names.find(b'/\n',at);assert end>=at;name=names[at:end].decode()
   elif raw not in ('/','//','/SYM64/'):name=raw.rstrip('/')
   left=size;hh=hashlib.sha256();parts=[];magic=b''
   while left:
    b=f.read(min(left,1048576));assert b
    if not magic:magic=b[:4]
    hh.update(b);left-=len(b)
    if raw=='//':parts.append(b)
   if raw=='//':names=b''.join(parts)
   pad=f.read(size%2)
   rows.append(dict(name=name,sha256=hh.hexdigest(),bytes=size,magic=magic.hex(),date=h[16:28].decode(),other_header=(h[:16]+h[28:]).hex(),offset=pos,pad=pad.hex()))
 return rows
allsummary={}
for proj in ['toolchain','basedev']:
 summary=W/'temp/night-20261103'/proj/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/native-archive-conversion/summary.json'
 source=json.loads(summary.read_text());modes={r['path']:r['results'] for r in source['archives']}
 rows=[];converted=[];preserved=[];datechanges=[];other=[];seen={};duplicates=[]
 for a in sorted((P/proj).glob('*/old/**/*.a')):
  pack=a.relative_to(P/proj).parts[0];rel=str(a.relative_to(P/proj/pack/'old'));b=P/proj/pack/'new'/rel
  aa,bb=members(a),members(b)
  assert [r['name'] for r in aa]==[r['name'] for r in bb],rel
  objs=[r for r in aa if r['name'] not in ('/','//','/SYM64/')]
  if rel in seen:
   assert seen[rel]==[(r['name'],r['sha256']) for r in aa],('duplicate package payload mismatch',rel)
   duplicates.append(dict(package=pack,path=rel))
  if rel in modes and rel not in seen:
   assert len(objs)==len(modes[rel]),rel
   for r,s in zip(objs,modes[rel]):
    assert r['name']==s['name'],(rel,r['name'],s['name'])
    (preserved if s['preserved'] else converted).append(dict(path=rel,ordinal=s['ordinal'],name=r['name'],old_sha256=r['sha256'],new_sha256=bb[aa.index(r)]['sha256']))
  seen[rel]=[(r['name'],r['sha256']) for r in aa]
  for x,y in zip(aa,bb):
   assert x['sha256']==y['sha256'] and x['other_header']==y['other_header'] and x['pad']==y['pad'],(rel,x['name'])
   if x['date']!=y['date']:datechanges.append(dict(path=rel,member=x['name'],old=x['date'],new=y['date']))
  rows.append(dict(package=pack,path=rel,member_names_order_equal=True,members=[dict(name=x['name'],bytes=x['bytes'],old_sha256=x['sha256'],new_sha256=y['sha256']) for x,y in zip(aa,bb)]))
 assert len(converted)==3853,(proj,len(converted))
 assert all(r['old_sha256']==r['new_sha256'] for r in converted)
 result=dict(duplicate_package_paths=duplicates,project=proj,converted=len(converted),native_members_preserved=len(preserved),all_member_SHA_equal=True,archives=len(rows),date_fields_changed=len(datechanges),converted_members=converted,preserved_members=preserved,archives_all=rows,date_changes=datechanges,classification_source=str(summary),classification_source_sha256=hashlib.sha256(summary.read_bytes()).hexdigest())
 data=(json.dumps(result,indent=2)+'\n').encode()
 import gzip
 (E/f'{proj}-archive-members.json.gz').write_bytes(gzip.compress(data,mtime=0))
 allsummary[proj]={k:v for k,v in result.items() if k in ['converted','native_members_preserved','all_member_SHA_equal','archives','date_fields_changed']}
 print(proj,allsummary[proj],flush=True)
(E/'archive-summary.json').write_text(json.dumps(allsummary,indent=2)+'\n')
