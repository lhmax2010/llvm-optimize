"""Enumerate every changed source line; topic labels are mechanical, not causal attribution."""
from common import *
import csv,re,email,difflib
from bs4 import BeautifulSoup
from urllib.parse import urlparse,parse_qs

def write(name,rows):
 fields=list(dict.fromkeys(k for r in rows for k in r))
 with (OUT/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
commits=[]
for repo,name,direction in [('llvm','llvm_range.patch','old..new'),('qemu-accel','qemu-accel_range.patch','old..new'),('qemu-accel','qemu-accel_reverse_range.patch','new..old（补充反向集合）')]:
 p=RAW/name
 if not p.exists():continue
 s=p.read_text();starts=list(re.finditer(r'^From ([0-9a-f]{40}) Mon Sep 17 00:00:00 2001$',s,re.M))
 for j,m in enumerate(starts):
  part=s[m.end()+1:starts[j+1].start() if j+1<len(starts) else len(s)]
  msg=email.message_from_string(part.split('\n\n',1)[0]+'\n\n');ln=s[:m.start()].count('\n')+1
  commits.append({'repository':repo,'direction':direction,'commit':m[1],'author':str(msg['From']),'author_date':str(msg['Date']),'title':re.sub(r'\s+',' ',str(msg['Subject'])),'evidence':f'raw/{name}:{ln}-{ln+4}'})
for repo in ['llvm','qemu-accel']:
 name=f'{repo}_range_log.html'
 for i,line in enumerate((RAW/name).read_text().splitlines(),1):
  if 'logsubject' not in line:continue
  soup=BeautifulSoup(line,'html.parser');td=soup.find('td',class_='logsubject')
  if td is None:continue
  a=td.find('a');sha_id=parse_qs(urlparse(a['href']).query).get('id',[''])[0]
  for c in commits:
   if c['repository']==repo and c['commit']==sha_id:
    c['format_patch_subject']=c['title'];c['title']=a.get_text();c['log_evidence']=f'raw/{name}:{i}'
    age=soup.find('span',title=True);c['committer_date']=age['title'] if age else '未获取'
for c in commits:
 if not c.get('committer_date'):c['committer_date']='未获取（补充反向集合未取得 commit 页面；author_date 已获取）'
write('source_commits.csv',commits)
rows=[]
inputs=[('llvm','endpoint_packaging','llvm_packaging_complete.diff'),('qemu-accel','endpoint_full','qemu-accel_full_retry.diff'),('llvm','commit_series','llvm_range.patch'),('qemu-accel','commit_series','qemu-accel_range.patch'),('qemu-accel','reverse_commit_series','qemu-accel_reverse_range.patch')]
for repo,scope,name in inputs:
 p=RAW/name
 if not p.exists():continue
 path='';old=new=0;active=False;section='';commit='';hunk=''
 for ln,line in enumerate(p.read_text().splitlines(),1):
  m=re.match(r'From ([0-9a-f]{40}) Mon Sep 17',line)
  if m:commit=m[1]
  if line.startswith('diff --git '):path=line.split(' b/',1)[1];active=False;section='';continue
  m=re.match(r'@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@(.*)',line)
  if m:old,new=int(m[1]),int(m[2]);active=True;hunk=line;continue
  if not active or not line or line[0] not in ' +-':continue
  if line.startswith('-- '):active=False;continue
  sign=line[0];body=line[1:]
  if body.startswith(('%prep','%build','%install','%files','%post','%description','%package')):section=body.split()[0]
  if sign in '+-':
   themes=[];mapping='未对应';why='无可用的逐文件证据把本行映射到本次包增量；不作原因推断'
   if re.search(r'CFLAGS|CXXFLAGS|LDFLAGS|-[Of][A-Za-z0-9=-]+|LINKER|LINK_LLVM|LINK_CLANG|ENABLE_LTO|compiler|linker',body,re.I):themes.append('编译/链接选项')
   if re.search(r'cmake|\s-D[A-Z_]+|CMAKE_',body,re.I):themes.append('cmake 参数')
   if re.search(r'%ifarch|%ifnarch',body):themes.append('%ifarch 条件')
   if section=='%files' or body.startswith('%files'):themes.append('%files 文件列表')
   if re.search(r'debug|DWARF|(?<![\w.])(?:llvm-)?strip(?:\s|$|-)',body,re.I) and 'Strip pre-existing optimization flags' not in body:themes.append('strip/调试信息处理')
   if section=='%install' or (path=='packaging/llvm.spec' and new>=429):themes.append('%install 步骤')
   if re.search(r'Source1005|abidw|abidiff|abicompat|abipkgdiff|kmidiff|localedef|BuildRequires.*dash',body) or path.endswith('llvm-static-archives-native.py'):themes.append('新增/删除工具或工具实现')
   if repo=='qemu-accel':
    if re.search(r'clang|binaries|bindir|localedef|abigail|dash',body):themes.append('工具收录/依赖')
    if re.search(r'compress|payload|xz|zstd|gzip',body,re.I):themes.append('压缩方式')
    if re.search(r'%package|%files|accel.list',body):themes.append('子包划分')
   if path=='packaging/llvm.spec' and re.search(r'LLVM_LINK_LLVM_DYLIB|CLANG_LINK_CLANG_DYLIB',body):
    mapping='链接方式变化';why='参数字面含义对应目标动态库依赖开关；实际逐文件 NEEDED 见 files_compare/elf_detail，不能把每个字节分摊给此单行'
   elif path=='packaging/llvm.spec' and any(t in themes for t in ['编译/链接选项','cmake 参数']) and new<426:
    mapping='代码节变大（选项主题对应，单项效果未对应）';why='存在代码节大小观测，但多个选项及源码共同变化；未隔离任何单项影响'
   elif path.endswith('llvm-static-archives-native.py') or (path=='packaging/llvm.spec' and ('Source1005' in body or new>=429)):
    why='静态归档转换/安装逻辑；llvm-static-devel 不在本轮 RPM 集合，未对应工具 ELF 的体积归因'
   elif path.startswith('packaging/libcxx') or path=='packaging/SOURCE_PROVENANCE':why='libc++ runtimes/来源记录；对应运行库子包不在本轮样本中'
   elif repo=='qemu-accel':why='端点 spec 的 clang 收录、strip、子包分割文本未变化；无匹配按用户机械规则标记 qemu-accel 打包变化，但不能据此归因到此改动'
   rows.append({'repository':repo,'scope':scope,'commit':commit if 'series' in scope else '', 'file':path,'old_line':old if sign=='-' else '', 'new_line':new if sign=='+' else '', 'sign':sign,'text':body,'hunk':hunk,'themes':';'.join(themes) or '其他改动（完整保留）','category_correspondence':mapping,'correspondence_limit':why,'evidence':f'raw/{name}:{ln}'})
  if sign in ' -':old+=1
  if sign in ' +':new+=1
write('source_changes.csv',rows)
write('source_to_categories.csv',[{k:r[k] for k in ['repository','scope','file','old_line','new_line','text','category_correspondence','correspondence_limit','evidence']} for r in rows])
# Full qemu endpoint specs validate that downloaded endpoint diff is not confused with commit messages.
a=(RAW/'qemu-accel_old_armv7l_retry.spec').read_text().splitlines(keepends=True);b=(RAW/'qemu-accel_new_armv7l_retry.spec').read_text().splitlines(keepends=True)
(RAW/'qemu_armv7l_endpoint_spec.diff').write_text(''.join(difflib.unified_diff(a,b,fromfile='old/packaging/qemu-accel-armv7l.spec',tofile='new/packaging/qemu-accel-armv7l.spec')))
# Explicit context citations include unchanged collection and strip rules.
contexts=[]
patterns=[('clang 收录/依赖展开',r'prepare_package_list|ldd \$executable|%\{_bindir\}/(?:clang|opt|lli|llc|llvm|lld|ld.lld)|libLTO|LLVMgold'),('strip',r'strip debug|_rpm_strip_disable'),('压缩',r'PAYLOAD|payload|_binary_payload|_source_payload'),('子包划分',r'%package.*clang|%files.*clang|clang-full.list|comm -13.*clang'),('ELF 修改',r'patchelf|set-interpreter|set-rpath|remove-rpath')]
for side,lines in [('old',a),('new',b)]:
 for i,l in enumerate(lines,1):
  for theme,pat in patterns:
   if re.search(pat,l):contexts.append({'side':side,'theme':theme,'text':l.rstrip('\n'),'evidence':f'raw/qemu-accel_{side}_armv7l_retry.spec:{i}'})
write('source_context.csv',contexts)
facts={'commit_counts':dict((repo,sum(c['repository']==repo and c['direction']=='old..new' for c in commits)) for repo in ['llvm','qemu-accel']),'reverse_qemu_commit_count':sum(c['repository']=='qemu-accel' and c['direction'].startswith('new..old') for c in commits),'source_changed_line_rows':len(rows),'endpoint_changed_lines':dict((repo,sum(r['repository']==repo and r['scope'].startswith('endpoint') for r in rows)) for repo in ['llvm','qemu-accel']),'qemu_armv7l_endpoint_removed_lines':[l[2:].rstrip('\n') for l in difflib.ndiff(a,b) if l.startswith('- ')],'qemu_armv7l_endpoint_added_lines':[l[2:].rstrip('\n') for l in difflib.ndiff(a,b) if l.startswith('+ ')]}
(RAW/'source_analysis.json').write_text(json.dumps(facts,ensure_ascii=False,indent=2)+'\n');print(json.dumps(facts,ensure_ascii=False))
