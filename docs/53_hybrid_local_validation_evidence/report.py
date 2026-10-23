"""Render final report from captured evidence, never substitutes missing checks."""
import collections,datetime,json
from pathlib import Path
from validate import W,D,E
load=lambda n:json.loads((E/n).read_text())
gib=lambda b:f'{b/2**30:.3f}'
link=lambda n:f'[{n}](53_hybrid_local_validation_evidence/{n})'
disk=load('disk-comparison.json');build=load('build-result.json');sizes=load('final-sizes.json');runtime=load('runtime-final.json');objects=load('objects-result.json');archives=load('archives-result.json');sdk=load('sdk-result.json');need=load('installed-needed-corrected.json');rpms=load('rpm-size-comparison.json');baseline=disk['baseline'];peak=disk['peak']['bytes'];bins=[r for r in rpms if not r['rpm'].endswith('.src.rpm')];old=sum(r['baseline_bytes'] for r in bins);new=sum(r['hybrid_bytes'] for r in bins);cache=int(next(r for r in sizes if r['name']=='cache')['stdout'].split()[0]);localtime=lambda ns:datetime.datetime.fromtimestamp(ns/1e9,datetime.timezone(datetime.timedelta(hours=8))).isoformat()
lines=['# Hybrid 本地完整构建、验证与磁盘测量（2026-10-23）','',
'**结论：完整构建和 22+1 RPM 产出成功，但验证未全部通过。** 188 项期望表最终实物 NEEDED 为 183 PASS、4 未产出、1 ANALYSIS_PENDING；四个非默认目标遇到 gtest 缺失与 fuzzer 编译错误，未修改源码或重试这些失败目标。已打包工具的共享库解析无缺失，但部分 Python 脚本的运行依赖不齐，详见 §5。',
f'主构建完整根的离散采样峰值 **{gib(peak)} GiB**，相对 32 号全静态+BOLT 基线 224.718 GiB 减少 **{gib(disk["root_peak_reduction_bytes"])} GiB**；结束时 ThinLTO 缓存 **{gib(cache)} GiB**，比 91.438 GiB 少 **{gib(98180825088-cache)} GiB**。普通链接至%install初期有约76.3分钟的有效采样空档，不能保证捕获整轮绝对峰值。',
f'22 个二进制 RPM 合计 **{gib(old)} → {gib(new)} GiB**，减少 **{gib(old-new)} GiB（{100*(1-new/old):.2f}%）**；逐包字节见 §4。BOLT 自有约 4.346 GiB 单列，不能把本轮全部降幅都归因于链接方式。','',
'## 1. 身份、条件与保护边界','',
'源码提交 `6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2`，tree `80a6fd231c4564a3b762f4ec288cf2c41f9d2e20`，父 `67619ec8bbbac7238a6cfc33a481ccfbcd12206f`。全程不改源码/spec、不推 Gerrit、不操作 QB、不创建分支。收尾输入复核 '+link('final-input-audit.json')+' 确认源码仍干净、配置和build.conf SHA均未变。所有 cmake/ninja 调用只在本次新根；历史根与 BOLT 保全资产只读。',
'新根：`temp/hybrid-local-20261023/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0`，位于 `/home`；构建结束后保留。GBS 自身 `%clean` 正常移除了本次 BUILDROOT 载荷，本任务没有手动清理历史目录。','',
'| 输入 | 核对结果 |','|---|---|',
'| 固定 Base | tizen-base-toolchain_20261013.024319，仅 packages、debug 两仓库；没有 Unified/reference |',
'| build.conf SHA256 | `e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945` |',
'| 用户指定 gbs 配置 SHA256 | `ce60cb95bad10e8e7ed20f3eb69094c4f91efacb8d89725967a6a4deb2a3d388`，只读，-B 指向新根 |',
'| GBS | 2.1.0；新 export 的 spec 与 0001–0008 全部同 docs/llvm_optimize_intranet_fetch.md §4，未用 VCS 例外 |',
'| spec SHA256 | `1da77fe8dfe45134bf7ae558ef366da2cfda6eccd917740449b85557b00e7f07` |',
'| 宏 | `jobs 8`、`_smp_mflags -j8`、`_costomized_smp_mflags -j20`；外层 `--threads=30` |',
'| 实际主构建 | Ninja -j6、compile pool 6/link pool 2；ThinLTO + TIZEN_HYBRID_LINK=ON；LLVM/Clang dylib ON |',
'| 实际后处理 | find-debuginfo -j8；Source1005 workers=4、单进程 AS=4 GiB |',
'| 与 QB 差别 | 本机 GBS，QB 是 NGBS JOBS_N=12/WORKER_N=28；本机资源限制、worker、并发背景不同 |',
'| shelve | 本地只使用干净的 6e9d4f2（相对 upstream 的 8 个导出补丁），无额外 shelve |','',
'输入证据：'+', '.join(link(n) for n in ['preflight.json','export-checks.json','build-command.json','build-metadata/identities.json'])+'。完整配置、原始 CMakeCache/build.ninja/rules 和 argv 均保存在证据目录。','',
'## 2. 完整构建与时间线','',
f'GBS 退出 **{build["exit_code"]}**，起止 **{localtime(build["start_ns"])} — {localtime(build["end_ns"])}**，wall **{build["seconds"]:.3f}s**。RPM 日志从 14:04:26 CST 起计时；GBS 包装器计时还包含启动/收尾，二者不可混用。',
'| 阶段 | 日志秒数 | RPM 日志行 |','|---|---:|---:|']
seen=set()
for a in disk['anchors']:
 if a['kind'] in seen:continue
 seen.add(a['kind']);lines.append(f'| {a["kind"]} | {a["elapsed_seconds"]:.3f} | {a["line"] or "GBS end_ns（日志无 finished 时间行）"} |')
