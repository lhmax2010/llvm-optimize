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
| 2 v4.1/补丁草案/fixtures | 草案封存；59fixture PASS、静态apply/整树PASS；宏/pipeline未认证 | 01 v4.1、05、tools/bolt、patches/bolt；LLVM本地b3ec4f0 |
| 3 旧树流水线预演 | 未执行；准备异常后依用户规则停止 | 无新重链/BOLT/三目标/30对数据；E/stop-and-recovery.json |
| 4 standalone配置/干跑 | 未执行（停止后不继续产品实验） | 仅LLVMConfig文件现存，兼容性/任务数UNKNOWN |
| 5 90对资产 | 未执行，0/90新文件 | 不是确认材料缺失；未将历史30对冒充90对 |
| 6 profile压缩 | 完成，解压SHA PASS | Source9735212B/SHA52fd8522…；uncompressed171232190B/SHA d9b132f9… |
| 7 周三预注册 | 文档完成；未执行 | 01附录V4.1-6；新树正式交接/共享锁/匹配优先/普通任务0门禁 |
| 8 收尾 | 临时R1绑定/所有scope已回收，正在封存推送 | 本文与05；源提交未推Gerrit |

本轮Quickbuild模式结论分项目，实际job项目UNKNOWN；独立归档摘要见04 §3。sandbox原样建分支已授权完成；本轮BOLT草案不推Gerrit。

### v4.1 停止点与证据强度

- 按本轮“规定之外的情况停止”规则停止产品实验：R1私有mount准备首次unshare propagation Invalid argument；第二次root self-bind/make-private失败Unknown error5005，观察到本任务绑定传播到宿主。已精确卸载自己的R1绑定；findmnt -R退出1/输出空、mountinfo无R1条目。E/stop-and-recovery.json直接证据；没有挂/proc/overlay或运行parser/linker/BOLT。停止后仅归档现有材料和写文档。
- 本轮59fixture PASS（轻4GiB），真实pipeline/宏/完整RPM未执行；本地LLVM草案b3ec4f03259e695bb2e6c64d7b61474380eaaa38，父cb679968，作者FatTank。完整format-patch静态apply与tree d2f7657e…相同；文本评审patch+profile公开封套也重建相同tree。文档与源提交身份不同，不混用。
- 全profile Source压缩9.735MB可进GitHub；完整patch12.58MB及xz10.13MB超10MB文件规范，留E，通过文本patch+Source+manifest完整交付，不拆片。Gerrit大小限制尚未验证；Source/BOLT commit未推，只建分支原始cb已推。
- 待恢复：安全R1输出/cache隔离；Source helper全pipeline夹具；真实spec debug条件/完整post展开；实际工具install manifest差集；普通final debug清单与无DWARF候选的严格例外边界。草案暂用两次post取参考，未认证，不允许发货。
- 旧树预演R、S/N、双flags对照、VMHWM、三目标/30对、standalone、90资产均UNKNOWN/未执行。没有因历史正例/fixture PASS把它们写成通过。共享flock未取未等；归档两锁/根与W tracked文件未动。
