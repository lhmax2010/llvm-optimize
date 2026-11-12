# r6 local entry: 2026-11-11

Authorized for one complete night run of fea0fe464d56e17f2c7588c557bfffd9f6ac352b on 2026-11-11, Toolchain first and Base-Dev second, and daytime rehearsal-02 checks. Daytime preparation does not run a full build.

Use ../run-night.sh from a project directory (or run-night.sh at the entry root). It calls each project's own launch.sh. Toolchain uses tizen-base-toolchain_20261030.061318; Base-Dev uses tizen-base-dev_20261030.061217. Build logic, limits, gates and comparisons are unchanged.

The copied night.py is preserved byte-for-byte and must not be used: its legacy coordinator calls the Base-Dev launcher for both projects and monitors different roots/unit names. The Base-Dev launch.sh accepts only full/rehearsal/rehearsal-02 basedev. The legacy night and rehearsal toolchain branches are rejected.

run-night.sh SOURCE_SHA --dry-run prints commands/units/roots without creating output directories or starting services. Without --dry-run it creates the summary directory, appends stdout/stderr to night.log, checks both full roots are absent, then waits for each project's controller to finish. A valid failed/stopped T result proceeds to D only after every project service has ended. Launcher failure (129/130/143 preserved, otherwise rc=2), missing/invalid result, failed state query or a live child service stops the queue. Before D, /home must have at least 80 GiB available. Each stop records a project and overall ended line with its reason. No terminal input is read.

Full roots: W/temp/rebase-359934-20261111-r6/{toolchain,basedev}.
Rehearsal roots: W/temp/rebase-359934-20261111-r6/rehearsal/{toolchain,basedev}/retry-02.
Summary: W/temp/night-20261111-r6/night.log.
Source: W/temp/rebase-359934-20261111-r6/source.

The night coordinator is launched in rebase359934r6-night-20261111.service using systemd-run --user --collect, independent of a terminal. If Linger=no, do not log out during the build. test_serial.py covers the serial failure boundaries without starting real services. Existing test expectations remain unchanged; new CLI tests require legacy Base-Dev branches to be rejected.


## 第七轮评审入口跟进（82号，2026-11-13）

子服务只有 inactive、failed 视为结束（空列表允许）；其他状态或不完整查询输出停止队列，reason=project-services-not-confirmed-ended。T/D 调用 launch.sh 前即记 started，轮询收到信号时保留可能在运行的状态。Base-Dev launcher 直接断言 FINAL_PROJECT=basedev，不能绕过 shell 进入 Toolchain 的旧配置。启动时读取 Linger，no 只打印 NIGHT_WARNING，提示保持登录，不更改 Linger。

30项 mock 测试通过：原16项保留，新增14项（含磁盘精确80GiB边界、故障/非数字、短行、reloading/maintenance、D缺结果、SIGTERM、直接入口断言和Linger）。第一次磁盘失败夹具漏接退出码，修正故障注入后全量重跑，断言未变。详见 docs/bolt/82_entry_fixes.md。本轮没有启动真实构建或修改 Toolchain launcher。
