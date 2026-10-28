from pathlib import Path
import gzip,re,json,subprocess,urllib.request,hashlib
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=Path(__file__).resolve().parent;E=B/'tools/bolt/results/qb-fail-20261028/meta/buildconf';E.mkdir(parents=True,exist_ok=True)
R=W/'temp/qb-meta-20261028/repo'
logs={'1202084':B/'tools/bolt/results/qb-timeout-20261021/child/1202084-full-log.txt.gz','1211018':B/'tools/bolt/results/qb-fail-20261028/1211014/1211018-child-full-log.txt.gz'}
for name,p in logs.items():
 lines=gzip.decompress(p.read_bytes()).decode(errors='replace').splitlines();hits=set()
 for i,line in enumerate(lines):
  if re.search(r'get_build_conf|project_config|build.conf|_config|set.*config|prjconf|base.*config',line,re.I):hits.update(range(max(0,i-3),min(len(lines),i+7)))
 (E/(name+'-config-excerpts.txt')).write_text('\n'.join(f'{i+1}: {lines[i]}' for i in sorted(hits))+'\n')
for name in ('manifest.xml','project_config','project_env','project_meta','snapshot_info'):
 p=R/'TIZEN/Tizen/Tizen-Base-Toolchain'/name;(E/('toolchain-'+name)).write_bytes(p.read_bytes())
files=subprocess.check_output(['git','-C',str(R),'ls-files'],text=True).splitlines();(E/'repository-file-inventory.txt').write_text('\n'.join(files)+'\n')
for paths,label in [(['TIZEN/Tizen/Tizen-Base-Toolchain/project_config'],'toolchain-project-config-history'),([':(glob)**/project_config*',' :(glob)**/build.conf*'.strip()],'override-history')]:
 out=subprocess.check_output(['git','-C',str(R),'log','--all','--format=fuller','--stat','--since=2026-10-01','--',*paths],text=True);(E/(label+'.txt')).write_text(out)
urls=['https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261013.024319/repos/standard/','https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261013.024319/repos/standard/source/']
prov=[]
for i,url in enumerate(urls):
 try:
  with urllib.request.urlopen(url,timeout=60) as r: data=r.read();code=r.status;final=r.url
  (E/f'source-index-{i}.html').write_bytes(data);prov.append(dict(url=url,final=final,status=code,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()));print(url,code,len(data),flush=True)
 except Exception as ex:prov.append(dict(url=url,error=str(ex)));print(url,ex,flush=True)
(E/'source-discovery.json').write_text(json.dumps(prov,indent=2)+'\n')
