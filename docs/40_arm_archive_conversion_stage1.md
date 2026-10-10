# 40 ARM 静态库转换第一段：历史记录与 C 阶段续接

> **最新状态（2026-10-10，§11）：armv7l 标准完整 `%build` PASS，7,147任务/1,998.953884s；210开发归档普查完成。C3在 `libLLVMARMCodeGen.a(ARMAsmPrinter.cpp.o)` 的未认证 `R_ARM_TLS_GD32`（104）处停止。** 没有OOM，未扩展规则或重试转换；消费者/strip与aarch64均未执行。构建树、缓存和失败现场保留，Source未改。
>
> **用户恢复命令：`sudo sysctl -w vm.mmap_min_addr=65536`。** 宿主开场和结束均为 0，本轮允许 GBS 标准初始化保持此值；结束不代恢复。重启也会重新加载系统配置、恢复该非持久化修改。GBS 注册条目保留，代理未手工注册。以下 §1–§10 保留历史状态，当前结论见 §11。

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

## 9. 2026-10-10 新配置续接：C0 通过，C1 导出校验器错误停止

本节取代 §8 的**当前**包源阻塞；不改判前次 404、§6 的历史政策停止或 §5 的 x86 PASS。
本轮 11:53 +08:00 开场；两次 C0 于 12:03/12:14 结束，导出检查于 12:16 停止。结果码：**STOP_C1_EXPORT_VALIDATOR_VCS_METADATA**。
**停止由代理编写的过严 SHA 断言造成，责任在本轮执行脚本，不能归因于用户配置、LLVM、GBS 导出或机器故障。**

本节证据缩写：

```text
W  = /home/linhao/Toolchain/development/llvm-optimize
E9 = W/temp/arm-archive-stage1-c-newrepo-20261010
V9 = /var/tmp/llvm-optimize-arm-stage1-20261010
R32 = V9/gbs-c0-armv7l/local/BUILD-ROOTS/scratch.armv7l.0
R64 = V9/gbs-c0-aarch64/local/BUILD-ROOTS/scratch.aarch64.0
```

E9 保存完整命令、stdout/stderr、逐 30 秒资源样本、配置与仓库元数据；V9 保留两根及全部 GBS 缓存。
这些绝对路径下的大文件/日志仅在本机，不上传 GitHub。没有读取或清理用户列出的四个旧根。

### 9.1 独占、输入与用户配置

开场 HEAD=`d1d720eac091475aeeb27cc97853442762734689`；`git status --short` 仅 ` M gbs_llvm.conf`，是用户已说明的修改。
新配置 SHA 为 `28f1caf93cd39738a7da1e0da8d5f945f7372963bb9823a507f9157294272169`，执行前后相同。
旧 Git HEAD 配置 SHA 为 `a3fea7732532db26c11b88407464e0274a6d8b4277623364fe16b6980181b03f`。
**本轮所有 GBS 调用均显式 `-c W/gbs_llvm.conf`，没有使用 `~/Toolchain/gbs_llvm.conf`；未修改或暂存用户配置。**

完整配置 diff（用户改动，不是本轮代理修改）：

```diff
diff --git a/gbs_llvm.conf b/gbs_llvm.conf
index 58d118d..ed58cbb 100644
--- a/gbs_llvm.conf
+++ b/gbs_llvm.conf
@@ -6,7 +6,7 @@ buildroot = /home/linhao/Toolchain/development/llvm-optimize/temp/GBS-ROOT-TIZEN
 repos = repo.base-standard, repo.unified-standard

 [repo.base-standard]
-url=https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20260912.061113/repos/standard/packages/
+url=https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261001.092726/repos/standard/packages/

 [repo.unified-standard]
 url=https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20260814.092727/repos/standard/packages/
```

`precheck.json`：/home 可用 638,372,028,416 B；/var/tmp 可用 380,068,433,920 B；项目竞争构建进程 0。
项目及 Rnew 两锁由 PID 750108 持有，记录在 `lock-acquired.json`，结束释放。
W/llvm/spec、生产 Source、候选 Source、两份评审补丁的 SHA 前后相同，见 `protected-{start,final}.json`。
候选仍为 `6a36f173c3efb05c7011aa7029aeb2ae3119e1f77a32536fcc791938bf20c4b7`；未改参数表或重定位表。

### 9.2 仓库与包身份门禁 PASS

配置中的完整 URL 为上方 diff 的新 Base URL、未变 Unified URL；对每个 URL 追加 `repodata/repomd.xml` 请求一次。
没有换源、reference 解析、旧缓存回退或失败重试。原始 headers/body/命令在 `E9/repositories/`。

| 仓库 / 快照 | HTTP | repomd.xml 字节 | SHA256 |
| --- | ---: | ---: | --- |
| Base / tizen-base-toolchain_20261001.092726 | 200 | 3,558 | `9db4185d657356bc96b0eea8082548014664e469f186619c8e68621d158c29e7` |
| Unified / tizen-unified-toolchain_20260814.092727 | 200 | 4,476 | `e7af3f222f0ce958678d964589f2d156e8b47ba463ac0b3b0b96c74663382200` |

两份 primary 均按 repomd 的 checksum 校验通过。压缩正文 SHA：Base `3600bf6291d9c700f773bb091691b7a5413e99884c86fe8963c55572e0656a69`；Unified `f379273fe499c9e93bf01d4eb754b027d8f674e3c72c3e2b131df968fd7533a1`。
以下包来自 Base，Unified primary 没有同名目标条目；每包下载 URL 与 VCS 见 `repositories/packages.json`。

| NEVRA（含 epoch） | 仓库 | primary 中 RPM SHA256 |
| --- | --- | --- |
| clang-0:22.1.8-1.6.armv7l | Base | `86a60cfa8898b169a4df7edb37f18fc1b30f8863215e2f9a5637d566bbcfb2b8` |
| clang-0:22.1.8-1.7.aarch64 | Base | `49ff306320cfbb20f08f6ee1acc1a5d688e87812bfaa12b536476060237254f9` |
| clang-accel-aarch64-0:0.4-1.1.aarch64 | Base | `3f7204919fe5dfb3d44d140f6f8fdac32311822fc36925f54479151bd6ca7923` |
| clang-accel-armv7l-0:0.4-1.1.armv7l | Base | `989944352d4f85e2e9381c757ece4daf7bdbd0262730da519d1a4d6bba5a058e` |
| clang-accel-x86_64-aarch64-0:0.4-1.1.aarch64 | Base | `00a3ed436cc6a2fffd7c76a03e5d4dc9ead4fa02b4f805a1a74b897e9c275d0e` |
| clang-accel-x86_64-armv7l-0:0.4-1.1.armv7l | Base | `3336a12c1d5c2e0c7eacd3064520340c209163f645f1f083b2d6dd6add4e9b75` |
| llvm-0:22.1.8-1.6.armv7l | Base | `2b3e438ecebcea4ca5182c5bbde8b08f192582dfe6bbb5b72b454fad9321aa5c` |
| llvm-0:22.1.8-1.7.aarch64 | Base | `787ef54171f0aa200261b57e0e0d06c1467d8f1d34927fbb6b5e4677e2b9f1b2` |

clang/llvm 的 VCS 均为 `platform/upstream/llvm#cb67996861d070d68fec2b4c623eed7d20ba2e23`。
accel 包的 0.4 是打包项目版本，**LLVM 主版本以 ELF 自报为准**：两份 RPM 解包中的 `/emul/usr/bin/clang-22` 都为 141,497,504 B，SHA
`31cdc6d78f8dcd471c7519f0bfbc5d57f80e2914ff4ea290702931d2ab80a864`，`clang version 22.1.8`。
两次 GBS 新根内该 ELF 的 SHA 也一致。
原始记录：`accel-check/download-verification.json`、`accel-check/*/identity.json`、`c0-*/check-outputs/gate.json`。

解包 RPM 不自带 `/emul` loader；最初查询器对此作了错误定位，尚未执行 clang 即报 FileNotFound。
只读定位后使用已有 ARM 根的 x86_64 loader 与包内库查询版本；C0 又在各新根中独立查询并编译验证。没有重跑 GBS 包。

### 9.3 C0：两次极小包、binfmt 与 accel/guest 证据

一次 armv7l、一次 aarch64，串行；每根全新。实际 GBS 命令模板如下，两个完整 argv 分别在 `c0-*/launch.json`：

```sh
gbs -c "$W/gbs_llvm.conf" build -A "$ARCH"   -B "$V9/gbs-c0-$ARCH" --threads 1 --include-all   --define '_smp_mflags -j4' "$E9/c0-package-$ARCH"
```

小包沿用测试包 8 GiB 准入/6 GiB cap、MemorySwapMax=0、nice15/ionice3；没有把该 cap 用作 C1 的容量授权。
小 C 文件按 `__arm__`/`__aarch64__` 打印架构；明确分开 `clang -O1 -c` 与链接，再在 `%check` 中运行。
命令及源文件：`prepare_c0.py`、`c0-package-*/packaging/probe.spec`、`c0-*/build.log`。

执行证据：

- `QEMU_STRACE=1 LD_DEBUG=files /usr/bin/clang --version` 以及编译/链接的原始 trace 保存在 `check-outputs/{version,compile,link}.route`。
  armv7l 日志 `c0-armv7l/build.log:537` 自报 22.1.8；aarch64 日志 `c0-aarch64/build.log:538` 同版本。
  两次原生 ARM 入口的运行 trace 实际加载 `/emul/usr/lib64/ld-linux-x86-64.so.2` 和 `/emul/usr/bin/../lib64/` 下的 x86_64 库；
  例如 AArch64 编译进程原文见 `build.log:693–714`，ARM32 见相应 `compile.route`。
  这是实际运行的 loader trace，与 `/usr/bin`、`/emul/usr/bin` 的 ELF 头/哈希和 binfmt 分派共同佐证 accel 路由；不是仅凭 `clang --version` 猜测。
- `readelf -h probe` 分别为 ARM / AArch64；`QEMU_STRACE=1 ./probe` 有 guest 系统调用 trace，返回 0。
  `%check` 原文分别为 `C0_GUEST_OK armv7l`、`C0_GUEST_OK aarch64`，随后各自 `C0_PACKAGE_PASS <arch>`。
  全部 trace、文件头与查询 argv 在 `c0-*/check-outputs/`；两包 GBS 最终均 succeeded 1。

| 时间点 | mmap_min_addr | 注册列表（不含 status/register） |
| --- | ---: | --- |
| 首次 GBS 前，11:57:31 | 65536 | jar、python3.12 |
| armv7l GBS 完成 | 0 | jar、python3.12、arm、armeb、aarch64、riscv64 |
| aarch64 GBS 完成及收尾 | 0 | 同上 |

注册来源已核对：`/usr/lib/build/init_buildsystem:768–774` 调用 initvm 并写 mmap；
随后正常根初始化运行 qemu-linux-user 的 postinstall，按 RPM 脚本重置对应 interpreter。
脚本原文 `c0-*/check-outputs/qemu-linux-user-x86_64-cross-*.scripts.txt:3–19`；执行日志 ARM32 `build.log:196–199`、AArch64 `build.log:197–198`。
最终 arm interpreter 为 `/usr/bin/qemu-arm-binfmt`、aarch64 为 `/usr/bin/qemu-aarch64-binfmt`，均 flags `P`；
initvm 早期临时注册的 `qemu-arm-static` 不能当作最终 accel 路由。
完整 magic/mask 与注册前后 mountinfo 见 `c0-*/host-{before,after}.json`、`final-cleanup-before-unlock.json`。

