# ThinLTO 缓存释放与双轮本地测量（2026-10-22）

**最终状态：两轮完整构建、299测试、五项Tizen RPM解析、全部BOLT实物门禁PASS；候选不变，22个二进制RPM清单一致；部分ar头时间戳不同，成员内容一致，未宣称RPM逐字节相同。源码提交仅保留在本地，未推Gerrit。最终结论见第13节。**

以下为2026-10-22停止快照，最终结果见第13节。 第一次未改 9e5675f 的构建停在普通 LLVM 链接；分段暂停后，等待内存准入达到 60 分钟上限。BOLT 实际增量尚未测得；释放后的整轮峰值及后处理降幅尚未测得；clang 与 RPM 一致性尚未验证。不得用历史 97 GB 缓存代替本次测量。

## 1. 源码与边界

本地源提交 `d20e873b2c7dfac10fab9235e2b781dad08dc4c7`，父 `67619ec8bbbac7238a6cfc33a481ccfbcd12206f`，在 `9e5675f57d122549997caffa39b655dfefc46fee` 上 amend。保留 Change-Id `Ic98eab90cc017f127a66e1729b44fab8b8e8fb41`；作者、提交者和 Signed-off-by 为 Hao Lin。不改全局配置、不访问 Gerrit。

源码仓库原为 detached HEAD，没有名为 bolt_pgo 的本地分支；沿用此前 detached amend 做法，不新建分支。这里的本地提交没有推送到远端 bolt_pgo。

spec 仅在 `echo BOLT_COMPARE_ROOT_PASS` 后新增以下三行，移除这三行后与 9e5675f 全文逐字节相同：

```spec
# No subsequent step consumes this ThinLTO cache.
# Release it only inside the enabled x86_64 BOLT block.
python3 -B %{SOURCE1201} cache-release "$PWD" "$BOLT_WORK"
```

普通构建、基线安装、Source1005、平台 post 链、四次 disk-report 均未改。源码全文 diff、完整 helper/spec、结构检查见本页证据目录。

## 2. helper 行为

新命令先调用 `replay_script` 验证 link.original 的完整格式及唯一绝对缓存路径规则；再要求 realpath 与 build/lto.cache 相同、路径为实际目录且不是软链接。否则输出 skipped 并返回 0。删除前 disk_entries 统计普通文件数和实际 allocated bytes（含目录）；rmtree 成功输出 removed、耗时，并原子保存 cache-release.json。部分删除失败输出 partial 和可读剩余文件数（统计失败时为 unknown）。记录文件写入失败仅报告 record-unavailable，不改变成功退出约定；参数用法错误由 argparse 返回 2。

disk-report / disk-diagnose 未修改：缓存缺失时 disk_entries 返回空集合，正增量为 0，净变化允许为负数。原因仍取自失败 errno/日志，缺失缓存本身不是磁盘失败。新增测试验证了释放后的非磁盘诊断和真正 ENOSPC 诊断。

## 3. 已完成认证

- 全部 299 测试 PASS：既有 289 + 新增 10。原始 stdout/stderr 已保存。
- 新增覆盖：正常删除、外部路径跳过、软链接跳过、目录缺失跳过、中途删除出错、重复缓存参数跳过、link.original 缺失、JSON 写满、参数错误、释放后报告与诊断。
- 新提交 gbs export PASS；Tizen rpm/rpm-build 4.14.1.1-1.7 五项解析全部 PASS，每项保留七个 Patch。
- profile 和 Source1005 与 9e5675f 字节相同。生产 helper 与测试镜像相同。

## 4. 构建条件与采样口径

固定 Base `20261013.024319`，仅 packages/debug 两仓库；build.conf SHA256 `e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945`。使用既有 `gbs_llvm_qb1202084.conf`，命令行 -B 指向本次新根，不改旧配置。

本地 GBS 2.1.0，与 QB NGBS 有差异。外层 --threads=30，三个宏为 `jobs 8`、`_smp_mflags -j8`、`_costomized_smp_mflags -j20`；固定 build.conf 和 spec 的 mlgo_build_jobs=6 保持。实际普通 Ninja 为 -j6，CMake link pool=2，宿主 nproc=20；QB记录为NGBS JOBS_N=12、WORKER_N=28，属于用户已允许的本地并行度差异。没有额外 shelve。GBS 包构建入口实际 argv 也存入日志。

仅在本次新根执行构建，历史根完全不动。首次 GBS 段在持锁 1884.592 秒后受控结束；后续控制器每持锁 3200 秒，先冻结整个构建 cgroup、确认 frozen，再释放锁，按原准入条件重新取锁后恢复。单次持锁小于 60 分钟；16 GiB / swap0 / nice15 / ionice3，开始 MemAvailable >=12 GiB，低于3 GiB停止。本地磁盘准入参考为历史219.931 GiB下界+15 GiB BOLT估计+20 GiB导出保留+30 GiB底线，非精确峰值，也不是发布代码门槛。采样目标每60秒，资源目标每5秒。实际 I/O 等待使部分 du 扫描超过60秒，必须按原始起止时间解释为离散采样，不能宣称连续峰值。另设独立资源监视器，避免 du 阻塞影响低内存停止检查。

同时记录外层 GBS 根与独立 chroot 根：普通用户外层 du 对 usr/share/upgrade、var/cache/ldconfig、root 有权限盲区，错误原样保留；补充以既有 sudo chroot 权限在本次新 chroot 内执行 du -sx -B1 /，完整根读数单独存档，不把盲区读数称为完整值。三个盲区初次各12,288字节。普通 sudo du 未授权，没有绕过或改权限。

修订 spec 的解析使用新基线根中的 RPM，专用 /home/abuild/cache-release-parse 仅存两份小 spec；不执行其安装或构建，不影响基线源码。此验证小目录包含两份小spec，约60KiB，计入采样；与产品构建输入分离。

## 5. 准备性修正

第一次启动遗漏 tar 模式的预导出，8.323秒即失败，未进入 %prep：

```text
/usr/bin/build: line 1215: cd: .../baseline-root/local/sources/tizen_base_toolchain_standard/llvm-22.1.8-1: No such file or directory
llvm.spec is empty.  This should not happen...
```

