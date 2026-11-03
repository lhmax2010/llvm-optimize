# 50 号本地启动入口

来源：`../debuglink-launch-20261030/launcher.py`（dca920a8 的 gbs-driver 布局），
用独立 physical `gbs-root` 和 `gbs-driver/local/BUILD-ROOTS` 符号链接。
历史脚本、历史根及源码的前两个提交均不修改。本地资源限制不进入发布代码。

```sh
/bin/sh tools/bolt/final-launch-20261103/launch.sh toolchain rehearsal
/bin/sh tools/bolt/final-launch-20261103/launch.sh basedev rehearsal
```

演练停止于 `+ cmake -G Ninja`，不运行 LLVM Ninja。每次使用新根；已存在即拒绝，
失败现场保留。支持 `rehearsal-02` 独立重试目录，不自动重试。

完整构建入口仅准备，本轮不运行：

```sh
/bin/sh tools/bolt/final-launch-20261103/launch.sh toolchain full
# T 构建及验证全部通过后，另行执行 D，不能并行：
/bin/sh tools/bolt/final-launch-20261103/launch.sh basedev full
```

两个 full 根分别为 `W/temp/final-20261103/toolchain`、`basedev`。
配置保存在 `W/temp/final-20261103/configs/{toolchain,basedev}`；只启用固定快照
packages/debug 仓库。GBS profile 的键名保留既有 `tizen-base-toolchain_standard`，
以保持 driver sources 路径不变；实际项目由 URL 和 build.conf 决定。

仅本地控制器调整：T 保留历史 profile/strip 身份监视；D 不套用 T 的固定身份值，
仍由发布 helper 执行全部门禁，仍监视 `BOLT_GATE_FAILED` 和磁盘停止条件。
这是不同编译器和 release 模式的身份范围区分，不是放宽任何发布门禁。

每次启动会打印实际后台日志查看命令；控制器无论成功失败都会打印带时区的
`FINAL_PROJECT_FLAGS 已结束 ... status=... reason=...`。

T 夜间验收：strip-all、RUNPATH 后、最终 clang 的 SHA 必须分别为
`13a07cb7f84bd1ceda4d851c8bd71bddf7ef0c2d4864892eba64cbbb9a0350b8`、
`8c2429d870f421a29a9914458bc4d4ff2ce359a15e0bdd20f39bfb4580c40bdf`、
`4f08e12d499ebd492ce4951f74915ba435f57f2e380dc6f3520f24644996cb17`。
ordinary、clang-22.debug 和静态归档成员可以因记录编译命令的节不同而改变 SHA，
但必须定位具体节和字节差异，证明只改变命令记录，其余字节相同。
不能跳过整个 `.debug_info` 或整个成员；ar 成员日期差异仍按既定三条件单列。
23 包逐项比较和 90 TU 仍须执行；完整构建未运行之前不能声称产物认证通过。
