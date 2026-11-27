# 170 · 修正 PGO+BOLT 的参数分词

**新 QB 验证分支已创建，远端指向 `a752ddf8e826ab70bffe2354619a7f9977513764`。**
 [远端回执](../../tools/bolt/results/task170/candidate/sandbox-after.stdout.txt)

- 分支 `sandbox/lhmax2025/llvm-pgo-bolt-20261127-2`
- 修正后的集成提交 `722b933efb1dc04a1aec50d6665c675d0567f595`
- QB 测试提交 `a752ddf8e826ab70bffe2354619a7f9977513764`
- R 配方提交 `dd3525973a1044a6e93c143813d207d33aa2383d`

## Spec 修正

在 Source1202 的闭引号与可选宏之间插入一个空格。R 和集成提交的产品 diff 各为一行。新 QB 测试提交的树相对上一版测试提交也只有这一个空格变化。

```diff
diff --git a/packaging/llvm.spec b/packaging/llvm.spec
index ba0273fbf699..a495137b2c10 100644
--- a/packaging/llvm.spec
+++ b/packaging/llvm.spec
@@ -388,7 +388,7 @@ cd build
 %else
 %global llvm_pgo_project T
 %endif
-python3 -B %{SOURCE1201} pgo-prepare "%{SOURCE1204}" %{llvm_pgo_project} "$PWD/pgo-profiles" "%{SOURCE1202}"%{?llvm_pgo_bolt_source} || exit 1
+python3 -B %{SOURCE1201} pgo-prepare "%{SOURCE1204}" %{llvm_pgo_project} "$PWD/pgo-profiles" "%{SOURCE1202}" %{?llvm_pgo_bolt_source} || exit 1
 %endif
 cmake \
     -G Ninja \
```

[R diff](../../tools/bolt/results/task170/r-spec.diff) · [集成 diff](../../tools/bolt/results/task170/integration-spec.diff) · [QB 测试提交内容](../../tools/bolt/results/task170/test-only.diff) · [与前一测试提交的 diff](../../tools/bolt/results/task170/test-vs-previous.diff)

## 真实 shell 参数矩阵

Tizen RPM 4.14.1 对 x86_64 展开 T、D 与 PGO/BOLT 开关的八种组合。检查显式展开安装后置宏，遍历直接调用及逐调用点转发的 bolt_step。Bash 仅求值参数，导入的产品 helper 提供真实 argparse parser。PGO 参数逐项核对 manifest、项目、work、profdata 和可选 BOLT profile。两种项目的 PGO+BOLT 旧版都在实际拼接处报错，修正后候选的 118 条调用均解析成功。R 的八种组合也通过。

### 修正前原文

```text
RPM version 4.14.1
FAIL T-pgo1-bolt1 helper_calls=28
argv pgo-prepare /home/linhao/Toolchain/development/llvm-optimize/archive/task160/candidates/B/assets/llvm-profiles.manifest T /home/linhao/Toolchain/development/llvm-optimize/archive/task170/argv-original/build-fixture/pgo-profiles /home/linhao/Toolchain/development/llvm-optimize/archive/task160/candidates/B/assets/T-clang.profdata.xz--bolt-profile /home/linhao/Toolchain/development/llvm-optimize/archive/task160/candidates/B/assets/T-clang.fdata.xz
usage: check_helper_argv.py [-h]
                            {preflight,certified,security,tool-prepare,tool-verify,tool-plan,pipeline,strip-all,cache-release,cache-copy,package-compare,unpack,replay,rewrite,tiny,installed-baseline,snapshot,compare-root,install,post,pgo-prepare,pgo-check-ninja,pgo-post,disk-report,disk-diagnose,run-step}
                            ...
check_helper_argv.py: error: unrecognized arguments: /home/linhao/Toolchain/development/llvm-optimize/archive/task160/candidates/B/assets/T-clang.fdata.xz
PASS T-pgo1-bolt0 helper_calls=3
PASS T-pgo0-bolt1 helper_calls=27
PASS T-pgo0-bolt0 helper_calls=1
FAIL D-pgo1-bolt1 helper_calls=28
argv pgo-prepare /home/linhao/Toolchain/development/llvm-optimize/archive/task160/candidates/B/assets/llvm-profiles.manifest D /home/linhao/Toolchain/development/llvm-optimize/archive/task170/argv-original/build-fixture/pgo-profiles /home/linhao/Toolchain/development/llvm-optimize/archive/task160/candidates/B/assets/T-clang.profdata.xz--bolt-profile /home/linhao/Toolchain/development/llvm-optimize/archive/task160/candidates/B/assets/T-clang.fdata.xz
usage: check_helper_argv.py [-h]
                            {preflight,certified,security,tool-prepare,tool-verify,tool-plan,pipeline,strip-all,cache-release,cache-copy,package-compare,unpack,replay,rewrite,tiny,installed-baseline,snapshot,compare-root,install,post,pgo-prepare,pgo-check-ninja,pgo-post,disk-report,disk-diagnose,run-step}
                            ...
check_helper_argv.py: error: unrecognized arguments: /home/linhao/Toolchain/development/llvm-optimize/archive/task160/candidates/B/assets/T-clang.fdata.xz
PASS D-pgo1-bolt0 helper_calls=3
PASS D-pgo0-bolt1 helper_calls=27
PASS D-pgo0-bolt0 helper_calls=1
```

### 修正后原文

```text
RPM version 4.14.1
PASS T-pgo1-bolt1 helper_calls=28
PASS T-pgo1-bolt0 helper_calls=3
PASS T-pgo0-bolt1 helper_calls=27
PASS T-pgo0-bolt0 helper_calls=1
PASS D-pgo1-bolt1 helper_calls=28
PASS D-pgo1-bolt0 helper_calls=3
PASS D-pgo0-bolt1 helper_calls=27
PASS D-pgo0-bolt0 helper_calls=1
```

[旧版逐调用 argv](../../tools/bolt/results/task170/argv/before/result.json) · [修正版逐调用 argv](../../tools/bolt/results/task170/argv/fixed/result.json) · [R 逐调用 argv](../../tools/bolt/results/task170/argv/recipe/result.json)

技能 64 项单测通过，技能校验器通过，共享文本扫描零命中。候选推送前强制要求八项 PASS，将检查收据绑定到候选中的 spec 和 helper 两个 blob。旧候选使用新收据会因 SHA256 不匹配被拒绝。
 [候选推送门禁改动](../../tools/bolt/results/task170/candidate-prepush-gate.diff) · [绑定证明](../../tools/bolt/results/task170/receipt-binding.txt)

## QB 候选静态核对

157-B 的三架构展开、profile SHA256 和压缩前身份、清单与 BOLT 参数核对均通过。打包继续使用配对 fdata 和 -stale-threshold=5。提交说明和新增行的对外文本门禁零命中。集成提交的 UNQUALIFIED 清单仍被生产 READY 门禁拒绝，QB 测试提交仅放宽状态检查。当前清单只含 T 映射，D 的矩阵结果覆盖参数解析。 [核对回执](../../tools/bolt/results/task170/result.json) · [推送原文](../../tools/bolt/results/task170/candidate/sandbox-push.stdout.txt)
