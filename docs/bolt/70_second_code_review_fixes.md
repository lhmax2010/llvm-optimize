# 70. 第二轮代码评审修复（2026-11-06）

本轮代码修复、轻量检查、实物门禁复核和两次 CMake 入口演练均通过。
7706 个成员的重放参数完全一致，保留的 BOLT 中间产物重新 strip、修 RUNPATH、加 debuglink 后，最终 clang 与 63 号产物逐字节相同。
没有完整重建 LLVM 或 RPM；全量归档转换输出和新整包一致性尚未证明，三个源码提交仅保留在本地。

## 1. 提交、归属和资源边界

分支仍为 bolt-on-359934，基线固定 13c3e223d9e1b35e4affb55255c5042f8c940f35。
在原 HEAD 7d5e28ca89ed68e3360765bc4e42234eaaabae27 上制作 BOLT fixup ee58716244c9385da9d70d55514b279c686cca13 和第三提交的 amend/fixup 594676e15f9d4923ee17374095cf9e479b7c5ddb，再执行 GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash 13c3e223d9e1b35e4affb55255c5042f8c940f35。
仍恰好三个提交，混合链接的 SHA/tree 均不变。作者、提交者、Signed-off-by 均为 Hao Lin <hao.lin@samsung.com>，三个 Change-Id 保持原值。

| 标题 | SHA | tree | 标题字符数 |
|---|---|---|---|
| cmake: use hybrid LLVM linkage on x86_64 | a73a7da32049569b1360e9c13d0633c168b8f173 | 3d961cbb04f5446f84d2089b4f65f3178f2bd7fa | 40 |
| packaging: optimize x86_64 clang with BOLT | 7d11ad53629ac7b670664fcbe6aee8348848d5d6 | c2cfd3c7330e4f918806c049efcb9832492f5534 | 42 |
| packaging: fix x86 LLVM flags and archive mode | 5a27edb4265366781f07049ad17a3796f2e05301 | 843bf6573c9ec9c1164535338af02ab9c7c239c5 | 46 |

[完整身份、父链和 trailers](../../tools/bolt/results/rebase-359934-20261106-r2/commit-identities.json)；[三个补丁及全文](../../patches/rebase-359934-20261106-r2/README.md)。
三个 format-patch 在独立临时 index 中从 PS10 顺序应用，得到 tree 843bf6573c9ec9c1164535338af02ab9c7c239c5，与 HEAD 相同（[应用验证](../../tools/bolt/results/rebase-359934-20261106-r2/patch-application.json)）；没有新建分支或改变源码工作树。

除演练沿用原入口限制外，所有命令串行运行在独立 systemd 用户服务中：MemoryMax=8G、MemorySwapMax=0、CPUQuota=400%、Nice=19、IOSchedulingClass=idle。没有 OOM、没有提高限制；服务均打印带时区的结束行。没有完整构建、手动 sudo、文件删除、Gerrit/sandbox/QB 操作。新根及失败夹具保留。

[测试入口、完整 PATH、CMake 版本和包装器 SHA、源码 SHA](../../tools/bolt/results/rebase-359934-20261106-r2/test-invocation.json)。CMake 通过既有 host-tools 包装器在新临时目录执行，未在历史构建根运行 CMake/Ninja/GBS。

## 2. 逐条修复与评审方案

| 评审意见 | 采用的方案与验证 |
|---|---|
| assembler 参数被宽泛 -W 分支放过 | 第三提交在宽泛分支前拒绝 -Xassembler/-Wa,，其他 HQ 分支不改。3 个负例拒绝，-Wall/-Wno-unused 通过。 |
| 三工具可能不是同一版本 | 按 Kimi 方案匹配 clang version X.Y.Z、LLVM version X.Y.Z；保留主版本检查和原返回字段。dis/nm 任一不等均拒绝，同版通过；真实 C-2 也通过实际版本核对。 |
| debug-info 报错重复、-g0 边界 | 保留 expected/found 两个值，去掉括号重复；仅补 -g0 注释，分类逻辑不改。7706 条实际命令中 -g0 为 0。 |
| debuglink 未覆盖 ELF 头和 LOAD 填充 | 第二提交加入 execution_layout=strip_layout(path)，仍只归一化 e_shoff[40,48)、e_shnum[60,62)、e_shstrndx[62,64)，不扩大例外。真实正例和四个单字节负例均符合预期。 |
| 可选诊断吞掉取消 | cli 返回 128+signal；bolt_optional 对 129/130/143 退出整个脚本，其他非零返回 0。只改五处可选调用，失败分支中随后 exit 1 的诊断不动。 |
| 清理取消覆盖原命令失败 | call 保留原错误，生成 CANCELLED: cancelled by signal N; while handling: COMMAND_ERROR: COMMAND_FAILED …。纯取消信息沿用。GateError.cancel_originated 属性决定是否跳过磁盘诊断，混合失败仍诊断。 |
| 混合错误可能再被 TIMEOUT 包装 | run_step 的 TIMEOUT 判断由包含改为 startswith，避免覆盖前置 CANCELLED；TIMEOUT 原路径保持。 |
| 注释与 docstring | rpath_layout 注释放在 docstring 后；Popen/ACTIVE_GROUP 注明第二次信号微秒窗口与 preexec_fn 死锁风险；record_cancel 注明第二次信号终止不恢复旧处理器。 |
| expected-dropped 受环境影响 | 第三提交固定四 token 字面值，上方注明 QB 1214821；环境未设、空值、其他值的行为都一致。 |
| 空 debug 序列提示不清 | debug CFLAGS/CXXFLAGS 序列为空时显示 no debug options；非空序列沿用原格式，不改变编译参数。 |
| 第三提交 MODULE/LDFLAGS 说明 | 明确 Base-Dev MODULE 获得 -z relro、--as-needed、--gc-sections，EXE/SHARED 仍由 spec 指定；补充 assembler 拒绝和三工具版本检查一句。 |

