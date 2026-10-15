# 混合链接组员验证指南 v2

状态（2026-10-15）：**PM 已通过补丁 cef4d90；本版只修订指南、期望表与检查脚本。Quickbuild 为主路径，本地 GBS 仅作可选正确性验证。** 本轮没有运行构建或新 RPM 验收。补丁 tree 保持 `80a6fd231c4564a3b762f4ec288cf2c41f9d2e20`，配置级证据见 [设计报告](52_hybrid_link_tizen_base.md)。

本版文件身份和检查摘要见 [validation-v2-checks.json](52_hybrid_link_evidence/validation-v2-checks.json)；原 `delivery-manifest.json` 保留为 v1 交付记录，不用于核对本版指南的 SHA。

## 0. 一次填写的变量块

在组员验证终端执行；切换到验证 worker 时，将同一块中的路径改成该机的挂载位置并重新导出。账号、工作目录、仓库、日志与产物位置集中在这里维护，正文不再另设一套。尖括号值必须替换后执行。Base/Unified 默认值取自对照 QB 的日志，**不是 latest**；选择规则与失效处理见 §3。Quickbuild 新构建的输入/输出快照也要回填到本块和结果表。

```bash
set -euo pipefail
export W="$HOME/Toolchain/development/llvm-optimize"
# 本机工作目录示例：/home/linhao/Toolchain/development/llvm-optimize
export GERRIT_USER='<组员自己的 Gerrit 账号>'
# 本机账号示例：lhmax2025；不得直接照抄为组员账号。
export GERRIT_REPO="ssh://${GERRIT_USER}@review.tizen.org:29418/platform/upstream/llvm"
export SANDBOX_BRANCH="sandbox/${GERRIT_USER}/hybrid_link"
export BOLT_BRANCH='sandbox/lhmax2025/bolt_pgo' # 风险登记用；不检出、不修改。
export BASE=67619ec8bbbac7238a6cfc33a481ccfbcd12206f
export EXPECTED_TREE=80a6fd231c4564a3b762f4ec288cf2c41f9d2e20
export PATCH="$W/docs/52_hybrid_link.patch"
export PATCH_SHA=30e90aa305dd1e5ae237adaa19b27996a722b53ef481aa8ba53f510cb3f9c678
export EVIDENCE="$W/docs/52_hybrid_link_evidence"
export EXPECTATIONS="$EVIDENCE/needed-expectations-v2.json"
export QB_REF="$W/docs/qb_1199098_vs_1178133"
export S="$W/temp/llvm-hybrid52-team"
export G=/var/tmp/llvm-hybrid52-team-build
export LOG="$W/temp/hybrid52-team-validation-v2"
export INPUT_CONFIG="$W/gbs_llvm.conf"
export CONFIG="$LOG/inputs/gbs-hybrid.conf"
export BC="$LOG/inputs/project-buildconfig.conf" # 从本次 QB 项目导出的完整 buildconfig
export BASE_SNAPSHOT=tizen-base-toolchain_20261015.022255
export UNIFIED_SNAPSHOT=tizen-unified-toolchain_20260917.132101
export BASE_REPO="http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/${BASE_SNAPSHOT}/repos/standard/packages/"
export UNIFIED_REPO="http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/${UNIFIED_SNAPSHOT}/repos/standard/packages/"
export QB_LLVM_PROJECT='Tizen-Base-Toolchain/standard'
export QB_DOWNSTREAM_PROJECT='Tizen-Unified-Toolchain/standard'
export CONTROL_QB=1199098
export NEW_QB='<本次 QB ID>'
export NEW_BASE_SNAPSHOT='<重建 llvm 和 accel 后发布的具体 Base 快照>'
export NEW_UNIFIED_SNAPSHOT='<本次下游使用的具体 Unified 快照>'
export RPM_DIR="$LOG/rpms/x86_64" # QB 下载到这里；本地构建时改为 G 下的 RPMS/x86_64
export N="$LOG/extracted-llvm" # 22 包解包目录，只作文件检查，不能充当完整运行根
export TEST_ROOT='<已安装本次 RPM 和运行依赖的独立 x86_64 测试根>'
export SMOKE=/tmp/llvm52-smoke # 测试根内目录
export ARM_SYSROOT=/srv/tizen-sysroots/armv7l
export A64_SYSROOT=/srv/tizen-sysroots/aarch64
export ARM_GCC=/srv/tizen-cross/armv7l
export A64_GCC=/srv/tizen-cross/aarch64
export ACCEL_ARCH=armv7l # §6 分别改成 armv7l / aarch64，完整执行两遍
export ACCEL_RPM='<本次 clang-accel 对应架构 RPM 的绝对路径>'
export ACCEL_EXTRACT="$LOG/accel-${ACCEL_ARCH}"
export EMUL=/emul # 新 Base worker 的实际 accel 根
export ACCEL_LOADER="$EMUL/lib64/ld-linux-x86-64.so.2"
export ACCEL_LIBPATH="$EMUL/lib64:$EMUL/usr/lib64"
export HEAVY_LOCK="$W/../heavy-stage.lock"
export UNIT=llvm-hybrid52-team-v2
mkdir -p "$LOG/inputs"
```

