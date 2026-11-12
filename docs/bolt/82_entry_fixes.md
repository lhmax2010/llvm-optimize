# 82. 第七轮评审的本地入口修复

结论：PASS。只改证据仓库的 r6 入口；未同步执行副本、未运行真实构建。原16项 + 新14项 = **30/30 PASS**。Toolchain launcher 与修改前字节相同。

## 读取与范围

已读 STATUS、设计v9 §2.2/§2.4/§4.1/§4.2/§6相关段落，r6 run-night.sh、test_serial.py、Base-Dev launcher/launch.sh、README/provenance。未读/改 LLVM 仓库，未访问 QB/Gerrit，未构建。分析/测试均在8G、swap0、CPU400%、nice19、idle IO的串行systemd用户服务。

## 修改与理由

1. 子服务白名单仅 inactive / failed；空列表通过；其他状态及短行停止，reason=project-services-not-confirmed-ended。
2. 在启动 T/D 的 launch.sh 之前设置 project_status 和对应汇总状态为 started；信号时汇总保持 started，不误写 not_run。
3. Base-Dev launcher 在配置选择前断言 PROJECT == basedev；Toolchain launcher 不变。
4. Linger=no 打印 NIGHT_WARNING，保持继续，不开启 linger；dry-run只读检查，不建输出根。
5. README、provenance和SHA256SUMS已更新并校验。[完整diff](../../tools/bolt/results/night-82-84-20261113/82/entry-changes.diff)。

## 新夹具的断言

|用例|退出码|D启动|原因/额外断言|
|---|---:|---|---|
|reloading / maintenance|2|否|project-services-not-confirmed-ended|
|list-units列数不足|2|否|project-services-not-confirmed-ended|
|85,899,345,920 B|0|是|serial-builds-and-validation-finished|
|少1字节|2|否|insufficient-space-before-D|
|磁盘查询失败 / 非数字|2|否|disk-query-failed|
|D缺result.json|2|是（已启动后被检查拦截）|missing-or-invalid-result.json|
|T轮询时向协调器SIGTERM|143|否|signal-15；T=started D=not_run|
|旧 night basedev 参数|2|否|CLI直接拒绝，未进入协调器，故无night日志；记录于legacy-night-result.json|
|不设FINAL_PROJECT直接调用Base-Dev|1|否|AssertionError在配置与副作用之前；无night日志，记录于direct-launcher-result.json|
|空服务列表 / failed服务|0|是|serial-builds-and-validation-finished|
|Linger=no|0|是|正常完成且有NIGHT_WARNING|

以上前置CLI/断言用例本来不产生night日志，证据JSON单列拒绝原因，不虚构日志字段。[逐用例完整结果目录](../../tools/bolt/results/night-82-84-20261113/82/fixtures-run2/)。

## 准备修正（1次）

首次测试18项运行到磁盘失败用例：17通过、1 FAIL，原文保留。原因是新夹具虽然传入MOCK_DISK_RC=7，生成的python3替身却没有使用它，实际返回0；尚未注入所需故障。只给替身接入该退出码，不改期望或入口判断，然后使用全新fixtures-run2从头运行30项。[首次输出](../../tools/bolt/results/night-82-84-20261113/82/tests.stderr)、[修正diff](../../tools/bolt/results/night-82-84-20261113/82/preparation-fix1.diff)。

## 全量测试原文