补齐 gbs export 并明确 --spec llvm.spec，第二次启动成功进入 %prep/%build。该准备类修正一次；原始失败日志保留。只读定位 RPM 临时脚本时按实际日志确认目录为 /var/tmp，采集器补入该目录，不修改任何产品输入。du 权限盲区按第4节另列完整 chroot 读数。只读查找时曾因rg排除模式未正确排除新根/proc而遇到权限错误，后改用限定深度的find；未执行错误的产品输入。续跑前的路径查找更正及本地监视器修正不改产品参数。

## 6. 2026-10-22停止快照（后续已完成，见第13节）

| 项目 | 结果 |
|---|---|
| cache-release 实现、精确 spec 改动范围 | PASS |
| 全部本地测试 | 299/299 PASS，新增10 |
| 新提交 gbs export / Tizen RPM 五项解析 | PASS / 5/5 PASS |
| 第一轮 9e5675f 完整构建 | 未完成：普通 LLVM 链接阶段暂停后，内存准入等待超时 |
| 第一轮 BOLT 四次报告、candidate、identity、RPM | 未产生；不是零占用 |
| 第二轮完整构建 | NOT RUN；仅准备了源码导出 |
| 构建白名单、compare-root、post 实物门禁 | NOT RUN，本次未到这些阶段 |
| 两轮 candidate SHA / RPM 文件清单及文件 SHA 比较 | NOT RUN，无完整第一轮产物 |
| cache-release 的真实构建 removed 原文 | 无，本次只有夹具执行，不能冒充真实构建证据 |
| 整轮峰值及后处理占用降幅 | 未知，不能推算成已测结果 |

### 6.1 执行与停止经过

第一次有效 GBS 段：完整日志 `baseline-segment2/rpm-build.log.gz` 第448行 `[368s] Executing(%prep)`，第506行 `[393s] Executing(%build)`。完成4102/7634项后，为处理单次持锁时限受控停止；最后第7313行 `[1879s] Terminated` 是本地控制器停止，不是产品错误。该段持锁1884.592秒。

之后用捕获的原 RPM argv 和环境，以完整 `rpmbuild -ba --noprep` 续跑（不使用 short-circuit）。重新配置后的计划3534项为剩余任务加两项TF刷新。续跑环境中捕获的 PATH、CFLAGS、CXXFLAGS、LDFLAGS 等与第一次 Ninja 逐项相同，见 `baseline-resume1/environment-compare.json`；这不代表对未采集环境变量作了证明。续跑方式与一次不中断的 GBS/NGBS 有差异，必须保留该限制。

续跑日志第5274行是最后一个完成任务：

```text
[ 980.375s] [3275/3534] Linking CXX static library lib64/libclangdRemoteIndex.a
```

当时仍在链接 `lib64/liblldb.so.22.1.8` 和 `bin/bugpoint`。只读线程观察发现两路LLD各有线程在 `folio_wait_bit_common` 等待，cgroup I/O pressure高；不能据此断言死锁。另观察到本机其他会话的工作负载；df变化不能全部归于本次构建，其他工作负载未被干预。

2026-10-22 22:23:03 CST，确认整个构建cgroup为frozen后释放共享锁，该段持锁3203.387秒。冻结保留约14.1GiB链接现场内存。随后60次准入采样的 MemAvailable 为8,120,979,456–10,618,048,512B（约7.56–9.89GiB），均低于12GiB；等待期限3600秒，到23:23按规则停止。冻结保留内存也是未能再次准入的因素，不能将原因全部归于其他任务。

控制器原始终止信息见 `baseline-resume1/controller-terminal.json`：

```text
RuntimeError: memory admission timeout
```

运行期间为后续轮次完善过本地控制器/看护脚本；Python traceback回读磁盘上的新源行，导致其中一处显示行号与当时执行版本偏移。保留原文，不把那一行误读为冻结失败：leases记录明确显示freeze rc0、FreezerState=frozen、release成功；最终异常是memory admission timeout。生产helper/spec未因此变化。

23:23:10停止命令返回0，随后确认构建、看护、du、脚本采集服务均inactive，两个LLD已退出。只卸载本次新根的两层proc、两层devpts和一个dev/shm，五次均rc0，mountinfo无残留。共享锁早在22:23释放；未重新取锁。两轮新目录、源码导出和第一轮对象全部保留，没有删除历史目录或本次构建根；没有访问Gerrit或QB。

### 6.2 已取得的局部采样（不是整轮峰值）

| 范围 | 最高已记录值 | 限制 |
|---|---:|---|
| 完整chroot根 | 29,401,939,968B，27.383GiB | 仅到普通链接/暂停阶段；不是完整构建峰值 |
| 外层GBS根（含导出等） | 28,946,673,664B，26.959GiB | 有三处权限盲区；采样较早，不能与上行同时间比较 |
| BUILD | 24,349,007,872B，22.677GiB | 部分普通构建；父子目录不可相加 |
| LLVM build/ | 22,379,102,208B，20.842GiB | 包含当时的ThinLTO缓存 |
| lto.cache | 7,209,250,816B，6.714GiB | 普通构建产生；不是BOLT新增占用 |
| BOLT工具、工作目录、静态库转换、candidate | 未到达 | 不得填为完整阶段的零占用 |
| BUILDROOT / RPMS / SRPMS | 只有预建空目录 | 无产品文件，见final-state.json |

完整chroot读数共72次（首段23、续跑49）；最长单次du耗时1008.268秒，因此“每60秒”只达到了调度目标，未实现稳定采样间隔。原始记录包含时间、扫描耗时、stdout/stderr/rc；部分跨越暂停时刻，不能将扫描起始时刻视为所有文件的精确同时读数。外层采样线程被du阻塞的问题，已通过独立5秒资源看护解决；原始采样空档仍保留，未补造数据。

首个有效段cgroup峰值7,428,624,384B；续跑峰值17,179,869,184B（16GiB），memory.events的oom和oom_kill均0，max计数13142不能当作OOM次数。最大观察到的单进程VmHWM为13,728,436KiB；它是采样观察值。参数、资源、暂停/准入、线程及I/O原文分别在各段JSON/JSONL中。

## 7. 当时继续工作的条件与边界

