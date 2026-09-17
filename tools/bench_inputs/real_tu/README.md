# 预处理翻译单元入口

本目录收录 docs/13 的 10 个 LLVM ARM 预处理输入，使用最终 RPM 中的 clang 22.1.8
采集；没有修改 LLVM 的源码或生成配置头。`selection.json` 固定原 Ninja 目标与历史
x86_64 编译耗时（该耗时只用于选材，不是 ARM 基准数据）。
`llvm_sema_SemaExprCXX.ii` 超过 10 MB，保存在对应 sidecar 的绝对 `input` 路径。
其他 `.ii` 与 sidecar 一并提交。重新采集可使用 `tools/collect_llvm_real_tu.py`，
传入 `--candidates tools/bench_inputs/real_tu/selection.json`；完整用法见 docs/13。
没有输入时结果仍标记 `REAL_TU_ABSENT`；本机不进行 Chromium 全量构建。

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

本次 bundled clang 18 参考轮使用它自己的资源目录重新生成 ARM 输入，仅保存在
`temp/baseline-resume-20260917/reference-inputs/`。clang 18 不能直接消费本目录中
clang 22 预处理选中的全部编译器内建功能；该参考轮的输入、资源目录及链接夹具不同，
不是受控对照，不能用其比值声称优化收益。