`BASE_REPO`/`UNIFIED_REPO` 来源是 [1199098 quickbuild 原文 338–347 行](qb_1199098_vs_1178133/raw/1199098_quickbuild.txt#L338)。日志中 Unified 是注释掉的参考仓库，不据此声称它参与了每个包的依赖解析；运行时有效仓库集合以所选项目导出配置为准。Base LLVM 的 **29864 秒**来自关联 Base 构建日志，而非 Unified 的 llvm 重建，项目/版本/源码对应见 [llvm_builds.csv 第 2 行](qb_1199098_vs_1178133/llvm_builds.csv#L2)。

## 1. 应用补丁与身份

使用组员已有的 Git 身份，不在命令中覆盖作者或提交者。`git am` 保留补丁里的作者 Hao Lin，提交者取组员自己的 Git 配置。组员以自己的账号推 sandbox 时，提交者与账号不一致可能被 Gerrit 拒收；若身份未配置，先用组员本人姓名/邮箱配置该 checkout，不能套用补丁作者身份。

```bash
test "$GERRIT_USER" != '<组员自己的 Gerrit 账号>'
printf '%s  %s\n' "$PATCH_SHA" "$PATCH" | sha256sum -c -
test ! -e "$S"
git clone --no-checkout "$GERRIT_REPO" "$S"
git -C "$S" switch -c hybrid_link "$BASE"
git -C "$S" var GIT_COMMITTER_IDENT
git -C "$S" apply --check "$PATCH"
git -C "$S" am "$PATCH"
test "$(git -C "$S" rev-parse HEAD^{tree})" = "$EXPECTED_TREE"
test -z "$(git -C "$S" status --porcelain)"
git -C "$S" show -s --format=fuller HEAD | tee "$LOG/applied-commit.txt"
git -C "$S" rev-parse HEAD^{tree} | tee "$LOG/applied-tree.txt"
```

提交者与提交时间不同会改变 commit SHA，**tree 校验不变**。原补丁身份及七文件摘要见 [patch-identity.json](52_hybrid_link_evidence/patch-identity.json)，干净应用记录见 [fresh-apply.json](52_hybrid_link_evidence/fresh-apply.json)。356627 已在基线中；不重复叠加。遇到更新的配方先走 §8 变基核对，不能跳过 tree 门禁后继续冒用本表。

## 2. 主路径：Quickbuild 逐步清单

以下推送与 QB 操作由组员执行。本轮文档任务没有代为推送 Gerrit/sandbox。

1. **推个人 sandbox**。核对 §1 身份和 tree 后执行下面模板，记录远端分支与 commit。

   ```bash
   git -C "$S" push origin "HEAD:refs/heads/$SANDBOX_BRANCH"
   git -C "$S" ls-remote origin "refs/heads/$SANDBOX_BRANCH" | tee "$LOG/sandbox-head.txt"
   ```

2. **构建 x86_64 llvm**。在 `$QB_LLVM_PROJECT` 中选择 `$SANDBOX_BRANCH`，以与 `$CONTROL_QB` 关联的 Base llvm 构建相同的项目/仓库启动。核对所选 spec 为 `packaging/llvm.spec`，完整保存项目导出配置、buildconfig、实际源码 commit、输入仓库快照、RPM 版本和 worker 信息。记录总耗时、`%build` 与 `%install` 阶段耗时、转换 BEGIN–END；QB 能看到构建机峰值内存时记录数值/单位/口径，看不到则写“未获取”。总耗时与 **29864 秒**对照，并同时写两次输入及产出快照。阶段时间取阶段边界日志，不能把下载/准备时间算进 `%build`，也不能用总时长反推峰值内存。旧完整日志：[1199098 Base x86_64 llvm](qb_1199098_vs_1178133/raw/1199098_base_x86_64_llvm.txt)，阶段依据及旧 5686 秒见 [llvm_builds.csv](qb_1199098_vs_1178133/llvm_builds.csv)。下载本次 22 个 RPM，执行 §4–§5。
3. **重建两个 accel**。把该 llvm 产物提供给 qemu-accel 的 x86_64 工具输入，分别生成 armv7l、aarch64 的 clang-accel；保存 qemu-accel 构建日志中所消费的 llvm/clang/libllvm NEVRA、仓库 URL 和 SHA，不能只凭版本主号认定用了新包。记录 clang-accel 的 RPM 文件字节数、RPM 头 `FILESIZES` 合计、解包 `du -sB1` 与 `du -sb`，命令见 §6。与 [SIZE_FINDINGS.md](qb_1199098_vs_1178133/size_attribution/SIZE_FINDINGS.md)、[package_summary.csv](qb_1199098_vs_1178133/size_attribution/package_summary.csv) 同口径比较；当前逐文件基线只有 armv7l，aarch64 不填写伪造基线。
4. **下游六格验证**。以新 Base/accel，在 armv7l、aarch64 各构建 zlib、libpng、libinput，锁定旧日志同一源码/配方，记录差异。zlib 对照来自 Base，libpng/libinput 来自 Unified，保持各自项目。每格记录成功/失败、实际安装的 clang/accel 版本、buildroot 准备时间、包构建时间及日志行号。准备时间定义为日志开始到第一条 `%prep`，包构建时间为 `%prep` 到 finished，另保留 started–finished 总时长；新旧按同一边界重新取数，不能把页面 Profiling 时长直接当准备时间。旧日志分秒时间戳的精度为秒，缺边界则“未获取”。

   | 包 | armv7l 对照 | aarch64 对照 |
   |---|---|---|
   | zlib | `raw/{1199098,1178133}_base_armv7l_zlib.txt` | `raw/{1199098,1178133}_base_aarch64_zlib.txt` |
   | libpng | `raw/{1199098,1178133}_armv7l_libpng-1.6.44-0.txt` | 未获取；既有这批 Unified 只有 armv7l，仍须做新 aarch64 验证 |
   | libinput | `raw/{1199098,1178133}_armv7l_libinput-1.31.3-0.txt` | 未获取；同上 |

   表中路径均相对 `$QB_REF`。来源范围见 [FINDINGS.md](qb_1199098_vs_1178133/FINDINGS.md)“下游实际使用的编译器与链接器”“两次构建是否同条件”。为每一格保存 `arch,package,source_commit,base_snapshot,unified_snapshot,accel_nevra,result,root_prepare_s,package_build_s,total_s,peak_memory,log_evidence`，未获取项注明原因。
5. **accel 依赖闭合**。在两种架构的新 worker 上分别执行 §6，检查所有实际 accel ELF，包括工具与 DSO。不能只检查 clang，也不能只以包内存在同名共享库判闭合。依赖缺失、下游构建失败或待分析项未闭合，均不能提交“全项 PASS”。

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

### 3.2 独立根与资源

本地仅证明正确性；与 QB 的机器、并发、缓存不同，不作耗时收益结论。配方仍为 Ninja 6 / compile pool 6 / link pool 2，不能无记录换成 9 月的 4/4/1。沿用独立根、显式 llvm.spec、debuginfo `-j4` 命令结构。准入 MemAvailable ≥16 GiB；构建文件系统可用 ≥263.758319 GiB，且扣除历史预算 219.798599 GiB 后仍 ≥30 GiB。18 GiB cap、swap0，nice19/ionice3；历史 6/6/2 撞峰见 [docs/49 第二轮报告](49_x86_build_round2_result.md)。不足则用 QB，不改门槛硬跑。

```bash
test ! -e "$G"
exec 9>"$HEAVY_LOCK"
flock 9
python3 - <<'PY'
import os,pathlib
m=int(next(s.split()[1] for s in pathlib.Path('/proc/meminfo').read_text().splitlines()
           if s.startswith('MemAvailable:')))*1024
v=os.statvfs(pathlib.Path(os.environ['G']).parent); free=v.f_bavail*v.f_frsize
assert m>=16*1024**3, ('MemAvailable',m)
assert free>=263.758319*1024**3 and free-219.798599*1024**3>=30*1024**3, ('disk',free)
print('ADMISSION_PASS',m,free)
PY
# 先在另一个终端启动下方监控（同一变量块），再执行构建。
set +e
/usr/bin/time -v -o "$LOG/time-v.txt" \
 systemd-run --user --scope --unit="$UNIT" -p MemoryMax=18G -p MemorySwapMax=0 \
 nice -n 19 ionice -c3 \
 gbs -c "$CONFIG" build -A x86_64 -B "$G" --threads 1 --include-all \
 --spec llvm.spec --define '_smp_mflags -j4' -D "$BC" "$S" \
 2>&1 | tee "$LOG/build.log"
rc=(${PIPESTATUS[@]})
set -e
printf 'build=%s tee=%s\n' "${rc[0]}" "${rc[1]}" | tee "$LOG/exit.txt"
test "${rc[0]}" -eq 0 && test "${rc[1]}" -eq 0
flock -u 9
```

监控每 2 秒记录 cgroup 峰值、进程 VmHWM、磁盘；宿主可用内存 <2 GiB 或磁盘 <30 GiB 则终止整个 scope。构建结束退出；启动失败没有产生 scope 时 Ctrl-C 收尾。退出前未取到最终 `memory.peak` 时只报“最后采样值”，`time -v` 不替代 cgroup 峰值。

```bash
python3 - <<'PY'
import json,os,pathlib,subprocess,time
seen=False
while True:
    q=subprocess.run(['systemctl','--user','show',os.environ['UNIT']+'.scope',
        '-p','ControlGroup','--value'],capture_output=True,text=True)
    cg=q.stdout.strip(); root=pathlib.Path('/sys/fs/cgroup'+cg) if cg else None
    if not root or not root.exists():
        if seen: break
        time.sleep(2); continue
    seen=True
    m=int(next(s.split()[1] for s in pathlib.Path('/proc/meminfo').read_text().splitlines()
               if s.startswith('MemAvailable:')))*1024
    v=os.statvfs(pathlib.Path(os.environ['G']).parent); free=v.f_bavail*v.f_frsize
    row=dict(time=time.time(),MemAvailable=m,disk_available=free,processes=[])
    for key in ['memory.current','memory.peak','memory.events']:
        try: row[key]=(root/key).read_text()
        except FileNotFoundError: pass
    for f in root.rglob('cgroup.procs'):
        try: pids=f.read_text().split()
        except FileNotFoundError: continue
        for pid in pids:
            try:
                lines=pathlib.Path('/proc',pid,'status').read_text().splitlines()
                row['processes'].append(dict(pid=pid,status=[s for s in lines
                    if s.startswith(('Name:','VmRSS:','VmHWM:'))]))
            except FileNotFoundError: pass
    with open(pathlib.Path(os.environ['LOG'])/'resources.jsonl','a') as f:
        f.write(json.dumps(row)+'\n')
    if m<2*1024**3 or free<30*1024**3:
        subprocess.run(['systemctl','--user','kill','--signal=SIGTERM',os.environ['UNIT']+'.scope'])
        time.sleep(3)
        subprocess.run(['systemctl','--user','kill','--signal=SIGKILL',os.environ['UNIT']+'.scope'])
        raise SystemExit('RESOURCE_FLOOR_ABORT')
    time.sleep(2)
PY
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

在 `$TEST_ROOT` 安装新 RPM 与全部依赖后，按 `needed-results.json` 中成功识别的 ELF 路径逐个运行根内 `ldd`，保存全文；动态 ELF 的返回码须 0 且无 `not found`，不能把解包根内有库文件当运行闭合。三组“静态”仅指 LLVM 组件，通常仍有 libc 等 NEEDED。

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

```bash
for f in "${rpms[@]}"; do
  name=$(rpm -qp --qf '%{NAME}' "$f")
  rpm -qpl "$f" | awk '/\.a$/ {print}' > "$LOG/$name.archives"
  case "$name" in
    *devel*|compiler-rt) ;; # compiler-rt 的 45 个运行库保留，不是 LLVM 开发库
    *) test ! -s "$LOG/$name.archives" ;;
  esac
