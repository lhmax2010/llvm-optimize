# BOLT v4 状态（新会话开场必读）

## 长期署名规则（PM 裁决，2026-10-15）

作者与提交者可直接使用本机全局配置 liushanshan <ss0217.liu@samsung.com>，或以单次命令参数显式使用 Hao Lin <hao.lin@samsung.com>。任何后续提交、提交说明（含 Signed-off-by）和交付文档仅使用这两组身份，不再使用此前昵称或其他姓名。不修改全局 git 配置；历史提交不因此重写，历史身份按提交号查询原始元数据。

若 Gerrit 因提交者与推送账号不一致而拒收，立即停止该次操作，保留并原样报告完整拒绝输出；报告后再以 Hao Lin <hao.lin@samsung.com> 重新提交。不得隐瞒拒收或继续使用被拒身份重试；仍须遵循具体任务的分支推送授权。


## 长期远端授权与证据发布规则（PM 澄清，2026-11-14）

- 任务中“远端写操作只有……”这类限制，只约束 LLVM 侧远端（Gerrit、sandbox、tizen_base 等）和 QB。
- 证据仓库 llvm-optimize 的 bolt-v4 提交与推送始终允许。按 [docs/README.md 第4条](../README.md)，每个任务完成后都要提交并推送，不需每次单独授权。
- 证据仓库只能推 bolt-v4，不推 main，不 force push。不把证据发布授权扩展为 LLVM 或 QB 的写授权。
- 此澄清覆盖90号中“证据仓库推送另待确认”的解释；原执行记录保留。

## 长期对外文本规则（91号PM补充，2026-11-14起）

### 对外文本发布范围与授权（PM补充，2026-11-14）

- Gerrit及其他总部可见位置只放与评审代码本身有关的文本：提交说明、对评审意见的回复，以及用户明确要求发布的说明。
- 不得发布内部问题、进展、分析结果或未结项状态；这些内容统一写进周报。
- 在Gerrit上发布任何新文本之前，必须先有用户的明确指示。下方的语言、引用和格式门禁不构成发布授权。
- 94号TLS结论只保留在证据仓库，后续进入周报，不发布到Gerrit。

适用于发到Gerrit或其他总部可见位置的提交说明、patch-set note、评论、放弃说明和评审回复：

1. 只用英文；不得出现中文、其他语言标点或全角字符。
2. 不得引用总部无法访问的内容：GitHub链接或lhmax2010仓库名、证据仓库路径（docs/…、tools/bolt/results/…）、raw链接、bolt-v4或main/master分支、sandbox分支名、本地机器路径（/home/…、W/B工作区）、内部文档编号。
3. 允许QB构建号、Gerrit change号、提交/tree SHA、LLVM源码路径。
4. 每次发布前，对每份待发文本执行以下门禁；两者输出均须为空（grep rc=1）。任何命中或grep执行错误均STOP，不发布，保留原文。LLVM源码路径中的tools/允许，但需逐条说明理由。

```sh
grep -nP '[^\x00-\x7F]' TEXT
grep -niE 'github|lhmax|raw\.githubusercontent|bolt-v4|sandbox|/home/|docs/bolt|tools/bolt|\bmaster\b|\bmain\b|号' TEXT
```

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

- 46号发布后复核：扫描stdout的一级目录计数已改为实际扫描集合；重跑确认1034spec、9487BR、0命中。嵌套rsync spec此前已经参与扫描；两个Gerrit提交及结论不变。


## 2026-10-29：43号 debuglink 旧快照完整构建前置认证停止

- 用户改用39号同条件的旧Toolchain20261013.024319调试配置，build.conf SHA e5187fd7…核对通过；不沿用45号新Base配置。
- 原569d734d缺发布模式分支，按“缺项先补”授权补齐：pipeline默认无符号，debug分支显式 --debug-symbols；release不分离、不加链接。仅本地amend为69807d06b89f5d14140854e99485182bdef9546b，tree f117b3c47eca5739f6829bd3ff9446bc632d77c1，父hybrid6e9d4f2和Change-Id不变。profile/OPTIONS/白名单不变。
- 348测试PASS，gbs export PASS，新根依赖安装与%prep PASS，Tizen rpm4.14.1.1五项解析PASS；39号products全部35个SHA条目PASS。
- **STOP：BOLT-off debug展开与f308fe08多一个空行（15914→15915B），对应原草稿新增的条件BuildRequires: elfutils。按逐字节门禁停下，不忽略空白、不启动完整构建。** release展开比较及全部产物认证NOT RUN。详见[43号报告](43_debuginfo_symbols.md)。
- 新根temp/debuglink-20261028/及本地提交保留，没有删除目录、没有Gerrit/sandbox/QB操作；准备结束后无新根残留挂载。
- 崩溃定位：函数级代码已实现、42号临时方案已验证；正式RPM完整认证未完成，不能宣称部署可用。源码行方案成本实验、LLVM only-keep-debug修复继续挂账。scm/meta/qb评审359363、359364进展，以及合入后第一次QB使用哪份最终编译配置的核对也继续挂账。


## 2026-10-29：43号空行修复与全部前置检查完成

