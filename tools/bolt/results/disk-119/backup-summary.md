# 源码保护备份（不删除）

总大小98,026,516,480 B；26个repository.bundle，另有3个_selftest目录。verified.git用于原备份解包验证，未安装refs，不能将它的空refs误当成无源码。以下使用bundle头与inspection-before的原仓库身份。

|备份|原仓库|原HEAD|当前LLVM引用覆盖|
|---|---|---|---|
|00-source/root-5645c783|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/_selftest2/source|fba080e9571938aaa00ddae88789503470a3c331|UNKNOWN: no bundle tip matches current LLVM remote refs; no objects fetched|
|00-source/root-759fbb28|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/_selftest/source|861a5fb6fd917729cd897b0894863b64646ed839|UNKNOWN: no bundle tip matches current LLVM remote refs; no objects fetched|
|00-source/root-e27851fd|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/_selftest3/source|45180459a9ab2f8a3c774fe24e8540411debc1f8|UNKNOWN: no bundle tip matches current LLVM remote refs; no objects fetched|
|04-pgo-resource-20261102/source-D-aa70a0e3|/home/linhao/Toolchain/development/llvm-optimize/temp/pgo-resource-20261102/source-D|4ff8ceb44b04b48f6299b6ddf7c5b147ad788b54|False|
|05-review-round3-continue-20261012/patch-apply-check-c54a3707|/home/linhao/Toolchain/development/llvm-optimize/temp/review-round3-continue-20261012/patch-apply-check|cb67996861d070d68fec2b4c623eed7d20ba2e23|False|
|05-review-round3-continue-20261012/patch-work-617ca250|/home/linhao/Toolchain/development/llvm-optimize/temp/review-round3-continue-20261012/patch-work|db23b26079776684d09c620ae614a59cd40007a0|False|
|09-archive-fix-full-build-20260927/test-package-bfd-4a09ebac|/home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-full-build-20260927/test-package-bfd|3d6cae6fe9508cd25dea205ae5bec86485ca551d|UNKNOWN: no bundle tip matches current LLVM remote refs; no objects fetched|
|09-archive-fix-full-build-20260927/test-package-lld-6ad747a2|/home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-full-build-20260927/test-package-lld|05845d42cb9a581d9cd5edb9b24694e3b07644c5|UNKNOWN: no bundle tip matches current LLVM remote refs; no objects fetched|
|10-archive-followup-review-20261014/apply-check-5b6fd066|/home/linhao/Toolchain/development/llvm-optimize/temp/archive-followup-review-20261014/apply-check|67619ec8bbbac7238a6cfc33a481ccfbcd12206f|False|
|10-archive-followup-review-20261014/submit-work-4512d286|/home/linhao/Toolchain/development/llvm-optimize/temp/archive-followup-review-20261014/submit-work|d4dd40da3b6ab28925b57d24d66bd992b4ad798c|False|
|18-release-x86-full-build-20261013/latest-base_source-ae3cb8ab|/home/linhao/Toolchain/development/llvm-optimize/temp/release-x86-full-build-20261013/latest-base/source|4c36e899dffee2869af9afd174346e3eb9a7d7ca|False|
|18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-bfd-1b27e3f6|/home/linhao/Toolchain/development/llvm-optimize/temp/release-x86-full-build-20261013/round2-eight-output-proof/test-package-bfd|ab863a0f64d932bff7f310df9e40a329b50b3225|UNKNOWN: no bundle tip matches current LLVM remote refs; no objects fetched|
|18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-lld-40f1e6ad|/home/linhao/Toolchain/development/llvm-optimize/temp/release-x86-full-build-20261013/round2-eight-output-proof/test-package-lld|ac0d12ca8d2970be2ec9fee05d2f57944e106a8c|UNKNOWN: no bundle tip matches current LLVM remote refs; no objects fetched|
|19-release-attribution-20261013/patch-apply-check-6105a95d|/home/linhao/Toolchain/development/llvm-optimize/temp/release-attribution-20261013/patch-apply-check|cb67996861d070d68fec2b4c623eed7d20ba2e23|False|
|19-release-attribution-20261013/patch-work-45589d5e|/home/linhao/Toolchain/development/llvm-optimize/temp/release-attribution-20261013/patch-work|4c36e899dffee2869af9afd174346e3eb9a7d7ca|False|
|24-llvm-strip-alternative-20260929/test-package-bfd-03f3e641|/home/linhao/Toolchain/development/llvm-optimize/temp/llvm-strip-alternative-20260929/test-package-bfd|7aa4dc8d7cf0c82edb9fc6e86a9c27ede378e40e|UNKNOWN: no bundle tip matches current LLVM remote refs; no objects fetched|
|24-llvm-strip-alternative-20260929/test-package-lld-c8f02f6f|/home/linhao/Toolchain/development/llvm-optimize/temp/llvm-strip-alternative-20260929/test-package-lld|316a0e4710972a50507b6814b1547896f2d00a61|UNKNOWN: no bundle tip matches current LLVM remote refs; no objects fetched|
|25-llvm-strip-x86_64-20261009/continue-20261009_test-package-bfd-2ca8bd4a|/home/linhao/Toolchain/development/llvm-optimize/temp/llvm-strip-x86_64-20261009/continue-20261009/test-package-bfd|b6f90adcc39b04c9df0cc94203a98af084bf7ab2|UNKNOWN: no bundle tip matches current LLVM remote refs; no objects fetched|
|25-llvm-strip-x86_64-20261009/continue-20261009_test-package-lld-81b277b8|/home/linhao/Toolchain/development/llvm-optimize/temp/llvm-strip-x86_64-20261009/continue-20261009/test-package-lld|dc37bbaeab1cc855a52262e0b0318c824b7c618a|UNKNOWN: no bundle tip matches current LLVM remote refs; no objects fetched|
|29-llvm-hybrid-trial/root-8885f3e3|/home/linhao/Toolchain/development/llvm-optimize/temp/llvm-hybrid-trial|f111162e94aa48ed367c9d2c039456c70e7160ae|False|
|30-llvm-archivefix-trial/root-fd4d3568|/home/linhao/Toolchain/development/llvm-optimize/temp/llvm-archivefix-trial|f111162e94aa48ed367c9d2c039456c70e7160ae|False|
|32-followup-356949-ps2-message-20261014/review-work-c226bed9|/home/linhao/Toolchain/development/llvm-optimize/temp/followup-356949-ps2-message-20261014/review-work|a18ce53708d3b6ef596dcd27d0b51e18ce1db282|True|
|36-qb_analysis/work3_control_findutils-5ecf1d1e|/home/linhao/qb_analysis/work3/control/findutils|3c642a58d65e19068cdab83b579082b1764c53b2|UNKNOWN: no bundle tip matches current LLVM remote refs; no objects fetched|
|36-qb_analysis/work3_control_which-3a31a668|/home/linhao/qb_analysis/work3/control/which|a981379118f5f702c2c10641be4abe8d1844af92|UNKNOWN: no bundle tip matches current LLVM remote refs; no objects fetched|
|36-qb_analysis/work3_coreutils-38da01e5|/home/linhao/qb_analysis/work3/coreutils|9199f8fcc3ae026925098254b9be9a1ef9b42095|UNKNOWN: no bundle tip matches current LLVM remote refs; no objects fetched|
|36-qb_analysis/work3_findutils-01add93a|/home/linhao/qb_analysis/work3/findutils|242a7683b6551eca6d76bbc2b5f28dd019ea7110|UNKNOWN: no bundle tip matches current LLVM remote refs; no objects fetched|

全部分支名、bundle头、原stash/工作树补丁记录、未覆盖提交原文见backup-bundle-summary.json。仅用本地已有对象与当前广告引用的交集证明覆盖；UNKNOWN不等于已证明未发布。findutils/coreutils/which不是LLVM项目，未访问其远端，覆盖状态UNKNOWN。目录保持原样。
