# 混合链接完整构建验证指南（交组员执行）

状态：**本机仅配置级核对完成；以下构建、安装和运行命令尚未执行，先等 PM review。**
精确基线 `67619ec8bbbac7238a6cfc33a481ccfbcd12206f`；补丁与配置证据见 [52_hybrid_link_tizen_base.md](52_hybrid_link_tizen_base.md)。本轮不包含 356949。以下命令中的用户名为本机示例；异机应整体替换工作区前缀，并在报告中记录，不混用他人的现有构建根。

## 1. 应用与构建输入

在组员的独立 checkout 执行，不在原 `W/llvm` 或其他会话的树上操作：

```bash
set -euo pipefail
W=/home/linhao/Toolchain/development/llvm-optimize
S=$W/temp/llvm-hybrid52-team
BASE=67619ec8bbbac7238a6cfc33a481ccfbcd12206f
PATCH=$W/docs/52_hybrid_link.patch
sha256sum "$PATCH"
# 预期 30e90aa305dd1e5ae237adaa19b27996a722b53ef481aa8ba53f510cb3f9c678

git clone --no-checkout \
  ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm "$S"
git -C "$S" switch -c hybrid_link "$BASE"
git -C "$S" apply --check "$PATCH"
git -C "$S" -c user.name='Hao Lin' -c user.email=hao.lin@samsung.com am "$PATCH"
test "$(git -C "$S" rev-parse HEAD^{tree})" = 80a6fd231c4564a3b762f4ec288cf2c41f9d2e20
test -z "$(git -C "$S" status --porcelain)"
git -C "$S" show --stat --oneline HEAD
```

应用后的 commit 时间可能不同，**tree 必须相同**。补丁原提交为 `cef4d90b478597e20ff105591af3c5f4417363f1`。七文件清单/摘要见 [patch-identity.json](52_hybrid_link_evidence/patch-identity.json)。两份已上传的归档修复补丁无需再叠加；356627 已在 BASE 中。

### 仓库预检（必须先通过）

本轮实读 W/gbs_llvm.conf 的 Base 20261001.092726 已 404；Unified 20260814.092727 为 200。**不能直接用当前配置启动成功的完整构建**。由组员/PM 确定可用的具体 Base 快照并更新其构建配置后，再执行下面预检和构建；本指南不自行指定替换仓库，也不把配置生成结果当成新快照验证。若走 Quickbuild，则使用该项目的仓库并记录项目/快照。

```bash
python3 - <<'PY'
import configparser, urllib.request, hashlib
c = configparser.ConfigParser()
c.read('/home/linhao/Toolchain/development/llvm-optimize/gbs_llvm.conf')
for name in ['repo.base-standard', 'repo.unified-standard']:
    url = c[name]['url'].rstrip('/') + '/repodata/repomd.xml'
    with urllib.request.urlopen(url, timeout=30) as r:
        assert r.status == 200
        data = r.read()
    print(name, url, hashlib.sha256(data).hexdigest())
PY
sha256sum "$W/gbs_llvm.conf"
```

历史宏配置可取本工作区 `temp/hybrid-trial-20260922/run/buildconfig.conf`，SHA `1e7610b6a922d27b80eb59c1c78bdf716f7de2e8e24700e0ee7c62522739ed52`（docs/22）。异机拿不到此文件应从所选项目导出实际 buildconfig 并记录差异，不能创建假的空文件。

## 2. x86_64 完整构建命令

沿用 9 月命令结构：GBS x86_64、独立 `-B`、threads=1、debuginfo `_smp_mflags -j4`、明确 buildconfig，补显式 `--spec llvm.spec` 防止误选 libcxx-runtimes。**当前补丁仍保留最新 spec 的 Ninja 6、compile pool 6、link pool 2**，9 月的 4/4/1 不作为本次产物配置冒用。本机历史 6/6/2 曾撞内存保护（docs/49_x86_build_round2_result.md），团队应在满足容量的服务器验证；不得无记录改变配方。

