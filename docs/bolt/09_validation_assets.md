# 09 90 对验证资产：预处理全部完成

90/90 PASS，缺源0、缺头0。ARM训练10、ARM留出10、AArch64训练10的历史同批selection，各自对armv7l/aarch64/x86_64重新从真实.cpp预处理；不是把旧.ii改target字段。组间重复源保留，实际30个selection、20个不同源路径，不虚称30个独立源。

| cohort | ARM | AArch64 | x86_64 |
| --- | ---: | ---: | ---: |
| ARM训练 | 10 | 10 | 10 |
| ARM留出 | 10 | 10 | 10 |
| AArch64训练 | 10 | 10 | 10 |

## 输入、方法与身份

宿主native普通clang为已验证历史RPM实体，SHA3283505cdfebae8a211b0d5fb7befbe5295812787554eb1199ee52e3cfc4a61c；宿主loader+明确libxml2库路径，只读sysroot分别为用户指定R32/R64/R1；不执行外国ELF，不chroot/挂载R32/R64。保留原selection宏/语义/O3/C++17参数，去原输出/依赖/target/march/ThinLTO等参数，源与生成include重定位到只读R1源码树，三目标分别使用对应sysroot。完整实际argv与移除项逐条登记，未静默补新宏或下载头文件。

所有30selection的源SHA、cohort、索引和原selection文件SHA均保存；每份.ii的完整SHA与大小、depfile、逐个实际头文件SHA（含生成头、系统/C++/资源头）均保存。所需C++头实际位于sysroot的lib/gcc/.../include/c++，不因usr/include/c++目录缺失就误报缺头。首份核对没有宿主/usr头路径；完整headers.json可逐条复核。

全部.ii合计 677747108B；header记录合计 49773 项（每份去重，跨份允许重复）。净预处理/哈希登记42.576s，4GiB/nice19/ionice3/swap0 scope43.598s，无资源终止。没有对90份做.o或性能测量，不把资产PASS当90对象门禁PASS。

## 产出位置

E=/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261014。assets90/<cohort>/<index-source>/<triple>/下保存input.ii、argv.json、headers.d/headers.json、stdout/stderr；大.ii留E，未提交Git。公开tools/bolt/results/assets90-manifest.json保存完整90条命令、源/.ii/头清单SHA和各目录位置；可用SHA核查本地大资产。没有缺失清单条目。
