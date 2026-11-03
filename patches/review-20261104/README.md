# 第二轮外部评审材料：hybrid + BOLT + 固定参数

建议首先阅读 [相对上一轮的增量](changes-since-review-20261102.diff) 和 [BOLT 纯文本 diff](0002-text-only.diff)，无需先打开带二进制 profile 的完整 BOLT 补丁。旧评审包保留；本包取代 review-20261102 用于本轮评审。

三个提交基于 `67619ec8bbbac7238a6cfc33a481ccfbcd12206f`，按 0001、0002、0003 顺序应用：

1. hybrid `d4d6ca16b55a9afcb64a30ebf634f340f968267b`：NEEDED 断言对 readelf/grep 错误失败关闭；grep 采用 here-document；加入五个可选静态工具的检查和 SKIP。
2. BOLT `f2553114b05cbb022ff3ac062dbac284e1029df4`：SIGINT、纯 Python 与尾部取消、第二信号立即终止、CANCELLED 独立前缀；补维护说明。不改 profile、OPTIONS、白名单或候选生成参数。
3. fixed flags `9e39fa8a61392652bb28b75fc26216675bcad1d5`：准确恢复 IFS/$-；非法 release/native CPU 失败。**按用户追加裁决**，其他未评审项目参数丢弃并在 stdout/stderr 各输出一次汇总 warning；非认证 debug 序列只 warning。Source1005 要求 --debug-info yes/no，逐成员核对 recorded command；原生成员原样保留并计数。

三个 Change-Id 不变，均仅本地提交，未上传 Gerrit/sandbox。普通流程仍为普通编译/安装→工具构建→重链/BOLT→strip/RUNPATH/debuglink→compare-root→原生归档转换→候选安装→平台后处理和 post 尾检。debug 模式带函数符号文件和 debuglink，release 模式不带。回退仍使用既有 x86_64 BOLT bcond 开关；混合链接和参数提交是独立层，不能用 BOLT 开关声称回退它们。

## 验证与限制

- 393 项 helper 测试、42 项参数/转换器测试通过；再用本轮新根 clang 做 Claude C-2 的合成 release 正/负例，2/2 通过。
- full-20261030 的 3853 个转换成员全部带 debug 参数，因此启用显式模式检查；真实 release 包成员还须在完整构建后补测，合成夹具不替代它。
- 两配置 12 项完整展开、Tizen RPM 五项解析通过；ARM 展开与 5aff6c0c 字节相同。
- 补丁顺序应用后的 tree 与源码一致：`cbc33271f8a9a7a5bd4de3c806bed6182c268e98`。
- Toolchain 和 Base-Dev 两个启动演练均 PASS：到 CMake 入口即停止，未运行 Ninja，参数符合预期且无 warning，清理检查通过。完整原文见 [51 号文档](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/51_second_review_fixes.md)。本轮没有运行完整 LLVM 构建，不宣称新产物 SHA 或 RPM 已验证。
- 挂账：关闭 BOLT 的完整构建、release 完整构建/真实成员、67619ec8 精确 RPM 基线缺口。源码行级定位及 llvm-objcopy only-keep-debug 缺陷继续按既有记录处理。
- 不采纳本轮改变 debugfiles 路径接口及对原样保留成员强加 release 无调试节断言；理由见 51 号。

Source1200 仍为 `packaging/clang-bolt-v2.fdata.xz`，9,735,212 字节，SHA256 `52fd8522b8cceadebfb6bfc0a19f721f1072cff95c682b12b2c4dd5b0cc1e27f`。完整二进制在 0002 format-patch 内；纯文本 diff 只排除该文件，包含 helper/spec 全部 BOLT 改动。

## 文件

完整文本文件取最终三层应用后的版本；6 个 CMake 文件属于 hybrid 改动。提交说明另存全文。SHA256SUMS 对所有材料（除其自身）逐个给出 SHA256。

| 文件 | 用途 / raw |
|---|---|
| `0001-hybrid-linkage.patch` | [raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261104/0001-hybrid-linkage.patch) |
| `0001-message.txt` | [raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261104/0001-message.txt) |
| `0002-bolt.patch` | [raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261104/0002-bolt.patch) |
| `0002-message.txt` | [raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261104/0002-message.txt) |
| `0002-text-only.diff` | [raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261104/0002-text-only.diff) |
| `0003-fixed-project-flags.patch` | [raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261104/0003-fixed-project-flags.patch) |
| `0003-message.txt` | [raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261104/0003-message.txt) |
| `changes-since-review-20261102.diff` | [raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261104/changes-since-review-20261102.diff) |
| `files/clang/cmake/modules/AddClang.cmake` | [raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261104/files/clang/cmake/modules/AddClang.cmake) |
| `files/clang/tools/driver/CMakeLists.txt` | [raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261104/files/clang/tools/driver/CMakeLists.txt) |
| `files/lld/cmake/modules/AddLLD.cmake` | [raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261104/files/lld/cmake/modules/AddLLD.cmake) |
| `files/lld/tools/lld/CMakeLists.txt` | [raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261104/files/lld/tools/lld/CMakeLists.txt) |
| `files/llvm/cmake/modules/AddLLVM.cmake` | [raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261104/files/llvm/cmake/modules/AddLLVM.cmake) |
| `files/llvm/tools/llvm-ar/CMakeLists.txt` | [raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261104/files/llvm/tools/llvm-ar/CMakeLists.txt) |
| `files/packaging/clang-bolt-helper.py` | [raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261104/files/packaging/clang-bolt-helper.py) |
| `files/packaging/llvm-static-archives-native.py` | [raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261104/files/packaging/llvm-static-archives-native.py) |
| `files/packaging/llvm.spec` | [raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261104/files/packaging/llvm.spec) |
| `range-diff.txt` | [raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261104/range-diff.txt) |

关联证据：[48 号](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/48_review_fixes.md)、[49 号](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/49_qb_1215143_1214821.md)、[50 号](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/50_project_flag_independence.md)、[51 号](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/51_second_review_fixes.md)。