## 3. 测试与预期调整

| 检查 | 本轮结果 | 原始证据 |
|---|---|---|
| 显式 helper 全部既有测试 | 393/393，27.070 s | [helper-02.stderr](../../tools/bolt/results/rebase-359934-20261106-r2/helper-02.stderr)、[helper-02.stdout](../../tools/bolt/results/rebase-359934-20261106-r2/helper-02.stdout) |
| 51/69 参数与转换器回归（既有 42 + HQ 4） | 46/46，17.759 s；显式导入新转换器并打印 SHA | [converter.stderr](../../tools/bolt/results/rebase-359934-20261106-r2/converter.stderr)、[test_regressions.py](../../tools/bolt/results/rebase-359934-20261106-r2/test_regressions.py) |
| 50 号 release 回归 | 5/5 | [converter50.stderr](../../tools/bolt/results/rebase-359934-20261106-r2/converter50.stderr) |
| 53/69 真实 release C-2 #5/#6 | 真实 AArch64AsmParser.cpp.o 正例无 debug 节；注入调试元数据反例拒绝 | [real-c2-result.json](../../tools/bolt/results/rebase-359934-20261106-r2/real-c2-result.json) |
| 本轮新增检查 | 12/12，1.408 s | [new-tests-02.stderr](../../tools/bolt/results/rebase-359934-20261106-r2/new-tests-02.stderr)、[new-tests-02-observed.json](../../tools/bolt/results/rebase-359934-20261106-r2/new-tests-02-observed.json) |
| 真实 ELF strip/debuglink/post | 全通过；3 个 tiny、8 个 real 用例 | [real-gates-result-02.json](../../tools/bolt/results/rebase-359934-20261106-r2/real-gates-result-02.json)、[real-post-result-02.json](../../tools/bolt/results/rebase-359934-20261106-r2/real-post-result-02.json) |
| 两配置完整展开 | 12/12 | [parse-03/expansion-summary.json](../../tools/bolt/results/rebase-359934-20261106-r2/parse-03/expansion-summary.json) |
| Tizen RPM 五项解析 | 5/5 | [parse-03/five-summary.json](../../tools/bolt/results/rebase-359934-20261106-r2/parse-03/five-summary.json) |

C-2 #1–4、#7、#8 与原转换器测试包含在 46 项中；#5/#6 另用 D 保存的真实 bitcode 成员实测，不使用 tools 旧转换器副本。
五个可选调用点分别为 disk-report begin、tool-built、pipeline、cache-release、post。探针从实际 Tizen RPM 展开的函数和调用行构造 /bin/sh -e 脚本，只向 helper 发三种信号：15 个组合退出码均为 143/129/130，后续标记均不执行；5 个普通 rc=1 组合均继续。
post 宏通过测试副本追加 %check 调用 __spec_install_post 展开，发布 spec 不加测试段。命令 rc=1 后清理期间 SIGTERM 的并发例同时保留 COMMAND_FAILED/CANCELLED 并调用磁盘诊断。二次信号及子孙进程清理既有测试继续通过。

| 原预期/准备方式 | 新预期/处理 | 原因 |
|---|---|---|
| 取消测试笼统 nonzero 或 rc=1 | SIGHUP=129、SIGINT=130、SIGTERM=143；纯 Python SIGTERM 从 1 改为 143 | 取消不能被 spec 可选诊断吞掉 |
| expected debug, found release (expected=yes found=no) | expected debug, found release（反向同理） | 去掉重复部分 |
| 环境空 expected-dropped 注入负例 | 环境任何值无效；负例改写副本字面值 | 不允许环境覆盖发布清单 |
| 空调试序列 [] | no debug options | 明确警告含义 |
| 稀疏 checkout 直接读 AddLLVM.cmake | 文件未检出时 git show HEAD:llvm/cmake/modules/AddLLVM.cmake；断言不变 | 首次 helper 唯一 ERROR 为未检出文件 |
| 复制的解析脚本假定 export 有 8 个 Patch | 按本 clone 的 native export 核对，Patch 数 0 | 源码归档实际为 llvm-22.1.8.tar.gz，五项解析完整通过 |
| 普通 rpmspec -P 已可见第 5 个调用 | 测试副本追加 %check 调用 __spec_install_post，实际展开后取第 5 行 | 宏默认不执行；发布 spec 未加测试段 |
| 旧源测试拒绝 -fno-function-sections | 沿用69号对 PS10 的接受/按开关重放预期 | 既有基线行为，非本轮放宽 |

完整清单见 [expectation-adjustments.json](../../tools/bolt/results/rebase-359934-20261106-r2/expectation-adjustments.json)。第一次 helper 缺文件 ERROR、旧解析脚本对象/导出布局错误、post 宏探针准备错误、实物 post 夹具缺 int_lib.h 的原文均保留。实物第二次准备将 compiler-rt builtins 头文件复制到新目录；没有为测试失败放宽发布门禁。成功结果使用 -02/-03 文件名，与失败证据分开。

## 4. 导出与展开逐处比较

GBS native export 成功，源码为最终 HEAD（[命令](../../tools/bolt/results/rebase-359934-20261106-r2/export-command.json)、[输出](../../tools/bolt/results/rebase-359934-20261106-r2/export.stdout)）。
Toolchain build.conf SHA e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945；
Base-Dev SHA 8ace286a5f98f2e02a79be275a64c22a86ea2b0034174c1e293381e181ce3f6a。

各配置覆盖 x86 debug/release 的 BOLT on/off，以及 armv7l/aarch64，共 12 项。相对 7d5e28ca：