初始化日志还保留 ARM32 的早期 armeb 条目不存在/写入报错，以及两根 qemu-accel preinstall 时 `liblto_plugin.so` 尚不存在的 mv 提示；
没有隐藏这些行，也没有手工修复。后续正常安装、最终注册、编译和 `%check` 均成功；不把早期提示写成最终门禁 FAIL。
已检索初始化脚本/路径及日志，所见宿主配置写入为获批的 binfmt/mmap 两类；未执行手工注册、其他 sysctl、宿主安装或 GBS/build 脚本修改。
这不是一次对宿主所有文件写入的审计。

GBS 缓存已保留并逐 RPM 登记路径、NEVRA、SHA：

```text
V9/gbs-c0-armv7l/local/cache   # 106 RPM
V9/gbs-c0-aarch64/local/cache # 107 RPM
E9/c0-<arch>/check-outputs/cache-inventory.json
```

### 9.4 新快照宏展开预检 PASS；尚无 LLVM CMakeCache

在上述两新根内用该根 `rpmspec`、`.rpmrc`、`.rpmmacros` 展开相同 cb679968 的 spec。
宏参数沿用 docs/39：`_smp_mflags -j4`、`_srcdefattr (-,root,root)`、`_build_create_debug 1`、`_topdir /home/abuild/rpmbuild`、对应 `--target`。
`--rcfile` 与 `--macros` 显式包含 abuild 配置，避免误用宿主/默认 root 宏。
只执行解析与把 CMake 调用替换为 printf 的变量展开；没有执行 `%build`。

| 对照项 | armv7l | aarch64 |
| --- | --- | --- |
| 完整 CMake argv 与 docs/39 | 逐项相同 | 逐项相同 |
| `%optflags` | 字符串相同 | 字符串相同 |
| CMAKE_C/CXX/ASM_FLAGS | 与 docs/39 附录 A32 完全相同 | 与附录 A64 完全相同 |
| CMAKE_BUILD_TYPE / LLVM_ENABLE_LTO | MinSizeRel / Thin | Release / Thin |
| LLVM/CLANG_LINK_*_DYLIB | ON / ON | ON / ON |
| LLVM_PARALLEL_COMPILE_JOBS / LINK_JOBS | 6 / 2 | 6 / 2 |
| 构建期实际末项优化、IR、归档 | 尚未产生，UNKNOWN | 尚未产生，UNKNOWN |

证据：`macro-precheck/*-{parsed.stdout,build.txt,cmake.json,comparison.json,optflags.stdout}` 与各 `.command.json`。
固定目标 spec SHA `9ee73e37f1297a261b835bcd9c7fa2fbff72e271816950991cbe95be0945edda`。
GBS 从本轮 W 配置取得的 buildconfig 保存在 `buildconfig-from-W.conf`，SHA `1e7610b6a922d27b80eb59c1c78bdf716f7de2e8e24700e0ee7c62522739ed52`。
**这只闭合宏展开一致性，不冒称 LLVM configure/实际对象认证已通过。**

### 9.5 C1 停止点：导出后整文件 SHA 断言未考虑 VCS 元数据

在 E9 的独立 Git clone 中检出 cb679968；原 W/llvm 只作为只读对象来源。
实际执行（完整命令/退出码 `c1-export-commands.jsonl`）：

```sh
gbs -c "$W/gbs_llvm.conf" export   --commit cb67996861d070d68fec2b4c623eed7d20ba2e23   --no-patch-export --outdir-directly --outdir "$E9/c1-export"   "$E9/c1-export-repository"
```

Git clone、checkout 和 GBS export 三个命令均 **exit 0**。GBS 输出：

```text
info: Creating (native) source archive llvm-22.1.8.tar.gz from 'cb67996861d070d68fec2b4c623eed7d20ba2e23'
info: package files have been exported to:
     /home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-stage1-c-newrepo-20261010/c1-export
```

随后 `E9/prepare_c1_export.py:15` 用上述 Git spec SHA 断言导出文件整 SHA，发生 AssertionError，外层退出 1。
导出 spec 实际 SHA 为 `390ac8fce01a807f23d1c3f5906c68e05e71a4747449f2fe01a317343ef9c5dd`。
失败后仅做只读 diff，完整内容如下：

```diff
--- cb679968:packaging/llvm.spec
+++ GBS export llvm.spec
@@ -30,6 +30,7 @@
 %endif

 Name:      llvm
+VCS:       home/linhao/Toolchain/development/llvm-optimize/llvm#cb67996861d070d68fec2b4c623eed7d20ba2e23
 Summary:   The LLVM Project is a collection of modular and reusable compiler and toolchain technologies
 Version:   22.1.8
 Release:   1
```

`/usr/lib/python3/dist-packages/gitbuildsys/cmd_export.py:155` 显式传 `--git-spec-vcs-tag=%s#%(commit)s`，说明来源。
从内存中的导出文本仅去除这一条 VCS 行后，与目标 spec **逐字节相同**；未修改磁盘上的导出文件。
因此编译参数差异为 0，没有证据表明 ARM 配方/源码不兼容。
但本轮执行检查已经失败，遵守“任一步失败即停止、不改后重试”：**没有修检查器重跑 export、没有启动后续 prep/configure 或库构建**。
`c1-prep-plan.json` 只是准备好的计划，未执行；其中新的 `gbs-libraries-armv7l` 根没有创建。

`c1-export-readonly-diagnosis.json` 记录上述结论，`c1-export-inventory.json` 保存成功导出的全部文件 SHA。
外层通用 monitor 的 `chroot command exit status: 1` 是沿用的通用错误文案；本阶段没有执行 chroot，失败点是宿主 Python 断言。
后续恢复应先把**导出身份检查**定义为：VCS 精确匹配目标提交，且除此一行外 spec 同字节，再复用已导出输入；
不能放宽 CMake/编译参数、Source 或 ARM 重定位门禁。本轮只登记这一修正方向，不实施重试。

### 9.6 资源与剩余阶段

使用已有 build guard 的 cgroup、nice/ionice、每 30 秒 free/load/RSS/disk 样本、宿主可用 <2 GiB 中止与采样回收机制。
导出使用 16 GiB 准入/18 GiB cap；它不是 LLVM 编译耗时。全部 scope 为 MemorySwapMax=0，无 OOM。

| 阶段 | 外层 exit | wall 秒 | cap GiB | cgroup MemoryPeak 字节 | 最低宿主 MemAvailable（采样值） | oom_kill |
| --- | ---: | ---: | ---: | --- | --- | ---: |
| c0-armv7l | 0 | 344.287086 | 6 | 3,819,786,240（3.557453 GiB） | 19.849171 GiB | 0 |
| c0-aarch64 | 0 | 418.848787 | 6 | 3,288,268,800（3.062439 GiB） | 20.178913 GiB | 0 |
| c1-source-export | 1 | 106.852313 | 18 | 7,299,203,072（6.797913 GiB） | 19.796204 GiB | 0 |

证据：`stage-summary.json`；各阶段 `launch.json`、`outcome.json`、`time-v.txt`、`samples.jsonl`、`process-memory.jsonl`、`scope-after-rpm.{json,log}`。
这些是环境建立/导出单次资源观测，不作性能结论，不推算 ARM 库构建成本。

| 工作项 | armv7l | aarch64 |
| --- | --- | --- |
| C0 两源、22 版本、binfmt/accel、极小包 guest | PASS | PASS |
| 同新根宏展开对 docs/39 | PASS | PASS |
| C1 原始源码导出 | GBS exit0，导出后代理校验器 exit1，STOP | 未开始 C4 |
| C1 `%prep` / CMakeCache / 安装规则推导静态目标 / Ninja | NOT RUN | NOT RUN |
| C2 原命令/IR/ABI/重定位全集 | NOT RUN | NOT RUN |
| C3 转换、PIC/索引、消费者、GNU/LLVM strip | NOT RUN | NOT RUN |
| C4 构建树处理与后续全流程 | 不适用 | NOT RUN，受 armv7l 停止阻断 |

未修改候选 Source，因此没有相对 6a36f173 的新 diff、新 SHA 或 x86 重跑；§5 的 225 档/3864 成员/60 测试是既有结果，不记成本轮新测试。
未知 relocation（如 TARGET2）的 PM 门禁未触发，不能据 C0 PASS 宣称真实 ARM 归档已经认证。

### 9.7 收尾与证据保全

- 两个极小包各一次；源码 export 一次；LLVM 完整/静态库构建、LLVM `%install`/打包、BOLT、性能校准、Chromium 均 0；未推 Gerrit。
- 三个 scope 收尾均 `ActiveState=inactive / SubState=dead`；每个 outcome 的 sampler_reaped/log_reader_reaped 均 true；无本轮残留构建进程或 V9 下挂载。
- 项目/Rnew 两锁收尾释放；证据 `final-cleanup-before-unlock.json`、`lock-released.json`、`final-cleanup.json`。
- 所有缓存、导出 tarball、独立 clone、根和日志保留。没有磁盘清理，没有删除用户指定保留资产。
- 仅 docs/40 与 STATUS 提交；用户 gbs_llvm.conf 修改仍保持未暂存且字节未变。Source、W/llvm/spec 和两个评审补丁未改。
- 原 §1–§8 和其他历史报告不改；报告开头刷新当前状态/恢复命令；本 §9 与 STATUS 同 commit 推送 GitHub。

