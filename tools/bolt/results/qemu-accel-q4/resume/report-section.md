## 108号续：SSH 获取与 Q4 结论（2026-11-16）

**结论：SSH 获取成功，Q4 草稿完成，仅供用户发布。** accel 收集范围远超 clang/lld/llvm-ar：其他工具的动态依赖仍会引入 libLLVM、libclang-cpp。与保留的混合链接前静态 LLVM RPM 相比，模拟的 LLVM 文件集合按路径总大小减少 77.27%；这是有限范围模拟，不是重新构建后的 accel RPM 大小。新 accel 的 buildroot setup 耗时尚未测得。没有构建、访问 QB 或向 Gerrit 写入。

优先交付：[可直接复制的 Q4 英文草稿](../../tools/bolt/results/qemu-accel-q4/resume/Q4-for-user.txt)。该文件通过英文及内部引用检查，未发布；[检查原文](../../tools/bolt/results/qemu-accel-q4/resume/reply-gate.json)。

### 1. 获取与身份

按用户指定，从现有 LLVM origin 的 SSH 地址替换项目名，使用已有凭据、BatchMode=yes，单次执行：

```sh
GIT_SSH_COMMAND=ssh