done
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os,sys,pathlib,json
sys.path.insert(0,str(pathlib.Path(os.environ['W'])/'tools'))
from inspect_llvm_archives import inspect
log=pathlib.Path(os.environ['LOG']); root=pathlib.Path(os.environ['N'])
paths=(log/'llvm-static-devel.archives').read_text().splitlines()
assert len(paths)==225,len(paths)
with (log/'archives.jsonl').open('w') as f:
    for name in paths:
        r=inspect(root/name.lstrip('/'))
        assert not r['thin'] and r['bitcode']==0 and r['other']==0,r['path']
        assert r['machine']==r['member_count'] and r['index_equals_machine_symbols'],r['path']
        assert all(not m['debug_sections'] for m in r['members']),r['path']
        f.write(json.dumps(r)+'\n')
print('225 native archives / full index / no debug: PASS')
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

交叉验证环境须安装本次 x86_64 clang/clang++，并提供与新快照对应、含 libc crt、libstdc++ 头/库与 GCC runtime 的两目标 sysroot。在该环境执行下列命令（同一变量块、已有 hello 源码），保存日志；缺 sysroot 记未验证，不能仅产出 `.o` 冒充链接成功。

```bash
cd "$SMOKE"
for dir in "$ARM_SYSROOT" "$A64_SYSROOT" "$ARM_GCC" "$A64_GCC"; do test -d "$dir"; done
for lang in c cc; do
  driver=clang; test "$lang" = c || driver=clang++
  "$driver" --target=armv7l-tizen-linux-gnueabi --sysroot="$ARM_SYSROOT" \
    --gcc-toolchain="$ARM_GCC" -fuse-ld=lld "hello.$lang" -o "hello-armv7l-$lang"
  "$driver" --target=aarch64-tizen-linux-gnu --sysroot="$A64_SYSROOT" \
    --gcc-toolchain="$A64_GCC" -fuse-ld=lld "hello.$lang" -o "hello-aarch64-$lang"
  readelf -h "hello-armv7l-$lang" "hello-aarch64-$lang"
done
```

