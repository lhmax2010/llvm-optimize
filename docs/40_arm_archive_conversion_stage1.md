# 40 ARM 静态库转换第一段：A2安全停止，B/C未执行

> **最新状态（2026-10-10，§8）：C0 仓库预检 STOP。** GBS 标准 binfmt/mmap 初始化已获授权；指定 Base 快照返回 HTTP 404，本轮没有启动 GBS，C1–C4 未执行。前次 B 的 x86 全量回归 PASS 保持有效。
>
> **用户恢复命令：`sudo sysctl -w vm.mmap_min_addr=65536`。** 这是本次实测原值；若以后 GBS 临时写为 0，可用此命令恢复，重启也会重新加载系统配置、恢复这类非持久化修改。本轮前后均为 65536，**本轮无需执行恢复**；代理没有执行此命令，也没有手工注册 binfmt。以下 §1–§7 保留各次历史状态，当前结论见 §8。

日期：2026-10-10（Asia/Shanghai）。本报告与[docs/42](42_disk_cleanup.md)、STATUS同commit发布。

**STOPPED_BEFORE_B。** 夜间任务先清理再执行x86回归与ARM第一段。A1完成，但A2发现保留范围的`plan_evaluation/analysis/05E_worktree`依赖待删`chromium-efl/.git`；未得到关于这份额外依赖的处置规则，依无人值守“规定之外停止”要求结束全部后续步骤。三个Chromium目录均未删除；A3只备份日志并生成脚本。不能把本轮停止归因于x86回归或ARM能力。

## 1. 输入与当前Source身份

- 既有Source：`tools/llvm_static_archives_source.py`，SHA256 `6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557`，仍为docs/35已验证的x86版本。
- 对照记录：`temp/archive-fix-v2-final-20261009/continue-20261009/ba-install-conversion-evidence/summary.json`；docs/39 §7.2登记225档、3864成员，不将历史PASS记为本轮回归结果。
- 本轮没有新Source、没有隔离实现分支、没有相对6bd0546a的代码diff；两份已上传补丁、W/llvm/spec、gbs_llvm.conf保持不变。
- 保护摘要与停止证据：`/home/linhao/Toolchain/development/llvm-optimize/temp/night-arm-stage1-20261010/protected-final.json`、`stop-context.json`。

## 2. B：x86_64不变性回归

| 要求 | 本轮状态 |
|---|---|
| 隔离工作树内实现独立架构policy分派 | NOT RUN：A2停止 |
| Rnew的225个原始归档before_sha256核验 | NOT RUN；没有把读取旧报告作为重新核SHA |
| 新Source全量转换、225整档及3864成员SHA一致 | NOT RUN |
| 现有单元测试、正负夹具 | NOT RUN |

既有x86行为未修改，不能由此宣称新ARM分派实现通过不变性认证。Rnew/B等指定输入保持，未使用已清理的docs/30旧BUILD作回归输入。

## 3. C：ARM第一段

| 要求 | armv7l | aarch64 |
|---|---|---|
| C0：全新/var/tmp根的极小GBS包、binfmt/accel exec证据 | NOT RUN | NOT RUN |
| C1：prep/configure，仅static-devel/libomp-devel库目标 | NOT RUN | NOT RUN |
| C2：全量bitcode原命令、triple/PIC/ABI/末项优化普查 | NOT RUN | NOT RUN |
| C3：转换/索引/强符号/PIC正负夹具 | NOT RUN | NOT RUN |
| GNU ld/lld、A/B/shared/dlopen/GC/bitcode反例 | NOT RUN | NOT RUN |
| GNU strip和llvm-strip两副本验收 | NOT RUN | NOT RUN |

没有创建ARM构建根、执行GBS、配置LLVM、注册binfmt或采集新ARM数据。docs/39的草案仍是草案；本轮没有执行C0，故不伪造C0失败原因或据此给出未经核实的root注册命令。

## 4. 收尾

按用户“任一步失败即停止后续所有步骤”要求记录停止并推送；不重试、不请求夜间确认。项目锁在收尾释放，无本任务构建/采样器/挂载残留，证据`/home/linhao/Toolchain/development/llvm-optimize/temp/night-arm-stage1-20261010/final-cleanup.json`及`lock-released.json`。

后续仅在A2的保留Git依赖有明确处置后，重新决定如何继续B/C。没有改变16GiB/18GiB/swap0/6/6/2等预注册资源规则，也没有消耗本轮ARM构建次数。

## 5. 2026-10-10续接：清理与本任务解耦，B PASS

上文§1–4是`26da4ac`停止时的原文，保留不改。用户随后明确本任务仅B/C、清理不构成前置条件；本节起为新执行，不能将前次NOT RUN当作本次结果。
开场/home可用532,224,368,640 B（495.673 GiB），通过120 GiB门槛；主仓库HEAD=`26da4acd80cd55ea6ecc5a2350a550947b832489`、status为空，无本项目竞争进程。
没有读取/修改用户指定的四个旧根，没有执行任何磁盘清理。

本轮证据目录 **E=`/home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-stage1-20261010`**。原始输出只保存在本机。
持有主项目和Rnew的独占锁，记录于`E/lock-acquired.json`；本阶段完成后锁继续持有至C检查与收尾。
开场证据：`E/precheck.json`、`E/protected-start.json`。

### 5.1 隔离实现与边界

隔离工作树`/home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-source-stage1-20261010`，分支`arm-archive-stage1-20261010`，基于上述主仓库HEAD。
候选Source：`tools/llvm_static_archives_arm_trial.py`，SHA256 **`6a36f173c3efb05c7011aa7029aeb2ae3119e1f77a32536fcc791938bf20c4b7`**。
原`tools/llvm_static_archives_source.py`及已上传补丁中的Source仍为`6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557`，没有替换。
候选文件随本阶段提交发布，隔离分支的提交由`git log -1 -- tools/llvm_static_archives_arm_trial.py`定位；主仓库只接收该分支的快进提交。

