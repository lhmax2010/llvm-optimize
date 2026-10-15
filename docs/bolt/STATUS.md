# BOLT v4 状态（新会话开场必读）

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

## 2026-10-13 v4.1 本轮计划与人工裁决

1. Quickbuild 只能从 Gerrit 的 llvm 仓库构建。交付方式：把 BOLT 提交推到 Gerrit platform/upstream/llvm 的新 sandbox 分支 sandbox/lhmax2025/bolt_pgo，由 Quickbuild 在 x86_64 下构建。第一目标是"先在 Quickbuild 的 x86_64 上成功构建出 BOLT 版 clang"
2. 新分支基于最新的 tizen_base HEAD 创建；BOLT 补丁直接做在它上面，不叠加 356627、356639
3. 在该 sandbox 提交中，x86_64 的 BOLT 默认开启（Quickbuild 不会传 --with 参数），例如只在 x86_64 生效的 %bcond_without clang_bolt；其他架构不变
4. 磁盘空间由 Codex 自行检查；project_config 由 Codex 自行查询，需要 Gerrit 路径时用户提供


PM裁决：

1. llvm-bolt 来源（周五版）：仅在开启 BOLT 的 x86_64 构建中，向 LLVM 项目列表追加 bolt，只构建 llvm-bolt 目标；install 之后按开启 BOLT 前后 install 清单的差集删除全部 BOLT 产物。硬门禁：最终 buildroot 文件清单与不开 BOLT 的同配方清单相同（clang 实体与别名除外）。standalone 私有子构建今天只做 cmake 配置加 ninja -n 干跑，不作为周五依赖
2. 重链时在链接命令尾部同时追加 -Wl,--emit-relocs 与 -Wl,--strip-debug，取消单独的预剥离步骤。须验证：与"只加 --emit-relocs 重链、再 llvm-strip --strip-debug"相比，全部非调试 ALLOC 节内容、重定位记录、符号表一致；不一致则退回预剥离方案并给出实测内存
3. profile v2 以 xz 压缩后作为 Source，spec 内解压并核对未压缩 SHA d9b132f9…；记录压缩后大小与 SHA
4. 第一版 BOLT 只支持 debug 包开启的构建：请求 BOLT 但 __debug_package 未定义时直接失败，错误信息写明原因；brp-strip 包装器不进入第一版
5. clang 家族别名统一规范为指向 clang-22 的相对软链接，记录链接类型变化；任何别名仍指向旧内容即失败
6. 匹配度门禁：R=(S+U)/(N+U) ≤ 5% 且 S/N ≤ 5%，整数比较，禁用 infer-stale
7. find-debuginfo：BOLT 版 clang 必须无任何调试节；对实际 buildroot 绝对路径做硬断言（不得含 debug 字样），后处理后核查 clang 未被提取或修改
8. 任何门禁失败即构建失败，不自动降级为普通包


新共享重任务锁：/home/linhao/Toolchain/development/heavy-stage.lock，空文件flock独占；持锁≤60min、等锁≤2h，超时跳过该项。重阶段16GiB/swap0/nice15/ionice3/入口MemAvailable≥12GiB/运行低于3GiB终止；轻任务4GiB/nice19/ionice3/入口≥6GiB/串行。不获取归档两锁。R1允许chroot但已有构建文件只读，输出只在BOLT目录；R32/R64只读sysroot。

| 步骤 | 进度/提交 | 产出 |
|---|---|---|
| 1 新分支/环境调查 | 完成；16030e7（完整号见git log） | 04_baseline_and_quickbuild.md；sandbox已原样创建指向cb679968，无新提交 |
| 2 v4.1/补丁草案/fixtures | b6b5624封存；59fixture PASS、静态apply/整树PASS；宏/pipeline未认证 | 01 v4.1、05、tools/bolt、patches/bolt；LLVM本地b3ec4f0 |
| 3 旧树流水线预演 | 未执行；准备异常后依用户规则停止 | 无新重链/BOLT/三目标/30对数据；E/stop-and-recovery.json |
| 4 standalone配置/干跑 | 未执行（停止后不继续产品实验） | 仅LLVMConfig文件现存，兼容性/任务数UNKNOWN |
| 5 90对资产 | 未执行，0/90新文件 | 不是确认材料缺失；未将历史30对冒充90对 |
| 6 profile压缩 | 完成，210f82b；解压SHA PASS | Source9735212B/SHA52fd8522…；uncompressed171232190B/SHA d9b132f9… |
| 7 周三预注册 | 文档完成；未执行 | 01附录V4.1-6；新树正式交接/共享锁/匹配优先/普通任务0门禁 |
| 8 收尾 | 完成；本条所在提交，11个scope与R1绑定已回收 | 本文与05；源提交未推Gerrit |