把产物交对应 ARM worker 执行，C/C++ 均输出 `hello`、退出 0；记录 ELF Machine、实际工具路径、sysroot 身份与运行日志。zlib/libpng/libinput 六格构建是主路径的真实负载验证，不能由这里的 hello 替代。

## 6. 两架构 accel 体积与全部 ELF 依赖闭合

每种架构分别设置 §0 的 `ACCEL_ARCH`、`ACCEL_RPM`、`ACCEL_EXTRACT`，重复以下命令，不得重用上一架构的解包目录。

```bash
test ! -e "$ACCEL_EXTRACT"
mkdir -p "$ACCEL_EXTRACT"
stat -Lc '%s %n' "$ACCEL_RPM" | tee "$LOG/accel-$ACCEL_ARCH-rpm-bytes.txt"
sha256sum "$ACCEL_RPM" > "$LOG/accel-$ACCEL_ARCH-rpm.sha256"
rpm -qp --qf '%{NEVRA}\n' "$ACCEL_RPM" > "$LOG/accel-$ACCEL_ARCH-nevra.txt"
rpm -qp --qf '[%{FILENAMES}\t%{FILESIZES}\n]' "$ACCEL_RPM" > "$LOG/accel-$ACCEL_ARCH-filesizes.tsv"
awk -F '\t' '{s+=$2} END {printf "%.0f\n",s}' "$LOG/accel-$ACCEL_ARCH-filesizes.tsv" \
  | tee "$LOG/accel-$ACCEL_ARCH-filesizes-total.txt"
(cd "$ACCEL_EXTRACT"; rpm2cpio "$ACCEL_RPM" | cpio -idm --quiet)
du -sB1 "$ACCEL_EXTRACT" | tee "$LOG/accel-$ACCEL_ARCH-du-blocks.txt"
du -sb "$ACCEL_EXTRACT" | tee "$LOG/accel-$ACCEL_ARCH-du-apparent.txt"
```

