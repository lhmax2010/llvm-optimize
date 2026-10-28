# BOLT v4 状态（新会话开场必读）

## 长期署名规则（PM 裁决，2026-10-15）

作者与提交者可直接使用本机全局配置 liushanshan <ss0217.liu@samsung.com>，或以单次命令参数显式使用 Hao Lin <hao.lin@samsung.com>。任何后续提交、提交说明（含 Signed-off-by）和交付文档仅使用这两组身份，不再使用此前昵称或其他姓名。不修改全局 git 配置；历史提交不因此重写，历史身份按提交号查询原始元数据。

若 Gerrit 因提交者与推送账号不一致而拒收，立即停止该次操作，保留并原样报告完整拒绝输出；报告后再以 Hao Lin <hao.lin@samsung.com> 重新提交。不得隐瞒拒收或继续使用被拒身份重试；仍须遵循具体任务的分支推送授权。


日期：2026-10-12（Asia/Shanghai）；证据目录名20261013按用户指定。
W=`/home/linhao/Toolchain/development/llvm-optimize`；B=`/home/linhao/Toolchain/development/llvm-optimize-bolt`；E=`/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013`。
分支bolt-v4；起点为最新origin/main `fb833a4c8ee1ece09027a0d5d04e254ea9899a5f`。W开场docs/47_review_round4_package.md与gbs_llvm.conf有归档会话修改，未触碰；其后主分支提交由归档会话独立推进，不合并到本任务。

## 计划

今晚五步已完成可执行范围：独立树/状态→只读盘点→串行strip矩阵→≤50KB设计v4→逐里程碑提交推送/远端核验。后续按01设计接周三/周四，不自动构建或部署。

## 进度

| 任务 | 状态/提交 | 产出 |
|---|---|---|
| 建立分支与状态 | 完成；ba825d62dff5f7c683c65e0f23fd87de90e8a7f3 | STATUS.md；E/inventory/opening-inputs.json |
| 资料盘点 | 完成；51d534ff67ec3aae560643564e764455bc9fc953 | 02_inventory.md；E/inventory输入/工具/SHA/spec/宏/锁快照 |
| strip实验 | 完成可执行项；7ceaf2b00d6bfd0e87f4c8319d54b0aff12229bc；e因2GiB预剥离OOM跳过 | 03_strip_experiments.md；E/strip、strip-results.json |
| 设计v4 | 完成；ea901a4fc1be99d76d8601cd7427da89230a66dd | 01_bolt_v4_design.md；POSIX片段语法及大小检查 |
| 收尾 | 完成；本条所在提交，SHA见git log -1及最终回复 | 15原件SHA全同、10新shell dash检查、23独立scope摘要；推送后E/final-publication.json登记远端一致性 |

同一提交无法写入自己的SHA：最终行用所在提交，其他里程碑均为完整号。所有提交只在B/bolt-v4，中文说明；没有PR或Gerrit推送。

## 已闭合结论

| 结论 | 证据与强度 |
|---|---|
| profile v2、v1/v2 clang、relocs clang、RPM基线及BOLT/strip工具全在磁盘，收尾未变 | E/inventory/artifacts.json、original-preservation.json；15项完整SHA一致，直接事实 |
| 两spec主项目不包含bolt；既有llvm-bolt来自docs/15历史增量构建，不是现有spec正常产物 | 两git对象spec与实际cache、工具版本/SHA；源文+直接事实 |
| cb与f111两套x86均为LLVM库静态，但编译器/flags处理不同 | spec.diff及旧ELF/cache；直接事实；新cb profile适配尚UNKNOWN |
| GNU strip默认/debug与GNU objcopy处理BOLT v2均SIGSEGV，eu-strip返回0却LOAD0 | E/strip各副本result、readelf、版本及三个目标编译退出；直接实测，非所有版本泛化 |
| LLVM debug/all strip可运行、三目标.o与RPM基线一致；debug保留note，all删除note | E/strip/v2-llvm-debug、v2-llvm-all；直接三对完整字节事实，非性能证明 |
| 无原生按文件exclude API；实际FD无debug正常路径跳过且SHA不变 | rpm脚本原文、v2-fd-pathfixed；源文+脚本副本实测 |
| FD选择器误匹配路径debug；预debug-strip+FD+专用LLVM brp组合存活 | 初始误选/修正/安全链日志；直接实测，完整RPM尚未认证 |
| LLVM strip替换inode使动态硬alias识别失败；冻结路径组再重建硬链接方案通过 | v2-wrapper-audit FAIL、v2-wrapper-audit-fixed PASS/路线/内容SHA与inode；直接实测 |
| relocs LLVM debug/all及eu-strip在2GiB OOM；e及输出后处理未运行，新BOLT重写0次 | 相应scope systemd Result=oom-kill；直接资源失败，不宣称新重写成功 |
| 23个实验/核查scope全部回收，采样最低MemAvailable12474175488B，全部入口≥8GiB | scope-summary.json、scope argv/env/samples、最终scope-recovery.json；采样事实，非连续最低保证 |
| 未改W跟踪文件/W llvm/构建根，未构建LLVM、采profile、插桩、挂载或干扰项目锁 | 命令日志/写入限定/原件SHA；操作边界；供应商原Bash脚本只读复制，新写shell全POSIX |

## 历史v4人工裁决（本轮变更由下方v4.1覆盖）

1. 目标：本周五（2026-10-16）前交付一个 BOLT 补丁进 Quickbuild 试验验证。试验不是上 Gerrit
2. 第一版范围：只做 x86_64 构建分支；只做 clang（lld、llvm-ar 以后）；保持现有全静态链接，混合链接不进第一版；llvm-static-devel 照常发布，不撤
3. profile 直接用现有 v2，作为 spec 的一个 Source 文件提交，不单独打 RPM；构建时必须检查 profile 与二进制的匹配度，不匹配函数比例 ≤5%，否则构建失败
4. 第一版不追求 BOLT 版 clang 的源码级调试信息，但必须保证经过完整 RPM 后处理（含 find-debuginfo、strip）后仍能正常运行
5. 补丁基线：tizen_base 提交 cb67996861d070d68fec2b4c623eed7d20ba2e23 加上归档修复的 356627 PS3 与 356639 PS2 候选；同时必须能干净应用到不带这两个补丁的 cb679968
6. 硬约束：不得影响用 LLVM 编译的其他 RPM 包——不得引起编译错误、运行时性能下降或运行内存升高；BOLT 版 clang 产出必须与原版逐字节相同；LLVM 包自身构建内存若显著增加必须报告
7. 总部计划把 bash 换成 dash：你写的任何 shell 脚本都必须是 POSIX sh，不得依赖 bash
8. 评审：周四只对补丁做一轮外部评审
9. 时间表（供你理解，不是今晚任务）：周三晚在归档会话完成的 x86 完整构建树上续跑构建（只重链 clang、做 BOLT、打包），周四验证与评审，周五交付

## 重任务锁协作规则

归档会话开场使用W/temp/review-round4-20261012/hold_lock.py，以O_CREAT|O_EXCL同时占用W/temp/.llvm-optimize-exclusive.lock与W/temp/gbs-root-x86_64-archivefix-v2/.llvm-optimize-exclusive.lock，JSON含pid/session/start；只有拥有者匹配记录才删除。脚本/记录只读封存E/inventory/archive-*。以后重任务先由归档会话明确释放/移交，再核验树身份/无重进程并按该机制取得锁；不能删“看似过时”的锁。本轮没有获取、等待、释放锁或向拥有者发信号。后续新根的锁路径随移交重新固定。

## 挂账

| 项 | 下一步/边界 |
|---|---|
| cb profile匹配与新完整树路径 | 归档会话周二夜完成cb+指定PS3/PS2树后登记SHA/路径，周三实測≤5%失配；不继承旧树PASS |
| 预剥离OOM | 周三明确资源预算再测；今晚不抬cap，e及输出a–d/FD七项保留SKIP |
| 生产llvm-bolt来源 | 同源standalone私有子构建与Tizen/MLGO exports未认证；历史工具可做单独资格实验，不能冒充可复现spec生产来源 |
| spec/helper补丁与新RPM | 今晚只设计；周三实现并正常RPM后处理，裸cb/叠PS3/PS2干净应用；不short-circuit拼正式RPM |
| 完整RPM/其他子包/90对.o/accel | 周四最终包检查；30源文件×三目标不是历史30对；新patchelf双次/完整accel/worker实物仍待验 |
| Quickbuild部署与下游资源 | 三种交付途径待用户选择；OBS项目/快照/仓库/CLI接口与性能协议由用户/内部团队提供；本轮不提问、不部署、不测性能 |

未整体停止；三项2GiB strip OOM及依赖e链按资源约束跳过，完成其余授权工作。辅助相对路径失败和动态inode alias失败均原样保留，修正验证单独记录。完整debug/FDeu-strip破坏风险没有因工具rc0被隐藏。

## 2026-10-13 v4.1 历史阶段（已被后续裁决覆盖）

早期草案/Quickbuild环境与首次准备停止详见05和905b14f之前的STATUS；原文另保全在25对应raw。该阶段59夹具和profile压缩完成，初始草案b3ec4f0未推Gerrit；历史debug-only、双flags、二次安装与缓存复制方案均已由后文最新裁决替代。共享重锁规则仍为flock独占、等锁≤2h、单次≤60min；普通重段16GiB/swap0、nice15/ionice3、准入12GiB、运行<3GiB终止，轻段4GiB/nice19/ionice3、准入6GiB。特定任务明确覆盖的资源上限单独登记。

## 2026-10-13 续任务：完全 strip 双模式（最新裁决覆盖旧限制）

人工前提：用户确认当前 Quickbuild 在 Tizen-Base-Toolchain 定义 _toolchain，走 debug；以后 Tizen-Base 无 _toolchain 走发布，不跑 FD，由 GNU brp-strip 处理 not stripped ELF。必须双模式。

PM八项新裁决按01附录修订执行：fully strip、前note/前后SHA/最终SHA、普通包无symtab核实、指定普通chroot临时proc、完整缓存副本与三路径、原post只一次、本地严格双模式文件例外、周五前不做standalone。旧debug-only/两次post/note终检/私有挂载方案全部作废，05历史停止事实不改。

步骤1已完成：84fixtures PASS，完整patch apply/tree 与公开封套 tree PASS；本地源提交 e5239cd50dce5e16cb43b99395388b6bb60829f1，无Gerrit推送。普通历史RPM原件SHA不变，clang无.symtab且file stripped。06给身份与证据。步骤2–4待执行，05的未执行不再作为禁止按本次明确授权恢复的依据。周三计划已按新裁决更新01附录，最终状态将随实测补齐。

步骤2实测：缓存完整复制及原缓存终审PASS；dual/reference严格符号表不一致（2344个STT_FILE），按已裁决fallback到reference；BOLT匹配R0.004238545%、S/N0%，note/strip-all/三目标PASS。30输入初轮首个.o因.GCC.command.line编译器路径差异FAIL，剩余29未执行；公平argv0重测遇到入口内存不足及共享锁占用，待继续等锁。07与r1-rehearsal.json给全部实测，不把该30门禁记PASS。

步骤3双模式小spec判据PASS：历史v2 strip-all副本，两模式clang均被选择器跳过、控制正例FD/eu-strip与GNU strip -g实际执行；RPM SHA保持575fc9db…及三目标PASS。Debug一次post、release一次；测量脚本.gnu_debuglink错误与已有输出保护失败日志保留，修正后用同一debugRPM及新releaseRPM。08/dual-mode-smoke给证据。两模式真实草案rpmspec解析亦PASS，不冒充完整安装宏认证。

步骤4：90/90新预处理资产PASS（30历史selection/20独立路径×3目标），缺源/缺头0，完整argv/源SHA/.ii SHA/逐头SHA已保存，.ii合计677747108B留E。净42.576s/scope43.598s；09与assets90-manifest公开，小spec与资产不冒充90对象或完整包认证。