- 两配置的 ARM 展开逐字节相同，diff 为空。
- x86 BOLT on 仅 expected-dropped 字面赋值/注释、空调试序列描述、bolt_optional 定义和五处可选调用有变化。
- x86 BOLT off 仅参数函数中上述两处变化。
- 每项按精确允许片段还原后与旧版逐字节相同，全部 *-unexpected.diff 为空。源码末尾 post 宏另有实际展开探针。

全文、原始 diff 和允许片段位于 [parse-03/](../../tools/bolt/results/rebase-359934-20261106-r2/parse-03/)；五项解析覆盖 x86 on/off/一行回退及两个 ARM 架构。

## 5. 参数和转换输出一致性的证据

[replay-summary.json](../../tools/bolt/results/rebase-359934-20261106-r2/replay-summary.json)：

```json
{
  "toolchain": {
    "members": 3853,
    "equal": 3853,
    "mismatches": [],
    "assembler_options": 0,
    "g0": 0
  },
  "basedev": {
    "members": 3853,
    "equal": 3853,
    "mismatches": [],
    "assembler_options": 0,
    "g0": 0
  }
}
```

T 3853 + D 3853 条参数列表逐项相同；-Wa,/-Xassembler 条数 0；-g0 条数 0。每条原命令、新旧列表和成员路径见 [replay-members.jsonl.gz](../../tools/bolt/results/rebase-359934-20261106-r2/replay-members.jsonl.gz)。

helper 的 pipeline、replay_script、add_debuglink、adjust_rpath、tiny_gate、real_gate、post_gate AST 均与旧版相同；全部大写常量及 Source1200 不变。本轮修改检查和取消路径，成功路径生成参数不变。[generation-parameters-proof.json](../../tools/bolt/results/rebase-359934-20261106-r2/generation-parameters-proof.json)。

一个真实 release bitcode 成员用旧/新转换器分别生成原生对象，SHA 均为 ec3c09329a17d0809ac8371d258bf8b9ae364b59b57c0e4f94d123f352696106（[output-sample-result.json](../../tools/bolt/results/rebase-359934-20261106-r2/output-sample-result.json)）。此处仅抽查 **1 个真实成员**，没有全量重转 7706 个成员。

## 6. 保留产物上的门禁复核

只读来源为 63 号 temp/night-20261105/toolchain 的 build/clang-bolt。来源/副本逐个校验 SHA；在本轮新目录使用该根 llvm-strip、llvm-objcopy、loader/运行库处理副本，CMake RPATH_CHANGE 也只改新副本。

| 阶段 | 本轮 SHA | 与保留产物 |
|---|---|---|
| strip-all | 13a07cb7f84bd1ceda4d851c8bd71bddf7ef0c2d4864892eba64cbbb9a0350b8 | 相同 |
| RUNPATH 后 | 8c2429d870f421a29a9914458bc4d4ff2ce359a15e0bdd20f39bfb4580c40bdf | 相同 |
| 重新加 debuglink 后 | e08724d81231d8675c51d4908f4ff0e8d233ef3740c878da1c7eda42dd3532f5 | 相同 |

符号文件 SHA 9942e19c75ffef55f2846e6f1ea60651b4502de6e099c038a3d93bad4f5df690。CRC、debugfiles.list、安装 SHA、别名和安全属性检查通过；post 原函数在新目录安装形态副本上通过 3 个 tiny + 8 个 real 编译检查。没有重新装 RPM、运行平台后处理或执行 BOLT 重写。

| 真正添加 debuglink 后的副本负例 | 文件偏移 | 结果 |
|---|---:|---|
| e_entry 一个字节 | 24 | 拒绝 |
| e_flags 一个字节 | 48 | 拒绝 |
| LOAD 内节间填充一个字节 | 796 | 拒绝 |
| .text 一个字节 | 41938944 | 拒绝 |

[复制清单](../../tools/bolt/results/rebase-359934-20261106-r2/real-gates-copies-02.json)、[完整 argv](../../tools/bolt/results/rebase-359934-20261106-r2/real-gates-calls-02.json)、[正反例](../../tools/bolt/results/rebase-359934-20261106-r2/debuglink-real-cases-02.json)、[原始输出](../../tools/bolt/results/rebase-359934-20261106-r2/real-gates-02.stdout)。

## 7. T/D 串行演练

新入口副本为 tools/bolt/rebase-launch-20261106-r2/，只替换 T 源码路径、新根和服务名前缀。T 继承 night-launch-20261105，D 继承已修复的 rebase-launch-20261106/basedev。
[T 入口 diff](../../tools/bolt/results/rebase-359934-20261106-r2/toolchain-launcher.diff)、[D 入口 diff](../../tools/bolt/results/rebase-359934-20261106-r2/basedev-launcher.diff)；各副本 provenance.json 记录模板 SHA。

源码均为 5a27edb4265366781f07049ad17a3796f2e05301。T 使用 tizen-base-toolchain_20261030.061318，build.conf SHA 8f201a0d58eb634e60a1f213f47fc09dfa953d9869cdc5724f326a76203587bf；
D 使用 tizen-base-dev_20261030.061217，SHA 8ace286a5f98f2e02a79be275a64c22a86ea2b0034174c1e293381e181ce3f6a。
沿用 MemoryMax=MemTotal−8GiB、swap0、CPUQuota1200%、Nice10、ionice2/7。

| 审计 | T | D |
|---|---|---|
| 停止点 | + cmake -G Ninja | + cmake -G Ninja |
| Ninja | 未运行 | 未运行 |
| log-restarts | 0 | 0 |
| 原始/复制日志字节数 | 58806/58806 | 58198/58198 |
| 日志逐字节相同 | PASS | PASS |
| FLAGS 与对应 QB | PASS | PASS |
| WARNING | 0 | 0 |
| 资源报告 | 正常生成 | 正常生成 |
| 残留挂载/进程 | 0/0 | 0/0 |
| prep/build/controller | inactive，Result=success | inactive，Result=success |