```bash
W=/home/linhao/Toolchain/development/llvm-optimize
S=$W/temp/llvm-hybrid52-team
G=/var/tmp/llvm-hybrid52-team-build
LOG=$W/temp/hybrid52-team-validation
BC=$W/temp/hybrid-trial-20260922/run/buildconfig.conf
mkdir -p "$LOG"
test ! -e "$G"
test "$(sha256sum "$BC" | cut -d' ' -f1)" = \
  1e7610b6a922d27b80eb59c1c78bdf716f7de2e8e24700e0ee7c62522739ed52
# 准入：MemAvailable >=16GiB；构建所在文件系统按既有全构建预算
# 219.798599GiB×1.2=263.758319GiB，且预计写完仍 >=30GiB。
python3 - <<'PY_ADMISSION'
import os, pathlib
m=int(next(x.split()[1] for x in pathlib.Path('/proc/meminfo').read_text().splitlines()
           if x.startswith('MemAvailable:')))*1024
v=os.statvfs('/var/tmp'); free=v.f_bavail*v.f_frsize
assert m>=16*1024**3, ('MemAvailable',m)
assert free>=263.758319*1024**3 and free-219.798599*1024**3>=30*1024**3,('disk',free)
print('ADMISSION_PASS',m,free)
PY_ADMISSION
free -b | tee "$LOG/memory-before.txt"
df -B1 /var/tmp | tee "$LOG/disk-before.txt"

set +e
/usr/bin/time -v -o "$LOG/time-v.txt" \
  systemd-run --user --scope --unit=llvm-hybrid52-team \
    -p MemoryMax=18G -p MemorySwapMax=0 \
  nice -n 19 ionice -c3 \
  gbs -c "$W/gbs_llvm.conf" build -A x86_64 \
    -B "$G" --threads 1 --include-all --spec llvm.spec \
    --define '_smp_mflags -j4' -D "$BC" "$S" \
  2>&1 | tee "$LOG/build.log"
rc=(${PIPESTATUS[@]})
set -e
printf 'build=%s tee=%s\n' "${rc[0]}" "${rc[1]}" | tee "$LOG/exit.txt"
test "${rc[0]}" -eq 0 && test "${rc[1]}" -eq 0
```

服务器上可按团队批准的资源规则运行。若仍在本机执行，应先启动下方监控终端再启动上述命令，并必须持 `/home/linhao/Toolchain/development/heavy-stage.lock`，并用既有守护器每 2 秒采样：MemAvailable<2GiB 或目标文件系统可用<30GiB 时终止整个 scope；不能只依赖 MemoryMax。需要同时记录 cgroup `memory.peak/memory.events`、进程 VmHWM、磁盘最低值；`time -v` 只作为进程口径，不能替代 cgroup 峰值。监控中读到的 memory.peak 是截至采样点的内核高水位；若退出前最终值未能取得，须标记“最后采样值”而非捏造最终峰值。下面为可直接包住上述命令的本机监控流程（在启动构建之前开一个终端；构建完成后 Ctrl-C，保留日志）：

```bash
# 先在构建终端持锁：exec 9>/home/linhao/Toolchain/development/heavy-stage.lock; flock 9
python3 - <<'PY'
import json, pathlib, subprocess, time, os
log=pathlib.Path('/home/linhao/Toolchain/development/llvm-optimize/temp/hybrid52-team-validation/resources.jsonl')
log.parent.mkdir(parents=True, exist_ok=True)
seen=False
while True:
    p=subprocess.run(['systemctl','--user','show','llvm-hybrid52-team.scope',
                      '-p','ControlGroup','--value'],capture_output=True,text=True)
    cg=p.stdout.strip()
    if not cg:
        if seen: break
        time.sleep(1); continue
    root=pathlib.Path('/sys/fs/cgroup'+cg)
    if not root.exists():
        if seen: break
        time.sleep(1); continue
    seen=True
    mem=int(next(x.split()[1] for x in pathlib.Path('/proc/meminfo').read_text().splitlines()
                 if x.startswith('MemAvailable:')))*1024
    st=os.statvfs('/var/tmp'); disk=st.f_bavail*st.f_frsize
    sample={'time':time.time(),'MemAvailable':mem,'disk_available':disk}
    for name in ['memory.current','memory.peak','memory.events']:
        try: sample[name]=(root/name).read_text()
        except FileNotFoundError: pass
    sample['processes']=[]
    for f in root.rglob('cgroup.procs'):
        try: pids=f.read_text().split()
        except FileNotFoundError: continue
        for pid in pids:
            try:
                lines=pathlib.Path('/proc',pid,'status').read_text().splitlines()
                sample['processes'].append({'pid':pid,'status':[s for s in lines
                    if s.startswith(('Name:','VmHWM:','VmRSS:','VmPeak:'))]})
            except FileNotFoundError: pass
    with log.open('a') as f: f.write(json.dumps(sample)+'\n')
    if mem<2*1024**3 or disk<30*1024**3:
        subprocess.run(['systemctl','--user','kill','--kill-whom=all',
                        '--signal=TERM','llvm-hybrid52-team.scope'],check=True)
        raise SystemExit('RESOURCE_FLOOR_ABORT: retain evidence; do not retry')
    time.sleep(2)
PY
```