收尾磁盘输出：

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       1.8T  1.2T  586G  67% /home
/dev/nvme0n1p1  468G   99G  345G  23% /
```

推送后提交号与原始输出保存在 E9 的 `commit.txt`、`git-push.log`、`remote-head.txt`。

## 10. 2026-10-10 C1 续接：导出核验与 prep 通过，辅助驱动第二次失败停止

本节承接 `2c9081b5195bc2162d05e1a256a131b665bc4d56`，不改判 §9 的历史停止，也不重跑已通过的 C0/B。
用户替换导出身份判据，并授权每个辅助检查/驱动步骤在证明门禁不放宽后修正一次；同一步骤第二次失败必须停止。
**本轮结果：STOP_C1_CONFIGURE_HELPER_SECOND_FAILURE。** 错误发生在代理实现的独立宏查询与驱动准备，责任属于执行辅助脚本；没有 LLVM/GBS 配方编译失败证据。
虽然第二次宏查询输出了完整前导文本，但退出码非零，未忽略退出码、未执行其文本、未进行第三次尝试。

### 10.1 现场、身份与导出复用

```text
W   = /home/linhao/Toolchain/development/llvm-optimize
E10 = W/temp/arm-archive-stage1-c1-20261010
E9  = W/temp/arm-archive-stage1-c-newrepo-20261010
V10 = /var/tmp/llvm-optimize-arm-c1-20261010
R10 = V10/gbs-libraries-armv7l/local/BUILD-ROOTS/scratch.armv7l.0
T   = cb67996861d070d68fec2b4c623eed7d20ba2e23
```

原始数据和辅助脚本均保留在 E10，仅本机；本轮没有修改或发布新转换 Source。
开场主仓库只有用户的 ` M gbs_llvm.conf`；配置 SHA 精确为
`28f1caf93cd39738a7da1e0da8d5f945f7372963bb9823a507f9157294272169`，前后相同，未暂存。
候选 Source SHA 仍为 `6a36f173c3efb05c7011aa7029aeb2ae3119e1f77a32536fcc791938bf20c4b7`。
/home 可用 585.286831 GiB，/var/tmp 可用 344.850224 GiB；未发现竞争构建进程。
项目与 Rnew 两锁由 PID 779218 持有至收尾，见 `precheck.json`、`lock-acquired.json`。
W/llvm/spec、生产 Source 与两份上传补丁摘要均未变，见 `protected-{start,final}.json`。

导出校验使用 `E10/check_export.py`，没有重新运行 GBS export，也没有修改 E9 的导出：

| 项 | 实测结果 |
| --- | --- |
| 额外 VCS 行数 | 恰好 1；`home/linhao/Toolchain/development/llvm-optimize/llvm#cb67996861d070d68fec2b4c623eed7d20ba2e23` |
| 导出 spec SHA | `390ac8fce01a807f23d1c3f5906c68e05e71a4747449f2fe01a317343ef9c5dd` |
| 内存中仅删除这一行后的 SHA | `9ee73e37f1297a261b835bcd9c7fa2fbff72e271816950991cbe95be0945edda`，与 T 的 spec 逐字节相同 |
| 源码 tarball SHA | `4ec43e91d8fa7b340acec9b1c3b292eb4983b718e119ed894add5a3f3b480ab1`；344,932,497 B |
| tarball / git archive 条目数 | 184,836 / 184,836；路径、类型、mode、大小、链接目标、常规文件内容 SHA 全部一致，差异 0 |
| 校验器文本夹具 | 1 正例 + 4 负例通过（缺 VCS、错误提交、重复 VCS、额外内容均拒绝） |
| 所有导出文件 | 大小和 SHA 全部匹配 E9/c1-export-inventory.json，含三架构模型 tarball |

比较基准命令为 `git -C E9/c1-export-repository archive --format=tar --prefix=llvm-22.1.8/ T`；流式读 tar，不解压/重写历史导出。
内容比较不比较 gzip 压缩字节、tar 的时间戳/uid 等容器元数据；实际导出压缩文件另与历史 SHA 完全相同。
证据：`export-identity.json`、`export-tar-manifest.jsonl`、`git-tar-manifest.jsonl`、`export-files-recheck.json`。

### 10.2 新根仅执行 prep：PASS

为避免普通 `gbs build` 进入全部 Ninja 目标和 `%install`，本轮使用其已安装的标准 `/usr/bin/build` 后端的 stage 选项，限定实际 rpmbuild 为 `-bp`。
依据：`/usr/lib/build/build-recipe:49–53` 接收 stage，`build-recipe-spec:113,151–155` 只在未指定时默认 `-ba`，否则传给 rpmbuild。
没有修改宿主 GBS/build 脚本，也没有改 spec。仓库 URL 从 W/gbs_llvm.conf 读取并逐项断言一致；buildconfig 复用 §9 由该配置取得的原件，SHA
`1e7610b6a922d27b80eb59c1c78bdf716f7de2e8e24700e0ee7c62522739ed52`。
本轮没有再次调用 GBS CLI（export/C0 均复用），没有使用另一份 GBS 配置。

成功入口完整命令如下（外层 time/scope/nice/ionice 见 `c1-armv7l-prep-rerun/launch.json`）：

```sh
sudo -n /usr/bin/build --uid 1000:1000 --target armv7l-tizen-linux   --jobs 6 --cachedir "$V10/gbs-libraries-armv7l/local/cache"   --dist "$E9/buildconfig-from-W.conf"   --arch armv7l:armv7el:armv6l:armv5tejl:armv5tel:armv5l:armv4tl:armv4l:armv3l:noarch   "$E9/c1-export/llvm.spec"   --repository https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261001.092726/repos/standard/packages/   --repository https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20260814.092727/repos/standard/packages/   --debug --root "$R10" --define '_smp_mflags -j4' --stage=-bp
```

先把 §9 ARM32 cache 中 106 个可读 RPM 复制至新 cache，逐个 SHA 一致；历史 cache 未改。
GBS 后端追加下载 17 个依赖，结束保留 123 个缓存 RPM，逐文件大小/SHA 见 `cache-final-inventory.json`。
实际根内已装 122 个包，NEVRA 全清单 `root-installed.stdout`，查询退出 0；缓存数不等于已安装包数。
本轮未切仓库、清理缓存或改宿主软件。

`c1-armv7l-prep-rerun/build.log` 原文摘录：

```text
[  107s] Building for target armv7l-tizen-linux
[  107s] Executing(%prep): /bin/sh -e /var/tmp/rpm-tmp.lM1NxU
[  107s] + /bin/gzip -dc /home/abuild/rpmbuild/SOURCES/llvm-22.1.8.tar.gz
[  107s] + /bin/tar -xof -
[  116s] + tar -C mlgo_verify_assets -xzf /home/abuild/rpmbuild/SOURCES/mlgo_arm_model.tar.gz
[  116s] + exit 0
[  116s] linhao-linux finished "build llvm.spec" at Sat Oct 10 05:20:25 UTC 2026.
```

这里的 finished 仅表示授权的 `-bp` 完成，不是 LLVM 构建成功。
初始化正常运行 binfmt/mmap 步骤；开场和结束 mmap 均 0，最终注册列表为 arm/armeb/aarch64/riscv64/jar/python3.12，保留原文于 `precheck.json` 和 `final-cleanup-before-unlock.json`。
未执行手工注册、其他 sysctl 修改、软件安装到宿主或脚本修改；没有把新根内部安装依赖描述成修改宿主包。

### 10.3 宏参数对照 PASS；实际 CMake NOT RUN

`compare_macros.py` 用 R10 原生 rpmspec、abuild 的 rpmrc/rpmmacros、同样的 define 展开 T：
完整 CMake argv、`%optflags` 与 docs/39 **逐字相同**，参数差异字典为空。
日志见 `macro-precheck/armv7l-{comparison.json,cmake.json,build.txt,parsed.stdout}`。
展开值仍为 MinSizeRel、Thin、C/CXX/ASM 公共 -Os、LLVM/CLANG dylib=ON、compile=6/link=2、MLGO jobs=6。
这些是宏展开值，**没有 CMakeCache 关键行可贴**：R10 的 `BUILD/llvm-22.1.8/build/` 尚未创建。
C1 的实际编译器 exec、CMake 默认 flags、静态目标清单/大小、编译耗时与内存均为 NOT RUN/UNKNOWN。
未用宏预检替代真实 CMake 门禁，也未用 §9 小包的 exec trace 冒充本轮 LLVM 编译证据。

### 10.4 辅助脚本缺陷条款：逐项记录

三个辅助动作按顺序列出；前两个修正后通过，第三个同一步骤第二次失败触发本轮停止。
没有把脚本错误包装成 LLVM/GBS 产品不兼容，也没有在失败后放宽编译参数、容量或退出码门禁。

| 辅助步骤 | 首次失败与只读诊断 | 修正与一次重跑 |
| --- | --- | --- |
| 缓存准备 | `os.link` 对 root:0644 的 RPM 报 EPERM；同文件系统、文件可读不可写，`/proc/sys/fs/protected_hardlinks=1`。尚未启动 build | 改为复制到新 cache 并逐个 SHA 校验，106/106 PASS；不改权限、不改历史 cache。原随后启动 driver 因计划未生成也在读取计划时退出，未创建 scope/root |
| prep 驱动 argv | `--stage -bp` 报 `--stage needs an agrument`；`build:800–811` 把以 `-` 开头的独立 ARG 清空，尚未初始化根 | 改成 `--stage=-bp`，纯 shell 解析正负例分别 exit0/1；语义仍严格 `-bp`。一次实际重跑成功，不进入 build/install |
| CMake 驱动前导查询 | standalone `rpmspec --eval '%{__spec_build_pre}'` 用小写 name/version/release，输出还含大写 `%{NAME}` 等和 `%{_docdir}`；辅助脚本断言失败，未执行输出 | 依据根宏 `usr/lib/rpm/macros:237,286,829–844` 改成精确大写包身份、`_docdir=%{_defaultdocdir}` 并加 verbose 查询；**第二次 root rpmspec exit28**，stdout 已展开，但 stderr 输出版本/usage。保留失败，不再修正或执行该前导 |

第二次查询的 stderr 开头：

```text
RPM version 4.14.1
Copyright (C) 1998-2002 - Red Hat, Inc.
This program may be freely redistributed under the terms of the GNU GPL

Usage: rpmspec [OPTION...]
```

完整 argv 与原始 stdout/stderr：`initial-build-pre.*`、`build-pre.*`；第二次 `build-pre.command.json` 明确 `rc: 28`。
`prepare_configure.py` 因 rc 断言向外 exit1。未进一步尝试变更参数组合，不推断 exit28 的全部内部原因，也不声称输出非空就算成功。
本轮**第三次尝试为 0**，C2/C3/C4 均停止；后续恢复需要新的任务授权，并先解决驱动的纯文本宏查询，不能直接跳过其错误。

修正 diff 原件：`helper-cache-fix.diff`（从首次内联命令整理）、`helper-stage-fix.diff`、`helper-configure-fix.diff`；诊断分别为 `helper-*-diagnosis.json`。
下面保存实际改变的逻辑（完整 diff 附于本节末尾）：

`E10/helper-cache-fix.diff`：

```diff
--- prepare_c1.before
+++ prepare_c1.fixed
@@ -1,7 +1,7 @@
 from pathlib import Path
 import json,hashlib,os,configparser,shutil
 W=Path('/home/linhao/Toolchain/development/llvm-optimize'); E=Path(__file__).resolve().parent;old=W/'temp/arm-archive-stage1-c-newrepo-20261010';V=Path('/var/tmp/llvm-optimize-arm-c1-20261010');root=V/'gbs-libraries-armv7l'
-V.mkdir(exist_ok=False);root.mkdir()
+assert V.is_dir() and root.is_dir() and not (root/'local/BUILD-ROOTS').exists()
 for row in json.loads((old/'c1-export-inventory.json').read_text()):
  p=Path(row['path']);assert p.stat().st_size==row['bytes'];assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],str(p)
 (E/'export-files-recheck.json').write_text((old/'c1-export-inventory.json').read_text())
@@ -11,7 +11,9 @@
 source=Path('/var/tmp/llvm-optimize-arm-stage1-20261010/gbs-c0-armv7l/local/cache');copied=[]
 for f in source.rglob('*.rpm'):
  dest=root/'local/cache'/f.relative_to(source);dest.parent.mkdir(parents=True,exist_ok=True)
- os.link(f,dest)
+ assert not dest.exists()
+ shutil.copyfile(f,dest)
  digest=hashlib.sha256(f.read_bytes()).hexdigest()
+ assert hashlib.sha256(dest.read_bytes()).hexdigest()==digest
  copied.append({'source':str(f),'dest':str(dest),'bytes':f.stat().st_size,'sha256':digest})
 (E/'cache-seed.json').write_text(json.dumps(copied,indent=2));(E/'c1-prep-plan.json').write_text(json.dumps(p,indent=2));print('verified export files; copied cached RPMs:',len(copied));print(json.dumps(p,indent=2))
```