第一轮尚未完成，不能删除其根来腾空间。新根位于 `W/temp/bolt-v4-20261022-cache-release/baseline-root`，下一次续跑需重新满足本地资源准入；本轮到等待上限后已停止，没有通过重启来重置等待期限。第二轮仍须相同固定快照/宏条件，先保全第一轮所有RPM、candidate、identity与四次报告，再执行修订轮并逐文件比较。源码修改不能视为已经完成两轮实物认证。

## 8. 首次停止时的原始证据

目录：[`tools/bolt/results/cache-release-20261022/`](../../tools/bolt/results/cache-release-20261022/)。源码、测试、解析为已完成材料；构建运行及停止记录已保存；见partial-measurement.json、timeline.tsv、各段完整压缩日志与JSONL。没有删除历史目录或任何真实构建缓存。

原始RPM生成脚本保留4处行末空白，原始iostat保留EOF空行；git diff --check对此给出提示，未改写原文以消除提示。排除这两份原始证据后的文档/脚本差异检查通过；110份归档证据SHA复核通过，详见delivery-checks.json。

## 9. 2026-10-23 内存释放后的续跑历史

用户明确要求继续后，01:01:51 CST重新取得共享锁。准入 MemAvailable=28,059,787,264B，/home可用427,441,000,448B；复核本次新根的四项SOURCES和固定build.conf身份未变。以原RPM入口继续完整 `rpmbuild -ba --noprep`，未触碰历史根。新计划356项；普通bugpoint、libLTO和liblldb先后完成，128/356后仍在同时链接普通clang-22与libclang-cpp.so.22.1，尚未进入BOLT。

16GiB限额下两路LLD几乎用满匿名内存，memory.events的max计数增加、I/O压力高，但oom/oom_kill均0。2026-10-23 01:45:30 CST，用户明确批准“允许本次两轮使用20GiB”，随即用systemctl set-property --runtime把本次构建MemoryMax调到21,474,836,480B；swap=0、nice15、ionice3、低于3GiB停止和锁时限不变。第二轮本地控制器使用同样20GiB上限。此裁决只适用于本次两轮本地测量，不改spec、helper或构建参数；第一轮调整前后分段记录，不能称为从头到尾统一资源条件。原始前后值与命令见baseline-resume2/memory-limit-adjustment.json。

新增独立5秒进程采样，避免du阻塞时漏采VmHWM；du存在临时文件扫描竞态的读数标注rc1，不能称为完整精确值。未取得第一轮完整产物前不启动第二轮、不删除第一轮根。

后续裁决（2026-10-23）：用户先批准“仅冻结续跑使用3GiB准入”，01:57:59已重新取锁、恢复同一现场；第一次持锁3200.515秒，冻结/释放均成功。随后用户明确要求“解除内存限制，所以目前不考虑准入内存和冻结内存，你跑你的”，01:59:18已将MemoryMax设为infinity；第二轮本地入口取消内存上限和准入等待。原始命令/返回值见memory-unlimited.json，控制器交接见controller-handoff.json。源码和构建参数不变；锁与磁盘规则继续执行。原运行采样器仍包含运行中<3GiB的紧急停止检查（并非启动准入，未在本次续跑触发），没有为热替换采样器而重启LLVM链接。

02:03左右普通libclang-cpp链接完成，进度恢复到138/356；该时点cgroup峰值26,155,147,264B（约24.4GiB），oom/oom_kill仍0。普通clang仍在链接，尚不能填写BOLT实测增量。

### 9.1 普通构建与 BOLT 工具完成（03:49 进行中快照）

本次续跑日志第2351行 `[8487.851s] [356/356] Linking CXX executable bin/opt`，第2353行 `[8488.817s] Executing(%install): /bin/sh -e ...`。普通安装完成后，begin报告时间为03:35:08，完整根采样226,526,859,264B（210.97GiB），BUILDROOT约49.03GiB。安装快照、preflight/certified和proc检查通过。

实际tool-plan为113项：111个BOLT任务（102对象、7静态库、1可执行文件、1生成文件）和2个TF刷新；ninja_diagnostics为空。实际-j1构建113/113，打印BOLT_NINJA_EXIT_0；tool-verify确认本次生成llvm-bolt且TF归档SHA保持。tool-built报告used_bytes=4,039,049,216（3.762GiB），其中cache正增量1,202,872,320B（1.120GiB）。这只是工具完成时点，不是完整BOLT峰值。当前进入reference重链，candidate、后处理和RPM尚未产生，第二轮未开始。

03:41:43续租前冻结全组，持锁3200.228秒后释放；约1秒后重新取得并恢复，minimum=null，没有内存准入等待。后续新轮次的本地采样器也移除低内存停止条件；锁时限和本地30GiB磁盘底线保留。已运行的第一轮Python采样器未热替换，原有运行中3GiB检查尚在，未触发。

全根du采样器曾因ThinLTO临时文件恰好消失而rc1退出，约01:17至02:08存在完整根采样缺口；原始记录保留。修正后的du-root2仅对全部报错均为“No such file or directory”的扫描竞态继续采样，其他错误仍停止采样器；每条rc/stderr保留。常规分项du和资源记录继续，但不能补造缺失的完整根读数。此前把过期读数误称为仍在扫描，发现服务inactive后已更正。详见du-sampler-correction.json。查找证据索引时误在任务临时目录执行rg，随后在B定位，未影响产品输入。

本节材料为进行中快照，不能视为整轮认证；下一次归档将保留完整后续日志。

## 10. 第一轮完整结果与保全（2026-10-23 05:21）

第一轮rpmbuild退出0，当前续跑段15095.144秒；这不是整轮从零开始的时间，之前的编译段、内存暂停和环境差异仍见第6、9节。所有真实门禁通过：113项工具计划与执行、TF归档身份、重链/BOLT/strip、安全属性、两次pipeline tiny、compare-root、候选原子安装、平台链后的post tiny/SHA/别名检查。最终产生22个二进制RPM和1个源码RPM。