本轮Quickbuild模式结论分项目，实际job项目UNKNOWN；独立归档摘要见04 §3。sandbox原样建分支已授权完成；本轮BOLT草案不推Gerrit。

### v4.1 停止点与证据强度

- 按本轮“规定之外的情况停止”规则停止产品实验：R1私有mount准备首次unshare propagation Invalid argument；第二次root self-bind/make-private失败Unknown error5005，观察到本任务绑定传播到宿主。已精确卸载自己的R1绑定；findmnt -R退出1/输出空、mountinfo无R1条目。E/stop-and-recovery.json直接证据；没有挂/proc/overlay或运行parser/linker/BOLT。停止后仅归档现有材料和写文档。
- 本轮59fixture PASS（轻4GiB），真实pipeline/宏/完整RPM未执行；本地LLVM草案b3ec4f03259e695bb2e6c64d7b61474380eaaa38，父cb679968，作者FatTank。完整format-patch静态apply与tree d2f7657e…相同；文本评审patch+profile公开封套也重建相同tree。文档与源提交身份不同，不混用。
- 全profile Source压缩9.735MB可进GitHub；完整patch12.58MB及xz10.13MB超10MB文件规范，留E，通过文本patch+Source+manifest完整交付，不拆片。Gerrit大小限制尚未验证；Source/BOLT commit未推，只建分支原始cb已推。
- 待恢复：安全R1输出/cache隔离；Source helper全pipeline夹具；真实spec debug条件/完整post展开；实际工具install manifest差集；普通final debug清单与无DWARF候选的严格例外边界。草案暂用两次post取参考，未认证，不允许发货。
- 旧树预演R、S/N、双flags对照、VMHWM、三目标/30对、standalone、90资产均UNKNOWN/未执行。没有因历史正例/fixture PASS把它们写成通过。共享flock未取未等；归档两锁/根与W tracked文件未动。

最终GitHub封存：04环境16030e7；草案/59fixtures/05/设计v4.1 b6b5624；压缩Source210f82b；本状态收尾提交可由git log追溯。v4.1正文44782B≤50KB，POSIX片段dash -n及本地链接检查通过；Python3.9语法兼容性静态检查通过。E/final-publication.json在本次push后登记本地/远端和raw文件核对。**任务按停止规则收尾，未完成全部产品验证步骤；不自动恢复实验。**

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

最终本地LLVM源草案a3c31d2c40809adbfacfd8cb6c12f3e87476a058，父cb67996861d070d68fec2b4c623eed7d20ba2e23，tree4ec0029fcb10baf632af6fc9e2bd58aad1eed224；作者FatTank；不是GitHub证据仓库提交。未向Gerrit推BOLT提交。sandbox仍仅此前原样创建基线，周五前没有standalone、没有完整LLVM构建。

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

## 2026-10-14 周三续跑五：删除第二次安装与文本门禁STOP

PM确认追加bolt后第二次完整安装创建两个未登记manifest的BOLT别名，Quickbuild会在prune失败。采用去掉第二次安装/exports备份恢复/prune，不增加特例；普通安装后baseline到BOLT pipeline结束重新取完整清单，逐项比较路径/类型/权限/大小/SHA/链接目标，有差异即停，候选install仍单独替换clang。前轮cache+361/+1674072B接受为交接缓存正常变动，后续临时配置专用cache；本轮无需配置。原树禁所有cmake/ninja/-P安装。文本比对现存build.ninja/rules.ninja、包含无输入CUSTOM，禁compdb。其余资源/保护/准备性最多一次修正/产品失败即停与sandbox资格规则不变。