`E10/helper-stage-fix.diff`：

```diff
--- c1-prep-plan
+++ c1-prep-plan-fixed
@@ -1,5 +1,5 @@
 {
-  "label": "c1-armv7l-prep",
+  "label": "c1-armv7l-prep-rerun",
   "operation": "standard GBS build backend restricted to rpmbuild -bp; no LLVM compile/install/package",
   "admission_gib": 16,
   "memory_max_gib": 18,
@@ -30,8 +30,7 @@
     "/var/tmp/llvm-optimize-arm-c1-20261010/gbs-libraries-armv7l/local/BUILD-ROOTS/scratch.armv7l.0",
     "--define",
     "_smp_mflags -j4",
-    "--stage",
-    "-bp"
+    "--stage=-bp"
   ],
   "jobs": 6,
   "cmake_compile_jobs": 6,
```

`E10/helper-configure-fix.diff`：

```diff
--- prepare_configure.before
+++ prepare_configure.fixed
@@ -10,7 +10,7 @@
 (E/'macro-precheck-driver.log').write_text(r.stdout+r.stderr);assert r.returncode==0,r.stderr
 c=json.loads((E/'macro-precheck/armv7l-comparison.json').read_text());assert c['status']=='PASS',c
 parsed=json.loads((E/'macro-precheck/armv7l-parsed.command.json').read_text())['argv']
-query=parsed[:parsed.index('--parse')]+['--define','name llvm','--define','version 22.1.8','--define','release 1','--define','buildsubdir llvm-22.1.8','--eval','%{__spec_build_pre}']
+query=parsed[:parsed.index('--parse')]+['-v','--define','NAME llvm','--define','VERSION 22.1.8','--define','RELEASE 1','--define','_docdir %{_defaultdocdir}','--define','buildsubdir llvm-22.1.8','--eval','%{__spec_build_pre}']
 r=subprocess.run(query,capture_output=True,text=True);(E/'build-pre.command.json').write_text(json.dumps(dict(argv=query,rc=r.returncode),indent=2));(E/'build-pre.stdout').write_text(r.stdout);(E/'build-pre.stderr').write_text(r.stderr);assert r.returncode==0,r.stderr
 assert '%{' not in r.stdout,'unexpanded build preamble'
 build=(E/'macro-precheck/armv7l-build.txt').read_text();end=build.index('    ../llvm\n')+len('    ../llvm\n');prefix=build[:end]
```

### 10.5 资源实测与剩余阶段

全部实际 prep 调用均 16 GiB 准入、18 GiB cap、MemorySwapMax=0、nice15/ionice3；6/6/2 记录值未变，尚未运行编译池。
每 30 秒记录 free/loadavg/RSS/disk，宿主 <2 GiB 中止保护沿用；完整原始输出位于两个 prep scope 目录。

| 项 | 错误 argv 的入口 | 修正后仅 prep |
| --- | ---: | ---: |
| 外层 exit | 1 | 0 |
| wall 秒 | 2.116660 | 116.850637 |
| 启动 MemAvailable B | 21,972,795,392 | 22,025,969,664 |
| scope MemoryPeak B | 12,496,896 | 7,616,188,416（7.093128 GiB） |
| 采样最低宿主 MemAvailable B | 21,970,931,712 | 21,977,894,912 |
| memory.events max/oom/oom_kill | 0/0/0 | 0/0/0 |
| sampler/log reader 回收 | true/true | true/true |

峰值含包安装与源码解压的页缓存，不是 ARM 编译/链接或转换内存需求；没有性能结论。
证据：两个 `outcome.json`、`scope-after-rpm.{json,log}`、`samples.jsonl`、`process-memory.jsonl`、`time-v.txt`。
资源摘要 `final-cleanup-before-unlock.json`。宏查询在 scope 外仅执行只读秒级解析，没有运行编译任务。

| 工作项 | armv7l | aarch64 |
| --- | --- | --- |
| C0/B | 沿用 §9/§5 PASS，未重跑 | 沿用 §9 C0 PASS |
| 导出 spec/tarball 身份 | PASS，复用 E9 | 共用输入核验 PASS，不代表 C4 开始 |
| C1 新根初始化、prep | PASS | NOT RUN |
| C1 宏 argv 对 docs/39 | PASS | 沿用 §9，只读旧证据 |
| C1 实际 configure、Cache、静态库目标构建 | NOT RUN：准备脚本第二次失败 | NOT RUN：依赖 ARM32 |
| C2 普查与参数/重定位认证 | NOT RUN | NOT RUN |
| C3 转换、PIC、消费者、两种 strip | NOT RUN | NOT RUN |
| C4 后续流程 | 不适用 | NOT RUN |

候选 Source 未改，没有新参数表/重定位 diff，没有要求触发的新 SHA/x86 全量回归；§5 的既有 PASS 不作为本轮新执行。
ARM 真实归档能力仍未认证；本轮没有产生可用于新 patchset 的 ARM 产物。

### 10.6 收尾

两个 scope 均 inactive/dead，监控/日志线程已回收；V10 下挂载 0，本任务残留构建进程 0。
项目/Rnew 锁在结束释放，证据 `final-cleanup-before-unlock.json`、`lock-released.json`、`final-cleanup.json`。
123 个 GBS 缓存 RPM、完整新根、已展开源码/模型、E9 导出与全部 E10 日志均保留；没有磁盘清理。
收尾 /home 可用 628,360,404,992 B，/var/tmp 可用 362,176,614,400 B。
本轮无 LLVM 静态库编译/完整构建/安装/打包，无 BOLT、性能校准、Chromium 或 Gerrit 推送；仅真实 LLVM prep 一次成功。
只提交 docs/40 与 STATUS，用户的配置修改仍未暂存。§1–§9 原文保留，仅刷新报告开头的当前状态与恢复说明。
提交与 push 原始输出保存 `E10/commit.txt`、`git-push.log`、`remote-head.txt`。

## 11. 2026-10-10 续接：标准 rpmbuild -bc

本节承接 `256d759231d855248da068f1d4c024041fab4b56`。用户弃用代理手工提取/重建 `%build` 前导与 CMake 的路线；本轮没有调用或修正 `prepare_configure.py`。
改用标准 `/usr/bin/build --stage=-bc`，由 rpmbuild 原样执行 `%prep` 与完整 `%build`，允许所有编译/链接目标，禁止 `%install`/打包。
这是本轮新增授权；此前“只编静态库”的历史结果与停止记录不改判。armv7l 失败即阻断 aarch64。

### 11.1 输入、根与资源入口

```text
W   = /home/linhao/Toolchain/development/llvm-optimize
E11 = W/temp/arm-archive-standard-build-20261010
E9  = W/temp/arm-archive-stage1-c-newrepo-20261010
V10 = /var/tmp/llvm-optimize-arm-c1-20261010
R10 = V10/gbs-libraries-armv7l/local/BUILD-ROOTS/scratch.armv7l.0
B10 = R10/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build
```

原始命令、日志、辅助脚本和 JSON 仅保存在 E11；没有覆盖 §10 的证据。
开场主仓库只有用户的 ` M gbs_llvm.conf`，未修改或暂存。项目/Rnew 两锁持有者为 PID 798956。
输入逐 SHA 重核全部通过：配置 `28f1caf93cd39738a7da1e0da8d5f945f7372963bb9823a507f9157294272169`；
buildconfig `1e7610b6a922d27b80eb59c1c78bdf716f7de2e8e24700e0ee7c62522739ed52`；导出 spec `390ac8fce01a807f23d1c3f5906c68e05e71a4747449f2fe01a317343ef9c5dd`；
导出 tarball `4ec43e91d8fa7b340acec9b1c3b292eb4983b718e119ed894add5a3f3b480ab1`，其余导出文件也全匹配 §9 inventory。
本轮按授权只重核摘要，沿用 §10.1 已完成的 VCS/git archive 内容身份核验，没有重新导出。
候选 Source 仍为 `6a36f173c3efb05c7011aa7029aeb2ae3119e1f77a32536fcc791938bf20c4b7`。
证据：`precheck.json`、`protected-start.json`、`export-files-recheck.json`、`lock-acquired.json`。

标准 backend 的 `--noinit` 由 `/usr/lib/build/build:817–820` 设置 DO_INIT=false，跳过已安装包初始化；`:1254–1285` 是被跳过的初始化分支。
仍正常执行 recipe_setup/prepare、根挂载与 rpmbuild；`build-recipe-spec:24–39` 的构建工作目录重新准备和 `%prep` 重新解压均为标准行为。
本轮没有清理磁盘、删除缓存或手工拼装 shell/CMake；只在 §10 同命令上改 stage 并加一次 `--noinit`。
`build-recipe-spec:151–155` 将指定阶段交给 rpmbuild；保留 `--stage=-bc` 的等号写法。

```sh
sudo -n /usr/bin/build --uid 1000:1000 --target armv7l-tizen-linux \
  --jobs 6 --cachedir "$V10/gbs-libraries-armv7l/local/cache" \
  --dist "$E9/buildconfig-from-W.conf" \
  --arch armv7l:armv7el:armv6l:armv5tejl:armv5tel:armv5l:armv4tl:armv4l:armv3l:noarch \
  "$E9/c1-export/llvm.spec" \
  --repository https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261001.092726/repos/standard/packages/ \
  --repository https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20260814.092727/repos/standard/packages/ \
  --debug --root "$R10" --define '_smp_mflags -j4' --stage=-bc --noinit
```

外层由 `run_standard_build.py` 复用原 build guard：`/usr/bin/time -v`、systemd user scope MemoryMax=18G/MemorySwapMax=0、nice15/ionice3；
16GiB 启动准入、spec 并发6/6/2不变。每30秒 free/loadavg/进程树RSS/磁盘样本、每2秒进程 VmHWM/链接目标、宿主可用<2GiB中止、退出回收均沿用。
ARM Cache 检查独立比较 docs/39 的48个显式定义、各语言4种配置追加flags及生成器/BUILD_SHARED_LIBS，共62项；不会执行生成的CMake命令。
BOOL按CMake布尔语义比较，flags按保留次序的token比较（连续空白不影响参数），编译器绝对路径只接受已核验别名。
初始门禁测试1正10负通过；旧残留Cache不得认证新调用，重跑只接收 mtime/size 已改变的新Cache。
证据：`armv7l-plan{,-rerun}.json`、`cache_gate.py`、`cache-gate-tests.txt`、每次 scope 的 `launch.json`/`samples.jsonl`/`process-memory.jsonl`。

### 11.2 辅助检查器一次修正与重跑

首次标准调用确已进入原样 `%build`；CMake打印 Configuring done (64.8s)，但检查器误把 `/bin/<triple>-clang{,++}` 与预期 `/usr/bin/…` 判为不同。
其余60项无差异。监控于76.564500s结束（中止判定约76.5s），尚未进入Ninja。只读诊断证明根内 `bin -> usr/bin`，两种路径均解析为同一 `usr/bin/clang-22`，
device=66305/inode=9080376/70,512B，SHA `23f30bae06a763cfb58ecb3495d1eeb908e305ef0b712018fed47222daf6ce00`。
这是代理路径假设缺陷，不是 LLVM 配方/编译参数差异；原始失败不删除。