步骤5计划与最终草案已修订：公平完整对象改为同一专用实体路径的两批验证；新树先匹配、复制缓存（工具链接也需隔离核查）、不豁免STT_FILE、debug本地逐包SHA/逐个缺失DWARF证明，发布完整构建不得由小spec代替。只读origin/main aeea5f8仍未正式交接新树，未进入归档根。最终源码草案 a3c31d2c40809adbfacfd8cb6c12f3e87476a058，完整与公开封套再次apply/tree PASS，无Gerrit推送；周五前standalone仍未做。

## 本次续任务最终状态（2026-10-13）

本次授权六步已执行并分步推送GitHub bolt-v4；没有规定外环境异常导致整体停止。真实门禁失败和测量错误均保留：dual-flags与reference的完整符号表一致性FAIL（2344 STT_FILE），按上一轮PM明确的fallback采用reference+LLVM strip-debug，不放宽；30对象首轮不同编译器路径使.GCC.command.line差异，公平同一实体路径重测30/30 PASS；小spec.gnu_debuglink错误判定及重复strip输出被保护拒绝均记录，复核同一debugRPM并单次正常release后所有规定判据PASS。

| 步骤 | 最终结果 | 证据 |
| --- | --- | --- |
| 1 草案/fixture/普通包 | 完全strip双模式、单次完整post尾检、三路径cache重放、SHA身份链、本地严格双模式清单策略；84/84 PASS；静态完整patch与公开封套apply/tree PASS；普通RPM clang无.symtab/file stripped/原件不变 | 06/helper/test/patch/manifest |
| 2 R1预演 | cache全复制/原cache最终不变PASS；dual严格对照FAIL但authorized reference fallback；R=0.004238545%、S/N=0%；前BOLT标识/strip-all/三目标PASS；公平历史30/30完整对象PASS | 07/r1-rehearsal/resource-metrics |
| 3 两模式小spec | historical-v2 fallback副本，debug/release原post各一次，clang两模式都跳过，普通控制分别FD/eu-strip及GNU strip -g处理；RPM clang SHA575fc9db…/三目标均PASS | 08/dual-mode-smoke/两spec |
| 4 90资产 | 90/90新.ii及argv/源/逐头SHA PASS；缺源0/缺头0；30selection/20源路径，677747108B留E | 09/assets90-manifest |
| 5 周三计划 | 正式origin/main交接+锁空闲为开始条件，先匹配、新树完整cache副本、工具链接cache隔离/普通任务0、debug本地逐包字节对照及逐缺失DWARF证明；发布完整构建待做；Gerrit推送条件/命令列出但不执行 | 01附录v4.1 |
| 6 收尾 | 原cache/普通clang不变、R1/proc与scope全部回收、设计≤50KB、Python3.9、Git文件≤10MB；最后提交/推送及raw清单 | 本文/resource-metrics/10 raw清单 |

最终本地LLVM源草案a3c31d2c40809adbfacfd8cb6c12f3e87476a058，父cb67996861d070d68fec2b4c623eed7d20ba2e23，tree4ec0029fcb10baf632af6fc9e2bd58aad1eed224；作者记录见该提交元数据；不是GitHub证据仓库提交。未向Gerrit推BOLT提交。sandbox仍仅此前原样创建基线，周五前没有standalone、没有完整LLVM构建。

共享锁cache段约41m、其余最长reference约11m；公平30段实际等锁363.056s/持锁351.706s，未等锁超时；一次内存准入SKIP和自己的未取锁等待暂挂记录保留，没有豁免入口12GiB。轻实验与公平重测串行，没有向归档项目锁/进程发信号。只在B/E/R1新BOLT工作写入，W tracked/llvm不改，未进入归档任何构建根。

当前origin/main aeea5f83f35d9e957c329830fa61eb3ec0aa7e88的STATUS仍未正式交接cb新树，周三不能据目录存在开始。完整in-tree新llvm-bolt图/其cache隔离/install差集、cb匹配与实际完整spec后处理尾挂接、同模式普通cbRPM本地文件清单/DWARF逐项证明、发布完整构建/其他包/消费者/90真实对象/性能均仍待认证。小spec与R1资格不代替这些门禁；草案不可据本次直接推送发货。

原始E=/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261014；R1专用/home/abuild/bolt-work/bolt-v4-20261014。大cache/ELF/.ii/完整patch/原日志均留新工作目录；Git只提交可评审文档、helper/fixtures、文本patch+压缩Source+manifest、小spec及JSON摘要。全部raw分支版/钉提交版索引随本次10发布；最终GitHub提交由git log与收尾回复给出。

## 2026-10-13 晚轻任务：最新人工裁决（覆盖此前相关方案）

1. spec/helper唯一生产路径为 emit-relocs 重链→LLVM strip-debug→BOLT→匹配/三目标→LLVM strip-all→安装与单次原post终检；删除双flags快路径、双路比较和回退。R1仅差2344 STT_FILE：LLVM strip-debug删除STT_FILE，LLD链接时strip-debug不删；final SHA575fc9db…与历史v2完全strip一致。
2. 周三新树在origin/main STATUS正式交接后归本会话使用；原地引用原ThinLTO cache，LLD写入/prune可接受，不复制、不要求原cache冻结。cache路径改写仅保留为可选能力，R1等受保护非交接树才用。交接前不触碰根。
3. 预计单次写入>10GiB的操作，所在文件系统写完必须仍有≥30GiB free，reserve另计；不足跳过报告。设计/helper预检按实际文件系统核算，预算必须含临时产物及新增cache。
4. 今天复制98,248,402,280B导致工作区一度仅约5.6GB可用，LLD自动prune副本才恢复。原因是复制巨大cache而仅留4GiB重链reserve、未守30GiB底线。07正式备案；对策为第2、3项，不把审核PASS解释成安全。
5. 归档完整x86树在/var/tmp，具体路径以正式交接STATUS为准；周三不得写死W/temp路径。
6. .GCC.command.line记录实际编译器路径，30与90完整对象验证均必须用同一专用实体路径、两批复制来源SHA、相同argv/cwd/input/output，不改参数或过滤节，argv0伪装不足。

步骤1完成：95/95 fixtures PASS（0.408s；4GiB轻scope1.528s），完整patch及公开封套静态apply/整树PASS；本地源码 d6ddbff5ba74bfb420b357b5b6ba9ed300971bb4（父cb679968），文本patch/profile/manifest更新，无Gerrit推送。Quickbuild单一路径估12–15分钟、kernel峰约6.04GiB（R1温缓存依据；新llvm-bolt构建/正常post另计），详情11与single-path-estimate.json。今晚不取共享锁、不跑重阶段、不进入归档根。步骤2副本清理、步骤3周三计划更新待执行。

步骤2清理完成：仅删除授权副本 lto-cache 残余目录；前2,365文件/4,671,566,600B（实际占块4,676,378,624B），后0文件/0B/目录不存在；同文件系统free从79,338,237,952B（73.89GiB）到84,019,998,720B（78.25GiB），观测增4,681,760,768B。共享磁盘并发写入会影响free差量，不将其等同精确释放字节。原cache47,770文件/98,248,402,280B完整清单mtime/34跨度SHA前后及上轮基线一致，其他459条BOLT证据元数据清单一致。4GiB轻scope16.063s（工作15.095s），没有flock/chroot/mount；r1-cache-cleanup.json记录路径来源和审计哈希。步骤1 GitHub提交55a2e06已推送。

步骤3周三计划更新完成：01最新附录覆盖原v4/旧v4.1；正式READY交接（/var/tmp具体路径由STATUS给出）、共享锁与磁盘/内存准入→先匹配→新树原地cache、只构建同树BOLT且普通任务0、唯一重链/strip/BOLT/三目标/SHA链/单次原post尾检→30与90同一实体路径完整对象→本地debug同模式普通cb RPM逐包字节清单与逐缺失普通DWARF/全部其他debug证明→满足资格/评审/源recipe一致性/Source传输条件才可未来sandbox推送。发布分支完整普通/BOLT构建继续挂账。今夜只读同步origin/main=6e874fdbd0149a33167c9b83f8938d17df7c7ceb，其STATUS明确BOLT交接NOT READY，没有新根/cache/完成指纹；没有进入归档根，不凭目录存在开跑。旧段落的复制新树cache/原cache冻结/双路严格比较均已被最新人工裁决覆盖。

## 今晚轻任务最终状态（2026-10-13）

授权三步全部完成，未遇规定外情况而停止；新树续跑条件仍未满足，留周三，不在今晚启动。步骤1 55a2e06（唯一重链/磁盘预检/95fixture/static apply-tree）；步骤2 7ecdcf7（仅自建R1 cache残余清理/原cache与其他证据审计）；步骤3设计/周三计划与本收尾提交均推GitHub bolt-v4。

- 本地LLVM源码 d6ddbff5ba74bfb420b357b5b6ba9ed300971bb4，父cb67996861d070d68fec2b4c623eed7d20ba2e23，tree3f0fec567a7adcca0ffd405469fe5f08a3e35857；完整patch、文本+Source封套apply/tree均PASS，未推Gerrit。profile原SHA不变。它与GitHub文档提交身份不同。
- 最终95/95fixture PASS；旧fast/compare/fallback已删除，默认cache字串保留，optional第三项仍可用；匹配、前后tiny、strip身份、post/aliases、本地双模式清单门禁保留。Python3.9 parse、helper镜像一致、8段POSIX shell片段、文档≤50KB/提交文件≤10MB检查PASS。设计46,354B。
- 仅4GiB/swap0/nice19/ionice3轻scope，入口≥6GiB、运行≥3GiB；fixture峰0.049GiB、freeze峰0.198GiB、清理峰0.306GiB，scope均回收。无共享锁、重阶段、chroot/mount、归档根进入、standalone或完整LLVM构建；W tracked只保留其他会话既有gbs_llvm.conf变更，W/llvm未写。
- 清理前2,365文件4,671,566,600B，后0/0；free79,338,237,952B→84,019,998,720B。原cache完整清单mtime/34SHA与上一轮及清理前后一致，其他459条证据元数据一致；原数据/候选/大.ii/日志保留。磁盘险情原因与原地cache/30GiB底线对策在07和本文。
- Quickbuild pipeline仅温cacheR1依据，估12–15分钟、峰约6.04GiB，新同树llvm-bolt构建/正常post不含；详细采样跨度及边界在11/single-path-estimate.json。
- origin/main6e874fdb…仍NOT READY；正式交接后才读准确/var/tmp根，先匹配，原cache单路径，30/90同一实体路径完整对象，本地debug RPM与普通DWARF逐项证明；发布完整构建/完整同树工具与post/RPM/消费者仍挂账。今晚不声称这些通过。

新原始E=/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261014-simplify；公开11、single-path-estimate、r1-cache-cleanup、light-task-validation及补丁manifest；全raw分支/钉提交索引10随最终提交更新。

## 2026-10-14 周三续跑：交接PASS，先行匹配探测参数错误后STOP

最新授权：main正式交接的/var/tmp新树原地cache；同树只建llvm-bolt并核对bolt配置前后clang链接字串；前六步全部PASS且性能geom(candidate/ordinary)<0.98后，父cb679968、无归档补丁BOLT提交可直推sandbox/lhmax2025/bolt_pgo；不推refs/for/tizen_base。内存准入不足5分钟复查、最多60分钟。本授权覆盖旧“不推BOLT”及旧更宽/不同推送前提，实际门禁失败仍不推。

main=91b45c167a8773bbe1564b5ab902033da5060d83、docs/49_x86_build_resume_result.md §11/15正式READY，时间13:10:12。用户列出的clang/CMakeCache/build.ninja SHA、cache47,107文件/96,877,810,360B全部相符；8交接文件和22普通RPM逐SHA/大小通过；环境/源码/补丁指纹与冻结记录相符。归档review49-independent-install元数据基线保存，原件只读；新输出在/home/abuild/bolt-work/bolt-v4-20261014-wednesday及W/temp/bolt-v4-20261014-wednesday。

