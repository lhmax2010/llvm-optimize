import sys,hashlib,json
from pathlib import Path
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');pin=sys.argv[1]
paths=['docs/bolt/25_real_install_rehearsal.md','docs/bolt/STATUS.md','patches/bolt/draft-manifest.json']
paths += [p.relative_to(B).as_posix() for p in sorted((B/'tools/bolt/results/install-rehearsal-20261015').rglob('*')) if p.is_file()]
paths += [p.relative_to(B).as_posix() for p in sorted((B/'tools/bolt/results').glob('rehearsal-sandbox-*')) if p.is_file()]
base='https://raw.githubusercontent.com/lhmax2010/llvm-optimize/'
files=[];rows=[]
for n in range(0,len(paths),30):
 number=7+n//30;p=B/('docs/bolt/10_raw_links_part%d.md'%number);files.append(p.name)
 s='# Raw 续表：sandbox 收拢与真实安装演练（%d）\n\n证据钉提交：`%s`。分支链接随 bolt-v4 更新；钉提交链接固定。xz 为原文压缩件。\n\n| 文件 | 分支版 | 钉提交版 | 字节 | SHA256 |\n| --- | --- | --- | ---: | --- |\n'%(number,pin)
 for name in paths[n:n+30]:
  q=B/name;sha=hashlib.sha256(q.read_bytes()).hexdigest();b=base+'bolt-v4/'+name;f=base+pin+'/'+name;s+='| '+name+' | [bolt-v4]('+b+') | ['+pin[:7]+']('+f+') | '+str(q.stat().st_size)+' | '+sha+' |\n';rows.append({'path':name,'branch':b,'pinned':f,'sha256':sha})
 assert len(s.encode())<50000;p.write_text(s)
intro='\n\n真实安装演练25的全部raw：'+ '、'.join('['+f+']('+f+')' for f in files)+'。\n'
p=B/'docs/bolt/10_raw_links_part6.md';s=p.read_text();assert '真实安装演练25的全部raw' not in s;p.write_text(s+intro)
E=Path(__file__).resolve().parent;(E/'raw-links-to-verify.json').write_text(json.dumps(rows,indent=2)+'\n');print('raw pages',files,'links',2*len(rows))
