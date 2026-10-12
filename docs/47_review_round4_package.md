# 47 第三轮评审修订与第四轮材料

日期：2026-10-12（Asia/Shanghai）。开场提交 `bda33ec60e694aeb92e71ac0444901350567a8ba`。

**当前完成第零步及第一步事实核查。Source 修订、测试、四次全量转换、根内小试与新补丁尚未执行，不用历史通过代替本轮认证。**

## 0. 范围、证据与资源规则

W=`/home/linhao/Toolchain/development/llvm-optimize`；本轮 E=`W/temp/review-round4-20261012`，下述 temp 证据仅在本机。依用户裁决：轻量阶段准入6 GiB，全量转换10 GiB；不足每5分钟复查、最多60分钟。运行中scope 18 GiB、swap0、nice15/ionice3、30秒采样，宿主可用低于2 GiB即中止。Commands、356627 spec、W/llvm与配置不改；不做完整RPM构建、不推Gerrit。后续仅授权四个小spec实验。

宿主 `mmap_min_addr` 沿用先前GBS设置；需要恢复时用户执行 `sudo sysctl -w vm.mmap_min_addr=65536`，重启也会恢复。本轮尚未挂载/proc。

## 1. 第零步完整性

| 项目 | 结果 | E内证据 |
|---|---|---|
| 截止点 | reflog 2026-10-12 19:35:32+08；本地HEAD/origin/main/远端main均bda33ec，无新提交 | integrity/main-*.stdout、remote-head.stdout |
| 主仓库全量status | 4,995,871行；非忽略差异只有用户gbs_llvm.conf | integrity/main-status-all.stdout |
| W/llvm | HEAD f111162e94aa48ed367c9d2c039456c70e7160ae；sandbox/fangyu.he/llvm_optmize；仅原三处并发改动 | integrity/llvm-*.stdout |
| 保护文件 | 69个HEAD blob全同；spec SHA95887b2d…、配置28f1caf9…均相符 | integrity/head-blob-check.json、input-integrity.jsonl |
| 修改时间全集 | 104条全部归因，未知0；15个权限盲目录免密只读补扫，新增0 | metadata-attribution.json、privileged-newer-command.json |
| 输入内容 | x86 225+ARM32 210+AArch64 212=647档；工具/代码/补丁等合计672项SHA PASS | input-integrity-result.json、input-integrity.jsonl |

归因类别：本轮锁/证据52、Git目录元数据15、上一收尾提交对象13、Codex自动树/refs15、上一提交/推送元数据9。自动树与HEAD的唯一差异是已登记配置，其blob SHA28f1caf9…一致。没有回滚或修复任何历史文件。本阶段未动用辅助脚本重试条款。原始find exit1仅来自15个权限盲目录，已补扫补齐；不把不完整扫描本身记为PASS。（证据：metadata-gate.json、git-object-attribution.json、codex-ref-attribution.json。）

## 2. 本轮实际资源

| 阶段 | 准入GiB | 启动可用GiB | scope峰GiB | 结果 |
|---|---:|---:|---:|---|
| input-integrity-scope | 6 | 13.937710 | 1.200821 | exit 0，采样回收 |
| integrity-scope | 6 | 9.839542 | 5.730644 | exit 0，采样回收 |
| metadata-completion-scope | 6 | 10.701515 | 0.016010 | exit 0，采样回收 |

均未触发OOM或宿主2GiB保护；scope峰包含文件缓存。原始命令、日志、采样与退出状态见各scope目录。

## 3. 第一步事实核查

### 3.1 发布模式与当前认证边界