草案编辑与103/103 fixtures PASS，旧95+新8，prune保留供历史夹具但生产不调用；snapshot/compare-root记录目录与链接权限，报错含路径。新源提交a1410e3d14b8836e3f9be5a1b4380f914dc2e705 父cb679968，spec SHA14d17a60369a2c05661037583740b410f0fd710aef2c0c78de08175a57bb6c0c、helper SHA7614228b5da020fd1ae08eaef0ebaf096c317f21a370e249285ee632711888e7，完整patch与公开封套静态apply/tree PASS。第一步后续读取审核依赖第二步，故在两模式展开前做文本比对；该严格产品门禁FAIL后立即停，第一步尚未完整认证，debug/release展开未执行，未拿旧展开顶替。17与fixtures/draft-change/manifest给证据，未推Gerrit。

第二步完整文本门禁FAIL，状态STOP_ORDINARY_BUILD_EDGE_CHANGE：7439个非equal文本块，允许BOLT构建9/规则1/聚合5/混合1；普通PDB元数据7421块（6255对象+583链接边）、CMake普通依赖移除2块不允许。88个普通compiler-check/benchmark依赖被删，同时新增20个BOLT依赖；不能只计新增忽略删除。普通clang对象TARGET_COMPILE_PDB/TARGET_PDB删除，链接TARGET_PDB bin/clang.pdb→clang.dbg；虽此前普通编译/链接命令相同且Linux规则不引用PDB变量，仍严格停止，不豁免。17/edge-compare/build.diff/rules.diff及全记录xz给分类、例子与完整原文。

第一步第4项后续读取资料审核列出own BOLT work资产、源目录clang Python、安装树普通动作及原debug find-debuginfo对DWARF引用build源/生成头的间接读取；86配置同字节只为部分证据，因全边FAIL及DWARF验证未跑，不认证完全不受影响。当前新草案两模式rpmspec展开未执行；第三步对象/双模式/预期清单/性能全NOT RUN，geom未知，sandbox未尝试/远端未查。源a1410e3d14b8836e3f9be5a1b4380f914dc2e705父cb679968，封套apply/tree PASS但不是合格推送提交。候选仍历史后备SHA4ec07159…，周四匹配统计同量级/双5%+性能，不核local/Quickbuild SHA一致。

保护审计PASS：原clang/22RPM/归档证据/源码/坏cache-ninja配置不变，原cache47987/96881772832B本轮零新增（前轮增长PM已接受）。本轮没有CMake/Ninja/link/新配置/chroot/proc/shared-lock，全部4GiB轻scope已回收，无准备性错误重试；严格失败后只读完善分类/封套/报告，不继续产品实验。W tracked仅原有gbs改动，不写W/llvm、不进入ARM树。原根free59147931648B，未有>10GiB写入。

## 2026-10-14 续跑六（历史）

甲类7421块/6838普通语句PASS，两个PDB变量在2454规则中0引用；当时乙类只限RERUN_CMAKE，配对phony输出块未获许可而STOP。完整人工裁决、88/20全文、保护与资源见18及GitHub dd7053a中的本STATUS；该历史停止被后续PM扩充许可覆盖，原始证据不删。

## 2026-10-15 续跑七（历史）

7439文本/当前a141两模式展开PASS，120输入SHA准备PASS；两次辅助脚本路径查询错误触发当时准备STOP，后续对象等未跑。完整人工裁决/路径错误/资源/保护见19及GitHub dd7053a中的本STATUS。续跑八PM已调整查找错误规则，此历史状态被后续执行覆盖，原证据保留。

## 2026-10-15 续跑八（历史完成）

120完整对象、双模式mini、22RPM/DWARF预期清单、x86性能geom0.855890085 PASS；sandbox已更新并核对a1410e3d父cb，历史后备候选4ec保持。完整进度/资源/保护/四类准备修正见20及GitHub 053fe704中的STATUS。原证据不删；该资格不代表续跑九门禁认证。

## 2026-10-15 续跑九（进行中）

