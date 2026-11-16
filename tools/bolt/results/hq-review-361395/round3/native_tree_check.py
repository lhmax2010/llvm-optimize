import pathlib,subprocess,tarfile,hashlib,gzip,json,datetime
E=pathlib.Path(__file__).parent;c=json.loads((E/'candidate.json').read_text());S=c['source'];rev=c['HEAD']
tar=pathlib.Path(S).parent/'exports/candidate/llvm-22.1.8.tar.gz'
entries={}
for item in subprocess.check_output(['git','-C',S,'ls-tree','-r','-z',rev]).split(bytes([0])):
 if not item:continue
 meta,path=item.split(bytes([9]),1);mode,typ,oid=meta.decode().split();path=path.decode()
 if path.split('/')[0] in ('packaging','.git'):continue
 entries[path]=(mode,typ,oid)
seen=set();bad=[];count=0;excluded=0
with tarfile.open(tar,'r|gz') as tf,gzip.open(E/'native-git-files.jsonl.gz','wt') as out:
 for m in tf:
  if m.isdir():continue
  path=m.name.split('/',1)[1]
  if path.split('/')[0] in ('packaging','.git'):excluded+=1;continue
  seen.add(path);count+=1
  if m.isfile():
   h=hashlib.sha1(('blob '+str(m.size)+'\\0').encode());h2=hashlib.sha256()
   f=tf.extractfile(m)
   for b in iter(lambda:f.read(1024*1024),b''):h.update(b);h2.update(b)
   oid=h.hexdigest();sha=h2.hexdigest()
  elif m.issym():
   b=m.linkname.encode();oid=hashlib.sha1(('blob '+str(len(b))+'\\0').encode()+b).hexdigest();sha=hashlib.sha256(b).hexdigest()
  else:oid=None;sha=None
  expected=entries.get(path)
  good=expected is not None and expected[2]==oid
  row={'path':path,'bytes':m.size,'tar_blob':oid,'git':expected,'sha256':sha,'PASS':good}
  out.write(json.dumps(row)+'\\n')
  if not good:bad.append(row)
 missing=sorted(set(entries)-seen)
report={'PASS':not bad and not missing,'files':count,'excluded':excluded,'mismatches':bad,'git_only':missing,'tar':str(tar),'commit':rev,'time':datetime.datetime.now().astimezone().isoformat()}
(E/'native-git-result.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2),flush=True)
if not report['PASS']:raise SystemExit(1)