lines+=['',f'Source1005：`NATIVE_ARCHIVES_BEGIN` 9388s、`NATIVE_ARCHIVES_END` 11960s，**225/225 PASS**。summary 记录转换自身 1970.965s；BEGIN–END 2572s 还包含安装，不能混作同一个时长。'+link('native-archive-summary.json.gz')+'；完整日志 '+link('rpm-build.log')+'，GBS 外层 '+link('service.stdout')+'，时间点 '+link('timeline.tsv')+'。','',
'资源：MemoryMax=MemTotal−8GiB=24,482,983,936 B、swap0、nice10、IO class2/priority7；内存无准入、无冻结、无分段续租。仅 /home<20GiB 正常停止；本次未触发。cgroup memory.peak=24,206,639,104 B，OOM/oom_kill/max 事件均0，swap峰值0。共享锁仅覆盖本任务重阶段，结束释放。cgroup io.stat 未暴露，未把它误报为0。以上均在本地包装器，不进入发布代码。','',
'条件偏差：15:38 只读发现另一 VS Code scope 运行 qb_analysis/work3/round7 的 GBS/grep 矩阵，与本轮链接 I/O 等待重叠；未操作其进程/根。证据 '+link('concurrent-build-observation.json')+'、'+link('concurrent-build-observation-later.json')+'。因此不是安静独占环境，不据本轮耗时宣称 hybrid 加速，也不把 df 整盘变化当作本根占用。','',
'## 3. 磁盘占用','',
f'同口径测量 chroot 完整根（du -sx -B1），每60秒尝试，50秒超时记缺失。本轮周期采样 {disk["complete_samples"]-1} 个完整值、{disk["missing_samples"]} 次失败/超时，加构建后验证前独立 du 一次，共 {disk["complete_samples"]} 个完整值。所有数值是**离散采样所见峰值/下界**，不是连续监测的精确最大值；缺失区间不插值、不补造。有效周期读数间隔最大4577秒（76.3分钟，14:59:43–16:15:59 CST，覆盖普通链接及%install初期），见 du-missing-coverage.json；不能把相邻点连线视为实际用量。初始观察器假定根内 timeout(1) 存在，初始化阶段失败；%build 前已改为根内 Python 超时，原始失败流保留。',
'| 阶段 | 全静态+BOLT 基线峰值 GiB | Hybrid 采样峰值 GiB | Hybrid 完整样本数 |','|---|---:|---:|---:|']
oldph={'ordinary-build':161.025505,'ordinary-install':205.561378,'static-conversion-install':224.717625,'platform-post':217.609959,'packaging':219.842541}
for k,b in oldph.items():
 p=disk['phases'][k];lines.append(f'| {k} | {b:.3f} | {gib(p["peak"]["bytes"]) if p["peak"] else "缺失"} | {p["samples"]} |')