采用docs/39 §7.1分派：x86的原classifier、IR settings、PIC scanner及命令flags保持；ARM使用独立函数和精确参数表。
原有函数/类除公共convert的分派调用与CLI入口外，AST逐个相同；新增ARM分支在x86路径不可达。
ARM32草案为末项Os、thumbv7/softfp/little-endian；AArch64为末项O3、tune-cpu=cortex-a53。
ARM ELF32 REL/RELA、AArch64 ELF64重定位草案带未知类型硬失败，夹具覆盖只读绝对重定位、SHN_ABS、GOT/PLT/PREL31、ADRP+LO12。
**ARM表仅是docs/39草案，尚未通过真实归档C2/C3认证；本阶段PASS只认证x86不变性。** 未改spec、LLVM源码、gbs_llvm.conf或两份已上传补丁。
完整差异见本节末尾diff；生成原件`E/source-vs-6bd0546a.diff`、`E/candidate.json`。

### 5.2 输入身份与实际执行

Rnew构建树：`W/temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build`。
225个`lib64`原始归档逐档核对docs/35的before_sha256全部相同，再只读复制到`E/x86-input/usr/lib64`，复制后再次核对；合计5,482,378,620 B。
对照为`W/temp/archive-fix-v2-final-20261009/continue-20261009/ba-install-conversion-evidence/summary.json`，SHA256
`4d824c4f2c9fae5b1064e76b1eb8b328248bdbbfca2beb98b32759592529fcd6`。成员以对应`members/<归档>/after.json`的序号、名称、同名出现序号和SHA比对。
这是**strip前**转换结果比较，不拿RPM剥离后归档冒充基准。

| 工具（均来自Rnew的B/bin，直接执行） | SHA256 |
| --- | --- |
| clang-22 | d25e99607c9ea23bf2e50da5075c21f0145f6da24a39a4228d2fd8026ead70cf |
| llvm-dis | 9416f931e11ca81259c02fb53f103125771cb8fa3a534a1bf4c7daf2df9a34c7 |
| llvm-nm | 2a5d1928b5b7a40eae2dc8187794be5f73e04491a08c1123646992a7102b3eda |

脚本`E/run_x86_regression.py`调用候选`convert(root, output, clang, dis, nm, B, 'x86_64', 4, 4294967296)`；
LD_LIBRARY_PATH只指向既有`temp/toolchain-runtime-baseline/libxml2/usr/lib64`。
完整命令与逐成员argv：`E/x86-regression-scope/launch.json`、`commands.log`、`E/x86-conversion/members/**/convert.json`。
每次写出一个after.json就立即比对历史整档SHA/有序成员SHA/完整索引映射，发现不同会抛异常停止后续档；没有事后豁免。
所有3,853条补回后端flags及顺序另逐条与历史记录核对一致。编译器路径采用同SHA的宿主绝对路径，输入/输出路径使用新证据目录。

资源入口沿用既有离线转换策略：min(18, floor(MemAvailable/GiB)-4)，本次得到**16 GiB**；不改变完整构建18GiB门禁。
MemorySwapMax=0，nice15/ionice3，4worker，各子命令4GiB地址空间；30秒采样，宿主MemAvailable低于2GiB中止。

### 5.3 回归结果

| 检查 | 结果 |
| --- | --- |
| 输入225档before SHA | 225/225 PASS |
| 转换后整档after SHA | 225/225 PASS，与docs/35逐字节一致 |
| 有序成员身份+SHA | 3,864/3,864 PASS；3,853转换+11原机器码 |
| 完整索引映射 | 225/225 PASS，与docs/35一致 |
| 后端flags与次序 | 3,853/3,853 PASS |
| 原有转换/解析/消费者命令测试 | 54项PASS |
| 新分派/ARM草案正负夹具 | 6项PASS；合计60项，13.174210s |
| 全量转换wall | 1748.271039s |
| 含复制的驱动wall | 1830.325873s |
| 单成员最大RSS | 1043800 KiB |
| scope采样观测MemoryPeak | 14,240,006,144 B（13.262039 GiB，含文件cache） |
| 宿主最低采样MemAvailable | 21,079,465,984 B（19.631783 GiB） |

完整225档表及所有SHA在`E/x86-regression-result.json`，逐档中间门禁在`x86-comparison-progress.json`，输入在`x86-input-check.json`/`x86-input-copy.json`。
转换内建索引、PIC、强符号门禁全部通过；允许缺失的弱符号按原规则登记，汇总`{"W": 1920}`，不是新增放行。
测试模块列表与原始输出为`E/unit-tests-result.json`、`unit-tests.log`；测试将历史8个相关模块导入指向候选Source，再加新夹具。没有声称无关的全库/性能/旧RPM配方入口测试均重跑。
资源原始证据`x86-regression-scope/samples.jsonl`、`process-memory.jsonl`、`time-v.txt`、`scope-after-rpm.json`、`outcome.json`及`memory-summary.json`。

结论：本输入范围的**x86_64全量不变性PASS**；没有重新构建LLVM或打包。scope外层wall 1,832.077124s，exit0，所有memory.events为0；sampler_reaped/log_reader_reaped均为true。C尚须独立通过环境与实际ARM归档门禁。

### 5.4 候选Source相对6bd0546a的完整diff

以下为全部改动的零上下文diff（`E/source-vs-6bd0546a-u0.diff`）；带上下文原件仍保留在`E/source-vs-6bd0546a.diff`。

