"""Render review report from CSV/raw evidence. All sizes are exact bytes."""
from common import *
import csv,re

def rows(name):return list(csv.DictReader((OUT/name).open()))
def ev(ref):
 # Keep line ranges visible; GitHub line anchors point to the first line.
 m=re.match(r'(raw/[^:]+):(\d+(?:-\d+)?)',ref)
 return f'[{m[1]}:{m[2]}]({m[1]}#L{m[2].split("-")[0]})' if m else ref

def n(v):return f'{int(v):,}'
summary=rows('package_summary.csv');cats=rows('category_summary.csv');files=rows('files_compare.csv');top=rows('top30_files.csv');elf=rows('elf_detail.csv');commits=rows('source_commits.csv');members=rows('category_membership.csv')
out=[]
def add(s=''):out.append(s)
def table(headers,data):
 add('| '+' | '.join(headers)+' |');add('| '+' | '.join('---' for _ in headers)+' |')
 for row in data:add('| '+' | '.join(str(x).replace('|','\\|').replace('\n',' ') for x in row)+' |')
 add()
add('# Tizen Base LLVM / clang-accel RPM 体积事实与逐文件证据')
add()
add('对象：基线 `tizen-base-toolchain_20260914.073422` 与优化快照 `tizen-base-toolchain_20261015.022255`。本文中的“旧/新”只表示这两个快照。快照、实际包版本、下载 URL、SHA256、RPM payload 元数据见 [rpm_metadata.csv](rpm_metadata.csv)，原始下载记录为 '+ev('raw/fetch_manifest.jsonl:1')+' 起。')
add()
add('x86_64 clang、llvm 和 llvm-devel 的主要文件增量落在满足“旧版依赖 libLLVM/libclang-cpp，新版不再依赖对应库”规则的 ELF 上。clang-accel 中大部分文件与指定来源 RPM 不同 SHA256，必须保留为“无匹配”；qemu-accel 两端源码的 clang 收录和 strip 规则未变化。下面给出机械分类和逐项证据，不把多个编译选项、不同源码提交或打包处理的作用分摊为未经验证的因果比例。')
add()
add('## 采集范围和计量口径')
add()
add('工作目录采用用户已确认的当前工作区 `/home/toolchain/Desktop/tmp_hfy/qb_analysis/llvm-optimize`。开始前 temp 所在磁盘可用 **213,247,823,872 bytes**，记录在 '+ev('raw/preflight.txt:1-6')+'。本轮 RPM 和解包内容仅放 `temp/qb_size/`，每个包依次下载、解包、记录，再删除该包解包目录。没有编译、安装 RPM、执行产品脚本、修改产品代码或提交 Gerrit。')
add()
add('采集覆盖用户指定的全部 RPM；下载与解包串行，源码下载同时最多两路，总下载并发未超过用户上限。采集服务 CPU 配额为单核的 25%，MemoryMax 为 768 MiB；配置原文及成功退出状态见 '+ev('raw/package_resource_limits.txt:1')+' 起，逐包完成/删除记录见 '+ev('raw/package_collection_journal.txt:1')+' 起。')
add()
add('本文所有大小均为 bytes，不把目录网页四舍五入的 MB 用作计算输入。`rpm_bytes` 是下载到的压缩 RPM 文件大小；`path_bytes` 是全部路径的 regular 文件长度加符号链接文本长度，目录记零。对缺失路径，差值计算用零，同时明确标记“仅旧有/仅新有”，不把零当成已取得的文件。每个 regular 文件 SHA256 与 RPM 头中 FILEDIGESTS 一致，解包大小与 FILESIZES 一致；按路径和按物理 regular 文件去重的合计相同。核验见 '+ev('raw/validation.json:1-12')+' 和各包 `*_complete.json`。')
add()
add('压缩流无法按单个文件无损分摊为 RPM 增量。因此以下分类占比的分母固定为**解包路径大小净增量**，不是 RPM 压缩增量。没有给出压缩后各类字节的估算；该项为“未获取：RPM 使用整体 payload 压缩，现有证据不能提供逐文件压缩贡献”。')
add()
add('## RPM 总量、版本和压缩格式')
add()
table(['架构 / 包','旧 RPM','新 RPM','RPM 增量','旧路径总量','新路径总量','路径净增量','raw 证据'],[[s['arch']+' / '+s['package'],n(s['old_rpm_bytes']),n(s['new_rpm_bytes']),n(s['rpm_delta_bytes']),n(s['old_path_bytes']),n(s['new_path_bytes']),n(s['path_delta_bytes']),ev(s['derived_evidence'])] for s in summary])
add('精确版本：旧 x86_64 LLVM 系列为 `22.1.8-1.6`，旧 armv7l clang/llvm 为 `22.1.8-1.7`；新 LLVM 系列为 `22.1.8-3.1`。clang-accel 为旧 `0.4-1.1`、新 `0.4-2.2`。每个包分别可查 `raw/{old,new}_{arch}_{package}_rpm_header.txt:1-6`，例如 '+ev('raw/old_x86_64_clang_rpm_header.txt:1-6')+'、'+ev('raw/old_armv7l_clang_rpm_header.txt:1-6')+'、'+ev('raw/new_armv7l_clang-accel-x86_64-armv7l_rpm_header.txt:1-6')+'。')
add()
add('全部 **14** 个 RPM 的 `PAYLOADCOMPRESSOR=xz`、`PAYLOADFLAGS=5T`，未观察到压缩格式或该头字段标志变化；逐包原文在 header 文件第 5–6 行，合计见 '+ev('raw/coverage_facts.jsonl:47')+'。相同格式不代表相同压缩率。armv7l clang/llvm 的 RPM 增大而解包文件总量减少，两个口径都保留在上表。')
add()
add('## 源码提交、完整 diff 和对应范围')
add()
add('LLVM 精确区间 `8dfebafe1a477b3dcc678ee4cb18a3a4306d5a7c..67619ec8bbbac7238a6cfc33a481ccfbcd12206f` 的全部提交如下。作者按原始历史记录保留，日期为 author date；CSV 另列 cgit 页面中的 committer date。')
add()
table(['提交','原始作者','作者日期','标题','raw 证据'],[[c['commit'],c['author'],c['author_date'],c['title'],ev(c['evidence'])+('<br>'+ev(c['log_evidence']) if c.get('log_evidence') else '')] for c in commits if c['repository']=='llvm'])
add('完整最终 packaging diff 为 [raw/llvm_packaging_complete.diff](raw/llvm_packaging_complete.diff)，逐字节筛自 [raw/llvm_full.diff](raw/llvm_full.diff) 的全部 `packaging/` diff 块；来源说明见 '+ev('raw/derived_source_provenance.txt:1')+'。完整提交补丁序列另存 [raw/llvm_range.patch](raw/llvm_range.patch)。')
add()
add('qemu-accel 正向 `e01aa7250a1a73aa8f88ba9ac4a05cbc954d1c9f..2737f3bf78ed33be4333114c0e5c741a1deca467` 与补充的反向提交集合均列出，防止把正向提交标题误认为端点树差异：')
add()
table(['方向','提交','作者','作者日期','标题','raw 证据'],[[c['direction'],c['commit'],c['author'],c['author_date'],c['title'],ev(c['evidence'])] for c in commits if c['repository']=='qemu-accel'])
add('qemu-accel 的完整端点 diff 为 [raw/qemu-accel_full_retry.diff](raw/qemu-accel_full_retry.diff)：各架构 spec 及模板仅删除 `BuildRequires:  dash`。两端完整 armv7l spec 独立作文本 diff 得到同一行删除，见 '+ev('raw/qemu_armv7l_endpoint_spec.diff:1-10')+'。正向 `2737f3bf` 与反向 `06b28703` 均包含 libabigail 增补，不能把这批工具当作两个快照之间的新增工具。')
add()
add('[source_changes.csv](source_changes.csv) 保存最终 diff 和提交序列中**每条增删行**的文件、原/新行号、原文、主题及 raw 行号；不是只保留关键词命中的摘要。`scope=endpoint_*` 是最终差异，`commit_series` 是途中改动，不能重复计数。[source_to_categories.csv](source_to_categories.csv) 对每条记录给出分类主题对应或“未对应”及限制。')
add()
table(['源码位置 / 原文','可对应的观测类别','限制 / raw 证据'],[
 ['`llvm.spec`: `-DLLVM_LINK_LLVM_DYLIB=OFF`、`-DCLANG_LINK_CLANG_DYLIB=OFF`，在 `%ifarch x86_64` 中','链接方式变化','目标库依赖变化逐文件核对；'+ev('raw/llvm_new_llvm.spec:279-289')],
 ['`llvm.spec`: C/CXX flags 清除既有选项并追加 `-O3 -flto=thin -fomit-frame-pointer`；显式 clang/clang++','代码节变大（只作选项主题对应）','多个选项及源码同时变化，单项效果未对应；'+ev('raw/llvm_new_llvm.spec:200-243')],
 ['`llvm.spec`: 链接 flags 增加 ThinLTO、`LLVM_ENABLE_LTO=Thin`、llvm-ar/ranlib','代码节变大（只作选项主题对应）','条件是 `%if %{defined _toolchain}`，不能概括为仅 x86_64；'+ev('raw/llvm_new_llvm.spec:250-257')],
 ['新增 `llvm-static-archives-native.py`，x86_64 `%install` 调用，保留 archive strip -g','未对应','处理静态归档，本轮没有 llvm-static-devel 样本；不能分配到工具 ELF 增量；'+ev('raw/llvm_packaging_complete.diff:240-245')+'、'+ev('raw/llvm_new_llvm.spec:429-441')],
 ['新增 libcxx-runtimes.spec、manifest、map 和来源记录；运行库编译器改动','未对应','运行库子包不在本轮 RPM 集合；'+ev('raw/llvm_packaging_complete.diff:1-239')],
 ['qemu-accel 最终差异仅删除 dash 构建依赖','未对应','未取得将该依赖删除对应到任一目标文件增量的证据；'+ev('raw/qemu-accel_full_retry.diff:1-48')],
 ['qemu-accel 的 clang 文件列表、strip、压缩、子包划分','最终 diff 未变化 / 未对应新增源码改动','完整端点 spec 与全文 diff 可复查；上下文逐行索引见 [source_context.csv](source_context.csv)']])