lines+=['| BOLT 独立阶段 | 218.040（全根） | 不执行 | — |','',
f'峰值出现在 **Source1005 转换/安装** 阶段（{localtime(disk["peak"]["time_ns"])}，{peak:,} B）。基线的普通构建161.026 GiB仅为最后一次续跑段，不能视为整轮该阶段完整曲线。基线曾冻结/改变内存上限，另有2.065 GiB中断链接遗留；均不能直接归为hybrid收益。',
f'基线 BOLT disk-report 自有占用最大 **{gib(disk["baseline_bolt_fixed_report_peak_bytes"])} GiB**，其中包含 ThinLTO 正增量；这不是可与缓存再次相加的独立项。基线224.718GiB与本轮{gib(peak)}GiB差值是观测差，不是完全控制变量的因果估计。基线原始数据复制自32号的测量 JSON，未重新扫描或改动其构建根。','',
'结束后、任何补建/RPM安装验证之前的独立 du：','', '| 项目 | 实际分配字节 | GiB |','|---|---:|---:|']
for r in sizes:
 b=int(r['stdout'].split()[0]) if r['rc']==0 else None;lines.append(f'| {r["name"]} | {b if b is not None else "失败"} | {gib(b) if b is not None else "—"} |')
lines+=['','BUILDROOT 4KiB 是标准 `%clean` 后的空目录，非安装阶段峰值。build 包含 lto.cache，root 包含二者，不能相加。RPM du 为分配字节，§4为文件长度，口径略有差异。',
'证据：'+', '.join(link(n) for n in ['du-root-complete.jsonl','du-root.jsonl','final-sizes.json','disk-comparison.json','resources.jsonl.gz'])+'。补建22目标在以上测量封存后执行，失败耗时与文件变化单独记录，不计入本轮峰值。','',
'## 4. RPM 数量与大小','',
'22个二进制包名称全部同冻结清单，1个源码包。完整SHA、NEVRA、BUILDTIME见 '+link('rpm-identities.json')+'，逐包大小见 '+link('rpm-size-comparison.json')+'。','',
'| RPM（省略22.1.8-1.x86_64后缀） | 全静态+BOLT B | Hybrid B | 变化 B | 变化 % |','|---|---:|---:|---:|---:|']
for r in rpms:lines.append(f'| {r["rpm"].replace("-22.1.8-1.x86_64.rpm","")} | {r["baseline_bytes"]:,} | {r["hybrid_bytes"]:,} | {r["delta_bytes"]:+,} | {r["delta_percent"]:+.3f} |')
lines+=['','多数工具由重复静态LLVM/Clang代码改为共享依赖，与llvm/clang/lldb及其debuginfo显著缩小一致；这是体积解释，不是逐字节差异归因认证。两份配方不完全相同：基线启用BOLT、clang完全strip，本轮普通clang保留独立debug；源码RPM内容也不同。几十到几万字节的小变化可能含元数据/时间戳，未断言全部由链接方式造成。','',
'## 5. 功能与打包验证','',
'| 检查 | 结果 |','|---|---|',
'| 完整构建/RPM | PASS：22 binary + 1 source，GBS exit0 |',
'| 188目标实物NEEDED | 183 PASS /188；4未产出；AnnotateFunctions.so缺少预期libLLVM依赖，保留ANALYSIS_PENDING |',
f'| 已安装映射路径 | {need["status"]}：170 ELF/别名通过，10个非ELF不适用NEEDED检查 |',
f'| 全部打包可执行入口 | 144/158通过，14个脚本依赖缺失；缺失共享库路径数 {len(runtime["missing_shared_library_paths"])} |',
f'| 30 TU×3目标对象 | {objects["passed"]}/{objects["total"]} 完整 .o 字节相同 |',
f'| LLVM/Clang SDK | {"PASS" if sdk["pass"] else "FAIL"}：配置、动态链接、运行；329条imported文件记录均存在 |',
f'| llvm-static-devel | {archives["passed"]}/{archives["count"]}：native归档、索引完整；Source1005 PASS225 |',
'| ARM32/ARM64 | 同一8补丁GBS导出，Tizen rpm4.14.1.1-1.7解析均0；未做ARM完整构建 |','',
'### 5.1 NEEDED与188目标限制','',
'期望表包含3组静态、5个上游静态例外、29个不依赖这两库的目标、108个LLVM动态、43个LLVM+Clang动态，不把“其他全部动态”覆盖这些明确例外。clang/lld/llvm-ar及别名实际没有libLLVM.so/libclang-cpp.so依赖。安装后的映射路径逐项核对见 '+link('installed-needed-corrected.json')+'；原始166实物见 '+link('linkage-188.json')+'。',
'22个缺失项均在保存的build.ninja中有规则，但不属于默认all闭包、不安装。其配置关系不是实物认证。为补齐覆盖，在主构建结束、峰值封存后补建22目标；dry-run50条，未重配CMake。5.386s后失败，保留原文：','',
'```text',"fatal error: 'gtest/gtest.h' file not found",'ld.lld: error: unable to find library -ldefault_gtest',"error: unknown type name 'uint8_t'",'ninja: build stopped: subcommand failed.','```','',
'前两项来自OpenMP非默认测试，最后一项来自clang-fuzzer/clang-objc-fuzzer；未装新依赖、未改源码、未重试四个失败目标。其余18项因首次Ninja提前退出而未执行，随后单独补建成功（38任务、190.340秒），CMakeCache/build.ninja/rules前后SHA一致。第二次补建使用已安装的本次hybrid编译器，属于补充验证而非原QB条件的完整构建；全部时间/磁盘与主构建分开。全部22路径及规则/default依赖证据见 '+link('linkage-188-classification.json')+'，任务与原文 '+link('optional-target-dry-run.json')+'、'+link('optional-target-build.log')+'、'+link('optional-build-result.json')+'。','',
'补充结果 '+link('linkage-188-supplemental.json')+'、'+link('optional-remaining-result.json')+'：183 PASS，4个缺失；唯一实物偏离是 `lib64/AnnotateFunctions.so`（预期libLLVM=true，实际只有libstdc++.so.6与libc.so.6）。保存规则123604–123615行同时含libLLVM与--as-needed；实物插件加载后成功产生example_annotation，与未用依赖被--as-needed丢弃的解释一致。未做改变链接参数的反事实实验，因此不擅自把冻结表这一项改成PASS。见 '+link('annotate-analysis.json')+'、'+link('annotate-link-edge.txt')+'、'+link('annotate-plugin-smoke-corrected.json')+'。首次插件探针将--no-default-config放在-cc1前，误入driver模式；原错误保留，修正为-Xclang透传后测试通过。补建日志出现无法读/proc/cpuinfo的警告：GBS已卸载本次根/proc；目标构建退出0，警告保留。','',
'安装检查器首次选择路径时，宽泛/sdk_tools/正则误纳入4个.debug伴随文件；原始ERROR保留，改为明确排除/usr/lib/debug后复核实际ELF/DSO。这是探针选择修正，不是忽略缺失工具或放宽NEEDED规则。','',
'### 5.2 可执行程序运行','',
'本次新建构建根中安装全部22RPM（rpm -Uvh --oldpackage --replacepkgs，无--nodeps），依赖检查/安装成功。根仍包含构建依赖与编译树，属于用户允许的构建根环境复用；未宣称是最小运行时根。每个已打包可执行ELF/shebang脚本均运行，别名逐路径覆盖；DSO和.debug不冒充可执行工具。','',
'首轮136/158入口直接通过；8个工具改用其支持的等价参数（如diagtool list-warnings、llvm-c-test --targets-list、MS工具/?、clang-installapi上游basic输入），首次失败输出仍保留。最终未通过项如下：','',
'| 路径 | 最后探针原文（摘要） |','|---|---|']
for r in runtime['rows']:
 if r['status']=='PASS':continue
 a=r.get('equivalent_probe') or r['attempts'][-1];raw=(a.get('stderr') or a.get('stdout') or a.get('error','')).strip().splitlines();lines.append(f'| `{r["path"]}` | `{(raw[-1] if raw else "无输出").replace("|","/")}` |')
