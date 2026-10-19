# 混合链接组员验证指南 v3

状态（2026-10-19）：**统一 Gerrit 分支已创建并回读，A 的身份与 GBS 导出检查通过；组员直接选择该分支验证，不再提交或推送。** 本轮未构建。补丁与 188 目标期望表保持不变，配置级证据见 [设计报告](52_hybrid_link_tizen_base.md)。

固定身份：HEAD `6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2`；tree `80a6fd231c4564a3b762f4ec288cf2c41f9d2e20`；parent `67619ec8bbbac7238a6cfc33a481ccfbcd12206f`；Change-Id `I28171720d5bbbf9eaf491cdafc0aee0b43f9cd06`。原补丁 commit cef4d90 的 tree 相同，提交说明只重新折行。身份、推送原文、新克隆及 export 证据见 [本轮记录](52_hybrid_sandbox_evidence/README.md)。v1/v2 manifest 保留为历史，不用于核对 v3 指南 SHA。

## 0. 一次填写的变量块

先填尖括号，再执行适用步骤；目录由变量组合得到的行是本指南明确创建/使用的位置，不表示已存在。未知的工作区、克隆 URL、GBS 根、下载 RPM 路径均使用占位，不提供伪造的现成 sysroot/测试根。Base/Unified 采用对照日志中的固定 URL，失效即按 §3 报错；不得自动替换 latest。宿主需要 Bash、Python ≥3.9、Git、rpm/rpm2cpio、cpio、readelf；可选本地构建另需已配置的 GBS 与 `/usr/bin/time`，根内运行检查需要 sudo/chroot 权限。

```bash
set -euo pipefail
export W='<本仓库 checkout 的绝对路径>'
export LLVM_REPO='<组员具有读取权限的 Gerrit SSH URL>'
# URL 格式：ssh://<组员账号>@review.tizen.org:29418/platform/upstream/llvm
export LLVM_BRANCH='sandbox/lhmax2025/llvm_optimize'
export EXPECTED_HEAD=6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2
export BASE=67619ec8bbbac7238a6cfc33a481ccfbcd12206f
export EXPECTED_TREE=80a6fd231c4564a3b762f4ec288cf2c41f9d2e20
export BOLT_BRANCH='sandbox/lhmax2025/bolt_pgo' # 仅风险登记，不访问。
export EVIDENCE="$W/docs/52_hybrid_link_evidence"
export V3_EVIDENCE="$W/docs/52_hybrid_sandbox_evidence"
export EXPECTATIONS="$EVIDENCE/needed-expectations-v2.json"
export ARCHIVE_EXPECTATIONS="$V3_EVIDENCE/expected-static-devel-archives.txt"
export QB_REF="$W/docs/qb_1199098_vs_1178133"
export S="$W/temp/llvm-hybrid52-team-v3" # §1 会新建
export G='<本地 x86_64 GBS 独立根的绝对路径>' # 仅执行可选 §3 时填写
export LOG="$W/temp/hybrid52-team-validation-v3"
export INPUT_CONFIG="$W/gbs_llvm.conf"
export CONFIG="$LOG/inputs/gbs-hybrid.conf"
export BC="$LOG/inputs/project-buildconfig.conf" # 项目导出的完整 buildconfig
export BASE_SNAPSHOT=tizen-base-toolchain_20261015.022255
export UNIFIED_SNAPSHOT=tizen-unified-toolchain_20260917.132101
export BASE_REPO="http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/${BASE_SNAPSHOT}/repos/standard/packages/"
export UNIFIED_REPO="http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/${UNIFIED_SNAPSHOT}/repos/standard/packages/"
export QB_LLVM_PROJECT='Tizen-Base-Toolchain/standard'
export QB_DOWNSTREAM_PROJECT='Tizen-Unified-Toolchain/standard'
export CONTROL_QB=1199098
export NEW_QB='<本次 QB ID>'
export NEW_BASE_SNAPSHOT='<新 llvm 和 accel 的具体 Base 快照名>'
export NEW_UNIFIED_SNAPSHOT='<本次下游实际使用的 Unified 快照名>'
export RPM_DIR='<下载的本次 22 个 x86_64 RPM 所在目录>'
export N="$LOG/extracted-llvm" # §4.1 新建，仅解包检查
export TEST_ROOT="$G/local/BUILD-ROOTS/scratch.x86_64.0" # §3 成功后实际生成，§4.2 验证
export ROOT_RPMS=/var/tmp/hybrid52-test-rpms # §4.2 在测试根内新建
export SMOKE=/var/tmp/hybrid52-smoke # §5 在测试根内新建
export ACCEL_ARCH='<armv7l 或 aarch64，每个架构分别执行 §6>'
export ACCEL_RPM='<该架构 clang-accel-x86_64-ARCH RPM 的绝对路径>'
export QEMU_ACCEL_RPM='<同一快照同架构 qemu-accel-x86_64-ARCH RPM 的绝对路径>'
export ACCEL_EXTRACT="$LOG/accel-pair-$ACCEL_ARCH" # §6.1 新建两包合并目录
export ACCEL_CLANG_ONLY="$LOG/accel-clang-only-$ACCEL_ARCH" # 单包 du 统计用
export EMUL="$ACCEL_EXTRACT/emul" # §6.1 路径；§6.2 按实际 GBS 根重设
export ARM_GBS_ROOT='<已完成本地该 ARM 架构 gbs build 的 -B 目录>' # 只用于 §6.2
export ACCEL_LOADER="$EMUL/lib64/ld-linux-x86-64.so.2"
export ACCEL_LIBPATH="$EMUL/lib64:$EMUL/usr/lib64"
mkdir -p "$LOG/inputs"
```

