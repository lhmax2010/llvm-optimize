# clang BOLT + hybrid 外部评审材料（2026-10-28）

基线67619ec8bbbac7238a6cfc33a481ccfbcd12206f → hybrid 6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2 → BOLT f308fe08eeaad4e219f8505449b88bd5f644ea8c。最终tree为214bd2ff9ec7680e045b36b5b8c7e873e953846d；采集时只读ls-remote确认sandbox/lhmax2025/bolt_pgo仍为f308fe08。本轮不推Gerrit/sandbox、不改源码、不构建。

0001、0002由git format-patch --no-binary --no-signature生成，保留作者、提交说明、Signed-off-by和各自Change-Id。0001为hybrid，**此前未经过外部评审**；0002为相对hybrid的BOLT完整变更，不应拿它单独套在67619ec8上。files/是两个提交触及的全部8个文本文件在f308fe08的完整最终版本，尤其llvm.spec已包含两份改动，并非0001后的中间版本。

## 省略的二进制Source1200

- 文件：`packaging/clang-bolt-v2.fdata.xz`
- 字节：9,735,212
- SHA256：`52fd8522b8cceadebfb6bfc0a19f721f1072cff95c682b12b2c4dd5b0cc1e27f`
- 本目录不含profile内容；0002只保留Binary files differ声明和文件统计，没有GIT binary patch。该文本材料包**不是自包含构建输入**；需要构建/完整应用时须从f308fe08取回原件并核对上述SHA，不得拿空文件代替。
- 41号仅做崩溃定位探测，发布提交没有保留符号表等新修改。后续若用户采用新方案并改变提交，必须重新生成本材料包。

## 文件、作用与校验

以下SHA256是文件原始字节；全部文本与git show f308fe08对应路径逐字节核对。README自身的SHA记录在SHA256SUMS中，避免自引用哈希；SHA256SUMS作为校验清单不自哈希。raw链接是bolt-v4分支版，固定版本可将URL中的bolt-v4替换为本次材料提交SHA。

| 文件/raw链接 | 作用 | 字节 | SHA256 |
|---|---|---:|---|
| [0001-cmake-use-hybrid-LLVM-linkage-on-x86_64.patch](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261028/0001-cmake-use-hybrid-LLVM-linkage-on-x86_64.patch) | hybrid完整文本format-patch，父67619ec8 | 8094 | `d8ed2e14e31830deac3e18485a2feed6d48aa3b04a8abe86a595777808607c8f` |
| [0002-packaging-optimize-x86_64-clang-with-BOLT.patch](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261028/0002-packaging-optimize-x86_64-clang-with-BOLT.patch) | BOLT累计文本format-patch，父hybrid；profile仅二进制占位 | 116797 | `7d6a565f49c378cf7067f691fcfcc4c7328105338131a9f9d8d4b4e19bee4340` |
| [changes-since-round3.md](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261028/changes-since-round3.md) | 第三轮评审后六个版本的改动、原因、证据和补丁定位 | 4834 | `37f12503e7957e200c299248d10162b968a4d61ea277eb64595fc2dec39003fc` |
| [files/clang/cmake/modules/AddClang.cmake](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261028/files/clang/cmake/modules/AddClang.cmake) | f308fe08完整文本：clang/cmake/modules/AddClang.cmake | 8036 | `cc505b09c2856008843c430269fb989648090bdcfd1048ab1c2ca16d2c499480` |
| [files/clang/tools/driver/CMakeLists.txt](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261028/files/clang/tools/driver/CMakeLists.txt) | f308fe08完整文本：clang/tools/driver/CMakeLists.txt | 7447 | `e3957b3fed9db504f032d1c3271b23d369c1d65afe4bd54f119f6b343978aad5` |
| [files/lld/cmake/modules/AddLLD.cmake](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261028/files/lld/cmake/modules/AddLLD.cmake) | f308fe08完整文本：lld/cmake/modules/AddLLD.cmake | 2862 | `d43aa8961e5f3a4fd77a2a4b2051e39bea50c643b5a60d403af7c8db68c6a72f` |
| [files/lld/tools/lld/CMakeLists.txt](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261028/files/lld/tools/lld/CMakeLists.txt) | f308fe08完整文本：lld/tools/lld/CMakeLists.txt | 1364 | `ebb6c00e06c799ad8b09969b11b2710e5f5928363fbc03dd98c220dd44ae7656` |
| [files/llvm/cmake/modules/AddLLVM.cmake](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261028/files/llvm/cmake/modules/AddLLVM.cmake) | f308fe08完整文本：llvm/cmake/modules/AddLLVM.cmake | 105835 | `a06c1d55d9866328d3230752efe9c31db6393fc2ef9fc788b4c911ed23d25f89` |
| [files/llvm/tools/llvm-ar/CMakeLists.txt](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261028/files/llvm/tools/llvm-ar/CMakeLists.txt) | f308fe08完整文本：llvm/tools/llvm-ar/CMakeLists.txt | 946 | `5c44903dc53de9e25dea766fa69110068e4367b79d2511ca943e6a29bfe3866f` |
| [files/packaging/clang-bolt-helper.py](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261028/files/packaging/clang-bolt-helper.py) | f308fe08完整文本：packaging/clang-bolt-helper.py | 102447 | `6325aa767ff04cc3b90e2e846afa24cd259f1590792837156499a5767bc6e804` |
| [files/packaging/llvm.spec](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261028/files/packaging/llvm.spec) | f308fe08完整文本：packaging/llvm.spec | 27863 | `3904f944305021e6dcd6e81c53de9d2e1ff844351db04db36f837a59d0459c56` |
| [generation.json](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261028/generation.json) | 生成命令、源提交/tree、文件集合与省略profile身份 | 2203 | `b299504f481ed370fc76695ba8204b80be9977db3e0e3fb6a7e3f18a67a13e55` |
| [hybrid-summary.md](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261028/hybrid-summary.md) | hybrid首次外审摘要和内部验收边界 | 4009 | `ec0c6fe4cd99d0feb47fe3f3d7095c6febe08b19c40f54c0e9751b545a039354` |