修正仅允许上述已核对同inode的两条 `/bin` 别名；每次检查再次核验根内链接关系。
新增正负例：已验证别名通过、未验证别名拒绝、其他路径拒绝、构建类型变化拒绝。
完整 diff 在 `helper-cache-path-fix.diff`、`helper-runner-fix.diff`；只读证据 `helper-path-diagnosis.json`；测试 `cache-path-tests.json`。
按用户辅助脚本条款只重跑一次，backend argv、spec、编译flags和资源规则均不改。
首次停止的 `systemctl --user kill` 返回 Access denied，原文保留；实际 abuild子进程已被终止，标准backend打印失败并回收挂载。
重跑前只读核查：构建进程0、R10挂载0、旧scope inactive/dead；没有遗留并行构建。
首次scope结束后的累计MemoryPeak已不可读，已有采样保留，不把 UNKNOWN 写为0。

重跑的真实CMake门禁于 **78.5s PASS**；完整62项对照 `armv7l-cmake-comparison.json`，原Cache在 `c1-armv7l-build-rerun/CMakeCache.txt`。
本轮辅助重跑次数至此用完；后续产品失败不重试。

### 11.3 C1：原样完整 %build 通过

标准 rpmbuild 的实际 argv 含 `--target=armv7l-tizen-linux -bc`，见 `root-build.command.txt`、`c1-armv7l-build-rerun/execution-observations.jsonl` 首条；没有 `%install`、brp 或 RPM 生成阶段。
成功这一轮从 13:56:29 到 14:29:48，**wall 1,998.953884 s（约33分19秒），Ninja 7,147/7,147，exit0**。
此前一次辅助门禁中止的 configure 不冒充成功构建，也不从证据中抹去。

**实际 CMakeCache 对照**：48个配方显式项、12个按配置追加flags及2个生成器/共享库项全部符合 docs/39 附录A；没有影响编译参数的差异。
完整逐项 expected/actual 在 `armv7l-cmake-comparison.json`，Cache 原文在 `c1-armv7l-build-rerun/CMakeCache.txt`。关键值如下（C/CXX/ASM各行均真实核验）：

```text
CMAKE_C_COMPILER=/bin/armv7l-tizen-linux-gnueabi-clang
CMAKE_CXX_COMPILER=/bin/armv7l-tizen-linux-gnueabi-clang++
CMAKE_ASM_FLAGS=-Os -fstack-protector -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument  -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -march=armv7-a -mtune=cortex-a8 -mlittle-endian -mfpu=neon -mfloat-abi=softfp -mthumb -Wp,-D__SOFTFP__ -D_FILE_OFFSET_BITS=64 -g
CMAKE_C_FLAGS=-Os -fstack-protector -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument  -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -march=armv7-a -mtune=cortex-a8 -mlittle-endian -mfpu=neon -mfloat-abi=softfp -mthumb -Wp,-D__SOFTFP__ -D_FILE_OFFSET_BITS=64 -g
CMAKE_CXX_FLAGS=-Os -fstack-protector -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument  -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -march=armv7-a -mtune=cortex-a8 -mlittle-endian -mfpu=neon -mfloat-abi=softfp -mthumb -Wp,-D__SOFTFP__ -D_FILE_OFFSET_BITS=64 -g
LLVM_USE_LINKER=lld
LLVM_ENABLE_LTO=Thin
LLVM_ENABLE_ASSERTIONS=No
CMAKE_BUILD_TYPE=MinSizeRel
LLVM_TARGETS_TO_BUILD=ARM;BPF
LLVM_BUILD_LLVM_DYLIB=ON
CLANG_BUILD_CLANG_DYLIB=ON
LLVM_LINK_LLVM_DYLIB=ON
CLANG_LINK_CLANG_DYLIB=ON
LLVM_OPTIMIZED_TABLEGEN=ON
LLVM_PARALLEL_COMPILE_JOBS=6
LLVM_PARALLEL_LINK_JOBS=2
CMAKE_C_FLAGS_DEBUG=-g
CMAKE_C_FLAGS_RELEASE=-O3 -DNDEBUG
CMAKE_C_FLAGS_MINSIZEREL=-Os -DNDEBUG
CMAKE_C_FLAGS_RELWITHDEBINFO=-O2 -g -DNDEBUG
CMAKE_CXX_FLAGS_DEBUG=-g
CMAKE_CXX_FLAGS_RELEASE=-O3 -DNDEBUG
CMAKE_CXX_FLAGS_MINSIZEREL=-Os -DNDEBUG
CMAKE_CXX_FLAGS_RELWITHDEBINFO=-O2 -g -DNDEBUG
CMAKE_ASM_FLAGS_DEBUG=-g
CMAKE_ASM_FLAGS_RELEASE=-O3 -DNDEBUG
CMAKE_ASM_FLAGS_MINSIZEREL=-Os -DNDEBUG
CMAKE_ASM_FLAGS_RELWITHDEBINFO=-O2 -g -DNDEBUG
CMAKE_GENERATOR=Ninja
BUILD_SHARED_LIBS=OFF
```

并发由 spec 的 `mlgo_build_jobs=6`/`LLVM_PARALLEL_COMPILE_JOBS=6`/`LLVM_PARALLEL_LINK_JOBS=2` 控制，Ninja 实际 `-j6`，scope外层18GiB/swap0；没有按x86的4/4/1改配方。
`-D…FLAGS_MINSIZEREL` 的末项 `-Os` 在后述3,683个bitcode命令中再次确认；不能用公共flags或其他构建类型的 `-O3` 推翻实际末项。

**实际执行链**：编译 argv 为 `/bin/armv7l-tizen-linux-gnueabi-clang++`，但 `/proc/PID/exe` 与 maps 指向 **R10/emul/usr/bin/clang-22**；
141,497,504 B，SHA `31cdc6d78f8dcd471c7519f0bfbc5d57f80e2914ff4ea290702931d2ab80a864`，版本22.1.8。
例如PID808235的记录保存在 execution-observations.jsonl。构建期自产的 `llvm-min-tblgen`、`llvm-tblgen`、`clang-tblgen` 则观察到 `/usr/bin/qemu-arm -0 <B10/bin/...> <B10/bin/...> ...`；
66个被采样捕获的tablegen执行进程（不声称穷尽所有短进程），见 `build-phase-evidence.json` 与原 `process-memory.jsonl`。
额外exe观察器仅匹配argv前两项，未捕获qemu后第三/四项的tblgen；这里使用完整进程采样的argv证据，不把缺记录误判为accel。

| 阶段/边界 | 实际记录 | 证据（成功轮build.log行号） |
| --- | --- | --- |
| prep | 13:56:31进入，13:56:40进入build，边界差约9s | 19、33 |
| CMake | Configuring 64.9s，Generating 2.4s | 1849–1858 |
| Cache门禁 | 启动后78.520806s PASS | cache-gate.json |
| Ninja | 首个任务完成13:57:49，最后完成14:29:47；完成时间跨度1,918s | 1860、9111 |
| 标准backend完成 | 14:29:47打印finished，外层约14:29:48退出 | 9114；outcome.json |

编译与链接交错，不把这1,918s拆成互斥的“编译wall+链接wall”；各任务列表保存在 `ninja-tasks.json`，构建树 `.ninja_log` 保留细粒度起止。
下表各阶段wall是独立scope端到端时间；C2/C3不是新构建。所有成功保留的scope `memory.events` 的max/oom/oom_kill均0。

| 操作 | exit | wall s | cgroup MemoryPeak B（GiB） | 最低宿主MemAvailable B |
| --- | ---: | ---: | ---: | ---: |
| C1标准-bc | 0 | 1998.953884 | 16,465,817,600（15.334988） | 13,406,343,168 |
| C2 bitcode只读普查 | 0 | 257.691927 | 1,642,967,040（1.530132） | 21,891,801,088 |
| C2原机器码只读普查 | 0 | 4.168496 | 148,410,368（0.138218） | 22,736,642,048 |
| C3副本转换，门禁拒绝 | 1 | 58.487611 | 5,463,015,424（5.087830） | 22,534,610,944 |

C1累计CPU usage 15,025.019980 CPU秒，不是wall；采样67次，单个编译进程最大已观察VmHWM 1,424,624 KiB。
链接期Top10如下（2秒采样的进程VmHWM，短进程可能未覆盖；不能把不同PID峰值相加当整体峰值）：

| 链接输出 | PID | 已观察VmHWM KiB | GiB |
| --- | ---: | ---: | ---: |
| `lib/libclang-cpp.so.22.1` | 827193 | 9,343,716 | 8.910862 |
| `lib/libclang.so.22.1.8` | 834176 | 7,527,116 | 7.178417 |
| `lib/libLLVM.so.22.1` | 823615 | 7,079,624 | 6.751656 |
| `bin/clangd` | 837312 | 4,350,436 | 4.148899 |
| `bin/clangd-fuzzer` | 837272 | 4,345,248 | 4.143951 |
| `bin/llvm-exegesis` | 838318 | 2,966,076 | 2.828671 |
| `lib/liblldb.so.22.1.8` | 831183 | 2,851,968 | 2.719849 |
| `bin/clang-tidy` | 836964 | 2,841,760 | 2.710114 |
| `bin/clangd-indexer` | 837369 | 2,460,660 | 2.346668 |
| `bin/obj2yaml` | 839299 | 2,190,844 | 2.089352 |

资源原始证据：各操作目录的 `launch.json`（完整time/systemd/nice/ionice argv）、`time-v.txt`、`samples.jsonl`、`process-memory.jsonl`、`scope-after-rpm.{json,log}`、`outcome.json`。
第一轮辅助检查中止的scope最终MemoryPeak不可读，不写为0；其已有样本全部保留于 `c1-armv7l-build/`。

构建期间 `/var/tmp` 所在文件系统最少空闲339,707,936,768 B；相对首样本减少22,461,325,312 B。这是30秒采样的文件系统占用变化，包含其他进程活动，不是目录独占峰值。
收尾 `du -sxB1 B10`=22,547,320,832 B；未连续du构建目录，因此**目录自身瞬时磁盘峰值 UNKNOWN**，不能用收尾值假充峰值。`build-summary.json`、`samples.jsonl`、`build-du.txt`为依据。
BUILD、ThinLTO cache、源目录及GBS缓存全保留。

### 11.4 C1安装规则清单与C2普查

从B10全部 `cmake_install.cmake` 的 `TYPE STATIC_LIBRARY` 条目中选安装目标 `/usr/lib`（即ARM32 `%{_libdir}/*.a`）对应开发库；没有执行install。
共 **210档 / 4,652,224,292 B**，全部存在。每项规则文件、行号、源路径、大小、SHA见 `c1-armv7l-build-rerun/static-install-inventory.json`。
不拿x86的225计数硬套ARM32：本次目标仅ARM/BPF；导出spec:648–651的 `%ifnarch %arm` 排除了ARM32的 `libarcher_static.a`。
compiler-rt安装在clang资源目录，不属于本轮static-devel/libomp-devel清单。