第一步匹配资格仅一次调用rc1：本任务错误地把带cdsort/split-eh的最终重写参数组用于无emit-relocs的普通clang，BOLT原文“function reordering only works when relocations are enabled”。这是探针入口参数错误，不是profile失配；N/M/S/U/Q、R、S/N未知，5%双门禁未评估。按“规定之外停止”不改参数重试、不先重链绕过，也不拿旧R1数据顶替。步骤2–7（新工具、流水线、30/90对象、小spec/DWARF预期差异、性能、sandbox）全部NOT RUN；没有Gerrit推送或远端前后核对。

资格scope1.025s、kernel峰515,751,936B/0.480GiB，16GiB/swap0/nice15/ionice3；入口17.43GiB、最低17.40GiB，OOM0。短命BOLT未被0.5秒VmHWM采样捕获，采样Python12596kB不能冒充BOLT峰值。共享锁等约0.000014s/持1.063s，finally已释；proc已卸载，所有scope回收。停止后轻审计8文件/22RPM SHA大小不变、原cache完整name/size/mtime相同、归档证据元数据相同；未进入本次两棵/var/tmp ARM根，W tracked既有gbs改动保留不写。

本次授权未完成，状态STOP_QUALIFICATION_ARGUMENT_ERROR；只完成身份/准备及失败探测证据，停止后仅审计/报告/提交，不继续产品实验。下次恢复先明确非重定位资格查询入口。源码草案/patch/manifest/profile不变，仍d6ddbff5…父cb679968；周五若tizen_base合归档补丁仍需变基并解spec冲突，本次未做。12给全部资源、失败原文与边界；wednesday-handoff/matching/stop及qualification.txt公开，10更新全部raw。

## 2026-10-14 修正顺序续跑：最新人工裁决与开工

PM判断：上次把含函数重排的正式参数用于无emit-relocs普通clang，BOLT按设计拒绝，是执行顺序错误，不是profile失配，匹配仍未知。本次取消普通clang独立探测；先保存配置bolt前的原clang链接字串，原地cache同树只加emit-relocs重链并LLVM strip-debug，再历史SHA1da7bb73…工具以正式参数完整重写，仅检查N/M/S/U/Q、R、S/N，早期产物用后删除且不作候选；5%双门禁失败即停、不建新工具。正式候选仍必须由本树新建llvm-bolt产生，配置前后clang链接命令逐字相同、CMake变化仅bolt相关、独立DESTDIR差集/exports门禁不变。其后30/90同实体对象、双模式/22RPM DWARF预期清单、30×5性能geom<0.98及sandbox直推条件继续有效；Gerrit拒绝原文停止、不拆profile。本顺序修正不豁免任何门禁。

三个关键SHA复核PASS：普通clang7df0ff90…、CMakeCache f7e93b87…、build.ninja9fcc8683…均未变。既有完整交接PASS沿用，不重新访问ARM树。新E=W/temp/bolt-v4-20261014-relink-first；根内新/home/abuild/bolt-work/bolt-v4-20261014-relink-first。普通bin/clang-22保留作对照；“原地重链”为在交接build执行、输出BOLT专用目录、原cache不改路径不复制，与spec重放方式一致。第一步重阶段进行中，后续结果按门禁逐步登记。

第一步PASS：唯一原链接字串已保存（SHA352a6f57…），只改输出/depfile、保留原cache字串并追加emit-relocs；链接8.840s、LLVM strip-debug5.376s、scope17.571s，kernel峰13.071GiB、最大采样VmHWM10211668kB。去debug输入SHA158275040dbaa71999f60a4b62e4dd9a23a58b4d72e7ff85fb3c5f5ebff064e4，226,738,888B；之前完整ELF3,560,483,168B。普通clang未变，cache仍47107/96877810360B，free60,410,531,840B；锁/proc/scope均回收。早期匹配下一步，不把本重链PASS冒充匹配PASS。

第二步早期匹配PASS：历史SHA1da7bb73…工具以全部正式参数对去debug的重链输入完整重写，N=23592/M=144032/S=0/U=1/Q=383，R=0.004238545%、S/N=0%，整数5%双门禁PASS，禁infer-stale。scope26.075s、kernel峰3.809GiB；早期产物用后已删除（非候选），日志/输出SHA保留；共享锁/proc/scope均回收。只有下一步本树新工具的正式产物可以成为候选。

第三步STOP_CMAKE_NON_BOLT_CHANGES：按草案同树一次cmake追加bolt，命令rc0/18.107s，但编译器变量变化导致CMake自动删cache并重新配置；681键变化，其中678非BOLT/项目列表。ThinLTO Thin→OFF、projects→空、targets→all、prefix /usr→/usr/local，严格“不超过bolt相关”门禁FAIL。配置后build.ninja无clang-22边，链接字串一致性不能通过；cache门禁处停止，没再运行ninja查询/dry-run/构建，llvm-bolt未产生。scope19.065s/峰0.677GiB/最大采样VmHWM328736kB。

**交接树的CMakeCache/build.ninja已被失败配置改写且未恢复**，停止SHA bd8ad3aa…/a37efa6a…，before/after快照在本次E；其他生成配置也受影响，不可直接ninja续跑，不能假定只覆盖两文件即完整恢复。本轮不修复重试，按停止规则只审计/报告。普通clang仍7df0ff90…；22RPM逐SHA大小及归档独立install证据元数据未变；cache规模47107/96877810360B不变，部分mtime由原地LLD访问改变，符合授权。锁/proc/scope全回收，未进入两棵ARM树。

当前完成范围：步骤1重链PASS（link8.840/strip5.376s，scope17.571s，峰13.071GiB、VmHWM10211668kB），步骤2早期匹配PASS（N23592/M144032/S0/U1/Q383，R0.004238545%、S/N0%，scope26.075s/峰3.809GiB，早期产物已删除），步骤3配置FAIL且未建新工具；正式匹配/正式流水线/DESTDIR/30+90对象/双模式与预期清单/性能/推送均NOT RUN。未向Gerrit推BOLT，不用历史候选顶替。源码草案及封套不变d6ddbff5…父cb679968，周五若mainline合归档补丁仍需变基解spec冲突，本轮未做。13与relink-first-stop/tool/relink/early-match给全部原文/资源。GitHub前两里程碑2bc142d/59899b7已推；本停止材料随后提交，raw索引更新。

## 2026-10-14 周三续跑二：原因诊断与临时布局错误STOP

最新PM前提：早期匹配PASS不变；此次比较original-rpm-build.sh完整环境/命令、失败入口、spec debug/release展开后才判断草案缺陷；临时不删cache/仅bolt差异/链接逐字验证PASS才恢复。恢复dry-run扣除已证明8触碰和LLDB头后≤50才-j1补完，>50允许历史1da7bb73后备；spec临时验证、候选、对象及性能geom<0.98仍是sandbox直推前提。原证据/22RPM/ARM树保护、Gerrit拒绝原文停与源父cb679968规则沿用。

只读诊断新增关键证据：原RPM登录PATH /usr/local/bin:/bin:/usr/bin:/usr/local/sbin先/bin；失败userspec入口PATH先/usr/bin，且未复用RPM前导。相对compiler cache clang/clang++因此从原/bin拼写变/usr/bin，两路径实际同inode。CMake模块非绝对compiler通过find_program定位，原日志触发变量明确CMAKE_C_COMPILER/CMAKE_CXX_COMPILER。三组完整命令/两宏展开/选定环境在cmake-recovery-diagnosis.json。判断选本地命令/环境与spec正常RPM环境不一致；初判spec缺陷在检查PATH前依据不足，已撤回，生产spec未改。spec无删cache/链接保持认证仍需临时实证，不把该判断当PASS。

第二步唯一临时baseline配置rc1：本任务仅准备llvm源链接却漏同级cmake/Modules，CMakePolicy/LLVMVersion include缺失、VERSION '..' invalid；是临时布局准备错误，未到追加bolt。按规定外停止，不补链/换源重试；临时失败cache/文件清单留E，自己新建temp-debug已删除，其他证据保留。两模式rpmspec展开PASS不替代临时配置门禁。无原树恢复、干跑分类、候选、对象/双模式/DWARF、性能或sandbox推送；草案/fixtures/本地提交/文本patch/manifest保持旧版d6ddbff5…，没有本次新增fixture PASS。

停止后审计仅修正一次错误的.ninja_log旧基线比较（可变生成记录，不是保护原件），必要清理审计PASS；22RPM与普通clang/source/spec/ar/lld SHA、归档证据元数据未变，原cache仍bd8ad3aa…/ninja a37efa6a…保持上轮STOP状态、未恢复。本次只4GiB轻任务，未取共享锁，proc/scope均回收，没有进入两棵ARM树，W tracked/llvm未写。E=W/temp/bolt-v4-20261014-cmake-recovery；根内新/home/abuild/bolt-work/bolt-v4-20261014-cmake-recovery。14给全部证据/未完成边界，raw随后更新。本任务状态STOP_TEMPORARY_SOURCE_LAYOUT_ERROR。

## 2026-10-14 周三续跑三：人工裁决与临时验证 PASS

PM确认删缓存源于本地PATH先/usr/bin、原RPM先/bin；spec同一RPM环境无此缺陷，不改草案。所有cmake/ninja必须用原RPM环境前导并记录PATH/which；临时原源码-S加新-B，不复制源码；准备性错误每类允许一次修正，同类第二次或产品门禁失败即停。原树恢复dry-run扣除已证明8触碰/LLDB头后≤50才-j1补完，>50走历史工具后备；候选/30+90对象/双模式/22RPM-DWARF/性能geom<0.98与sandbox父cb直推条件沿用。

第一步PASS：原PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin，四次cmake/ninja均which=/bin/clang及/bin/clang++；无删cache，追加仅13个BOLT相关差异，其中目录计数667→684经17个全部tools/bolt新增生成目录逐项证明。原clang链接命令与临时前后两边逐字相同（SHA352a6f57…），原源码元数据清单一致，临时目录已删除。使用一次cache-delta-classifier准备性修正：初版仅按键名误报派生目录计数，修正后须集合与数量证明；首轮证据保留，不放宽产品门禁。生产草案/源d6ddbff5/patch/manifest不改。15/rpm-env-temporary及四日志给全部记录。接下来恢复原树，尚无候选/性能/sandbox结果。

第二步STOP_RESTORATION_GATE：按原RPM环境与原始完整cmake参数仅恢复一次，PATH/which仍正确且rc0，但污染cache中的/usr/bin compiler改回/bin又触发删cache/默认重配。50关键项中41不一致，664完整cache键变化；Thin→OFF、projects→空、prefix /usr→/usr/local、targets→all。产品恢复门禁FAIL，按PM立即停止，不重试、不运行ninja干跑/分类/补完，>50后备条件未评估，无本次候选/SHA/正式匹配/30+90对象/双模式/DWARF清单/性能或sandbox推送。唯一准备性修正为第一步cache-delta-classifier的派生目录计数误报，不放宽产品门禁。

树仍未恢复，当前cache17f7fbc72b14f6b1a5116aa17622e0af244fe84f2e72ef1e32bba61d3ca32876、ninja c0068a3e42ae3b4303357000ddb6f30a0f72d46da704128277a052953ead4d42；失败配置开始以来923个时间筛选改写文件清单、原始命令/环境、关键项与完整cache差异、59,160,293B ninja差异均保存。15与rpm-env-stop/restoration/configure给证据。恢复cmake32.714s/scope35.128s，峰0.567GiB/VmHWM328556kB；均4GiB轻scope、无共享锁/重阶段，proc/scope回收。普通clang与22RPM逐SHA大小、归档证据元数据、源码前后清单全部PASS；cache47626/96880098760B原地使用、不复制（比开工+519/+2288400B，允许LLD写入）。free60543275008B。草案/源d6ddbff5/patch/manifest无修改，无新夹具PASS声明；本次未完成候选验证目标，在恢复产品门禁处停止。

## 2026-10-14 周三续跑四：PM后备路线与原树禁用