```diff
--- a/tools/llvm_static_archives_source.py
+++ b/tools/llvm_static_archives_arm_trial.py
@@ -365,0 +366,275 @@
+# Experimental ARM tables: recipe-derived until the full per-architecture census
+# and consumer gates complete. Never change the certified x86_64 tables above.
+# Evidence: Clang Arch/ARM.cpp 275-353, 660-679; AArch64.cpp 200-266;
+# BackendUtil.cpp 383-405; CodeGenModule.cpp 2729-2740, 2929-2992.
+ARM_OPTIMIZATION = {'armv7l': '-Os', 'aarch64': '-O3'}
+ARM_IR_TRIPLES = {'armv7l': {'thumbv7-tizen-linux-gnueabi'},
+                  'aarch64': {'aarch64-tizen-linux-gnu'}}
+ARM_DRIVER_TRIPLES = {'armv7l': {'armv7l-tizen-linux-gnueabi', 'thumbv7-tizen-linux-gnueabi'},
+                      'aarch64': {'aarch64-tizen-linux-gnu'}}
+ARM_EXACT_TOKENS = {
+    'armv7l': {
+        '-march=armv7-a': ('ir', 'triple/CPU/features'),
+        '-mthumb': ('ir', 'Thumb triple and target features'),
+        '-mfpu=neon': ('ir', 'FPU target features'),
+        '-mfloat-abi=softfp': ('restore', 'calling convention and backend FloatABI'),
+        '-mlittle-endian': ('restore', 'driver endianness cross-check'),
+        '-mtune=cortex-a8': ('irrelevant', 'LLVM 22 ARM driver ignores mtune'),
+    },
+    'aarch64': {
+        '-march=armv8-a+fp+simd+crc+crypto': ('ir', 'CPU target features'),
+        '-mtune=cortex-a53': ('ir', 'tune-cpu attribute'),
+    },
+}
+ARM_REQUIRED_TOKENS = {
+    'armv7l': {'-march=armv7-a', '-mthumb', '-mfpu=neon', '-mfloat-abi=softfp', '-mlittle-endian'},
+    'aarch64': {'-march=armv8-a+fp+simd+crc+crypto', '-mtune=cortex-a53'},
+}
+
+
+def arm_classify_options(argv, arch):
+    """Certified policy, not arbitrary compiler-option replay; consume operands."""
+    if arch not in ARM_OPTIMIZATION:
+        raise ValueError('uncertified architecture: '+arch)
+    rows, optimizations, dwarfs, contractions = [], [], [], []
+    switches = {key: [] for key in ('function-sections', 'data-sections',
+                                  'unique-section-names', 'addrsig')}
+    operand_options = {'-D', '-I', '-isystem', '-resource-dir', '-o', '-MT', '-MF', '-x'}
+    exact_ir = {'-fomit-frame-pointer', '-fno-omit-frame-pointer', '-fexceptions',
+                '-fno-exceptions', '-fasynchronous-unwind-tables', '-funwind-tables',
+                '-fno-asynchronous-unwind-tables', '-fno-unwind-tables', '-fno-common',
+                '-ftrapping-math', '-fstack-protector', '-fPIC', '-fPIE', '-fpic', '-fpie',
+                '-fno-pic', '-fno-pie', '-fno-semantic-interposition'}
+    exact_ir.update({'-fvisibility-inlines-hidden', '-fno-visibility-inlines-hidden'})
+    index = 0
+    while index < len(argv):
+        token = argv[index]
+        category, reason = None, None
+        if index == 0 and re.fullmatch(r'(?:(?:armv7l-tizen-linux-gnueabi|aarch64-tizen-linux-gnu)-)?clang(?:\+\+)?(?:-22)?', Path(token).name):
+            category, reason = 'irrelevant', 'original driver path'
+        elif token in ARM_EXACT_TOKENS[arch]:
+            category, reason = ARM_EXACT_TOKENS[arch][token]
+        elif token.startswith('--target='):
+            if token.split('=', 1)[1] not in ARM_DRIVER_TRIPLES[arch]:
+                raise ValueError('uncertified ARM driver target: '+token)
+            category, reason = 'irrelevant', 'target cross-checked against architecture policy'
+        elif token.startswith('-m'):
+            raise ValueError('unclassified original command token: '+token)
+        elif token in operand_options:
+            if index+1 == len(argv) or argv[index+1].startswith('-'):
+                raise ValueError('missing operand for '+token)
+            category, reason = 'irrelevant', 'preprocessing, driver resource, output or language operand'
+            rows.append(dict(index=index, token=token, category=category, reason=reason))
+            index += 1
+            rows.append(dict(index=index, token=argv[index], category=category, reason='operand of '+token))
+            index += 1
+            continue
+        elif re.fullmatch(r'-O(?:[0-3szg]|fast)', token):
+            category, reason = 'ir', 'original IR pipeline; certified last optimization is also replayed'
+            optimizations.append(token)
+        elif re.fullmatch(r'-gdwarf-\d+', token):
+            category, reason = 'restore', 'debug emission version'
+            dwarfs.append(token)
+        elif token.startswith('-ffp-contract='):
+            category, reason = 'restore', 'backend FP fusion policy'
+            contractions.append(token.split('=', 1)[1])
+        elif any(token in ('-f'+key, '-fno-'+key) for key in switches):
+            category, reason = 'restore', 'backend section/symbol emission policy'
+            for key in switches:
+                if token in ('-f'+key, '-fno-'+key):
+                    switches[key].append(token == '-f'+key)
+        elif (token in exact_ir or re.fullmatch(r'-fvisibility=(?:default|hidden|protected)', token)
+              or re.fullmatch(r'-g(?:[0-3]|line-tables-only|line-directives-only)?', token)
+              or token in ('-frecord-command-line', '-frecord-gcc-switches')
+              or token.startswith('-std=')):
+            category, reason = 'ir', 'function/module attributes, metadata or frontend semantics'
+        elif token == '-flto=thin':
+            category, reason = 'irrelevant', 'pre-link bitcode format already materialized; never replay LTO'
+        elif (token.startswith(('-W', '-D', '-I', '--target=', '-fmessage-length=',
+                               '-fdiagnostics-color=')) or token in
+              ('-fdiagnostics-color', '-fcolor-diagnostics', '-fno-color-diagnostics',
+               '-pedantic', '-pipe', '-c', '-MD', '--driver-mode=g++')):
+            category, reason = 'irrelevant', 'diagnostics, preprocessing or driver action'
+        elif not token.startswith('-') and re.search(r'\.(?:c|cc|cpp|cxx|C|ii|i|bc|ll|o|obj|s|S)$', token):
+            category, reason = 'irrelevant', 'input/output path'
+        if category is None:
+            raise ValueError('unclassified original command token: '+token)
+        rows.append(dict(index=index, token=token, category=category, reason=reason))
+        index += 1
+    if not optimizations or optimizations[-1] != ARM_OPTIMIZATION[arch]:
+        raise ValueError('uncertified last optimization: '+str(optimizations[-1:] or 'missing'))
+    if not dwarfs or dwarfs[-1] != '-gdwarf-4':
+        raise ValueError('uncertified last DWARF option: '+str(dwarfs[-1:] or 'missing'))
+    effective = {}
+    for key, values in switches.items():
+        effective[key] = values[-1] if values else DEFAULTS.get(key, False)
+        if not effective[key]:
+            raise ValueError('original command does not enable '+key)
+    contraction = contractions[-1] if contractions else DEFAULTS['fp-contract']
+    if contraction not in ('on', 'off', 'fast'):
+        raise ValueError('uncertified FP contraction value: '+contraction)
+    missing = set(ARM_REQUIRED_TOKENS[arch]) - set(argv)
+    if missing:
+        raise ValueError('uncertified ARM command missing: '+repr(sorted(missing)))
+    return dict(tokens=rows, optimization=optimizations[-1], dwarf=dwarfs[-1],
+                switches=effective, fp_contract=contraction,
+                fp_contract_source='last explicit option' if contractions else 'LLVM 22 non-CUDA/HIP default on')
+
+
+
+def arm_ir_settings(lines, arch):
+    """Read LLVM 22 textual metadata/attributes without modifying input IR."""
+    lines = list(lines)
+    retained, metadata = [], {}
+    triple, command_id = None, None
+    levels, cpus, features = {}, set(), set()
+    for line in lines:
+        # Intrinsic references, not string literals in LLVM's own implementation.
+        for intrinsic in ('llvm.type.test', 'llvm.public.type.test'):
+            if re.search(r'@'+re.escape(intrinsic)+r'(?:\.|\s*\()', line):
+                raise ValueError('unsupported type metadata/intrinsic: '+intrinsic)
+        if re.search(r'!vcall_visibility\b', line):
+            raise ValueError('unsupported type metadata: !vcall_visibility')
+        if re.search(r'!"EnableSplitLTOUnit"\s*,\s*i32\s+1\b', line):
+            raise ValueError('unsupported type metadata: EnableSplitLTOUnit=1')
+        if line.startswith('!llvm.commandline = '):
+            match = re.fullmatch(r'!llvm.commandline = !\{!(\d+)\}\s*', line)
+            if not match or command_id is not None:
+                raise ValueError('exactly one recorded command is required')
+            command_id = match[1]
+        match = re.fullmatch(r'!(\d+) = !\{!"(.*)"\}\s*', line)
+        if match:
+            metadata[match[1]] = match[2]
+        if line.startswith('target triple = '):
+            value = line.split('"')[1]
+            if triple is not None:
+                raise ValueError('multiple IR triples')
+            triple = value; retained.append(line.rstrip())
+        if line.startswith('attributes #'):
+            retained.append(line.rstrip())
+            cpus.update(re.findall(r'"target-cpu"="([^"]+)"', line))
+            features.update(re.findall(r'"target-features"="([^"]+)"', line))
+        if line.startswith('!') and any('"'+n+'"' in line for n in ('PIC Level', 'PIE Level', 'Code Model')):
+            retained.append(line.rstrip())
+            match = re.search(r'!"(PIC Level|PIE Level|Code Model)", i32 (\d+)', line)
+            if not match:
+                raise ValueError('unrecognized relocation flag: '+line.rstrip())
+            key, value = match.groups()
+            if key in levels and levels[key] != int(value):
+                raise ValueError('conflicting relocation flags')
+            levels[key] = int(value)
+    if triple not in ARM_IR_TRIPLES.get(arch, set()):
+        raise ValueError('uncertified '+arch+' IR triple: '+str(triple))
+    pic, pie = levels.get('PIC Level', 0), levels.get('PIE Level', 0)
+    if pic not in (0, 1, 2) or pie not in (0, 1, 2) or (pie and pie != pic):
+        raise ValueError('unsupported PIC/PIE flags')
+    if 'Code Model' in levels:
+        raise ValueError('explicit code model requires separate certification')
+    if command_id not in metadata:
+        raise ValueError('missing original command: backend policy cannot be certified')
+    recorded_command = shlex.split(re.sub(r'\\([0-9A-Fa-f]{2})',
+        lambda match: chr(int(match[1], 16)), metadata[command_id]))
+    policy = arm_classify_options(recorded_command, arch)
+    flags = ['--no-default-config', '--target='+triple, '-x', 'ir', policy['optimization'],
+             *BACKEND_FLAGS, '-ffp-contract='+policy['fp_contract'], '-c']
+    flags += ([{1: '-fpie', 2: '-fPIE'}[pie]] if pie else
+              [{1: '-fpic', 2: '-fPIC'}[pic]] if pic else ['-fno-pic', '-fno-pie'])
+    if arch == 'armv7l':
+        if any('-thumb-mode' in f.split(',') or '-neon' in f.split(',') for f in features):
+            raise ValueError('ARM IR features contradict certified Thumb/NEON policy')
+        # Clang BackendUtil FloatABI and driver endianness are not inferred here.
+        flags += ['-mfloat-abi=softfp', '-mlittle-endian']
+    elif arch == 'aarch64':
+        tunes = set(re.findall(r'"tune-cpu"="([^"]+)"', ''.join(lines)))
+        if tunes and tunes != {'cortex-a53'}:
+            raise ValueError('uncertified AArch64 tune-cpu: '+repr(sorted(tunes)))
+    return dict(triple=triple, pic_level=pic, pie_level=pie, target_cpu=sorted(cpus),
+                target_features=sorted(features), flags=flags, evidence=retained,
+                recorded_command=recorded_command, policy=policy)
+
+
+
+def arm_pic_relocations(data, arch):
+    """Experimental, fail-closed ARM PIC policy for REL/RELA input sections.
+
+    LLVM ELFRelocs/{ARM,AArch64}.def and lld/ELF/Arch/{ARM,AArch64}.cpp
+    define the numbers and expressions. Unknown/TLS/platform policies require
+    separate certification. Low-12 address fragments are not full addresses.
+    """
+    bits, machine = (1, 40) if arch == 'armv7l' else (2, 183)
+    if (arch not in ARM_OPTIMIZATION or member_kind(data) != 'machine' or
+            data[4:6] != bytes([bits, 1]) or struct.unpack_from('<H', data, 18)[0] != machine):
+        raise ValueError('not certified '+arch+' little-endian ET_REL')
+    if bits == 1:
+        off = struct.unpack_from('<I', data, 32)[0]
+        stride, count = struct.unpack_from('<HH', data, 46)
+        sfmt, symfmt = '<IIIIIIIIII', '<IIIBBH'
+    else:
+        off = struct.unpack_from('<Q', data, 40)[0]
+        stride, count = struct.unpack_from('<HH', data, 58)
+        sfmt, symfmt = '<IIQQQQIIQQ', '<IBBHQQ'
+    if stride < struct.calcsize(sfmt) or not off:
+        raise ValueError('invalid ARM ELF section header')
+    if not count:
+        count = struct.unpack_from(sfmt, data, off)[5]
+    sections = [struct.unpack_from(sfmt, data, off+i*stride) for i in range(count)]
+    if arch == 'armv7l':
+        absolute = {2,5,6,7,8,38,43,44,47,48,55,132,133,134,135}
+        narrow = {5,6,7,8}
+        # NONE, relative code/data, GOT/PLT and EHABI PREL31. TARGET2/BASE_ABS
+        # and TLS are deliberately absent pending platform/corpus evidence.
+        allowed = {0,1,3,4,10,11,24,25,26,27,28,29,30,40,42,45,46,49,50,
+                   51,52,53,54,56,57,58,59,60,61,62,63,64,65,66,67,68,69,
+                   96,97,98,102,103}
+    else:
+        absolute = {0x101,0x102,0x103,0x13d,0x244} | set(range(0x107,0x111))
+        narrow = {0x102,0x103}
+        # ADRP+LO12, PREL, branches and GOT fragments; no TLS/PAuth default.
+        allowed = {0,0x100,0x104,0x105,0x106,0x111,0x112,0x113,0x114,
+                   0x115,0x116,0x117,0x118,0x11a,0x11b,0x11c,0x11d,0x11e,
+                   0x11f,0x120,0x121,0x122,0x123,0x124,0x125,0x12b,
+                   0x12c,0x12d,0x12e,0x12f,0x130,0x131,0x132,0x133,
+                   0x134,0x135,0x136,0x137,0x138,0x139,0x13a,0x13b}
+    checked, forbidden, types = 0, [], Counter()
+    for section in sections:
+        if section[1] not in (4, 9):
+            continue
+        target = sections[section[7]]
+        if not target[2] & 2:
+            continue
+        symidx = section[6]; symbols = sections[symidx]
+        if symbols[1] != 2 or symbols[9] < struct.calcsize(symfmt):
+            raise ValueError('invalid ARM relocation symbol table')
+        xindex = [s for s in sections if s[1] == 18 and s[6] == symidx]
+        rfmt = ('<IIi' if section[1] == 4 else '<II') if bits == 1 else ('<QQq' if section[1] == 4 else '<QQ')
+        if section[9] < struct.calcsize(rfmt) or section[5] % section[9]:
+            raise ValueError('invalid ARM relocation stride')
+        for pos in range(section[4], section[4]+section[5], section[9]):
+            rel = struct.unpack_from(rfmt, data, pos); info = rel[1]
+            kind, si = (info & 255, info >> 8) if bits == 1 else (info & 0xffffffff, info >> 32)
+            if si*symbols[9] >= symbols[5]:
+                raise ValueError('ARM relocation symbol index outside table')
+            sym = struct.unpack_from(symfmt, data, symbols[4]+si*symbols[9])
+            ndx = sym[5] if bits == 1 else sym[3]
+            if ndx == 0xffff:
+                if len(xindex) != 1 or si*4 >= xindex[0][5]:
+                    raise ValueError('missing extended ARM symbol section index')
+                ndx = struct.unpack_from('<I', data, xindex[0][4]+4*si)[0]
+            checked += 1; types[kind] += 1
+            if kind not in absolute | allowed:
+                raise ValueError('uncertified '+arch+' relocation '+str(kind)+' at section '+str(section[7]))
+            if ndx != 0xfff1 and (kind in narrow or kind in absolute and not target[2] & 1):
+                forbidden.append(dict(type=kind, target_section=section[7], symbol_index=si))
+    return dict(checked=checked, forbidden=forbidden, types=dict(types))
+
+
+def policy_for_arch(arch):
+    if arch == 'x86_64':
+        # These are the original functions; the ARM branches are unreachable.
+        return dict(settings=lambda lines: ir_settings(lines, arch=arch), relocations=pic_relocations)
+    if arch in ARM_OPTIMIZATION:
+        return dict(settings=lambda lines: arm_ir_settings(lines, arch),
+                    relocations=lambda data: arm_pic_relocations(data, arch))
+    raise ValueError('uncertified architecture: '+arch)
+
+
@@ -592 +867,2 @@
-    if arch not in CERTIFIED_OPTIMIZATION or jobs < 1 or address_space_bytes < 1:
+    policy = policy_for_arch(arch)
+    if jobs < 1 or address_space_bytes < 1:
@@ -639 +915,3 @@
-                    relocs = pic_relocations(target.read_bytes())
+                    relocs = policy['relocations'](target.read_bytes())
+                    if arch != 'x86_64' and relocs['forbidden']:
+                        raise ValueError('non-PIC original ARM member: '+str(target))
@@ -647 +925 @@
-                    settings = ir_settings(lines, arch=arch)
+                    settings = policy['settings'](lines)
@@ -652 +930 @@
-                relocs = pic_relocations(data)
+                relocs = policy['relocations'](data)
@@ -772 +1050 @@
-    parser = argparse.ArgumentParser(description='Convert certified x86_64 ThinLTO archives before standard RPM stripping')
+    parser = argparse.ArgumentParser(description='Experimental ARM policy dispatch; x86_64 policy preserved')
@@ -776 +1054 @@
-    parser.add_argument('--arch', choices=['x86_64'], required=True)
+    parser.add_argument('--arch', choices=['x86_64', 'armv7l', 'aarch64'], required=True)
```