add('LLVM 主 `packaging/llvm.spec` 的 `%files` 列表在端点 diff 中没有改动；新增运行库 spec 自带 `%files`，已经完整纳入逐行表。没有把“源码中新建打包脚本”当作“RPM 中新增文件”。')
add()
add('## 逐文件增量和 ELF 明细')
add()
add('[files_compare.csv](files_compare.csv) 是全部包按完整路径配对的结果，包含旧/新大小、差值、存在性、类型、SHA256、分类和原始行号。[top30_files.csv](top30_files.csv) 对每个包按差值降序、路径字典序打破同值排序，保留前 30 个非目录路径；少于 30 个时全部列出，零值和负值没有伪造为增长。')
add()
add('以下是每包最大增量的实际路径，完整排行见 CSV：')
add()
table(['架构 / 包','路径','旧大小','新大小','差值','raw 证据'],[[r['arch']+' / '+r['package'],'`'+r['path']+'`',n(r['old_size']),n(r['new_size']),n(r['delta_bytes']),ev(r['old_evidence'])+'<br>'+ev(r['new_evidence'])] for r in top if int(r['rank'])<=3])
add('[elf_detail.csv](elf_detail.csv) 包含 x86_64 clang 的全部 **24** 个 ELF（不足所要求上限）、llvm 增量最大的 **30** 个 ELF，两版分别列出；另加 libLLVM 对照。选择数量与 strip/build-id 检查见 '+ev('raw/coverage_facts.jsonl:45-46')+'。字段包括完整 NEEDED、目标库标志、`.symtab`、所有 `.debug_*`/`.zdebug_*`、指定节大小、build-id，以及 raw readelf 行号。[elf_sections.csv](elf_sections.csv) 把这些 ELF 的全部节逐节列出。[elf_all.csv](elf_all.csv) 保留整个样本中的 ELF 字段，支持核对排行外的分类。')
add()
add('例如 `/usr/bin/clang-22`：旧版 NEEDED 包含 `libclang-cpp.so.22.1` 和 `libLLVM.so.22.1`；新版 NEEDED 不含这两个名称，仍有其他共享库依赖。不能把“不依赖这两个库”写成“整个程序完全静态链接”。证据：'+ev('raw/elf/old_x86_64_clang/00005.txt:78-86')+'、'+ev('raw/elf/new_x86_64_clang/00005.txt:81-91')+'。')
add()
add('整个样本的 **646** 个 regular ELF 观测中，`.symtab` 和 `.debug_*`/`.zdebug_*` 均未出现；按本任务定义没有 strip/调试节“有无”变化。`.dynsym` 与 `.gnu_debuglink` 不当作 `.symtab` 或 DWARF 调试节。合计证据：'+ev('raw/coverage_facts.jsonl:48')+'，逐对象 `readelf -S` 原文可由 `elf_all.csv` 追溯。所选排行 ELF 与 libLLVM 对照的 build-id 均为**未获取：readelf -n 没有列出 Build ID**，并非下载失败；每个 CSV 行附对应 note 输出位置。')
add()
add('## libLLVM.so.22.1 动态库对照')
add()
control=[r for r in elf if r['selection']=='libLLVM_control'];a,b=sorted(control,key=lambda r:0 if r['side']=='old' else 1)
table(['字段','旧','新','差值 / 状态','raw 证据'],[
 ['文件大小',n(a['size']),n(b['size']),n(int(b['size'])-int(a['size'])),ev(a['inventory_evidence'])+'<br>'+ev(b['inventory_evidence'])],
 *[[s,n(a[s+'_bytes']),n(b[s+'_bytes']),n(int(b[s+'_bytes'])-int(a[s+'_bytes'])),ev(a[s+'_evidence'])+'<br>'+ev(b[s+'_evidence'])] for s in ['.text','.rodata','.data.rel.ro','.eh_frame']],
 ['`.symtab` / 调试节','均无','均无','无有无变化',ev('raw/elf/old_x86_64_libllvm/00003.txt:26-65')+'<br>'+ev('raw/elf/new_x86_64_libllvm/00003.txt:26-65')],
 ['build-id','未获取','未获取','两版 note 输出未列出',ev('raw/elf/old_x86_64_libllvm/00003.txt:116-120')+'<br>'+ev('raw/elf/new_x86_64_libllvm/00003.txt:116-120')]])