候选SHA `4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9`，与历史候选逐字节相同。当前普通clang SHA为`06c940726269210ce3655e17366820a080bfe236a3adc24622958e6a6709e309`，并非历史7df0ff90；基线已有此差异，不能归因于尚未运行的cache-release。新固定快照/构建续跑与历史条件不同，未对普通二进制差异做进一步逐节归因。新树llvm-bolt SHA为`0ecdff6172f7fffb08d30f3865976ca15dc8708c3a1ef9fe0d2a543059996f75`。匹配N=23592、M=144032、S=0、U=1、Q=383，R=0.0042385%，S/N=0，双门禁PASS。

| 阶段 | 本次续跑日志秒数 |
|---|---:|
| 普通构建最后任务 | 8487.851 |
| %install开始 | 8488.817 |
| BOLT begin报告 | 9196.848 |
| tool-built报告 | 9862.925 |
| pipeline PASS / 报告 | 10141.488 / 10142.119 |
| compare-root PASS | 10492.440 |
| Source1005开始 / 结束PASS225 | 10497.070 / 12565.334 |
| candidate install调用 | 12565.440 |
| find-debuginfo开始 | 12569.154 |
| BOLT_POST_GATE_PASS | 14025.646 |
| RPM文件处理开始 | 14028.334 |
| 源码RPM写出 | 14306.899 |
| 最后一个二进制RPM写出 | 15094.470 |
| %clean结束 / rpmbuild成功返回 | 15095.106 / 15095.144 |

| BOLT报告 | BOLT自有allocated bytes | GiB | ThinLTO正增量B |
|---|---:|---:|---:|
| begin | 0 | 0 | 0（基线记录） |
| tool-built | 4,039,049,216 | 3.762 | 1,202,872,320 |
| pipeline | 4,665,483,264 | 4.345 | 1,202,872,320 |
| post | 4,667,088,896 | 4.346 | 1,202,872,320 |

完整chroot的**已观测峰值241,288,712,192B=224.718GiB**，在静态库转换归档安装阶段；外层GBS根最高242,613,411,840B有权限盲区，单独保留，不与chroot混用。BOLT重链期间观测到234,118,369,280B，较BOLT开始附近的226,526,859,264B多约7.070GiB；这是瞬时中间文件及缓存增量的采样，不等于四次disk-report时点值，也不能称为ON/OFF整轮净峰值差。基线静态库转换临时目录最高采样7,443,349,504B，结束后按原Source1005清理。没有重跑BOLT-OFF构建。

本次续跑cgroup峰值30,516,629,504B，oom/oom_kill均0；最大观察到的单进程VmHWM为18,219,596KiB（ld.lld）。首轮经历16GiB、20GiB和无限额三个时期；第二轮仅用无限额，时间不能直接归因于源码变化。后处理有普通工具/调试文件缺少build-id的warning，平台链和打包仍成功；原文全部保留。

采样限制：本次续跑的完整根du共166条成功读数；后处理一次扫描571.357秒，早期还有已记录缺口，故只报告已观测峰值。新增filesystem-independent.jsonl独立记录整个/home文件系统剩余量和本地磁盘保护；它包含其他进程影响，不能替代根du。没有把采样缺口补造为每60秒数据。

### 10.1 保全、空间回收与挂载状态

保全脚本复制并对源/目的逐文件核对SHA：28,009个文件，11,963,421,755B，含全部23个RPM、candidate、ordinary、llvm-bolt、identity、四次报告、工作日志、CMake/Ninja元数据及Source1005文本证据。保全持锁196.395秒、退出0；详见baseline-products/preserved.json和baseline-preserve。后续RPM逐文件比较将读取保全的RPM，不依赖清理后的构建缓存。

构建结束后全部监视服务自行退出、systemd已回收；清理代码首次将not-found的stop返回误判为错误，修正一次为读取LoadState/ActiveState确认inactive。旧SIGSTOP控制器只在真实构建服务inactive后SIGKILL回收，其工具会话返回137/Killed是本地控制器清理，不是rpmbuild失败。

/dev/shm和/dev/pts正常卸载；/proc正常umount返回32，原文`umount: /proc: target is busy.`。lsof/fuser证明是用户VS Code PID4237持有proc目录和proc/2558句柄。没有强制/懒卸载、没有结束编辑器。已请求用户释放句柄；这只影响挂载清理，不必阻塞第二轮。

用户已授权保全后清理本次第一轮新根。采取更小范围：仅删除该新根`build/lto.cache`，其余树、RPM与被占用的/proc全部保留。删除前核对保全成功、23RPM、关键报告、realpath/非软链、/dev/sda1、无缓存句柄及缓存下无挂载；普通用户执行`rm -rf --one-file-system -- <本次baseline-root内的build/lto.cache>`，rc0，无残留。这是**第一轮测量结束后的本地腾空间**，不是新helper在生产流水线中的验证。原始命令、文件数、du、df与释放量见baseline-space-recovery/cleanup.json；清理后/home可用354,500,767,744B（约330.15GiB）。未删除任何历史目录。

第二轮将在独立revised-root用原固定快照/宏及d20e873b开始；不设本地内存上限/准入/低内存冻结条件，保留swap0、低优先级、共享锁时限及本地磁盘规则。源码/发布代码没有资源门槛变化。完整双轮峰值降幅与RPM逐文件一致性仍待第二轮，不能把第一轮成功代替它。

## 11. 第二轮普通构建完成（2026-10-23 07:38进行中）

使用同一固定快照/build.conf/三个宏，以d20e873b在本任务独立revised-root从零运行GBS；四个SOURCES逐文件SHA与修订导出一致，见revised-run/input-identities.json。05:24:56启动；原生日志第10848行 `[7967s] [7634/7634] Linking CXX executable bin/opt`，第10850行 `[7968s] Executing(%install): /bin/sh -e ...`。GBS自身控制台日志较少，直接逐字节跟随根内.build.log保存为rpm-build.log，阶段观察时间另存rpm-phase-observed.jsonl。

第二轮从开始即MemoryMax=infinity、swap0，不设内存准入或运行中低内存停止；nice15/idle IO和共享锁规则不变。前两段持锁3201.526、3200.788秒，均先确认冻结后释放，约一秒后重新取锁并恢复；没有重启构建。与首轮分段恢复及16→20GiB→无上限的资源历史不同，不能把两轮耗时差全部归因于缓存释放。

