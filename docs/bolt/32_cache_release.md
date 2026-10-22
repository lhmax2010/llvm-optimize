# ThinLTO 缓存释放与双轮本地测量（2026-10-22）

最新状态（2026-10-23）：**用户释放内存后已恢复第一轮基线构建；实现、299 项测试、五项 Tizen RPM 解析 PASS，两轮完整构建认证仍未完成。**

以下为2026-10-22停止快照，当前续跑见第9节。 第一次未改 9e5675f 的构建停在普通 LLVM 链接；分段暂停后，等待内存准入达到 60 分钟上限。BOLT 实际增量尚未测得；释放后的整轮峰值及后处理降幅尚未测得；clang 与 RPM 一致性尚未验证。不得用历史 97 GB 缓存代替本次测量。

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

## 6. 双轮结果：资源停止，不能宣称完整认证

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

## 7. 继续工作的条件与边界

第一轮尚未完成，不能删除其根来腾空间。新根位于 `W/temp/bolt-v4-20261022-cache-release/baseline-root`，下一次续跑需重新满足本地资源准入；本轮到等待上限后已停止，没有通过重启来重置等待期限。第二轮仍须相同固定快照/宏条件，先保全第一轮所有RPM、candidate、identity与四次报告，再执行修订轮并逐文件比较。源码修改不能视为已经完成两轮实物认证。

## 8. 原始证据

目录：[`tools/bolt/results/cache-release-20261022/`](../../tools/bolt/results/cache-release-20261022/)。源码、测试、解析为已完成材料；构建运行及停止记录已保存；见partial-measurement.json、timeline.tsv、各段完整压缩日志与JSONL。没有删除历史目录或任何真实构建缓存。

原始RPM生成脚本保留4处行末空白，原始iostat保留EOF空行；git diff --check对此给出提示，未改写原文以消除提示。排除这两份原始证据后的文档/脚本差异检查通过；110份归档证据SHA复核通过，详见delivery-checks.json。

## 9. 2026-10-23 内存释放后的续跑（进行中）

用户明确要求继续后，01:01:51 CST重新取得共享锁。准入 MemAvailable=28,059,787,264B，/home可用427,441,000,448B；复核本次新根的四项SOURCES和固定build.conf身份未变。以原RPM入口继续完整 `rpmbuild -ba --noprep`，未触碰历史根。新计划356项；普通bugpoint、libLTO和liblldb先后完成，128/356后仍在同时链接普通clang-22与libclang-cpp.so.22.1，尚未进入BOLT。

16GiB限额下两路LLD几乎用满匿名内存，memory.events的max计数增加、I/O压力高，但oom/oom_kill均0。2026-10-23 01:45:30 CST，用户明确批准“允许本次两轮使用20GiB”，随即用systemctl set-property --runtime把本次构建MemoryMax调到21,474,836,480B；swap=0、nice15、ionice3、低于3GiB停止和锁时限不变。第二轮本地控制器使用同样20GiB上限。此裁决只适用于本次两轮本地测量，不改spec、helper或构建参数；第一轮调整前后分段记录，不能称为从头到尾统一资源条件。原始前后值与命令见baseline-resume2/memory-limit-adjustment.json。

新增独立5秒进程采样，避免du阻塞时漏采VmHWM；du存在临时文件扫描竞态的读数标注rc1，不能称为完整精确值。未取得第一轮完整产物前不启动第二轮、不删除第一轮根。

后续裁决（2026-10-23）：用户先批准“仅冻结续跑使用3GiB准入”，01:57:59已重新取锁、恢复同一现场；第一次持锁3200.515秒，冻结/释放均成功。随后用户明确要求“解除内存限制，所以目前不考虑准入内存和冻结内存，你跑你的”，01:59:18已将MemoryMax设为infinity；第二轮本地入口取消内存上限和准入等待。原始命令/返回值见memory-unlimited.json，控制器交接见controller-handoff.json。源码和构建参数不变；锁与磁盘规则继续执行。原运行采样器仍包含运行中<3GiB的紧急停止检查（并非启动准入，未在本次续跑触发），没有为热替换采样器而重启LLVM链接。

02:03左右普通libclang-cpp链接完成，进度恢复到138/356；该时点cgroup峰值26,155,147,264B（约24.4GiB），oom/oom_kill仍0。普通clang仍在链接，尚不能填写BOLT实测增量。