PM裁决及本轮边界见21：修门禁不改生成参数/4ec候选，源父a141；仅push bolt-v4，禁止Gerrit。QB默认开关保持开启；回退需新spec提交改bcond_with，不能改QB配置。第一步离线闭包1911边（普通1792/command1715、新增phony9、实际BOLT110=102对象+7库+1链接），精确描述白名单及固定NINJA_STATUS，109/109夹具PASS。准备入口cwd修正一次，详见21；后续待。

续跑九STOP_PROCESS_TIMEOUT_FIXTURE_SECOND_ERROR：健壮性修改后的138夹具137通过1失败，进程后代退出观察修正一次后仍见R，按第二次错误立即停，不再试。安全属性/宏链开关OFF比对/ARM与AArch64性能/真实新门禁全部NOT RUN，不能生成合格源提交。候选4ec、普通clang、禁用cache/ninja未变；22RPM/归档/源码保护PASS、原cache47987/96881772832B；scope已回收，无重锁/proc/CMake/Ninja/ARM树/Gerrit动作。源HEAD仍a141，未完成修复及manifest单独保存；生产prune移除，rsp证据无@不改代码。35新增测试方法；准备/查找错误、初次109单测未纳入cgroup偏差详见21及review-corrections/resources。保持QB默认开启，回退需新spec提交改bcond_with，正式说明必须注明。

## 2026-10-15 续跑十（进行中）

PM：上轮为真实退出证明缺口，按SIGKILL/直接回收/扫描pgrp等待非Z-X成员清空（10s上限、列存活PID状态）修复；rsp无@关闭；110描述tool-plan已认证不重做；生成参数不改、4ec候选变化即停。原树禁cmake/ninja/-P，禁止任何Gerrit动作；资源/保护/准备修正规则继续。工作副本继续使用，源父a141。步骤1 140/140夹具PASS，比上轮138新增2项；真实shell/子/孙心跳停止、持续存活mock报PID及原错误/日志通过，4GiB scope已回收，无准备修正。安全属性等后续待，详细21。

续跑十步骤2 PASS：两真实ELF安全属性全部保持（均无GNU property），65241动态符号/版本、43需求相同；helper流水线strip-all后及post新增比较。6新安全夹具、全套146/146 PASS；旧post夹具placeholder改真实ELF一次准备修正，原文保留。原/候选SHA不变；原文/表/资源见21与reviewfinish-security-*。宏链及真实门禁待。

续跑十步骤3 PASS：当前canonical双模式小spec复用源override完整原文、同处install/files之后（历史20为路径适配，非原文相同，已澄清）；小spec只展开未重跑RPM。源条件块空白移入BOLT分支，OFF debug/release所有相关段与cb逐字节相同。rpmspec无--without，依rpmbuild实证的_without_clang_bolt字符串与已安装bcond宏作等价展开；选项兼容及宏值报告各准备修正一次，原文保留。累计三类各一次，具体21。

续跑十最终PASS_LOCAL_GATES_STOP_BEFORE_PUSH：真实tiny/security、20双模式根副本完整post/反向检查/compare-root、110计划正反例全PASS；146夹具。新源97c060a10bf0d19cea4b163853ceb873ed431478父a141，patch0002静态apply/整树PASS，spec/helper SHA见21与manifest；profile及4ec候选不变。没有Gerrit查询/推送，按授权停在推送前。三类准备修正各一次、两macro采集错误原因不同均保留；原22RPM/归档/源码/坏配置/cache审计PASS；所有4GiB scopes/proc回收，无重锁/CMake/Ninja/ARM/完整构建。

## 2026-10-15 续跑十一A：署名与sandbox

源仓库user.name/email均来自global /home/linhao/.gitconfig：liushanshan / ss0217.liu@samsung.com，未修改配置。单次-c amend/reset-author后，新源b7e61fb92b34795868230e4f9cee8e3ec65496f6，author/committer均FatTank <hao.lin@samsung.com>；父a1410e3d，tree ea70ea066dd16430b23c238d9654e1667479b960与97c060a相同，spec df1198d1…/helper4590b337…不变。文本补丁/manifest同步。sandbox查询前a1410e3d→无force快进推送→查询后b7e61fb92b34795868230e4f9cee8e3ec65496f6，确认成功；Gerrit仅提示subject>50字符警告，原文在manifest。未推评审/tizen_base，未做其他验证步骤。