三根展开`%{defined _toolchain}|%{_toolchain}`均为`1|clang`。W/gbs_llvm.conf:6,9,12只列仓库，不直接定义宏；GBS取得的E9=`temp/arm-archive-stage1-c-newrepo-20261010/buildconfig-from-W.conf`:161原文为`%_toolchain %{?_toolchain_override}%{!?_toolchain_override:clang}`，SHA1e7610b6…；其来源链已由docs/13§3、docs/40§9核查为Unified配置。根内`home/abuild/.rpmmacros`对应行为x86:63、ARM32/A64:65。目标cb679968 spec:11–16因此进入`llvm_release_build=0`分支；178–186的移除调试选项sed不执行。（本轮facts-result.json/macro_files；三份*-toolchain-macro.stdout；target-spec.stdout。）

历史x86构建采用此带调试分支，docs/13及docs/35的日志同时有带`-gdwarf-4`的CMake调用、find-debuginfo与9个debuginfo RPM写出；docs/30/34/38沿用同配方、22包结果及debug分支记录，不把它们说成发布模式认证。两ARM只执行-bc，日志CMake flags保留`-g2 -gdwarf-4`；没有运行%install或生成debuginfo RPM，不能由“未产包”推断发布模式。具体日志路径、逐行摘录与SHA见facts-result.json/historical_logs；历史打包记录见docs/13§8、docs/30、docs/34–38。

静态模拟使用cb679968:180原样CFLAGS sed表达式，经`/usr/bin/sed`作用于每条完整记录命令，再由本轮开场分类函数分类；不转换任何成员。结果：

| 架构 | 全部记录命令 | PASS | FAIL | 唯一失败原因 |
|---|---:|---:|---:|---|
| x86_64 | 3853 | 0 | 3853 | `uncertified last DWARF option: missing` |
| armv7l | 3683 | 0 | 3683 | `uncertified last DWARF option: missing` |
| aarch64 | 3699 | 0 | 3699 | `uncertified last DWARF option: missing` |

**发布模式未被当前认证策略覆盖。** 删除调试参数后缺少强制的-gdwarf-4；这是纯文本模拟结论，不是本轮构建失败。按PM约束只记录，不改Source策略，后续如何支持发布模式待PM裁决。（证据：三份*-release-input.txt/output.txt/simulation.json；facts.py；target-spec.stdout。）

### 3.2 原生读取与工具身份

两根都执行用户给定命令：目标`/usr/bin/prlimit --as=4294967296 -- /emul/usr/bin/bash --noprofile --norc -p -c ...`，使用bash内建read/printf读取/proc/self/limits。原始读回均为：

```text
Max address space         unlimited            unlimited            bytes
```

exit均0。这证实此路径的4GiB限制没有传到原生bash，不能把旧失效归因于“只读到了错误的模拟cat”。本轮探针只读，不修改Commands或限制策略。（证据：armv7l-native-readback.stdout、aarch64-native-readback.stdout、facts-commands.json。）

| 根 | bash SHA256 | RPM归属 | ELF/解释器 |
|---|---|---|---|
| armv7l | `a0f9c3ac42deef107e32940003fb7373ab3d697dcfccb49734286e562cbc9000` | `qemu-accel-x86_64-armv7l-0.4-1.1.armv7l` | ELF64小端machine62；`/emul/usr/lib64/ld-linux-x86-64.so.2` |
| aarch64 | `4cfa54c74219fb7294ed8ce1d91909b36c52e6def59798d12d61ea3a736a5780` | `qemu-accel-x86_64-aarch64-0.4-1.1.aarch64` | ELF64小端machine62；`/emul/usr/lib64/ld-linux-x86-64.so.2` |

两根`home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/CMakeCache.txt`均存在；第六步根内小试不因缺构建目录而跳过。R32/R64沿用docs/46§0路径；完整绝对路径/Cache SHA在facts-result.json。/proc分别临时挂载并finally卸载，前/中/后mountinfo全部保存。（证据：*-facts-mount-*.txt，*-bash-{file,elf-header,elf-program,owner}.stdout，facts-result.json。）

## 4. 后续状态

Source仍014fd32f…/c3edada0…，两候选补丁仍1293f698…/aab2cfd1…。代码/测试/小型spec/转换/根内小试/新补丁尚未执行；第四轮评审、x86完整构建、ARM第二段待完成。