PM认定上轮没有先移开污染cache是恢复方法问题，不是新产品缺陷。已刷新的普通生成头mtime会触发大量对象重建，本周放弃恢复及树内工具路线；禁止在原树cmake/ninja（含-n），原树仅作只读输入来源，周五后定恢复/废弃。本周本地正式候选改为历史1da7bb735f7bc1afab9a863154260699b0b0f88c6fd05b99231dd21ef653fd5a工具；树内llvm-bolt构建与安装清理由Quickbuild验证，其余门禁不变。周四不要求Quickbuild/local clang SHA一致（前BOLT输入不同），核对日志N/M/S/U/Q、R、S/N同量级且5%双门禁及Quickbuild性能。准备性错误每类一次修正，产品失败即停；原RPM环境/记录要求、资源/保护与最终sandbox父cb直推条件沿用。

第一步PASS：保留13的emit-relocs+strip-debug输入，SHA158275040dbaa71999f60a4b62e4dd9a23a58b4d72e7ff85fb3c5f5ebff064e4/226738888B与原记录一致，不重放、不进入原树cmake/ninja。tool/profile/普通clang指纹PASS，新E=bolt-v4-20261014-fallback，轻scope12.049s。16与fallback-input给证据，后续尚未认证。

第二步后备候选PASS：历史工具按两模式展开的同一helper正式参数重写，N23592/M144032/S0/U1/Q383，R0.004238545%、S/N0%，禁infer-stale；BOLTnote/strip-all/前后各三目标/身份链PASS。最终SHA4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9。草案pipeline/main stdout JSON包含全部匹配统计，详细BOLT日志另存，未改草案。资源及路径见16/fallback-candidate/formal-bolt；第三步与对象/性能/推送资格仍待。

第三步STOP_PREPARATORY_COMMAND_CAPTURE_SECOND_ERROR：根内Ninja不支持compdb -a，使用一次采集准备性修正为显式全部规则；修正轮两次cmake及采集rc0，但compdb漏无输入CUSTOM_COMMAND（before2016/after2067），同类第二次错误即停，不再换采集器。全部边未认证；已采11405普通命令相同，86个普通配置产物相同，compile_commands聚合只追加BOLT。临时目录删、源码未变。

停止后快照只读诊断还证明清理覆盖FAIL：非BOLT安装规则不变，17新增BOLT安装脚本带7个/usr/lib64/libLLVMBOLT*.a（manifest/prune覆盖）及/usr/bin/perf2bolt、llvm-boltdiff两链接（指向llvm-bolt）。LLVMInstallSymlink不登记manifest，prune_install会拒绝两个未注册新增路径，现草案遗漏；47导出元数据仅额外检查的LLVMConfig.cmake变化且普通exports完整恢复覆盖。建议下轮绑定baseline/链接类型目标证据后清理两别名，最终inventory严格相同；本轮按约束不改草案。16及fallback-config-install/stop、两份完整配置tar.xz给四项结果/建议/原文。

原clang/22RPM/归档证据/源码与原树cache/ninja配置SHA审计PASS，未在原树cmake/ninja或刷新生成头；但临时配置沿用15原lto.cache预置，测试链接仍新增361文件1674072B（cache47987/96881772832B），未满足原树仅作输入来源意图，已如实记录，不再触碰原cache。下次临时配置用专用cache且不复制原cache。全部proc/scope回收、候选重锁已释；第四步对象/双模式/DWARF清单/性能全部NOT RUN，geom未知，sandbox未尝试。最终候选SHA4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9保留；源d6ddbff5与封套未改。周四核Quickbuild统计/双5%门禁及性能，不核local/Quickbuild SHA相等。

## 2026-10-14 续跑五（历史停止）

采用去掉第二次安装/compare-root，源a141父cb，103夹具PASS；全7439文本块当时未获PDB/配对phony许可而STOP。后续六/七PM许可已覆盖停止原因，原始差异不删。完整当时记录见17、dd7053a版STATUS；未冒充当时对象/性能已跑，未推sandbox。归档/RPM/原clang/源码/缓存保护PASS。

## 2026-10-14 续跑六（历史）

甲类7421块/6838普通语句PASS，两个PDB变量在2454规则中0引用；当时乙类只限RERUN_CMAKE，配对phony输出块未获许可而STOP。完整人工裁决、88/20全文、保护与资源见18及GitHub dd7053a中的本STATUS；该历史停止被后续PM扩充许可覆盖，原始证据不删。

## 2026-10-15 续跑七（历史）

7439文本/当前a141两模式展开PASS，120输入SHA准备PASS；两次辅助脚本路径查询错误触发当时准备STOP，后续对象等未跑。完整人工裁决/路径错误/资源/保护见19及GitHub dd7053a中的本STATUS。续跑八PM已调整查找错误规则，此历史状态被后续执行覆盖，原证据保留。

## 2026-10-15 续跑八（历史完成）

120完整对象、双模式mini、22RPM/DWARF预期清单、x86性能geom0.855890085 PASS；sandbox已更新并核对a1410e3d父cb，历史后备候选4ec保持。完整进度/资源/保护/四类准备修正见20及GitHub 053fe704中的STATUS。原证据不删；该资格不代表续跑九门禁认证。

## 2026-10-15 续跑九（进行中）

PM裁决及本轮边界见21：修门禁不改生成参数/4ec候选，源父a141；仅push bolt-v4，禁止Gerrit。QB默认开关保持开启；回退需新spec提交改bcond_with，不能改QB配置。第一步离线闭包1911边（普通1792/command1715、新增phony9、实际BOLT110=102对象+7库+1链接），精确描述白名单及固定NINJA_STATUS，109/109夹具PASS。准备入口cwd修正一次，详见21；后续待。

续跑九STOP_PROCESS_TIMEOUT_FIXTURE_SECOND_ERROR：健壮性修改后的138夹具137通过1失败，进程后代退出观察修正一次后仍见R，按第二次错误立即停，不再试。安全属性/宏链开关OFF比对/ARM与AArch64性能/真实新门禁全部NOT RUN，不能生成合格源提交。候选4ec、普通clang、禁用cache/ninja未变；22RPM/归档/源码保护PASS、原cache47987/96881772832B；scope已回收，无重锁/proc/CMake/Ninja/ARM树/Gerrit动作。源HEAD仍a141，未完成修复及manifest单独保存；生产prune移除，rsp证据无@不改代码。35新增测试方法；准备/查找错误、初次109单测未纳入cgroup偏差详见21及review-corrections/resources。保持QB默认开启，回退需新spec提交改bcond_with，正式说明必须注明。

## 2026-10-15 续跑十（历史完成）

146夹具、安全属性、宏链18段OFF字节相同、真实tiny/post反向/compare-root/tool-plan全部PASS，生成本地源97c060a父a141；未推Gerrit，后续十一A修署名并推。原4ec候选/参数不变、保护/资源回收PASS。三类准备修正各一次，详细原文见21和949734c版STATUS；不把canonical小spec展开冒充新RPM执行。

## 2026-10-15 续跑十一A：署名与sandbox

源仓库user.name/email均来自global /home/linhao/.gitconfig：liushanshan / ss0217.liu@samsung.com，未修改配置。单次-c amend/reset-author后，新源b7e61fb92b34795868230e4f9cee8e3ec65496f6，author/committer使用当时的历史署名（后续遵循下述长期规则）；父a1410e3d，tree ea70ea066dd16430b23c238d9654e1667479b960与97c060a相同，spec df1198d1…/helper4590b337…不变。文本补丁/manifest同步。sandbox查询前a1410e3d→无force快进推送→查询后b7e61fb92b34795868230e4f9cee8e3ec65496f6，确认成功；Gerrit仅提示subject>50字符警告，原文在manifest。未推评审/tizen_base，未做其他验证步骤。

## 2026-10-15 续跑十一B（历史完成）

ARM/AArch64性能均PASS：geom30 0.856351167/0.847699213；独立20与留出10、600样本/条件/保护见21及95a2955版STATUS。无源码/Gerrit动作，锁/proc/scope回收。

## 2026-10-15 续跑十二（历史STOP）

202夹具与真实历史候选新门禁PASS，d08父b7；overlay权限不足NOT RUN，第七步采集准备第二次失败STOP，未推sandbox。完整人工裁决/过程/保护与源码SHA见22和858c114版STATUS；PM材料补发ac299f4。十三A重新授权捕获计次，明确本轮不含真实树演练，故不以十二缺项阻塞本轮授权推送；历史证据不删。

## 2026-10-15 续跑十三A（历史完成）

ad8a2606父b7，214夹具、闭包111、完整22RPM/四post/真实门禁PASS，sandbox已推、QB未启动。完整裁决、资源、纠正与raw见[23](23_closure_post_certification.md)及43c6a3720606bb1f8ed79b666be726c929ba1f2b版STATUS，历史证据未删。

## 2026-10-15 续跑十四A（历史STOP）

源8be7348a6baf9d4b8b55c382b8a04dade712208d父67619ec8，RPM身份停止，sandbox未推。完整修复、252阶段夹具/宏/post及停止/发布纠正见24与ac56ad25aeda6a96ea5d9488c4b885e60a19d203版STATUS。十四B的PM裁决已解释为旧路径指向docs38产物，未发现产品问题；不删除历史证据。

## 2026-10-15 续跑十四B：PASS，新sandbox已推

PM裁决：docs35原22包在W/temp/archive-fix-v2-final-20261009/rpms-docs35，旧R/RPMS为docs38；十四A停止是来源路径问题，不是产品问题。逐包对照docs35附录A的字节/SHA后使用保全包，Source1005与67619ec8字节相同，spec差异不涉及.cmake安装/%files（%install起后文全相同），照常继续。两组历史包均不称作67619ec8新构建物。

最终压缩源506dc25c86e4e2154150796d10b77b71d71ad6bb，父67619ec8bbbac7238a6cfc33a481ccfbcd12206f；仅新增helper文件头维护说明，修改提交说明的内部流程/外部维护入口；可执行AST、spec/profile不变，Hao Lin作者/提交者/Signed-off-by及Change-Id保留。257/257测试PASS（252+安装顺序1+本轮4），最后两项日志诊断微调已覆盖，stdout2609字节含5条夹具JSON、stderr原文公开；完整二进制补丁独立index apply/tree PASS，公开--no-binary文本patch及单独Source，不再误发超限文件。

22RPM逐包身份PASS；完整合并根no_bolt_products 17722路径/47cmake，最终helper复查PASS。新压缩提交OFF debug20/release18段与新基线逐字相同，ON顺序snapshot<compare-root<转换<install且转换一次；四post平台段逐字一致、尾检最后；真实7df/4ec安全、tiny三目标、双根post/反向/compare-root、111计划正负例全PASS。4ec候选未重生成。受保护22RPM/归档证据/原坏配置/缓存/源码未变，锁/proc/scope回收。产品准备修正0次、产品门禁失败0次；发布准备三类各修正1次（stdout错误假设、忽略归档暂存、索引脚本目标路径），查找更正及完整原文见24。

维护完整版见maintenance.md（四remedy、运行前提、升级与重训、锚点、资料保留/崩溃/回退）；23已明确静态图边界与stdout实际内容（2600/2609字节的夹具JSON）。上次GitHub ls-remote已补核PASS。材料先GitHub公开并核验126 raw/远端后，无force新建sandbox/lhmax2025/bolt_pgo_v2，前空/后查已等于该源提交，旧sandbox/refs-for/tizen_base不动。QB/真实树演练/发布全构建及accel-worker身份仍NOT RUN，用户在PM审完后启动。完整状态/资源/原文见24和review4b系列。

## 2026-10-15 sandbox 收拢（长期人工裁决）

BOLT 在 platform/upstream/llvm 只使用 sandbox/lhmax2025/bolt_pgo，后续不再新建 sandbox 分支。变基更新仅该分支允许 --force-with-lease，租约必须写明当前远端完整 SHA；其他分支一律不得强推。

A PASS：以明确租约 ad8a2606ec3c9e53b657f3f8261be9f7d63b23c8 更新 bolt_pgo 至 506dc25c86e4e2154150796d10b77b71d71ad6bb，推后核验一致；bolt_pgo_v2 已删除并查询确认不存在。其他六个分支只登记，不删除。未改源码、未推 refs/for 或 tizen_base。B真实overlay安装演练见25及下文最终状态。

