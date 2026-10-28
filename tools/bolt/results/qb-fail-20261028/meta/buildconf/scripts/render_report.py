from pathlib import Path
import json,re,collections,hashlib,shutil,urllib.parse
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=Path(__file__).resolve().parent;E=B/'tools/bolt/results/qb-fail-20261028/meta/buildconf';prefix='../../tools/bolt/results/qb-fail-20261028/meta/buildconf/'
usage=json.loads((E/'spec-macro-usage.json').read_text());byfile={r['file']:r for r in usage};cov=json.loads((E/'project-spec-coverage.json').read_text());acq=json.loads((E/'spec-acquisition.json').read_text())
errs=[]
for r in acq:
 if r['status']!='ok' or len(r['specs'])!=len(r['header_spec_names']):errs.append(r['srpm'])
 for s in r['specs']:
  p=E/s['file']
  if p.stat().st_size!=s['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=s['sha256']:errs.append(s['file'])
for n in ('git-spec-provenance.json','git-qb-spec-provenance.json'):
 for r in json.loads((E/n).read_text()):
  if r['archive_rc']!=0 or not r['specs']:errs.append(r['project'])
  for s in r['specs']:
   if hashlib.sha256((E/s['path']).read_bytes()).hexdigest()!=s['sha256']:errs.append(s['path'])
assert not errs,errs
assert len([r for r in cov if r['qb_commit']])==251
assert all(r['exact_qb_commit_specs'] for r in cov if r['qb_commit'])
(E/'validation.json').write_text(json.dumps({'srpm_count':len(acq),'header_spec_count_matches':True,'spec_sha_checks':'PASS','examined_spec_records':len(usage),'qb_project_count':251,'qb_projects_with_matching_commit_spec':251,'manifest_count':245,'union_project_count':252,'missing_projects':[],'no_build_or_spec_execution':True},indent=2)+'\n')
raw=[];table=[];projectrows=[]
legend='''名单有三个不同口径，不能混称：当前Toolchain `manifest.xml` **245个源码仓库**；1211018日志L136/278/417/5737的四份相同`build_pkg_list_dic`为**251个实际调度仓库**；两者并集252个，额外的tensorflow2只在当前manifest内、该次实际列表没有。旧固定Toolchain快照的source索引有**365份SRPM、256个源码包名**（同包可能多个release，且源码包名不一定等于仓库名）。\n
来源：[manifest原文](PREFIXtoolchain-manifest.xml)、[manifest解析](PREFIXmanifest-projects.json)、[QB实际名单及原日志行号](PREFIX1211018-package-lists.json)、[快照source目录原HTML](PREFIXsource-index-1.html)、[完整365份列表](PREFIXsrpm-list.txt)。已顺序读取全部365份SRPM，保存其中所有spec，数量与RPM头的spec名单吻合、文件大小/SHA复核全PASS。[每份URL/大小/压缩方式/spec SHA](PREFIXspec-acquisition.json)。这只提取spec，不运行包内脚本；为避免下载大量源码，在全部spec读完后终止流，**download_prefix_sha256不是完整SRPM SHA**。\n
快照优先；缺少对应包或快照VCS不是QB所用提交时，再只读取Gerrit `tizen_base`/日志提交的packaging归档。最终251个实际仓库都有与QB提交号匹配的spec证据，tensorflow2有快照spec；[逐仓库提交与spec覆盖](PREFIXproject-spec-coverage.json)、[分支获取](PREFIXgit-spec-provenance.json)、[按QB精确提交获取](PREFIXgit-qb-spec-provenance.json)。分支头查询与archive分开记录，不把branch查询SHA冒充服务端tar内置签名；最终实际名单的匹配不依赖这六个分支读取的时间窗口，另按明确提交号取得了spec。\n
全量逐行搜索包括31个变化宏、间接消费变量及段入口，保留注释标记和上下文：[spec-macro-usage.tsv](PREFIXspec-macro-usage.tsv)、[JSON](PREFIXspec-macro-usage.json)、[全部源码包版本影响表](PREFIXpackage-impact.tsv)。下表按仓库逐项列出（同一仓库多份spec时全部合并），优先该次QB提交；原始快照的额外/旧包版本仍包含在上述全量表中。\n
影响代号是**直接替换build.conf的静态条件推导**，不是编译结果；A方案继承这些变化，B/C若恢复完整有效Toolchain配置则消除这些配置变化（仍有Base依赖包版本变化），D改回旧依赖来源：\n
- **H**：表中列出的prep/build/install入口不再有Toolchain的AR/RANLIB、CC/CXX export；install入口的debug_package插入也消失。是否最终产生debug子包还取决于平台与spec，不武断地说每个包都关debug。\n- **F**：直接消费optflags或CFLAGS/CXXFLAGS/RPM_OPT_FLAGS，默认Clang -Os选项链变为Base GCC -O2链；包自行覆盖的最终值须另核对。\n- **T**：直接使用__cc/__cxx/__ar/__ranlib宏，工具分派/拼写可能变化。\n- **G**：指定_toolchain_override gcc；旧条件已经选GCC，Base也默认GCC，不是必然换编译器，仍需核对工具名/flags。\n- **L**：直接消费build_ldflags，项目定义消失，须检查平台或包本身是否补定义，不能保证链接flags相同。\n- **X**：有包专属_toolchain/toolchain_is分支，见下一张原文表及LLVM小节。\n- **M**：MLGO宏有自身默认；不能把配置宏消失说成MLGO必然关闭。\n- **E**：所有项目均面对Required/Support/预安装/依赖版本/发行版标识变化。即使只有noarch脚本或无直接命中，也不能据此证明RPM相同。\n
段入口列P/B/I分别为prep/build/install；“—”表示所查spec无该类直接命中。链接后的`L`是保留spec的原行号，所有命中全文在TSV/JSON。\n
| 包/源码仓库（来源） | 变化宏直接命中；间接消费 | 段入口 | 两配置下的影响 | spec原文/行号 |
|---|---|---|---|---|
'''.replace('PREFIX',prefix)
for c in cov:
 selected=c['exact_qb_commit_specs'] or c['available_specs']
 # Prefer immutable exact archive over branch read; retain distinct spec basenames.
 selected=sorted(selected,key=lambda x:(x['source']=='Gerrit exact QB commit',x['source']=='local immutable Git object'))
 chosen={Path(s['file']).name:s for s in selected}
 rs=[byfile[s['file']] for s in chosen.values()]
 direct=sorted(set().union(*(set(r['changed_direct']) for r in rs)));indirect=sorted(set().union(*(set(r['indirect']) for r in rs)));hooks=sorted(set().union(*(set(r['hooks']) for r in rs)));codes=['E']
 if hooks:codes.append('H')
 if set(indirect)&{'optflags','CFLAGS','CXXFLAGS','RPM_OPT_FLAGS'}:codes.append('F')
 if set(direct)&{'__cc','__cxx','__ar','__ranlib'}:codes.append('T')
 if '_toolchain_override' in indirect:codes.append('G' if c['project'].split('/')[-1].startswith('gcc') or c['project'].endswith('/glibc') else 'X')
 if 'build_ldflags' in direct:codes.append('L')
 if set(direct)&{'_toolchain','toolchain_is'}:codes.append('X')
 if set(direct)&{'_with_mlgo','mlgo_build_jobs','mlgo_verify_configure_only'}:codes.append('M')
 codes=list(dict.fromkeys(codes));evidence=[]
 for r in rs:
  hits=[h for h in r['hits'] if not h['comment']];nums=[h['line'] for h in hits];label=Path(r['file']).name
  key=next((h['line'] for h in hits if set(h['macros'])&set(direct)),nums[0] if nums else 1)
  evidence.append('['+label+']('+prefix+urllib.parse.quote(r['file'],safe='/')+'#L'+str(key)+') L'+','.join(map(str,nums)))
 name=c['project'];source='QB' if c['qb_commit'] else '仅manifest';tokens=', '.join('`'+n+'`' for n in direct) or '—';other=', '.join(indirect) or '—'
 table.append('| '+name+'（'+source+'） | '+tokens+'；'+other+' | '+('/'.join({'prep':'P','build':'B','install':'I'}[h] for h in hooks) or '—')+' | '+','.join(codes)+' | '+'；'.join(evidence)+' |')
 projectrows.append(dict(project=name,qb_commit=c['qb_commit'],source=source,direct=direct,indirect=indirect,hooks=hooks,effects=codes,specs=[r['file'] for r in rs]))
(E/'project-impact.json').write_text(json.dumps(projectrows,indent=2,ensure_ascii=False)+'\n')
critical=['iptables','kmod','readline','sed','xmlstarlet','xz','toybox','gcc','glibc','xxhash']
for name in critical:
 rs=[r for r in usage if r['package']==name]
 if not rs:continue
 r=rs[-1];ls=(E/r['file']).read_text().splitlines();selected=set()
 for h in r['hits']:
  if set(h['macros'])&{'_toolchain','toolchain_is','_toolchain_override','build_ldflags'}:selected.update(range(max(0,h['line']-2),min(len(ls),h['line']+5)))
 raw.append('\n### '+r['file']+'\n'+'\n'.join(f'{i+1}: {ls[i]}' for i in sorted(selected)))
(E/'critical-spec-excerpts.txt').write_text('\n'.join(raw)+'\n')
criticaldoc='''
\n直接分支原文与后果（[完整上下文摘录](PREFIXcritical-spec-excerpts.txt)，每段注明具体spec文件）：

| 包 | 原文和行号 | 直接使用Base配置后的差异 |
|---|---|---|
| iptables | L80–84 `%{?_toolchain:` / `%if %{toolchain_is clang}` / sed删除`-Wno-stringop-truncation` | 外层变假，跳过Clang参数清理；不是宏解析失败 |
| kmod | L102–106 `%{?_toolchain:` / `%if !%{toolchain_is clang}` / `CFLAGS+=" -Wno-maybe-uninitialized"` | 旧默认Clang与新Base都不加这项；若旧选GCC override则分支有差异。编译器选择仍有变化 |
| readline | L128–133 `defined _toolchain` / `toolchain_is gcc` / else加`-ftree-loop-linear` | 默认Clang分支原不加；无_toolchain的Base分支加GCC选项 |
| sed | L16–20条件BuildRequires compiler-rt；L50–63 Clang运行`llvm-profdata merge`，else用普通反馈宏 | compiler-rt不再由此条件引入；do_profiling启用时切换反馈数据/命令；有外层保护 |
| xz | L18–22条件compiler-rt；L103–115 Clang的LLVM_PROFILE_FILE/llvm-profdata与else反馈目录 | 同样改变依赖和启用PGO时的工作流；有外层保护 |
| xmlstarlet | L29–33 `_toolchain`保护下加`-Wno-error=incompatible-function-pointer-types` | 新配置跳过Clang专用警告参数；不直接解析失败 |
| toybox | L100–102 `%{?!_toolchain:` / `export CC="gcc"` | 最小动态toybox显式选择GCC，不再继承原Clang环境 |
| GCC原生/交叉、glibc | gcc L30 / glibc L36 `_toolchain_override gcc` | 原来也选择GCC；不能断言这些包因Base配置改成不同编译器家族。需比较宏工具拼写/选项 |
| LLVM | f308 L18–37、198–207 | release开关、debug子包、去-g和debug目录清理定义发生变化，详见7.1 |

LLVM L13–16已经在三架构使用`%bcond_without mlgo`，L63–64自备jobs=6与verify=0默认值。因此配置删除三项MLGO宏，**不等于该LLVM spec必定关闭MLGO或改jobs**；但旧配置 `_with_mlgo`还参与全局Clang选项选择，完整链仍需核验。

31个变化宏的覆盖统计（数量是spec记录/版本而非唯一项目；0表示无直接语法引用，不表示没有宏内部或平台间接依赖）：

| 宏 | 命中spec记录数（包含注释外的段入口） |
|---|---|
'''.replace('PREFIX',prefix)
changed=json.loads((E/'config-classification.json').read_text())['changed_macro_names']
for n in changed:
 count=sum(any(not h['comment'] and n in h['macros'] for h in r['hits']) for r in usage)
 criticaldoc+='| `'+n+'` | '+str(count)+' |\n'
body=(D/'report-body.md').read_text().replace('<!-- PACKAGE_INVENTORY -->',legend+'\n'.join(table)+'\n'+criticaldoc)
body=body.replace('没有启动gbs export、环境准备或完整构建','没有启动新的gbs export、构建根环境准备或完整构建')
p=B/'docs/bolt/45_qb_meta_fix_and_snapshot.md';saved=D/'docs45-before-buildconf.md'
if not saved.exists():saved.write_bytes(p.read_bytes())
s=saved.read_text();start=s.index('\n\n')+2;end=s.index('\n\n## 1.')
s=s[:start]+'''两份build.conf不只是少了`_toolchain`：还改变编译器选择、默认优化参数、段入口环境、调试包插入和基础依赖。LLVM会改走release分支，sed/xz的PGO、readline/toybox等包也有明确分支变化；全部251个QB实际仓库已找到匹配提交的spec，但NGBS最终是否合并项目配置仍没有日志证据。推荐保留Toolchain自己的完整编译配置、仅让RPM依赖来自Tizen-Base，先确认配置装配机制，不能只给LLVM补一个宏；debuglink完整构建按用户要求暂停。'''+s[end:]
s=s.replace('第三件将在x86_64+BOLT条件内显式BuildRequires elfutils。','此前第三件的本地草稿在x86_64+BOLT条件内显式BuildRequires elfutils；现在暂停，未作新构建认证。')
a=s.index('**需裁决的冲突**');b=s.index('\n\n## 5.',a)
s=s[:a]+'''**已收到用户裁决**：暂停第三件，不采用仅本地补`_toolchain`来继续构建。对两份build.conf直接替换而言，LLVM入口分支会改变；但NGBS还有项目配置生成步骤，不能把下载地址等同最终RPM宏。第6–10节补全项目级调查、逐包影响和推荐方案，取代此前等待单包宏授权的状态。'''+s[b:]
a=s.index('工具链不同：第三件采用');s=s[:a]+'''工具链不同，后续不能继承39号精确clang SHA验收。第一件本地meta提交保留且不推送；第二件快照差异已确认。第三件本地草稿保留、完整构建暂停，未产生新RPM，不把函数级符号实验或配置下载称为打包验证通过。
'''+body
p.write_text(s)
print('rendered',len(table),'project rows;',len(usage),'spec records;',len(s.encode()),'bytes')
