# 预处理翻译单元入口

本轮保持目录为空。没有 `.ii` 时，结果必须标记 `REAL_TU_ABSENT`。
后续可从 LLVM 自身编译中采集输入；本机不进行 Chromium 全量构建。

每个输入由两个同名文件组成，名字仅用字母、数字、下划线和短横线：

```text
llvm_sema.ii
llvm_sema.flags.json
```

`.ii` 必须是完整的 C++ 预处理文本，不依赖外部 include、PCH、模块缓存或响应文件。
采集时使用实际编译命令，将 `-c` 改为 `-E`，去掉原 `-o`、依赖文件输出选项，
把输出写到工作区 `temp/`。不在原源码或构建目录写文件。
预处理本身也必须使用 `--target=armv7l-tizen-linux-gnueabi` 和同一 ARM sysroot；
不能把已有的 x86_64 预处理文本仅在 JSON 中重标为 ARM。若原构建是 x86_64，
保留原命令作为来源，并另行记录实际 ARM 预处理命令及必要的配置调整。

配套 JSON 格式：

```json
{
  "target": "armv7l-tizen-linux-gnueabi",
  "sha256": "替换为实际 .ii 文件的 SHA256",
  "flags": ["-std=c++17", "-O2", "-fno-exceptions", "-fno-rtti"],
  "source": "原始源码的路径与版本",
  "original_command": ["完整原始编译命令，按 argv 数组记录"],
  "preprocess_command": ["实际预处理命令，按 argv 数组记录"]
}
```

`flags` 仅保存编译语义选项，不能含工具路径、输入/输出路径、target、sysroot、
include、PCH、插件、响应文件、依赖输出或链接选项。脚本采用明确的选项白名单；
遇到其他选项应先审查并扩充白名单，不能静默删除。target 与脚本固定 triple 必须一致。
脚本统一追加 `-x c++-cpp-output -c <input> -o <temporary object>`。
编译产物须为 ARM ELF object，因此本入口不接受 LTO bitcode 选项。

单个 `.ii` 超过 10,000,000 字节时留在 `temp/`：只提交 `.flags.json`，其中加
`"input": "/工作区/temp/实际路径.ii"`。该文件也会进入扫描，缺失或哈希不匹配时失败；
把路径和获取办法写入相应任务文档。小文件可以和 `.flags.json` 一起放在本目录。
新增输入后，输入集身份会改变，必须重新完成两轮噪声校准。

这是快速筛选负载；结果与专用服务器 Chromium 全量耗时是否方向一致，需后续交叉验证。
