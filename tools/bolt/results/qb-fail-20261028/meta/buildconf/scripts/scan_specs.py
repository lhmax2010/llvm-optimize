from pathlib import Path
import json,re,collections,tarfile
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';E=B/'tools/bolt/results/qb-fail-20261028/meta/buildconf';D=Path(__file__).resolve().parent
config=json.loads((E/'config-classification.json').read_text());changed=config['changed_macro_names'];names=sorted(set(config['indirect_search_names']+['RPM_OPT_FLAGS']));hooks={'prep','build','install'}
rows=[];files=[]
for prov in sorted((E/'specs').glob('*/provenance.json')):
 row=json.loads(prov.read_text())
 for spec in row['specs']:
  files.append({'package':row['srpm'].rsplit('-',2)[0],'version':row['srpm'],'source':'snapshot SRPM','url':row['url'],'file':spec['file'],'sha256':spec['sha256']})
for row in json.loads((E/'git-spec-provenance.json').read_text()):
 t=D/(row['project'].replace('/','__')+'.tar')
 if row['archive_rc']==0:
  with tarfile.open(t) as tar: row['archive_commit']=tar.pax_headers.get('comment')
 for spec in row['specs']:files.append({'package':row['project'],'version':row['ls_remote'].split()[0],'source':'Gerrit tizen_base fallback','url':row['url'],'file':spec['path'],'sha256':spec['sha256'],'archive_commit':row.get('archive_commit')})
for row in json.loads((E/'git-qb-spec-provenance.json').read_text()):
 for spec in row['specs']:
  files.append({'package':row['project'],'version':row['requested_commit'],'source':'Gerrit exact QB commit','url':row['url'],'file':spec['path'],'sha256':spec['sha256']})
# Also inspect the actually requested LLVM commit, separately from the old snapshot recipe.
f308=E/'llvm-f308fe08.spec'
if not f308.exists():
 import subprocess
 f308.write_bytes(subprocess.check_output(['git','-C',str(W/'temp/oldtext-final-20261027/source'),'show','f308fe08:packaging/llvm.spec']))
files.append({'package':'llvm@f308fe08 (QB request)','version':'f308fe08eeaad4e219f8505449b88bd5f644ea8c','source':'local immutable Git object','file':f308.name})
for row in files:
 lines=(E/row['file']).read_text(errors='replace').splitlines();hits=[];section='preamble'
 for i,line in enumerate(lines):
  if re.match(r'^%(prep|build|install|check|files|package|description|post|pre)\b',line):section=line.split()[0]
  found=[]
  for n in names:
   token=r'(?<![A-Za-z0-9_])'+re.escape(n)+r'(?![A-Za-z0-9_])'
   macro=(re.search(r'%\{[^}\n]*'+token+r'[^}]*',line) or re.search(r'%'+re.escape(n)+r'(?![A-Za-z0-9_])',line) or re.search(r'%(?:define|global|undefine)\s+'+re.escape(n)+r'(?![A-Za-z0-9_])',line))
   shell=(n in ('CC','CXX','AR','RANLIB','CFLAGS','CXXFLAGS','LDFLAGS','RPM_OPT_FLAGS') and re.search(token,line))
   if macro or shell: found.append(n)
  if found:hits.append({'line':i+1,'macros':found,'text':line,'section':section,'comment':line.lstrip().startswith('#')})
 row['hits']=hits;row['changed_direct']=sorted({n for hit in hits if not hit['comment'] for n in hit['macros'] if n in changed and n not in hooks});row['indirect']=sorted({n for hit in hits if not hit['comment'] for n in hit['macros'] if n not in changed});row['hooks']=sorted({n for hit in hits if not hit['comment'] for n in hit['macros'] if n in hooks and re.match(r'^%'+n+r'\b',hit['text'])});rows.append(row)