### toolchain 原文

```text
TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] CXXFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] LDFLAGS=[]
TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[] CXXFLAGS=[] LDFLAGS=[]
TIZEN_LLVM_FLAGS_WARNING: 0 条
NIGHT_PROJECT 已结束 2026-11-06T21:08:44.399838+08:00 status=ok reason=rehearsal-complete-at-CMake
```

[原日志、行号、清理检查和资源表](../../tools/bolt/results/rebase-359934-20261106-r2/rehearsal-toolchain/)

### basedev 原文

```text
TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[-O2 -fstack-protector-strong -fno-omit-frame-pointer] CXXFLAGS=[-O2 -fstack-protector-strong -fno-omit-frame-pointer] LDFLAGS=[]
TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4] CXXFLAGS=[-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4] LDFLAGS=[]
TIZEN_LLVM_FLAGS_WARNING: 0 条
NIGHT_PROJECT 已结束 2026-11-06T21:17:15.953004+08:00 status=ok reason=rehearsal-complete-at-CMake
```

[原日志、行号、清理检查和资源表](../../tools/bolt/results/rebase-359934-20261106-r2/rehearsal-basedev/)

## 8. 证明边界

| 主张 | 已证明 | 未证明 |
|---|---|---|
| 参数一致 | 7706 条新/旧重放列表相同；helper 成功路径生成代码/常量不变；T/D 演练 FLAGS 与 QB 相同 | 新完整构建所有命令的最终观察 |
| 转换输出一致 | 1 个真实 release 成员的原生对象 SHA 相同；真实 C-2 正反例通过 | 7706 个成员全量重新转换后的逐字节比较 |
| clang 产物一致 | 保留中间产物的新 strip/RUNPATH/debuglink 结果 SHA 与 63 号一致；新 post 门禁通过 | 新源码完整构建后产生的 BOLT 输入/clang |
| 整包一致 | 本轮不作此结论；完成 export、展开、解析 | 新完整构建及逐包/成员比较和平台后处理实测 |

## 9. 相对 7d5e28ca 的完整 diff

仅三个 packaging 文件，67 行新增、23 行删除；六个 CMake 文件不变。