## 6. C0环境门禁：启动前停止，未构建ARM包

B已单独提交并推送：`e66396a9e05483ce7d272fe6d1b267df492db41e`。随后进入C的环境检查。
**STOP_BEFORE_C0_GBS**：本任务禁止修改宿主sysctl；已安装的正常GBS跨架构初始化明确包含将宿主`vm.mmap_min_addr`写为0的步骤，当前实际值为`65536`。
按“规定之外停止当前步骤”的无人值守规则，没有执行这一入口，也没有修改GBS、使用替代入口或临时更改系统配置绕过。
这不是实测ARM编译失败、不是新的binfmt执行失败，也不能写成“GBS正常流程不能注册binfmt”；**本轮C0包构建次数为0**。

### 6.1 可复核的入口与停止依据

| 事实 | 证据 |
| --- | --- |
| docs/39两ARM根对应配置可定位 | `/home/linhao/Toolchain/gbs_llvm.conf`的general.buildroot为`~/GBS-ROOT-TIZEN-UNIFIED-LLVM`；SHA `436fd7d66db9262e1b680f63ef15894de1a43578208fc4394b2b73293565011b` |
| 正常GBS把架构交给depanneur | `/usr/lib/python3/dist-packages/gitbuildsys/cmd_build.py:612–620`；ARM不在`:54–63`的32位personality替换表 |
| 默认使用宿主build脚本 | `/usr/bin/depanneur:129`，`/usr/lib/build/build:33–34,1268`；本轮未设置VIRTUAL_ENV/BUILD_DIR替换 |
| x86_64主机执行ARM会选择模拟分支 | `/usr/lib/build/common_functions:23–30,97–124`；`:115–119`发现initvm/qemu-reg后返回需要emulator |
| initvm与注册表实际存在 | `/usr/lib/build/initvm.x86_64`、`/usr/lib/build/qemu-reg`；只stat/读取，未执行chmod/initvm |
| 注册之后明确写宿主sysctl | `/usr/lib/build/init_buildsystem:766–778`，关键`:773`为下方原文 |
| 当前mmap_min_addr | `/proc/sys/vm/mmap_min_addr`：`65536` |
| 当前binfmt注册 | 仅jar/python3.12（另有status/register）；无arm/aarch64注册 |