add('两版均为 `DYN (Shared object file)`，完整 NEEDED 集合相同：`'+a['needed'].replace(';','`, `')+'`。证据：'+ev('raw/elf/old_x86_64_libllvm/00003.txt:8-10')+'、'+ev('raw/elf/new_x86_64_libllvm/00003.txt:8-10')+'、'+ev('raw/elf/old_x86_64_libllvm/00003.txt:77-85')+'、'+ev('raw/elf/new_x86_64_libllvm/00003.txt:77-85')+'。这是动态库体积/节大小的端点观测；没有单独改变一个优化选项的对照实验，不能从本表分离 O3、ThinLTO 或其它改动各自的作用。')
add()
add('## clang-accel 收录和来源核对')
add()
add('匹配集合严格使用**同一快照 x86_64 clang、llvm、libllvm RPM**，普通文件以完整字节 SHA256 查找所有匹配路径。[clang_accel_sources.csv](clang_accel_sources.csv) 包含每个路径、类型、大小、SHA、所有来源匹配或“无匹配”。符号链接单独按链接文本 SHA256 核对，明确标为“链接文本匹配（非文件内容匹配）”；目录没有文件内容哈希。`llvm-devel` 等不属于用户指定的来源匹配集合，没有用它们补造匹配。')
add()
table(['快照','regular 文件数','原样匹配数 / bytes','无匹配数 / bytes','raw 合计证据'],[
 ['旧','107','2 / 146,346,256','105 / 93,565,744',ev('raw/coverage_facts.jsonl:43')],
 ['新','105','0 / 0','105 / 2,756,647,328',ev('raw/coverage_facts.jsonl:44')]])