Base/Unified 来源见 [1199098 quickbuild 338–347 行](qb_1199098_vs_1178133/raw/1199098_quickbuild.txt#L338)。Unified 在该日志里是注释掉的参考仓库，实际启用集合以项目导出配置为准。29864 秒来自关联 Base 的 x86_64 llvm 构建，并非该 Unified 请求重建了 llvm：[llvm_builds.csv 第 2 行](qb_1199098_vs_1178133/llvm_builds.csv#L2)。

## 1. 只读克隆统一分支

本次匿名 HTTPS `https://review.tizen.org/gerrit/platform/upstream/llvm` 在禁用交互凭据时要求用户名，未能匿名读取；请填写组员具有仓库读取权限的 SSH URL。这里只执行 clone/fetch，不推送。组员不提交、不推送，所以不涉及提交者身份。

```bash
test ! -e "$S"
git clone --single-branch --branch "$LLVM_BRANCH" "$LLVM_REPO" "$S"
# GBS patch-export 需要 upstream 引用；没有它会选择 native 导出。
git -C "$S" fetch origin refs/heads/upstream:refs/remotes/origin/upstream
test "$(git -C "$S" rev-parse HEAD)" = "$EXPECTED_HEAD"
test "$(git -C "$S" rev-parse HEAD^{tree})" = "$EXPECTED_TREE"
test "$(git -C "$S" rev-parse HEAD^)" = "$BASE"
test -z "$(git -C "$S" status --porcelain)"
git -C "$S" show -s --format=fuller HEAD | tee "$LOG/branch-identity.txt"
```

若今后分支已更新，HEAD 核对会失败；先取得同步更新的指南/身份，不跳过门禁。混合链接线只维护 `$LLVM_BRANCH`，不再另建 sandbox。此次新克隆和 GBS 导出均已实测：8 个自动 Patch 声明、8 个 `%patch` 都在条件块之外，见 [export 检查](52_hybrid_sandbox_evidence/a3-export-conditions.json)。本地可复核导出（仍不构建）：

```bash
gbs -c "$INPUT_CONFIG" export --commit "$EXPECTED_HEAD" --spec llvm.spec \
 --outdir-directly --outdir "$LOG/export" "$S" 2>&1 | tee "$LOG/export.log"
```

## 2. 主路径：Quickbuild 逐步清单

1. **直接选择统一分支**。在 QB 中选择 `sandbox/lhmax2025/llvm_optimize`（`$LLVM_BRANCH`），确认解析到 `$EXPECTED_HEAD`，在 `$QB_LLVM_PROJECT` 起 x86_64 llvm 构建。组员不再执行任何 sandbox push。

2. **构建 x86_64 llvm**。在 `$QB_LLVM_PROJECT` 中选择 `$LLVM_BRANCH`，以与 `$CONTROL_QB` 关联的 Base llvm 构建相同的项目/仓库启动。核对所选 spec 为 `packaging/llvm.spec`，完整保存项目导出配置、buildconfig、实际源码 commit、输入仓库快照、RPM 版本和 worker 信息。记录总耗时、`%build` 与 `%install` 阶段耗时、转换 BEGIN–END；QB 能看到构建机峰值内存时记录数值/单位/口径，看不到则写“未获取”。总耗时与 **29864 秒**对照，并同时写两次输入及产出快照。阶段时间取阶段边界日志，不能把下载/准备时间算进 `%build`，也不能用总时长反推峰值内存。旧完整日志：[1199098 Base x86_64 llvm](qb_1199098_vs_1178133/raw/1199098_base_x86_64_llvm.txt)，阶段依据及旧 5686 秒见 [llvm_builds.csv](qb_1199098_vs_1178133/llvm_builds.csv)。下载本次 22 个 RPM，执行 §4–§5。
3. **新 llvm 之后的 accel 构建：先确认触发方式**。现有证据只能确认顺序和消费的版本，**不能确定是同一 Base QB 请求、依赖更新自动触发还是另行人工请求，需向 QB 管理员确认**。1199098 本身是 Unified 请求，其包列表既无 llvm 也无 qemu-accel；不能据它编造“勾选一起构建”的步骤。

   | 已知事实 | 证据（均为保存的原文） |
   |---|---|
   | Base x86_64 llvm 22.1.8-3.1 在 2026-10-14 15:22:15 UTC 完成 | [llvm_builds.csv:2](qb_1199098_vs_1178133/llvm_builds.csv#L2) |
   | 两种 accel 均在 17:18:03 UTC 开始，晚于 llvm 完成 | [qemu_builds.csv:2–3](qb_1199098_vs_1178133/qemu_builds.csv#L2) |
   | 两者构建环境实际安装 libllvm/llvm/clang 22.1.8-3.1 | [armv7l 日志:247/253/312](qb_1199098_vs_1178133/raw/1199098_base_x86_64_qemu-accel-armv7l.txt#L247)、[aarch64 日志:247/253/312](qb_1199098_vs_1178133/raw/1199098_base_x86_64_qemu-accel-aarch64.txt#L247) |
   | 此 Unified 请求引用已有 Base 快照，而非该请求重建这两个包 | 上述 CSV 的 `unified_rebuilt` 字段及 [quickbuild:315–323](qb_1199098_vs_1178133/raw/1199098_quickbuild.txt#L315) |

   组员操作顺序：①保存新 llvm 的构建结果、版本与产物仓库；②把该信息交 QB 管理员，明确询问 Base 项目是否启用依赖重建、怎样触发/定位两个 qemu-accel 包的构建请求，保存回答与请求 ID；③按管理员确认的方法触发或等待已经排队的 `qemu-accel-armv7l`、`qemu-accel-aarch64`（**这两个打包构建本身是 x86_64**），检查其安装清单确实消费新 llvm/clang/libllvm，若不是则不能继续验证；④取得同一新快照中每个目标架构的 qemu-accel-x86_64 与 clang-accel-x86_64 两包，再执行 §6。不在这里假定一条未经证实的 QB CLI 或自动触发规则。

   记录 clang-accel RPM 字节、头 FILESIZES、单包解包 du，与 [SIZE_FINDINGS](qb_1199098_vs_1178133/size_attribution/SIZE_FINDINGS.md) 同口径比较；aarch64 缺旧逐文件体积基线就注明未获取。

4. **下游六格验证**。以新 Base/accel，在 armv7l、aarch64 各构建 zlib、libpng、libinput，锁定旧日志同一源码/配方，记录差异。zlib 对照来自 Base，libpng/libinput 来自 Unified，保持各自项目。每格记录成功/失败、实际安装的 clang/accel 版本、buildroot 准备时间、包构建时间及日志行号。准备时间定义为日志开始到第一条 `%prep`，包构建时间为 `%prep` 到 finished，另保留 started–finished 总时长；新旧按同一边界重新取数，不能把页面 Profiling 时长直接当准备时间。旧日志分秒时间戳的精度为秒，缺边界则“未获取”。

   | 包 | armv7l 对照 | aarch64 对照 |
   |---|---|---|
   | zlib | `raw/{1199098,1178133}_base_armv7l_zlib.txt` | `raw/{1199098,1178133}_base_aarch64_zlib.txt` |
   | libpng | `raw/{1199098,1178133}_armv7l_libpng-1.6.44-0.txt` | 未获取；既有这批 Unified 只有 armv7l，仍须做新 aarch64 验证 |
   | libinput | `raw/{1199098,1178133}_armv7l_libinput-1.31.3-0.txt` | 未获取；同上 |

   表中路径均相对 `$QB_REF`。来源范围见 [FINDINGS.md](qb_1199098_vs_1178133/FINDINGS.md)“下游实际使用的编译器与链接器”“两次构建是否同条件”。为每一格保存 `arch,package,source_commit,base_snapshot,unified_snapshot,accel_nevra,result,root_prepare_s,package_build_s,total_s,peak_memory,log_evidence`，未获取项注明原因。
5. **accel 依赖闭合**。按 §6 下载两包离线检查，或使用本地 GBS 根，分别验证两种架构，检查所有实际 accel ELF，包括工具与 DSO。不能只检查 clang，也不能只以包内存在同名共享库判闭合。依赖缺失、下游构建失败或待分析项未闭合，均不能提交“全项 PASS”。

QB 网页/API 的启动方式由团队现有流程操作；本仓库没有可验证的通用启动 CLI，故没有编造命令。回传原始页面/完整日志，不能只报耗时汇总。

## 3. 可选：本地 GBS 正确性验证

### 3.1 仓库和 buildconfig 必须与对照项目一致

`BASE_REPO` 使用对照 QB 日志记录的具体 Base 快照；本版默认已经填好，不能留空或自动改 latest。对照若改为另一次 QB，先从那次完整日志提取 Base/Unified URL、快照名和实际启用仓库，再统一更新 §0。本地记录输入快照，与新产出快照分开。**404 或任一非 200 直接退出，不换源重试**；这表示无法复现该输入，需报告。旧工作区配置的 Base 曾 404，不能直接拿它构建。

从 `$QB_LLVM_PROJECT` 导出本次完整 buildconfig 到 `$BC`，保存导出项目、时间、URL/页面证据和 SHA。不得使用 9 月历史 buildconfig 或空文件。下面只生成验证用配置副本，不改 `$INPUT_CONFIG`；若实际项目仓库集合与两仓库模板不一致，停止并按项目导出配置核对后再登记。

```bash
test -s "$BC"
sha256sum "$BC" "$INPUT_CONFIG" | tee "$LOG/inputs/input-sha.txt"
python3 - <<'PY'
import configparser, hashlib, json, os, pathlib, urllib.request
out=pathlib.Path(os.environ['LOG'])/'inputs'
c=configparser.ConfigParser(interpolation=None)
assert c.read(os.environ['INPUT_CONFIG']), 'missing input config'
records=[]
for section, env in [('repo.base-standard','BASE_REPO'),('repo.unified-standard','UNIFIED_REPO')]:
    assert section in c, 'project/config section mismatch: '+section
    base=os.environ[env].rstrip('/')+'/'
    assert 'latest' not in base and '_20' in base, 'require concrete snapshot'
    url=base+'repodata/repomd.xml'
    # HTTPError (including 404), timeout, or non-200 aborts this command and shell.
    with urllib.request.urlopen(url,timeout=30) as r:
        assert r.status==200,(url,r.status)
        data=r.read(); final_url=r.url
    (out/(section+'-repomd.xml')).write_bytes(data)
    records.append(dict(repo=section,url=url,final_url=final_url,status=200,
                        sha256=hashlib.sha256(data).hexdigest()))
    c[section]['url']=base
profile=c['general']['profile']
assert profile in c, 'missing selected profile: '+profile
c[profile]['buildconf']=os.environ['BC']
with open(os.environ['CONFIG'],'w') as f: c.write(f)
(out/'repository-preflight.json').write_text(json.dumps(records,indent=2)+'\n')
PY
# diff 的退出码 1 表示有差异，>1 才是错误；逐项确认只涉及上述仓库/buildconfig。
diff -u "$INPUT_CONFIG" "$CONFIG" > "$LOG/inputs/config.diff" || test "$?" -eq 1
sha256sum "$CONFIG" "$BC" | tee "$LOG/inputs/build-input-sha.txt"
```

### 3.2 可选本地完整构建与资源参考

只在组员自己的独立目录执行，用于正确性验证；服务器资源配置由其管理员决定，本指南不携带本机的锁、内存 cap、磁盘准入或杀进程规则。

**旧源码参考，不是本次实测或最低配置承诺**：9 月混合试构建最大单链接 RSS 约 **15.18 GiB**、受限 scope 记账峰值 **18 GiB**，可读 GBS 根约 **47 GiB**、源码约 **2.5 GiB**；同文件系统可用空间减少约 **60.05 GiB**（包含同期活动，不能全算为构建），见 [docs/22 §4](22_hybrid_link_trial.md#4-构建终态与资源实测)。docs/49 后续配方的最大链接约 **10.27 GiB**、scope 峰值同样达到当时的 18 GiB 上限，见 [docs/49 §1 资源表](49_x86_build_resume_result.md#1-唯一一次续跑成功)。其启动可用 266.280327 GiB、续跑期最低约 55.15 GiB，对应文件系统变化约 211 GiB；这是跨阶段、含其他活动的空间变化，不是独占构建树精确峰值，来源 [第二轮启动记录 §1](49_x86_build_round2_result.md#1-清理准入与唯一调用)、[续跑资源表](49_x86_build_resume_result.md#1-唯一一次续跑成功)。因此容量规划按**数十 GiB 内存、数百 GiB 工作空间**考虑，并为源码、ThinLTO 缓存、安装树、RPM 和解包留余量；并发大链接需要更多内存。这里只有参考，不做硬性拦截。

配方仍为 Ninja 6 / compile pool 6 / link pool 2；保留 debuginfo `-j4`。以下命令不改变这些编译参数，`time -v` 记录 wall 和其进程统计口径的最大 RSS，不把它称为所有并发进程的总峰值；如服务器另有整体峰值观测，注明口径。

```bash
test ! -e "$G"
set +e
/usr/bin/time -v -o "$LOG/time-v.txt" \
 gbs -c "$CONFIG" build -A x86_64 -B "$G" --threads 1 --include-all \
 --spec llvm.spec --define '_smp_mflags -j4' -D "$BC" "$S" \
 2>&1 | tee "$LOG/build.log"
rc=(${PIPESTATUS[@]})
set -e
printf 'build=%s tee=%s\n' "${rc[0]}" "${rc[1]}" | tee "$LOG/exit.txt"
test "${rc[0]}" -eq 0 && test "${rc[1]}" -eq 0
# 本地结果用这里的 RPM；仅使用 QB 结果时继续使用变量块中的下载目录。
export RPM_DIR="$TEST_ROOT/home/abuild/rpmbuild/RPMS/x86_64"
```

## 4. 新 RPM、NEEDED 与归档检查（QB / 本地通用）

### 4.1 22 包及解包清单

把本次产物放到 `$RPM_DIR`，不同架构/旧版本不得混入。命令在验证宿主执行；解包根 `$N` 必须全新。

```bash
mapfile -t rpms < <(find "$RPM_DIR" -maxdepth 1 -type f -name '*.rpm' | sort)
test "${#rpms[@]}" -eq 22
rpm -qp --qf '%{NAME}\n' "${rpms[@]}" | sort > "$LOG/rpm-names.txt"
diff -u "$EVIDENCE/expected-rpm-names.txt" "$LOG/rpm-names.txt"
sha256sum "${rpms[@]}" > "$LOG/rpms.sha256"
stat -Lc '%s %n' "${rpms[@]}" > "$LOG/rpms-bytes.txt"
rpm -qp --qf '%{NEVRA}\n' "${rpms[@]}" > "$LOG/rpms-nevra.txt"
test ! -e "$N"
mkdir -p "$N"
for f in "${rpms[@]}"; do
  (cd "$N"; rpm2cpio "$f" | cpio -idm --quiet)
done
rpm -qpl "${rpms[@]}" | sort -u > "$LOG/rpm-paths.txt"
```

PASS：包名集与 [22 包名单](52_hybrid_link_evidence/expected-rpm-names.txt) 完全一致，记录各 RPM 字节数与 SHA。Source/静态归档转换保留不变，不能只看有 RPM 就宣称通过。

### 4.2 配置图驱动的 NEEDED 期望

[期望表](52_hybrid_link_evidence/needed-expectations-v2.json) 对 [a-all-link-targets.json](52_hybrid_link_evidence/a-all-link-targets.json) 的 **188 个链接目标逐个登记**。从 `link_libraries` 解析共享输入并与已有布尔列交叉核对，结合 [CMake 别名表](52_hybrid_link_evidence/aliases.json)、[安装别名证据](52_hybrid_link_evidence/install-aliases.txt)、[spec 安装动作](52_hybrid_link_evidence/x86_64-hybrid-install.txt#L6) 及 [展开后的 RPM 路径模式](52_hybrid_link_evidence/rpm-install-paths.txt) 映射安装文件；LLDB 的 SDK 搬移/复制也纳入。每行保存图行号、规则、安装路径和两种共享库期望。

| 类别 | 图目标数 | 直接 NEEDED 期望 | 示例/边界 |
|---|---:|---|---|
| 静态三组 `static_three_groups` | 3 | 两者均无 | clang-22、lld、llvm-ar；别名映射到同一目标 |
| 上游静态例外 `upstream_static_exceptions` | 5 | 两者均无 | llvm-tblgen、clang-tblgen、lldb-tblgen、llvm-config、llvm-exegesis |
| 两种共享库都不链 `neither_shared_library` | 29 | 两者均无 | obj2yaml/yaml2obj **若实际安装也按此类**；另含非安装构建工具、运行库和共享库生产者，不等于“零组件 .a” |
| 动态 LLVM `dynamic_llvm` | 108 | libLLVM 有、libclang-cpp 无 | opt、llc、lli、llvm-objcopy 等 |
| 动态 LLVM+clang-cpp `dynamic_llvm_clang_cpp` | 43 | 两者均有 | clang-repl/check/tidy、clangd 等 |

188 是配置图目标数，不是安装可执行文件数；没有安装路径的目标也保留，不把缺少这些 RPM 文件当失败。自检覆盖 188/188、无遗漏/重复，158 条显式安装路径（其中 `/usr/bin` 133），证据 [self-check.json](52_hybrid_link_evidence/needed-expectations-v2-self-check.json)。`obj2yaml/yaml2obj` 当前不在显式 `%files` 表中，未来若出现实际文件仍能按图映射；未知 ELF 硬报错，不默认为动态。

```bash
python3 "$W/tools/check_hybrid_link_needed.py" self-check \
 --graph "$EVIDENCE/a-all-link-targets.json" --aliases "$EVIDENCE/aliases.json" \
 --rpm-paths "$EVIDENCE/rpm-install-paths.txt" --table "$EXPECTATIONS" \
 --output "$LOG/needed-table-self-check.json"
# 从真实 RPM 清单取全部 /usr/bin 项，以及图中共享库及 SDK 位置；不包含 debuginfo 副本。
awk '/^\/usr\/bin\// || /^\/usr\/lib64\/.*\.so/ || /\/sdk_tools\/lldb\/(bin|lib64)\//' \
 "$LOG/rpm-paths.txt" > "$LOG/needed-paths.txt"
set +e
python3 "$W/tools/check_hybrid_link_needed.py" check --table "$EXPECTATIONS" \
 --root "$N" --paths "$LOG/needed-paths.txt" --require-declared --output "$LOG/needed-results.json"
needed_rc=$?
set -e
printf 'needed_exit=%s\n' "$needed_rc" | tee "$LOG/needed-exit.txt"
test "$needed_rc" -eq 0
```

检查器仅运行 `readelf -dW`，不执行被检 ELF；绝对软链接在 `$N` 内解析，避免误读宿主同名文件。逐文件保存完整 readelf 命令/输出及实际 NEEDED。`--require-declared` 还检查期望表的安装路径没有从输入清单漏掉。退出码：0 PASS；1 意外共享依赖（FAIL）；2 输入、映射、文件或 readelf 错误；**3 待分析：期望共享输入却没有对应 NEEDED**，可能被 `--as-needed` 删除，必须分析链接行/传递依赖，不能直接记 PASS。有记录的脚本/配置文件可记非 ELF；应为目标的文件却不是 ELF 则报错。脚本覆盖测试见 [21 项结果](52_hybrid_link_evidence/needed-checker-v2-tests.txt)。

#### 可执行的测试根准备（仅在完成 §3 的组员服务器）

前提：§3 已用该项目快照成功生成 x86_64 GBS 根，组员拥有该独立根的 sudo/chroot 权限；GBS 已安装构建依赖。`TEST_ROOT` 是由该次 `-B` 实际生成的 `local/BUILD-ROOTS/scratch.x86_64.0`，不是另一个假定存在的解包目录。安装以下 22 个新 RPM，**不使用 --nodeps**；`--oldpackage` 仅允许在这个独立测试根内以本次产物替换 release 数字更高的仓库包（本地构建 release 可能为 1），不改变宿主。若缺运行依赖，停止该根的运行检查并记录缺包，不能用宿主库补洞。

```bash
test -x "$TEST_ROOT/usr/bin/rpm"
test -x "$TEST_ROOT/bin/bash"
sudo chroot "$TEST_ROOT" uname -m | tee "$LOG/test-root-arch.txt"
grep -Fx x86_64 "$LOG/test-root-arch.txt"
sudo chroot "$TEST_ROOT" rpm -qa | sort > "$LOG/test-root-before.txt"
sudo test ! -e "$TEST_ROOT$ROOT_RPMS"
sudo mkdir -p "$TEST_ROOT$ROOT_RPMS"
sudo cp -- "${rpms[@]}" "$TEST_ROOT$ROOT_RPMS/"
sudo chroot "$TEST_ROOT" /bin/bash -eux -c \
 'rpm -Uvh --oldpackage --replacepkgs "$1"/*.rpm' bash "$ROOT_RPMS" \
 2>&1 | tee "$LOG/test-root-install.txt"
sudo chroot "$TEST_ROOT" rpm -qa | sort > "$LOG/test-root-after.txt"
# 核对安装 ELF 内容等于已通过 readelf 检查的解包副本，不能只看 RPM 版本。
sudo env N="$N" TEST_ROOT="$TEST_ROOT" LOG="$LOG" python3 - <<'PY_ROOT'
import hashlib,json,os,pathlib
root=pathlib.Path(os.environ['TEST_ROOT']); extracted=pathlib.Path(os.environ['N'])
rows=json.loads((pathlib.Path(os.environ['LOG'])/'needed-results.json').read_text())['results']
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
for r in rows:
    if r['status']!='PASS': continue
    # resolved 是检查器在 N 内解析出的真实实体，避免绝对 symlink 跳到宿主。
    relative=pathlib.Path(r['resolved']).relative_to(extracted.resolve())
    assert digest(root/relative)==digest(extracted/relative),str(relative)
print('INSTALLED_ELF_IDENTITY_PASS')
PY_ROOT
```

之后按 `needed-results.json` 中 ELF 路径逐个执行根内 `ldd`，动态 ELF 返回码须 0 且无 `not found`。三组“静态”仅指 LLVM 组件，仍可能依赖 libc。**只做 QB、没有本地测试根的组员**：保留 §4.1/§4.2 解包 readelf 与 §4.3 归档检查，运行闭合由 §6 的离线 accel 检查替代，编译/链接运行由 §2 六格观察；原生 x86_64 smoke/SDK LLDB 等未被六格覆盖的项目明确记“未执行”，不得声称全工具运行 PASS。这避免要求登录 QB worker 或捏造一棵根。

```bash
python3 - <<'PY'
import json,os,pathlib,subprocess
log=pathlib.Path(os.environ['LOG'])
checked=json.loads((log/'needed-results.json').read_text())
assert checked['status']=='PASS',checked['status']
rows=[]; failed=False
for item in checked['results']:
    if item['status']!='PASS': continue
    if not item['needed']:
        rows.append({'path':item['path'],'status':'NO_NEEDED'}); continue
    argv=['sudo','chroot',os.environ['TEST_ROOT'],'ldd',item['path']]
    r=subprocess.run(argv,capture_output=True,text=True,timeout=30)
    ok=r.returncode==0 and 'not found' not in r.stdout+r.stderr
    rows.append(dict(path=item['path'],argv=argv,exit=r.returncode,
                     stdout=r.stdout,stderr=r.stderr,status='PASS' if ok else 'FAIL'))
    failed |= not ok
(log/'ldd-results.json').write_text(json.dumps(rows,indent=2)+'\n')
assert rows and not failed,'ldd dependency closure failed'
PY
```

另检查以下别名仍是链接并解析到相应实体：

```bash
for f in clang clang++ clang-cpp clang-cl ld.lld ld64.lld lld-link wasm-ld llvm-ranlib llvm-lib llvm-dlltool; do
  sudo chroot "$TEST_ROOT" test -L "/usr/bin/$f"
  sudo chroot "$TEST_ROOT" readlink "/usr/bin/$f"
  sudo chroot "$TEST_ROOT" readlink -f "/usr/bin/$f"
done
```

### 4.3 常规包与静态开发包

归档清单取自对照 1199098 所引用快照的 `llvm-static-devel-22.1.8-3.1.x86_64.rpm`，本轮重新下载后 SHA 与原记录一致，再用 `rpm -qpl` 生成：[完整文件表](52_hybrid_sandbox_evidence/baseline-static-devel-files.txt)、[预期 .a 清单](52_hybrid_sandbox_evidence/expected-static-devel-archives.txt)、[来源/摘要/命令](52_hybrid_sandbox_evidence/baseline-static-devel-provenance.json)。门禁是逐路径集合相同，不能用固定归档数量替代；数量恰好相同但缺失/新增路径也失败。


```bash
for f in "${rpms[@]}"; do
  name=$(rpm -qp --qf '%{NAME}' "$f")
  rpm -qpl "$f" | awk '/\.a$/ {print}' > "$LOG/$name.archives"
  case "$name" in
    *devel*|compiler-rt) ;; # compiler-rt 的 45 个运行库保留，不是 LLVM 开发库
    *) test ! -s "$LOG/$name.archives" ;;
  esac
done
LC_ALL=C sort -u "$LOG/llvm-static-devel.archives" > "$LOG/static-devel-actual.txt"
diff -u "$ARCHIVE_EXPECTATIONS" "$LOG/static-devel-actual.txt"
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os,sys,pathlib,json
sys.path.insert(0,str(pathlib.Path(os.environ['W'])/'tools'))
from inspect_llvm_archives import inspect
log=pathlib.Path(os.environ['LOG']); root=pathlib.Path(os.environ['N'])
paths=(log/'llvm-static-devel.archives').read_text().splitlines()
expected=(pathlib.Path(os.environ['ARCHIVE_EXPECTATIONS'])).read_text().splitlines()
assert paths and sorted(paths)==expected, {'missing':sorted(set(expected)-set(paths)),
                                        'extra':sorted(set(paths)-set(expected))}
with (log/'archives.jsonl').open('w') as f:
    for name in paths:
        r=inspect(root/name.lstrip('/'))
        assert not r['thin'] and r['bitcode']==0 and r['other']==0,r['path']
        assert r['machine']==r['member_count'] and r['index_equals_machine_symbols'],r['path']
        assert all(not m['debug_sections'] for m in r['members']),r['path']
        f.write(json.dumps(r)+'\n')
print('Manifest-matched native archives / full index / no debug: PASS',len(paths))
PY
```

完整符号→成员索引按 header offset/序号区分同名成员，不用“armap 非空”替代。核对 libomp-devel 的 libarcher_static.a 与 static-devel 双归属文件一致，compiler-rt 为 45 个 `.a`；检查完整 NATIVE_ARCHIVES BEGIN/END、转换成功与标准 brp 后处理无格式错误。归档转换 Source 未改变；`.llvm_addrsig` 已知边界仍见 [docs/51](51_gnu_strip_merged_validation.md)，本补丁没有宣称修复该问题。

## 5. 实际编译、链接、运行

在安装新 RPM 的 `$TEST_ROOT` 内运行；`SMOKE` 取 §0，保存完整输出和退出码：

```bash
sudo chroot "$TEST_ROOT" /usr/bin/env SMOKE="$SMOKE" /bin/bash -eux <<'SH' \
  > "$LOG/native-smoke.txt" 2>&1
mkdir -p "$SMOKE"
cd "$SMOKE"
printf '#include <stdio.h>\nint main(void){puts("hello");return 0;}\n' > hello.c
printf '#include <iostream>\nint main(){std::cout<<"hello\\n";}\n' > hello.cc
clang -c hello.c -o hello.o
clang++ -c hello.cc -o hello-cxx.o
clang -fuse-ld=lld hello.o -o hello
clang++ -fuse-ld=lld hello-cxx.o -o hello-cxx
test "$(./hello)" = hello
test "$(./hello-cxx)" = hello
printf 'int answer(void){return 42;}\n' > answer.c
clang -c answer.c -o answer.o
llvm-ar rcs libanswer.a answer.o
llvm-ar t libanswer.a
llvm-nm --print-armap libanswer.a
ld.lld -r answer.o -o answer-linked.o
readelf -h answer-linked.o
opt --version
llc --version
clang-tidy --version
SH
```

armv7l/aarch64 的交叉编译和链接由 §2 的六格下游构建覆盖，使用项目实际 sysroot/工具链，删除独立交叉 hello 与人为假设的 sysroot/GCC 路径。保留每格实际 clang 路径、目标架构、链接命令和结果；构建成功只说明这些负载成功，不冒充每个工具的专项运行测试。仅在具备上述已安装测试根时执行本节 x86_64 smoke。

## 6. accel 体积与全部 ELF 依赖闭合：无需 QB worker 登录

两种方法任选其一，在能原生运行 x86_64 ELF 的组员服务器执行；每个目标架构各做一遍。虽然 RPM 的包架构是 armv7l/aarch64，`emul` 工具仍是 x86_64。只解包不安装这些 ARM RPM 到宿主。

### 6.1 两个 RPM 合并解包（QB 用户的默认路径）

需要同一新快照、同一目标架构且 release 配套的 **`qemu-accel-x86_64-<arch>` 与 `clang-accel-x86_64-<arch>`** 两个 RPM。只拿 clang-accel 不能假定 libc/loader/其他运行库齐全。来源 URL/快照/NEVRA/SHA 全部登记；若两包仍不闭合，按实际缺失库报告，不能偷用宿主库。

```bash
test "$ACCEL_ARCH" = armv7l || test "$ACCEL_ARCH" = aarch64
test "$(rpm -qp --qf '%{NAME}' "$ACCEL_RPM")" = "clang-accel-x86_64-$ACCEL_ARCH"
test "$(rpm -qp --qf '%{NAME}' "$QEMU_ACCEL_RPM")" = "qemu-accel-x86_64-$ACCEL_ARCH"
for f in "$ACCEL_RPM" "$QEMU_ACCEL_RPM"; do
  test "$(rpm -qp --qf '%{ARCH}' "$f")" = "$ACCEL_ARCH"
done
test "$(rpm -qp --qf '%{VERSION}-%{RELEASE}' "$ACCEL_RPM")" = \
     "$(rpm -qp --qf '%{VERSION}-%{RELEASE}' "$QEMU_ACCEL_RPM")"
test ! -e "$ACCEL_EXTRACT"
test ! -e "$ACCEL_CLANG_ONLY"
mkdir -p "$ACCEL_EXTRACT" "$ACCEL_CLANG_ONLY"
sha256sum "$ACCEL_RPM" "$QEMU_ACCEL_RPM" > "$LOG/accel-$ACCEL_ARCH-rpms.sha256"
rpm -qp --qf '%{NEVRA}\n' "$ACCEL_RPM" "$QEMU_ACCEL_RPM" > "$LOG/accel-$ACCEL_ARCH-nevra.txt"
# 两包覆盖情况保留清单；在新目录依次解包，不使用宿主 /emul。
rpm -qpl "$ACCEL_RPM" > "$LOG/clang-accel-$ACCEL_ARCH-files.txt"
rpm -qpl "$QEMU_ACCEL_RPM" > "$LOG/qemu-accel-$ACCEL_ARCH-files.txt"
for f in "$QEMU_ACCEL_RPM" "$ACCEL_RPM"; do
  (cd "$ACCEL_EXTRACT"; rpm2cpio "$f" | cpio -idm --quiet)
done
export EMUL="$ACCEL_EXTRACT/emul"
export ACCEL_LOADER="$EMUL/lib64/ld-linux-x86-64.so.2"
export ACCEL_LIBPATH="$EMUL/lib64:$EMUL/usr/lib64"
# 单包体积另解包统计，不能拿两包合并目录的 du 与历史 clang-accel 比。
stat -Lc '%s %n' "$ACCEL_RPM" | tee "$LOG/accel-$ACCEL_ARCH-rpm-bytes.txt"
rpm -qp --qf '[%{FILENAMES}\t%{FILESIZES}\n]' "$ACCEL_RPM" > "$LOG/accel-$ACCEL_ARCH-filesizes.tsv"
awk -F '\t' '{s+=$2} END {printf "%.0f\n",s}' "$LOG/accel-$ACCEL_ARCH-filesizes.tsv" \
 | tee "$LOG/accel-$ACCEL_ARCH-filesizes-total.txt"
(cd "$ACCEL_CLANG_ONLY"; rpm2cpio "$ACCEL_RPM" | cpio -idm --quiet)
du -sB1 "$ACCEL_CLANG_ONLY" | tee "$LOG/accel-$ACCEL_ARCH-du-blocks.txt"
du -sb "$ACCEL_CLANG_ONLY" | tee "$LOG/accel-$ACCEL_ARCH-du-apparent.txt"
```

### 6.2 使用已有本地该架构 GBS 根

需要组员已完成一次该架构 `gbs build -A "$ACCEL_ARCH" -B "$ARM_GBS_ROOT"`，且其新 Base 仓库确实安装了上述两包。可以复用组员在本地执行的 §2 下游包构建根，不要求在本任务新造一个 ARM 构建环境。准确根路径由 GBS 的标准布局和此次 `-B` 推导；先验证路径及已安装版本，再运行同一个闭合脚本：

```bash
export LOCAL_ARM_ROOT="$ARM_GBS_ROOT/local/BUILD-ROOTS/scratch.$ACCEL_ARCH.0"
test -d "$LOCAL_ARM_ROOT/emul"
# 在 x86_64 宿主读取 RPM 数据库，无须执行 ARM 根中的 rpm。
sudo rpm --root "$LOCAL_ARM_ROOT" -q --qf '%{NEVRA}\n' \
 "qemu-accel-x86_64-$ACCEL_ARCH" "clang-accel-x86_64-$ACCEL_ARCH" \
 | tee "$LOG/accel-$ACCEL_ARCH-local-installed.txt"
export EMUL="$LOCAL_ARM_ROOT/emul"
export ACCEL_LOADER="$EMUL/lib64/ld-linux-x86-64.so.2"
export ACCEL_LIBPATH="$EMUL/lib64:$EMUL/usr/lib64"
```

NEVRA 必须与本次新快照两包一致；旧缓存里的旧 accel 不算。若宿主 rpm 无法读取该数据库，记录错误，改选 §6.1 的两包解包方法，不假定查询成功。此方法只读已有根，不运行新的 GBS 构建。

### 6.3 两种方法共用的闭合检查

三种体积口径分开：RPM 压缩文件、头 `FILESIZES` 合计、解包 du。历史 path-bytes 合计是 regular+链接文本（目录不计），不能充当历史 du 或未经复算的 FILESIZES。本次从既有逐文件记录复算的头 FILESIZES 合计为旧 **239,912,044 B**、新 **2,756,647,372 B**，恰与这两个样本的 path-bytes 相等，计算来源和条目数见 [估算文件的 historical_rpm_filesizes_totals](52_hybrid_link_evidence/accel-alias-savings-estimate.json)。历史头原始值可从 [old tsv](qb_1199098_vs_1178133/size_attribution/raw/old_armv7l_clang-accel-x86_64-armv7l_rpm_files.tsv)、[new tsv](qb_1199098_vs_1178133/size_attribution/raw/new_armv7l_clang-accel-x86_64-armv7l_rpm_files.tsv) 复算，保留表头和字段定义。

使用上一步明确得到的 `$EMUL`、`$ACCEL_LOADER`、`$ACCEL_LIBPATH`，在组员 x86_64 服务器上执行；loader 和库搜索路径必须位于该目录内。不能把宿主库或另一个构建根的库作为闭合依据：

```bash
python3 - <<'PY' > "$LOG/accel-$ACCEL_ARCH-closure.json"
import json,os,pathlib,subprocess
root=pathlib.Path(os.environ['EMUL']).resolve(); loader=os.environ['ACCEL_LOADER']
assert pathlib.Path(loader).is_file(),loader
assert pathlib.Path(loader).resolve().is_relative_to(root), 'loader escapes emul'
for directory in os.environ['ACCEL_LIBPATH'].split(':'):
    assert directory and pathlib.Path(directory).is_dir(), 'missing library directory: '+directory
    assert pathlib.Path(directory).resolve().is_relative_to(root), 'library path escapes emul'
env={k:v for k,v in os.environ.items() if not k.startswith('LD_')}
env['LC_ALL']='C'
rows=[]; failed=False
for p in sorted(root.rglob('*')):
    if p.is_symlink() and not p.resolve().is_relative_to(root):
        rows.append({'path':str(p),'status':'FAIL_SYMLINK_OUTSIDE_EMUL'}); failed=True; continue
    if not p.is_file(): continue
    with p.open('rb') as f: magic=f.read(4)
    if magic!=b'\x7fELF': continue
    row={'path':str(p)}
    h=subprocess.run(['readelf','-hW',str(p)],capture_output=True,text=True,env=env)
    d=subprocess.run(['readelf','-dW',str(p)],capture_output=True,text=True,env=env)
    row.update(header=h.stdout,dynamic=d.stdout,readelf_errors=h.stderr+d.stderr)
    if h.returncode or d.returncode:
        row['status']='FAIL_READELF'; failed=True
    elif 'Advanced Micro Devices X86-64' not in h.stdout:
        row['status']='ANALYSIS_PENDING_OTHER_MACHINE'; failed=True
    elif '(NEEDED)' not in d.stdout:
        row['status']='NO_NEEDED' # 静态 ELF/无依赖 DSO；仍有 header/dynamic 证据
    else:
        r=subprocess.run([loader,'--library-path',os.environ['ACCEL_LIBPATH'],'--list',str(p)],
                         capture_output=True,text=True,timeout=30,env=env)
        row.update(exit=r.returncode,stdout=r.stdout,stderr=r.stderr)
        # 已解析到本次 EMUL 外的库直接失败，不能让宿主库掩盖缺包。
        resolved=[line.split('=>',1)[1].strip().split()[0]
                  for line in r.stdout.splitlines() if '=>' in line and 'not found' not in line]
        outside=[s for s in resolved if s.startswith('/') and
                 not os.path.realpath(s).startswith(str(root.resolve())+'/')]
        row['outside_emul']=outside
        row['status']='PASS' if r.returncode==0 and 'not found' not in r.stdout+r.stderr and not outside else 'FAIL_CLOSURE'
        failed |= row['status']!='PASS'
    rows.append(row)
assert rows,'no ELF inspected'
print(json.dumps({'status':'FAIL' if failed else 'PASS','elf_paths':len(rows),'results':rows},indent=2))
raise SystemExit(1 if failed else 0)
PY
```

保存全部 ELF 清单与旧 [107 工具路径映射](52_hybrid_link_evidence/accel-tool-map.csv) 对照，增删逐项解释。脚本遍历整个 `$EMUL`，因此包含 libLTO/LLVMgold、libLLVM/libclang-cpp 及其他加速包的 DSO；额外架构或无法解析的依赖不自动豁免。新混合工具应能从 accel 包集合找到所需 libLLVM/libclang-cpp，并由实际 loader/RUNPATH 解析。来源包/NEVRA 使用 §6.1 的两包文件清单与包头，或 §6.2 的本地根数据库查询留证。已有旧动态时期的两库路径与 qemu-accel 自动收依赖逻辑见 [设计报告 §6](52_hybrid_link_tizen_base.md#6-clang-accel-影响)，不能替代本次闭合检查。

## 7. 预期结果和回传

| 检查 | 本次预期 / 已有证据 | 性质与来源 |
|---|---|---|
| 分支身份 | 6e9d4f2b，tree 80a6fd23…，与 cef4d90 内容相同 | [分支身份](52_hybrid_sandbox_evidence/a1-identity.json)、[推送原文](52_hybrid_sandbox_evidence/a2-push.txt) |
| 图与 NEEDED | 188 目标，五类 3/5/29/108/43；缺预期 NEEDED 待分析 | 本次配置图与 v2 自检；新 RPM 实际 NEEDED 待组员执行 |
| 架构隔离 | 两 ARM `%build/%install` 与基线同字节 | [macro-comparison.json](52_hybrid_link_evidence/macro-comparison.json) |
| 包/正确性 | 22 RPM；归档 native/full index；工具与下游正常 | 9 月试构建 22 RPM、30/30 TU 同字节，[docs/22 §5、§6.2](22_hybrid_link_trial.md)；**旧源码参考，不是本次实测** |
| LLVM 构建耗时 | 旧 5686 s，1199098 关联 Base 29864 s；本次填实测 | [llvm_builds.csv](qb_1199098_vs_1178133/llvm_builds.csv)；输入/机器不同，只作参考 |
| armv7l accel RPM | 54,806,369 → 659,624,309 B；本次填实测 | [package_summary.csv](qb_1199098_vs_1178133/size_attribution/package_summary.csv) |
| armv7l accel path-bytes | 239,912,044 → 2,756,647,372 B | 同上；不是 du，也不替代 FILESIZES 合计 |
| 准备/包时长 | 六格逐项填，缺旧 aarch64 Unified 日志记未获取 | §2 第 4 步对应日志；不得用包耗时解释全部准备耗时 |
| 峰值内存 | 填 QB 可见口径/本地 time -v 最大 RSS；不可见写未获取 | 本次尚未构建，无预测数值 |

回传目录至少包含：检出身份、QB ID/项目/源码和快照/buildconfig、完整构建日志、阶段时间及内存口径、22 RPM 清单/字节/SHA、全部 NEEDED 结果及待分析处置、归档 JSON、别名/ldd/smoke 日志、两 accel 体积和闭合、六格下游对照。任何失败保留原文与退出码，不填推测结果。配置级证据、历史实测、新构建实测分开写。

## 8. 风险与后续边界

- **BOLT 与 356949 合并顺序**：变量块的 `$BOLT_BRANCH` 尚未合入，它与本补丁修改同一段 x86_64 CMake 参数；谁后合入谁变基。在混合配置上必须重新认证 BOLT 的 dry-run 任务白名单，因为 llvm-bolt 与 libLLVM.so 相关构建图会变化。356949 合入后同样须变基、检查配方/宏/Source 组合并重新核对。本指南登记风险，不访问或修改该会话资产。
- **accel 别名可选优化**：qemu-accel 的 `cp -aL` 展开 lld/ld.lld 与 llvm-ar/llvm-ranlib/llvm-lib/llvm-dlltool，末尾只恢复 clang 组软链接；证据为 [spec 第 382 行](qb_1199098_vs_1178133/size_attribution/raw/qemu-accel_new_armv7l_retry.spec#L382)、[第 617–643 行](qb_1199098_vs_1178133/size_attribution/raw/qemu-accel_new_armv7l_retry.spec#L617)。`%fdupes` 没有使此清单中的六项变成硬链接：每项 nlink=1、不同 RPM inode，同组 SHA 相同。[估算及逐文件来源](52_hybrid_link_evidence/accel-alias-savings-estimate.json)：保留 lld、llvm-ar 两份实体，将余下四项改成相对软链接，冗余 regular 字节为 `84,409,520 + 3×14,832,464 = 128,906,912`；扣除链接文本 `3+3×7=24`，**按现有 armv7l accel 清单估算可减少 128,906,888 B（122.94 MiB）path-bytes**。这是后续改 qemu-accel 的可选优化，**不在混合补丁中**；不预测压缩 RPM/磁盘块节省，aarch64 未取得相同清单，新混合产物还需重算。
- 动态 LLVM 目标仍可能链接工具私有 `.a`，共享库生产者也会消费组件 `.a`；两者均不能机械地按“链接行出现 .a”判失败。按共享输入/NEEDED 和包范围分别检查。
- QB/本地快照、硬件、并发和缓存不同会影响耗时；本轮没有运行构建，不承诺体积或耗时降低的数值。按实际执行项目交付结论；只有六格不能声称额外的原生 x86_64/SDK 工具专项全部通过。
