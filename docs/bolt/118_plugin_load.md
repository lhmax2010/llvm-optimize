# 118 C：Q5 插件载入

最终结论：PASS（一次准备修正后）。首次驱动调用错误与记录保留在后文。

使用 QB 1231417 的 clang、clang-devel、llvm-devel 等 RPM 私有解包；不安装到系统。Clang/LLVM 头来自该 RPM；C/C++ 运行库及 loader 只读使用74号 T构建根。以 -fPIC -shared 编译，未链接任何 LLVM/clang 库。构建与加载的完整 argv、退出码和输出见 [plugin证据](../../tools/bolt/results/qb-1231417-1231418/plugin/)。只将源码、脚本和日志入库，私有载荷与生成的二进制留本地。

插件注册 PluginASTAction，在顶层函数声明时打印名称；加载使用 -fplugin，编译tiny.c。

原始错误见 compile.json / load.json。

已结束 2026-11-16T23:34:36.921060-08:00 C MISSING_DEPENDENCIES

## 准备修正一次后的实际结果
首次并非头文件缺失，而是loader重执行路径错误；上面的首次状态保留。拆分编译与链接，见 preparation-fix.diff 和 retry1-results.json。最终：PASS。

```text
PLUGIN_FUNCTION alpha
PLUGIN_FUNCTION beta
PLUGIN_FUNCTION main
```
已结束 2026-11-16T23:35:34.829351-08:00 C PASS