三种体积口径分开：RPM 压缩文件、头 `FILESIZES` 合计、解包 du。历史 path-bytes 合计是 regular+链接文本（目录不计），不能充当历史 du 或未经复算的 FILESIZES。本次从既有逐文件记录复算的头 FILESIZES 合计为旧 **239,912,044 B**、新 **2,756,647,372 B**，恰与这两个样本的 path-bytes 相等，计算来源和条目数见 [估算文件的 historical_rpm_filesizes_totals](52_hybrid_link_evidence/accel-alias-savings-estimate.json)。历史头原始值可从 [old tsv](qb_1199098_vs_1178133/size_attribution/raw/old_armv7l_clang-accel-x86_64-armv7l_rpm_files.tsv)、[new tsv](qb_1199098_vs_1178133/size_attribution/raw/new_armv7l_clang-accel-x86_64-armv7l_rpm_files.tsv) 复算，保留表头和字段定义。

在**实际新 Base worker** 上执行依赖闭合（本机解释器须能执行 x86_64 accel，不能把宿主 `/usr/lib` 当作 accel 的库）：

```bash
python3 - <<'PY' > "$LOG/accel-$ACCEL_ARCH-closure.json"
import json,os,pathlib,subprocess
root=pathlib.Path(os.environ['EMUL']); loader=os.environ['ACCEL_LOADER']
assert pathlib.Path(loader).is_file(),loader
rows=[]; failed=False
for p in sorted(root.rglob('*')):
    if not p.is_file(): continue
    with p.open('rb') as f: magic=f.read(4)
    if magic!=b'\x7fELF': continue
    row={'path':str(p)}
    h=subprocess.run(['readelf','-hW',str(p)],capture_output=True,text=True)
    d=subprocess.run(['readelf','-dW',str(p)],capture_output=True,text=True)
    row.update(header=h.stdout,dynamic=d.stdout,readelf_errors=h.stderr+d.stderr)
    if h.returncode or d.returncode:
        row['status']='FAIL_READELF'; failed=True
    elif 'Advanced Micro Devices X86-64' not in h.stdout:
        row['status']='ANALYSIS_PENDING_OTHER_MACHINE'; failed=True
    elif '(NEEDED)' not in d.stdout:
        row['status']='NO_NEEDED' # 静态 ELF/无依赖 DSO；仍有 header/dynamic 证据
    else:
        r=subprocess.run([loader,'--library-path',os.environ['ACCEL_LIBPATH'],'--list',str(p)],
                         capture_output=True,text=True,timeout=30)
        row.update(exit=r.returncode,stdout=r.stdout,stderr=r.stderr)
        # 已解析到 /emul 外的库也须分析，不能让宿主库掩盖缺包。
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

保存全部 ELF 清单与旧 [107 工具路径映射](52_hybrid_link_evidence/accel-tool-map.csv) 对照，增删逐项解释。脚本遍历整个 `$EMUL`，因此包含 libLTO/LLVMgold、libLLVM/libclang-cpp 及其他加速包的 DSO；额外架构或无法解析的依赖不自动豁免。新混合工具应能从 accel 包集合找到所需 libLLVM/libclang-cpp，并由实际 loader/RUNPATH 解析。来源包/NEVRA 可用 worker 的 `rpm -qf <路径>` 留证。已有旧动态时期的两库路径与 qemu-accel 自动收依赖逻辑见 [设计报告 §6](52_hybrid_link_tizen_base.md#6-clang-accel-影响)，不能替代本次闭合检查。

## 7. 预期结果和回传

| 检查 | 本次预期 / 已有证据 | 性质与来源 |
|---|---|---|
| 补丁身份 | cef4d90，tree 80a6fd23…，7 文件 | 本次配置级 [patch identity](52_hybrid_link_evidence/patch-identity.json) |
| 图与 NEEDED | 188 目标，五类 3/5/29/108/43；缺预期 NEEDED 待分析 | 本次配置图与 v2 自检；新 RPM 实际 NEEDED 待组员执行 |
| 架构隔离 | 两 ARM `%build/%install` 与基线同字节 | [macro-comparison.json](52_hybrid_link_evidence/macro-comparison.json) |
| 包/正确性 | 22 RPM；归档 native/full index；工具与下游正常 | 9 月试构建 22 RPM、30/30 TU 同字节，[docs/22 §4](22_hybrid_link_trial.md)；**旧源码参考，不是本次实测** |
| LLVM 构建耗时 | 旧 5686 s，1199098 关联 Base 29864 s；本次填实测 | [llvm_builds.csv](qb_1199098_vs_1178133/llvm_builds.csv)；输入/机器不同，只作参考 |
| armv7l accel RPM | 54,806,369 → 659,624,309 B；本次填实测 | [package_summary.csv](qb_1199098_vs_1178133/size_attribution/package_summary.csv) |
| armv7l accel path-bytes | 239,912,044 → 2,756,647,372 B | 同上；不是 du，也不替代 FILESIZES 合计 |
| 准备/包时长 | 六格逐项填，缺旧 aarch64 Unified 日志记未获取 | §2 第 4 步对应日志；不得用包耗时解释全部准备耗时 |
| 峰值内存 | 填 QB 可见口径/本地 cgroup 采样；不可见写未获取 | 本次尚未构建，无预测数值 |

回传目录至少包含：应用身份、QB ID/项目/源码和快照/buildconfig、完整构建日志、阶段时间及内存口径、22 RPM 清单/字节/SHA、全部 NEEDED 结果及待分析处置、归档 JSON、别名/ldd/smoke 日志、两 accel 体积和闭合、六格下游对照。任何失败保留原文与退出码，不填推测结果。配置级证据、历史实测、新构建实测分开写。

## 8. 风险与后续边界

- **BOLT 与 356949 合并顺序**：变量块的 `$BOLT_BRANCH` 尚未合入，它与本补丁修改同一段 x86_64 CMake 参数；谁后合入谁变基。在混合配置上必须重新认证 BOLT 的 dry-run 任务白名单，因为 llvm-bolt 与 libLLVM.so 相关构建图会变化。356949 合入后同样须变基、检查配方/宏/Source 组合并重新核对。本指南登记风险，不访问或修改该会话资产。
- **accel 别名可选优化**：qemu-accel 的 `cp -aL` 展开 lld/ld.lld 与 llvm-ar/llvm-ranlib/llvm-lib/llvm-dlltool，末尾只恢复 clang 组软链接；证据为 [spec 第 382 行](qb_1199098_vs_1178133/size_attribution/raw/qemu-accel_new_armv7l_retry.spec#L382)、[第 617–643 行](qb_1199098_vs_1178133/size_attribution/raw/qemu-accel_new_armv7l_retry.spec#L617)。`%fdupes` 没有使此清单中的六项变成硬链接：每项 nlink=1、不同 RPM inode，同组 SHA 相同。[估算及逐文件来源](52_hybrid_link_evidence/accel-alias-savings-estimate.json)：保留 lld、llvm-ar 两份实体，将余下四项改成相对软链接，冗余 regular 字节为 `84,409,520 + 3×14,832,464 = 128,906,912`；扣除链接文本 `3+3×7=24`，**按现有 armv7l accel 清单估算可减少 128,906,888 B（122.94 MiB）path-bytes**。这是后续改 qemu-accel 的可选优化，**不在混合补丁中**；不预测压缩 RPM/磁盘块节省，aarch64 未取得相同清单，新混合产物还需重算。
- 动态 LLVM 目标仍可能链接工具私有 `.a`，共享库生产者也会消费组件 `.a`；两者均不能机械地按“链接行出现 .a”判失败。按共享输入/NEEDED 和包范围分别检查。
- QB/本地快照、硬件、并发和缓存不同会影响耗时；本轮没有运行构建，不承诺体积或耗时降低的数值。只有 §2–§6 新产物验证完成后才能交付该次验证结论。