完整根目前最高采样173872345088B（161.93GiB），已开始普通安装；不是整轮峰值。ThinLTO临时文件消失导致的du rc1逐条保留，最终完整峰值只采用rc0记录。尚未运行cache-release、未生成第二轮candidate/RPM。只读定位脚本时一次rg搜索误遍历新根的proc并报权限错误；没有产品操作或输入变化，随后改为限定深度的查找，见lookup-note.json。

本次中间归档一次使用相对脚本路径，systemd-run工作目录为/home/linhao而非调用目录，启动即rc2；改为绝对路径后归档成功。未影响产品构建，原文见archive-launch-correction.json。

## 12. 第二轮BOLT门禁与真实缓存释放（08:15进行中）

工具计划和实际执行均113项（111BOLT+2TF），ninja_diagnostics为空；BOLT_NINJA_EXIT_0与tool-build-verification通过。llvm-bolt SHA为0ecdff6172f7fffb08d30f3865976ca15dc8708c3a1ef9fe0d2a543059996f75，与首轮一致。TF归档前后均f15c565d30a981c22c71cbcf823030302cf51d19a381f4cc82e44626688be1ed。

流水线全部PASS，ordinary、重链输入、BOLT输出和strip-all候选四项SHA均与首轮相同，最终候选为4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9。N/M/S/U/Q=23592/144032/0/1/383，R=0.0042385%、S/N=0；安全属性与三目标微型门禁PASS。pipeline报告BOLT自有allocated bytes为4,665,487,360B，tool-built为4,039,049,216B。

compare-root PASS之后，日志第23650行原文：

```text
[10113s] BOLT_CACHE_RELEASE removed path=/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache files=47717 allocated_bytes=98180882432 seconds=29.205012623002403
```

cache-release.json状态removed。释放约91.438GiB，随后完整根采样132,480,196,608B（123.382GiB）；此时Source1005刚开始，不能把前后单点差直接称为最终峰值降幅。第二轮截至此时完整根最高采样231,374,397,440B，发生在pipeline期间；待整轮结束再判定整轮峰值、阶段降幅和RPM差异。第三段持锁3200.754秒后正常冻结/释放/恢复；未因内存等待。

只读进度显示脚本修正了重复拼接-root导致未显示Source1005计数的问题；不涉及产品输入或采样。tool-verify.json只读查找未命中后按目录清单定位tool-build-verification.json；原始说明在monitor-corrections.json。

### 12.1 首轮续跑残留的占用混杂因素

只读对比两轮build树文件大小（排除缓存/BOLT工作区/转换工作区）发现首轮独有两个普通链接临时文件：bin/bugpoint.tmpb222052和lib64/liblldb.so.22.1.8.tmpe4ea0a7，mtime均在此前被中断的首轮链接阶段。逻辑大小合计2,657,653,320B，实际allocated bytes合计2,216,964,096B（约2.065GiB）。保留原件不删除，最终实测峰值差须单列这一混杂因素，不可全部归因于cache-release。原文在build-size-differences.json与baseline-linker-temporary-residue.json。

CMakeCache只读diff另存cmake-cache-comparison.diff：首轮恢复配置留下C/CXX编译器相对名与UNINITIALIZED类型，第二轮首次配置记录/bin绝对名及STRING；AR/RANLIB路径相同，仅缓存类型/注释不同。两轮实际ordinary/relink/tool/candidate SHA均一致，但仍保留该配置历史差异，不宣称缓存文件逐字节相同。

## 13. 双轮最终结果（2026-10-23）

两轮完整构建均成功，第二轮GBS退出0，耗时15112.151秒；22个二进制RPM和1个源码RPM均已保全。首轮最终续跑段15095.144秒仅代表该续跑段，不能与第二轮从零GBS总耗时直接比较。没有向Gerrit推送，也没有操作QB。

### 13.1 磁盘结论与口径

BOLT四个固定报告时点的自有占用，首轮为0 / 3.762 / 4.345 / 4.346GiB；第二轮为0 / 3.762 / 4.345 / 3.226GiB。第二轮post数值较低，是正缓存增量随整个缓存删除后归零，并不代表工具或候选被额外清理。未运行BOLT-OFF第三轮，因此这些数值是BOLT自有路径与缓存正增量的实测，不能当作ON/OFF完整构建的因果峰值差。

BOLT开始后、compare-root之前的整根瞬时增量观测值为首轮7.070GiB、第二轮6.578GiB。它与固定报告时点不同，受采样对齐影响；不把分别采样的父子目录峰值相加。

整轮完整chroot观测峰值 **224.718 → 215.484GiB**，实测差 **9.233GiB**。首轮峰值在静态库转换产物安装阶段，第二轮峰值提前到缓存释放之前的BOLT pipeline。首轮另有2.065GiB中断链接残留；扣除这个已知因素后的峰值改善**估算**为7.169GiB。不是第三轮受控实测，仍有续跑历史和采样差异。

真实cache-release删除47,717个文件、98,180,882,432B（91.438GiB），耗时29.205秒。因此不能说“整轮峰值下降91GiB”：释放前的高占用仍然发生，主要收益在随后的转换、后处理和打包。

| 阶段完整扫描的最高读数 | 首轮GiB | 第二轮GiB | 首轮减第二轮GiB |
|---|---:|---:|---:|
| 普通构建（首轮为最后续跑段） | 161.026 | 154.395 | 6.630 |
| 普通安装 | 205.561 | 206.161 | -0.600 |
| BOLT开始至compare-root | 218.040 | 215.484 | 2.556 |
| compare-root后至find-debuginfo（含转换/安装） | 224.718 | 131.250 | 93.468 |
| 平台后处理至post报告 | 217.610 | 127.134 | 90.476 |
| RPM文件处理/打包 | 219.843 | 126.529 | 93.314 |

上表只纳入扫描起止均在对应阶段内的完整读数，跨阶段扫描不强行归类。平台后处理阶段观测最高值下降90.476GiB；post报告之后的首个完整根读数为211.826 → 118.326GiB，下降93.500GiB。扣除已知首轮残留后，post结束时降幅**估算**91.435GiB，与实际缓存释放量接近。各采样时刻和扫描时长保留，不用全盘df差替代本构建根占用。

四次报告的原始字节数：