## 2026-10-15/16 真实树安装演练：时限中止

A PASS：bolt_pgo最终506dc25，v2删除，六个其他分支只列出，长期仅bolt_pgo规则已登记。B已运行但未完成：普通安装、preflight/certified、路径/proc、真实111 BOLT+2 TF计划和实际构建/tool-verify PASS；新llvm-bolt SHA34686c3362e736763cf0a1a6a44bb54b4d2e5cc34e58322477f2fa63696259fc，本次产出，TF前后同f15c565d…。

55分钟计算截止时clang emit-relocs重链仍在运行，监护按“shared lock 3300-second deadline, leaving 300 seconds for cleanup/audit”终止六个abuild进程，存活0；rpmbuild=-9。未观察到产品门禁失败，不能据此断言QB失败。匹配度/新候选/strip/tiny/security/compare-root/转换/后处理/post/no-work均NOT RUN。原缓存仅61文件14,977,512B，历史温缓存条件不等同。

持锁3374.417秒（56.240分钟）<60；18GiB/swap0/nice15/ionice3，scope峰11.102GiB、最大观测VmHWM10.410GiB，宿主最低可用5.581GiB、disk最低free236.253GiB，内存事件全0。卸载/进程/锁/scope全部回收；下层240,718路径清单和六SHA前后完全一致。上层完整保留至周五待用户处置，无源码/Gerrit评审/tizen_base/QB操作。准备估算与askpass环境各修正1次，首次只读准备未设cgroup偏差如实在25登记；图形实际输入一次。原始日志/分阶段采样/完整脚本、dry-run、tool-plan/tool-verify、TF与下层审计全部公开于25对应raw，Source父676不变。


## 2026-10-16：QB Source 条件屏蔽 Patch 修复（必需认证 PASS，sandbox 已更新）

长期规则：spec 的 Source 行一律无条件声明；每次提交 QB 前先 gbs export，再对 x86_64（BOLT 开/关）、armv7l、aarch64 解析导出的 spec。

gbs 实际导出已复现：旧506dc25的 Patch0–6处于 x86_64/BOLT 条件块，七条 patch 命令无条件。仅移动两行 Source，源提交 `af82efed1a688ba0877a4b4ca723922abbc96d20`，父67619ec8/Change-Id保持；helper/profile均未变。两份五项 Tizen rpm 认证全部符合预期（旧1过4失败，新5过），ARM实际 prep 0退出/七补丁全部应用，AArch64可选prep因额外认证未完成记NOT RUN，helper/profile均不变；sandbox 已按506dc25精确租约更新为af82efed1a688ba0877a4b4ca723922abbc96d20，推后指向一致；无 refs/for、QB操作或新分支。QB三份日志尚未收到。见 [26](26_source_order_parse_fix.md)。

发布材料固定于efb591178a7f52cf61d2e0719235d6858603a031，raw索引12–19；436个URL全量SHA核验PASS。完整diff、提交说明diff、准备错误/多次图形输入偏差均在26中公开；不得把通用包装器的CLI/计数器误报当作产品失败，也不得掩盖它们。


## 2026-10-16：仅重排提交说明，消除 Gerrit 长度警告

当前源提交 `e2463165829cc91b0a1d60a3e0f915a587865f70`，父 `67619ec8bbbac7238a6cfc33a481ccfbcd12206f`；与 af82efed 的 tree 同为 `f82d94e9a69255e339187a2fb63c7df6989e6a49`，源码 diff 为空，五项解析认证直接沿用 af82efed。正文去掉标题后空白归一完全一致，标题42字符、全文每行≤72字符，文件路径仅在逗号后折行，Change-Id/Signed-off-by原样保留。作者/提交者Hao Lin，未改全局配置。

指定租约af82efed更新bolt_pgo成功，推后为新提交，返回中没有warning；没有refs/for、QB操作或新分支。0000文本补丁仅更新元数据，diff载荷保持；完整cat-file、验证、远端原文见26末节与 tools/bolt/results/message-wrap-20261016。


## 2026-10-19：去掉磁盘门槛，诊断与原子安装；发布暂停

长期规则：发布代码不设磁盘空间门槛，只记录剩余空间；磁盘失败的诊断值必须在失败后由本次构建实际数据计算。本地开发机的资源、锁、磁盘规则只约束本地操作，不得进入发布代码。

历史未采用草案e97171ff：本地285测试PASS，唯一图形认证失败，Tizen五项NOT RUN，未推sandbox。其普通步骤包装与25处审计已被下节收窄修订取代；原文保留在27前半和67b0227材料钉提交。

## 2026-10-19：收窄磁盘诊断范围（认证及推送PASS）

长期规则：rpm 以 sh -e 执行脚本段；BOLT 改动不得改写普通构建、基线 %install 步骤和平台后处理链的执行方式。

直接在e2463165 amend为 `9e5675f57d122549997caffa39b655dfefc46fee`（父67619ec8，Hao Lin/原Change-Id），不叠加e971。%build全段9331B、基线install1895B、实际平台链304B逐字节相同；只允许尾检-B及末尾report，8个BOLT shell动作包装。call恢复直接日志，无线程/管道、不检查成功日志文本；诊断disk/not-disk/unknown，日志不可用不猜测。289测试、三类加unknown、sh-e rc1、gbs export及构建根Tizen五项全部PASS。一次图形认证，锁171.4秒，overlay/proc/dev卸载完、下层清单及六SHA不变；未运行原树cmake/ninja/-P。材料de32b57先GitHub，304raw核验PASS后以e246精确租约更新唯一bolt_pgo，推后已等于该源SHA；无refs/for、QB或新分支操作。详见27末节和narrow-disk-20261019。


## 2026-10-22 磁盘测量：输入准备完成，完整补测未启动

用户已释放内存，准入采样 MemAvailable 约23.95GiB，满足准入。固定Base 20261013.024319的build.conf已下载并按repomd压缩前后SHA验证（解压e5187fd7…）；专用gbs_llvm_qb1202084.conf仅指定base packages/debug，原W/gbs_llvm.conf未改。源树仍干净9e5675f，尚未改清理逻辑、无新源提交/候选、无Gerrit/QB动作或新分支。

历史无BOLT完整构建582份du采样最高236,149,145,600B（219.931GiB），三权限盲区及打包末段缺采，因此只是下界；不同于本次快照及开关OFF。25号中止演练当前工具+工作+cache上层条目12,247,695,360B（11.407GiB），不是完整BOLT增量峰值。旧upper约65GB还含普通安装，旧普通缓存约96.9GB也不能归给BOLT。ON/OFF净增峰值尚未知，未满足条件，不执行删除。

目的盘当前可用229,464,346,624B；以历史OFF下界+本地30GiB保留量作准入参考需268,361,400,320B，差38,897,053,696B（36.225GiB），还未计BOLT/导出。该参考不是新快照精确需求；容量未覆盖参考，完整构建未启动，没有持重锁或编译进程。补测/清理/清理后全构建、RPM对比、五项解析全部NOT RUN。本地容量规则不进发布代码；旧树/保全证据不删。29及disk-footprint-20261021给原始采样副本、当前du、输入来源、缺项、生命周期边界与续测方法。


## 2026-10-22：构建根只读盘点，等待逐项清理裁决

完成 [31_build_root_inventory.md](31_build_root_inventory.md)：三块已挂载本地文件系统扫描、88个候选独立du，列95个>5GiB根/重要子目录（父子项不可相加）。保全17个关键资产大小/SHA，核实22RPM硬链接；权限盲区原样报告。末次可见lsof/fuser无根句柄，未见活动overlay/项目锁，不能据此解除保护；main patch/hybrid、Rnew/N/N38/H、两ARM树、var/tmp交接树继续建议保留。

待用户批准：P1/P2/P3三个可重建解包目录合计135.852GiB；P4旧演练upper为可选项，先保全14文件约2.360GiB，四项合计预计净释放194.022GiB。全部在/home；全采用时预计可用407.647GiB，/var/tmp仍约46.524GiB，不能相加。P4有root所有的0755目录，本轮没有提权/改权限。29的完整补测仍未启动。

未删除、移动或修改任何构建树；未运行cmake/ninja/构建；未改源码/spec或QB、未访问Gerrit、未新建分支。只发布盘点与原始读数；下一步等用户逐项确认。证据目录 tools/bolt/results/root-inventory-20261022/，数据一致性检查全部PASS，不是产品构建认证。


## 2026-10-22：批准目录清理——P1已删，P2/P3按前置条件跳过

用户仅批准31号P1/P2/P3三个可重建解包目录，要求任一检查不满足就跳过；P4 upper未批准。普通用户复核realpath、父目录非链接、/dev/sda1、lsof/fuser和全量可读mountinfo后，P1检查通过，于19:34执行唯一一条 `rm -rf --one-file-system -- .../bolt-v4-20261015-review3/payload-merged`，rc0、无错误/残留。

P2/P3未删：P2仍由review4b/real_gates.py:46及install-rehearsal/disk_budget.py:4读取；P3仍由validation/expected.py:22/28/49/50读取，无法通过“没有其他脚本依赖”的前置条件。历史可重建性不替代本次条件，未修改这些脚本来绕过检查。

