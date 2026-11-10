from pathlib import Path
import signal
import urllib.request,urllib.error,urllib.parse,json,re,hashlib,subprocess,datetime,xml.etree.ElementTree as ET
E=Path(__file__).resolve().parent
S=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/hq-463c9a13/repo')
rev='463c9a133a6dfea9adf1e6c8e07ab705cbf2a587'
def git(*a):return subprocess.check_output(['git','-C',str(S),*a],timeout=30).decode()
stat=git('diff','--stat','67619ec8bbbac7238a6cfc33a481ccfbcd12206f',rev)
names=git('diff','--name-only','67619ec8bbbac7238a6cfc33a481ccfbcd12206f',rev).splitlines()
(E/'candidate-source-stat.txt').write_text(stat)
(E/'candidate-source-chain.txt').write_text(git('log','-6','--format=fuller',rev))
ancestry={'status':'UNKNOWN: optional full-history ancestry walk interrupted after 13 minutes; source tree comparison used instead'}
source={'revision':rev,'patchset':7,'change':359934,'files_vs_67619ec8':names,'no_hybrid_tree':names==['packaging/llvm-static-archives-native.py'],'hybrid_ancestry':ancestry}
(E/'candidate-source.json').write_text(json.dumps(source,indent=2)+'\n')
def request(url,method='GET'):
 row={'url':url,'method':method,'time':datetime.datetime.now().astimezone().isoformat()}
 print('REQUEST',method,url,flush=True)
 def expired(sig,frame):raise TimeoutError('total request timeout 45s')
 signal.signal(signal.SIGALRM,expired);signal.alarm(45)
 try:
  with urllib.request.urlopen(urllib.request.Request(url,method=method),timeout=45) as resp:
   row.update(status=resp.status,final_url=resp.url,content_length=resp.headers.get('Content-Length'),content_type=resp.headers.get('Content-Type'))
   data=b'' if method=='HEAD' else resp.read(4*1024*1024+1)
   if len(data)>4*1024*1024:raise RuntimeError('directory or manifest exceeds 4 MiB')
   return row,data
 except Exception as ex:
  row.update(error=str(ex),status=getattr(ex,'code',None));return row,b''
 finally:signal.alarm(0)
results=[]
for bid,project,expected in [('1216400','Tizen-Base-Dev','tizen-base-dev_20261030.061217'),('1216401','Tizen-Base-Toolchain','tizen-base-toolchain_20261030.061318')]:
 text=(E/bid/'overview.txt').read_text()
 def field(name):return next(x.split('\t',1)[1].strip() for x in text.splitlines() if x.startswith(name+'\t'))
 build=field('Build Package List');profile=field('Profile URL');base=field('Download_URL').replace('http://','https://').rstrip('/')+'/'
 snap=base.rstrip('/').rsplit('/',1)[-1]
 row={'qb':bid,'qb_url':'https://quickbuild.tizen.org/build/'+bid,'project':project,'source_line':build,'source_confirmed':build=='platform/upstream/llvm@'+rev,'revision':rev,'change':359934,'patchset':7,'profile_url':profile,'snapshot':profile.rstrip('/').rsplit('/',1)[-1],'snapshot_matches':profile.rstrip('/').endswith('/'+expected),'output_url':base,'no_hybrid':source['no_hybrid_tree'],'architectures':[]}
 mu=base+'builddata/manifest/'+snap+'_standard.xml'
 mr,md=request(mu);row['manifest_request']=mr
 if md:
  (E/bid/'manifest.xml').write_bytes(md)
  try:row['manifest_llvm']=[p.attrib for p in ET.fromstring(md).findall('.//project') if p.get('name')=='platform/upstream/llvm']
  except Exception as ex:row['manifest_error']=str(ex)
 for arch in ['armv7l','aarch64']:
  url=base+'repos/standard/packages/'+arch+'/'
  meta,data=request(url)
  ar={'arch':arch,'directory':meta,'packages':[]}
  if data:
   (E/bid/(arch+'-packages.html')).write_bytes(data)
   links=re.findall(r'href=["\x27]([^"\x27]+)["\x27]',data.decode(errors='replace'))
   wanted=[x for x in links if re.match(r'^(clang|llvm-devel)-[0-9].*\.rpm$',x.rsplit('/',1)[-1])]
   for link in wanted:
    pm,_=request(urllib.parse.urljoin(url,link),'HEAD')
    ar['packages'].append(pm)
  ar['downloadable']=meta.get('status')==200 and len(ar['packages'])>=2 and all(x.get('status')==200 for x in ar['packages'])
  row['architectures'].append(ar)
  print(bid,arch,json.dumps(ar),flush=True)
 row['usable_arm_baseline']=row['source_confirmed'] and row['snapshot_matches'] and row['no_hybrid'] and all(a['downloadable'] for a in row['architectures'])
 row['reason']='all four conditions satisfied' if row['usable_arm_baseline'] else 'one or more required conditions not demonstrated'
 results.append(row)
(E/'arm-candidates.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2),flush=True)
print('ARM_CANDIDATES 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status=ok',flush=True)