普查全部3,690个成员：**3,683 bitcode + 7机器码 + 0其他；thin归档0**。
每成员保留ordinal、同名occurrence、header/data offset、SHA，完整结果 `armv7l-native-census/*.a.json`；原始7机器码的完整重定位、符号目标节及PIC判定另存 `*.relocations.json`。
`armv7l-ir-census/<archive>/<ordinal>.json` 含每bitcode的llvm-dis完整argv/退出码/输出SHA、llvm.commandline、triple、datalayout、函数attrs、PIC/PIE/DWARF/Debug Info元数据及token分类。
不是只抽样一条命令代替全集。

| 认证输入项 | 全集结果 | 证据/解释 |
| --- | --- | --- |
| IR triple | 3,683/3,683 = thumbv7-tizen-linux-gnueabi | IR summary triples |
| PIC/PIE | 3,683/3,683 = PIC2 / PIE0 | module flags及summary |
| 原命令末项优化 | 3,683/3,683 = -Os | settings.policy.optimization |
| 浮点ABI/端序/模式 | 原命令softfp、little-endian、mthumb；thumbv7 triple；候选显式重放softfp/little-endian | 全集recorded_command与flags |
| CPU/features | 3,657个成员含generic CPU及相同ARMv7/NEON/Thumb features；26个无该函数属性记录 | ir-policy-summary.json；不对缺属性者补猜CPU |
| mtune | 命令cortex-a8；未观测tune-cpu属性 | ARM driver当前忽略mtune的依据仍docs/39 §1.3 |
| 后端补回策略 | 全集末项DWARF4、四种section/addrsig开关启用、fp-contract默认on；候选生成flags只有一种 | ir-policy-summary.json policies/settings |
| token分类 | 11,580种token+分类组合（含路径/宏操作数），其中71种以`-`开头的switch+分类/理由组合；未分类0 | IR summary tokens、ir-policy-summary.json switches |
| 调试元数据 | 全量保留DICompileUnit/DISubprogram计数及模块标志 | 每成员JSON debug/retained_ir；未strip |

ARM新增switch类别沿用docs/39 §1.3源码证据：`-march/-mfpu/-mthumb`进入IR/triple/features（ARM.cpp:275–353,664–679），softfp还影响后端FloatABI（Clang.cpp:1475–1491、BackendUtil.cpp:383–391），
little-endian进入datalayout且显式重放（ARM.cpp:34–45），mtune当前仅消费参数（ARM.cpp:660–662），stack protector进入ssp属性（CodeGenModule.cpp:2729–2740）。
完整71项在 `ir-policy-summary.json`，没有发现必须扩展候选命令白名单的token；**这只闭合参数普查，不等于重定位全集/整库转换认证完成**。
候选Source保持6a36f173，参数表没有定稿改动，§5的60测试及225档/3864成员x86 PASS为沿用历史证据，本轮未重跑或伪称新执行。

全部原机器码与已生成转换对象的重定位分列如下。已生成列仅包含2个完成归档中的2成员，加失败归档保留的3个机器码对象；不是3,683个成员的全量转换。

| 类型（数字） | 原机器码：只读ALLOC / 可写ALLOC | 已生成：只读ALLOC / 可写ALLOC | 已生成：非ALLOC |
| --- | ---: | ---: | ---: |
| R_ARM_NONE (0) | 114 / 0 | 612 / 0 | 0 |
| R_ARM_ABS32 (2) | 0 / 5 | 0 / 1557 | 154747 |
| R_ARM_REL32 (3) | 178 / 0 | 1517 / 0 | 0 |
| R_ARM_THM_CALL (10) | 381 / 0 | 4072 / 0 | 0 |
| R_ARM_CALL (28) | 36 / 0 | 0 / 0 | 0 |
| R_ARM_THM_JUMP24 (30) | 5 / 0 | 61 / 0 | 0 |
| R_ARM_TARGET1 (38) | 0 / 0 | 0 / 1 | 0 |
| R_ARM_PREL31 (42) | 192 / 0 | 620 / 0 | 0 |
| R_ARM_GOT_PREL (96) | 59 / 0 | 199 / 0 | 0 |
| R_ARM_TLS_GD32 (104) | 0 / 0 | 3 / 0 | 0 |

原机器码7成员在现有PIC规则下通过；ABS32在可写ALLOC中的使用不属于只读TEXTREL拒绝项。已生成对象中的154,747个非ALLOC ABS32主要落于调试节，原始节名保存在完整relocation JSON，未把非ALLOC计入只读可加载节门禁。
统计解析器对docs/39两架构既有probe与readelf逐类型/计数交叉核对PASS，见 `relocation-parser-tests.json`；没有为统计目的执行新编译。

### 11.5 C3停止：未经认证的TLS重定位104

先把210档逐SHA只读复制到 `E11/armv7l-input/usr/lib/`，再在新 `armv7l-conversion/` 工作；原B10归档未改。
工具用同根accel clang/llvm-dis/llvm-nm，经根内x86_64 loader和独立 `--library-path` 显式执行；实际ELF/包装器路径及SHA见 `armv7l-conversion-tools.json`。
此路径不依赖宿主安装或ARM binfmt来转换；与C1 bitcode生产者是同一个accel clang22 ELF。

转换flags原样为：

```sh
--no-default-config --target=thumbv7-tizen-linux-gnueabi -x ir -Os \
  -ffunction-sections -fdata-sections -funique-section-names -faddrsig \
  -g -gdwarf-4 -ffp-contract=on -c -fPIC -mfloat-abi=softfp -mlittle-endian
```

4workers，每命令prlimit AS=4GiB/core0，外层18GiB/swap0/nice15/ionice3/监控回收不变；没有传-flto。
转换函数运行44.910675s，含复制/版本核验等的scope端到端58.487611s，退出1。
**cgroup峰5,463,015,424 B，memory.events全0；停止不是OOM或超时。**
仅完成 `libLLVMABI.a`、`libLLVMARMAsmParser.a`，各1成员，其身份/索引/符号检查通过；其余208档不能宣称转换PASS。

原始停止输出：

```text
ValueError: uncertified armv7l relocation 104 at section 422
status: FAILED
reason: uncertified armv7l relocation 104 at section 422
```

出处：`c3-armv7l-convert/build.log`、`armv7l-conversion/summary.json`；候选Source:588–594明确将TLS留待认证，:624–625遇未认证类型抛异常。
未修改Source、未再次转换、未增加例外。并行在途进程由候选cancel回收；后续只读取保留对象。

| 定位项 | 实测 |
| --- | --- |
| 归档 | libLLVMARMCodeGen.a |
| 成员身份 | ordinal=1（从0起）、name=ARMAsmPrinter.cpp.o、occurrence=1 |
| 原bitcode SHA | b4f1996101f6c3623b7778d3d4084a98affadddda847506a263635c12095f0e0 |
| 保留机器码SHA | 5de46a0524f45460fcecf1369ffb26ac0e776479c4c613e61d340fcf94f06b79 |
| 编译命令本身 | exit0，0.481047s，wait4 maxRSS467,376KiB；后续PIC策略抛错 |
| 新类型 | 104 = R_ARM_TLS_GD32；3处，都在不可写SHF_ALLOC代码节 |
| 首个目标节 | #422 `.text._ZSt9call_onceIRFvRN4llvm12PassRegistryEEJSt17reference_wrapperIS1_EEEvRSt9once_flagOT_DpOT0_` |
| 此节offset 0x4c/0x50 | `_ZSt15__once_callable` / `_ZSt11__once_call`，均SHN_UNDEF |
| 第三处offset 0x18 | `.text._ZZNSt9once_flag18_Prepare_executionC1IZSt9call_onceIRFvRN4llvm12PassRegistryEEJSt17reference_wrapperIS4_EEEvRS_OT_DpOT0_EUlvE_EERSB_ENUlvE_8__invokeEv` → `_ZSt15__once_callable` |

只读 `llvm-dis` 原bitcode证明两符号本来就是 `external thread_local`；不是转换助手临时注入TLS（`conversion-stop-diagnosis/failed-member-tls-ir-excerpt.txt` 原IR第355–356行）。
完整 `readelf -rW/-SW/-AW`、命令退出码、全部5对象重定位存于 `conversion-stop-diagnosis/`。
转换stderr还有 `warning: overriding the module target triple with armv7-tizen-linux-gnueabi [-Woverride-module]`，原文保留；输入是thumbv7，输出attributes含Thumb-2、VFPv3、NEONv1和Prefer Size。
本轮未完成全部ARM attributes/浮点ABI及运行验证，不能仅据这些属性把全库兼容性写成PASS。

**ABI与lld依据（全部只读，供PM裁决）：**

- `llvm/llvm/include/llvm/BinaryFormat/ELFRelocs/ARM.def:111`：0x68即R_ARM_TLS_GD32。
- `temp/arm-archive-feasibility-20261009/aaelf32.stdout:1974` 的AAELF32表将它定义为 `GOT(S)+A-P`；:2595–2599说明GOT新增两项，由TLS_DTPMOD32/TLS_DTPOFF32动态重定位，代码位置记录到GOT首项的偏移。原文来源仍docs/39 §4所存ARM ABI。
- `llvm/lld/ELF/Arch/ARM.cpp:147–148` 返回 `R_TLSGD_PC`；:615–622写32位最终值；:893–899按32位有符号取addend。`llvm/llvm/lib/Target/ARM/MCTargetDesc/ARMELFObjectWriter.cpp:230` 也映射该类型。

据此建议PM评估：将**104这一种**作为TLS GD的PC相对/GOT路径另行认证，不能把所有TLS编号自动归为安全，也不能把它直接当只读节S+A绝对重定位。
所需下一轮证据应包括TLS正例、只读绝对重定位负例、GNU ld/lld真实共享链接无TEXTREL、运行TLS路径，以及Source改动后的全部测试/225档x86 SHA回归。
这是分类建议，**本轮未批准、未实现、未验证该扩展**。未知重定位触发的是用户规定的停止边界；C2整库重定位认证未闭合，C3消费者/strip和C4全部停止。

### 11.6 C1全部开发静态库清单

每行大小为转换前构建树原件，归档按名字排序；逐成员格式/索引完整表在 `armv7l-native-census/`，规则路径/行号/SHA在 `static-install-inventory.json`。