如走 Quickbuild，先在 PM 批准后由**组员用自己的账号**推其 sandbox，随后在 Quickbuild 选择该分支启动 x86_64 LLVM，再重建 qemu-accel/镜像。这里仅提供模板，本任务没有执行：

```bash
# 在独立 S 中；替换为组员自己的 Gerrit 账号和 sandbox 分支
GERRIT_USER=your_account
BRANCH=sandbox/your_account/llvm-hybrid-link
git -C "$S" push "ssh://$GERRIT_USER@review.tizen.org:29418/platform/upstream/llvm" \
  "HEAD:refs/heads/$BRANCH"
```

## 3. RPM 完整性、链接方式与依赖

```bash
R=$G/local/BUILD-ROOTS/scratch.x86_64.0
B=$R/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build
P=$R/home/abuild/rpmbuild/RPMS/x86_64
N=$LOG/unpacked
mkdir -p "$N"
mapfile -t rpms < <(find "$P" -maxdepth 1 -name '*.rpm' -type f | sort)
test "${#rpms[@]}" -eq 22
rpm -qp --qf '%{NAME}\n' "${rpms[@]}" | sort > "$LOG/rpm-names.txt"
diff -u "$W/docs/52_hybrid_link_evidence/expected-rpm-names.txt" "$LOG/rpm-names.txt"
sha256sum "${rpms[@]}" > "$LOG/rpms.sha256"
stat -c '%s %n' "${rpms[@]}" > "$LOG/rpms.bytes"
for rpmfile in "${rpms[@]}"; do
  # 保留逐包文件表；解包到合并根，重复文件必须记录而非静默当作新增。
  rpm -qpl "$rpmfile" > "$LOG/$(basename "$rpmfile").files"
  (cd "$N"; rpm2cpio "$rpmfile" | cpio -idm --quiet)
done
```

22 个名字详见 [expected-rpm-names.txt](52_hybrid_link_evidence/expected-rpm-names.txt)，不是根据版本发行号字符串猜测。%files 未变，基准来自 docs/35 附录 A；数量变化必须解释，不能直接忽略。

在**新测试 chroot**安装本次 RPM 后查 NEEDED/运行，勿把宿主 libLLVM 混入。可以用组员本次构建根作测试根（构建已结束），在 `gbs chroot --root "$R"` 中以 root 安装该根自己的 RPMS/x86_64 非 debuginfo 包；不要在宿主安装。安装失败/依赖缺失即 FAIL，不使用 `--nodeps`：