```sh
# /usr/lib/build/init_buildsystem:769–775
if check_use_emulator ; then
    echo "registering binfmt handlers for cross build"
    "$BUILD_DIR/$INITVM_NAME"
    echo 0 > /proc/sys/vm/mmap_min_addr
    read mmap_min_addr < /proc/sys/vm/mmap_min_addr
```

这是静态路径核查，不声称网络/初始化一定已执行到第773行；它足以说明直接授权外执行会有宿主配置写入风险，故在启动前停下。
对应配置的Base/Unified条目仍是历史日期快照；本轮没有借此更换仓库、发起新GBS或声称其在线状态。
配置安全字段、原始binfmt状态、宿主值、全部源码SHA、原文副本和只读命令输出：`E/c0-preflight/result.json`及同目录。

### 6.2 用户侧注册命令（仅提供，未执行）

下面用本机`qemu-reg`的ELF magic/mask；arm将直接QEMU入口换为`qemu-arm-binfmt`并加P，确保保留argv[0]交给accel-aware dispatcher。
aarch64沿用该表的`qemu-arm64-binfmt:P`。docs/39 §2/§8已记录历史根里这些别名指向`qemu-binfmt`；新根仍必须做实际exec验证。
**命令只解决注册，不会消除GBS第773行的sysctl写入；该冲突须先由用户决定环境政策/入口，再恢复C0。** 不提供或执行sysctl放宽命令，不保证仅注册即可通过整个C0。