| 归档 | B | bitcode / 机器码成员 |
| --- | ---: | ---: |
| libLLVMABI.a | 25,442 | 1 / 0 |
| libLLVMARMAsmParser.a | 3,792,182 | 1 / 0 |
| libLLVMARMCodeGen.a | 59,419,974 | 49 / 0 |
| libLLVMARMDesc.a | 5,842,962 | 13 / 0 |
| libLLVMARMDisassembler.a | 1,834,704 | 1 / 0 |
| libLLVMARMInfo.a | 92,702 | 1 / 0 |
| libLLVMARMUtils.a | 139,368 | 1 / 0 |
| libLLVMAggressiveInstCombine.a | 3,174,222 | 2 / 0 |
| libLLVMAnalysis.a | 130,965,992 | 125 / 6 |
| libLLVMAsmParser.a | 10,123,838 | 4 / 0 |
| libLLVMAsmPrinter.a | 30,437,626 | 27 / 0 |
| libLLVMBPFAsmParser.a | 492,810 | 1 / 0 |
| libLLVMBPFCodeGen.a | 19,250,366 | 26 / 0 |
| libLLVMBPFDesc.a | 849,804 | 5 / 0 |
| libLLVMBPFDisassembler.a | 227,322 | 1 / 0 |
| libLLVMBPFInfo.a | 90,460 | 1 / 0 |
| libLLVMBinaryFormat.a | 3,131,190 | 14 / 0 |
| libLLVMBitReader.a | 11,420,226 | 5 / 0 |
| libLLVMBitWriter.a | 7,282,914 | 4 / 0 |
| libLLVMBitstreamReader.a | 638,212 | 1 / 0 |
| libLLVMCAS.a | 7,900,924 | 15 / 0 |
| libLLVMCFGuard.a | 764,388 | 1 / 0 |
| libLLVMCFIVerify.a | 2,171,826 | 2 / 0 |
| libLLVMCGData.a | 4,941,728 | 7 / 0 |
| libLLVMCodeGen.a | 244,598,490 | 237 / 1 |
| libLLVMCodeGenTypes.a | 94,214 | 1 / 0 |
| libLLVMCore.a | 81,690,084 | 80 / 0 |
| libLLVMCoroutines.a | 12,727,732 | 11 / 0 |
| libLLVMCoverage.a | 7,017,856 | 3 / 0 |
| libLLVMDTLTO.a | 496,468 | 1 / 0 |
| libLLVMDWARFCFIChecker.a | 1,594,476 | 4 / 0 |
| libLLVMDWARFLinker.a | 117,712 | 2 / 0 |
| libLLVMDWARFLinkerClassic.a | 6,812,322 | 4 / 0 |
| libLLVMDWARFLinkerParallel.a | 15,450,442 | 11 / 0 |
| libLLVMDWP.a | 1,388,918 | 2 / 0 |
| libLLVMDebugInfoBTF.a | 1,233,358 | 2 / 0 |
| libLLVMDebugInfoCodeView.a | 14,943,678 | 40 / 0 |
| libLLVMDebugInfoDWARF.a | 24,478,376 | 29 / 0 |
| libLLVMDebugInfoDWARFLowLevel.a | 1,017,386 | 3 / 0 |
| libLLVMDebugInfoGSYM.a | 7,960,830 | 14 / 0 |
| libLLVMDebugInfoLogicalView.a | 25,716,962 | 19 / 0 |
| libLLVMDebugInfoMSF.a | 1,741,854 | 4 / 0 |
| libLLVMDebugInfoPDB.a | 29,660,016 | 93 / 0 |
| libLLVMDebuginfod.a | 2,125,194 | 4 / 0 |
| libLLVMDemangle.a | 1,904,428 | 6 / 0 |
| libLLVMDiff.a | 1,289,042 | 3 / 0 |
| libLLVMDlltoolDriver.a | 692,412 | 1 / 0 |
| libLLVMExecutionEngine.a | 3,087,694 | 5 / 0 |
| libLLVMExegesis.a | 15,972,510 | 25 / 0 |
| libLLVMExtensions.a | 26,526 | 1 / 0 |
| libLLVMFileCheck.a | 2,702,756 | 1 / 0 |
| libLLVMFrontendAtomic.a | 557,914 | 1 / 0 |
| libLLVMFrontendDirective.a | 51,068 | 1 / 0 |
| libLLVMFrontendDriver.a | 101,954 | 1 / 0 |
| libLLVMFrontendHLSL.a | 2,030,646 | 6 / 0 |
| libLLVMFrontendOffloading.a | 3,510,196 | 3 / 0 |
| libLLVMFrontendOpenACC.a | 177,290 | 1 / 0 |
| libLLVMFrontendOpenMP.a | 9,248,660 | 4 / 0 |
| libLLVMFuzzMutate.a | 4,476,832 | 4 / 0 |
| libLLVMFuzzerCLI.a | 337,610 | 1 / 0 |
| libLLVMGlobalISel.a | 30,147,258 | 30 / 0 |
| libLLVMHipStdPar.a | 1,085,640 | 1 / 0 |
| libLLVMIRPrinter.a | 198,716 | 1 / 0 |
| libLLVMIRReader.a | 512,094 | 1 / 0 |
| libLLVMInstCombine.a | 37,689,278 | 15 / 0 |
| libLLVMInstrumentation.a | 47,708,904 | 28 / 0 |
| libLLVMInterfaceStub.a | 2,723,222 | 3 / 0 |
| libLLVMInterpreter.a | 2,416,896 | 3 / 0 |
| libLLVMJITLink.a | 43,572,606 | 35 / 0 |
| libLLVMLTO.a | 19,826,098 | 6 / 0 |
| libLLVMLibDriver.a | 976,986 | 1 / 0 |
| libLLVMLineEditor.a | 268,298 | 1 / 0 |
| libLLVMLinker.a | 3,551,552 | 2 / 0 |
| libLLVMMC.a | 26,456,522 | 70 / 0 |
| libLLVMMCA.a | 5,699,784 | 24 / 0 |
| libLLVMMCDisassembler.a | 750,556 | 5 / 0 |
| libLLVMMCJIT.a | 1,124,214 | 1 / 0 |
| libLLVMMCParser.a | 8,378,256 | 13 / 0 |
| libLLVMMIRParser.a | 6,223,010 | 3 / 0 |
| libLLVMObjCARCOpts.a | 5,609,600 | 8 / 0 |
| libLLVMObjCopy.a | 18,552,910 | 26 / 0 |
| libLLVMObject.a | 35,414,558 | 36 / 0 |
| libLLVMObjectYAML.a | 44,105,786 | 29 / 0 |
| libLLVMOptDriver.a | 6,813,858 | 2 / 0 |
| libLLVMOption.a | 1,696,116 | 4 / 0 |
| libLLVMOrcDebugging.a | 7,714,182 | 7 / 0 |
| libLLVMOrcJIT.a | 85,301,420 | 57 / 0 |
| libLLVMOrcShared.a | 1,112,954 | 7 / 0 |
| libLLVMOrcTargetProcess.a | 10,254,816 | 15 / 0 |
| libLLVMPasses.a | 44,276,622 | 6 / 0 |
| libLLVMPlugins.a | 148,400 | 1 / 0 |
| libLLVMProfileData.a | 31,619,308 | 21 / 0 |
| libLLVMRemarks.a | 5,078,222 | 11 / 0 |
| libLLVMRuntimeDyld.a | 9,434,142 | 8 / 0 |
| libLLVMSandboxIR.a | 9,945,320 | 15 / 0 |
| libLLVMScalarOpts.a | 122,484,048 | 81 / 0 |
| libLLVMSelectionDAG.a | 53,232,102 | 26 / 0 |
| libLLVMSupport.a | 42,826,902 | 175 / 0 |
| libLLVMSupportLSP.a | 2,691,840 | 3 / 0 |
| libLLVMSymbolize.a | 4,653,964 | 5 / 0 |
| libLLVMTableGen.a | 11,453,964 | 14 / 0 |
| libLLVMTableGenBasic.a | 9,194,186 | 13 / 0 |
| libLLVMTableGenCommon.a | 27,154,536 | 23 / 0 |
| libLLVMTarget.a | 1,597,584 | 5 / 0 |
| libLLVMTargetParser.a | 5,495,360 | 15 / 0 |
| libLLVMTelemetry.a | 246,322 | 1 / 0 |
| libLLVMTextAPI.a | 9,727,282 | 15 / 0 |
| libLLVMTextAPIBinaryReader.a | 1,429,868 | 1 / 0 |
| libLLVMTransformUtils.a | 95,795,980 | 94 / 0 |
| libLLVMVectorize.a | 81,883,764 | 33 / 0 |
| libLLVMWindowsDriver.a | 280,432 | 1 / 0 |
| libLLVMWindowsManifest.a | 411,186 | 1 / 0 |
| libLLVMXRay.a | 5,270,752 | 14 / 0 |
| libLLVMipo.a | 109,920,184 | 45 / 0 |
| libclangAPINotes.a | 8,302,588 | 5 / 0 |
| libclangAST.a | 206,299,578 | 114 / 0 |
| libclangASTMatchers.a | 14,691,932 | 3 / 0 |
| libclangAnalysis.a | 44,897,308 | 31 / 0 |
| libclangAnalysisFlowSensitive.a | 20,256,582 | 18 / 0 |
| libclangAnalysisFlowSensitiveModels.a | 11,790,968 | 3 / 0 |
| libclangAnalysisLifetimeSafety.a | 10,639,870 | 10 / 0 |
| libclangAnalysisScalable.a | 886,600 | 4 / 0 |
| libclangApplyReplacements.a | 1,693,662 | 1 / 0 |
| libclangBasic.a | 48,388,308 | 73 / 0 |
| libclangChangeNamespace.a | 5,374,490 | 1 / 0 |
| libclangCodeGen.a | 212,077,212 | 101 / 0 |
| libclangCrossTU.a | 1,830,048 | 1 / 0 |
| libclangDaemon.a | 166,802,672 | 82 / 0 |
| libclangDaemonTweaks.a | 38,055,076 | 20 / 0 |
| libclangDependencyScanning.a | 7,788,878 | 7 / 0 |
| libclangDirectoryWatcher.a | 722,550 | 2 / 0 |
| libclangDoc.a | 22,231,286 | 11 / 0 |
| libclangDocSupport.a | 352,520 | 2 / 0 |
| libclangDriver.a | 70,447,784 | 76 / 0 |
| libclangDynamicASTMatchers.a | 46,342,314 | 5 / 0 |
| libclangEdit.a | 1,584,932 | 3 / 0 |
| libclangExtractAPI.a | 14,100,448 | 6 / 0 |
| libclangFormat.a | 18,450,518 | 23 / 0 |
| libclangFrontend.a | 52,453,336 | 32 / 0 |
| libclangFrontendTool.a | 1,102,922 | 1 / 0 |
| libclangHandleCXX.a | 511,494 | 1 / 0 |
| libclangHandleLLVM.a | 1,530,216 | 1 / 0 |
| libclangIncludeCleaner.a | 10,591,834 | 8 / 0 |
| libclangIncludeFixer.a | 3,783,590 | 6 / 0 |
| libclangIncludeFixerPlugin.a | 922,024 | 1 / 0 |
| libclangIndex.a | 14,611,112 | 9 / 0 |
| libclangIndexSerialization.a | 345,800 | 1 / 0 |
| libclangInstallAPI.a | 9,010,516 | 8 / 0 |
| libclangInterpreter.a | 11,110,778 | 10 / 0 |
| libclangLex.a | 24,364,784 | 25 / 0 |
| libclangMove.a | 4,627,312 | 2 / 0 |
| libclangOptions.a | 1,151,380 | 2 / 0 |
| libclangParse.a | 31,562,240 | 18 / 0 |
| libclangQuery.a | 4,391,262 | 2 / 0 |
| libclangReorderFields.a | 2,852,190 | 2 / 0 |
| libclangRewrite.a | 1,504,354 | 3 / 0 |
| libclangRewriteFrontend.a | 3,401,860 | 8 / 0 |
| libclangSema.a | 331,045,866 | 86 / 0 |
| libclangSerialization.a | 52,197,558 | 17 / 0 |
| libclangStaticAnalyzerCheckers.a | 175,053,686 | 134 / 0 |
| libclangStaticAnalyzerCore.a | 60,015,296 | 49 / 0 |
| libclangStaticAnalyzerFrontend.a | 7,272,060 | 7 / 0 |
| libclangSupport.a | 675,554 | 1 / 0 |
| libclangTidy.a | 10,547,330 | 9 / 0 |
| libclangTidyAbseilModule.a | 31,909,346 | 22 / 0 |
| libclangTidyAlteraModule.a | 6,153,624 | 6 / 0 |
| libclangTidyAndroidModule.a | 13,146,546 | 17 / 0 |
| libclangTidyBoostModule.a | 2,694,844 | 3 / 0 |
| libclangTidyBugproneModule.a | 179,935,082 | 105 / 0 |
| libclangTidyCERTModule.a | 1,611,684 | 1 / 0 |
| libclangTidyConcurrencyModule.a | 2,033,460 | 3 / 0 |
| libclangTidyCppCoreGuidelinesModule.a | 42,523,680 | 32 / 0 |
| libclangTidyCustomModule.a | 1,411,176 | 2 / 0 |
| libclangTidyDarwinModule.a | 1,818,200 | 3 / 0 |
| libclangTidyFuchsiaModule.a | 5,490,844 | 8 / 0 |
| libclangTidyGoogleModule.a | 15,851,726 | 16 / 0 |
| libclangTidyHICPPModule.a | 6,040,358 | 6 / 0 |
| libclangTidyLLVMLibcModule.a | 3,523,396 | 5 / 0 |
| libclangTidyLLVMModule.a | 10,218,496 | 9 / 0 |
| libclangTidyLinuxKernelModule.a | 1,316,198 | 2 / 0 |
| libclangTidyMPIModule.a | 2,195,506 | 3 / 0 |
| libclangTidyMain.a | 1,315,334 | 1 / 0 |
| libclangTidyMiscModule.a | 42,853,622 | 28 / 0 |
| libclangTidyModernizeModule.a | 115,920,184 | 50 / 0 |
| libclangTidyObjCModule.a | 8,040,666 | 10 / 0 |
| libclangTidyOpenMPModule.a | 2,182,744 | 3 / 0 |
| libclangTidyPerformanceModule.a | 31,193,910 | 21 / 0 |
| libclangTidyPlugin.a | 856,222 | 1 / 0 |
| libclangTidyPortabilityModule.a | 4,884,302 | 6 / 0 |
| libclangTidyReadabilityModule.a | 104,989,516 | 59 / 0 |
| libclangTidyUtils.a | 24,428,760 | 23 / 0 |
| libclangTidyZirconModule.a | 411,652 | 1 / 0 |
| libclangTooling.a | 11,578,850 | 17 / 0 |
| libclangToolingASTDiff.a | 5,800,910 | 1 / 0 |
| libclangToolingCore.a | 1,535,658 | 2 / 0 |
| libclangToolingInclusions.a | 1,408,414 | 3 / 0 |
| libclangToolingInclusionsStdlib.a | 1,184,598 | 1 / 0 |
| libclangToolingRefactoring.a | 29,930,300 | 12 / 0 |
| libclangToolingSyntax.a | 8,760,856 | 8 / 0 |
| libclangTransformer.a | 6,737,492 | 7 / 0 |
| libclangdMain.a | 6,746,542 | 2 / 0 |
| libclangdRemoteIndex.a | 98,750 | 1 / 0 |
| libclangdSupport.a | 4,835,052 | 16 / 0 |
| libfindAllSymbols.a | 5,368,494 | 8 / 0 |
| liblldCOFF.a | 25,128,222 | 18 / 0 |
| liblldCommon.a | 4,414,706 | 13 / 0 |
| liblldELF.a | 65,592,590 | 41 / 0 |
| liblldMachO.a | 29,424,804 | 30 / 0 |
| liblldMinGW.a | 684,802 | 1 / 0 |
| liblldWasm.a | 13,214,248 | 14 / 0 |