lines+=['','这些缺失模块/解释器/外部git是当前根的真实运行限制，不能算全项PASS；它们与共享库缺失不同。15个首轮待查脚本（含后续通过的hmaptool）在基线对应RPM与本轮RPM中file digest全部相同；两侧clang/llvm/devel清单均无libscanbuild。见 '+link('runtime-baseline-comparison.json')+'。这支持“脚本内容没有因hybrid变化”，不证明运行环境完全等价。未擅自安装依赖或改脚本。',
'运行原文 '+link('runtime-final.json')+'、环境 '+link('runtime-environment.json')+'；C/C++编译、clang++/lld链接与执行、llvm-ar索引、ld.lld -r、opt/llc/clang-tidy通过：'+link('native-smoke-result.json')+'。','',
'### 5.3 对象、SDK、归档','',
'沿用30条历史TU（20独立源+10留出条目）×x86_64/armv7l/aarch64，总90份既有预处理输入；SHA先逐份核对。原argv/target来自资产，不发明参数；两编译器依次覆盖同一实体路径、同一inode，--no-default-config、同一resource-dir/input/output，不移除.GCC.command.line。ordinary固定SHA `06c940726269210ce3655e17366820a080bfe236a3adc24622958e6a6709e309`，使用用户指定BOLT第一轮的普通clang，非BOLT候选。',
'本轮hybrid clang SHA `'+objects['identities'][1]['sha256']+'`；完整参数、逐文件SHA与原始命令输出：'+link('objects-result.json')+'、objects/子目录；输入 '+link('tu-inputs.json')+'。','',
'开发示例 find_package(LLVM)/find_package(Clang)，链接target LLVM和clang-cpp，输出动态NEEDED含两库；生成/运行成功，所有配置导入目标的LOCATION/IMPLIB检查存在。'+link('sdk-result.json')+'、'+link('sdk-imported-files.tsv')+'。225归档严格核对冻结路径，native成员无bitcode、索引存在且等于机器符号表：'+link('archives-result.json')+'。','',
'## 6. 结论、未通过项与后续建议','',
'本轮已完成一次QB条件的完整本地构建和允许范围内验证，保留构建根。磁盘用量显著下降，但不是全部认证PASS：188表仍有4个非默认目标不能产出、1个NEEDED期望偏离待分析，14个脚本运行依赖限制仍需核查（以最终runtime表为准）。建议后续先明确188验收对非安装测试/示例目标的要求，检查四个失败目标的测试依赖/编译条件，并由维护者确认AnnotateFunctions是否应接受--as-needed例外；对脚本运行依赖核对RPM Requires/载荷，另行授权后处理。本轮不修复源码、不更改发布配方、不触发QB。','',
'测量限制：60秒采样且存在50秒超时；基线含BOLT与中断链接遗留；本轮检测到其他会话并发I/O；不能从本次时长推导性能提升，也不能保证没有短暂更高峰值。各包体积差和缓存差以实测字节为准。','',
'原始证据均在 [53_hybrid_local_validation_evidence/](53_hybrid_local_validation_evidence/)，含完整命令、日志、采样、配置快照、188逐项结果、运行输出及对象/归档报告。大JSONL以gzip发布并保存原始字节SHA；本地原件保留。证据索引见 '+link('evidence-manifest.json')+'。']
(W/'docs/53_hybrid_local_validation.md').write_text('\n'.join(lines)+'\n')