/home可用从229,374,218,240B增到279,041,572,864B（259.878GiB），实测释放49,667,354,624B（46.256GiB）；未达到三项预计135.85GiB，因为P2/P3的89.595GiB保留。三个父目录其余1878个普通文件的SHA/元数据逐项相同，P4、原RPM、.ii输入、其他构建根保持。未构建、提权、改权限、新建分支或访问Gerrit。详见 [31 执行记录](31_build_root_inventory.md#7-执行记录用户批准三项删除-p1跳过-p2p32026-10-22) 与 tools/bolt/results/approved-root-cleanup-20261022/；本轮结束，等下一步指令。


## 2026-10-22：用户豁免历史脚本引用，P2/P3已删除

用户确认review4b/real_gates.py、install-rehearsal/disk_budget.py、validation/expected.py均为已完成的一次性脚本，不会再运行；仅对P2/P3豁免无脚本依赖条件，重跑前须先从保留的原始22RPM重新解包。脚本本身未修改、移动或运行。其他前置条件重新检查全部PASS：realpath精确一致、本身及父目录非链接、/dev/sda1、lsof/fuser无命中、mountinfo与overlay无引用。

20:07普通用户分别对review4b/payload-merged、validation/baseline-extract执行精确范围的 `rm -rf --one-file-system --`，均rc0且无残留。实测释放96,201,940,992B（89.595GiB）；/home从278,610,055,168B增至374,811,996,160B可用（349.071GiB）。连同P1，三项分次实测释放135.851GiB。父目录其余1574个普通文件及三个历史脚本的SHA/元数据全部保持，P4 upper仍未批准且未动，原RPM和.ii保留。无构建、提权、权限修改、Gerrit或新分支操作。

详见 [31号文档7.4](31_build_root_inventory.md#74-用户豁免历史脚本依赖后执行-p2p32026-10-22) 与 tools/bolt/results/approved-root-cleanup-p2-p3-20261022/。本轮完成，等待下一步指令。


## 2026-10-22：cache-release 实现通过，本地双轮测量进行中

本地 amend d20e873b2c7dfac10fab9235e2b781dad08dc4c7，父67619ec8/Change-Id保留，未推Gerrit、不新建分支。spec仅compare-root后新增三行；helper新增安全限定路径、尽力释放且预期错误返回0的新命令。299测试（新增10）及五项Tizen RPM解析PASS，disk-report/diagnose无需修改。9e5675f基线在/home本次新根开始普通编译，修订轮尚未开始；实测峰值、候选/RPM一致性仍未确认。首次tar模式缺少预导出已按准备性规则修正一次，原始失败保留。完整状态见32；不得将此在跑状态当作完整构建认证。


## 2026-10-22 23:23：cache-release 双轮测量因内存准入超时停止

源提交仍为 d20e873b2c7dfac10fab9235e2b781dad08dc4c7，仅本地，未推Gerrit；299测试及五项Tizen RPM解析PASS。第一轮9e5675f只完成到普通LLVM链接，最后3275/3534，未进入BOLT或install；第二轮未启动，candidate/RPM一致性和实际磁盘降幅均未验证。

续跑段持锁3203.387秒后确认cgroup冻结并释放锁；冻结保留约14.1GiB内存。随后60分钟的准入采样仅约7.56–9.89GiB可用，未达12GiB，按规则停止。cgroup峰值16GiB，oom/oom_kill均0；此前LLD有文件页I/O等待。所有本次构建/监视进程退出，新根5个挂载已卸载、无残留；完整新根和对象保留，没有删除任何历史根或缓存。

完整chroot最高局部采样27.383GiB只是未完成普通构建的读数；单次du最长1008秒，不能称为整轮/连续峰值。详见[32_cache_release.md](32_cache_release.md)及cache-release-20261022原始日志。暂停/直接RPM续跑与不中断GBS有差异，均已记录；本轮停止，不以未完成基线启动第二轮。

## 2026-10-23 cache-release双轮测量续跑与临时内存裁决

用户释放内存后，第一轮9e5675f在本任务新根baseline-root恢复；普通构建尚未完成。01:45:30 CST用户明确批准本次两轮本地测量使用20GiB cgroup上限（原16GiB），已调整本轮并为第二轮使用同一限额。swap0、运行中MemAvailable<3GiB停止、锁与其他本地规则不变；不进入发布代码。源提交仍为d20e873b；既有299测试/五项解析PASS，不代表双轮完整构建认证。详见32第9节，当前进行中。

同日后续用户裁决覆盖上面的20GiB上限：取消本次测量的cgroup内存上限与内存准入等待，已设置MemoryMax=infinity；冻结续租已恢复，同一普通链接现场继续。锁/磁盘/代码边界不变，详见32第9节及memory-unlimited.json。


2026-10-23 03:49进度：第一轮普通构建356/356和普通安装完成，BOLT实际tool-plan/执行均113项（111BOLT+2TF），工具实物复核通过。tool-built BOLT自有占用3.762GiB（含cache新增1.120GiB）；正在重链，尚无完整candidate/RPM，不能宣称完整增量或释放收益。MemoryMax=infinity、无内存准入续租；最新持锁3200.228秒后冻结/释放/恢复成功。全根du历史竞态缺口、修正和原始读数均存证，见32第9.1节。未访问Gerrit/QB，未删除任何构建根。


## 2026-10-23 05:21：cache-release首轮完整构建PASS，第二轮待运行

9e5675f首轮rpmbuild rc0，22二进制RPM+1源码RPM；真实工具计划/执行113项、pipeline、compare-root、225静态库转换、post全部PASS。candidate为历史同一4ec07159完整SHA。BOLT四次报告自有占用0/3.762/4.345/4.346GiB；完整chroot已观测峰值224.718GiB在静态库归档安装阶段，du缺口/长扫描限制明确保留。

全部23RPM和关键二进制/报告已逐文件SHA保全（28009文件，11.96GB）。仅清理本次首轮新根的lto.cache腾空间，其余树和历史目录不动；/home可用354.50GB，足够第二轮。/proc因用户VS Code PID4237句柄暂未能正常卸载，未强制卸载/终止编辑器；devpts、devshm已卸载。该挂载清理待用户释放，第二轮不依赖删除它。详见32第10节。新源仍d20e873b，仅本地；299测试/五项解析PASS，双轮比较尚未完成，无Gerrit/QB操作。


2026-10-23 07:38：第二轮d20e873b在独立revised-root完成普通构建7634/7634，进入%install；固定输入SHA已核对。全程无内存上限/准入/低内存冻结，两次共享锁续租成功。首轮已保全，第二轮缓存释放、候选/RPM和峰值比较待完成；详见32第11节。


2026-10-23 08:15：第二轮113项工具计划/实物、pipeline、compare-root全部PASS，候选与第一轮同为4ec07159。新增cache-release实际删除47717文件，释放98180882432B（约91.44GiB），耗时29.205秒；随后原有Source1005正常开始。尚待静态库转换、post、打包和两轮RPM逐文件对比；不得把局部释放量称作整轮峰值降幅。详见32第12节。


## 2026-10-23：cache-release双轮完整测量完成

用户取消内存上限、准入和低内存冻结后，本地第二轮正常完成；共享锁仍按小于60分钟分段续租，swap0/nice/IO与本地磁盘规则保留，均未写入发布代码。9e5675f首轮及d20e873b修订轮均完整构建成功，各22二进制RPM+1源码RPM，产物已保全。299测试、五项Tizen RPM解析和真实113任务白名单/工具实物、匹配、安全属性、tiny、compare-root、225归档转换及post全部PASS。源提交d20e873b2c7dfac10fab9235e2b781dad08dc4c7仅在本地，没有推Gerrit或操作QB。

真实cache-release回收98,180,882,432B（91.438GiB），47,717文件，29.205秒。BOLT固定报告自有占用峰值约4.35GiB，整根BOLT期间增量观测6.58–7.07GiB；未跑BOLT-OFF第三轮，不冒充ON/OFF因果差。整轮观测峰值224.718→215.484GiB，下降9.233GiB；首轮有2.065GiB中断链接残留，扣除后的改善估算7.169GiB。平台后处理阶段峰值下降90.476GiB，post结束读数下降93.500GiB，扣除已知残留后估算91.435GiB。du存在长扫描/竞态缺口，全部按观测值报告。

两轮candidate同为4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9。22二进制RPM清单及非时间元数据一致；19包全部文件SHA相同，另3包271个.a仅ar头时间戳不同，所有成员内容相同。源码RPM仅helper/spec变化，导出spec另有GBS自动VCS提交号；所有差异原文保留，未声称RPM容器逐字节相同。

第二轮所有构建/采样服务已退出、挂载已清理；首轮proc仍被VS Code PID4237 FD48/49占用，未强制卸载。只删除过本次首轮新根的缓存腾空间及第二轮产品命令释放的缓存，历史树未动。详见32第13节及原始证据。任务完成，停止并等待下一步指令。


## 2026-10-23 19:17：cache-release 异常处理修复任务停止于挂载检查

首轮 baseline-root 的 proc 仍被 VS Code PID **202760** FD **48/49** 持有；lsof、fuser 均命中，/proc/fd 复核一致。按用户“仍然被占用就停下”要求，未尝试 umount、未结束占用进程、未删除根；后续修复、300 测试、导出、五项解析与 sandbox 推送均 NOT RUN。源提交仍为 d20e873b2c7dfac10fab9235e2b781dad08dc4c7，本轮仅追加停止证据。见 32 第14节和 tools/bolt/results/cache-release-exception-20261023/。等待用户释放占用。


## 2026-10-23：cache-release 异常兜底修复已认证并推 sandbox

按用户独立授权，首轮 baseline-root 的唯一 proc 挂载通过 chroot 内 `umount -l /proc` 成功脱离，findmnt 确认该根下无残留挂载；未终止进程、未删除根或修改 VS Code 配置。此前第14节停止条件现已按新授权处理。

在 d20e873b 上 amend 为 **3d3b4bf564fd8edec793e49e6de75b5fa7007d16**，tree **1143bd87650ddf8c8ed5ca40c0643c58c82db5ca**，父67619ec8与Change-Id不变。仅 cache_release 外层 except Exception 和解析注释；另补 IndexError 测试。300/300测试、GBS export、Tizen RPM4.14.1.1-1.7五项解析全部PASS；spec逐字节未改，其他helper函数未改，不重跑完整构建，第13节双轮结论沿用。

已用精确租约把 sandbox/lhmax2025/bolt_pgo 从9e5675f更新为新提交，推后ls-remote一致；没有推refs/for或操作QB。QB使用 `platform/upstream/llvm@3d3b4bf564fd8edec793e49e6de75b5fa7007d16`，由用户启动。详见[32第15节](32_cache_release.md#15-2026-10-23懒卸载cache-release-异常兜底修复与-sandbox-更新)和 tools/bolt/results/cache-release-fix-20261023/。


## 2026-10-24：BOLT on hybrid 本地完整构建与验证 PASS

本地 detached 提交 `aa637c1b4a0f9ea9f6f0317cf035126eba85aeb7`（父6e9d4f2，cherry-pick3d3b4bf），无冲突、无源码额外修改，未推Gerrit。五项Tizen解析PASS；llvm-bolt仍静态链接LLVM，原111+2白名单实际planned/executed=113，无需改白名单。profile N23592/M144032/S0/U1/Q383，R0.004238545%，与静态参考相同；pipeline、安全属性、tiny、compare-root、post全部PASS；cache-release释放20.138GiB。22二进制RPM+1源码RPM，30TU×3目标完整.o 90/90相同。完整根已观测峰值64.055GiB（hybrid66.696、全静态+BOLT224.718；采样缺失与历史差异详见33）。本次根与products保留供性能测量；candidate SHA `8b799f18e2bc37269385db125c881609e8457de1dd179f5d9d0ff9f557b58d16`。资源按本次用户放宽规则，无OOM/冻结/重试；完成后停止。见[33号报告](33_bolt_on_hybrid.md)。


## 2026-10-24：hybrid+BOLT 已推统一 sandbox，等待用户启动 QB

按用户授权，用精确 `--force-with-lease` 将 `sandbox/lhmax2025/bolt_pgo` 从 `3d3b4bf564fd8edec793e49e6de75b5fa7007d16` 更新为 **`aa637c1b4a0f9ea9f6f0317cf035126eba85aeb7`**；推后 ls-remote 确认一致。tree 为 `1c52e7922a5ae112b96dc18c297ed2dff58aa218`；父 hybrid `6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2` 及其 Change-Id 保持原样，再上一层为 `67619ec8bbbac7238a6cfc33a481ccfbcd12206f`。署名、BOLT Change-Id 与干净工作区检查全部 PASS；33号报告的导出、五项解析及本地构建认证针对同一提交，直接沿用。

推送退出 0，无警告；未修改源码、重做构建、创建分支、推 refs/for 或操作 QB。命令、原样输出与前后远端记录见 [33 第10节](33_bolt_on_hybrid.md#10-2026-10-24授权更新统一-sandbox-分支)。QB 软件包：`platform/upstream/llvm@aa637c1b4a0f9ea9f6f0317cf035126eba85aeb7`。已完成授权推送并停止，由用户启动 QB。

## 2026-10-25：C / C++、-O2 / -Os 性能补测完成

- 报告：[34_perf_c_o2_os.md](34_perf_c_o2_os.md)；原始证据：`tools/bolt/results/perf-c-o2-os-20261025/`。
- 静态组 `06c94072…` / `4ec07159…` 与 hybrid 组 `d5090159…` / `8b799f18…` 均完成；保全原件 SHA 不变。20 个本机 zlib/minizip C 文件、20 个独立 LLVM C++ 文件，三个历史 Tizen 目标；固定 CPU 2、单编译、关闭 ASLR、每侧五次，角色按轮交替。
- HQ 表：C -O2 节省 12.06%–13.91%，C -Os 12.67%–14.45%；C++ -O2 14.91%–15.44%，C++ -Os 15.52%–16.35%。hybrid 和静态组收益接近。静态 x86 C++ -O3 比值 0.851867（节省 14.81%），与历史约14%–15%相符；历史30条目与本轮20独立源权重差异已另列。
- 主矩阵6000次，加独立去无效 -I 的C补测2400次，共8400次全部退出0；7560份非参考输出做完整字节比对全部相同，保留 .GCC.command.line。所有原始样本保留，HQ采用主矩阵C++与无警告C补测。单侧计时试运行149条另存，不混入配对结果。
- 限制与处理：C仅覆盖zlib/minizip；预处理在宿主通过Tizen loader及只读sysroot执行，未进入chroot；C++沿用已有-O3预处理输入。原C命令的无效-I警告、计时器准备修正、补测计时外fsync及历史ASLR差异均披露。各次负载与频率原始值完整保留，无异常样本剔除。
- 本轮只测量并更新证据，没有修改生产源码/spec/helper、构建软件包、推送Gerrit或操作QB；生产工作树仍为干净的 `aa637c1b4a0f9ea9f6f0317cf035126eba85aeb7`。结果提交仅推GitHub bolt-v4，完成后停止。


## 2026-10-26：W/temp 只读清理盘点（38）

完成 [38_temp_cleanup_inventory.md](38_temp_cleanup_inventory.md)，原始材料在
`tools/bolt/results/temp-cleanup-20261026/`。本轮没有删除、移动、改权限、提权、挂载、构建或推送 Gerrit；仅提交 GitHub bolt-v4 的文档与证据。

- W 可见实占 1011.690 GiB，其中 temp 1004.114 GiB；覆盖 140 个一级目录、481 个细分范围，逐项分析 42 个大于 5 GiB 的 temp/var-tmp 目录。65 条遍历权限错误保留原文，大小可能是下界。
- /home 当前可用 149.060 GiB；稳妥方案预计净释放 256.833 GiB、执行后约 405.893 GiB；激进方案预计净释放 398.888 GiB、执行后约 547.948 GiB。均已扣除 5.517 GiB 保全预算。只有38号第3节的精确子范围属于建议，不整删任何混合父目录。
- /var/tmp 位于另一块盘：可用 46.446 GiB；两方案分别净释放 90.322 / 136.621 GiB，执行后约 136.768 / 183.067 GiB。不得与 /home 相加。
- products、90份TU、34号C/C++输入、profile、QB配置、源码/工作树/工具/已提交证据全部保留。hybrid+BOLT根若将来获准删除，须先保全测量用Tizen运行库和resource-dir；旧脚本未来重跑要改指保全路径。
- docs35、docs38、docs49各22个原始二进制RPM均仍在，66/66 SHA与原报告一致。可恢复载荷仅列入激进建议；未重新解包验证。
- 当前可读lsof/fuser与mountinfo未见建议范围被使用；有权限可见性盲区，删除前须再核查。root属主/不可写目录已单列，本轮不提权。
- P1–P3已不存在；P4旧upper也不存在，旁有preserved-from-upper。本轮未找到解释P4后续处置的记录，不推测操作者、不把旧60.530 GiB再计入收益。runpath-fix-20261026当前不存在；以后创建时整目录保留。

**所有建议等待用户逐项批准，当前没有删除授权的自动延伸。**


## 2026-10-26：38号批准范围清理执行

用户明确批准10个精确范围；先保全，再逐项核对并删除。结果见[38号第9节](38_temp_cleanup_inventory.md#9-执行记录用户批准的10个精确范围2026-10-26)及 `tools/bolt/results/temp-cleanup-20261026/execution/`。

- CLEANUP FINISHED 2026-10-26T18:59:43+08:00 status=partial deleted=9 skipped=1
- /dev/sda1 /home：保全前可用145.197 GiB，结束456.414 GiB，净增311.217 GiB。
- /dev/nvme0n1p1 /：保全前可用46.436 GiB，结束181.637 GiB，净增135.201 GiB。
- 保全清单及SHA256SUMS已生成；products、TU/C/C++输入、profile、QB配置、源码与不确定范围保持。未运行构建、未推送Gerrit。
- 已据用户说明与原日志补记10-22晚间旧R1/旧archivefix缓存及P4 upper清理，日志340→500 GiB；14个保全产物及SHA256SUMS仍在。
- 本次授权仅这10项，不延伸到其它目录。完成后停止。


## 2026-10-26：revised-root 单路径清理完成

- 用户再次批准38号第2项；保全SHA256SUMS 124/124通过，没有重新复制。
- 修正一次对无关snap命名空间警告的分类，重新检查无进程/挂载引用；先普通rm，再通过图形sudo清理root权限残留。没有删除任何其它路径。
- /home删除前可用456.395 GiB，删除后539.413 GiB，df净增83.019 GiB。父目录、products及保全目录仍在。
- CLEANUP FINISHED 2026-10-26T21:51:27+08:00 status=ok path=revised-root
- 详情见[38号第9.5节](38_temp_cleanup_inventory.md)，原文在 `tools/bolt/results/temp-cleanup-20261026/revised-root-followup/`。本轮完成后停止。


## 2026-10-27：RUNPATH / 工具并行 / real 门禁（37）——RPM内容门禁停止

- 本地 detached amend `ac112ebfd6e7983bdfd4c38dd156e6baba72731b`，tree `581bc4d92752ee7e2de9f7aa70d79cb174c3293b`，父 hybrid `6e9d4f2`，Change-Id不变。只推GitHub证据，不推Gerrit/sandbox。
- 317项夹具、五项Tizen rpm解析、OFF两模式逐字节展开全部PASS。完整本地构建返回0，22二进制RPM+1源码RPM，cgroup峰值14.999GiB，无OOM。
- CMake RPATH_CHANGE及安全/布局检查、tool-plan/tool-verify 113/113、profile双门禁、tiny、compare-root、缓存释放、post全部PASS。RUNPATH精确为`$ORIGIN/../lib64`，无RPATH/构建路径/空项；最终candidate SHA `963f1163fa983737a43ec5b4bd04fa142a4236829dee290b23feeda28abd1c9e`。
- 三处real共24/24对、52.61秒。llvm-bolt纯构建108秒，上次原日志337秒；begin→compare-root883秒，上次1201秒。不同运行条件，不声称全部差值来自并行。
- **停止**：独立RPM比较在compiler-rt包发现45个.a完整SHA不同。只读诊断证实仅ar头内部日期变化、成员内容一致；没有自行放宽严格内容门禁。其它未比较包、90TU、old-text、RSS均未继续。
- 根`W/temp/runpath-fix-20261026/gbs-root`及`products/`保留，观测峰值67.519GiB，122有效/4缺失du样本。日志移动造成一次采集路径修正，错误和修正均保留，不属于产品断言失败。
- 详情：[37_runpath_and_improvements.md](37_runpath_and_improvements.md)，证据`tools/bolt/results/runpath-fix-20261026/`。待用户裁决ar内部日期的验收口径；old-text是否采用、崩溃定位方案继续挂账。


## RUNPATH续跑验收（2026-10-27）

用户裁决：仅当ar成员名单/顺序、逐成员SHA、日期字段外全部字节均一致时，允许内部日期差异；单列统计，不并入内容相同。此规则仅在结果目录比较脚本中实施，发布spec/helper不变。

23RPM PASS：clang-22及源码spec/helper为允许内容变化；271个包内条目（270独立路径）的ar日期差异单列。最终candidate和old-text各90/90对象一致，45个native跳过归档全部成员为x86_64 ELF ET_REL、无bitcode。old-text体积减少30,691,864B（16.75%），三方速度及六组RSS已完成；Git解包干扰轮次完整保留并整轮补测，详见[37号第10节](37_runpath_and_improvements.md#10-续跑验收2026-10-27用户批准-ar-日期差异单列)。

源码ac112ebfd6e7983bdfd4c38dd156e6baba72731b保持clean；没有重构建、改发布参数、删除根、创建分支或推送Gerrit/sandbox。old-text是否采用仍待用户决定。


## 2026-10-27：采用 -use-old-text（39，已完成）

**已闭合：用户已决定采用 -use-old-text，不再挂账“是否采用”。** 崩溃定位方案仍挂账。新 detached BOLT 提交 `f308fe08eeaad4e219f8505449b88bd5f644ea8c`（父 hybrid `6e9d4f2`）仅在 OPTIONS 末尾追加此参数；spec/profile/白名单及其它发布代码不变。318项测试、gbs export、五项Tizen rpm解析、OFF debug/release逐字节比对均PASS。新根 `W/temp/oldtext-final-20261027/gbs-root` 完整构建及全部身份/RPM/90TU/RSS认证均已PASS，并按指定租约推送sandbox；详见[39号报告](39_use_old_text_final.md)。QB由用户启动。


### 39号主机重启续跑（2026-10-27）

普通构建在6,614/7,633处因主机重启中断，未进入BOLT；用户明确授权控制资源后继续。内核日志未发现OOM kill证据，不能断言原因。源提交f308fe08和tree不变，输入SHA复核PASS；同一新根以正常`rpmbuild -ba --noprep`续跑，原环境/宏/spec不变。最新本地限额：20GiB、swap0、CPUQuota1200%/20逻辑CPU、nice15、ionice idle；不进入发布代码。独立监控已处理可选io.stat缺失，原错误保留。该记录为恢复时状态；后续全部产品门禁完成，最终结果如下。


### 39号最终认证与sandbox（2026-10-28）

- 完整构建22个二进制RPM+1个源码RPM；tool-plan/tool-verify 113/113、profile、strip、tiny、24项real、安全属性、RUNPATH、compare-root、cache-release、post全部PASS。
- 精确profile N23592/M144032/S0/U1/Q383，R=0.004238545331242318%；strip-all后、RUNPATH调整前SHA为13a07cb7f84bd1ceda4d851c8bd71bddf7ef0c2d4864892eba64cbbb9a0350b8，大小152532296B。最终clang SHA 8c2429d870f421a29a9914458bc4d4ff2ce359a15e0bdd20f39bfb4580c40bdf，RUNPATH精确`$ORIGIN/../lib64`。
- 23RPM许可外内容差异0；271个归档日期条目单列，mtime2471项单列；clang-debuginfo内容不变。ELF限定区域外逐字节相同；90/90 TU PASS。
- 1200次RSS测量及对象检查PASS，整批无持续外部干扰。candidate/ordinary六组RSS比0.625825–0.942891（降低5.71%–37.42%）；begin→compare-root842秒，37号883秒，不将全部时间差归因于参数。
- BOLT源提交f308fe08eeaad4e219f8505449b88bd5f644ea8c，tree214bd2ff9ec7680e045b36b5b8c7e873e953846d，父hybrid6e9d4f2不变。以aa637c1显式租约推送sandbox/lhmax2025/bolt_pgo成功，推后ls-remote一致；未推refs/for、未创建分支、未操作QB。
- 本轮根/products全部保留；构建结束的普通/proc卸载因busy失败，未强制/懒卸载或结束占用进程。续跑cgroup OOM计数0。源码/所有发布参数除OPTIONS追加flag外不变。
- “是否采用-use-old-text”已闭合；崩溃定位方案仍挂账。QB：platform/upstream/llvm@f308fe08eeaad4e219f8505449b88bd5f644ea8c。


## 2026-10-28：41号崩溃定位探测

探测已完成，待用户决定；崩溃定位方案仍挂账。现行BOLT栈20有名/7地址，符号表版+symbolizer为24/3；完整符号表版离线24/24 clang地址成功，15/15对象一致。三个ELF均无GNU build-id；hybrid原调试文件1,652,177,424B，本轮BOLT debuginfo没有clang-22.debug。符号表版增大33,142,648B。**部分完成项：llvm-objcopy --only-keep-debug发生SIGSEGV，symbols-only大小/解析未完成**；没有改代码或换方案掩盖。详见[41号报告](41_crash_localization_probe.md)。


## 2026-10-28：40号perf/AutoFDO能力探测

硬件arch_lbr、cpu_core/cpu_atom各32条分支能力可见；普通用户perf_event_paranoid=4，带/不带-b的cycles:u均拒绝（rc255），未采到有效数据。/usr/bin/perf缺当前6.17.0-1033内核工具；只读使用已有perf7.0.14也被权限拒绝。llvm-profgen/perf2bolt/llvm-profdata存在、版本可运行，但profgen转换因无数据NOT RUN。部分完成，不提权、不安装、不改系统配置，详见[40号报告](40_perf_autofdo_probe.md)。


## 2026-10-28：外部评审材料包

以只读确认的sandbox f308fe08为准，发布patches/review-20261028/：hybrid6e9d4f2的0001、BOLT f308的0002（显式--no-binary）、8个改动文本文件完整最终版、第三轮后变更说明、hybrid首次外审摘要、README/raw索引/SHA256SUMS。Source1200仅列文件名、9,735,212B和52fd8522…SHA，不含二进制内容，包不自包含构建输入。41符号文件失败和40权限限制均透明链接；源码/提交未改变。本轮仅推GitHub bolt-v4，发布后按README逐个检查raw链接。


## 2026-10-28：42号崩溃定位根因与临时方案

LLVM only-keep-debug 的 PT_PHDR 越界写已实证：旧偏移140,509,184、写728B，而输出缓冲区仅35,243,528B；37/39两种BOLT都崩溃，ordinary正常，非old-text独有。原始ELF范围/对齐检查无异常，GNU objcopy和平台eu-strip均可分离符号。方案甲GNUdebug文件33,147,264B，debuglink后clang仅+104B、RUNPATH与ALLOC内容保持、15/15 TU一致；新临时chroot中的已有Tizen LLDB自动加载标准debug路径，21个clang帧全有函数名，显式symbolizer24/24。自动symbolizer经主文件debuglink仅19/24，不夸大。平台列表与自动拆包规则支持手工debug文件归入clang-debuginfo，但本轮未重打包。方案乙因带DWARF重链输入已被strip-debug就地覆盖，按要求NOT RUN，未重新链接。临时proc已正常卸载，既有输入SHA不变，源码/发布代码未改。崩溃定位：根因和函数名临时方案已验证，正式集成及源码行仍挂账；详见[42号报告](42_crash_localization_rootcause.md)。


## 2026-10-28：44号 QB 1210836 / 1211014 失败分析

两轮请求均为f308fe08，子构建分别1210837/1211018，在不同worker上同因失败：armv7l/aarch64/x86_64项目均报 `broken repository 'DOD:Tizen-Base/standard' is unavailable`，尚未进入LLVM包编译。日志创建DOD:Tizen-Base-Toolchain、主项目却引用DOD:Tizen-Base；此名称/引用差异已确认，具体生成缺陷或恢复状态原因待管理员核实。随后Publish_Each_Build因输出repo不存在报FileNotFoundError，为连带错误。没有BOLT门禁执行或hybrid链接失败证据，也无已取得日志中的磁盘满/OOM/超时证据。

已保存两父两子完整日志、页面文本/截图、provenance/逐行节选及与本地39号对比；独立包日志和profiling不可得，报告页空白/公开产物404如实记录。QB用Tizen-Base 20261026.005418+NGBS，本地39用Toolchain 20261013.024319+GBS，不能当作同环境。只提出仓库元数据和发布错误处理建议，未改源码、未构建、未操作QB、未推Gerrit/sandbox。详见[44号报告](44_qb_failure_1210836_1211014.md)。


### 44号配置根因追查（2026-10-28）

只读克隆scm/meta/qb master并查历史，定位3c78318b0764d892950f11ec8f460719d4eff6a7：Dongkyun Son，AuthorDate 10-26 16:19:54+09、CommitDate 10-28 12:28:41+09，merge 3ed92e4于03:29:11 UTC合入。为临时用Base RPM，把Toolchain和Dev的DOD引用与snapshot_info同时切到Base；实际QB仍创建DOD:Tizen-Base-Toolchain，引用名脱节解释两轮仓库不可用。三次项目/Ref. Snapshot/reference/仓库覆盖选项相同，解析URL变化对应配置提交，未见选错项目证据。最小建议恢复Toolchain project_meta:6为DOD:Tizen-Base-Toolchain而保留Base下载意图；若恢复原环境，还需恢复snapshot_info和候选列表。只写建议，未实施，Dev实际运行结果未知。完整32个相关历史提交diff及3组git log已存meta/，44号第8节追加、前文不变；没有QB操作、配置修改或Gerrit推送。

## 2026-10-28：45号DOD本地修复与固定快照比较

默认自动生成DOD按项目名命名，下载地址由snapshot_info提供；全库异名Tools引用均有显式定义，两个已有Tools QB子构建成功，不能把默认规则泛化为所有项目。Toolchain/Dev各恢复一行DOD引用，snapshot_info保留使用Base快照的意图，XML和前后内容认证PASS。本地scm/meta/qb提交fd60db96806a372404bd4f04e68d4ba586290147，未推送；总部评审挂账。详见[45号](45_qb_meta_fix_and_snapshot.md)。

固定Toolchain20261013与Base20261026工具链不同：636个name+arch联合组中新增9、缺少11、EVR变503、同EVR但RPM校验变113。新build.conf SHA为840ef6de94c6d73e3fcced27dc777a399df435a0f2e4017347191a296f5f1975。后续应按工具链不同口径认证，不继承39号精确clang SHA。

新build.conf不定义_toolchain；直接使用它会令LLVM入口切到release、关闭debug_package、去-g，并定义删除debug目录的后处理宏。用户已回复：暂停debuglink完整构建，先做项目级build.conf调查，不以单独补LLVM宏继续。NGBS最终是否合并Toolchain project_config尚不能由现有日志确认，不能把下载地址直接当作最终宏。另挂账：LLVM only-keep-debug缺陷单独修复、方案乙源码行成本实验。


### 45号 build.conf 项目级调查（用户暂停第三件后的结果）

两份固定配置全量分类：31个宏名发生变化，另有六架构Optflags、Required/Support、clang-accel预安装/运行脚本和Keep变化；Prefer/Substitute/VMinstall等相同，Repotype两份均未声明。新SHA 840ef6de94c6d73e3fcced27dc777a399df435a0f2e4017347191a296f5f1975。Toolchain source索引365份SRPM全部提取spec并验SHA；按manifest245仓库、QB实际251仓库（并集252）逐项核对，实际251仓库均有匹配QB提交的spec，逐包表和原行号见45号第7节。

明确分支影响包括LLVM release/debug、sed/xz的PGO、readline GCC选项、toybox显式gcc、iptables/xmlstarlet Clang警告处理；GCC/glibc原本有GCC override，不误称它们必然由Clang换GCC。其余包仍受段入口、工具宏、选项和依赖条件影响，静态调查不等于全包实编。

关键边界：3c78318未改Toolchain project_config，父提交/该提交/本地HEAD的文件SHA均为fe00ccfb48579b473a9995d6d83682700b6b750029ac4bcb31cd26d9190ffc35。get_build_conf_text随snapshot_info取Base配置，但create_meta_for_ngbs仍读取Toolchain目录，日志没给最终NGBS _config/.rpmmacros；默认加载器是否支持独立config来源尚未确认。推荐Base RPM与Toolchain完整配置分离，先核验装配链；不改Base公共配置，不只补LLVM一个宏。

本地meta修复fd60db96806a372404bd4f04e68d4ba586290147保留、未推。暂停前本地debuglink草稿提交569d734d0ccb2959e3f33494593c5cd46a01c347及346项测试/旧产物副本实验保留，未新构建、未新RPM、未推源码；打包认证仍挂账。本次只发布45号调查证据与文档到GitHub bolt-v4，不含暂停的源码/测试修改。两个快照用于构建LLVM的工具链并不完全相同，不能沿用39号精确clang SHA。


## 2026-10-28：46号两个scm/meta/qb评审的上传前检查

用户确认总部意图：Toolchain类项目使用对应主项目的代码和包，继续使用自己的project_config。用户授权仅在各自全部检查通过后推refs/for/master；本轮两个评审都触发停止条件，**均未上传，没有Gerrit change URL**。

- Base：三架构新Base均缺11个包。251个实际仓库的spec扫描确认gcc-armv7hl.spec L1定义cross=armv7hl，L101条件BuildRequires展开为binutils-armv7hl；新三个架构无provider，按用户“命中即停”不上传。必装/Support/运行脚本等provider齐全，但Keep/条件Substitute有旧仓库也缺的历史项，未擅自豁免或宣称全配置检查PASS。旧clang22.1.8-3.1与新6.5解包后，ARMv7/AArch64显式MLGO两个advisor参数的最小编译4/4 PASS，非参数能力缺失。
- Unified：当前reference已核实tizen-unified_20261027.231956，base_id为tizen-base_20261026.005418；packages与平铺debug包含三架构。自身仓库不含Base工具链，两目录没有可照搬的第二层显式DOD定义。最近成功QB1209720及三子日志为GBS，DOD创建命令0条，不能证明NGBS两层创建。现有1046仓库对新standard1030：缺17、增1、267共同仓库revision变化；新Unified+Base联合仍缺115/115/114个包名。完整1046仓库spec依赖认证因前置停止条件NOT RUN，不能把旧RPM requires风险称为新spec已证明失败。own配置的pkgconfig(gl)替换RHS无provider。
- 元仓库最新读取master为7b2f2ae2d0e0cdc42307454c73c10be23b6d0ef5。原本地两行修复fd60db96806a372404bd4f04e68d4ba586290147未rebase、未推；Unified未生成提交/猜测配置diff。所有project_config保持不变，没有软件包构建、系统安装或QB状态操作。

挂账：两个评审待缺包/目标范围和Unified两层DOD机制解决后重新认证；合入后第一次QB必须确认最终实际使用哪份project_config/_config/.rpmmacros。debuglink完整构建仍暂停。详见[46号报告](46_qb_meta_toolchain_switch.md)，原始材料位于tools/bolt/results/qb-meta-switch-20261028/。


## 2026-10-28：46号用户裁决后的处理

- Base评审仍STOP：1202084 L1425–1426实际调度中有gcc-armv7hl及binutils-armv7hl依赖；1211018 L4884–4889单独导入gcc-armv7hl源码包及spec，不能按“只编gcc.spec”豁免。旧x86二进制gcc-armv7hl为1.3、binutils-armv7hl为1.1，主包分别1.13/1.14。fd60db96原样保留，未rebase/上传。
- 用户豁免已落实：Keep 11名字×3架构及Substitute 23项，共56项同架构provider缺项，旧/新都无提供者、新增退化0，解除此部分阻断。
- Unified新目标为“Unified代码 + Base-Toolchain依赖和配置”，不再沿用两层DOD方案。1209727证实依赖和get_build_conf_text取Base-Toolchain；但1046仓库清单同时与参考快照和meta/manifest.xml相同，日志没有实际manifest加载来源，按“看不出来就停止”未改snapshot_info、未进入1030仓库依赖认证、未创建或上传评审。
- 两项Gerrit均未上传；只推GitHub bolt-v4。下一步需QB manifest加载器/读取来源证据；项目自身PROJECT_CONFIG已见父日志变量，但拼接到最终build.conf尚未证实，首次QB配置核对继续挂账。详见[46号第7节](46_qb_meta_toolchain_switch.md#7-用户裁决后的处理2026-10-28)。


## 2026-10-28：46号第二次裁决落实，两个meta评审已上传

- Base：依赖可以来自依赖仓库或项目自产包。binutils-armv7hl已在新旧QB清单内，binutils revision相同，gcc-armv7hl依赖可由本项目提供；其余10缺包无待编spec依赖命中，56项历史provider缺项豁免继续有效。fd60db96无冲突rebase为ffba0ca45811e6ee70f95f527ae47b958431c20d，两行diff和提交说明保持不变。已上传[359363](https://review.tizen.org/gerrit/c/scm/meta/qb/+/359363)。
- Unified：3c78318b前后245仓库meta manifest SHA相同；1211018实际251仓库与Base快照集合一致、250revision一致，LLVM为用户覆盖。结合1209720的snapshot_num_url/base_path_url分离日志，按裁决确认代码取reference、基础依赖和build.conf取base。全量1030仓库、1034spec、9487BR，17个移除仓库134能力的BR命中0，闭包PASS。
- 独立提交12f22a9c3cd1262f91a798d8f6439f6e3835ad31只改Unified-Toolchain snapshot_info的latest/reference两行，固定到Unified20261027.231956，base和所有其他文件不变。已上传[359364](https://review.tizen.org/gerrit/c/scm/meta/qb/+/359364)。两个评审均基于7b2f2ae2d0e0cdc42307454c73c10be23b6d0ef5，没有互相叠加；只推refs/for/master、未加reviewer。
- 挂账：建议在Base-Toolchain按Base代码产出新快照、正常流程更新base固定引用后再合入Unified评审，避免新代码搭配旧依赖。合入后第一次QB仍须确认最终使用/合并的project_config和宏。详见[46号第8节](46_qb_meta_toolchain_switch.md)。