```bash
# 以下在测试 chroot 中执行；RPMS 在根内已存在
set -eu
find /home/abuild/rpmbuild/RPMS/x86_64 -maxdepth 1 -name '*.rpm' \
  ! -name '*-debuginfo-*' ! -name '*-debugsource-*' -print0 |
  xargs -0 rpm -Uvh --replacepkgs
rpm -ql llvm clang llvm-devel clang-devel lldb lldb-devel |
  sort -u | awk '/^\/usr\/bin\// {print}' > /tmp/llvm52-tools.txt
python3 - <<'PY'
import pathlib,subprocess,re
static={'clang-22','lld','llvm-ar'}
exceptions={'llvm-config','llvm-exegesis','llvm-tblgen','clang-tblgen','lldb-tblgen'}
for name in pathlib.Path('/tmp/llvm52-tools.txt').read_text().splitlines():
    p=pathlib.Path(name)
    assert p.exists(), name
    if not p.is_file(): continue
    with p.open('rb') as f: magic=f.read(4)
    if magic != b'\x7fELF': continue       # 脚本不应强行套 ELF NEEDED 判据
    real=p.resolve().name
    d=subprocess.check_output(['readelf','-dW',name],text=True)
    needed=re.findall(r'\(NEEDED\).*?\[(.*?)\]',d)
    print(name, '->',p.resolve(),needed)
    shared=any(s.startswith(('libLLVM.so','libclang-cpp.so')) for s in needed)
    assert shared == (real not in static|exceptions),(name,needed)
    if real in {'clang-tidy','clangd','clang-repl','clang-check','lldb'}:
        assert any(s.startswith('libclang-cpp.so') for s in needed),(name,needed)
    v=subprocess.run(['ldd',name],text=True,capture_output=True)
    assert v.returncode==0 and 'not found' not in v.stdout+v.stderr,(name,v.stdout,v.stderr)
for name in ['/usr/lib64/libLTO.so','/usr/lib64/LLVMgold.so','/usr/lib64/liblldb.so']:
    d=subprocess.check_output(['readelf','-dW',name],text=True)
    assert 'libLLVM.so.22.1' in d,(name,d)
    v=subprocess.run(['ldd',name],text=True,capture_output=True)
    assert v.returncode==0 and 'not found' not in v.stdout+v.stderr
PY
for f in clang clang++ clang-cpp clang-cl ld.lld ld64.lld lld-link wasm-ld llvm-ranlib llvm-lib llvm-dlltool; do
  test -L "/usr/bin/$f"
  readlink "/usr/bin/$f"
  readlink -f "/usr/bin/$f"
done
```

PASS：三组及五个上游例外不依赖 LLVM/clang-cpp 共享库；其余 LLVM 工具依赖共享 LLVM，指定 clang 工具依赖 clang-cpp；全部传递依赖可解析。静态在这里仅指 LLVM 组件，不是静态 glibc。若链接器 `--as-needed` 改变直接依赖，必须保留 readelf/ldd 全文分析，不能擅自改 PASS 表。clangd/tidy 私有 `.a`、opt 的 LLVMOptDriver 不否定其动态 LLVM 选择，见报告 §4。

## 4. 归档与包范围

宿主对每个 RPM 做文件名检查，compiler-rt 运行库例外单列；普通包不得包含 LLVM 开发 `.a`：

```bash
for f in "${rpms[@]}"; do
  name=$(rpm -qp --qf '%{NAME}' "$f")
  rpm -qpl "$f" | awk '/\.a$/ {print}' > "$LOG/$name.archives"
  case "$name" in
    *devel*|compiler-rt) ;; # compiler-rt 的 45 个运行库保留
    *) test ! -s "$LOG/$name.archives" ;;
  esac
done
```

沿用 356627 验收工具按 archive header offset/成员序号处理同名成员，检查完整符号→成员多重集合，不能只检查 armap 非空。在宿主执行：

```bash
export W N LOG
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os,sys,pathlib,json
w=pathlib.Path(os.environ['W']);n=pathlib.Path(os.environ['N'])
sys.path.insert(0,str(w/'tools'))
from inspect_llvm_archives import inspect
paths=(pathlib.Path(os.environ['LOG'])/'llvm-static-devel.archives').read_text().splitlines()
assert len(paths)==225,len(paths)
for name in paths:
    r=inspect(n/name.lstrip('/'))
    assert not r['thin'] and r['bitcode']==0 and r['other']==0,r['path']
    assert r['machine']==r['member_count'],r['path']
    assert r['index_equals_machine_symbols'],r['path']
    assert all(not x['debug_sections'] for x in r['members']),r['path']
    with (pathlib.Path(os.environ['LOG'])/'archives.jsonl').open('a') as f:
        f.write(json.dumps(r)+'\n')
print('225 native archives / full index / no debug: PASS')
PY
```