```diff
diff --git a/packaging/clang-bolt-helper.py b/packaging/clang-bolt-helper.py
index eeadcdaf85b1f7f126dd8e9bf0fa8883292cffb8..46b226af11f57d737f86c99a35f4c73ae7f534cc 100644
--- a/packaging/clang-bolt-helper.py
+++ b/packaging/clang-bolt-helper.py
@@ -104,7 +104,9 @@ TINY = ('unsigned bolt_probe(unsigned x, unsigned y) { return (x * 33u) ^ (y + (
         'int bolt_branch(int x) { return x < 0 ? -x : x * 7 + 1; }\n')
 
 class GateError(RuntimeError):
-    pass
+    def __init__(self, message, *, cancel_originated=False):
+        super().__init__(message)
+        self.cancel_originated = cancel_originated
 
 def require(ok, message):
     if not ok:
@@ -192,6 +194,7 @@ def record_cancel(signum, frame):
         if _ACTIVE_GROUP is not None:
             try: os.killpg(_ACTIVE_GROUP, signal.SIGKILL)
             except ProcessLookupError: pass
+        # This second-signal path terminates by signal; original handlers are not restored.
         signal.signal(signum, signal.SIG_DFL)
         os.kill(os.getpid(), signum)
         return
@@ -199,7 +202,9 @@ def record_cancel(signum, frame):
 
 
 def check_cancel():
-    require(_CANCEL_SIGNAL is None, 'CANCELLED: cancelled by signal %s' % _CANCEL_SIGNAL)
+    if _CANCEL_SIGNAL is not None:
+        raise GateError('CANCELLED: cancelled by signal %s' % _CANCEL_SIGNAL,
+                        cancel_originated=True)
 
 
 def peek_child_exit(process, timeout):
@@ -236,6 +241,9 @@ def call(argv, log, cwd=None, timeout=300):
               'SIGCHLD_original': str(previous), 'SIGCHLD_reset_to_default': previous != signal.SIG_DFL})
         with log.open('wb') as output:
             check_cancel()
+            # A microsecond-scale window exists between Popen and _ACTIVE_GROUP:
+            # a second signal here may leave the new process group uncleaned.
+            # Do not use preexec_fn: it risks deadlock in multithreaded programs.
             process = subprocess.Popen(list(map(str, argv)), cwd=cwd, stdout=output,
                                        stderr=subprocess.STDOUT, start_new_session=True)
             _ACTIVE_GROUP = process.pid
@@ -252,8 +260,9 @@ def call(argv, log, cwd=None, timeout=300):
         save(metadata, dict(invocation,completed=True,rc=0))
         return text
     except BaseException as error:
+        cancel_originated = isinstance(error, GateError) and error.cancel_originated
         if primary is None:
-            primary = (str(error) if str(error).startswith('CANCELLED:') else
+            primary = (str(error) if cancel_originated else
                        ('TIMEOUT: ' if isinstance(error, subprocess.TimeoutExpired) else 'COMMAND_ERROR: ')+str(error))
         cleanup = []
         if process is not None and not reaped:
@@ -274,12 +283,12 @@ def call(argv, log, cwd=None, timeout=300):
                 cleanup.append(str(failure))
         if isinstance(error, (KeyboardInterrupt, SystemExit)):
             raise
-        if _CANCEL_SIGNAL is not None:
-            primary = 'CANCELLED: cancelled by signal %s' % _CANCEL_SIGNAL
+        if _CANCEL_SIGNAL is not None and not cancel_originated:
+            primary = 'CANCELLED: cancelled by signal %s; while handling: %s' % (_CANCEL_SIGNAL, primary)
         message = primary+' (see '+str(log)+')'
         if cleanup:
             message += '; cleanup error: '+'; '.join(cleanup)
-        failure = GateError(message)
+        failure = GateError(message, cancel_originated=cancel_originated)
         failure.bolt_log = str(log)
         raise failure from error
     finally:
@@ -563,8 +572,8 @@ def installed_security(baseline, candidate):
 
 
 def rpath_layout(path, allowed_ranges=None):
-    # adjust_rpath has already enforced at most one RPATH/RUNPATH tag.
     """Freeze all bytes except the original path strings, including their NULs."""
+    # adjust_rpath has already enforced at most one RPATH/RUNPATH tag.
     elf = ELF(path)
     try:
         dynamic = elf.by_name.get('.dynamic')
@@ -769,7 +778,8 @@ def debuglink_layout(path):
                  for name, sec in zip(elf.names, elf.sections)
                  if name not in ('', '.shstrtab', '.gnu_debuglink') and sec[1] != 8}
         return {'program_headers': elf.phdrs, 'loaded_sections': loaded, 'other_sections': other,
-                'section_names': sorted(name for name in elf.names if name != '.gnu_debuglink')}
+                'section_names': sorted(name for name in elf.names if name != '.gnu_debuglink'),
+                'execution_layout': strip_layout(path)}
     finally:
         elf.close()
 
@@ -1611,7 +1621,7 @@ def disk_diagnose(step, log, error=None, build=None, work=None, root=None):
 
 
 def diagnose_safely(step, log, error=None):
-    if error is not None and str(error).startswith('CANCELLED:'): return None
+    if isinstance(error, GateError) and error.cancel_originated: return None
     try: return disk_diagnose(step,log,error)
     except Exception: return None
 
@@ -1633,7 +1643,7 @@ def run_step(step, log, argv, output=None, success_marker=None):
         # Preserve the failed command's actual output even when its exit is nonzero.
         try: print(Path(log).read_text(errors='replace'),end='',flush=True)
         except Exception: pass
-        if isinstance(error, GateError) and 'TIMEOUT:' in str(error):
+        if isinstance(error, GateError) and str(error).startswith('TIMEOUT:'):
             failure = GateError('TIMEOUT: step=%s elapsed_seconds=%.3f; %s' %
                                 (step, time.monotonic()-started, error))
             failure.bolt_log = str(log)
@@ -1896,15 +1906,16 @@ def cli():
         signal.signal(sig, record_cancel)
     try:
         main()
-        require(_CANCEL_SIGNAL is None,
-                'CANCELLED: cancelled by signal %s after work completed' % _CANCEL_SIGNAL)
+        if _CANCEL_SIGNAL is not None:
+            raise GateError('CANCELLED: cancelled by signal %s after work completed' % _CANCEL_SIGNAL,
+                            cancel_originated=True)
         return 0
     except (GateError, OSError, ValueError, lzma.LZMAError) as error:
         step = _DISK_CONTEXT.get('step') or (sys.argv[1] if len(sys.argv)>1 else 'helper')
         log = getattr(error,'bolt_log',None) or os.environ.get('BOLT_STEP_LOG','-')
         diagnose_safely(step,log,error)
         print('BOLT_GATE_FAILED: '+str(error),file=sys.stderr)
-        return 1
+        return 128 + _CANCEL_SIGNAL if _CANCEL_SIGNAL is not None else 1
     except Exception as error:
         step = _DISK_CONTEXT.get('step') or (sys.argv[1] if len(sys.argv)>1 else 'helper')
         log = getattr(error,'bolt_log',None) or os.environ.get('BOLT_STEP_LOG','-')
diff --git a/packaging/llvm-static-archives-native.py b/packaging/llvm-static-archives-native.py
index 9921f473b4f5c31bb0ff2dfcc295a75e807ce1e5..cce638977420920abf145db962f9882c6dc3ecc9 100644
--- a/packaging/llvm-static-archives-native.py
+++ b/packaging/llvm-static-archives-native.py
@@ -7,6 +7,8 @@ Text IR metadata/attribute parsing depends on LLVM 22 llvm-dis output syntax.
 Four architecture-specific policy points are deliberately explicit: backend
 options, recorded-command classification, relocation rules, and triple allowlist.
 Failing closed when parameters change is intentional; recertify before use.
+The HQ allowlist accepts -g0 and has_debug_options also counts it as debug.
+Current recorded commands contain no -g0; recheck this on clang upgrades.
 """
 import argparse
 from collections import Counter
@@ -247,6 +249,8 @@ def classify_options(argv, arch='x86_64'):
             category, reason = 'irrelevant', 'pre-link bitcode format already materialized; never replay LTO'
         elif re.fullmatch(r'--param=ssp-buffer-size=\d+', token):
             category, reason = 'ir', 'stack-protector-buffer-size function attribute already in the IR'
+        elif token == '-Xassembler' or token.startswith('-Wa,'):
+            raise ValueError('uncertified assembler option: '+token)
         elif (token.startswith(('-W', '-D', '-I', '--target=', '-fmessage-length=',
                                '-fdiagnostics-color=')) or token in
               ('-fdiagnostics-color', '-fcolor-diagnostics', '-fno-color-diagnostics',
@@ -332,9 +336,9 @@ def ir_settings(lines, require_recorded_options=True, arch='x86_64', debug_info=
         lambda match: chr(int(match[1], 16)), metadata[command_id]))
     found_debug = 'yes' if any(token.startswith('-g') for token in recorded_command) else 'no'
     if debug_info is not None and debug_info != found_debug:
-        raise ValueError('debug-info expected %s, found %s (expected=%s found=%s)' %
+        raise ValueError('debug-info expected %s, found %s' %
                          ('debug' if debug_info == 'yes' else 'release',
-                          'debug' if found_debug == 'yes' else 'release', debug_info, found_debug))
+                          'debug' if found_debug == 'yes' else 'release'))
     policy = classify_options(recorded_command, arch)
     flags = ['--no-default-config', '--target='+triple, '-x', 'ir', policy['optimization'],
              *(('-f'+key) if policy['switches'][key] else ('-fno-'+key)
@@ -566,6 +570,18 @@ def validate_tools(build, compiler, disassembler, nm, command, output):
     match = re.search(r'clang version (\d+)\.', text)
     if not match or int(match[1]) != CERTIFIED_LLVM_MAJOR:
         raise ValueError('uncertified compiler major (required 22): '+text.strip())
+    full_version = re.search(r'clang version (\d+\.\d+\.\d+)\b', text)
+    if not full_version:
+        raise ValueError('missing complete clang version: '+text.strip())
+    for label, tool in [('disassembler', disassembler), ('nm', nm)]:
+        tool_version = output/(label+'-version.txt')
+        with tool_version.open('wb') as stream:
+            command.run([tool, '--version'], output/(label+'-version-command'), stdout=stream)
+        tool_text = tool_version.read_text()
+        match = re.search(r'LLVM version (\d+\.\d+\.\d+)\b', tool_text)
+        if not match or match[1] != full_version[1]:
+            raise ValueError('%s version mismatch: expected %s, found %s' %
+                             (label, full_version[1], match[1] if match else tool_text.strip()))
     return dict(compiler=str(compiler), version=text, compiler_sha256=sha(compiler),
                 disassembler=str(disassembler), nm=str(nm))
 
diff --git a/packaging/llvm.spec b/packaging/llvm.spec
index b6cb759ec86885630f635bb381ed105ab3496f26..53eee9d20d49ba0069eccd8918a2f1b81216182c 100644
--- a/packaging/llvm.spec
+++ b/packaging/llvm.spec
@@ -219,7 +219,8 @@ TIZEN_LLVM_RELEASE=%{llvm_release_build}
 # The x86_64 policy is the certified Toolchain command (QB 1215143).
 # Only architecture and debug-mode options are inherited. Token matching is
 # exact: stripping -fstack-protector must never leave a -strong suffix.
-TIZEN_LLVM_EXPECTED_DROPPED=${TIZEN_LLVM_EXPECTED_DROPPED-'-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4'}
+# Reviewed Base-Dev options (QB 1214821) that this policy knowingly discards.
+TIZEN_LLVM_EXPECTED_DROPPED='-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4'
 tizen_llvm_flags()
 {
     tizen_llvm_kind=$1
@@ -294,8 +295,13 @@ tizen_llvm_flags()
     case $tizen_llvm_kind:$tizen_llvm_release in
         CFLAGS:0|CXXFLAGS:0)
             if test "$tizen_llvm_debug_sequence" != '-g2 -gdwarf-4 -g'; then
-                echo "TIZEN_LLVM_FLAGS_WARNING uncertified debug option sequence: [$tizen_llvm_debug_sequence]"
-                echo "TIZEN_LLVM_FLAGS_WARNING uncertified debug option sequence: [$tizen_llvm_debug_sequence]" >&2
+                if test -n "$tizen_llvm_debug_sequence"; then
+                    tizen_llvm_debug_description="[$tizen_llvm_debug_sequence]"
+                else
+                    tizen_llvm_debug_description="no debug options"
+                fi
+                echo "TIZEN_LLVM_FLAGS_WARNING uncertified debug option sequence: $tizen_llvm_debug_description"
+                echo "TIZEN_LLVM_FLAGS_WARNING uncertified debug option sequence: $tizen_llvm_debug_description" >&2
             fi ;;
     esac
     case $tizen_llvm_kind in
@@ -581,12 +587,23 @@ bolt_checked() {
     exit 1
   fi
 }
+bolt_optional() {
+  if "$@"; then
+    return 0
+  else
+    bolt_optional_rc=$?
+    case $bolt_optional_rc in
+      129|130|143) exit "$bolt_optional_rc" ;;
+      *) return 0 ;;
+    esac
+  fi
+}
 bolt_step() {
   bolt_stage=$1
   shift
   bolt_checked "$bolt_stage" "$BOLT_WORK/$bolt_stage.log" python3 -B %{SOURCE1201} run-step "$bolt_stage" "$BOLT_WORK/$bolt_stage.log" -- "$@"
 }
-python3 -B %{SOURCE1201} disk-report begin || true
+bolt_optional python3 -B %{SOURCE1201} disk-report begin
 echo "BOLT_BUILDROOT_OK %{buildroot}"
 python3 -B %{SOURCE1201} preflight || exit 1
 python3 -B %{SOURCE1201} certified || exit 1
@@ -618,14 +635,14 @@ bolt_checked tool-build "$BOLT_WORK/tool-build.txt" python3 -B %{SOURCE1201} run
 python3 -B %{SOURCE1201} tool-verify "$PWD" "$BOLT_WORK/tool-plan.json" "$BOLT_WORK/tool-build.txt" \
   "$BOLT_WORK/tool-before.json" "$BOLT_WORK/tool-build-verification.json" || exit 1
 cat "$BOLT_WORK/tool-build-verification.json"
-python3 -B %{SOURCE1201} disk-report tool-built || true
+bolt_optional python3 -B %{SOURCE1201} disk-report tool-built
 %if %{llvm_release_build}
 python3 -B %{SOURCE1201} pipeline "$PWD" "$BOLT_WORK" "$PWD/bin/llvm-bolt" || exit 1
 %else
 python3 -B %{SOURCE1201} pipeline "$PWD" "$BOLT_WORK" "$PWD/bin/llvm-bolt" --debug-symbols || exit 1
 %endif
 echo BOLT_PIPELINE_PASS
-python3 -B %{SOURCE1201} disk-report pipeline || true
+bolt_optional python3 -B %{SOURCE1201} disk-report pipeline
 # BOLT configuration/build/rewrite must not change the ordinary installation.
 # Do not reinstall: that would add BOLT libraries, unregistered aliases and exports.
 python3 -B %{SOURCE1201} compare-root "%{buildroot}" "$BOLT_WORK/install-before.json" \
@@ -633,7 +650,7 @@ python3 -B %{SOURCE1201} compare-root "%{buildroot}" "$BOLT_WORK/install-before.
 echo BOLT_COMPARE_ROOT_PASS
 # No subsequent step consumes this ThinLTO cache.
 # Release it only inside the enabled x86_64 BOLT block.
-python3 -B %{SOURCE1201} cache-release "$PWD" "$BOLT_WORK" || true
+bolt_optional python3 -B %{SOURCE1201} cache-release "$PWD" "$BOLT_WORK"
 # Any subsequent buildroot mutation (including native archive conversion) must follow this gate.
 %endif
 %endif
@@ -934,6 +951,6 @@ echo "plugin load /usr/share/dotnet.tizen/netcoreapp/SOS/libsosplugin.so" > /roo
     %{__bolt_original_spec_install_post} \
     python3 -B %{SOURCE1201} post "%{buildroot}" "%{_builddir}/%{buildsubdir}/build/clang-bolt/install-state.json" "%{_builddir}/%{buildsubdir}/build/clang-bolt/ordinary-clang-22" "%{_builddir}/%{buildsubdir}/build/clang-bolt/post-gate" --resource-dir "%{buildroot}%{_libdir}/clang/%{llvm_version}" || exit 1 \
     echo BOLT_POST_GATE_PASS \
-    python3 -B %{SOURCE1201} disk-report post || true
+    bolt_optional python3 -B %{SOURCE1201} disk-report post
 %endif
 %endif
```