(E/'spec-macro-usage.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
with (E/'spec-macro-usage.tsv').open('w') as f:
 f.write('package\tversion\tfile\tline\tmacros\tcomment\ttext\n')
 for row in rows:
  for hit in row['hits']:f.write('\t'.join([row['package'],row['version'],row['file'],str(hit['line']),','.join(hit['macros']),str(hit['comment']),hit['text'].replace('\t',' ')])+'\n')
groups=collections.defaultdict(list)
for row in rows:groups[row['package']].append(row)
summary=[]
for package,rs in sorted(groups.items()):
 short=package.rsplit('/',1)[-1]
 direct=sorted(set().union(*(set(r['changed_direct']) for r in rs)));indirect=sorted(set().union(*(set(r['indirect']) for r in rs)));hook=sorted(set().union(*(set(r['hooks']) for r in rs)))
 effects=[]
 if short=='toybox':effects.append('无_toolchain分支显式export CC=gcc，最小动态toybox不再继承Clang')
 if '_toolchain' in direct:effects.append('直接检查/设定_toolchain；原条件分支可能改变，详见逐行命中')
 if 'toolchain_is' in direct:
  if short=='iptables':effects.append('_toolchain外层保护使Clang专用参数清理跳过；不是直接触发宏解析错误')
  elif short=='kmod':effects.append('GCC专用-Wno-maybe-uninitialized分支受_toolchain外层保护；旧默认Clang和新Base均不加该项，旧GCC override时才存在差异')
  elif short in ('sed','xz'):effects.append('有外层保护：取消compiler-rt条件BuildRequires；do_profiling启用时从Clang profraw/llvm-profdata切到非Clang反馈路径')
  elif short=='readline':effects.append('有defined保护：从默认Clang跳过变为无_toolchain时加入-ftree-loop-linear')
  elif short=='xmlstarlet':effects.append('有_toolchain外层保护：跳过Clang专用-Wno-error=incompatible-function-pointer-types；不直接解析失败')
  else:effects.append('toolchain_is定义消失；须结合外层保护判断是否解析失败')
 if '_toolchain_override' in indirect:
  if short=='glibc' or short.startswith('gcc'):effects.append('原spec指定GCC覆盖；Base也默认GCC，不能说必然换编译器；工具拼写/flags仍需比对')
  else:effects.append('_toolchain_override失去全局选择器；若无自行导出则覆盖失效')
 if set(direct)&{'__ar','__ranlib','__cc','__cxx'}:effects.append('直接调用工具宏：Clang/LLVM工具选择不再由Toolchain宏保证')
 if set(direct)&{'_with_mlgo','mlgo_build_jobs','mlgo_verify_configure_only'}:effects.append('MLGO默认宏/条件变化，须区分spec自身默认值')
 if 'build_ldflags' in direct:effects.append('build_ldflags快照定义消失；平台默认/包自定义决定最终链接参数')
 if 'optflags' in indirect or any(n.startswith('__optflags') or n.startswith('___optflags') for n in direct):effects.append('继承选项由Clang -Os链转Base -O2/GCC链，架构选项也变')
 if hook:effects.append('prep/build/install入口不再自动export AR/RANLIB/CC/CXX；install的debug宏插入也取消')
 if not effects:effects=['未见直接差异宏/段入口；仍可能受依赖包和平台默认选项影响，不能断言二进制相同']
 summary.append({'package':package,'spec_variants':len(rs),'unique_spec_sha':len(set(r.get('sha256','') for r in rs)),'direct_macros':direct,'indirect_names':indirect,'hooks':hook,'effects':effects,'evidence':[dict(file=r['file'],version=r['version'],lines=[h['line'] for h in r['hits'] if not h['comment']]) for r in rs]})
(E/'package-impact.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
with (E/'package-impact.tsv').open('w') as f:
 f.write('package\tspec_variants\tchanged_macros\tindirect\tsection_hooks\tstatic_impact\tspec_files\n')
 for r in summary:f.write('\t'.join([r['package'],str(r['spec_variants']),','.join(r['direct_macros']),','.join(r['indirect_names']),','.join(r['hooks']),'；'.join(r['effects']),';'.join(x['file'] for x in r['evidence'])])+'\n')
(E/'macro-coverage.json').write_text(json.dumps({n:[r['package'] for r in summary if n in r['direct_macros'] or n in r['hooks']] for n in changed},indent=2)+'\n')
print('spec variants',len(rows),'package groups',len(summary),'direct toolchain groups',[r['package'] for r in summary if '_toolchain' in r['direct_macros']]);print('toolchain_is',[r['package'] for r in summary if 'toolchain_is' in r['direct_macros']])