| 阶段 | 首轮BOLT自有B | 第二轮BOLT自有B | 第二轮cache正增量B |
|---|---:|---:|---:|
| begin | 0 | 0 | 0 |
| tool-built | 4,039,049,216 | 4,039,049,216 | 1,202,868,224 |
| pipeline | 4,665,483,264 | 4,665,487,360 | 1,202,868,224 |
| post | 4,667,088,896 | 3,464,232,960 | 0 |

### 13.2 产物与门禁

完整RPM字节一致性不成立：时间元数据差异保留并按用户要求逐项归因，未放宽helper的任何产品门禁。两轮ordinary-clang-22、重链输入、llvm-bolt、BOLT输出、strip-all候选SHA一致；候选为 `4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9`，也与历史4ec07159一致。两轮均在各自新树构建llvm-bolt，非历史工具后备。工具计划与执行113/113、TF归档前后身份、匹配双门禁、安全属性、pipeline tiny、compare-root、原子安装和post tiny/SHA/别名全部PASS。

225个Source1005转换归档的输入/输出SHA、大小、成员和转换统计全部相同，第二轮225个安装完成并最终PASS；缓存删除后未重建。平台后处理原样执行一次，post尾检最后通过。

22个二进制RPM的文件清单、类型/模式、uid/gid、大小、链接目标和nlink逐包相同；mtime单列。部分静态归档完整SHA不同，下表如实列出；这些归档逐成员比较仅ar头时间字段不同，归档成员内容和其余字节均相同。没有改写保全的RPM或其载荷来抹平差异。RPM容器本身并非字节相同，构建时间等头字段和文件mtime另有原文记录。

| 二进制RPM | 载荷条目数 | 内容/类型/权限/链接比对 | mtime变化条目数 |
|---|---:|---|---:|
| clang-22.1.8-1.x86_64.rpm | 364 | 载荷文件SHA相同 | 65 |
| clang-debuginfo-22.1.8-1.x86_64.rpm | 27 | 载荷文件SHA相同 | 27 |
| clang-devel-22.1.8-1.x86_64.rpm | 1464 | 载荷文件SHA相同 | 237 |
| clang-devel-debuginfo-22.1.8-1.x86_64.rpm | 4 | 载荷文件SHA相同 | 4 |
| compiler-rt-22.1.8-1.x86_64.rpm | 400 | 45个ar时间头差异 | 105 |
| compiler-rt-debuginfo-22.1.8-1.x86_64.rpm | 17 | 载荷文件SHA相同 | 17 |
| libllvm-22.1.8-1.x86_64.rpm | 3 | 载荷文件SHA相同 | 3 |
| libllvm-debuginfo-22.1.8-1.x86_64.rpm | 4 | 载荷文件SHA相同 | 4 |
| libomp-22.1.8-1.x86_64.rpm | 3 | 载荷文件SHA相同 | 3 |
| libomp-debuginfo-22.1.8-1.x86_64.rpm | 6 | 载荷文件SHA相同 | 6 |
| libomp-devel-22.1.8-1.x86_64.rpm | 2 | 1个ar时间头差异 | 1 |
| lldb-22.1.8-1.x86_64.rpm | 8 | 载荷文件SHA相同 | 8 |
| lldb-debuginfo-22.1.8-1.x86_64.rpm | 16 | 载荷文件SHA相同 | 16 |
| lldb-devel-22.1.8-1.x86_64.rpm | 617 | 载荷文件SHA相同 | 34 |
| lldb-devel-debuginfo-22.1.8-1.x86_64.rpm | 7 | 载荷文件SHA相同 | 7 |
| llvm-22.1.8-1.x86_64.rpm | 105 | 载荷文件SHA相同 | 98 |
| llvm-debuginfo-22.1.8-1.x86_64.rpm | 85 | 载荷文件SHA相同 | 85 |
| llvm-debugsource-22.1.8-1.x86_64.rpm | 12126 | 载荷文件SHA相同 | 1292 |
| llvm-devel-22.1.8-1.x86_64.rpm | 2526 | 载荷文件SHA相同 | 204 |
| llvm-devel-debuginfo-22.1.8-1.x86_64.rpm | 11 | 载荷文件SHA相同 | 11 |
| llvm-static-devel-22.1.8-1.x86_64.rpm | 225 | 225个ar时间头差异 | 225 |
| python-clang-22.1.8-1.x86_64.rpm | 3 | 载荷文件SHA相同 | 0 |

共有271个归档完整SHA不同；逐成员原始差异及仅归一ar头时间戳后的SHA见archive-differences.json。两轮平台脚本都调用brp-strip-static-archive /bin/strip，脚本原文执行strip -g。归档时间字段分别落在04:54:59–04:55:24与09:16:02–09:16:36（CST），与各自后处理时刻对应；判断为平台归档时间元数据差异，不是cache-release改变成员代码。


源码RPM按预期与二进制载荷分开：

| 变化路径 | 变化字段 |
|---|---|
| clang-bolt-helper.py | sha256, size |
| llvm.spec | sha256, size |

源码包仅helper和spec两个文件的内容/大小不同。helper与各自源码完全匹配；导出spec的差异精确为三行cache-release改动及GBS自动生成的VCS提交号。源码tar、profile、Source1005、七个补丁及其他源码载荷均相同（文件mtime另列）。具体SHA见source-differences.json，不把源码包预期更新称作二进制包回归。

源码仍为d20e873b2c7dfac10fab9235e2b781dad08dc4c7，父67619ec8bbbac7238a6cfc33a481ccfbcd12206f，作者/提交者/Signed-off-by均Hao Lin。spec SHA为64bff4b4f6a9587a28ba2b2663ce05b61a4c391bb59d9120beb2845cce488f1f，helper SHA为516bf4189415bed604eac2e74049ab2b148690c79b3fea4e420e3617527630f5。299测试与gbs export后的五项Tizen RPM解析认证沿用同一未改源码提交的已通过结果；构建期间没有再改生产文件。

### 13.3 资源、采样限制和保留状态