同时核对 `libomp-devel` 中 libarcher_static.a 与 static-devel 对应内容一致，compiler-rt 仍为 45 个 `.a`。构建日志须含完整 NATIVE_ARCHIVES_BEGIN/END/PASS（或当前 Source 的对应状态）、转换无失败、标准 brp 后处理无 bitcode 格式错误。Source 未改变，可沿用 docs/35 的成员身份/次序、强符号与消费者验收方法。已知 `.llvm_addrsig` 后处理边界见 docs/51；此补丁没有宣称修复它。

## 5. 实际编译、链接和运行

先在新测试 x86_64 chroot（已安装本次 RPM）执行；保存命令与输出：

```bash
set -eu
mkdir -p /tmp/llvm52-smoke
cd /tmp/llvm52-smoke
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
```

交叉 hello **必须使用同一快照完整目标 sysroot**（含 libc crt、libstdc++ 头/库及 GCC runtime），不可拿 x86 根当 ARM sysroot。在有本次 x86 工具与 ARM sysroot 的验证机执行；以下变量是固定挂载约定，缺失即记录未验证，不能只编 `.o` 后声称链接 PASS：

```bash
ARM_SYSROOT=/srv/tizen-sysroots/armv7l
A64_SYSROOT=/srv/tizen-sysroots/aarch64
# GCC_TOOLCHAIN 指包含相应 target 的 lib/gcc 与 target/include 的工具链前缀。
ARM_GCC=/srv/tizen-cross/armv7l
A64_GCC=/srv/tizen-cross/aarch64
for dir in "$ARM_SYSROOT" "$A64_SYSROOT" "$ARM_GCC" "$A64_GCC"; do test -d "$dir"; done
for triple in armv7l-tizen-linux-gnueabi aarch64-tizen-linux-gnu; do
  case "$triple" in
    armv7l*) sysroot=$ARM_SYSROOT; gcc=$ARM_GCC ;;
    aarch64*) sysroot=$A64_SYSROOT; gcc=$A64_GCC ;;
  esac
  clang --target="$triple" --sysroot="$sysroot" --gcc-toolchain="$gcc" \
    -fuse-ld=lld hello.c -o "hello-$triple"
  clang++ --target="$triple" --sysroot="$sysroot" --gcc-toolchain="$gcc" \
    -fuse-ld=lld hello.cc -o "hello-cxx-$triple"
  readelf -h "hello-$triple"
  readelf -h "hello-cxx-$triple"
done
```

PASS：编译/链接退出 0，ELF Machine 为对应目标；在 ARM 设备或已配置好的 qemu 环境中运行，输出均为 hello、exit 0（若没有运行环境，明确仅链接通过、运行未验证）。记录 `clang -###`、sysroot/工具链 RPM 版本，防止 bundled 或系统旧 clang 混用。任何实际失败必须保存原文，不直接降级为“配置正确”。

## 6. accel 与总结果记录

新的 LLVM RPM 必须经过 qemu-accel 重建后再检查；旧静态 accel 中没有 libLLVM/clang-cpp，不能直接塞入动态工具。对新 accel：

```bash
# 将服务器实际产物保存为此路径；不在这里构建 accel
ACCEL_RPM=/srv/llvm52-results/clang-accel-x86_64-armv7l.rpm
stat -c '%s %n' "$ACCEL_RPM"
sha256sum "$ACCEL_RPM"
mkdir -p /srv/llvm52-results/accel-unpacked
(cd /srv/llvm52-results/accel-unpacked; rpm2cpio "$ACCEL_RPM" | cpio -idm --quiet)
du -sb /srv/llvm52-results/accel-unpacked
rpm -qpl "$ACCEL_RPM" | tee /srv/llvm52-results/accel-files.txt
```

`du -sb` 与 QB 的“文件路径长度合计”不是完全相同的统计口径，比较时同时提供 RPM 头 FILESIZES 合计：