```sh
sudo sh -s <<'ROOT'
set -eu
test "$(id -u)" = 0
test -w /proc/sys/fs/binfmt_misc/register
test ! -e /proc/sys/fs/binfmt_misc/aarch64
test ! -e /proc/sys/fs/binfmt_misc/arm
/usr/bin/printf '%s\n' ':aarch64:M::\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\xb7:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff:/usr/bin/qemu-arm64-binfmt:P' > /proc/sys/fs/binfmt_misc/register
/usr/bin/printf '%s\n' ':arm:M::\x7fELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x28\x00:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfa\xff\xff\xff:/usr/bin/qemu-arm-binfmt:P' > /proc/sys/fs/binfmt_misc/register
ROOT
```

使用`printf %s`保留文字形式的`\xNN`；不使用`%b`把`\x00`提前展开成NUL。格式及P/F语义依据[Linux binfmt_misc文档](https://docs.kernel.org/admin-guide/binfmt-misc.html)，仅做文本/ELF魔数匹配校验，未写register。

既有同名条目会使此命令停止，不覆盖他人注册；没有加F把宿主解释器固定到所有chroot。没有挂载binfmt_misc、安装软件或执行以上root命令。

### 6.3 本轮C状态与后续边界

| 要求 | armv7l | aarch64 |
| --- | --- | --- |
| C0极小GBS包/accel exec | NOT RUN：宿主sysctl约束在入口前停止 | NOT RUN：依赖ARM32阶段 |
| C1 prep/configure/仅静态库目标 | NOT RUN | NOT RUN |
| C2真实原命令/ABI/优化级普查 | NOT RUN | NOT RUN |
| C3全量转换/PIC/符号/消费者/两种strip | NOT RUN | NOT RUN |

没有创建新ARM构建根，没有ARM LLVM编译/安装/打包，没有修改ARM参数草案或重试。
候选Source的ARM资格仍是**未认证**；x86不变性的B PASS独立成立。两份已上传补丁、W/llvm及其spec、gbs_llvm.conf保持原样。
后续必须先解除C0入口约束，再按原C0→C1→C2→C3顺序执行；没有从docs/39小样本或本轮夹具推导真实ARM全库PASS。

## 7. 本次收尾与证据清单

B的scope/采样器已退出，项目锁已释放；没有本任务GBS/ninja/rpmbuild/编译器残留或新挂载。
保护SHA复核、进程/挂载/锁状态见`E/final-cleanup.json`、`E/protected-final.json`、`E/lock-released.json`。
B进度与本次停止各一提交并推GitHub；没有Gerrit推送。本报告前§1–4及docs/25–39、41、42原文保持不动。

| 证据 | 内容 |
| --- | --- |
| `E/precheck.json`、`lock-acquired.json` | 空间准入、工作树、项目独占 |
| `E/anchor-metadata.json`、`x86-input-check.json` | 历史基准与225原件身份 |
| `E/candidate.json`、`source-vs-6bd0546a.diff` | 隔离实现身份、完整代码差异 |
| `E/unit-tests.log`、`unit-tests-result.json` | 54相关旧测试+6新正负夹具PASS |
| `E/x86-regression-result.json`、`x86-conversion/summary.json` | 225整档/3864成员/完整索引/后端flags逐项一致 |
| `E/x86-conversion/members/` | 全部逐成员IR设置、命令、RSS、符号、重定位记录 |
| `E/x86-regression-scope/` | 完整scope命令、日志、time、内存/进程采样及回收状态 |
| `E/c0-preflight/` | 未启动C0的真实环境与源码证据；root命令仅文本 |
| `E/b-commit.txt`、`b-push.log` | B阶段已发布的提交与push输出 |

## 8. 2026-10-10 C 续接：初始化政策已解除，固定 Base 仓库门禁停止

### 8.1 授权、现场及输入身份

本轮起点 `e44fb6317811f063de566c012c36ea7b11ed79a8`，主仓库 status 为空。
用户明确允许 GBS 自身的 init_buildsystem/initvm 注册 qemu binfmt，并临时把宿主 vm.mmap_min_addr 写为 0；
§6 的旧政策停止不再作为本轮阻塞。仍不手工注册、不修改其他宿主配置、GBS/build 脚本或仓库。
用户同时明确：配置中的固定 Base/Unified 不可用时立即停止，不自行换源。
本轮 **E_C=`/home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-stage1-c-20261010`**，下列原始输出均位于该新目录；未覆盖 E 的前次证据。

| 核查 | 本轮实际值 / 结果 | 证据 |
| --- | --- | --- |
| /home 可用 | 638,375,489,536 B（594.533 GiB），大于原 120 GiB 空间门槛 | precheck-verified.json |
| /var/tmp 所在文件系统可用 | 380,068,466,688 B | 同上 |
| MemAvailable（只记录；未走构建准入） | 22,380,081,152 B | c0-preflight/host-before.json：21,855,548 kB × 1024 |
| 本项目竞争构建进程 | 0；项目/Rnew 两锁取得，PID 749085 | precheck-verified.json、lock-acquired.json |
| 候选 Source | tools/llvm_static_archives_arm_trial.py，SHA `6a36f173c3efb05c7011aa7029aeb2ae3119e1f77a32536fcc791938bf20c4b7`，与 §5.1 一致 | protected-start.json、protected-final.json |
| ARM GBS 配置 | `/home/linhao/Toolchain/gbs_llvm.conf`，SHA `436fd7d66db9262e1b680f63ef15894de1a43578208fc4394b2b73293565011b` | c0-preflight/config.json |
| 宿主 mmap_min_addr | 启动前核查 65536；停止后 65536 | c0-preflight/host-{before,after}.json |
| binfmt 注册 | 两次均为 jar、python3.12，另有 status/register；未新增 ARM/AArch64 | 同上，保存每个注册条目原文 |

进程扫描首次宽泛匹配到了本会话自身 bash here-document，并非竞争构建；改为排除本会话祖先进程且按可执行名识别后，竞争进程为 0。
两个检查的原始记录分别保存在 precheck.json 和 precheck-verified.json；没有因此终止他人进程或重跑构建。

已安装初始化脚本只读副本、SHA 和宿主写入检索保存在 c0-preflight/init-source-sha.json、*.source.txt、init-host-write-search.txt。
`/usr/lib/build/init_buildsystem:769–775` 的 initvm 与 mmap_min_addr 操作现在属于获批范围。
本轮在仓库可用性检查即停止，初始化程序没有执行，不能把静态检索写成已验证整个初始化没有额外副作用；
后续真正启动时仍须检查授权外宿主配置写入。未触及四个旧根、未创建 /var/tmp 新根。

### 8.2 固定仓库 HTTP 原始结果：Base 404，Unified 200

从上述配置逐节读取唯一 url，追加 `repodata/repomd.xml`；两个独立只读请求于 11:38:47 +08:00 发起，各请求一次，无重试。
使用配置原有 **HTTP** URL，`curl --location` 的最终 URL 与原 URL 相同，没有替换为其他快照、reference、缓存仓库或镜像。

| 仓库 | 配置固定快照 | HTTP | 正文大小 | 正文 SHA256 |
| --- | --- | ---: | ---: | --- |
| Base | tizen-base-toolchain_20260813.050338 | **404** | 146 B，HTML 错误页 | `55f7d9e99b8e2d4e0e193b2f0275501e6d9c1ebd29cadbea6a0da48a8587e3e0` |
| Unified | tizen-unified-toolchain_20260814.092727 | 200 | 4,476 B，repomd.xml | `e7af3f222f0ce958678d964589f2d156e8b47ba463ac0b3b0b96c74663382200` |

实际查询模板（完整展开 argv 分别在 base-http.json / unified-http.json）：

```sh
curl --silent --show-error --location --connect-timeout 15 --max-time 45   --dump-header "$E_C/c0-preflight/NAME-headers.txt"   --output "$E_C/c0-preflight/NAME-body.xml"   --write-out '%{http_code} %{url_effective}\n' "$URL"
```

stdout 原文：

```text
404 http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20260813.050338/repos/standard/packages/repodata/repomd.xml
200 http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20260814.092727/repos/standard/packages/repodata/repomd.xml
```

Base 响应头原文：

```text
HTTP/1.1 404 Not Found
Server: nginx
Date: Sat, 10 Oct 2026 03:39:03 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 146
Connection: keep-alive
```

两个 curl 传输退出码均为 0、stderr 均为空：命令没有使用 --fail，**退出 0 只证明收到 HTTP 响应，不表示仓库可用**；门禁依据是 HTTP 404。
服务器 Date 与本机发起时间分别原样保留，不用服务器时间替代本机计时。
证据：c0-preflight/{base,unified}-{http.json,headers.txt,body.xml,curl.stdout,curl.stderr}。
这证明该固定 Base 元数据端点在本次请求时不可用，不推测服务器为何返回 404。

### 8.3 停止结果及后续依赖

结果码：**STOP_BEFORE_C0_GBS_FIXED_BASE_404**。按本轮仓库规则停止，不发起一个已缺固定包源的 GBS 构建。
这不是 ARM 编译失败、不是 binfmt/accel 实测失败，也不是内存或磁盘不足。

| 要求 | armv7l | aarch64 |
| --- | --- | --- |
| C0 仓库前置检查 | STOP：Base repomd HTTP 404 | 使用同配置；不再进入构建 |
| C0 极小测试包、自动 binfmt、accel exec、guest 程序 | NOT RUN；GBS 0 次 | NOT RUN；GBS 0 次 |
| C1 prep / CMake / 仅静态库目标 | NOT RUN | NOT RUN |
| C2 真实归档、命令/IR/ABI/重定位全集普查 | NOT RUN | NOT RUN |
| C3 转换、索引/符号/PIC、消费者与 GNU/LLVM strip | NOT RUN | NOT RUN |
| C4 aarch64 后续流程 | 不适用 | NOT RUN：armv7l 未完成 |

候选 Source 没有修改，因此没有新 diff / SHA，也未重复 x86 全量回归或单元测试。
§5 的 225 档、3864 成员与 60 测试 PASS 仍是该同 SHA 候选的既有硬证据；不冒充本轮新执行，亦不替代 ARM 认证。
未知 ARM relocation（包括 TARGET2）必须交 PM 的新规则已登记，本轮没有真实 ARM 输入，未触发分类或自行放行。
继续需要指定固定 Base 恢复可用，或另行授权经过身份核对的来源；本轮没有启用 docs/36 本地仓库或改任何配置。

### 8.4 收尾与自检

- GBS、LLVM/Chromium 构建、BOLT、性能校准、归档转换均为 0；未安装软件、未修改宿主配置、未执行清理。
- W/llvm/spec、两个 GBS 配置、原转换 Source、候选 Source、两份已上传补丁的摘要前后相同，见 protected-final.json。
- 没有启动 scope、采样器或构建子进程，没有新挂载；项目锁在收尾释放，见 final-cleanup.json、lock-released.json。
- 原 §1–§7、docs/25–39、41、42 保留不动；仅新增报告开头的当前状态/恢复说明与本 §8，并在同一提交更新 STATUS。
- 本次停止报告提交并推送 GitHub；不推 Gerrit。提交号用 `git log -1 -- docs/40_arm_archive_conversion_stage1.md` 定位，推送输出保留 E_C/git-push.log。

收尾 `df -h` 原始输出：

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       1.8T  1.2T  595G  66% /home
/dev/nvme0n1p1  468G   90G  354G  21% /
```

全部证据留 E_C，日志/元数据仅本机；本次没有需提交的新 Source 或脚本。