- 用户裁决维持OFF全文字节门禁。只把单独elfutils行合并到同一条件块的`BuildRequires: xz elfutils`，源码其余内容和提交说明不变。local detached amend为`3ee2d84719e4bd358c0b2366161f70f2eb788313`，tree `43d60f7523439fa0ccf4a61f668dd60622554606`，父hybrid6e9d4f2、Change-Id和Hao Lin署名不变。
- 348/348测试PASS，gbs export PASS，Tizen RPM4.14.1.1五项解析PASS；OFF debug(15914B)/release(16401B)分别与f308fe08全文逐字节相同。release显式undefine _toolchain，避免根内默认宏误入debug。ON debug包含elfutils和--debug-symbols，ON release无--debug-symbols，分支检查PASS。
- 新旧Source/Patch和%prep内容相同，旧准备根可复用，不重跑会清理源码的%prep；新版spec已放SPECS/llvm.spec，无nodeps的`-bc --short-circuit --nobuild`检查通过。新导出/ready-plan在`temp/debuglink-20261028/preflight-fix-20261029/`；旧run.py/plan保留但不可原样启动旧提交。
- 只做轻任务，没有启动%build，没有CMake/ninja、软件包构建、Gerrit/sandbox/QB操作，没有删除目录。前置阻断已闭合，完整debuglink RPM/安装认证仍待后续。详见[43号第6节](43_debuginfo_symbols.md#6-修复空行与前置检查2026-10-29)。


## 2026-10-30：43号完整GBS构建入口失败，按停止条件结束

- 源码3ee2d84719e4bd358c0b2366161f70f2eb788313 / tree43d60f7523439fa0ccf4a61f668dd60622554606，开始/结束工作区干净，无源码修改，未重复第6节前置认证。
- 全新temp/debuglink-20261028/full-20261029/gbs-root，旧Toolchain快照配置和三个宏、threads30；无short-circuit/noprep，无旧%prep树复用。systemd内存24,482,979,840B/swap0/CPU1200%/nice10/ionice2-7。
- 实际GBS约8.123秒后退出1：新local/sources/tizen_base_toolchain_standard/llvm-22.1.8-1缺失，build报告`llvm.spec is empty. This should not happen...`。控制脚本漏掉就位导出源码目录，是本地启动准备疏漏，尚未进入%prep、不是debuglink门禁失败。按用户“构建失败即停”不重试。
- RPM0；身份、23包、90TU、安装实测及包大小/符号耗时全部NOT RUN。OOM计数0，内存峰116,064,256B；未取得完整构建磁盘峰值，结束目录占用4,857,856B不作为峰值。
- 新根和日志保留，无删除/历史根CMake/ninja/Gerrit/sandbox/QB操作。详见[43号第7节](43_debuginfo_symbols.md#7-完整构建验证2026-10-30指定目录-full-20261029)。下一次需先就位已认证导出输入，再完整GBS构建；本轮没有实施重试。


## 2026-10-30：43号启动方式修复与白天演练通过

- 计划：复用39号export/prep/完整GBS配方与37号已有gbs-driver/local布局，演练到CMake入口即停，准备全新full-20261030晚间入口，不做完整构建。
- 进度：两次演练完成。首轮导出/依赖/%prep/%build/CMake入口通过，因5层残留挂载判整轮失败；原文和脚本保留于rehearsal-20261030/attempt-01。增加仅本轮物理根的普通卸载收尾后，在全新retry-02重跑，全部启动与清理项目PASS，总用时401.781秒。命中CMake命令行后11.036毫秒内正常停服务，未进入主ninja编译，未产出RPM。
- 已闭合：源码仍3ee2d84719e4bd358c0b2366161f70f2eb788313/tree43d60f7523439fa0ccf4a61f668dd60622554606，工作树干净；配置与build.conf SHA不变；三个阶段argv除路径/提交外0差异；导出文件已逐个SHA证明就位。资源24,482,979,840B/swap0/CPU1200%/nice10/ionice2-7，实际root构建进程在相应cgroup；两轮服务已结束，rehearsal整个子树残留进程/挂载0。证据：tools/bolt/results/debuglink-20261028/rehearsal-20261030/{summary,all-argv-comparison,export-placement,final-preservation}.json，原始日志及失败全文按attempt分开保留。
- 晚间可直接执行：`/bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/debuglink-launch-20261030/launch.sh full`。full-20261030尚不存在、未启动；入口拒绝覆盖已有目录。与通过演练共用流程，只有full模式不停在CMake，直到GBS打包结束。
- 人工前提：没有新增待裁决项；“晚上可以直接启动”仅指启动流程已认证，不承诺未执行的完整编译/链接/打包成功。39号实际采用gbs-root/local，gbs-driver/local出处为37号，43第8节已明确区分；CPUQuota为本次用户要求的控制层上限，构建参数不变。
- 挂账：完整构建及身份链、23包、90TU、新chroot装包/LLDB/崩溃栈、包大小和耗时仍NOT RUN，按tools/bolt/debuglink-launch-20261030/validation-plan.md执行；GBS结束只标build-ok-validation-pending。源码行成本实验、LLVM only-keep-debug问题及此前QB相关核对仍保留，不在本轮操作QB/Gerrit/sandbox。
- 交付：只在43末尾追加第8节，前文逐字不变；同步本STATUS及入口/证据，同一GitHub bolt-v4提交。未删除既有目录或修改VS Code配置，未向其他任务发信号。


## 2026-10-31：43号完整构建成功，安装实测因 chroot 授权阻断停止

- 按 dca920a8 未修改的 launch.sh full，在全新 temp/debuglink-20261028/full-20261030 完成完整GBS，源码3ee2d847/tree43d60f75保持干净。22二进制+1源码RPM，GBS 8159.098秒；所有构建内门禁PASS。
- profile N23592/M144032/S0/U1/Q383；strip-all13a07cb7、RUNPATH后8c2429d8均匹配；最终含debuglink clang SHA4f08e12d499ebd492ce4951f74915ba435f57f2e380dc6f3520f24644996cb17，符号文件SHAbe17f7222b30b9aff8e9cb30847b7348c5b9897096e382518410dfb053c2f281。Build-ID不存在，与39号相同，按用户裁决通过。
- 39号35条产品SHA全部OK；23包比较PASS，唯一授权内容变化为clang实体、debuginfo新增符号、源码spec/helper。271个ar日期差异单列证明；90/90 TU完整对象字节一致。只执行D里的路径替换脚本副本，历史未跟踪证据不动。
- STOP：新建install-test-root首次 sudo -n /usr/sbin/chroot 调用返回1：`sudo: a password is required`。没有重试或改用其他提权；RPM安装、LLDB自动加载和崩溃符号化NOT RUN。未挂proc、未生成core；服务已结束、根和产品全部保留。整体不能标全部通过。
- 资源只记录：cgroup总峰20,299,001,856B（含文件缓存），OOM/swap0；构建根du最大采样68,252,237,824B，最少可用240,314,093,568B。分阶段真实内存峰值未重置记录、其他进程VmHWM和无du样本阶段均标UNKNOWN；详见43第9节。
- clang RPM +3692B，clang-debuginfo RPM +3862828B；分符号3.242秒，加debuglink1.940秒。日志末行DEBUGLINK FINISHED带时间/status=stopped；证据tools/bolt/results/debuglink-20261028/full-20261030。
- 挂账：函数级正式包符号已有，但安装认证待有效的chroot授权后另行继续；源码行实验、llvm-objcopy only-keep-debug缺陷、scm/meta/qb评审359363/359364进展及首次QB编译配置确认仍保留。本轮只推GitHub bolt-v4，不推Gerrit/sandbox、不操作QB。


## 2026-11-02：43号第5项补做，图形授权成功、RPM初始化因准备缺项停止

- 第1–4项不重做，沿用完整构建/身份/23包/90TU通过记录。仅继续D/install-test-root第5项。
- 找到并复用25号已实证的sudo -A -k + zenity SUDO_ASKPASS机制；一次标记防重复弹窗，单次root POSIX sh脚本包办全部操作/清理，执行前全文和SHA已打印。图形认证成功，没有保存密码。
- /dev/null创建PASS，chroot rpm --version返回4.14.1；rpm --dbpath /var/lib/rpm --initdb退出1：`rpm: --initdb: No such file or directory`。只读确认rpmpopt:181委派rpmdb，而测试根漏带/usr/bin/rpmdb；本轮构建根有该文件。这是测试准备遗漏，不是产品debuglink门禁失败。
- 按停止条件未补拷/重试：两个RPM尚未安装，安装SHA、LLDB自动加载、真实崩溃/地址符号化全部NOT RUN。本次没有挂proc/core，root清理审计mounts/processes均为空，全部现场保留。
- 结论有问题，第5项仍待续跑。证据tools/bolt/results/debuglink-20261028/install-test-20261102；43追加第10节，前文不改。源码/spec/helper/启动脚本未改，未构建、未推Gerrit/sandbox、未操作QB。此前源码行、only-keep-debug及QB相关挂账保持。


## 2026-11-02：43号安装续跑，rpmdb补齐，完整预检仍阻断

- 普通用户从本轮构建根复制/usr/bin/rpmdb到install-test-root，来源/副本SHA均b28b40ea816cd37c2949f094da3904a28a1346e11b8ccf5412ec4c91e6f600ff，19280B；依赖闭包18个ELF对象，库已齐，不新增库。
- 12个脚本所需程序（含RPM中待安装clang）及其解释器/NEEDED检查PASS。/dev/null为1:3、0666；原/var/lib/rpm为空，保留。
- STOP：全部rpmpopt exec项中3/10通过，7/10因rpmsign、rpmkeys、rpmspec缺失失败。遵守“每个转交目标都齐全”的判据，不按当前步骤用不到豁免、不擅自补拷。
- 未进入root脚本修改/执行，未弹窗、未sudo、未装包、未跑LLDB/崩溃或symbolizer。第1–4项不重做，继续沿用已通过记录。旧root-test.sh不应直接重跑，之后仍需按授权处理已有/dev/null。
- 本轮无新挂载/chroot进程、无删除。43末尾追加第11节，证据tools/bolt/results/debuglink-20261028/install-test-20261102-resume。整体有问题，第5项仍未完成；源码和发布代码未改，只推GitHub bolt-v4。


## 2026-11-02：43号安装续跑（二），完整预检PASS，单次图形认证失败

- 普通用户从本轮构建根新增rpmsign/rpmkeys/rpmspec及librpmsign/librpmbuild/libmagic/libdw共7个文件，来源/副本SHA相同，不覆盖既有文件。
- 重新完整预检12/12程序及10/10 rpmpopt exec全部PASS；dev/null为1:3、0666，RPM数据库目录为空。第1–4项未重做。
- 按用户补充裁决，root-test.sh仅改dev/null处理和E输出路径；原数据库路径不变。新SHA0224aa68fd587f40c0ad55d9409d19affde6e41731f7df4a5c90e725913ce54b，sh -n PASS，无旧证据路径残留；旧目录44文件SHA/大小全部不变。
- STOP：单次zenity+sudo -A -k认证返回1，root_entered=false；原文`Sorry, try again.` / `sudo: no password was provided` / `sudo: 1 incorrect password attempt`。没有重试、第二次弹窗或其他提权。
- root脚本未启动，初始化/装包/安装SHA/LLDB/崩溃符号化均NOT RUN；本轮无挂载/chroot进程/core，C的mountinfo引用为空，全部现场保留。整体有问题，安装第5项尚未闭合。
- 43追加第12节，前文不动；证据tools/bolt/results/debuglink-20261028/install-test-20261102-resume2。未构建，未改源码/spec/helper/启动脚本，未推Gerrit/sandbox或操作QB。


## 2026-11-02：43号安装续跑（三）全部PASS，第5项闭合

- 只核对上轮root-test SHA、7个补入文件SHA、空RPM数据库和/dev/null，均未变；未重做完整预检或第1–4项。
- resume3的root-test.sh只改E；新SHA a9efbd254767084ee39057ce7ab782241a1d37faeaec7b56e30e6eb58031fd58。旧resume2共130文件前后SHA/大小一致。
- 按用户裁决同一次sudo -A -k最多3次zenity提示；实际1次输入即通过，只有1次sudo调用，没有记录密码。
- RPM初始化和两个包装入C成功；clang SHA4f08e12d…、debug SHAbe17f722…、CRC1776780033均PASS，Build-ID不存在与39号相同。
- LLDB自动加载/usr/lib/debug/usr/bin/clang-22.debug，真实SIGILL的21/21 clang帧有函数名；llvm-symbolizer逐帧一致，另main+5冷函数6/6一致。函数级定位验证闭合，源码行信息未提供。
- proc正常卸载，root清理audit mounts=[]、processes=[]；final.exit=0，结束行status=ok phase=complete。现场保留，无删除、无重试、无构建。
- 43追加第13节，前文保留；证据tools/bolt/results/debuglink-20261028/install-test-20261102-resume3。只推GitHub bolt-v4；源码行方案、llvm-objcopy缺陷、QB配置评审及合入后编译配置确认等其他挂账不变。


## 2026-11-02：debuglink提交已更新sandbox，QB评审状态查询

- 源码工作区干净；HEAD3ee2d84719e4bd358c0b2366161f70f2eb788313、tree43d60f7523439fa0ccf4a61f668dd60622554606、父6e9d4f2；作者/提交者/Signed-off-by均Hao Lin，Change-Id不变，全部推前核对PASS。
- 按用户指定唯一命令，pack.threads=2、force-with-lease指定f308fe08，更新sandbox/lhmax2025/bolt_pgo。退出0；推后ls-remote精确为3ee2d84719e4bd358c0b2366161f70f2eb788313。未改源码或提交说明，未推refs/for/其他源码分支。
- QB软件包行：platform/upstream/llvm@3ee2d84719e4bd358c0b2366161f70f2eb788313；由用户启动，本轮不操作QB。
- 只读SSH查询：scm/meta/qb 359363已MERGED，Code-Review+2/Verified+1（另作者+1）；359364为NEW、Code-Review+1，Dongkyun Son建议使用usual sync-up process（原文见43第14节）。没有密码交互、评审写入或打分。
- 359363合入状态已闭合；359364进展、首次QB实际编译配置确认、源码行方案与llvm-objcopy缺陷等挂账继续保留。
- 43追加第14节，前文不改；证据tools/bolt/results/debuglink-20261028/sandbox-update-20261102。本轮没有构建、删除或修改VS Code配置。


## 2026-11-02：PGO资源试验设计、前置检查与配置演练完成（47号）

- 发布源码3ee2d847/tree43d60f75及spec/helper/Source未改；本地source-D detached试验提交4ff8ceb44b04b48f6299b6ddf7c5b147ad788b54仅增加LLVM_PROFDATA_FILE，不推送。A基于full-20261030原配置只加LLVM_BUILD_INSTRUMENTED=IR。
- 前置检查：既有348测试PASS、试验12测试PASS、GBS两次export退出0、TizenRPM五项解析5/5、13 ARM+10 AArch64训练输入23/23 SHA一致、7个编译器/工具与原根SHA相同。固定build.conf SHA e5187fd7…不变。
- 新根配置缺的profile runtime用历史同版本构建产物引导，只复制到新根；夜间先构建A自身runtime，再clang。阶段C只读使用同源码历史构建的llvm-profdata。A/B/C/D独立服务，2s全进程采样、5s statvfs、边界du；D子阶段用同FD memory.peak重置，已通过80MiB自测。边界du不能当真正瞬时峰值，短命进程可能漏采，47明确限制。
- 首次测试因宿主PATH缺cmake报8个错误，使用既有CMake修正环境后通过；rehearsal-01配置成功但采样线程在cgroup退出后读FD失败，不采信其旧status=ok。修复仅试验采样器，rehearsal-02/03均在全新根配置成功、未进入LLVM Ninja。所有失败原文保留。
- 最终rehearsal-03配置耗时38.301s、cgroup峰值560349184B；结束行status=ok reason=configure-only-no-ninja，服务全部停止、无残留阶段进程和挂载。全部根保留，未删除目录。
- 最终/home可用234376536064B；规划需求226231549952B（两个根各1.5×43号历史采样峰值+20GiB），PASS，真实PGO增长尚待实测；夜间再次检查。资源规则只在本地试验脚本。
- 晚上入口：/bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/pgo-resource-20261102/launch.sh full。本轮没有执行它，没有插桩clang完整编译、训练或PGO打包。PGO导致BOLT匹配失败时保留原门禁并停止，不绕过。
- 47号设计/原始证据已准备，仅推GitHub bolt-v4；不推Gerrit/sandbox、不操作QB。结论：晚上可以启动。其他既有挂账继续保留。


## 2026-11-02：debuglink BOLT提交说明与外部评审包更新（不推源码）

- 独立克隆W/temp/review-20261102/source，detached amend仅修改三个指定句子；新BOLT提交 **219f23edaffbd84434caf912e261ddb72a4eee2e**，tree仍为43d60f7523439fa0ccf4a61f668dd60622554606，父hybrid6e9d4f2；原作者（含时间）、Change-Id、Signed-off-by不变，提交者Hao Lin。源码没有diff，新提交未推Gerrit/sandbox。
- 用户补充裁决采用stripped ordinary比较。原保全ordinary SHA d5090159…、1793485376B含DWARF；只复制到本轮size-baseline内，用full-20261030同一个llvm-strip及--strip-all，工具SHA d5699b8f…；得到139929432B、SHA eab52018354b9bdd3bdd34b21cfb7731c28883b509fe371566b246c3a5e391cc，原件重新SHA核对不变。
- N=152532400−139929432=12602968B；P=9.006659871241384%→9.0%。历史+31.0%实为183223048−139929464=43293584（01:190、03:28/34）；183224160是后来的37号candidate。139930576是混合两个时期数字的算式，不是查到的实测基线。本次与旧RPM基线32B的具体ELF成因未确认，不推测。
- 新评审包patches/review-20261102/含相对67619ec8的两份完整format-patch（含Source1200二进制）、8个完整文本文件、两份提交说明、三处diff、尺寸原始证据、README及SHA256SUMS。两份补丁独立index顺序应用得到同一tree，PASS。旧review-20261028目录原样保留，新README注明取代关系。
- README关联39号old-text、43号第9节完整构建/23包/90TU、第13节装包/21帧符号化、37号RUNPATH，说明debug/release、回退、release完整构建及源码行/only-keep-debug/QB验证等挂账。
- 原PGO源码工作区与temp/pgo-resource-20261102全部未改；未构建、未操作QB、未推Gerrit或sandbox。仅更新GitHub bolt-v4评审材料，原代码tree的认证继续有效。

## 2026-11-02：外部评审修订（48；第 7 项阻断，不能开始完整构建）

- 按用户要求，仅在 `W/temp/review-20261102/source` detached HEAD 上生成两个本地提交：hybrid `38477c9b6e1401e5e1fe01fafa282ab92cf53887`（父 67619ec8，tree 0ce98bed0e7e92780ca6d9f8d316d1ee422fb8d6）；BOLT `bc0d58ffaab37dbcd88098ccb4c3734570345593`（父新 hybrid，tree d2a5e457ecd5d439a9dd50b67fb561a5f0d67eb3）。两者保留 Change-Id，作者/提交者/签署均 Hao Lin。未推 Gerrit/sandbox。
- 空组件探针：原 hybrid 完整配方配置，在新根副本用临时记录探针覆盖 96 个静态接口，空组件 0；因此加入 FATAL_ERROR，生产 guard 再配置成功。三个驱动的 x86 NEEDED 断言在 BOLT ON/OFF 均执行，三处 USE_SHARED 注释补齐；五个上游强制静态工具已逐项核对 docs/53 原文。
- BOLT 新增协作式 SIGTERM/SIGHUP 清理、精确 RUNPATH 字符串字节门禁、严格 strip LOAD 门禁、debugfiles.list 进包检查、14400 秒 run-step 超时、意外异常诊断；磁盘无证据标签改 unconfirmed；disk-report/cache-release 容错及子进程 Ninja 环境明确传递。profile、OPTIONS、111+2 白名单、Source1005 不变。
- 375 个夹具 PASS；旧 helper debuglink 负控制退出 1；GBS export/Tizen RPM 五项解析 PASS。真实 RUNPATH（13a07cb7→8c2429d8）和 full-20261030 debugfiles.list PASS。关闭 BOLT 的两模式展开与新 hybrid 相差两个 Source 和既有条件块的 14 行空行；与 3ee OFF 仅差本轮 NEEDED 断言，完整原文保留，不声称全文只差两行。
- **严格 strip 门禁真实复核 BLOCKED**：程序头和五个 LOAD 的偏移/地址/大小/标志均相同，但首个 LOAD 包含 ELF 头；strip 删除非加载节后，e_shoff/e_shnum/e_shstrndx 共 6 字节变化。原要求的 LOAD 原始 SHA 不相同。已询问是否允许仅归一化这三个字段；没有收到裁决，未把例外写进 helper。当前 BOLT 提交会在此停止，**不能用于夜间完整构建或上传**。
- 没有能确证为精确 67619ec8 完整构建的保全 RPM：已知基线为 9e5675f（BOLT ON）或 f111162e-dirty，未冒用其完成第16项包比较。四个非默认目标在新建 67619ec8/hybrid 配置图里都不在 all 闭包。
- 新报告 [48_review_fixes.md](48_review_fixes.md)、材料 [review-20261103](../../patches/review-20261103/README.md)、证据 [review-fixes-20261103](../../tools/bolt/results/review-fixes-20261103/)。旧评审包与历史产物保留，PGO 源码/试验目录未改，无完整构建，无 QB 操作。发布前挂账仍含 release 完整构建、本 revision QB、正常依赖装包、Clang/LLD 组件消费者、accel/worker、ARM 根及资源实测。

### 2026-11-02 续：第 7 项按用户裁决闭合

- 用户批准仅归一化 ELF64 的 e_shoff [40,48)、e_shnum [60,62)、e_shstrndx [62,64) 三个完整字段；其余 ELF 头、全部程序头字段、LOAD 地址/偏移/大小/标志和其余字节严格冻结。实现另独立比较归一化后的整个 ELF 头，不以 header 是否属于 LOAD 为前提。
- 378 项测试全部通过，含 e_entry 改动失败、e_phoff 指向另一份有效且相同程序头表仍失败、仅改变三个节表定位字段通过。full-20261030 实物 strip、RUNPATH、debugfiles 三项离线复核 PASS；字段原值/新值保存在 48 号 §20（185673536→152529864、43→38、40→37）。首轮失败证据保留，第7项不再阻断。
- BOLT 新提交 `5aff6c0c3ab663872cf997a13bb9242bac474092`，tree `b4b7d4e1913ea26ef75638147831b7abed9fe51f`；父 hybrid `38477c9b6e1401e5e1fe01fafa282ab92cf53887` 未变；Change-Id、署名不变。相对首轮只改 strip_layout 实现及对应说明；spec/profile/OPTIONS/白名单不变。
- 新提交 GBS export 和 Tizen RPM 五项解析 PASS，OFF 两模式差异仍只有首轮已说明的 Source/空行与 hybrid 断言。review-20261103 的补丁、全文文件、blob/ls-tree、README 和 SHA256SUMS 已刷新，两份补丁重放得到相同 tree。轻量门禁闭合，不表示 release/full-build/QB 等发布前验收完成；精确67619ec8旧RPM缺口仍如实保留。
- 本轮没有完整构建、没有推送 Gerrit/sandbox；PGO 相关目录保持不动。报告最新结论见 [48 §20](48_review_fixes.md#20-用户裁决后仅归一化三个节表定位字段第-7-项闭合)。


## 2026-11-02：QB 1215143 / 1214821 只读调查（49号）

- 1215143三架构均成功，但概览、RBS manifest、clang与debuginfo RPM及SRPM VCS一致指向 **f308fe08**，不是任务预期的3ee2d847。x86为debug模式，项目初始-Os但spec最终-O3；BOLT匹配N23592/M144032/S0/U1/Q383，R=0.004238545331242318%，tool113任务及全部既有门禁通过。begin→compare-root457s，最长输出间隔301s在Source1005归档转换。
- QB clang为152532296B、SHA8c2429d8…，精确等于full-20261030加debuglink前的文件；无.gnu_debuglink，clang-debuginfo无clang-22.debug，CRC不适用。**debuglink版本的QB验证仍未由这次成功闭合**，43号本地安装实测结论不受影响。
- 1214821为Tizen-Base-Dev；仅x86 LLVM在%install的Source1005失败，原文`ValueError: unclassified original command token: -feliminate-unused-debug-types`。普通7634项编译链接已结束；x86实际Clang22.1.8，ARM两架构GNU14.2.0且成功。根因是GCC项目flags与转换器认证策略不兼容，非BOLT/hybrid或编译器缺失。
- 9b8d74af父f999bd40，tree精确等于67619ec8，diff文件0；含356627静态库转换，不含hybrid/BOLT。当前远端tizen_base为f999bd40。固定快照build.conf SHA：Toolchain e5187fd7…、Base-Dev 8ace286a…；QB未打印worker最终配置SHA/project_config拼接过程，不能冒充已确认运行时整文件相同。
- C条件核对：Toolchain latest=20261030.120529，SRPM VCS f999bd40；reference=20261013.024319，SRPM VCS cb679968；均非67619ec8，按要求不下载static-devel、不作归档等价比较。
- 报告 [49_qb_1215143_1214821.md](49_qb_1215143_1214821.md)，证据 tools/bolt/results/qb-20261102。修复候选仅写建议，没有改源码/spec、运行构建、推Gerrit/sandbox或操作QB；PGO两处保护目录未触碰。


## 2026-11-02：50号固定项目参数，轻量测试环境错误后停止

- 新detached提交 `a379c766e17d12ba7738ff6079adb39645c0a740`，tree `37c8c6d3f249b5948db1517d84a79a4d53c9a112`，父5aff6c0c；hybrid38477c9b/BOLT5aff6c0c未改；新Change-Id Ic76505ddb122f1e06271ff7462e24eceee4d400a，Hao Lin署名。只改spec x86参数片段与Source1005 release分支，未推Gerrit/sandbox。
- 按用户补充裁决，完整token规范化打印NORMALIZED，额外过滤打印DROPPED；Toolchain独立shell副本C/CXX/LD输出与QB1215143逐字节相同，DROPPED为空。来源差异已披露：QB C/CXX字符串显式带function/data-sections，本地full-20261030没有，不能预先宣称产物相同。
- **停止**：显式helper测试378项中366通过、12 ERROR，均FileNotFoundError: cmake。48号已记录过host-tools入口，本轮未加入PATH是执行准备错误；按本任务任一轻量检查不通过即停，未修环境重跑。
- 新夹具/转换器既有测试、GBS导出、展开/五项解析、T/D入口与演练、正式磁盘准入、完整构建、包/90TU验证均未执行。source提交未取得构建资格；两个新构建根不存在，无后台构建服务。
- 报告[50_project_flag_independence.md](50_project_flag_independence.md)，证据tools/bolt/results/final-20261103；W/temp/final-20261103/monitor.log带时间status=stopped结束行。没有改PGO保护目录，没有运行历史根cmake/ninja或删除目录。


## 2026-11-03：50号轻量检查与两套演练闭合（未运行完整构建）

- 源码仍a379c766（tree37c8c6d3），父5aff6c0c/祖父38477c9b未改；无发布代码改动。
- 恢复48§13的host-tools/cmake后，显式helper378/378 PASS；显式新Source1005既有24项与新增11项全部PASS。
- GBS export、双build.conf的12组完整展开比较、Tizen RPM4.14.1.1五项解析PASS；ARM逐字节同父提交，x86及OFF只差参数块。
- T/D真实演练均到CMake即正常停止；T参数精确匹配QB1215143，D输出固定参数与架构参数，NORMALIZED/DROPPED原文存证。两根保留，服务/挂载/进程清理通过。
- 今晚入口见[50号§7](50_project_flag_independence.md#7-轻量检查与演练续)，先T验证后D，full模式本轮没有执行。演练后按两份历史峰值＋两份根外实测占用＋20GiB保留重新分项核对满足；演练前额外20%保守参考及重试后的变化均明列于50号，不冒充强制门槛。
- T的strip-all/RUNPATH/最终SHA保持硬要求；ordinary/debug/static成员仅允许严格证明为命令记录节的差异，ar日期单列，90TU仍必做。上一轮停止记录保留，不把轻量PASS冒充产物认证。
- 仅推GitHub bolt-v4，无Gerrit/sandbox/QB操作，不触碰PGO现场和历史根。


## 2026-11-03：第二轮外部评审修复与用户 warning 裁决（51号）

- 三层 detached 源码提交依次为 hybrid `d4d6ca16b55a9afcb64a30ebf634f340f968267b` → BOLT `f2553114b05cbb022ff3ac062dbac284e1029df4` → fixed flags `9e39fa8a61392652bb28b75fc26216675bcad1d5`；最终 tree `cbc33271f8a9a7a5bd4de3c806bed6182c268e98`，三个 Change-Id 不变，Hao Lin 署名。仅本地，未推 Gerrit/sandbox。
- 混合链接 readelf/grep 错误失败关闭并检查五个可选静态工具；BOLT 补齐 SIGINT、纯 Python/尾部取消、第二信号立即终止与 CANCELLED 独立诊断；不改 profile/OPTIONS/白名单。
- **用户裁决覆盖原第8、9条**：未知项目参数丢弃，三组汇总 TIZEN_LLVM_FLAGS_WARNING 在 stdout/stderr 各打印一次，继续构建；非认证 debug 序列 warning 后继续。预期四个 dropped 只审计；非法 release、march/mtune=native 仍失败。精确恢复 IFS/$-，保留三处 `|| exit 1`。
- full-20261030 的3853个转换成员全部带-g；Source1005新增必填--debug-info yes/no、逐成员核对模式。原生成员原样保留、不作release调试节断言，summary计数。Claude C-2八项通过，其中真实工具合成release正/负例2/2；真实完整release成员复测仍挂账。
- 最终393项helper、42项参数/转换器、12项两配置完整展开、Tizen RPM五项解析全部PASS。ARM全文与5aff6c0c字节相同。T/D新根演练各一次到CMake即停止，无Ninja；T dropped为空，D恰为四个预期token，两者warning均0、实际参数符合预期，服务/进程/挂载清理PASS。
- [51_second_review_fixes.md](51_second_review_fixes.md) 与 patches/review-20261104/ 刷新，结论**可以送审**。本轮未运行完整构建；BOLT关闭完整构建、67619ec8精确RPM基线、release真实成员等缺口如实保留。新根保留，后续完整构建须重新核对磁盘容量。


## 2026-11-03：三提交 sandbox 更新在目标核对处停止

- 用户已授权指定租约推送9e39fa8a（父f2553114/d4d6ca16）；当前review-20261102/source干净、完整父链、三套署名和Change-Id均PASS。
- 该独立克隆的origin实际为本地W/temp/debuglink-tb20261026/source，fetch/push均不是Gerrit；`git ls-remote origin refs/heads/sandbox/lhmax2025/bolt_pgo`返回0但无引用，不满足指定目标的前置核对。未执行push，未修改remote配置或旧源码仓库引用。
- 按任一项不符合即停止：磁盘清单及空间缺口估算NOT RUN。Gerrit真实当前SHA未查询，UNKNOWN，不能将本地origin的空结果解释成Gerrit分支变化。
- 详见[51号§9](51_second_review_fixes.md#9-sandbox-更新与磁盘清单2026-11-03推送前停止)。本轮只推送GitHub证据和停止记录，不操作QB、不运行构建、不删除目录。


## 2026-11-03：使用完整Gerrit地址完成sandbox更新；磁盘仅盘点

- 用户追加授权直接使用ssh://review.tizen.org:29418/platform/upstream/llvm；不改remote配置。推前3ee2d847精确匹配、源码HEAD9e39fa8a且clean；指定force-with-lease命令执行一次成功，推后远端精确为 `9e39fa8a61392652bb28b75fc26216675bcad1d5`。三层提交/Change-Id未变，未推refs/for。服务器只有标题>50字符warning，原文已存证，没有改提交说明。
- /home扫描结束可用163,685,830,656B（152.444GiB）。137个一级目录限时du：28个>5GiB、11个UNKNOWN；修改时间明确为目录自身mtime。oldtext-final有VS Code打开和proc挂载，保留。认证products、full-20261030、PGO、原始RPM和源码保留；未核实唯一性的交用户判断。
- 两根参考需求150.158GiB（43号两倍采样峰值+两份根外开销+20GiB保留），只余2.286GiB；加20%采样峰值规划余量后需175.584GiB，建议先释放约24GiB。五个已结束演练子根为优先候选：三项可见du合计19.571GiB、两项UNKNOWN，不保证净回收量，未删任何文件。
- [51号§9.3–9.6](51_second_review_fixes.md#93-用户授权完整-gerrit-地址续跑2026-11-03)记录推送原文、按保留/可删/用户判断分组的目录表、证据与空间公式。没有运行构建或操作QB；本轮仅更新GitHub证据文档。


## 2026-11-03：用户批准的十个目录清理完成（52号）

- 按用户精确清单删除五个已结束演练gbs-root及五个旧实验目录，10/10完成、0跳过；没有扩展到父/同级目录。第6–10项顶层/du及71个RPM的本次SHA清单先保存，未复制RPM。
- 每项真实目录/realpath、挂载、全权限/proc（含maps）和用户服务检查通过；一次zenity + sudo -A、一次输入成功。前五项root不可写目录用root删除，后五项UID1000删除；rm均带--one-file-system。
- 删除执行窗口/home可用空间从152,217,346,048B升至285,199,704,064B（265.613GiB），df净增123.849GiB。文件系统可用空间会随其他写入变化，时间/原文见52号。
- 十个路径均不存在，父目录其他条目元数据比较一致；products、full-20261030、PGO、配置、源码和证据保留。未构建、未改源码、未推Gerrit/sandbox、未操作QB。
- [52_disk_cleanup.md](52_disk_cleanup.md)与tools/bolt/results/disk-cleanup-20261103/存证；结束标记DISK_CLEANUP FINISHED status=ok。

## 2026-11-03：夜间 T/D 白天准备（53号）

新入口 `tools/bolt/night-launch-20261103/launch.sh SOURCE_SHA night` 已准备；源码仍为9e39fa8a61392652bb28b75fc26216675bcad1d5，未改LLVM源码、spec或历史入口。Toolchain和Base-Dev两个演练串行到真实CMake入口后停止，参数与51号一致，WARNING=0，服务已停止、无残留进程/挂载。

T认证产物自测23/23包、90/90 TU PASS，14项字节/归档/参数夹具、5项启动检查、8项集成检查及release C-2正反夹具PASS。D真实release成员、MODULE、post与D/T90TU留待完整构建后自动验证；认证装包留到明早。阶段资源缺采样标UNKNOWN，命令记录差异必须逐字节证明，不跳过整节/成员。

演练后/home可用263,345,737,728B（245.260GiB）；按51号两根峰值、根外开销、20GiB保留量及20%峰值余量共188,531,890,586B（175.584GiB），余74,813,847,142B（69.676GiB），空间规划通过。本轮没有启动full/night，两个完整根不存在。启动命令和全部判据见 [53_night_validation_prep.md](53_night_validation_prep.md)。T普通失败仍跑D；磁盘/OOM/残留/无法确认清理则停止。

## 2026-11-04：夜间 T/D 已结束，有问题（54号）

- 用户指定的 night 启动命令执行一次；启动前/home可用243.179GiB、两个full根和night.log均不存在、无其他GBS。T/D由入口自动串行执行，没有手动启动D或重试。
- T与D的GBS均exit0（12943.782s / 4173.033s），产出分别22+1、12+1个RPM；构建内BOLT/转换/post日志成功。**自动构建后验证未完成**：T在validate.py:100读累计日志时MemoryError；D控制器在构建后验证阶段被OOM杀死。最终 `NIGHT 已结束 2026-11-04T04:13:34.194671+08:00 status=stopped reason=memory-oom-stop`。
- 只读定位：入口日志游标bytes变量anchor被阶段循环覆盖为str，导致日志反复从头追加；T/D累计日志46.43GB/15.08GB，canonical GBS日志各约18MB。验证一次性读入大日志；T的Python MemoryError未归类为critical，入口自动继续D，D的systemd OOM触发最终停止。入口、源码均未修改；原始大日志和现场均保留。
- T strip-all=13a07cb7…、RUNPATH后=8c2429d8…匹配，最终=6c63c5c2…不匹配4f08e12d…；全文件比较证明仅.gnu_debuglink CRC的4字节变化，其余字节相同。符号文件也变化，CRC差异不属于已批准的命令记录节例外，不能判为通过。23包内容比较、T90TU、D真实成员复测/产物参数扫描/MODULE加载/D对T90TU均NOT RUN；未冒用历史自测结果。
- D profile N=23592 M=144032 S=23 U=1 Q=383，R=0.1017251%，在原门槛内；转换器输出225归档、3853转换成员、11原生成员，debug_members=0（尚未独立RPM成员复核）。D无debuginfo/debugsource包。T/D的CMAKE_MODULE_LINKER_FLAGS均精确为 `-Wl,-z,relro,--as-needed -Wl,--gc-sections`。
- T原资源表原样交付；D原表缺失，另标明用本次原始采样只读汇总。当前记录/home可用141,717,905,408B（131.985GiB）；最终停止原因不是磁盘不足。可读/proc与findmnt无本次构建残留，未手动清理、未做装包/LLDB、未推Gerrit/sandbox或操作QB。
- 详见 [54_night_results.md](54_night_results.md)，证据 `tools/bolt/results/night-results-20261103/`。后续须由用户决定修复验证入口、处理符号/CRC差异和补做剩余验证；本轮不重试。


## 2026-11-04：QB 1215801 / 1215600 身份核对（57号）

- 用户给定的两个编号与预期不符：1215801=Tizen-Unified，1215600=Tizen-Unified-Toolchain，均非 Base-Toolchain/Base-Dev。父构建 Recommended，standard 三架构子构建均 Successful。开始/耗时与计算结束时间、软件包行原文均已存证。
- 两份产出快照的 standard manifest 各1030个仓库，均不含 platform/upstream/llvm；父/x86日志没有9e39fa8a。实际 LLVM 编译版本为不适用（没有该包构建），不能用总体成功认定9e39fa8a通过。
- 保存两个父构建和两个x86子构建完整日志gzip、概览、manifest、产物索引。没有LLVM包日志（对应地址404），没有clang或clang-debuginfo RPM；FLAGS/BOLT/profile及本地SHA/包名/字节差异比较不适用，未借用其他快照产物。
- 本地night的T最终clang=6c63c5c2…、符号=59607550…、D最终clang=1664b9d2…已只读重新核对。54号未完成的验证不在本轮重做；night目录、源码、QB均未改。
- 详见 [57_qb_1215801_1215600.md](57_qb_1215801_1215600.md)。后续需要实际编译9e39fa8a的两个Base项目QB链接；本轮只推GitHub bolt-v4。


## 2026-11-04：正确编号 QB 1216409 / 1216410 核对（57号）

- 1216409=Tizen-Base-Toolchain，1216410=Tizen-Base-Dev；概览软件包行、产出manifest与下载的clang RPM VCS均确认实际源码9e39fa8a61392652bb28b75fc26216675bcad1d5。两父构建及三架构子构建成功，六份LLVM包日志均位于succeeded并正常结束。
- x86两项目NORMALIZED/DROPPED去时间前缀后分别与night本地T/D逐字相同，WARNING均0。profile全部计数一致：T S=0、R=0.004238545331%；D S=23、R=0.101725087950%。111+2任务、tool-verify113/113、三次real、pipeline/compare-root/cache-release/post和归档225均PASS；T debug-symbols/debuglink PASS，D按release无这两项。
- T22+1、D12+1包名清单分别与本地相同。D最终clang=1664b9d2…，与本地全文件相同；T最终=e08724d8…，对本地6c63c5c2…仅.gnu_debuglink CRC四字节变化（偏移152529896–152529899）。QB符号=9942e19c…，与本地59607550…不同但其CRC与QB clang匹配。符号文件差异已逐字定位到命令记录排列、.comment GCC版本记录及相关两字节节头/一字节尾部填充；不将其说成整文件相同或擅自放宽认证。
- [57_qb_1216409_1216410.md](57_qb_1216409_1216410.md)及tools/bolt/results/qb-1216409-1216410/保存完整日志gzip、原文行号、RPM来源/SHA、精确字节比较。错误编号旧报告此前已提交，本轮保留不改。只读采集，没有修改night或源码，没有构建、QB操作、Gerrit/sandbox推送；54号未完成的23包内容/90TU/安装验证不在本轮补做。


## 2026-11-04：记录节与 debuglink 追加判据；55号结果位置待确认

- 用户批准将.comment加入允许内容/长度变化的记录节；必须列出全部字符串及次数、验证只有编译器/链接器标识。命令记录差异须报告字符串种类/次数及新增缺失；debuglink按新口径判断。其他验证不重跑。
- 用57号已有QB1216409/本地夜间T证据核对：两边.comment仅标识字符串，PASS；.GCC.command.line的2335种字符串及次数、顺序和节SHA其实全部相同，仅受.comment缩短2B影响整体前移2B。已纠正57号此前“排列不同”的错误表述，保留原始逐字节差异证据。
- 用户确认T本地快照20261013.024319、QB1216409快照20261030.061318不同，是.comment差异来源；Base-Dev两边均20261030.061217。57号第8节先完整记录，待55号位置确认后写入其对应部分。
- 本地与fetch后的origin/bolt-v4尚无55号文档或其第二/三部分结果，已请求路径；不创建冒名的完整验证结果、不重跑90TU/23包、不将现有QB对比标作整项夜间重验证PASS。


## 2026-11-04：夜间入口修复与重新验证完成（55号，有问题）

- 用户已把此前追加判据替换为完整新任务，55号从头实施；此前“结果位置待确认”状态已关闭。仅修本地入口/验证器，未改LLVM源码/spec/helper、未重新构建、未做装包/LLDB。
- 修复日志游标覆盖、流式读取canonical GBS日志并设1GiB上限、内存错误/OOM停止串行队列、严格gbs-driver RPM定位和原始日志阶段计时；32项回归测试PASS。实际验证又修复合法重名ELF节解析与共享RPM头文件提取，原失败及定向补检全部保留。
- T对认证版严格比较FAIL：普通clang和符号文件存在.symtab/.strtab差异；最终clang虽仅debuglink CRC四字节变化且CRC正确，但符号文件不通过，不能放行。23包4PASS/19FAIL；T90TU为90/90。
- D全部验证在提取器专项补检后PASS：3853转换成员无调试节、1975原生成员仅计数、真实release正反例PASS、5802记录节无DROPPED token、两项MODULE加载PASS、90TU对T为90/90；D12+1包，无debuginfo/debugsource。原failed结果与更正后的result-effective.json并存。
- 本地T符号对QB1216409 PASS，仅.comment标识和相应布局；两边GCC命令记录完全相同。本地Toolchain快照20261013.024319、QB20261030.061318；Base-Dev两边均20261030.061217。
- 两轮独立16G/swap0服务，无OOM，全部已结束；原始GBS时间资源表已重算，缺采样写UNKNOWN。只删除获批两个重复rpm-build.log，df释放61,506,420,736B（57.282GiB）；产品/原始成功日志/旧validation均保留。
- 详见 [55_night_revalidation.md](55_night_revalidation.md)。整体仍有严格产物差异，等待用户裁决；本轮只推GitHub bolt-v4。


## 2026-11-04：PGO资源实验已结束（58号，D门禁失败）

- 用户批准本地预算改为目标177.548GiB（仅记录）/最低151.290GiB（门槛），原12项+3项边界检查15/15 PASS；运行中20GiB停止线不变。仅清理获批validation临时文件副本，JSON/文本/输入/原始RPM/所有根保留。
- 指定launch.sh full只启动一次，初始可用170.686GiB，低目标6.861GiB，预算JSON与controller首行均打印BUDGET_MARGIN_WARNING；使用入口原有免密sudo -n，没有新增认证方式。
- A/B/C PASS：插桩clang完成、23训练全通过，profraw 746,313,472B，profdata 52,528,216B（8c60fb56…）。D普通构建/安装、工具113项通过；llvm-bolt因15638/18343=85.3%陈旧profile超过原5%门槛退出1，未进入compare-root/cache-release/转换/打包；没有重试或修改门禁。
- 结束：`PGO_RESOURCE 已结束 2026-11-04T23:47:45.378355+08:00 status=failed reason=D: rc=1 reason=None; see /home/linhao/Toolchain/development/llvm-optimize/temp/pgo-resource-20261102/full/stage-D/evidence/D`。没有OOM，最低/home可用78.011GiB；内核cgroup峰值A6.731/B1.380/C1.699/D20.213GiB（含文件缓存）。全部根和失败现场保留，正常清理后无本次残留挂载/阶段进程。
- 原report.py已汇总。根du只有边界采样，普通编译出口扫描超时，连续磁盘峰值UNKNOWN；按稳定A根与D边界记录组合最大85.007GiB，不能冒充连续同时扫描。详见[58_pgo_resource_results.md](58_pgo_resource_results.md)，原始证据tools/bolt/results/pgo-resource-full-20261104/。尚需用户决定是否为PGO输入重新采BOLT profile；本轮只推GitHub bolt-v4。


## 2026-11-05：三项无人值守调查已结束（59/60号）

- 第一项：前置调查完成，实际PGO+BOLT插桩/训练/优化 **NOT RUN**。D根缺merge-fdata可执行文件及BOLT插桩runtime，按保守规则停止；没有替换工具或重编。复制件、正式OPTIONS、23训练输入出处和PGO+BOLT资源估算（未知项明确标注）见[59号](59_pgo_bolt_followup.md)，提交 `7d7e1cd99e828dac50d10dc745e04a4c6d075c86`，已推GitHub。
- 第二项：已通过公开地址取得QB T22+1、D12+1共36个RPM。比较规则8个正反例通过。D的12个二进制包内容PASS；T的python-clang PASS，debugsource的12,142条路径仅release目录名变化、内容一致，其余20个二进制包严格FAIL。两源码包仅spec有内容差异（除VCS/Release外，GBS导出的8条patch命令写法不同），未放宽。536条T/1条D失败文件原文和逐包元数据均保留。
- 第三项：55号449个拒绝文件全部审计。110,591条名字变化符合.llvm数字后缀；210条属性例外集中在ompdModule.so及其.debug。200个变化归档索引的目标成员名称与次序均不变。单TU旧/新参数模块哈希不同，新参数重复两次整个bitcode SHA相同。compiler-rt中1,237个受影响成员的节序和ALLOC内容均相同，旧命令已经有函数/数据分节选项，差异来自重复记录这些token与文件位置变化。AddLLVM的4行新增检查与混合链接提交源码完全一致。
- 通用debuglink重判85/133 PASS、48 FAIL；独立CRC校验133/133均匹配各自符号文件，FAIL仍因符号文件的非记录节或程序头变化。MODULE须按名字对齐，最终8个ALLOC节内容不同；MODULE链接参数新增--gc-sections已证实，但未隔离重链接，具体字节因果仍 **未解释**，不当作新门禁豁免。
- 第二/三项报告与完整证据见[60号](60_baseline_attribution.md)，提交 `b2fa686fda8c3afe1def995192bfb312711dcb86`，已推GitHub。原始逐次失败、按序遍历初稿与按节名校正结果都保留；最终MODULE范围以module-named-sections.json为准。
- 本轮不改LLVM源码/spec/helper/Source1200，不改三个受保护历史根，没有sudo、弹窗、软件包构建、删除、QB/Gerrit/sandbox操作。重操作均在独立systemd用户服务运行，MemoryMax=MemTotal−8GiB、swap0、CPUQuota1200%、nice10、ionice2/7；运行中30GiB停止线未触发，已取得的memory.events全为oom=0/oom_kill=0。没有本轮活动服务；两个失败下载前置服务的终态记录保留，没有reset-failed。
- 收尾时/home可用 `53138251776` B（49.489 GiB）；本次公开RPM、解包文件、单TU产物和所有历史根保留。需要用户后续决定如何补齐D来源插桩工具，以及是否做MODULE隔离链接实验；本轮不自行继续。

结束行原文：

```text
ITEM1 已结束 2026-11-05T00:11:43.545431+08:00 status=stopped reason=missing-D-root-merge-fdata-and-instrumentation-runtime
ITEM2 已结束 2026-11-05T00:41:25.825515+08:00 status=differences reason=comparison-complete
ITEM3 已结束 2026-11-05T01:04:01.863726+08:00 status=partial reason=449-files-audited-module-byte-causality-unproven
```


## 2026-11-05 PGO+BOLT补测完成与批准清理（本提交）

- [59号](59_pgo_bolt_followup.md)补齐完成：复用16号LLVM22.1.8 merge-fdata/runtime；bolt/1,154文件与3ee2d847一致、额外文件0，无工具构建。23/23插桩训练、一份合并profile、正式OPTIONS优化通过，N/M/S/U/Q=19648/164430/0/1/599，R=0.005089318%，未放宽5%门槛。
- llvm-bolt优化VmHWM=8,890,351,616B，比54号非PGO同口径低10.485%。保留use-old-text空间不足警告，未strip产物259,324,032B；不是完整发布验证。后处理/打包资源继续明确标为55号借用估算。
- 23输入×3编译器×3轮，共207次-O2速度编译全部成功；中位数120.362/108.553/104.708s。轮间波动较大，3.542%差不能确认为稳定加速。完整原始数据保留。
- [61号](61_disk_cleanup.md)：只删除批准的attribution/payload和PGO stage-A/gbs-root，跳过0；一次sudo调用、一次zenity认证。清理窗口df净增33,241,427,968B（30.958GiB），兄弟条目不变，D根及所有其他历史根只读。补测结束/home可用77,381,136,384B（72.067GiB）。
- 未改LLVM源码/spec/helper/Source1200；未推Gerrit或sandbox；所有新补测产物保留。后续完整PGO+BOLT打包和未见输入上的性能验证未执行。


## 2026-11-05 下午四项（62号，本提交）

- 后续逐字节比较基线固定为同一提交、同一快照的QB产物。比较器新增用户批准ET_REL例外：仅记录节变长造成的后续ALLOC文件offset移动可接受，其他加载属性/内容严格，EXEC/DYN不放宽；5项新正反例与8项旧规则通过。
- [62号](62_afternoon_20261105.md)：ompdModule新参数重链与T原件逐字节相同；移除gc-sections后与旧认证原件仅记录命令节不同，加载内容相同。剥离后仅隔离debuglink CRC，两边分别与各自RPM字节相同；不是完整打包复现。
- tools/bolt/night-launch-20261105：QB1216409固定快照20261030.061318，build.conf SHA8f201a0d…，单T入口准备。首次演练因prep旧日志被读取而restart=1失败，记录保留；修复epoch交接后第二轮PASS，restart=0、原件副本62193B完全相同、FLAGS/CMake与QB一致，无Ninja、无残留。今晚full未执行。
- QB安装新根测试PASS：clang/debug SHA e08724d8…/9942e19c…，CRC3891159848，LLDB自动符号加载，21/21 clang帧与symbolizer一致，5个冷样本通过，无源码行能力；proc正常卸载，无残留。第三四项一次sudo、一次zenity认证。
- 仅删除批准PGO stage-D/gbs-root，其他条目及followup保留；df净增60.378GiB。当前/home 119.019GiB，单T预算98.774GiB，余量20.245GiB。今晚可启动，命令见62号；没有发布源码修改或Gerrit/QB操作。


## 2026-11-05 批准目录清理（64号，部分完成）

- [64号](64_disk_cleanup.md)：34个实际获批路径中29项完整删除，第10项工作内容删除后恢复并保留Git对象库，第20/26/28/36项保留；34/35无操作。未启动night-launch-20261105。
- 第20项服务于4个清单外保留worktree，跳过。本轮检查遗漏第10项的alternates反向依赖，导致26/28查询失败；从已验证bundle读回副本恢复原对象库（4,556,627,020 B），SHA一致，5个受影响仓库查询恢复PASS；没有改依赖仓库配置，26/28不重试删除。
- 第36项的253个仓库完成4个保全后，检查器对bare仓库误用git stash list而停止；这是检查器适用性缺陷，不是仓库损坏证据。qb_analysis整目录保留，其余仓库源码保护未完成。
- 23个实际仓库已导出保全，未发布提交逐仓库计数合计51（非去重），5个有tracked改动；保全含format-patch、binary diff、standalone bundle及空仓库读回验证，位于temp/deleted-repo-backup-20261105，实际占用91.294GiB，全部保留。
- PGO profiles 24文件、798,841,688 B移至temp/pgo-profiles-keep-20261102，移动前后及收尾SHA全部相同。第1–3项兄弟条目和12个指定保留目录复核通过，6个保留源码HEAD对象可读。
- 全程一次sudo调用、一次zenity认证；未追加提权或重试。/home收尾可用335.444GiB，较清理前118.944GiB净增加216.500GiB（已包含保全和对象库恢复占用）。原始失败、逐项df、RPM SHA及恢复记录见tools/bolt/results/disk-cleanup-20261105b/。没有构建、发布源码修改、Gerrit/sandbox或QB操作。


## 2026-11-05 历史目录第二组只读盘点（65号）

- [65号](65_disk_review_group2.md)：64号结束后盘点13个目录，未删除、移动或修改其中任何文件；没有sudo、构建或Gerrit/QB操作。
- 6个目录可按文件清单瘦身，保守预计释放27.697GiB；7个建议保留，没有整目录删除建议。原RPM、认证products、profile原件和未发布探针仓库均保留，后续删除仍由用户逐项决定。
- 528个RPM路径，525个取得本次SHA、3个限时超时记UNKNOWN。A/B另有3处权限盲区，各自du只作可读下界；A旧lto.cache已不存在，B缓存仅17,752,064B，当前大头是build/bin/lib64。
- C2/C3仅709个逐文件同SHA重复归档列为候选；各组限时后未完成核对的档继续保留。4个无远端的最小探针本地提交保留。ARM离线210/212档已通过，最后根内试验停于Exec format error，安装打包和64MiB限制仍未认证；从零重搭耗时UNKNOWN。
- A根内没有合并前训练fdata；23原件在bolt-measurement-20260918/run/profiles，当前SHA全部吻合旧清单。旧merged与Source1200解压同SHA；重合并行顺序不固定，但746,704条完整行多重集及计数全同，未冒充新重合并SHA相同。
- 原始du、全部RPM/SHA、逐条引用、Git检查、精确保留及候选清单见tools/bolt/results/disk-review-group2-20261105/。本轮实际释放0B，未启动今晚构建。


## 2026-11-05 清理完成、QB同快照重建已启动（66号）

- [66号](66_disk_cleanup.md)：一次zenity认证及一次sudo调用，root补查无挂载/进程/服务占用后，仅删除qb_analysis；253个仓库只登记，不做额外源码保全。该窗口/home可用净增178,935,119,872 B。
- 源码备份26组检查中9组补丁链/公开基础可取得性通过，但root:root且不可写；依用户“root删除只在第一部分”裁决保留，没有再次sudo。其余17组因根提交、非线性/覆盖关系或不可证明公开基础保留；manifest在本轮证据目录，原备份和SHA256SUMS不变。
- 65号精确候选逐文件SHA核对后删除727文件（C2 494、C3 215、crash-probe 18），未发现SHA不符。cache-release解包、intranet检出/导出和MLGO root因65号缺完整历史SHA而整组保留，未把现算SHA冒充旧清单。
- 所有65号保留文件复查存在。启动前/home可用559,488,331,776 B，fresh root及无GBS/rpmbuild通过；只执行一次用户给定night-launch-20261105 full命令，controller初始active/running。当前是运行中，不宣称构建或验证通过；结束后另交63号。


## 2026-11-06 同快照Toolchain重建结束（63号）

- [63号](63_qb_snapshot_rebuild.md)：唯一一次用户指定入口已于2026-11-05T23:26:50.821583+08:00结束，status=failed；GBS构建exit0，失败来自自动验证，没有重试或修改入口。
- 同9e39fa8a、同tizen-base-toolchain_20261030.061318：三级SHA全部与QB1216409相同；最终clang为e08724d8…，符号为9942e19c…，两份RPM载荷也同SHA。FLAGS逐字相同、WARNING0、profile计数和构建内门禁通过。
- 23包为3 PASS / 20 FAIL：132对工具/符号涉及debuglink和DWARF，debug_str已逐节证实只是Release=1/2.1造成的debugsource路径变化；仍不放宽DWARF门禁。debugsource有12,142对路径前缀不同，去前缀后内容/权限相同；源码包17文件mode0664/0644不同，spec另有VCS/Release/patch导出语法差异。逐文件清单已保存。llvm-static-devel等3包通过。
- 90TU读取第一个旧输入路径hybrid-local-20261023/tu-inputs/000.ii时失败，完成0/90；不是目标文件不一致。该父目录已在64号授权清理中删除，本轮未恢复资产、未改验证脚本或重跑。
- 构建cgroup峰值17.261GiB（含文件缓存）、OOM0；根有效采样峰值63.079GiB，按GBS原始秒数生成资源表，缺采样UNKNOWN。入口最终审计无残留构建进程/挂载，现场全部保留。
- 66号清理结论不变：qb_analysis及727个同SHA候选文件已删；备份权限/公开基础及缺历史SHA的候选仍保留。后续90TU资产路径和打包元数据差异需用户决定，不自动续跑。


## 2026-11-06 改接前提核对（68号）

- 359934仍NEW，PS10为13c3e223；远端tizen_base仍为f999bd40，转换器不在该HEAD中。停止改接，不创建分支/worktree、不演练。
- PS10已采纳四项检查；cf4b6777与67619ec8的tree相同，但前者未合入当前tizen_base。完整证据见[68号](68_rebase_on_tizen_base.md)。第二、三项继续。

## 2026-11-06：90 TU 恢复与 DWARF 逐项核对（67 号）

- 90/90 输入从 full-20261030 保留副本恢复至 temp/tu-inputs-restored-20261106，全部 SHA 匹配；0 重新生成，两个现用验证入口改接，4 项测试 PASS；未重跑 90 TU。
- 132/132 调试文件检查完成：严格文本 0 PASS、132 DIFFERENT、0 UNKNOWN；全部其他节及节数量/名称/顺序相同。差异为 176,482 个行表编码长度字段，以及 8 个文件的 19 处 DW_AT_comp_dir 重复斜杠。88,987 个行表单元证明路径增长精确解释长度变化，行号程序字节相同；未擅自扩展归一化规则。
- 无 OOM/超时；历史根只读。改接停止的原因及未执行的检查/演练仍见 68 号，未创建新的 LLVM 分支或提交，未推送 Gerrit。
- 证据与逐文件清单：[67_tu_inputs_and_dwarf_check.md](67_tu_inputs_and_dwarf_check.md)。

## 2026-11-06：设计文档放置

- 下载文件已移动到 W/docs/bolt/design/tizen_llvm_speed_design_v1.md，并同步发布本分支同路径；SHA256 4374885a18743c8894323cac822f101bfccaf48bdf68eb02c8bf95aa03437ec0。

## 2026-11-06：359934 PS10 改接

见 [69](69_rebase_on_359934.md)。基线 13c3e223（NEW）；新链 a73a7da3 → e08ed9ed → a3d18c2d。7706/7706 重放完全相同，46+5 回归及真实 C-2 正反例通过。T 演练通过；D 到达 CMake 且参数正确，但 log-restarts=1 和收尾日志要求使审计未通过，保留现场、不重试。未完整构建、未推送 Gerrit。

## 2026-11-06：67 §8 候选规则复验，待 comp_dir 裁决

[67 §8](67_tu_inputs_and_dwarf_check.md#8-规则更新与复验2026-11-06规则发布待裁决)：8 项候选测试通过；按“先前缀归一化，再约束剩余斜杠差异”的候选解释，132 对 .debug 和 132 个 debuglink 通过，21/23 包通过；源码包权限/spec、debugsource release 路径仍 FAIL。指定正例 libRemarks 的原始 comp_dir 长度为 41/43 字节，与全部原始值等长的字面规则冲突，已询问用户。候选代码保存在结果目录 proposed/，现用 tracked 入口已恢复；正式规则待裁决，未重建、未重跑 TU。

## 2026-11-06：comp_dir 裁决闭合，67 §8 规则启用

用户确认：前缀替换后完全相同的 comp_dir 不要求原始等长；仅剩连续斜杠差异的才要求原始字节等长及 POSIX 词法等价；其他差异 FAIL。三条原文已写入 [67 §8](67_tu_inputs_and_dwarf_check.md)。现用两个验证入口已启用与原复验同 SHA 的候选代码；新增 45/46 字节反例正确拒绝，9 项测试 PASS。原 132/132 对 .debug、132/132 个 debuglink 正式记为 PASS，21/23 包 PASS；源码包权限/spec 与 debugsource 路径两项 FAIL 不变。未重建、未重跑 90 TU 或包比较；上一条“待裁决”已闭合。69 号 Base-Dev 演练失败结论不变。


## 2026-11-06：359934 基线上 sandbox 更新

第三个提交仅整理说明为 7d5e28ca89ed68e3360765bc4e42234eaaabae27，tree 不变，前两个 a73a7da3/e08ed9ed 不变。指定 lease 推送成功，远端已核对；359934 和 357163 仍 NEW。证据与命令原文见 [69 §5](69_rebase_on_359934.md)。Base-Dev 演练问题待本轮第二项处理。


## 2026-11-06：Base-Dev 演练审计闭合

仅 basedev 副本同步 Toolchain 的 prep→build epoch 交接和演练资源报告修复，2 项新增测试 PASS。以 sandbox 7d5e28ca 在新 retry-02 根重跑一次，正常停于 CMake、未运行 Ninja；log-restarts=0，原始/复制日志 58,264 B 且逐字节相同，FLAGS 对 QB 1216410 完全一致、WARNING 0，资源报告已生成，无残留挂载/服务进程。此前失败记录不改，问题现已闭合，详见 [69 §6](69_rebase_on_359934.md)。未完整构建，未再推送 Gerrit。


## 2026-11-06：设计 v2 与改接评审材料

设计 v2 从 /home/linhao/Downloads 移至 W/docs/bolt/design/ 并同步发布，v1 不变；v2 40994 B，SHA256 32b86b912acef9c4c9ccc39b5733d8d1520cbde78c866463adedbf1b42291989。补齐 [改接评审包](../../patches/rebase-359934-20261106/README.md)：最终 9 份文本（spec/helper/转换器/6 份 CMake）、转换器对 PS10 完整 diff、排除 profile 的 BOLT 文本补丁和 SHA256SUMS。源码及原三个完整补丁未改，本次未推送 Gerrit/sandbox。

## 2026-11-06：第二轮代码评审修复（70 号）

- 本地三提交：混合链接 a73a7da32049569b1360e9c13d0633c168b8f173 不变；BOLT 7d11ad53629ac7b670664fcbe6aee8348848d5d6；固定参数/转换器 5a27edb4265366781f07049ad17a3796f2e05301。Change-Id 保留，标题 40/42/46 字符，未推 Gerrit/sandbox。
- helper 393、参数/转换器 46（包含既有 42）、50 号 5 项、新增 12 项及真实 C-2 正反例通过；12 项展开和 5 项 RPM 解析通过。
- 7706/7706 重放参数一致，assembler token 和 -g0 均为 0；一个真实 release 成员新旧转换输出一致。63 号实物副本 strip/RUNPATH/debuglink/post 通过，最终 SHA e08724d8… 不变。
- T/D 串行演练通过，log-restarts=0，FLAGS 对 QB 一致，WARNING=0，无残留；未运行 Ninja 或完整构建。
- 参数一致已全量核对；转换输出仅实测一个真实成员；整包一致尚未重建验证。其余挂账和风险保持。
- [70 号文档](70_second_code_review_fixes.md)；[本轮评审包](../../patches/rebase-359934-20261106-r2/README.md)。

## 2026-11-09：QB 1221204/1221207 与 cli 取消修复

- [71 号](71_qb_1221204_1221207.md)：两次源码均为 7d5e28ca，三个架构 LLVM 全部成功；T 22/22、D 12/12 二进制包载荷逐字节相同，7706 个转换成员 SHA 全同。2 个源码包严格 FAIL，差异全部归因于 converter 源码与 spec VCS；无未解释差异。
- [70 号 §10](70_second_code_review_fixes.md#10-cli-取消漏洞修复与-sandbox-推送2026-11-09)：393+12+2=407 测试通过；12 项 T/D 展开与 5a27edb4 逐字相同。取消后非 GateError 异常返回 128+signal 并打印 traceback，普通异常仍 raise。
- 当前 sandbox/lhmax2025/bolt_pgo = c7fd5eed5e35ca335940239cae349a6936f74a7a；三提交为 a73a7da32049569b1360e9c13d0633c168b8f173, 3dc97ef3a8fae0bbc61b208fa2bc6c369f1146b0, c7fd5eed5e35ca335940239cae349a6936f74a7a。首提交未变，第三提交自身 diff/说明未变，最终只多 helper 的 4 行。
- 359934 仍 NEW / PS10 13c3e223；357163 仍 NEW / PS2 cf4b6777。新 HEAD 尚未完整构建或跑 QB；本轮没有操作 QB、推 refs/for 或删除文件。
- 证据仓库提交为本节所在提交（最终回复提供完整 SHA）。

## 2026-11-09：设计 v4 与第三轮评审材料

- 设计 v4 从 Downloads 移至 W/docs/bolt/design/，并同步发布到 bolt-v4，53,097 B，SHA256 2be0c79a48d34d20cb003f87b9c954154b9c92a2c2d103ab0f6f82643f7615f7；原文不改，v1/v2 保持原样，目标目录未见 v3。
- [第三轮评审包](../../patches/rebase-359934-20261109-r3/README.md) 以 c7fd5eed5e35ca335940239cae349a6936f74a7a 为准：三个完整补丁、BOLT 文本补丁、9 份全文、converter 对 PS10 diff、相对 7d5e28ca 的完整 diff、出处与 SHA256SUMS。导出内容与 Git 对象核对通过。
- 基线仍是总部 359934 PS10（13c3e223，NEW）及其父 cf4b6777（357163，NEW），状态引用今日 §70.10 查询；本轮不改源码、不构建、不推 Gerrit/sandbox。设计正文仍引用旧基线，README 已区分最终代码与历史验证范围。

## 2026-11-09 第三轮代码评审修复：测试停止，未推送 sandbox

详见 [72_third_code_review_fixes.md](72_third_code_review_fixes.md)。本地新链 a65688b1377e91819fcd46a18da36d52b3312089 → 22f1c9fd79de6086ee21f235868c70167868b7ff → fa4f9978c9162d3c6cd2113d0cfe1173f04881c8，基线 PS10/13c3e223，三个 Change-Id 保留。转换器 ar/PIC 边界、WNOWAIT/SIGHUP、同目录工具；helper Rollback 注释；spec bolt_checked 取消传播与提交说明已归并。

通过 helper 393、完整展开 12、Tizen RPM 解析 5。70 号 12 项初始化发现本轮普通 rpmspec -P 输出缺显式平台 post 展开，只含 4 个可选调用而非 5，0 项实际执行，这是本轮夹具输入准备错误。按任务停止：其他新旧测试、7706 重放、实物归档、T/D 演练未执行，未推 sandbox。r4 是未认证材料。此前 c7fd5eed sandbox 和两 change NEW/PS10 仅为历史记录；本轮未重新查询。后续须先修复测试输入准备，不能视为可发版。

## 2026-11-09 第三轮修复续跑：第二步通过，Base-Dev 调用参数错误停止

[72 §7](72_third_code_review_fixes.md) 与 r4 已更新。源码链 a65688b1 / 22f1c9fd / fa4f9978 及 tree 不变。显式展开平台 post 后五调用齐全；全量重跑 472 单元测试、真实 C-2 两项、7706 重放参数、450 归档/7728 成员/7527262 受检重定位、12 展开、5 RPM 解析全部 PASS。

Toolchain rehearsal-02 PASS（QB 1221204 FLAGS 同，WARNING=0、log-restarts=0、资源报告正常、无残留）。Base-Dev 驱动误用两参数形式，漏传末尾 basedev，入口退出 2；未创建新根/启动服务。按停止条件不重试、不推 sandbox、不复查 Gerrit。正确的未执行命令记录在 72 §7.5。新结果与失败原文均保全，尚不具备推送条件。

## 2026-11-09 Base-Dev 补跑：第三步通过，待指定 lease 推送

[72 §8](72_third_code_review_fixes.md) 记录正确 argv 与旧第234行逐字一致；Base-Dev 新建 retry-02，停在 CMake，log-restarts=0，日志58297B，FLAGS 与 QB1221207 全同，WARNING=0，资源报告正常，无残留。至此第二步全量检查和 T/D 两演练通过。源码 a65688b1 / 22f1c9fd / fa4f9978 及 tree 不变；r4已更新。按顺序先发布GitHub材料，随后仅按c7fd5eed显式lease推sandbox，结果另记。

## 2026-11-09 sandbox 推送完成（第三轮代码评审修复）

[72 §9](72_third_code_review_fixes.md) 与 r4：在第二步全量检查、T/D 演练通过且 GitHub 材料先发布后，以 c7fd5eed 显式 lease 一次推送成功。远端 sandbox/lhmax2025/bolt_pgo 已核对为 fa4f9978c9162d3c6cd2113d0cfe1173f04881c8，父链为 22f1c9fd → a65688b1 → 13c3e223 → cf4b6777。359934 NEW/PS10/13c3e223、357163 NEW/PS2/cf4b6777，推后均未关闭。三个本地提交和 tree 不变。只推该 sandbox，无 refs/for、无 QB 操作、无完整构建；现场保留。


## 2026-11-10：QB 1223601/1223602 核对，源码包白名单停止

[73 号](73_qb_1223601_1223602.md)：源码均 fa4f9978，T/D 三架构成功；34 个二进制包载荷逐字节相同，FLAGS/profile 同基线、WARNING 和 shell not found 均 0。两源码包多出 0008 混合链接补丁提交说明的两处换行（代码补丁正文全同），超出本任务仅允许 spec/helper/转换器/VCS 的范围，判 FAIL 并停止。每组225个完整静态归档SHA全同；7706成员独立SHA枚举因停止而 NOT RUN。两个工具版本文件 QB 不可见。第二项跳过，未移动v5或改r4README。无源码修改、构建、Gerrit推送或QB操作。


## 2026-11-10：fa4f9978 的 QB 验证完成（用户裁定）

[73 号第 8 节](73_qb_1223601_1223602.md#8-裁定2026-11-10)：0008 提交说明折行是设计方要求，本次白名单漏写属于设计方白名单错误。两份源码包按已归因例外 PASS；两次 QB 三架构成功，34/34 二进制包载荷逐字节相同，每组225个完整归档SHA相同。7706个成员由整体归档相同覆盖，未单独运行。旧FAIL及停止记录保留。

设计 v5 已从 Downloads 移至 W/docs/bolt/design/ 并同步发布到 bolt-v4，60890字节，移动前后 SHA256 均为 6c9776bb34e858c048a800320175ac5eb6a303ea83a9bf75e4425c5904a01ddb。r4 README 已追加 QB 验证，SHA256SUMS 全部校验通过。下一步：**三家完整评审（设计 v5 + r4 代码）**。本轮仅更新文档与评审材料，不推送 Gerrit/sandbox，不操作 QB。

## 2026-11-10：第四轮修复停止在新增 IR 夹具（75 号未完成）

当前有效设计为 [v6.1](design/tizen_llvm_speed_design_v6.1.md)，v6 已作为历史版入库，两份移动前后大小/SHA 均相同。用户三项裁决：ARM 已安装 CMake 模块文本变化接受为行为不变例外；本地完整构建用 fa4f9978（74 号），最终 tree 以 QB 比较衔接且任何发货内容差异使衔接作废；qemu-accel 性能主结论使用 Toolchain 产物。

[75 号](75_fourth_review_fixes.md)：本地链 8a50d712 / 539e2a86 / 80217ff8，基线与 Change-Id 保留。既有 472 项 PASS；新增已执行 11 项（10 PASS、1 FAIL），3 项未运行。失败是本轮夹具把 module asm 放在 source_filename 前面，llvm-as 报 expected top-level entity，尚未进入转换；按指令停止，不修复重试。12 组展开、5 项 RPM 解析及一个真实 release 成员/完整小归档新旧转换逐字节比较通过。450 归档复扫、ARM 模块、lld 包核查和 r5 交付未执行，不能宣称整轮通过。现场与失败原文保全，未推 Gerrit/sandbox、未操作 QB、未启动完整构建。

先补齐本轮验证。之后仍按用户指定顺序：夜间完整构建（fa4f9978，74 号）→等用户授权 sandbox→QB 重跑→三家完整评审（设计 v6.1 + 完成认证后的 r5）。75 号当前为停止记录，不是完成认证。

FOURTH_REVIEW 已结束 2026-11-10T22:03:24+08:00 status=stopped reason=module_asm_fixture_parse_error

## 2026-11-10：75 号续跑完成，r5 仅本地待后续认证

[75 号 §6](75_fourth_review_fixes.md#6-续跑2026-11-10)：修正 IR 夹具追加位置、R_X86_64_NONE 偏移例外和两段提交说明；源码链 8a50d712 / 35861544 / 60fabc72，Change-Id 保留，首提交 tree 不变。487/487 测试从头通过，12 展开/5 RPM 解析通过，450 归档/7728 成员/7527262 重定位新旧结果一致（7706 转换成员零拒绝）；真实 release 成员及完整小归档字节相同。第一次停止记录原文保留。

四组 ARM 包的 AddLLVM/AddClang 与 fa4f9978 相同、对 PS10 仅混合链接变化，AddLLD 未安装。发现同快照且无混合链接的 Base-Dev 历史 ARM 候选 QB1214821，但公开 RPM 目录现为404；Toolchain 未找到。两份 x86 初始化清单没有独立 lld 包，ld.lld 包归属在日志中未打印。相关证据边界已明确记录。

[评审包 r5](../../patches/rebase-359934-20261110-r5/README.md) 已导出并校验；72/73 和 r4 指定说明已同步。未完整构建、未推 Gerrit/sandbox、未操作 QB；不能把轻量检查当作新版本整包认证。**接下来依次是夜间完整构建（fa4f9978，74 号）、等用户授权推送 sandbox、QB 重跑、三家完整评审（设计 v6.1 + r5 代码）。**

FOURTH_REVIEW_RESUME 已结束 2026-11-10T22:32:46+08:00 status=ok reason=487_tests_expansion_archives_and_review_bundle_pass

## 2026-11-10：r5 sandbox 已推送，ARM 基线已找到（76 号）

[76 号](76_sandbox_push_r5.md)：全部前置核对通过后，以 fa4f9978 显式 lease 一次推送成功；sandbox/lhmax2025/bolt_pgo 已核对为 **60fabc723f30c5cc04146a9dd83487ebed63f259**。父链为 35861544 → 8a50d712 → 13c3e223 → cf4b6777。三个源码 tree 与 75 §6.1/r5 一致；未改源码、未建分支、未推 refs/for、未构建或操作 QB。推后查询 359934 NEW / PS10，357163 NEW / PS2。

ARM 可用基线已找到：**QB 1216401（Toolchain）和 1216400（Base-Dev）**。两者均为总部 PS7/463c9a13，源码相对无混合链接基线只改转换器；Profile URL 分别为 tizen-base-toolchain_20261030.061318、tizen-base-dev_20261030.061217，与 1223601/1223602 匹配。概览/公开 manifest 确认源码，两个 ARM 架构目录及 clang、llvm-devel 的 HEAD 均为200；未下载 RPM、未做内容比较。

下一步依次：**用户启动两个项目的 QB → 夜间完整构建（fa4f9978，74 号）→ QB 核对 → 三家完整评审（设计 v6.1 + r5 代码）**。

R5_SANDBOX 已结束 2026-11-10T23:26:22+08:00 status=ok

## 2026-11-10：74 号启动前停止，T/D 未运行

[74 号](74_local_full_build_fa4f9978.md)：无其他任务服务，fa4f9978 对象及 tree c9f61c77 正确，/home 可用约 313.11 GiB，超过151.3 GiB。只读检查发现 rebase-launch-20261106-r2/basedev/launch.sh 不接受 full basedev（仅 night / rehearsal / rehearsal-02）；两个入口还要求固定源码目录 HEAD 等于传入 SHA，而该目录当前为60fabc72。按 argv 不符停止，未启动 T/D、未改入口、未切换源码、未直接绕过 shell 入口。

构建审计、归因材料、两组包比较、T/D 函数比较和 install/LLDB 均 NOT RUN；资源峰值 UNKNOWN。本轮不推 Gerrit/sandbox、不操作 QB、不执行 sudo。后续需先处理完整构建入口与固定源码视图，再执行74号；76号的sandbox和ARM候选结论不变。

LOCAL74 已结束 2026-11-10T23:30:01+08:00 status=stopped reason=entry_preflight_blocked


## 2026-11-11：r5 的 QB 验证及 ARM PS7 基线比较完成（77 号）

[77 号](77_qb_1225393_1225395.md)：1225393=Toolchain、1225395=Base-Dev，源码均为60fabc723f30c5cc04146a9dd83487ebed63f259，固定输入快照与1223601/1223602一致，三架构均成功。对fa4f9978：x86_64 34/34、ARM 68/68二进制包载荷全同；两组各225完整归档SHA全同；源码包仅spec/转换器/VCS和授权0008说明变化，PASS。FLAGS/profile同旧QB，WARNING及shell not found、取消/SIGCHLD_RESET均0，NATIVE_ARCHIVES_TOOLS明确三个工具22.1.8且同目录。

ARM对PS7基线1216401/1216400：68/68包PASS，60包全同，8包只含AddLLVM/AddClang精确混合链接文本变化；PS7→PS10仅x86转换器变动，不影响ARM。记录过一次辅助邮件标题断言问题及重复Git读取超时；原文保留，最终均以精确字节证据闭合，未OOM。7706成员由整体归档相同覆盖，未另行逐成员算SHA。未构建、未操作QB、未推Gerrit/sandbox；74号启动前停止仍未解决。后续仍需74号本地完整构建及三家完整评审（设计v6.1+r5）。


## 2026-11-11 第五轮评审修复（78 号，测试准备错误停止）

设计 v7 已移动并核对 81285 B / 11dc134f…8d004。源码起点 60fabc72，fixup/autosquash 后本地 HEAD ae4487251aaa00c2ec4edf033cf8c9046d0d4b98；混合链接 8a50d712 不变，尚未完整认证。

helper 已运行 199 项，198 PASS、1 ERROR：本轮测试副本将夹具路径误写为 /review-closure-v3.py，导入失败。计划 499 项，其余 300 项未运行。按门禁停止，无修正重跑、无 OOM；450 归档复扫、10 个 debug 归档转换、两组 census、完整 12/5 检查、r6、sandbox 查询/推送均 NOT RUN。

详见 [78 号](78_fifth_review_fixes.md)。下一步先修正测试输入，再从头重跑全套，不能沿用部分 PASS。上一轮 sandbox 为 60fabc72，本轮没有访问 Gerrit 或更新远端。

FIFTH_REVIEW 已结束 2026-11-11T14:42:18+08:00 status=stopped reason=test_fixture_import_error


## 2026-11-11 第五轮续跑再次停止（78 号 §6）

源码 ae448725 / bea0348f 未改，工作树干净。测试副本的 results 路径已修正，3 份差异仅路径，20 个显式路径存在；但预检遗漏了参数套件的 debug-census.json 依赖。

本轮 helper 393/393 PASS；参数/转换器运行 27，26 PASS、1 ERROR（test_debug_yes 读取本轮缺失的 debug-census.json）。累计 420 项，419 PASS、1 ERROR；计划 499，其余 79 NOT RUN。没有补文件重跑。历史输入存在，属于本轮准备遗漏，不是产品门禁拒绝。450 归档/10 个 debug 库/census/完整 12+5 检查/r6/sandbox 查询推送全部 NOT RUN，无 OOM。详见 [78 号续跑](78_fifth_review_fixes.md#6-续跑2026-11-11路径已修正另一项输入遗漏后停止)。

FIFTH_REVIEW_RESUME 已结束 2026-11-11T14:50:27+08:00 status=stopped reason=missing_test_input_debug_census


## 2026-11-11 第五轮第二次续跑（78 号 §7，产品取消路径 FAIL）

完整复制75号已通过环境（282文件），预检361依赖、187读取表达式，本轮准备修正0次。六套从头运行：helper393、policy46、release5、R2 12、cli2全通过；R3/R4/R5运行17，16 PASS、1 FAIL。累计475项，474 PASS、1 FAIL，其余24 NOT RUN。

test_cli_mid_conversion_signals：SIGTERM应返回143，实际1。转换器 install_main 使用 sys.exc_info() 但没有 import sys，原取消异常被 NameError 覆盖。这是产品实现错误，已停止，不改代码、不调整预期、不重试。源码仍ae448725/tree bea0348f且干净。450归档、10个debug库、两组census、完整12/5检查、r6、sandbox查询/推送均NOT RUN，无OOM。详见 [78号第二次续跑](78_fifth_review_fixes.md)。

FIFTH_REVIEW_RERUN2 已结束 2026-11-11T15:03:47+08:00 status=stopped reason=converter_missing_sys_import


## 2026-11-11 第五轮第三次续跑（78号§8）：499项通过，实物复核驱动断言停止

仅补转换器import sys，fixup/autosquash后本地HEAD **fea0fe464d56e17f2c7588c557bfffd9f6ac352b** / tree **b2e8af2477cf623a945aa80bf8288a262dd4a5a9**；前两提交8a50d712、1e415935及tree不变，说明/Change-Id不变，工作树干净。pyflakes未安装，按指令NOT RUN。

499/499从头PASS（393+46+5+12+2+41），准备修正0次，上次test_cli_mid_conversion_signals已PASS。450个QB归档/7728成员（7706转换+22原生）新旧检查全同，零新增拒绝；第一组census共11种类型、94400431条调试节重定位，无表外类型。

已复制63号最大的10个ThinLTO库。首个libclangSema.a新旧转换均成功，86成员、完整归档SHA同为8de79182…f3de；随后复核驱动把inspect结果中的old/new输出path也作相等断言，触发AssertionError。只读定位唯一差异是path字段，是执行方的复核驱动错误。按停止规则未改断言重跑；其余9库、第二组census、12展开/5解析、r6和sandbox查询/推送均NOT RUN。无OOM，未构建或操作QB，现场保留。详见[78号第三次续跑](78_fifth_review_fixes.md#8-第三次续跑2026-11-11import-sys-已修正实物复核驱动断言停止)。

FIFTH_REVIEW_RERUN3 已结束 2026-11-11T15:39:20+08:00 status=stopped reason=verification_driver_compared_output_path


## 2026-11-11 第五轮第四次续跑（78号§9）：验证通过，MERGED状态阻止指定推送

源码fea0fe46 / tree b2e8af24及三个提交未改；仅按用户裁决从实物核对驱动排除inspect.path，修正次数1/2。10/10最大debug ThinLTO归档输出新旧逐字节相同，1100成员（1093转换、7原生）；第二组census调试节35560547条（类型1/10），全部7种类型，无表外类型、无新增拒绝。12展开/5RPM解析及独立说明检查PASS。同一HEAD此前499项与450归档结果保持有效。r6生成，17文件SHA校验PASS。

推送前sandbox确认为60fabc72；但359934已MERGED/PS10/13c3e223、357163已MERGED/PS2/cf4b6777（两者lastUpdated=2026-11-11T12:28:07+08:00），不满足用户要求仍NEW，因此未推送，没有推后SHA新观测。需要用户裁决该新状态后再继续，不能自行豁免。

[74号](74_local_full_build_fa4f9978.md)追加入口准备停止记录：新clone/新入口未创建，自测0项，T/D演练及夜间预算未运行；今晚命令未准备，不启动完整构建。详见[78号](78_fifth_review_fixes.md)、[r6](../../patches/rebase-359934-20261111-r6/README.md)。没有删除文件、操作QB或修改历史根。

FIFTH_REVIEW_RERUN4 已结束 2026-11-11T16:58:21+08:00 status=stopped reason=Gerrit_changes_MERGED_required_NEW


## 2026-11-11：总部合入已确认，r6 sandbox推送完成（78号§10）

359934/PS10/13c3e223与357163/PS2/cf4b6777已于2026-11-11T12:28:07+08:00由Dongkyun Son提交合入。tizen_base HEAD为61ef5d31ca91025c414c748477bef0c64ddfa67c，判定B：是13c3e223后代，后续仅1个合并提交，tree和完整diff均无内容变化；本地分支未改，不需要改接。

按用户新前提，以60fabc72明确lease一次推送sandbox成功，推后ls-remote已核对 **fea0fe464d56e17f2c7588c557bfffd9f6ac352b**。r6校验17项PASS，源码三提交与tree不变。详见[78号第五次续跑](78_fifth_review_fixes.md#10-第五次续跑2026-11-11总部合入判定bsandbox推送完成)。

公开目录最新快照：Toolchain tizen-base-toolchain_20261109.032334，Base-Dev tizen-base-dev_20261103.083743；仅记录，固定比较/构建快照不变。先发布本节，下一步准备fea0fe46独立源码副本和r6本地入口、串行T/D演练，记74号；不启动完整构建、不操作QB。

R6_SANDBOX 已结束 2026-11-11T17:17:44+08:00 status=ok


## 2026-11-11：sandbox fea0fe46 已发布；r6 夜间入口模板审计停止（74号§6）

78号推送阶段已完成（37d3e9d1）：总部两change已合入，tizen_base判定B，sandbox为fea0fe464d56e17f2c7588c557bfffd9f6ac352b。独立源码副本已克隆并核对HEAD/tree/父链/干净detached及远端一致，保留不动。

复制入口前发现r2的basedev/night.py始终调用basedev launcher，T会用旧20261013快照；协调器结果根/服务名与launcher不一致；新汇总目录没有创建即写文件。不能仅按获准的SOURCE/输出根/N/服务名替换完成，按“不改逻辑”停止，未新建入口、自测执行0项、T/D演练NOT RUN、完整构建未启动。/home可用258.308 GiB，预算通过。详见[74号§6](74_local_full_build_fa4f9978.md#6-入口准备与演练2026-11-11sandbox-已更新模板-night-调度审计停止)。今晚命令仅记录，尚不可执行。

ITEM3 已结束 2026-11-11T17:24:03.087548+08:00 status=stopped reason=template-night-dispatch-and-summary-directory-outside-allowed-edits


## 2026-11-11：fea0fe46 本地入口与 T/D 演练完成（74号§7）

新 tools/bolt/rebase-launch-20261111-r6 已准备，B 发布副本与 W 执行副本完全相同，原 r2 入口不变。按本轮授权新增 run-night.sh 分别调用 T/D 入口，Base-Dev shell 增加 full basedev；旧 night.py 保持原样不用。源码副本 fea0fe46 / tree b2e8af24 干净，sandbox只读确认同一SHA，未推Gerrit或sandbox、未操作QB。

T快照20261030.061318 / build.conf 8f201a0d…；D快照20261030.061217 / build.conf 8ace286a…，与QB1225393/1225395保全记录一致。入口自带82项：80PASS、2项原有不适用SKIP；新增串行协调6/6模拟用例PASS。路径输入定位修正1/2次，仅修正72号T命令证据的读取，期望/产品/源码未变。dry-run的argv、服务名和输出根一致。

T/D各一次演练均在 + cmake -G Ninja 停止，未运行Ninja；log-restarts=0、FLAGS与各自QB一致、WARNING=0，复制日志与原日志SHA/大小相同，资源报告生成，清理审计通过。全部完整根及汇总目录不存在，/home剩余244.021 GiB≥151.3GiB。本轮没有启动完整构建；今晚命令与进度查看见[74号§7](74_local_full_build_fa4f9978.md#7-入口准备与演练2026-11-11第二次)。

ENTRY_PREP2 已结束 2026-11-11T18:03:29.724748+08:00 status=ok reason=T_D_rehearsals_pass_full_build_not_started


## 2026-11-12：fea0fe46 T/D 完整构建、审计与比较完成（74号§8）

串行入口已修正，98项测试：96PASS、2项原有SKIP、无FAIL/ERROR。Linger=no，启动时已告知不要注销。T/D GBS均exit0、无OOM；原队列T=failed（旧自动包比较）、D=ok，原失败保留。新增审计/比较在8GiB受限服务串行完成。

指定QB1225393/1225395：T22/22二进制包按67号口径B PASS，D12/12载荷原始内容相同；各225静态归档的3853转换+11原生成员逐SHA全同，合计7706+22。FLAGS/profile/门禁/工具22.1.8检查通过，T/D最终参数仅差-g2/-gdwarf-4/-g。两份源码包原始FAIL保留：GBS合并源码tar vs QB八补丁、packaging目录及.git_archival提交标识的差异已逐文件归因，未扩大白名单。

T RPM在新的rootless namespace中实际安装，LLDB自动加载符号，21/21 clang帧与llvm-symbolizer一致，冷函数抽查通过；无额外sudo。T/D BOLT输入与改写日志已保全，函数差异清单已生成，只记录事实。资源数据及UNKNOWN、du超时见[74号§8](74_local_full_build_fa4f9978.md#8-入口修正与完整构建fea0fe46)。全部根/副本保留，无Gerrit/sandbox推送或QB操作。

LOCAL_FULL_R6 已结束 2026-11-12T12:13:57.322734+08:00 status=completed_with_differences reason=builds_ok_binary_policyB_pass_source_raw_FAIL_attributed


## 2026-11-12：74号放行后的 PM 裁决（79号 A2）

R1 T 的 controller status=failed，唯一来源是入口内置检查 QB-23-packages 用了过时的 r2 模板基线；其余 6 项 PASS。这不是产品失败，以 §8.6 的规则 B 比较为准。原 result.json 不动。

R2 第 8 条定案。本地 GBS 对 QB 源码包的“已知差异固定清单”只有以下五项，清单外任何差异仍判 FAIL：

- (a) 内容 SHA 相同、只有权限 0664/0644 不同的文件：Source1200、模型 tar、llvm.manifest；

  **PM 修正（2026-11-12T21:00:58.812766+08:00，原文保留）：** R2(a) 由“指定文件名清单”改为按规律判定：源码包中内容 SHA 相同、仅权限为本地 0664 对 QB 0644（只差组写位）的文件，属于已知差异。其他任何权限变化（含可执行位、属主、其他位）仍判 FAIL。

  原因：原清单是 PM 起草时漏列。74 号比较的是 60fabc72 的 QB，helper 和转换器当时内容不同，权限差异被内容差异覆盖；同提交比较时才暴露。来源相同，都是本地 GBS 导出的权限。

- (b) QB 把补丁 0001–0008 作为独立 source 文件，本地 tar 里补丁已经应用；应用 QB 补丁后，受影响的文件必须逐个一致；
- (c) 本地多出 packaging/ 目录及其文件，每个文件的内容必须与当次提交的 git 对象 SHA 一致；
- (d) clang/bindings/python/.git_archival.txt 的 node、node-date、describe-name 三行；
- (e) spec 中的 VCS、Release，以及 Patch/%patch 写法差异。

比较报告把“原始结果”和“按第 8 条清单归类后的结果”分开展示，原始 FAIL 照常保留。

**PM 判定方式修正（2026-11-12T22:18:04.265385+08:00，前述原文保留）：**

R2 对源码包的每个文件分两个维度独立判定，两项都通过该文件才通过：
- 权限维度：只差组写位（本地 0664、QB 0644）为已知差异，不论内容是否相同；其他任何权限、属主、链接变化判 FAIL。
- 内容维度：内容 SHA 相同直接通过；不同时只能由 R2 (b)(c)(d)(e) 解释，并且需要有逐项证据；无法解释的判 FAIL。
原因：PM 起草的 R2(a) 把权限例外绑在“内容相同”上，tar 和 spec 两头都套不上。拆开判定不放宽任何一个维度。


R3 74 号放行：fea0fe46 本地 T/D 完整构建通过上传门槛。

R4 决策 18：通用级和建议级的加固项推迟到上传后的跟进补丁；第 7 轮评审只做定向检查，不阻塞上传；评审只看问题是否严重。

R5 T 的 memory.peak 等于 MemoryMax，触顶事件 3877 次，无 OOM。作为资源数据记入，现在不处理。

R6 T/D 函数差异只记录事实，因果留给以后的归因实验。

设计 v8 已按大小及SHA核对后移动到 docs/bolt/design/；79号QB核对随后执行，不提前宣称新QB通过。


## 2026-11-12：79号 A整理完成，QB核对停在B5补充脚本

设计v8已移动并核对86911字节/SHA05f8aa29…；74§8.10的R1–R6裁决已追加，r6 README已更新实际放行状态；三个最终提交说明仅生成草稿，LLVM仓库未改写。

1226850=Tizen-Base-Toolchain、1226851=Tizen-Base-Dev，均为fea0fe46/tree b2e8af24，三个架构成功。B1–B4 PASS：102二进制包载荷一致；1294静态归档22520成员逐SHA相同；源码包仅3文件Git差异+VCS，0001–0008全部不变。x86两组转换7706、保留22均覆盖。

B5主体日志检查完成；补充脚本把Warnings.cpp、Cancellation.cpp等编译输入文件名误当告警，因Ninja编号不同触发断言。按停止规则未修判定重跑，B5未完成、B6未运行，总结论待PM裁决；不是已证实的产品失败。准备路径错误修正1次，原文和diff保留。详见[79号](79_qb_1226850_1226851.md)。只发布证据到bolt-v4，无LLVM/Gerrit/sandbox写操作。

79_ANALYSIS 已结束 2026-11-12T16:37:16+08:00 status=待PM裁决 reason=audit-script-filename-false-positive


## 2026-11-12：79号 B5 误报 PM 裁决与续跑

B5 第一次停止属于核对脚本误报：8 条命中都是 Ninja 进度行（"[N/7633] Building CXX object …"），旧 QB 1225393 的日志中有同样的 8 行，只有进度编号不同；新旧日志的命中总数都是 3357。这不是产品差异。原停止记录保留不动。

PM 授权的修正规则：先去掉行首时间戳和 Ninja 进度前缀，再按多重集合比较；单列非编译进度的真正诊断行。此次规则修正不计入准备错误次数。补跑 B5、B6 的结果见后续新增小节，旧结果不覆盖。


## 2026-11-12：79号续跑停止于B6源码权限固定清单

B5已按PM规则补跑T/D并通过：去时间戳和Ninja进度后新增/缺少均0；关键词命中T3357/3357、D3225/3225，真正诊断T465/465、D333/333，最终FLAGS和三级SHA均与基线相同。原误报证据保留，新结果在qb-1226850-1226851/resume-20261112/。

B6 T对1226850：22个二进制包规则B全部PASS，271静态归档5829成员相同。源码包原始FAIL；按R2精确清单归类仍FAIL：clang-bolt-helper.py及llvm-static-archives-native.py各自内容SHA相同，但本地0664、QB0644，不在R2(a)限定的Source1200/模型tar/llvm.manifest清单内。未扩大例外；T源码tar后续归因、D的B6、0003-v2和claims-to-code按停止规则NOT RUN。见[79号续跑](79_qb_1226850_1226851.md#79号续跑2026-11-12b5通过b6在固定清单外权限差异停止)。

B6 已结束 2026-11-12T20:51:18.957479+08:00 status=FAIL reason=source_permissions_outside_R2a

## 2026-11-12：79号续二，R2(a)已按PM修正，B6最终审计停止

新R2(a)已同步74号§8.10并保留原文。T的7个原始内容相同、只差组写位的文件通过重新分类；T二进制22/22、D二进制12/12规则B PASS。两组各271归档5829成员相同。源码包原始FAIL保留；补丁/packaging/git_archival/spec内容已完成核对。

新源码归类脚本错误组合内容与权限例外，临时PASS已被最终审计否决：T/D的tar和spec原始SHA不同、权限0664/0644，不满足R2(a)明确的等SHA前提。没有自行放宽或重跑；B6最终FAIL，0003-v2及claims-to-code未运行。需PM裁决是否允许这两类已归因内容差异与组写位差异组合。见[79号续二](79_qb_1226850_1226851.md#79号续二r2a修正后的b6复核与停止)。

B6 已结束 2026-11-12T21:07:46.411610+08:00 status=FAIL reason=source_tar_spec_mode_exception_requires_equal_SHA

## 2026-11-12：79号续三完成，B1–B6最终PASS

PM将R2权限/内容改为独立判定，已同步74号§8.10、79号并保留原文。T/D源码包9个共同文件的权限与内容分别PASS，8个独立补丁按R2(b)记录；不重新解包。两组tar各27个补丁目标、额外12个packaging文件、git_archival三行及spec的R2(e)差异都有逐项证据。源码包原始FAIL及之前审计否决仍保留，新R2最终均PASS。

B1–B5复用已完成证据；B6二进制T22/D12规则B PASS，源码按最新R2 PASS，79号总判定PASS。0003-final-draft-v2.txt及两份diff已生成，最长72列、连字符词不拆分；claims-to-code为5句对应、0句不符，并明确NONE偏移例外、原生成员不拦截forbidden及压缩声明大小边界。仅证据文件，LLVM提交/分支未变。

详见[79号最新结果](79_qb_1226850_1226851.md#r2-判定方式修正79号续三)和[草稿核对](../../tools/bolt/results/qb-1226850-1226851/commit-message-drafts/0003-claims-to-code.md)。本轮无构建、无QB访问、无Gerrit/sandbox操作。

## 2026-11-12：80号最终提交说明完成，sandbox更新为4e80f54e

新链8e35d0c90d5d87924b2f268b5ef20317e6b805d8 → 51417b0fa060154ad887e362235c68488003d009 → 4e80f54e10fe920439455123f0ac2cb8af5ab924。
三个tree分别仍为3d961cbb04f5446f84d2089b4f65f3178f2bd7fa、c23914776684bf94fdd5961f447f7c24e7bb79bc、b2e8af2477cf623a945aa80bf8288a262dd4a5a9；作者及作者日期不变，Change-Id和Signed-off-by不变。新消息与c413b67e指定草稿逐字节一致。最终git diff为空，range-diff只含说明差异。输出解析准备误报修正1次，原文保留。

tizen_base仍为61ef5d31ca91025c414c748477bef0c64ddfa67c，verdict B。sandbox以指定lease从fea0fe46推至4e80f54e，推后ls-remote一致，仅此一次LLVM远端推送，无refs/for或其他分支。原工作分支不动，新链在独立游离工作树。

PM裁决：只改提交说明、树不变，不需要新QB。源码包中0008补丁文件只有提交说明部分和首行提交号会变，代码正文不变；QB1226850/1226851对新HEAD有效。79号B1–B6 PASS，原始源码FAIL保留。

[80号](80_final_message_push.md)；[r7评审包](../../patches/rebase-359934-20261112-r7/README.md)。不构建、不访问QB；下一步按PM安排进行评审。

## 2026-11-13：81号续完成，第一批已上传 Gerrit，评审中

新链 c5244e13258bb541458dcd4a08254217d7c556a9 → bde009d1197a09f7b7b76382a0166e03c841bdb9 → 2cdd37ff747765e99c2befa3e6e8a88663ab77fe。
三个tree仍为3d961cbb04f5446f84d2089b4f65f3178f2bd7fa / c23914776684bf94fdd5961f447f7c24e7bb79bc / b2e8af2477cf623a945aa80bf8288a262dd4a5a9；作者/作者日期不变。0003仅明确“For converted PIC members”；本次续跑只更新时间重建，说明与上次链完全相同。

[361395](https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/361395)（混合链接）、[361396](https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/361396)（BOLT）、[361397](https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/361397)（固定参数/转换器）均NEW/tizen_base/PS1，revision及依赖核对通过。上传成功后sandbox已同步为2cdd37ff747765e99c2befa3e6e8a88663ab77fe；tizen_base仍verdict B。未加评审人、未打分、未提交合入。

第七轮评审结论（PM提供）：两家都判可以上传，没有严重问题。上传后跟进清单：入口子服务状态改为白名单及其他入口小项（下次使用入口之前完成）、产品加固补丁、claims文档补充PS10对照。设计以[v9](design/tizen_llvm_speed_design_v9.md)为准，95367字节，SHA256 534ac688da10ee10f3905a0780ec71da2c57b5a3b24e5cdad50f1963e070b989，已从Downloads移动并核对。

新规则：以后推送新patch set时，必须先推refs/for，成功后再同步sandbox，不能先推sandbox。第一次no new changes为PM推送顺序安排错误，不是代码失败，拒绝原文保留。

[81号](81_gerrit_upload.md)；[r8评审包](../../patches/rebase-359934-20261113-r8/README.md)。本轮未构建、未访问QB，旧证据保留。

## 夜间 82–84（2026-11-13）

- **82 PASS**：[入口跟进](82_entry_fixes.md)已完成。子服务仅 inactive/failed 放行；启动前记录 started；Base-Dev launcher 限定项目；Linger=no 仅警告。原16项加新14项，**30/30通过**；准备修正2次（夹具故障注入、收尾校验输出路径），原始错误保留。SHA256SUMS和dry-run通过；没有启动构建。
- **83 PASS（差异描述）**：[函数比较](83_td_function_diff.md)三项已知答案全部通过。两侧147113条函数记录，99048规范化相同、47997只差重定位目标/addend、68机器码不同、单侧0；原3543个对不上的名字各自全部通过ThinLTO后缀规范化配上。包含337条零大小符号，实际有非空字节的相同函数98711。68条差异缺少DWARF/可用STT_FILE，源文件前50聚合UNKNOWN；D report-stale待资源报备，未运行；不作因果推断。
- **84 PASS（已有资源拆分）**：[资源表](84_resource_breakdown.md)独立列出本地63-T、74-T/D及六份已存QB日志。恢复15个本地ThinLTO链接区间及九份日志的阶段窗口；QB链接起点、rewrite/strip等独立耗时、全构建进程峰值、anon/file、分层磁盘峰值仍UNKNOWN。74-T memory.peak≥24482992128 B（截断），max3877、oom0，时长受内存回收影响，不能作为候选实验对照基线；du32次超时，峰值只是91次成功样本最大值。候选表只定位阶段及现有占比，不排序、不判断可接受性。
- 操作边界：仅证据仓库bolt-v4；LLVM仓库、历史构建根和旧结果未修改；未访问QB/Gerrit，未运行完整构建，未删除文件。83的小夹具按用户授权使用74根平台clang/lld及其loader，在新证据目录编译。证据：[night-82-84-20261113](../../tools/bolt/results/night-82-84-20261113/)。
- 82 已结束 2026-11-13T00:40:15.356186+08:00 status=PASS
- 83 已结束 2026-11-13T00:47:25.773770+08:00 status=PASS
- 84 已结束 2026-11-13T00:56:47.575244+08:00 status=PASS


## 2026-11-14：PM 交接快照（85号）

[85号交接](85_handover_snapshot.md)；[全部新证据raw索引](../../tools/bolt/results/handover-20261114/RAW_LINKS.md)。只读盘点，不推进产品，结论PARTIAL。

- Gerrit 361395/361396/361397仍NEW/tizen_base/PS1，revision分别c5244e13、bde009d1、2cdd37ff；sandbox仍2cdd37ff747765e99c2befa3e6e8a88663ab77fe。tizen_base=61ef5d31ca91025c414c748477bef0c64ddfa67c，PS10祖先、仅合并提交、tree与内容相同，本周verdict B；无fetch或LLVM推送。
- SSH原文只返回上传评论，评审人/approvals字段未返回；REST GET为404，独立行内评论/Label完整性UNKNOWN。不把未返回写成全部为零。
- 82修复在B已完成30/30，但W执行入口副本仍有5个文件与B不同。下次使用前需另行授权同步/复核；85不修入口、不构建。
- 目录223条、du成功193、超时29、其他失败1；未知不估算。/home采样可用69,934,309,376B（约65.13GiB），不足历史151.3GiB两根阈值。旧仓库扩展扫描服务005达到4G被OOM，27个旧仓库汇总未保存，UNKNOWN；未提高限制、未重试。
- claims步骤STOP：PS10 L376为kind in (10, 11)，fea0fe46 L533为kind in (10, 11, 12, 14)，整条条件不同；按用户指令不追加“条件相同”句，原文件保持不动。需PM裁决准确措辞。
- 41项交接表覆盖入口、产品加固、claims、Gerrit、T/D归因、84缺采、V1b/V2、资源报备、乙一、§7未决、§8风险及每周基线。建议11/16起先确认裁决/入口部署和资源，再推进身份方法/归因/乙一；历史一次授权不延续。旧失败原文保留，最新状态按85及81–84读取。

85 交接已结束 2026-11-14T15:00:48+08:00 status=PARTIAL（步骤5 STOP；盲区见85）


## 2026-11-14：86号

[86号报告](86_claims_entry_bolt_warnings.md)。各步骤独立：1 PASS；2 STOP；3 STOP；4 PASS_WITH_UNKNOWN；5 STOP。未构建、未访问QB/Gerrit、未改LLVM。

- PM定性：85步骤5的STOP正确，是PM前提错误（整条条件相等），不计准备错误。PS10外层已有ALLOC过滤；32/32S/64的有效PIC政策与fea等价。全路径/192合法组合核对通过，claims已补父提交PS10说明；新增解析加固不称整函数接受集合相同。
- W授权五文件已备份同步，SHA均与B一致；完整清单还报basedev/SHA256SUMS、basedev/provenance.json及缺失顶层provenance.json。未越权同步、未回滚；30项测试及dry-run NOT RUN，下次使用仍阻塞。
- 74本地T/D内部BOLT日志各有10个jump-past-end和2804重定位汇总；58/59 PGO为2个和1551。QB保存主日志没有内部告警，不等于没有告警。22组定向反汇编保存；读取旧3ee2d847源码对象失败后STOP，可达性及类型/节细分未完成。
- 830在A构建stdout；B的23次训练stdout/stderr为0。C显式23个profraw全部对应B专用目录，保全SHA一致，A构建profile未进入该52,528,216B合并结果。每条警告精确PID及A默认profile内容UNKNOWN。
- 资源报备脚本argv切片断言失败，未修正/重跑；没有生成经核对的命令/采集/磁盘报备稿，仍需后续完成。所有STOP原文见86；已有证据不覆盖。


## 2026-11-14：87号

[87号报告](87_entry_sync_bolt_nop_resource_plan.md)。PM定性：86三个STOP为准备/清单问题，不是产品失败；86步骤3、5获批修正不计准备错误。
- 入口步骤本轮首次只读命令遇到rg缺失（rc127）STOP，未同步W、未运行两级校验或30测试/dry-run。86五文件同步保持现场；部署仍阻塞。
- fea产品T/D10处jump-past-end一一对应（需规范化一处ThinLTO数字后缀），目标/相对偏移核对。源码归因2处A、8处B；不能称全部严格证明不可达，不作“无害”结论。PGO同名两处旧源码UNKNOWN。
- 2804是BOLT对筛选后不支持重定位的计数；逐条日志需要LLVM_DEBUG/-debug-only=bolt。74两侧工具以-DNDEBUG构建，现有工具无法恢复明细，需另行裁决诊断工具或离线方案。最终clang与QB同SHA仅支持告警集合相同的推断，未直接证明QB内部日志。
- 86草案脚本仅argv[5:]→[4:]，成功生成report-stale/采集/清理候选草案，没有执行。当前df可用69,928,734,720B；历史双根最低预算缺口92,517,224,448B；目录大小沿用85限时du。资源申请未获执行授权。
- 执行组织偏差：分析拆成多个串行4GiB用户服务，未做到每步骤仅一个；全部无并行/无OOM。原始错误、证据边界及未运行项见87。


## 2026-11-14：89号

[单一评审准备](89_single_change_prep.md)：STOP（准备脚本错误，非产品失败）。tizen_base 仍为 61ef5d31ca91025c414c748477bef0c64ddfa67c，tree 与 PS10 相同；原三提交 tree 符合要求。脚本错误要求所有旧说明的 trailer 都采用 PS1 的顺序，在 BOLT 原说明处断言失败。未修改断言重跑，未创建工作树或 PS2/PS3；gbs export、解析、note 和补丁均 NOT RUN。无 LLVM/Gerrit/sandbox 写入；原文及读证据边界见89号。

89 已结束 2026-11-14T16:26:31+08:00 status=STOP


## 2026-11-14：89号续与准备错误长期规则

- PM 定性：89首次 STOP 为准备脚本错误，原提示词未说明三个旧 trailer 顺序不同，不是产品问题，不计准备错误次数；原记录保留。
- 自本任务起：准备脚本自身错误（解析假设、下标、路径拼写、工具缺失如 rg），同一步骤允许修正一次并重跑；修正 diff 与首次错误原文均保留。该步骤第二次准备错误仍 STOP。产品门禁、身份/tree核对、比较结果、远端拒绝、资源停止线不适用此例外，失败照旧 STOP。
- [89续](89_single_change_prep.md#89号续)：PS2 `d0b2e82aa90b11251a13b67d890642bf2fa6f66c`、PS3 `ecb2dec72ec5afde9c6c70f166e2ac12b47c093e` 已在新独立游离工作树生成，tree分别c2391477/b2e8af24，父均13c3e223；说明、身份及增量检查通过，原分支不变。
- 两次gbs export成功，但0008文件名/说明、两个spec的Patch7引用与文件名注释变化，超过“仅VCS/提交号”预期，**比较STOP**；0008代码正文相同不自动放行。五项解析及三条note未运行。没有LLVM/Gerrit推送。报告显示缺失diff文件的准备错误修正一次，未改变比较结论。

89续 已结束 2026-11-14T00:40:16-08:00 status=STOP


## 2026-11-14：90号
按设计第7节第8条的冻结规则，先裁决、再比较。单评审方案相对原链导出的已知差异固定为：

1. 两个 spec 的 VCS 行。
2. 两个 spec 中 Patch7 文件名与 %patch 前注释中的文件名；新名由 gbs 根据新标题生成。
3. 0008 文件名和头部（Subject 与提交说明），前提是从第一个 diff --git 到文件末尾逐字节相同。

清单外任何差异仍 STOP。PM 已裁定89续结果符合此三类（0008正文SHA e99fa7abdc0a828c9eb9295c163a239ed7438c0df378446bf10e07ae3a89b6c6，其余18文件全同），据此通过；原STOP记录不删除。本次仍按固定规则独立核对。以后QB源码包比较同样采用此单评审方案已知差异，作为R2(e)的Patch写法差异；不扩展其他规则。PS2相对bde009d1采用同一规则，不涉及Part3。

执行结果待本轮核对记录。

### 90号执行结果（2026-11-14T00:56:59-08:00）

- [90号](90_single_change_push.md)：两组导出按事先冻结清单PASS；每组五项配对解析PASS，Patch0–7全可见；无准备修正、STOP或远端拒绝。
- 361395 NEW/PS3：PS1 c5244e13258bb541458dcd4a08254217d7c556a9不变；PS2 d0b2e82aa90b11251a13b67d890642bf2fa6f66c；PS3 ecb2dec72ec5afde9c6c70f166e2ac12b47c093e。先两次refs/for，再lease同步sandbox：2cdd37ff→ecb2dec7。
- 361396/361397仍NEW/PS1，未放弃。三条note与两份放弃说明只有草稿，尚未发布。最终tree仍b2e8af24，无代码变更或新构建。
- Gerrit成功响应有标题>50字符warning，按本任务72列要求保留，没有重写重试。
- 本任务仅授权三项远端写，证据本地提交后，GitHub证据发布另待确认。


### 90号证据发布补记（2026-11-14T01:10:04-08:00）

用户确认后，已将证据提交 `cc79ac1ba753c7510aae4916d88ed7ee4fa44fc8` 普通推送到 GitHub bolt-v4；ls-remote 精确核对通过。PM授权范围澄清已写入上方长期规则。本轮不再操作任何LLVM远端，也不发布note或放弃说明。

读取README时首次误用仓库根目录README.md，FileNotFoundError；根据git ls-files定位为docs/README.md，路径修正一次，错误与diff保存在90号publication证据。身份核对和推送没有失败、没有重试。


## 2026-11-14：91号

[91号发布记录](91_single_change_notes.md)：PASS。PM定稿PS1/2/3 note已分别发布到361395,1/2/3，每条回读只移除自动Patch Set前缀，正文逐字节一致。361396,1与361397,1已按90号说明放弃，均ABANDONED/PS1；361395仍NEW/PS3（ecb2dec7），PS1/PS2 revision不变。未推代码、未动sandbox、未构建、未投票/增加评审人。

五份文本的ASCII/禁止引用门禁10/10通过。长期对外文本规则已置于STATUS顶部：只用英文，不引用总部不可访问的证据仓库/本地路径，每次发布前执行grep门禁。实际写入严格五项，无STOP、拒绝、准备错误或重试。旧90号草稿保留；本次发布文件位于publish/。

91 已结束 2026-11-14T01:26:43-08:00 status=PASS


## 2026-11-14：88号

[88号](88_entry_sync_reloc_stats_report_stale.md)：入口同步 PASS；补齐 W 的 basedev/SHA256SUMS、basedev/provenance.json 和顶层 provenance.json（覆盖前备份），完整目录一致、两级清单 OK、82号30/30、dry-run PASS。87号缺rg为准备错误，不是产品失败。本轮不使用rg。

T/D 只读ELF统计各复现2804条：TLSGD1536、TLSLD415、DTPOFF32 853，全部.rela.text→.text，差值0；每类20个符号/偏移样例已保全。源码含义是跳过对应静态重定位的后续分析，不作“无害”判断。

D report-stale **STOP/NOT RUN**：`profgen-release-build-20261114c.scope` 内 gbs/rpmbuild/ninja 正在运行，不满足无其他重任务前提；未取共享锁、未运行BOLT、未新建输出根、未删除或干预任何进程。原文：`STOP: other heavy tasks are running; D report-stale not started; shared lock not acquired.` 其他重任务结束后可重新核对前提执行已批准计划。本轮全部操作为单一串行4GiB/swap0/nice19/IO-idle服务。

88号交付脚本另有两次准备错误：第一次tar.gz被忽略；修正后第二次秘密扫描命中脚本自身的标记字符串，按规则STOP且不再改脚本重跑。两份空staging-audit文件原样保留，不能作为审计通过证据；已准备的报告、结果、夹具压缩包及STOP原文正常提交。


## 2026-11-14：92号

[92号](92_tls_relocs_secret_scan.md)：T2804条全量指令分类：1536 IE、1252 LE、16其他（已解码的cmp/mov disp32+imm8）；D抽15条。两边ET_DYN/PIE、PT_TLS memsz65 align8。1951条同序列PLT32(__tls_get_addr)通过输入筛选，最终注册/应用路径UNKNOWN，不能使用“全LE且无残留”结论，标待验证。

秘密扫描456个文件/版本或压缩成员记录，命中2处：21dcb101的88号报告L98和packaging-v2.stderr L3，都是引用扫描断言签名文字、不是私钥正文。按指定排除范围仍STOP，未扩大白名单、未改历史。88号原扫描误报的PM定性保留。

report-stale在2026-11-14T02:10:31.657016-08:00准入SKIPPED：仍有profgen-release-build-20261114c.scope的gbs/rpmbuild/ninja；MemAvailable24765747200B、/home available37301350400B。未取锁、不等、不重试、未运行BOLT。全部原文见新证据目录night-92-20261114。


## 2026-11-14：93号

PM关闭92号秘密扫描：PASS（无凭据）。两处命中是报告/stderr引用扫描断言文字，PM已核对无密钥正文；原STOP与历史不改。长期规则：引用扫描规则自身文字的报告和日志行登记为已知误报，不触发STOP，不豁免实际凭据。92号report-stale SKIPPED正确，周一由PM另行安排，本任务不运行。

[93号](93_tls_output_check.md)总体FAIL/STOP：T/D最终clang SHA及辅助ELF登记通过。T的TPOFF64 GOT集合相同（2槽），最终1537处IE目标全部正确；.text+.text.cold为1536，额外1处在.bolt.org.text 0x27e3521，与输入同地址、同字节、同目标，差值已定位。LD固定data16×3前缀输入415、输出3（均旧节），非零fs位移0；其余412处输出形式未建立对应，覆盖未闭合，不能写全部TLS通过，也不能直接认定产品误编译。原汇总FAIL不改，D指令核对NOT RUN。待PM处理；没有写Gerrit。


## 2026-11-14：94号

PM定性：93号FAIL为固定data16判据的覆盖缺口，不是已发现错误；原记录不改。[94号逐函数静态核对](94_tls_per_function.md) PASS：T/D各1187/1187个函数四项多重集合完全相同，未映射/不同0。辅助BOLT ELF与最终发货clang六个可执行节全同。主体IE1536、LD415、LD基址直线窗口内存操作494；415处LD均去掉冗余data16填充，旧节另保留3 LD和1 IE。每项目GOT集合相同、1537处输出IE目标全正确。全部126处旧节fs指令与输入同地址同字节。结论适用于两项目最终发货clang；不作“无害”或任意跨控制流证明。

未运行构建/BOLT/report-stale，不访问QB/Gerrit，不改LLVM；92号report-stale仍留待PM安排。4GiB/swap0/nice19/idle串行服务；无准备修正或STOP。

94 已结束 2026-11-14T02:56:17.938840-08:00 status=PASS


## 2026-11-14：96号

[96号转换器加固](96_converter_hardening.md)停在步骤1：四项与设计v9 §6/§7.18摘要一致，但第六轮评审原文未定位，不能完成逐条对应；已请求用户提供路径。不是产品失败，未创建源码工作树、未修改LLVM、未创建产品提交、未测试或推送sandbox。远端SHA未查询，不声明sandbox领先PS3。真实输入重放NOT RUN（范围前提未完成，不是空闲准入SKIPPED）；重放PASS之前不得触发QB。

准备错误一次：受限服务无rg，改用grep/find，原文保留。证据仅写B；未执行Gerrit/QB操作。后续从原文范围核对继续。

96步骤1 已结束 2026-11-14T03:28:37.828078-08:00 status=STOP


### 96号续：PM范围裁决与测试停点

评审原文未入库，以设计v9第7节第18条及第6节为准，不再等待原文；原STOP保留，将来原文提供再补对照。本次已在独立detached工作树W/temp/hardening-ps4-20261114/source实现四项，只有转换器未提交修改，spec不变，原分支/工作树未改。

新增15/15通过；既有套件实际68项，67 PASS、1 FAIL；合计83项、82 PASS、1 FAIL，剩余35项未运行。R3.test_converter_sighup在源码中三个信号循环文本计数处失败（3 != 2），新增日志的只读遍历使计数多1，实际HUP探针尚未执行。按任何失败STOP，未改期望或重跑。

没有产品提交、说明草稿、sandbox查询/推送；真实输入重放NOT RUN（测试门禁未通过，不是准入SKIPPED）。不声明sandbox领先PS3；真实输入重放PASS之前不得触发QB。全部证据见96号续节，旧STOP保持。

96续 已结束 2026-11-14T03:39:46.459382-08:00 status=STOP

96号证据补记：首次发布受*.log忽略规则影响缺5份测试日志；以单独后续提交补齐原日志，保留首提交。交付准备修正一次，不涉及产品或测试重跑。