add('旧版的两项原样匹配为 `/emul/usr/lib64/libLLVM.so.22.1`（来自 libllvm）和 `/emul/usr/lib64/libclang-cpp.so.22.1`（来自 clang）；新版均未收录。对应原文：'+ev('raw/old_armv7l_clang-accel-x86_64-armv7l_files.jsonl:113')+'、'+ev('raw/old_x86_64_libllvm_files.jsonl:3')+'、'+ev('raw/old_armv7l_clang-accel-x86_64-armv7l_files.jsonl:116')+'、'+ev('raw/old_x86_64_clang_files.jsonl:355')+'；新完整列表见 '+ev('raw/new_armv7l_clang-accel-x86_64-armv7l_files.jsonl:1-117')+'。两项移除合计 **−146,346,256 bytes**，共同路径净增加 **2,663,081,584 bytes**，合为包路径净增加 **2,516,735,328 bytes**；合计见 '+ev('raw/analysis_facts.jsonl:10-13')+'。')
add()
add('全部无匹配路径和大小单独列于 [clang_accel_unmatched.csv](clang_accel_unmatched.csv)。无匹配只证明指定集合内没有相同完整文件 SHA，不能证明该文件没有来源于这些 RPM，也不能证明 qemu-accel 源码新增了打包处理。完整 spec 已有 `cp -aL`、修改 interpreter、条件修改 RUNPATH 的逻辑，旧/新文本相同：'+ev('raw/qemu-accel_old_armv7l_retry.spec:383-400')+'、'+ev('raw/qemu-accel_new_armv7l_retry.spec:382-399')+'。本轮没有修改文件再试图反推 SHA。')
add()
add('两端 spec 同样调用 `prepare_package_list clang` 收录 clang-*、clang++、opt、lli、llc、llvm-*、lld、ld.lld、libLTO.so*、LLVMgold.so*，同时用 ldd 展开依赖；clang 子包从该列表去除 qemu-accel 共有文件。证据：'+ev('raw/qemu-accel_new_armv7l_retry.spec:303-346')+'、'+ev('raw/qemu-accel_new_armv7l_retry.spec:665-669')+'。strip 禁用宏同样存在于两端 '+ev('raw/qemu-accel_old_armv7l_retry.spec:29-31')+'、'+ev('raw/qemu-accel_new_armv7l_retry.spec:29-31')+'。完整 diff 没有这些条目的变化。')
add()
add('## 机械归类规则、金额和占比')
add()
add('分类只根据已保存的结构和字节事实执行，规则在 [scripts/analyze_sizes.py](scripts/analyze_sizes.py) 中。每条配对路径保留全部命中标签；为获得可加总结果，另外按以下优先级选取一个主类：新增文件 → 删除文件 → qemu-accel 打包变化 → 链接方式变化 → strip/调试信息变化 → 代码节变大 → 未分类/大小未变。优先级是记账约定，不是因果强弱判断。')
add()
table(['规则','机械条件'],[
 ['链接方式变化','同路径两端均为 ELF；旧 NEEDED 中的 libLLVM.so.22.1 或 libclang-cpp.so.22.1 至少一个在新版消失。仍保留完整其它 NEEDED。'],
 ['代码节变大','同路径两端均为 ELF，完整 NEEDED 集合相同，且 .text/.rodata/.data.rel.ro/.eh_frame 任一节增大。该标签不表示整个文件一定增大；其它节缩小的净结果照实记录。'],
 ['strip/调试信息变化','两端 ELF 的 .symtab 存在性，或 .debug_*/.zdebug_* 节名集合发生变化。只比较节大小但有无不变时不命中此类。'],
 ['新增文件 / 删除文件','路径仅新版存在 / 仅旧版存在。无新文件时不设虚构增长。'],
 ['压缩格式','按每包的 PAYLOADCOMPRESSOR/PAYLOADFLAGS 独立比较；不分配解包字节，不混入可加总类别。'],
 ['qemu-accel 打包变化','clang-accel 路径任一端 SHA 无匹配，或仅一端收录；这是用户要求的分类标签，不等价于端点打包源码改变。'],
 ['未分类 / 大小未变','不满足其它条件且文件长度有差异 / 无差异。大小未变不表示内容相同，CSV 另保留 SHA。']])
