"""Serial download, RPM query, extraction, hashing/readelf, then delete this extraction only.
Never installs RPMs or executes package code. Resume skips packages with a completed record.
"""
from common import *
import os,stat,subprocess,shutil,re,time
from bs4 import BeautifulSoup
PACKAGES=[('x86_64','clang'),('x86_64','llvm'),('x86_64','libllvm'),('x86_64','llvm-devel'),('armv7l','clang'),('armv7l','llvm'),('armv7l','clang-accel-x86_64-armv7l')]
def run(args):
 p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if p.returncode:raise RuntimeError(str(args)+': '+p.stderr.decode(errors='replace'))
 return p.stdout
RAW.mkdir(parents=True,exist_ok=True);TEMP.mkdir(parents=True,exist_ok=True)
for arch,pkg in PACKAGES:
 for label,snapshot in SNAPSHOTS.items():
  key=f'{label}_{arch}_{pkg}';done=RAW/f'{key}_complete.json'
  if done.exists():print('already complete',key,flush=True);continue
  base=f'https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_{snapshot}/repos/standard/packages/{arch}/'
  index=RAW/f'{label}_{arch}_rpm_index.html'
  if not index.exists():
   m=fetch(base,index)
   if m['status']!=200:raise RuntimeError('index download failed')
  s=BeautifulSoup(index.read_text(),'html.parser');candidates=[a['href'] for a in s.find_all('a',href=True) if re.fullmatch(re.escape(pkg)+r'-[0-9][^-]*-[^.]+(?:\.[^.]+)*\.'+arch+r'\.rpm',a['href'])]
  if len(candidates)!=1:raise RuntimeError((key,candidates))
  name=candidates[0];rpm=TEMP/label/arch/name;prior=[]
  if (RAW/'fetch_manifest.jsonl').exists():prior=[json.loads(l) for l in (RAW/'fetch_manifest.jsonl').read_text().splitlines() if json.loads(l)['file']==str(rpm.relative_to(ROOT)) and json.loads(l)['status']==200]
  if prior and rpm.exists() and rpm.stat().st_size==prior[-1]['bytes']:meta=prior[-1]
  else:meta=fetch(base+name,rpm)
  if meta['status']!=200:raise RuntimeError('RPM download failed')
  header_format='\n'.join(k+'=%{'+k+'}' for k in ['NAME','VERSION','RELEASE','ARCH','PAYLOADCOMPRESSOR','PAYLOADFLAGS','SIZE','ARCHIVESIZE','BUILDTIME','BUILDHOST','SOURCERPM','FILEDIGESTALGO'])+'\n'
  header=run(['rpm','-qp','--qf',header_format,str(rpm)]).decode();(RAW/f'{key}_rpm_header.txt').write_text(header)
  query='[%{FILENAMES}\t%{FILESIZES}\t%{FILEMODES:octal}\t%{FILELINKTOS}\t%{FILEINODES}\t%{FILEDEVICES}\t%{FILEFLAGS}\t%{FILEDIGESTS}\n]'
  listing=run(['rpm','-qp','--qf',query,str(rpm)]).decode();(RAW/f'{key}_rpm_files.tsv').write_text('path\theader_size\tmode_octal\tlink_target\tinode\tdevice\tflags\tdigest\n'+listing)
  header_rows=[l.split('\t') for l in listing.splitlines()];dest=TEMP/'extract'/key
  if dest.exists():raise RuntimeError(f'Incomplete extraction exists: {dest}; inspect before restart')
  dest.mkdir(parents=True);free_before=shutil.disk_usage(TEMP).free;started=now()
  print('extract',key,flush=True)
  p=subprocess.Popen(['rpm2cpio',str(rpm)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  c=subprocess.run(['cpio','-idm','--quiet','--no-absolute-filenames'],stdin=p.stdout,cwd=dest,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  p.stdout.close();err=p.stderr.read();rc=p.wait()
  (RAW/f'{key}_extract_stderr.txt').write_bytes(err+c.stderr)
  if rc or c.returncode:raise RuntimeError((key,rc,c.returncode))
  records=[];inode_cache={};elf_dir=RAW/'elf'/key;elf_dir.mkdir(parents=True,exist_ok=True)
  for i,h in enumerate(header_rows,1):
   path,hsize,mode,link,inode,device,flags,digest=h;relative=Path(path.lstrip('/'))
   if '..' in relative.parts:raise RuntimeError('unsafe RPM path')
   target=dest/relative;rec={'snapshot':snapshot,'side':label,'arch':arch,'package':pkg,'rpm':name,'path':path,'rpm_header_size':int(hsize),'rpm_header_mode_octal':mode,'rpm_header_link_target':link,'rpm_header_inode':inode,'rpm_header_device':device,'rpm_header_flags':flags,'rpm_header_digest':digest,'header_evidence':f'raw/{key}_rpm_files.tsv:{i+1}'}
   try:st=target.lstat()
   except FileNotFoundError:
    rec.update(type='missing',size=None,sha256=None,elf=False);records.append(rec);continue
   if stat.S_ISREG(st.st_mode):
    ident=(st.st_dev,st.st_ino);rec.update(type='regular',size=st.st_size,nlink=st.st_nlink)
    if ident in inode_cache:rec.update(inode_cache[ident]);rec['hardlink_duplicate']=True
    else:
     with target.open('rb') as f:magic=f.read(4)
     data={'sha256':sha(target),'elf':magic==b'\x7fELF','magic_hex':magic.hex(),'hardlink_duplicate':False}
     if data['elf']:
      ep=elf_dir/f'{i:05d}.txt'
      pieces=[]
      for args in [['readelf','-W','-h',str(target)],['readelf','-W','-S',str(target)],['readelf','-W','-d',str(target)],['readelf','-W','-n',str(target)]]:
       res=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
       pieces.append(('COMMAND: '+' '.join(args)+'\nEXIT: '+str(res.returncode)+'\n').encode()+res.stdout+b'\nSTDERR:\n'+res.stderr+b'\n')
      ep.write_bytes(b''.join(pieces));data['readelf_file']=str(ep.relative_to(OUT))
     inode_cache[ident]=data;rec.update(data)
   elif stat.S_ISLNK(st.st_mode):rec.update(type='symlink',size=st.st_size,link_target=os.readlink(target),sha256=None,elf=False)
   elif stat.S_ISDIR(st.st_mode):rec.update(type='directory',size=0,sha256=None,elf=False)
   else:rec.update(type='special',size=0,sha256=None,elf=False)
   records.append(rec)
  with (RAW/f'{key}_files.jsonl').open('w') as f:
   for rec in records:f.write(json.dumps(rec,ensure_ascii=False)+'\n')
  unique_regular_bytes=sum(v['size'] for v in records if v['type']=='regular' and not v['hardlink_duplicate'])
  logical_regular_bytes=sum(v['size'] for v in records if v['type']=='regular')
  missing=[v['path'] for v in records if v['type']=='missing'];before_delete=shutil.disk_usage(TEMP).free
  # This directory was created by this invocation; all metadata and readelf output are now saved.
  shutil.rmtree(dest)
  complete={'side':label,'snapshot':snapshot,'arch':arch,'package':pkg,'rpm':name,'url':meta['url'],'rpm_sha256':meta['sha256'],'rpm_bytes':meta['bytes'],'started_at':started,'finished_at':now(),'file_count':len(records),'regular_path_bytes':logical_regular_bytes,'unique_regular_bytes':unique_regular_bytes,'symlink_path_bytes':sum(v['size'] for v in records if v['type']=='symlink'),'elf_paths':sum(v['elf'] for v in records),'missing_paths':missing,'free_bytes_before_extract':free_before,'free_bytes_before_delete':before_delete,'free_bytes_after_delete':shutil.disk_usage(TEMP).free,'extraction_deleted':not dest.exists(),'inventory':f'raw/{key}_files.jsonl'}
  done.write_text(json.dumps(complete,indent=2,ensure_ascii=False)+'\n');print('complete',key,'files',len(records),'deleted',not dest.exists(),flush=True)