第二轮cgroup峰值30,096,756,736B，最大观察到单进程VmHWM为16,752,968KiB（ld.lld）；oom/oom_kill均0。首轮cgroup峰值30,516,629,504B、最大观察VmHWM 18,219,596KiB，且有16→20GiB→无上限与中断续跑历史，耗时不能作纯优化因果比较。第二轮每段持锁秒数为3201.526, 3200.788, 3200.754, 3214.213, 2292.384，均小于3600秒，冻结仅为释放/重新取得共享锁，不做内存准入或低内存等待。

第二轮完整根du有212个成功样本、23个临时文件竞态不完整样本，最长扫描769.497秒。每60秒为调度目标，I/O等待期间未能保持60秒完成一次；没有补造缺失读数。首轮早期空档和后处理长扫描见第9、10节。整轮峰值均为观测值而非连续上界。

两轮各23个RPM、candidate、ordinary、llvm-bolt、identity和四份报告均保全并逐文件SHA核对；第二轮保全28,010文件、11,963,443,118B。只删除过用户授权的本次首轮新根cache以腾第二轮空间，第二轮cache由产品新增命令在compare-root后删除；历史树未动。第二轮挂载已清理，所有第二轮构建/监视服务inactive。首轮proc仍被VS Code PID4237的FD48/49持有，保留挂载与其余首轮树，未强制卸载、未终止编辑器；相关原文另存。只读证据查找和显示修正见monitor-corrections.json；源码RPM归因脚本首次遗漏GBS生成VCS行，补上该项后仅剩预期差异，未更换产品输入或修改产物。

### 13.4 钉提交原始证据

- [双轮测量比较与公式](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/f4a39a5dc70f66f9e8ba0559d418af5dbe472a68/tools/bolt/results/cache-release-20261022/measurement-comparison.json)
- [第二轮完整结果与资源](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/f4a39a5dc70f66f9e8ba0559d418af5dbe472a68/tools/bolt/results/cache-release-20261022/revised-run/completed-revised-summary.json)
- [两轮候选/ordinary/工具SHA](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/f4a39a5dc70f66f9e8ba0559d418af5dbe472a68/tools/bolt/results/cache-release-20261022/rpm-validation/binary-identities.json)
- [逐包逐路径RPM差异](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/f4a39a5dc70f66f9e8ba0559d418af5dbe472a68/tools/bolt/results/cache-release-20261022/rpm-comparison.json)
- [归档成员与时间头差异](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/f4a39a5dc70f66f9e8ba0559d418af5dbe472a68/tools/bolt/results/cache-release-20261022/rpm-difference-analysis/archive-differences.json)
- [源码RPM差异归因](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/f4a39a5dc70f66f9e8ba0559d418af5dbe472a68/tools/bolt/results/cache-release-20261022/rpm-difference-analysis/source-differences.json)
- [RPM比较完整结果](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/f4a39a5dc70f66f9e8ba0559d418af5dbe472a68/tools/bolt/results/cache-release-20261022/rpm-validation/product-comparison-summary.json)
- [首轮RPM头字段](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/f4a39a5dc70f66f9e8ba0559d418af5dbe472a68/tools/bolt/results/cache-release-20261022/rpm-validation/baseline-rpm-headers.json)
- [第二轮RPM头字段](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/f4a39a5dc70f66f9e8ba0559d418af5dbe472a68/tools/bolt/results/cache-release-20261022/rpm-validation/revised-rpm-headers.json)
- [225归档转换比较](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/f4a39a5dc70f66f9e8ba0559d418af5dbe472a68/tools/bolt/results/cache-release-20261022/revised-run/archive-conversion-comparison.json)
- [真实缓存释放](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/f4a39a5dc70f66f9e8ba0559d418af5dbe472a68/tools/bolt/results/cache-release-20261022/revised-evidence/bolt-work/cache-release.json)
- [post尾检](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/f4a39a5dc70f66f9e8ba0559d418af5dbe472a68/tools/bolt/results/cache-release-20261022/revised-evidence/bolt-work/post-gate/post-result.json)
- [带行号时间线](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/f4a39a5dc70f66f9e8ba0559d418af5dbe472a68/tools/bolt/results/cache-release-20261022/timeline-final.tsv)
- [第二轮完整日志](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/f4a39a5dc70f66f9e8ba0559d418af5dbe472a68/tools/bolt/results/cache-release-20261022/revised-run/rpm-build.log.gz)
- [第二轮完整根du](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/f4a39a5dc70f66f9e8ba0559d418af5dbe472a68/tools/bolt/results/cache-release-20261022/revised-run/du-root-complete.jsonl)
- [证据SHA索引](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/f4a39a5dc70f66f9e8ba0559d418af5dbe472a68/tools/bolt/results/cache-release-20261022/build-evidence-provenance.json)


## 14. 2026-10-23：异常兜底修复前的挂载检查停止

用户要求先确认首轮 `baseline-root/proc` 无占用，再正常卸载；仍被占用时立即停止，不结束占用进程。本次 19:17（Asia/Shanghai）检查未满足该前提。

完整路径：`/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261022-cache-release/baseline-root/local/BUILD-ROOTS/scratch.x86_64.0/proc`。

`lsof -nP <路径>` 返回 0，原文：

```text
COMMAND    PID   USER   FD   TYPE DEVICE SIZE/OFF  NODE NAME
code    202760 linhao   48r   DIR   0,60        0     1 <路径>
code    202760 linhao   49r   DIR   0,60        0 51203 <路径>/2558
```

上方仅为可读性缩写路径；[原始输出](../../tools/bolt/results/cache-release-exception-20261023/mount-prechecks.json)保存完整路径。`fuser -v <路径>` 同样返回 0，显示 `linhao 202760 f.... code`；`findmnt -M <路径>` 确认 proc 挂载仍在。直接读取 `/proc/202760/fd/48`、`49` 的链接也确认相同占用，见 [句柄证据](../../tools/bolt/results/cache-release-exception-20261023/proc-holders.json)。

| 项目 | 结果 |
|---|---|
| 占用检查 | FAIL：VS Code PID 202760，FD 48/49 |
| 正常卸载 | NOT RUN，按用户停止条件未尝试 |
| cache_release 修复及新增 IndexError 测试 | NOT RUN |
| 300 项测试、gbs export、五项 Tizen RPM 解析 | NOT RUN |
| 源码 amend / sandbox 推送 | NOT RUN |