### 11.7 辅助脚本修正的完整diff与边界

以下仅是E11一次性检查/驱动脚本，未修改任何GBS/build脚本或候选Source。修正证明和正负对照见§11.2。

```diff
--- cache_gate.before.py
+++ cache_gate.py
@@ -23,7 +23,7 @@
    normalize=lambda x:'OFF' if x.upper() in ('0','OFF','FALSE','NO','N','IGNORE','NOTFOUND','') or x.endswith('-NOTFOUND') else 'ON'
    equal=normalize(got)==normalize(exp)
   elif key in ('CMAKE_C_COMPILER','CMAKE_CXX_COMPILER'):
-   equal=got in (exp,'/usr/bin/'+exp)
+   equal=got in (exp,'/usr/bin/'+exp) or (got=='/bin/'+exp and '/bin/'+exp in unused.get('verified_compiler_aliases', []))
   elif key.startswith('CMAKE_') and '_FLAGS' in key: equal=shlex.split(got)==shlex.split(exp)
   else:equal=got==exp
   if not equal:errors.append(f'{key}: expected {exp!r}, found {got!r}')
--- run_standard_build.before.py
+++ run_standard_build.py
@@ -6,7 +6,18 @@
 from run_bolt_stage import summarize
 E=Path(__file__).resolve().parent
 from cache_gate import validate
-guard.validate_cache=validate
+def root_validate(text,parameters,**kwargs):
+ # Only aliases independently verified by device/inode/SHA are accepted.
+ aliases=json.loads((E/'helper-path-diagnosis.json').read_text())['aliases']
+ verified=[]
+ for pair in aliases:
+  a,b=pair
+  # /bin is the relative usr/bin symlink in this root; recheck identity each gate.
+  root=Path(p['command'][p['command'].index('--root')+1])
+  left=root/a['input'].lstrip('/');right=root/b['input'].lstrip('/')
+  if os.readlink(root/'bin')=='usr/bin' and left.stat()==right.stat():verified.append(a['input'])
+ return validate(text,parameters,verified_compiler_aliases=verified)
+guard.validate_cache=root_validate
 p=json.loads(Path(sys.argv[1]).read_text());log=E/p['label'];assert not log.exists();audit=guard.Audit(log)
 available=guard.mem_available();assert available>=p['admission_gib']*guard.GIB,available
 assert hashlib.sha256((W/'gbs_llvm.conf').read_bytes()).hexdigest()=='28f1caf93cd39738a7da1e0da8d5f945f7372963bb9823a507f9157294272169'
@@ -38,6 +49,15 @@
  return tree
 guard.process_tree=traced_tree
 for s in (signal.SIGTERM,signal.SIGINT,signal.SIGHUP):signal.signal(s,lambda sig,frame:(_ for _ in ()).throw(KeyboardInterrupt(str(sig))))
-try:guard.build(audit,SimpleNamespace(buildroot=Path(p['root'])),plan,None,'systemd',command=[sys.executable,'-c',hold,str(completion),str(release),*p['command']],cache_check=True,completion_file=completion,release_file=release)
+# A prior aborted configure cache cannot certify the next standard invocation.
+class CacheRoot:
+ def __init__(self,path):
+  self.path=path;self.parent=path.parent
+  self.previous={str(x):(x.stat().st_mtime_ns,x.stat().st_size) for x in path.glob('local/BUILD-ROOTS/*/home/abuild/rpmbuild/BUILD/llvm-*/build/CMakeCache.txt')}
+  audit.json('previous-cache-signatures.json',self.previous)
+ def glob(self,pattern):
+  for x in self.path.glob(pattern):
+   if self.previous.get(str(x))!=(x.stat().st_mtime_ns,x.stat().st_size):yield x
+try:guard.build(audit,SimpleNamespace(buildroot=CacheRoot(Path(p['root']))),plan,None,'systemd',command=[sys.executable,'-c',hold,str(completion),str(release),*p['command']],cache_check=True,completion_file=completion,release_file=release)
 finally:
  trace.close();summarize(log);audit.stream.close()
```

收尾统计脚本另遇进程已退出时VmHWM字段为空，首次汇总IndexError；只把空字段视作“无样本”后重新解析既有JSON，不改变任何运行/门禁结果，不重跑构建或转换。
缓存收尾目录发现器曾少一级local而输出空清单，已改用§10的123条精确路径逐SHA核验，`cache-retention-check.json` PASS；未以空清单声称缓存通过。
这两处是只读报告汇总修正，不是产品失败重试；保留原始采样和§11.5拒绝结果。

### 11.8 最终状态、保全与收尾

| 工作项 | armv7l | aarch64 |
| --- | --- | --- |
| 配置/buildconfig/E9导出SHA | PASS | 共用输入；未启动新根 |
| C0环境 | 沿用§9 PASS | 沿用§9 PASS，不代表本轮C4 |
| C1完整-bc与Cache | PASS，7,147任务；仅一次完成，之前辅助门禁中止一次 | NOT RUN |
| C2命令/IR/原机器码普查 | 全部210档普查完成、命令分类PASS；整库重定位认证未完成 | NOT RUN |
| C3全量转换 | STOP：104未认证；2/210档完成 | NOT RUN |
| 全库成员/符号/PIC/ABI验收 | 未完成；只读已生成5对象诊断 | NOT RUN |
| GNU ld/lld消费者、共享库、GC、两种strip复验 | NOT RUN | NOT RUN |
| Source改表/测试/x86全量回归 | 没改Source，不触发；§5历史PASS不伪称本轮执行 | NOT RUN |

没有可上传的新ARM patchset；不能把成功 `%build` 等同于ARM转换方案通过。当前需要PM对R_ARM_TLS_GD32认证范围作决定，不是继续修手写CMake驱动。
收尾重新SHA核对210个B10原归档及独立输入副本，全部与C1清单相符（`originals-and-copies-final.json`）；
CMakeCache/build.ninja/.ninja_log与关键ELF摘要保存 `build-resume-anchors.json`，供下一轮原树增量身份核对，不声称授权下一轮安装/打包。
GBS 123缓存RPM逐文件与§10相符；B10、输入/输出副本和失败成员均保留。

保护文件开场/收尾摘要一致：用户配置、W/llvm/spec、候选Source、x86生产Source和两份已上传补丁均未改。用户配置仍只在工作树、未暂存。
5个scope全inactive/dead；所有采样器/日志线程已回收，R10挂载0、本任务残留构建/转换进程0；项目/Rnew两锁结束释放。
证据 `final-cleanup-before-unlock.json`、`lock-released.json`、`final-cleanup.json`。宿主mmap仍0、binfmt列表与开场一致，未手工注册/写sysctl/安装宿主包。
收尾/home可用623,245,197,312 B，/var/tmp可用339,629,785,088 B（`final-df.txt`）；未做任何磁盘清理。
本轮只执行获准标准ARM32 `%prep/%build` 与只读普查/副本转换；无 `%install`/打包、BOLT、性能校准、Chromium或Gerrit推送。

仅docs/40与STATUS同commit推送；§1–§10正文保留，开头更新当前状态。提交与push原始输出保存 `E11/commit.txt`、`git-push.log`、`remote-head.txt`。