```bash
rpm -qp --qf '[%{FILENAMES}\t%{FILESIZES}\n]' "$ACCEL_RPM" > /srv/llvm52-results/accel-path-bytes.tsv
awk -F '\t' '{s+=$2} END {printf "%.0f\n",s}' /srv/llvm52-results/accel-path-bytes.tsv
```

在**新 Base worker 的真实 `/emul` 环境**逐个 ELF 查询 NEEDED 与依赖，不在宿主直接执行旧快照 loader：

```bash
# 在 worker 上；只有确认 /emul 中 x86_64 loader 存在时执行
python3 - <<'PY'
import pathlib,subprocess
loader='/emul/lib64/ld-linux-x86-64.so.2'
assert pathlib.Path(loader).exists()
for p in sorted(pathlib.Path('/emul/usr/bin').iterdir()):
    if not p.is_file(): continue
    with p.open('rb') as f: magic=f.read(4)
    if magic!=b'\x7fELF': continue
    h=subprocess.check_output(['readelf','-hW',str(p)],text=True)
    assert 'Advanced Micro Devices X86-64' in h,(str(p),h)
    print(str(p),subprocess.check_output(['readelf','-dW',str(p)],text=True))
    r=subprocess.run([loader,'--library-path','/emul/lib64:/emul/usr/lib64',
                      '--list',str(p)],capture_output=True,text=True)
    print(r.stdout,r.stderr)
    assert r.returncode==0 and 'not found' not in r.stdout+r.stderr,str(p)
PY
```

对照报告 [accel-tool-map.csv](52_hybrid_link_evidence/accel-tool-map.csv) 的 107 个路径（含别名）；必须覆盖静态三组、92 个预计动态路径及两个上游例外。新旧清单有增减时全部列出；同时检查 libLTO/LLVMgold 的 ldd closure。两库必须出现在对应 accel/基础加速包集合中，loader/RUNPATH 可找到；不能仅以包内有同名文件判通过。aarch64 accel 同样执行，现有 QB 清单只涵盖 armv7l。

## 7. 预期结果与回传模板

| 项目 | 本次配置级结论 / 待完整构建 PASS | 参考证据（禁止当本次实测） |
| --- | --- | --- |
| clang/lld/ar 及别名 | 链接图无 libLLVM/clang-cpp；实际 NEEDED 仍需确认 | docs/22 §5 三组静态，旧源码参考 |
| 其他 14 个指定目标 | 共享 LLVM，clang 工具/LLDB 还有 clang-cpp；私有 `.a` 明列 | 本次 a-selected-commands.json，仅配置 |
| 开关 OFF | 188 个 link edge 与原版动态配置相同 | 本次 switch-off-control.json |
| ARM 配方 | build/install 同字节 | 本次 macro-comparison.json |
| RPM 与归档 | 22 包；225 开发归档 native/完整索引；45 compiler-rt | 名单来自 docs/35；本次尚未打包 |
| 编译正确性 | 上述三目标 hello、lld/ar 与动态工具全部通过 | docs/22 曾 30/30 TU 同字节，**旧源码参考，不是本次实测** |
| 旧混合构建容量 | 不作为本次准入认证 | docs/22：5040.295秒，scope达18GiB；旧源码参考 |
| QB x86 LLVM wall | 本次记录同口径总耗时与阶段耗时 | llvm_builds.csv：5686→29864秒，跨快照参考 |
| QB accel RPM / 路径总字节 | 本次记录实际值，不承诺比例 | SIZE_FINDINGS.md：54,806,369→659,624,309；239,912,044→2,756,647,372 字节 |

回传：准确 Git commit/tree/patch SHA、Base/Unified URL+repomd SHA、实际包版本、CMakeCache、完整 build.log 与 exit/tee 状态、总/阶段耗时、cgroup/进程内存和磁盘数据、22 RPM 清单与 SHA、NEEDED/ldd/链接类型、归档 JSON、smoke 原始命令/输出、accel 清单/大小/依赖闭合；每项 PASS/FAIL/未获取单列。所有 FAIL 先报告，不能用 9 月结果代替本轮验证。PM review 前不在本机启动完整构建。