源提交仍为 `d20e873b2c7dfac10fab9235e2b781dad08dc4c7`；没有修改 helper/spec，没有删除任何构建根，没有结束占用进程，也没有运行历史树中的 cmake/ninja。此前 299 项测试与五项解析结果不冒充本轮认证。仅提交本次停止记录和证据，等待用户释放句柄后再继续。


## 15. 2026-10-23：懒卸载、cache-release 异常兜底修复与 sandbox 更新

用户明确授权仅对首轮 baseline-root 下的 proc 挂载使用懒卸载，挂载结果不阻塞源码修复与推送。`findmnt -rn -o TARGET,SOURCE,FSTYPE` 检查该根只剩一个 `none proc` 挂载；执行：

```sh
sudo -n /usr/sbin/chroot /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261022-cache-release/baseline-root/local/BUILD-ROOTS/scratch.x86_64.0 /bin/umount -l /proc
```

返回 0，stdout/stderr 均为空。复查该根下挂载表为空；这是从挂载表脱离，不宣称 VS Code 已关闭原句柄。没有结束任何进程、修改 VS Code 配置或删除构建根。完整命令与过滤后的 findmnt 原文见 [mount.json](../../tools/bolt/results/cache-release-fix-20261023/mount.json)。

### 15.1 限定修复与认证

从 `d20e873b2c7dfac10fab9235e2b781dad08dc4c7` amend，源码差异只有 `packaging/clang-bolt-helper.py` 中的两处：`cache_release` 外层异常改为 `except Exception`；在 `original.strip()[5:-5]` 上方补充去掉 CMake Ninja `: && ` / ` && :`、与 replay_script 一致的注释。第三处为证据仓库新增的 IndexError 测试，不随 Source 发布。测试注入 replay_script 抛出 IndexError，确认 CLI 返回 0、打印 skipped、JSON status/reason 正确且缓存未删除。

- [源码完整 diff](../../tools/bolt/results/cache-release-fix-20261023/source.diff)：只改上述函数，2 行新增、1 行删除。
- [范围与身份核对](../../tools/bolt/results/cache-release-fix-20261023/verification.json)：spec 逐字节相同，其他 helper 顶层节点/函数 AST 相同；提交说明、父提交、Change-Id 不变。
- 全部 **300 项 PASS**（原 299 + IndexError 1）；[stdout](../../tools/bolt/results/cache-release-fix-20261023/tests.stdout)、[stderr](../../tools/bolt/results/cache-release-fix-20261023/tests.stderr)，`Ran 300 tests in 3.957s` / `OK`。
- 新提交 [GBS export](../../tools/bolt/results/cache-release-fix-20261023/export.json) 返回 0；[导出文件 SHA](../../tools/bolt/results/cache-release-fix-20261023/export-files.json)、[导出 spec](../../tools/bolt/results/cache-release-fix-20261023/exported-llvm.spec)。
- Tizen `rpm/rpm-build 4.14.1.1-1.7`，在首轮根中新建专用解析目录，使用 `rpmbuild -bp --nodeps --nobuild` 和 `rpmspec -P`，未执行构建或历史树 cmake/ninja，无需重新挂载 proc。

| 解析模式 | rpmbuild / rpmspec 退出码 | Patch0–6 | 结果 |
|---|---|---|---|
| x86_64 默认 BOLT 开 | 0 / 0 | 7 项 | PASS |
| x86_64 --without clang_bolt | 0 / 0 | 7 项 | PASS |
| x86_64 bcond 一行回退 | 0 / 0 | 7 项 | PASS |
| armv7l | 0 / 0 | 7 项 | PASS |
| aarch64 | 0 / 0 | 7 项 | PASS |

完整 [五项命令与结果](../../tools/bolt/results/cache-release-fix-20261023/five-parse/matrix.json)，各次 stdout/stderr 在同目录。成功路径未改，按本轮授权不重跑完整构建；第13节双轮构建、candidate 与 RPM 比较结论继续有效，不冒充本提交重新构建。

### 15.2 源码与推送

- 新源提交：`3d3b4bf564fd8edec793e49e6de75b5fa7007d16`。
- tree：`1143bd87650ddf8c8ed5ca40c0643c58c82db5ca`。
- 父提交：`67619ec8bbbac7238a6cfc33a481ccfbcd12206f`。
- 作者/提交者：Hao Lin <hao.lin@samsung.com>（单次 git -c，不改全局配置）。
- Change-Id：`Ic98eab90cc017f127a66e1729b44fab8b8e8fb41`。
- spec SHA256：`64bff4b4f6a9587a28ba2b2663ce05b61a4c391bb59d9120beb2845cce488f1f`。
- helper SHA256：`fca5e528402bc45bc8c1f574f8087ee7d2165b162470259763afab3d1b8caa71`。

推前远端为 `9e5675f57d122549997caffa39b655dfefc46fee`，使用精确租约：

```sh
git push --force-with-lease=refs/heads/sandbox/lhmax2025/bolt_pgo:9e5675f57d122549997caffa39b655dfefc46fee origin 3d3b4bf564fd8edec793e49e6de75b5fa7007d16:refs/heads/sandbox/lhmax2025/bolt_pgo
```

返回 0，输出如下（stdout 为空；展示去掉行尾空格，字节原文见 sandbox-push.stderr）：

```text
remote:
remote: Processing changes: refs: 1
remote: Processing changes: refs: 1, done
To ssh://review.tizen.org:29418/platform/upstream/llvm
 + 9e5675f57d12...3d3b4bf564fd 3d3b4bf564fd8edec793e49e6de75b5fa7007d16 -> sandbox/lhmax2025/bolt_pgo (forced update)
```

[推送完整记录](../../tools/bolt/results/cache-release-fix-20261023/sandbox-push.json)、[推前](../../tools/bolt/results/cache-release-fix-20261023/remote-before.json)、[推后](../../tools/bolt/results/cache-release-fix-20261023/remote-after.json)。推后远端精确等于新源提交。没有创建分支，没有推 refs/for，没有操作 QB。QB 软件包：`platform/upstream/llvm@3d3b4bf564fd8edec793e49e6de75b5fa7007d16`，由用户启动。
