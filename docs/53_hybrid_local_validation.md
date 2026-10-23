# Hybrid 本地完整构建与验证（2026-10-23）

状态：构建进行中，未宣称验证通过。源提交6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2未修改，未推送Gerrit、未操作QB。

## 1. 身份与输入

干净源码 `temp/llvm-optimize-intranet-20261020/llvm`，tree 80a6fd231c4564a3b762f4ec288cf2c41f9d2e20、upstream ca7933e47d3a3451d81e72ac174dcb5aa28b59d1、core.abbrev=12全部核对。GBS 2.1.0新导出的spec和0001–0008八个补丁SHA与llvm_optimize_intranet_fetch.md §4全部逐字节相同。

固定Base20261013.024319，仅packages/debug；build.conf SHA e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945。使用用户指定BOLT线配置只读，-B覆盖构建根为本次新建的 `/home/linhao/Toolchain/development/llvm-optimize/temp/hybrid-local-20261023/gbs-root`，没有写入配置中的旧根。外层threads30及jobs8、_smp_mflags -j8、_costomized_smp_mflags -j20保持。

## 2. 本地资源与采样

用户本轮裁决覆盖旧限制：MemTotal33,072,918,528B减8GiB，MemoryMax24,482,983,936B；swap0、nice10、IO class2/priority7。不设内存准入、不因低内存冻结，不按锁时限切段。此单任务持有共享重任务锁至结束；只在/home可用低于20GiB时正常停止，cgroup OOM记录且不重试。规则只在本地包装脚本中，不进入源码/spec。

完整chroot根每60秒尝试du，单次50秒加5秒终止宽限，超时/竞态记录缺失；不补造读数。资源每2秒记录，完整RPM日志另存。所有BOLT保全目录和历史根只读。

## 3. 验证范围与当前状态

188目标按docs/52冻结期望表核对，包括3组静态、5个上游静态例外、29个不依赖两共享库的目标、108个LLVM动态和43个LLVM+Clang动态；188不是安装可执行文件数，不以统一“其他全部动态”覆盖这些例外。

完整构建、22+1 RPM、188实物NEEDED、全部已打包工具运行、三目标90对对象、开发包CMake消费者/导出文件、225归档以及ARM两模式解析均待完成。最终不得以配置级期望代替实物验证。

证据目录：[53_hybrid_local_validation_evidence](53_hybrid_local_validation_evidence/)。