add('主类净金额为所属路径的 `新大小−旧大小` 之和；占比 = 主类净金额 / 包路径净增量 × 100%，显示小数仅作显示，CSV 保留精确整数分数。负增量、负占比和超过 100% 的值允许存在，用于保留移除文件的抵扣。armv7l 总量为负，分类净额也可为负。')
add()
table(['架构 / 包','主类','路径数','净增量 bytes','占包路径净增量','raw 证据'],[[c['arch']+' / '+c['package'],c['category'],c['paths'],n(c['net_delta_bytes']),c['share_percent']+'%',ev(c['derived_evidence'])] for c in cats if int(c['net_delta_bytes'])])
add('上表省略零金额行，完整含零行的主类表为 [category_summary.csv](category_summary.csv)。所有包“新增文件”和“strip/调试信息变化”金额均为零；其证据为该表各行的 `derived_evidence`。主类合计与包增量逐包相等，见 '+ev('raw/validation.json:7')+'。')
add()
add('为不掩盖 clang-accel 上同时存在的 NEEDED 变化，另列**非互斥**命中统计。此表的类别金额不能跨类相加，完整表见 [category_membership.csv](category_membership.csv)：')
add()
table(['架构 / 包','所有命中标签','路径数','净额 bytes','占包路径净增量','raw 证据'],[[m['arch']+' / '+m['package'],m['category'],m['matching_paths'],n(m['net_delta_bytes']),m['share_percent']+'%',ev(m['derived_evidence'])] for m in members if m['package']=='clang-accel-x86_64-armv7l' and int(m['matching_paths'])])
add('因此，qemu-accel 类别的百分比不能解释为“qemu-accel 源码改动造成了这些字节”。两版收录规则文本、无匹配事实、对应 ELF 的链接变化分别独立记录。LLVM 编译/链接选项也只对应到观察类别，没有把一个工具的整个字节增量归因给某一个源码行。')
add()
add('## 获取状态、验证和复现')
add()
add('指定 RPM、文件清单、哈希和 readelf 输出已全部取得。aarch64 不在本轮指定下载清单，未获取本轮逐文件扫描，不能用 armv7l 数据替代。独立单选项优化效果、逐文件压缩贡献未获取，原因如前。所选 ELF 没有可读出的 build-id，逐行注明。')
add()
add('部分 cgit 请求返回 HTTP 502，失败正文保留，不能当作源码：`llvm_packaging.diff`、`qemu-accel_full.diff`、`qemu-accel_full_diff.html`、最初的 `qemu-accel_{old,new}_qemu-accel-armv7l.spec`、commit 页面和反向 log 页面。成功替代是 `llvm_packaging_complete.diff`、`qemu-accel_full_retry.diff`、`qemu-accel_{old,new}_armv7l_retry.spec` 和正/反向 format-patch。每次 URL、状态、正文 SHA 都在 '+ev('raw/fetch_manifest.jsonl:1')+' 起，失败不会被静默覆盖。')
add()
add('下载/采集脚本位于 `scripts/collect_*.py`、`scripts/retry_source_context.py`；文本分析为 `analyze_sizes.py`、`analyze_sources.py`、`analyze_coverage.py`，报告为 `write_findings.py`。离线复现只需运行后三个分析脚本及报告脚本；不执行 raw 中的产品源码。脚本使用 Python、requests、BeautifulSoup，以及 rpm/rpm2cpio/cpio/readelf；采集日志记录命令与退出码。')
add()
add('数据验证：14 个包完成标记和解包删除标记齐全；全部 regular 文件大小和 SHA 与 RPM 头相符；readelf 调用退出正常；逐类净额可回算各包净增量。机器核验见 [raw/validation.json](raw/validation.json)，收尾目录/引用/文件集核验见 [raw/final_validation.json](raw/final_validation.json)。RPM 和解包内容不在提交范围。')
add()
add('全部 CSV 均在本目录，raw 证据引用相对此目录；`:N`/`:N-M` 是保存文件的物理行号，GitHub 链接锚点定位到首行。下载来的 HTML、diff、spec、readelf 输出不做排版清理，便于核对原文。')
(OUT/'SIZE_FINDINGS.md').write_text('\n'.join(out)+'\n')
print('wrote SIZE_FINDINGS.md',len('\n'.join(out).encode()),'bytes')