结论：轻量检查、实物门禁复核和两个演练通过；三个提交仅本地，未做完整构建，未推 Gerrit/sandbox。

## 10. cli 取消漏洞修复与 sandbox 推送（2026-11-09）

前置 QB 核对见 [71 号](71_qb_1221204_1221207.md)：1221204 / 1221207 都使用 7d5e28ca，三个架构全部成功；34 个二进制包与各自旧 QB 的载荷完全一致、7706 个转换成员 SHA 全同。两份源码包仅 converter 与 spec VCS 变化，严格 FAIL 保留但已完整归因。第一项通过后才执行本节。

本节仅修 cli 的非 GateError 异常路径：已记录取消时打印 traceback，并返回 128+signal；没有取消仍保留原 raise。成功路径没有改动。

### 10.1 修复和提交归属

~~~diff
diff --git a/packaging/clang-bolt-helper.py b/packaging/clang-bolt-helper.py
index 46b226af11f57d737f86c99a35f4c73ae7f534cc..68e20f230c659da78b32bfdc36cdf2b276e6efa5 100644
--- a/packaging/clang-bolt-helper.py
+++ b/packaging/clang-bolt-helper.py
@@ -50,6 +50,7 @@ Separate function symbols with eu-strip (LLVM only-keep-debug crashes on BOLT
 segment layout), then add/verify debuglink. clang-debuginfo carries the matching
 symtab at /usr/lib/debug/usr/bin/clang-22.debug; it contains no source-line DWARF.
 """
+import traceback
 import argparse
 import collections
 import shlex
@@ -1921,6 +1922,9 @@ def cli():
         log = getattr(error,'bolt_log',None) or os.environ.get('BOLT_STEP_LOG','-')
         diagnose_safely(step,log,error)
         print('BOLT_GATE_FAILED: unexpected %s: %s' % (type(error).__name__, error), file=sys.stderr)
+        if _CANCEL_SIGNAL is not None:
+            traceback.print_exc()
+            return 128 + _CANCEL_SIGNAL
         raise
     finally:
         for sig, handler in previous.items():
~~~

基于 5a27edb4 制作 fixup 1c4be1fe6a92；用指定身份执行 GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash 13c3e223d9e1b35e4affb55255c5042f8c940f35，归入第二提交。仍为三个提交，无新分支，三份提交说明和 Change-Id 均未修改。

|顺序|SHA|tree|标题|长度|
|---|---|---|---|---|
|1|a73a7da32049569b1360e9c13d0633c168b8f173|3d961cbb04f5446f84d2089b4f65f3178f2bd7fa|cmake: use hybrid LLVM linkage on x86_64|40|
|2|3dc97ef3a8fae0bbc61b208fa2bc6c369f1146b0|24b6aace2a36bb5840f33ea8fa4da710056ff078|packaging: optimize x86_64 clang with BOLT|42|
|3|c7fd5eed5e35ca335940239cae349a6936f74a7a|24addd0a47a8e7028fe5561cb4f1153bc293d36a|packaging: fix x86 LLVM flags and archive mode|46|

按用户确认的可执行口径核对（[pre-push-proof.json](../../tools/bolt/results/cli-cancel-20261109/pre-push-proof.json)）：

- 首提交 a73a7da3 的 SHA/tree 完全不变。
- 新旧第二提交 diff 只有 helper 上述 4 行；与新旧最终 HEAD 的 diff 逐字相同。
- 第三个提交自身的完整 full-index diff，与 7d11ad53..5a27edb4 逐字节相同；其说明和 Change-Id 不变。
- 三个最后段落都只有 Change-Id、Signed-off-by 两行，git interpret-trailers --parse 可解析。首提交原有顺序是 Signed-off-by 后 Change-Id；首次检查器误要求相反顺序，已按用户“不限定顺序”的条件修正检查器，提交说明未变，记录见 pre-push-check-note.txt。
- 作者、提交者和 Signed-off-by 都是 Hao Lin <hao.lin@samsung.com>；标题均不超过 50 字符，工作区干净。

### 10.2 回归和展开

所有命令串行运行于独立 systemd 用户服务，MemoryMax=8G、swap0、CPUQuota400%、nice19、ionice-c3。没有 OOM、完整构建、演练、sudo 或删除。测试临时文件沿用保全包装器留在新的 temp/cli-cancel-20261109/；历史根只读。

|项目|结果|原文证据|
|---|---|---|
|显式 helper 既有测试|393/393，21.691s|helper.stderr / helper.stdout|
|70 号新增测试|12/12，1.347s|review70.stderr / new-tests-02-result.json|
|本次新增异常取消测试|2/2，0.609s，含 3 种信号子用例|cli-cancel.stderr / cli-cancel-observed.json|
|T/D 完整 spec 展开|12/12，与 5a27edb4 全部逐字节相同|parse/expansion-summary.json 及全部 stdout / 空 diff|

总计 407 项通过。既有测试预期没有改变；70 号测试副本只替换新临时目录。新增用例对同一 KeyError 分别运行旧/新 helper：取消后的旧版 rc=1，新版 SIGHUP=129、SIGINT=130、SIGTERM=143，stderr 都含 traceback 和 KeyError；未取消的新旧均 rc=1、仍重新抛出，诊断保持调用。traceback 的文件名/源码行号不同不作为行为差异。

展开用 70 号相同的 Tizen rpm/loader、Toolchain build.conf e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945 和 Base-Dev 8ace286a5f98f2e02a79be275a64c22a86ea2b0034174c1e293381e181ce3f6a；每配置覆盖 x86 debug/release × BOLT on/off、armv7l、aarch64。源码 spec 本身也逐字节未变。只做展开，不做 export 或构建。

~~~text
Ran 393 tests in 21.691s
OK
Ran 12 tests in 1.347s
OK
Ran 2 tests in 0.609s
OK
EXPANSIONS_PASS 12 ALL_BYTE_IDENTICAL True
~~~

### 10.3 sandbox 推送与复核

SSH BatchMode、完整 URL，无密码提示。推前 ls-remote 精确为 7d5e28ca89ed68e3360765bc4e42234eaaabae27。只推送以下分支一次，没有 refs/for 或其他 Gerrit 分支推送：

~~~sh
git push --force-with-lease=refs/heads/sandbox/lhmax2025/bolt_pgo:7d5e28ca89ed68e3360765bc4e42234eaaabae27 ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm bolt-on-359934:refs/heads/sandbox/lhmax2025/bolt_pgo
~~~

输出原文：

~~~text
remote: 
remote: Processing changes: refs: 1        
remote: Processing changes: refs: 1, done            
To ssh://review.tizen.org:29418/platform/upstream/llvm
 + 7d5e28ca89ed...c7fd5eed5e35 bolt-on-359934 -> sandbox/lhmax2025/bolt_pgo (forced update)
~~~

推后 ls-remote：

~~~text
c7fd5eed5e35ca335940239cae349a6936f74a7a	refs/heads/sandbox/lhmax2025/bolt_pgo
~~~

五个提交的完整父链：

~~~text
c7fd5eed5e35ca335940239cae349a6936f74a7a 24addd0a47a8e7028fe5561cb4f1153bc293d36a packaging: fix x86 LLVM flags and archive mode
3dc97ef3a8fae0bbc61b208fa2bc6c369f1146b0 24b6aace2a36bb5840f33ea8fa4da710056ff078 packaging: optimize x86_64 clang with BOLT
a73a7da32049569b1360e9c13d0633c168b8f173 3d961cbb04f5446f84d2089b4f65f3178f2bd7fa cmake: use hybrid LLVM linkage on x86_64
13c3e223d9e1b35e4affb55255c5042f8c940f35 087e06cf9c79c571c711af8a07057496940ae73d packaging: classify -feliminate-unused-debug-types and mirror recorded backend policy
cf4b6777d056131e2534ecb460c5575327d99646 7b49745738b5512fbbed890e67e6a3861e1e39a5 Revert "Revert clang bootstrap + ThinLTO, fall back to GCC"
~~~

359934 仍为 NEW，当前 PS10=13c3e223d9e1b35e4affb55255c5042f8c940f35；357163 仍为 NEW，当前 PS2=cf4b6777d056131e2534ecb460c5575327d99646。原始 Gerrit JSON、命令、返回码和时间见 change-359934.txt / change-357163.txt 及对应 .json。没有关闭评审、添加 reviewer 或操作 QB。

[sandbox gitweb](https://review.tizen.org/gerrit/gitweb?p=platform/upstream/llvm.git;a=shortlog;h=refs/heads/sandbox/lhmax2025/bolt_pgo)。供 QB 使用的软件包行为 platform/upstream/llvm@c7fd5eed5e35ca335940239cae349a6936f74a7a。

证明边界：71 号完整 QB 和全量产物比较针对 7d5e28ca；本节新 HEAD 只通过上述轻量检查和 spec 不变性核对，未宣称已完成新 HEAD 的完整构建或 QB 验证。

~~~text
ITEM2 已结束 2026-11-09T15:57:10.410433+08:00 status=ok reason=407-tests-12-expansions-pass-sandbox-updated
~~~