- [README raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261028/README.md)：本文件，SHA见[SHA256SUMS raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261028/SHA256SUMS)。
- SHA256SUMS：覆盖本包除清单本身外的每一个文件，可在包根运行`sha256sum -c SHA256SUMS`。

## 关键验证文档（raw）

- [24_rebase_recertification.md](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/24_rebase_recertification.md)：第三轮修复最终十四B认证PASS、257测试；前半段停止原因和纠正记录保留。
- [32_cache_release.md](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/32_cache_release.md)：双轮构建证明释放缓存不改变候选；§15异常处理修复、300测试和解析通过。
- [33_bolt_on_hybrid.md](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/33_bolt_on_hybrid.md)：hybrid+BOLT完整22+1包、113任务门禁、profile匹配和90/90对象通过。
- [34_perf_c_o2_os.md](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/34_perf_c_o2_os.md)：C/C++的O2/Os三目标配对测量与O3复核，样本和干扰边界完整记录，不泛化为全Tizen收益。
- [37_runpath_and_improvements.md](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/37_runpath_and_improvements.md)：RUNPATH/并行工具/real检查完整构建通过；§10完成ar日期单列后的23包、90TU和old-text实验。
- [39_use_old_text_final.md](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/39_use_old_text_final.md)：采用old-text最终版：318测试、五解析、完整构建、精确13a→8c身份、23包、90TU、1200RSS全部通过。
- [41_crash_localization_probe.md](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/41_crash_localization_probe.md)：部分完成：现行栈20/7，符号表+symbolizer24/3、离线24/24、15对象一致；only-keep-debug段错误，方案待决定。
- [40_perf_autofdo_probe.md](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/40_perf_autofdo_probe.md)：能力探测部分完成：硬件LBR可见，perf权限阻断；AutoFDO转换无数据未测。
- [main/docs/53_hybrid_local_validation.md](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/main/docs/53_hybrid_local_validation.md)：第7节PM裁决PASS附4项N/A、as-needed插件、14脚本环境限制例外；详见hybrid-summary，不等于外部评审。

## 发布核对方式

推送后逐一GET本包文件及以上引用的raw文档/证据，核对HTTP200；本包文件同时核对返回字节SHA256。没有目录raw链接；证据目录使用GitHub tree链接。检查记录保留在本机temp/review-package-20261028/raw-verification.json；最终回复报告实际结果。