~~~text
test_D_missing_result (__main__.SerialTests.test_D_missing_result) ... ok
test_SIGTERM_while_polling_T (__main__.SerialTests.test_SIGTERM_while_polling_T) ... ok
test_T_failed_complete_runs_D (__main__.SerialTests.test_T_failed_complete_runs_D) ... ok
test_T_stopped_complete_runs_D (__main__.SerialTests.test_T_stopped_complete_runs_D) ... ok
test_basedev_reject_legacy_branches (__main__.SerialTests.test_basedev_reject_legacy_branches) ... ok
test_both_success (__main__.SerialTests.test_both_success) ... ok
test_child_activating (__main__.SerialTests.test_child_activating) ... ok
test_child_deactivating (__main__.SerialTests.test_child_deactivating) ... ok
test_child_maintenance (__main__.SerialTests.test_child_maintenance) ... ok
test_child_reloading (__main__.SerialTests.test_child_reloading) ... ok
test_controller_accepted_launch_returns7 (__main__.SerialTests.test_controller_accepted_launch_returns7) ... ok
test_controller_failed_prep_active (__main__.SerialTests.test_controller_failed_prep_active) ... ok
test_controller_state_empty (__main__.SerialTests.test_controller_state_empty) ... ok
test_direct_basedev_requires_project (__main__.SerialTests.test_direct_basedev_requires_project) ... ok
test_disk_exactly_80_GiB (__main__.SerialTests.test_disk_exactly_80_GiB) ... ok
test_disk_insufficient_before_D (__main__.SerialTests.test_disk_insufficient_before_D) ... ok
test_disk_one_byte_below_80_GiB (__main__.SerialTests.test_disk_one_byte_below_80_GiB) ... ok
test_disk_query_failure (__main__.SerialTests.test_disk_query_failure) ... ok
test_disk_query_nonnumeric (__main__.SerialTests.test_disk_query_nonnumeric) ... ok
test_dry_run_no_effects (__main__.SerialTests.test_dry_run_no_effects) ... ok
test_empty_service_list_is_ended (__main__.SerialTests.test_empty_service_list_is_ended) ... ok
test_existing_root_refused (__main__.SerialTests.test_existing_root_refused) ... ok
test_failed_service_is_ended (__main__.SerialTests.test_failed_service_is_ended) ... ok
test_invalid_result (__main__.SerialTests.test_invalid_result) ... ok
test_launch_signal_codes (__main__.SerialTests.test_launch_signal_codes) ... ok
test_linger_no_warns_and_continues (__main__.SerialTests.test_linger_no_warns_and_continues) ... ok
test_missing_result (__main__.SerialTests.test_missing_result) ... ok
test_old_night_basedev_refused (__main__.SerialTests.test_old_night_basedev_refused) ... ok
test_short_list_units_row (__main__.SerialTests.test_short_list_units_row) ... ok
test_subservice_query_fails (__main__.SerialTests.test_subservice_query_fails) ... ok

----------------------------------------------------------------------
Ran 30 tests in 1.969s

OK
~~~

## dry-run原文

~~~text
NIGHT_WARNING 2026-11-13T00:40:15+08:00 Linger=no; queue depends on user remaining logged in
ARGV /bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/rebase-launch-20261111-r6/toolchain/launch.sh fea0fe464d56e17f2c7588c557bfffd9f6ac352b full
SERVICE rebase359934r6-toolchain-full-controller-20261111.service
ROOT /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/toolchain
RESULT /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/toolchain/evidence/result.json
ARGV /bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/rebase-launch-20261111-r6/basedev/launch.sh fea0fe464d56e17f2c7588c557bfffd9f6ac352b full basedev
SERVICE rebase359934r6-basedev-full-controller-20261111.service
ROOT /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/basedev
RESULT /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/basedev/evidence/result.json
LOG /home/linhao/Toolchain/development/llvm-optimize/temp/night-20261111-r6/night.log
DRY_RUN 已结束 2026-11-13T00:40:15+08:00 status=ok
~~~

原有构建根/结果未改，没有运行LLVM构建或平台工具。其他未修改的入口验证器测试本轮未重跑；本任务要求的串行入口原16项及新增14项已全量运行。

82 已结束 2026-11-13T00:40:15.356186+08:00 status=PASS

## 收尾路径准备修正（第2次）

最终重复校验SHA256SUMS时，输出重定向把结果目录相对路径多退了一层，shell在启动sha256sum之前报“Directory nonexistent”。只将两处证据输出路径改为绝对路径，未改入口、测试、期望或清单；随后两套sha256sum -c均通过。原文和命令差异见 [preparation-fix2-error.txt](../../tools/bolt/results/night-82-84-20261113/82/preparation-fix2-error.txt)、[preparation-fix2.diff](../../tools/bolt/results/night-82-84-20261113/82/preparation-fix2.diff)。本项准备修正共2次。
