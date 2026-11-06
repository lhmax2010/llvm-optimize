# 67. 90 TU 输入恢复与 Toolchain 调试信息逐项比较

90 份输入全部从保留副本恢复，SHA256 与 53 号清单逐项一致；没有重新预处理，也没有重跑 90 TU。132 对调试文件全部检查完成，按本次指定的文本替换规则为 **0 PASS、132 DIFFERENT、0 UNKNOWN**。差异已归因于行表编码长度，以及 8 个文件的 19 处编译目录重复斜杠；其他要求严格比较的节全部逐字节相同。

## 1. 范围、执行条件与证据

- 日期：2026-11-06，Asia/Shanghai。第一项改接因上游前提不成立停止，见 [68 号](68_rebase_on_tizen_base.md)；第二、三项继续串行完成。
- 全部本机命令放入独立 systemd 用户服务，服务之间不并行：MemoryMax=8G、MemorySwapMax=0、CPUQuota=400%、Nice=19、IOSchedulingClass=idle（ionice -c3）。没有演练或构建，没有 sudo。
- [service-policy.json](../../tools/bolt/results/tu-dwarf-20261106/service-policy.json) 实读 memory.max=8589934592、memory.swap.max=0、cpu.max=400000 100000、nice=19。DWARF 服务末次 memory.events 的 oom=0、oom_kill=0、oom_group_kill=0；max=7081 是触及限额/回收事件，不是 OOM。
- 历史构建根和原产物只读，没有删除文件；LLVM 源码、spec、helper 未修改。仅两个现用本地验证入口更新输入清单路径。
- DWARF 服务正常退出，运行 2h 24min 29.124s。每侧输入的三种导出合计限时 30 分钟；最大实际导出耗时 667.469 秒，最大整对检查耗时 1547.746 秒，均未超过 30 分钟。
- 完整原始/归一化导出和 stderr 保留在 W/temp/dwarf-check-20261106/，合计 32066624394 B；逐文件路径、大小与 SHA 见 [raw-dump-manifest.json](../../tools/bolt/results/tu-dwarf-20261106/raw-dump-manifest.json)。完整差异前后各 5 行原文已复制到本仓库 contexts/，合计 16899073 B。
- [dwarf-service-end.txt](../../tools/bolt/results/tu-dwarf-20261106/dwarf-service-end.txt) 保留 systemd-run 原样结束输出。其中退出后显示的 Memory peak=508.0K 不用作整个工作负载的内存峰值结论；本任务只据限额配置与 memory.events 判断限制和 OOM。

## 2. 输入恢复

原清单：W/docs/53_hybrid_local_validation_evidence/tu-inputs.json。[original-tu-inputs.json](../../tools/bolt/results/tu-dwarf-20261106/original-tu-inputs.json) 保留原始内容；[restored-inputs.json](../../tools/bolt/results/tu-dwarf-20261106/restored-inputs.json) 保留每项原路径、原 argv、provenance.asset_preprocessing_argv、找到的副本路径及恢复路径。

| 项目 | 结果 |
|---|---:|
| 原清单条目 | 90 |
| 找到并复制同 SHA 副本 | 90 |
| 重新生成 | 0 |
| 未恢复 | 0 |
| 唯一内容 SHA | 60 |
| 复制的实际文件字节数 | 677,747,108 |
| armv7l / aarch64 / x86_64 | 各 30 |

新目录为 W/temp/tu-inputs-restored-20261106/，包含 000.ii–089.ii、tu-inputs.json 和 SHA256SUMS。全部命中来源为 W/temp/debuglink-20261028/full-20261030/validation-work/objects-current/<编号>/input.ii；原副本未修改。

搜索设整体 900 秒、单文件 SHA 45 秒限时；实际 264.265 秒，检查 148,380 个目录和 1,372,984 个文件元数据。存在 9 个 Permission denied 盲区，原文见 [restore-search.json](../../tools/bolt/results/tu-dwarf-20261106/restore-search.json)；所需 90 项均已找到并逐项 SHA 复核，盲区不影响恢复结果。没有使用宿主工具链重新生成任何输入。

以下编号同时对应新目录 <编号>.ii 与来源 objects-current/<编号>/input.ii。完整源文件路径和预处理命令见 restored-inputs.json，表中列源文件名便于检索。

| 编号 | 目标 | 原始源文件 | 字节数 | SHA256 |
|---|---|---|---:|---|
| 000 | armv7l-tizen-linux-gnueabi | SemaStmt.cpp | 9146650 | 343d8b0305811dd8fe96e36e2da421adb51ce25f93813e0fe6380f064f205ee6 |
| 001 | aarch64-tizen-linux-gnu | SemaStmt.cpp | 9145170 | d03fb3ec5be452f0ffaaf69af9ac8f611f5d2b7564a65d19dbf2fe7d88a90154 |
| 002 | x86_64-tizen-linux-gnu | SemaStmt.cpp | 9218290 | 14739bf225c299981d085311084429c1948ba4634b862d3ba517ca95d2dcfa07 |
| 003 | armv7l-tizen-linux-gnueabi | SemaExprCXX.cpp | 10236566 | 3f64a5489730d6bb1f0110bcdc538ec4ad2cf4ed5ba40a959fa0003720f7c842 |
| 004 | aarch64-tizen-linux-gnu | SemaExprCXX.cpp | 10235048 | 4e842590020cf760498f018a778b092f997f0e1962708daa051f8f53293a3398 |
| 005 | x86_64-tizen-linux-gnu | SemaExprCXX.cpp | 10308590 | 41e7ff2bd6f5a25fc4d1c2eaff9262e586a1b6f7916d417f3c67c0677fe78b5f |
| 006 | armv7l-tizen-linux-gnueabi | SelectionDAG.cpp | 6697511 | dd9dbea2aa676688a8e35911a1738955c499d38096a9349b506cbafee950c8fc |
| 007 | aarch64-tizen-linux-gnu | SelectionDAG.cpp | 6696120 | 7373b1e1d903218c18d6f88d8a2136d0feb0e63f7824f403fd6039298ca5da0a |
| 008 | x86_64-tizen-linux-gnu | SelectionDAG.cpp | 6768946 | 16cc3ae1b9d0335095118bc298c9d789f3c5a3ec03f44fc78e2384438910b00b |
| 009 | armv7l-tizen-linux-gnueabi | MachinePipeliner.cpp | 6623411 | 1c4a75e0b471c1ae901aeaaa21576856bff1797e6ba649b02056d79b71adcb15 |
| 010 | aarch64-tizen-linux-gnu | MachinePipeliner.cpp | 6620488 | abb9b93c438a1687f2d4c2a535ff43ac6d1f9262933081ec63ac154e8dfde2ba |
| 011 | x86_64-tizen-linux-gnu | MachinePipeliner.cpp | 6705389 | e8f9950ca7517abc479c24855a3fc976d104a71dc7b89cd9b5c7c02c277754eb |
| 012 | armv7l-tizen-linux-gnueabi | Attributor.cpp | 5539456 | 0946ff2d18b66a3406bdac8ff962b7e201b01e6ed69ca833f36f0e269f39e6fb |
| 013 | aarch64-tizen-linux-gnu | Attributor.cpp | 5538288 | 621f9f708e6501a4a4b3b492de585094e64d2e71aeda65ae650a05518a69fca7 |
| 014 | x86_64-tizen-linux-gnu | Attributor.cpp | 5608797 | 9769ddff5c7d89bf18a1b316bca7b8ef76b861daee9477d61c227149a1cdcbdd |
| 015 | armv7l-tizen-linux-gnueabi | WholeProgramDevirt.cpp | 5721218 | 5061ecab335e485c8449a5663cd2ef09dd680a93b3f64e0c1ee994609b22f3a7 |
| 016 | aarch64-tizen-linux-gnu | WholeProgramDevirt.cpp | 5763500 | c4276508f580e9c9eb88eb0b30dd0a265ed1b16d4bba6901aed80668f8773082 |
| 017 | x86_64-tizen-linux-gnu | WholeProgramDevirt.cpp | 5818446 | 4fc1da025b124d3b9ab13668b626ff0588157bd770937ce5b8bef448d12fcc57 |
| 018 | armv7l-tizen-linux-gnueabi | ARMISelLowering.cpp | 8277526 | bc09b475f9ab816bafcfc16b7248a6447c630769ad40878082998b5e8e466320 |
| 019 | aarch64-tizen-linux-gnu | ARMISelLowering.cpp | 8276007 | 874346b20c77c8b660da318211c0e2771108faa79ef48fdad1430adff27364a9 |
| 020 | x86_64-tizen-linux-gnu | ARMISelLowering.cpp | 8350433 | 5ef46eae369475b0a26469ffe34d74fc33770eeb355ce1a0fd9591f3335c3c25 |
| 021 | armv7l-tizen-linux-gnueabi | ARMTargetTransformInfo.cpp | 7665371 | 15fec0c045e021e0c635923c818433e6abe73af7dcf17e88655136ba0a74bce7 |
| 022 | aarch64-tizen-linux-gnu | ARMTargetTransformInfo.cpp | 7663854 | 202c0a2b0032dbdb52e5cac233a55ac65febd1291b10093c3136a607876fa181 |
| 023 | x86_64-tizen-linux-gnu | ARMTargetTransformInfo.cpp | 7738280 | 4e7920b6fc1053830903049cfba770cf70687ecda7d0674e6f1b0f6b5ea9b9f5 |
| 024 | armv7l-tizen-linux-gnueabi | MasmParser.cpp | 3941055 | 2322579d53376cbf476b8cb034c5ac75060fe952b7935757b4cf70eeb024bd0f |
| 025 | aarch64-tizen-linux-gnu | MasmParser.cpp | 3940005 | fbe1bd4c100066c8d40fcb468fae12bf341179e21f144b969e1ebbc7922ef1ea |
| 026 | x86_64-tizen-linux-gnu | MasmParser.cpp | 4008414 | b30eaaec94e2a47d531efcb7c664f4bf16bcb55995f5455329e876976b6ba22a |
| 027 | armv7l-tizen-linux-gnueabi | AsmParser.cpp | 4066265 | 7983fbd1866b93f522e5c63a2c927a3b3b6858572d009248183da35d864ea241 |
| 028 | aarch64-tizen-linux-gnu | AsmParser.cpp | 4065043 | a41f558f22dc16f20a9e0f98297331cca796b6610a26b5cf85b0c30b320951fb |
| 029 | x86_64-tizen-linux-gnu | AsmParser.cpp | 4134738 | ef4599e65546e561c4cc4d4d317c5559613f3699f26f45e824b46cc3f116698c |
| 030 | armv7l-tizen-linux-gnueabi | ParentMapContext.cpp | 8461841 | 385ce6262972ed3ab2fdf1ae38758258a1245266500705eba12abd464cd735d3 |
| 031 | aarch64-tizen-linux-gnu | ParentMapContext.cpp | 8461224 | 56ced4cf5bdf0c0f8fcb8d36b1e054936278469012d668463c275ae512546a28 |
| 032 | x86_64-tizen-linux-gnu | ParentMapContext.cpp | 8526907 | 996321863f27c976f2a2135279b1a1402aa310b6b3dd6587409025be4a0d02ef |
| 033 | armv7l-tizen-linux-gnueabi | ParseDecl.cpp | 9132995 | c8390092bf08486ee044021ac6dca8f376766e3e9d265ae00bf5c2e8afefa3c4 |
| 034 | aarch64-tizen-linux-gnu | ParseDecl.cpp | 9131460 | a54626f1cf32df61c2e7aba4acf6b383f2f3a82263ade9b432440f38b9ed7eee |
| 035 | x86_64-tizen-linux-gnu | ParseDecl.cpp | 9204969 | 1fc0197665f0830662cbb0812e0e6c27511502dd056b6ef6f6bb71e7a36ca8a0 |
| 036 | armv7l-tizen-linux-gnueabi | Driver.cpp | 4442459 | e9088dc32c6738c7bdaa2cc0a4eef731b5ad3a25d9fcb4f2da70b8a35f661c80 |
| 037 | aarch64-tizen-linux-gnu | Driver.cpp | 4441844 | 52795efac94f65c10458411ec7cdc9320476443b06c29b196251dfee754ec2bd |
| 038 | x86_64-tizen-linux-gnu | Driver.cpp | 4509192 | 82278e78bae454462a7cb613f39b41ce3d13a1aa1e8ededf221e33c8f8e4cde8 |
| 039 | armv7l-tizen-linux-gnueabi | CoverageMappingGen.cpp | 10795647 | a76c940883a7614538d51b1cf3f4f61958f02c1d6575a3552fe0a43983111600 |
| 040 | aarch64-tizen-linux-gnu | CoverageMappingGen.cpp | 10834433 | 6c5e545cae88d9d7db36ab447c9e9cfc9fd53bd01298bd030aea9be96bfae11c |
| 041 | x86_64-tizen-linux-gnu | CoverageMappingGen.cpp | 10902824 | 9b7de19a21321a55d039098ab8ce1ebdae9c6dfbb60bdee6b6cc669eeca41256 |
| 042 | armv7l-tizen-linux-gnueabi | Metadata.cpp | 4233254 | 5b553b4f957298bb89205827f641d3e97fea2b6fe25457f1d49c1a375fc598b2 |
| 043 | aarch64-tizen-linux-gnu | Metadata.cpp | 4233305 | 284fec52edb6e469f96c4abebecb7806a2994307b52fedc89da39bae04efd8bf |
| 044 | x86_64-tizen-linux-gnu | Metadata.cpp | 4293565 | a51e08eee2534212433f7edf471eec55bf7e1b9aca266f3c5f6b37be6e4eeef8 |
| 045 | armv7l-tizen-linux-gnueabi | ScalarEvolution.cpp | 5545017 | bd9493a92daa7e1e426d2b238877a55fd65ffde786e131b42b11fe15a8d20bb6 |
| 046 | aarch64-tizen-linux-gnu | ScalarEvolution.cpp | 5544012 | a6d9bb923f7f602d5a3445cf52852028bd97508ab57138d9bff14cede4b27e64 |
| 047 | x86_64-tizen-linux-gnu | ScalarEvolution.cpp | 5612935 | e84c6cff85743e6baacc21b4b9ec6f8e21071498281c4eb6b7c4c8b8a708e6d9 |
| 048 | armv7l-tizen-linux-gnueabi | AArch64InstructionSelector.cpp | 18959385 | 1aededac191c1b03a84bff3abf2cfa73fa7329a93016e7bc2c60c183b8088db2 |
| 049 | aarch64-tizen-linux-gnu | AArch64InstructionSelector.cpp | 18957961 | 5cd725ae1fbc6d64f660e3eb1aab462db315789e2584b8769d02f8084466f014 |
| 050 | x86_64-tizen-linux-gnu | AArch64InstructionSelector.cpp | 19031163 | 94cba1c7d22778cb48f9bd123d825a5d132e8a0d94f34b8fbeedd8edb2cbd620 |
| 051 | armv7l-tizen-linux-gnueabi | X86ISelDAGToDAG.cpp | 19667856 | 074f7a1694d3cbe9922cd6e825a72a5de8a90ced8311a45b3f93e5ed75e55532 |
| 052 | aarch64-tizen-linux-gnu | X86ISelDAGToDAG.cpp | 19666483 | 200d0de228c70f4028b7ab4649b5fb4297432c8e9cb2d91d9ab032f7e1696b10 |
| 053 | x86_64-tizen-linux-gnu | X86ISelDAGToDAG.cpp | 19739071 | 52fc2e93a61d14101e171756e898f101d56b9da7a186f9bf48cfa19ff7db1cdd |
| 054 | armv7l-tizen-linux-gnueabi | ELF.cpp | 2881638 | 1c72f877e498aa4b92c87d31a8630b811b3a044b80e3b8f27bf58aa209769357 |
| 055 | aarch64-tizen-linux-gnu | ELF.cpp | 2882206 | d1080e449439fec5040c4dd074709b8fd82ff2f4896af7ba202b5a98bebff67f |
| 056 | x86_64-tizen-linux-gnu | ELF.cpp | 2937328 | 8583d6b6e522c13528c45fbce2e20dc1b75628b8e90120648842d282ff21b961 |
| 057 | armv7l-tizen-linux-gnueabi | InstrProfReader.cpp | 5179752 | 37d73ce0ff7b876820eedee4b4ad96ed3f58c97bf05125f91925b3a9cf6551b9 |
| 058 | aarch64-tizen-linux-gnu | InstrProfReader.cpp | 5219384 | 96264b9e29ed46b24c09076892f03ff635936ee607491f774eaef144f32ba94f |
| 059 | x86_64-tizen-linux-gnu | InstrProfReader.cpp | 5279248 | cecd835503b0fb35c57144f2da2a3b7633ca172024a5a2c949463c3d8d6c35bc |
| 060 | armv7l-tizen-linux-gnueabi | SemaStmt.cpp | 9146650 | 343d8b0305811dd8fe96e36e2da421adb51ce25f93813e0fe6380f064f205ee6 |
| 061 | aarch64-tizen-linux-gnu | SemaStmt.cpp | 9145170 | d03fb3ec5be452f0ffaaf69af9ac8f611f5d2b7564a65d19dbf2fe7d88a90154 |
| 062 | x86_64-tizen-linux-gnu | SemaStmt.cpp | 9218290 | 14739bf225c299981d085311084429c1948ba4634b862d3ba517ca95d2dcfa07 |
| 063 | armv7l-tizen-linux-gnueabi | SemaExprCXX.cpp | 10236566 | 3f64a5489730d6bb1f0110bcdc538ec4ad2cf4ed5ba40a959fa0003720f7c842 |
| 064 | aarch64-tizen-linux-gnu | SemaExprCXX.cpp | 10235048 | 4e842590020cf760498f018a778b092f997f0e1962708daa051f8f53293a3398 |
| 065 | x86_64-tizen-linux-gnu | SemaExprCXX.cpp | 10308590 | 41e7ff2bd6f5a25fc4d1c2eaff9262e586a1b6f7916d417f3c67c0677fe78b5f |
| 066 | armv7l-tizen-linux-gnueabi | SelectionDAG.cpp | 6697511 | dd9dbea2aa676688a8e35911a1738955c499d38096a9349b506cbafee950c8fc |
| 067 | aarch64-tizen-linux-gnu | SelectionDAG.cpp | 6696120 | 7373b1e1d903218c18d6f88d8a2136d0feb0e63f7824f403fd6039298ca5da0a |
| 068 | x86_64-tizen-linux-gnu | SelectionDAG.cpp | 6768946 | 16cc3ae1b9d0335095118bc298c9d789f3c5a3ec03f44fc78e2384438910b00b |
| 069 | armv7l-tizen-linux-gnueabi | MachinePipeliner.cpp | 6623411 | 1c4a75e0b471c1ae901aeaaa21576856bff1797e6ba649b02056d79b71adcb15 |
| 070 | aarch64-tizen-linux-gnu | MachinePipeliner.cpp | 6620488 | abb9b93c438a1687f2d4c2a535ff43ac6d1f9262933081ec63ac154e8dfde2ba |
| 071 | x86_64-tizen-linux-gnu | MachinePipeliner.cpp | 6705389 | e8f9950ca7517abc479c24855a3fc976d104a71dc7b89cd9b5c7c02c277754eb |
| 072 | armv7l-tizen-linux-gnueabi | Attributor.cpp | 5539456 | 0946ff2d18b66a3406bdac8ff962b7e201b01e6ed69ca833f36f0e269f39e6fb |
| 073 | aarch64-tizen-linux-gnu | Attributor.cpp | 5538288 | 621f9f708e6501a4a4b3b492de585094e64d2e71aeda65ae650a05518a69fca7 |
| 074 | x86_64-tizen-linux-gnu | Attributor.cpp | 5608797 | 9769ddff5c7d89bf18a1b316bca7b8ef76b861daee9477d61c227149a1cdcbdd |
| 075 | armv7l-tizen-linux-gnueabi | WholeProgramDevirt.cpp | 5721218 | 5061ecab335e485c8449a5663cd2ef09dd680a93b3f64e0c1ee994609b22f3a7 |
| 076 | aarch64-tizen-linux-gnu | WholeProgramDevirt.cpp | 5763500 | c4276508f580e9c9eb88eb0b30dd0a265ed1b16d4bba6901aed80668f8773082 |
| 077 | x86_64-tizen-linux-gnu | WholeProgramDevirt.cpp | 5818446 | 4fc1da025b124d3b9ab13668b626ff0588157bd770937ce5b8bef448d12fcc57 |
| 078 | armv7l-tizen-linux-gnueabi | ARMISelLowering.cpp | 8277526 | bc09b475f9ab816bafcfc16b7248a6447c630769ad40878082998b5e8e466320 |
| 079 | aarch64-tizen-linux-gnu | ARMISelLowering.cpp | 8276007 | 874346b20c77c8b660da318211c0e2771108faa79ef48fdad1430adff27364a9 |
| 080 | x86_64-tizen-linux-gnu | ARMISelLowering.cpp | 8350433 | 5ef46eae369475b0a26469ffe34d74fc33770eeb355ce1a0fd9591f3335c3c25 |
| 081 | armv7l-tizen-linux-gnueabi | ARMTargetTransformInfo.cpp | 7665371 | 15fec0c045e021e0c635923c818433e6abe73af7dcf17e88655136ba0a74bce7 |
| 082 | aarch64-tizen-linux-gnu | ARMTargetTransformInfo.cpp | 7663854 | 202c0a2b0032dbdb52e5cac233a55ac65febd1291b10093c3136a607876fa181 |
| 083 | x86_64-tizen-linux-gnu | ARMTargetTransformInfo.cpp | 7738280 | 4e7920b6fc1053830903049cfba770cf70687ecda7d0674e6f1b0f6b5ea9b9f5 |
| 084 | armv7l-tizen-linux-gnueabi | MasmParser.cpp | 3941055 | 2322579d53376cbf476b8cb034c5ac75060fe952b7935757b4cf70eeb024bd0f |
| 085 | aarch64-tizen-linux-gnu | MasmParser.cpp | 3940005 | fbe1bd4c100066c8d40fcb468fae12bf341179e21f144b969e1ebbc7922ef1ea |
| 086 | x86_64-tizen-linux-gnu | MasmParser.cpp | 4008414 | b30eaaec94e2a47d531efcb7c664f4bf16bcb55995f5455329e876976b6ba22a |
| 087 | armv7l-tizen-linux-gnueabi | AsmParser.cpp | 4066265 | 7983fbd1866b93f522e5c63a2c927a3b3b6858572d009248183da35d864ea241 |
| 088 | aarch64-tizen-linux-gnu | AsmParser.cpp | 4065043 | a41f558f22dc16f20a9e0f98297331cca796b6610a26b5cf85b0c30b320951fb |
| 089 | x86_64-tizen-linux-gnu | AsmParser.cpp | 4134738 | ef4599e65546e561c4cc4d4d317c5559613f3699f26f45e824b46cc3f116698c |

## 3. 本地验证入口与测试

只改两个现用入口的一个路径行：

- tools/bolt/night-launch-20261105/validation_common.py:65
- tools/bolt/night-launch-20261103/validate.py:65

两者从旧 docs/53_hybrid_local_validation_evidence/tu-inputs.json 改读 temp/tu-inputs-restored-20261106/tu-inputs.json。原来的逐输入 SHA 检查保留，完整 diff 和前后脚本 SHA 见 [script-changes.diff](../../tools/bolt/results/tu-dwarf-20261106/script-changes.diff)、[script-changes.json](../../tools/bolt/results/tu-dwarf-20261106/script-changes.json)。

tools/ 下引用检索见 [tu-script-references.json](../../tools/bolt/results/tu-dwarf-20261106/tu-script-references.json)。results/ 下的历史验证脚本、测量脚本与报告生成器是历史证据，保留原文和原 SHA；不把它们作为现用入口，也不原地运行。今后重放历史脚本时应先复制并改接新清单。其余现用入口未发现旧清单引用。

测试直接提取现用 objects() 的清单读取语句和 SHA 断言：验证 90 项元数据与原清单一致、全部输入 SHA、有效副本可通过、改坏字节必被拒绝、两个现用入口没有旧清单路径。

```text
test_actual_entry_manifest (__main__.Restored.test_actual_entry_manifest) ... ok
test_actual_guard_rejects_changed_bytes (__main__.Restored.test_actual_guard_rejects_changed_bytes) ... ok
test_all_90_file_sha (__main__.Restored.test_all_90_file_sha) ... ok
test_no_old_manifest_in_active_entries (__main__.Restored.test_no_old_manifest_in_active_entries) ... ok

----------------------------------------------------------------------
Ran 4 tests in 6.374s

OK
```

没有重跑 63 号的 90 TU，也没有把 SHA 恢复检查说成编译正确性重测。

## 4. DWARF 检查方法

配对表来自 63 号保留的 validation/qb-changed-file-paths.json，筛出全部 132 对 .debug；本地来自 W/temp/night-20261105/toolchain，QB 来自 1216409 的已解包完整 RPM。每个文件导出前均核对配对表中记录的 SHA。配对完整路径、包名和两边 SHA 见 [dwarf-pairs.json](../../tools/bolt/results/tu-dwarf-20261106/dwarf-pairs.json)。

平台工具版本为 LLVM 22.1.8，不使用宿主 llvm-dwarfdump。[dwarfdump-tool.json](../../tools/bolt/results/tu-dwarf-20261106/dwarfdump-tool.json) 记录路径、版本与 SHA：

- llvm-dwarfdump：99f508775e7c5d0dbfbfef133b4cc97e1895a8b8836635e2770bb76f9fa2b147
- loader：7f937712d3dbebe4dce08fda30c8699c8245a3d5ddf45aebf1b211f7cc1b4ab1

实际 argv 模式如下（所有 792 次导出的完整 argv、rc、耗时、行数和摘要见 [dwarf-results.json.gz](../../tools/bolt/results/tu-dwarf-20261106/dwarf-results.json.gz)）：

```text
/home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/lib64/ld-linux-x86-64.so.2 --library-path /home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/lib64:/home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64 /home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/bin/llvm-dwarfdump --debug-info <file>
同样分别执行 --debug-line 和 --debug-aranges。
```

132 对均没有 .debug_str_offsets，故 str-offsets 导出不适用。全部导出 rc=0，stderr 均为空。文本逐行处理；每个差异区间完整保留前后各 5 行，长区间流式写入 gzip，摘要只保留有限样例。

归一化限定为：源码路径前缀 usr/src/debug/llvm-22.1.8-1.x86_64 → usr/src/debug/llvm-22.1.8-2.1.x86_64；输出文件名标题；DIE 行首偏移、debug_line[...] 位置、next unit at、abbr_offset/cu_offset/debug_info_offset/str_offsets_base、DW_AT_stmt_list 与显式字符串位置字段。不会删除实际 PC、地址范围、DW_OP 值、行列值、类型引用值或长度字段，也不折叠重复斜杠。实现为 [dwarf_check.py](../../tools/bolt/results/tu-dwarf-20261106/dwarf_check.py)。

```text
test_length_retained (__main__.Tests.test_length_retained) ... ok
test_offset (__main__.Tests.test_offset) ... ok
test_path (__main__.Tests.test_path) ... ok
test_real_address (__main__.Tests.test_real_address) ... ok
test_type_reference_retained (__main__.Tests.test_type_reference_retained) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.000s

OK
```

## 5. 总体结果与差异分类

| 检查 | 完全相同 | 有差异 | UNKNOWN |
|---|---:|---:|---:|
| 整个文件的指定归一化文本 | 0 | 132 | 0 |
| --debug-info | 124 | 8（19 行） | 0 |
| --debug-line | 0 | 132（176,482 行） | 0 |
| --debug-aranges | 132 | 0 | 0 |
| 节数量、名称及顺序 | 132 | 0 | 0 |
| 除 .debug_info/.debug_line/.debug_str/.debug_aranges 外的节内容 | 132 | 0 | 0 |

### 5.1 行表编码长度

176,482 处差异全部为 total_length 或 prologue_length。没有把长度值作为偏移列删除，因此这些文件严格文本结论保持 DIFFERENT。例如 libRemarks.so.22.1.debug：

```text
old: total_length: 0x0000015a    new: total_length: 0x0000015c
old: prologue_length: 0x0000013e new: prologue_length: 0x00000140
```

进一步按真实 .debug_line 二进制逐单元核对，共 88,987 个单元、132 对全部通过以下辅助归因检查：格式/版本前缀相同；目录和文件表头仅替换获批源码前缀后逐字节相同；行号程序本身逐字节相同；total_length 和 prologue_length 的增加值都精确等于路径替换次数 × 2 字节。完整单元旧值、新值、偏移与逐项断言见 [line-unit-proof.jsonl.gz](../../tools/bolt/results/tu-dwarf-20261106/line-unit-proof.jsonl.gz)，逐文件汇总见 [line-unit-proof-summary.json](../../tools/bolt/results/tu-dwarf-20261106/line-unit-proof-summary.json)，实现见 [classify_dwarf.py](../../tools/bolt/results/tu-dwarf-20261106/classify_dwarf.py)。

这证明行表长度差异来自版本路径从 -1 增长为 -2.1，并非地址或行号程序变化。辅助归因 PASS 不替换上面的严格文本 DIFFERENT。

### 5.2 8 个文件、19 处 DW_AT_comp_dir

| 文件 | 差异行数 |
|---|---:|
| usr/lib/debug/usr/lib64/clang/22/lib/linux/libclang_rt.hwasan-x86_64.so.debug | 2 |
| usr/lib/debug/usr/lib64/clang/22/lib/linux/libclang_rt.hwasan_aliases-x86_64.so.debug | 2 |
| usr/lib/debug/usr/lib64/clang/22/lib/linux/libclang_rt.asan-x86_64.so.debug | 1 |
| usr/lib/debug/usr/lib64/clang/22/lib/linux/libclang_rt.tsan-x86_64.so.debug | 1 |
| usr/lib/debug/usr/lib64/libomp.so.debug | 1 |
| usr/lib/debug/usr/bin/llvm-exegesis.debug | 4 |
| usr/lib/debug/usr/bin/lld.debug | 4 |
| usr/lib/debug/usr/lib64/libLLVM.so.22.1.debug | 4 |

源码前缀替换后，剩余差异是内部重复斜杠数量；所有 19 处按 POSIX 路径词法归一化都指向同一目录。但用户本轮只授权前缀替换和位置偏移处理，所以这里不额外折叠斜杠，不把这些属性行改判为文本相同。全部 19 行原文、行号和词法核对见 [attribute-differences.json](../../tools/bolt/results/tu-dwarf-20261106/attribute-differences.json)。不同原文组合及出现次数如下：

```text
occurrences=19
old: DW_AT_comp_dir	("/usr/src/debug/llvm-22.1.8-1.x86_64/////build")
new: DW_AT_comp_dir	("/usr/src/debug/llvm-22.1.8-2.1.x86_64///build")
```

未发现除此之外的属性、类型引用、实际 PC、地址范围或行号文本差异；UNKNOWN=0。分类计数原文见 [classification-summary.json](../../tools/bolt/results/tu-dwarf-20261106/classification-summary.json)。

## 6. 132 对逐文件清单

路径均相对 /usr/lib/debug/；info 一列标出差异行数，line 一列为长度字段差异行数。每行链接为包含差异及前后各 5 行的完整原文；aranges 与其他节检查均 PASS，strict 均 DIFFERENT。

| 编号 | 文件 | info | line | 原文上下文 |
|---:|---|---|---:|---|
| 0 | usr/lib64/libRemarks.so.22.1.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/000-debug_line.txt.gz) |
| 1 | usr/lib64/clang/22/lib/linux/libclang_rt.ubsan_minimal-x86_64.so.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/001-debug_line.txt.gz) |
| 2 | usr/share/gdb/python/ompd/ompdModule.so.debug | PASS | 4 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/002-debug_line.txt.gz) |
| 3 | usr/lib64/liblldbIntelFeatures.so.22.1.debug | PASS | 4 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/003-debug_line.txt.gz) |
| 4 | usr/bin/sanstats.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/004-debug_line.txt.gz) |
| 5 | home/owner/share/tmp/sdk_tools/lldb/bin/lldb-argdumper.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/005-debug_line.txt.gz) |
| 6 | usr/bin/llvm-cxxfilt.debug | PASS | 4 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/006-debug_line.txt.gz) |
| 7 | usr/bin/reduce-chunk-list.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/007-debug_line.txt.gz) |
| 8 | usr/bin/llvm-bcanalyzer.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/008-debug_line.txt.gz) |
| 9 | usr/bin/llvm-modextract.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/009-debug_line.txt.gz) |
| 10 | usr/bin/llvm-mt.debug | PASS | 4 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/010-debug_line.txt.gz) |
| 11 | usr/bin/llvm-cxxmap.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/011-debug_line.txt.gz) |
| 12 | usr/bin/llvm-undname.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/012-debug_line.txt.gz) |
| 13 | usr/bin/llvm-strings.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/013-debug_line.txt.gz) |
| 14 | usr/bin/llvm-ctxprof-util.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/014-debug_line.txt.gz) |
| 15 | usr/bin/llvm-c-test.debug | PASS | 26 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/015-debug_line.txt.gz) |
| 16 | usr/bin/llvm-cvtres.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/016-debug_line.txt.gz) |
| 17 | usr/bin/llvm-cat.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/017-debug_line.txt.gz) |
| 18 | usr/bin/llvm-as.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/018-debug_line.txt.gz) |
| 19 | usr/bin/llvm-cas.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/019-debug_line.txt.gz) |
| 20 | usr/lib64/libarcher.so.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/020-debug_line.txt.gz) |
| 21 | usr/bin/llvm-offload-wrapper.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/021-debug_line.txt.gz) |
| 22 | usr/lib64/libompd.so.debug | PASS | 16 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/022-debug_line.txt.gz) |
| 23 | usr/bin/llvm-tli-checker.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/023-debug_line.txt.gz) |
| 24 | usr/lib64/clang/22/lib/linux/libclang_rt.dyndd-x86_64.so.debug | PASS | 90 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/024-debug_line.txt.gz) |
| 25 | usr/bin/clang-extdef-mapping.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/025-debug_line.txt.gz) |
| 26 | usr/bin/clang-offload-bundler.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/026-debug_line.txt.gz) |
| 27 | usr/bin/llvm-stress.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/027-debug_line.txt.gz) |
| 28 | usr/lib64/clang/22/lib/linux/libclang_rt.ubsan_standalone-x86_64.so.debug | PASS | 114 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/028-debug_line.txt.gz) |
| 29 | usr/lib64/libLTO.so.22.1.debug | PASS | 4 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/029-debug_line.txt.gz) |
| 30 | usr/bin/llvm-sim.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/030-debug_line.txt.gz) |
| 31 | usr/bin/llvm-offload-binary.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/031-debug_line.txt.gz) |
| 32 | usr/bin/llvm-dis.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/032-debug_line.txt.gz) |
| 33 | usr/bin/llvm-cgdata.debug | PASS | 4 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/033-debug_line.txt.gz) |
| 34 | usr/bin/llvm-ml.debug | PASS | 6 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/034-debug_line.txt.gz) |
| 35 | usr/bin/offload-arch.debug | PASS | 12 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/035-debug_line.txt.gz) |
| 36 | usr/bin/verify-uselistorder.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/036-debug_line.txt.gz) |
| 37 | usr/bin/clang-check.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/037-debug_line.txt.gz) |
| 38 | usr/bin/llvm-dwp.debug | PASS | 4 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/038-debug_line.txt.gz) |
| 39 | usr/bin/llvm-size.debug | PASS | 4 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/039-debug_line.txt.gz) |
| 40 | usr/lib64/clang/22/lib/linux/libclang_rt.nsan-x86_64.so.debug | PASS | 120 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/040-debug_line.txt.gz) |
| 41 | usr/lib64/clang/22/lib/linux/libclang_rt.scudo_standalone-x86_64.so.debug | PASS | 54 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/041-debug_line.txt.gz) |
| 42 | usr/bin/pp-trace.debug | PASS | 6 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/042-debug_line.txt.gz) |
| 43 | usr/bin/clang-repl.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/043-debug_line.txt.gz) |
| 44 | usr/bin/llvm-lipo.debug | PASS | 4 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/044-debug_line.txt.gz) |
| 45 | usr/bin/llvm-ifs.debug | PASS | 8 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/045-debug_line.txt.gz) |
| 46 | usr/bin/llvm-debuginfod-find.debug | PASS | 12 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/046-debug_line.txt.gz) |
| 47 | usr/bin/llvm-opt-report.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/047-debug_line.txt.gz) |
| 48 | usr/bin/llvm-gsymutil.debug | PASS | 4 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/048-debug_line.txt.gz) |
| 49 | usr/bin/llvm-link.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/049-debug_line.txt.gz) |
| 50 | usr/bin/yaml2macho-core.debug | PASS | 26 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/050-debug_line.txt.gz) |
| 51 | usr/bin/llvm-split.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/051-debug_line.txt.gz) |
| 52 | usr/lib64/clang/22/lib/linux/libclang_rt.hwasan-x86_64.so.debug | DIFFERENT 2 | 144 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/052-debug_line.txt.gz) / [info](../../tools/bolt/results/tu-dwarf-20261106/contexts/052-debug_info.txt.gz) |
| 53 | usr/bin/clang-format.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/053-debug_line.txt.gz) |
| 54 | usr/lib64/clang/22/lib/linux/libclang_rt.hwasan_aliases-x86_64.so.debug | DIFFERENT 2 | 144 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/054-debug_line.txt.gz) / [info](../../tools/bolt/results/tu-dwarf-20261106/contexts/054-debug_info.txt.gz) |
| 55 | usr/lib64/clang/22/lib/linux/libclang_rt.memprof-x86_64.so.debug | PASS | 122 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/055-debug_line.txt.gz) |
| 56 | usr/bin/clang-sycl-linker.debug | PASS | 6 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/056-debug_line.txt.gz) |
| 57 | usr/bin/llvm-diff.debug | PASS | 14 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/057-debug_line.txt.gz) |
| 58 | usr/bin/llvm-mc.debug | PASS | 4 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/058-debug_line.txt.gz) |
| 59 | usr/bin/llvm-libtool-darwin.debug | PASS | 4 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/059-debug_line.txt.gz) |
| 60 | usr/bin/llvm-debuginfod.debug | PASS | 10 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/060-debug_line.txt.gz) |
| 61 | usr/bin/diagtool.debug | PASS | 28 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/061-debug_line.txt.gz) |
| 62 | usr/bin/llvm-cxxdump.debug | PASS | 4 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/062-debug_line.txt.gz) |
| 63 | usr/bin/clang-nvlink-wrapper.debug | PASS | 4 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/063-debug_line.txt.gz) |
| 64 | usr/bin/llvm-symbolizer.debug | PASS | 12 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/064-debug_line.txt.gz) |
| 65 | usr/bin/llvm-ir2vec.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/065-debug_line.txt.gz) |
| 66 | usr/lib64/LLVMgold.so.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/066-debug_line.txt.gz) |
| 67 | usr/bin/llvm-nm.debug | PASS | 4 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/067-debug_line.txt.gz) |
| 68 | usr/bin/llvm-lto2.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/068-debug_line.txt.gz) |
| 69 | usr/bin/llvm-rtdyld.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/069-debug_line.txt.gz) |
| 70 | usr/bin/clang-apply-replacements.debug | PASS | 4 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/070-debug_line.txt.gz) |
| 71 | usr/bin/llvm-cfi-verify.debug | PASS | 12 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/071-debug_line.txt.gz) |
| 72 | usr/bin/llvm-extract.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/072-debug_line.txt.gz) |
| 73 | usr/bin/llvm-readtapi.debug | PASS | 4 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/073-debug_line.txt.gz) |
| 74 | usr/bin/llvm-lto.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/074-debug_line.txt.gz) |
| 75 | usr/bin/sancov.debug | PASS | 4 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/075-debug_line.txt.gz) |
| 76 | usr/lib64/clang/22/lib/linux/libclang_rt.asan-x86_64.so.debug | DIFFERENT 1 | 160 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/076-debug_line.txt.gz) / [info](../../tools/bolt/results/tu-dwarf-20261106/contexts/076-debug_info.txt.gz) |
| 77 | usr/bin/clang-refactor.debug | PASS | 6 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/077-debug_line.txt.gz) |
| 78 | usr/bin/llvm-objcopy.debug | PASS | 6 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/078-debug_line.txt.gz) |
| 79 | usr/lib64/clang/22/lib/linux/libclang_rt.tsan-x86_64.so.debug | DIFFERENT 1 | 160 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/079-debug_line.txt.gz) / [info](../../tools/bolt/results/tu-dwarf-20261106/contexts/079-debug_info.txt.gz) |
| 80 | usr/bin/clang-linker-wrapper.debug | PASS | 8 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/080-debug_line.txt.gz) |
| 81 | usr/bin/llvm-dwarfdump.debug | PASS | 6 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/081-debug_line.txt.gz) |
| 82 | usr/bin/llvm-debuginfo-analyzer.debug | PASS | 4 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/082-debug_line.txt.gz) |
| 83 | usr/bin/llvm-rc.debug | PASS | 22 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/083-debug_line.txt.gz) |
| 84 | usr/bin/clang-reorder-fields.debug | PASS | 8 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/084-debug_line.txt.gz) |
| 85 | usr/bin/llvm-dwarfutil.debug | PASS | 6 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/085-debug_line.txt.gz) |
| 86 | usr/bin/clang-scan-deps.debug | PASS | 4 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/086-debug_line.txt.gz) |
| 87 | usr/bin/clang-include-fixer.debug | PASS | 18 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/087-debug_line.txt.gz) |
| 88 | usr/bin/lli.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/088-debug_line.txt.gz) |
| 89 | usr/bin/clang-installapi.debug | PASS | 6 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/089-debug_line.txt.gz) |
| 90 | usr/bin/llc.debug | PASS | 4 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/090-debug_line.txt.gz) |
| 91 | usr/bin/llvm-remarkutil.debug | PASS | 28 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/091-debug_line.txt.gz) |
| 92 | usr/bin/lldb-instr.debug | PASS | 2 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/092-debug_line.txt.gz) |
| 93 | usr/bin/clang-query.debug | PASS | 10 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/093-debug_line.txt.gz) |
| 94 | usr/bin/llvm-mca.debug | PASS | 38 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/094-debug_line.txt.gz) |
| 95 | usr/bin/find-all-symbols.debug | PASS | 28 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/095-debug_line.txt.gz) |
| 96 | usr/lib64/libomp.so.debug | DIFFERENT 1 | 332 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/096-debug_line.txt.gz) / [info](../../tools/bolt/results/tu-dwarf-20261106/contexts/096-debug_info.txt.gz) |
| 97 | usr/bin/clang-move.debug | PASS | 8 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/097-debug_line.txt.gz) |
| 98 | usr/bin/opt.debug | PASS | 6 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/098-debug_line.txt.gz) |
| 99 | usr/bin/clang-change-namespace.debug | PASS | 4 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/099-debug_line.txt.gz) |
| 100 | usr/bin/bugpoint.debug | PASS | 36 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/100-debug_line.txt.gz) |
| 101 | usr/bin/dsymutil.debug | PASS | 38 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/101-debug_line.txt.gz) |
| 102 | home/owner/share/tmp/sdk_tools/lldb/bin/lldb.debug | PASS | 164 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/102-debug_line.txt.gz) |
| 103 | usr/bin/llvm-config.debug | PASS | 218 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/103-debug_line.txt.gz) |
| 104 | usr/bin/llvm-xray.debug | PASS | 28 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/104-debug_line.txt.gz) |
| 105 | usr/bin/modularize.debug | PASS | 16 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/105-debug_line.txt.gz) |
| 106 | usr/bin/llvm-profdata.debug | PASS | 10 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/106-debug_line.txt.gz) |
| 107 | usr/bin/llvm-jitlink.debug | PASS | 12 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/107-debug_line.txt.gz) |
| 108 | usr/bin/llvm-cov.debug | PASS | 42 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/108-debug_line.txt.gz) |
| 109 | usr/bin/clang-include-cleaner.debug | PASS | 36 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/109-debug_line.txt.gz) |
| 110 | usr/bin/lldb-mcp.debug | PASS | 396 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/110-debug_line.txt.gz) |
| 111 | usr/bin/llvm-profgen.debug | PASS | 22 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/111-debug_line.txt.gz) |
| 112 | usr/bin/llvm-reduce.debug | PASS | 114 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/112-debug_line.txt.gz) |
| 113 | usr/bin/llvm-objdump.debug | PASS | 54 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/113-debug_line.txt.gz) |
| 114 | usr/bin/llvm-pdbutil.debug | PASS | 102 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/114-debug_line.txt.gz) |
| 115 | usr/bin/lldb-tblgen.debug | PASS | 468 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/115-debug_line.txt.gz) |
| 116 | usr/bin/clang-doc.debug | PASS | 48 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/116-debug_line.txt.gz) |
| 117 | usr/bin/llvm-readobj.debug | PASS | 44 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/117-debug_line.txt.gz) |
| 118 | usr/bin/lldb-dap.debug | PASS | 690 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/118-debug_line.txt.gz) |
| 119 | usr/bin/clang-tblgen.debug | PASS | 726 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/119-debug_line.txt.gz) |
| 120 | usr/bin/llvm-tblgen.debug | PASS | 1616 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/120-debug_line.txt.gz) |
| 121 | home/owner/share/tmp/sdk_tools/lldb/bin/lldb-server.debug | PASS | 3692 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/121-debug_line.txt.gz) |
| 122 | usr/bin/llvm-ar.debug | PASS | 3522 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/122-debug_line.txt.gz) |
| 123 | usr/bin/clang-tidy.debug | PASS | 2174 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/123-debug_line.txt.gz) |
| 124 | home/owner/share/tmp/sdk_tools/lldb/lib64/liblldb.so.22.1.8.debug | PASS | 15806 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/124-debug_line.txt.gz) |
| 125 | usr/lib64/liblldb.so.22.1.8.debug | PASS | 15806 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/125-debug_line.txt.gz) |
| 126 | usr/bin/clangd.debug | PASS | 3038 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/126-debug_line.txt.gz) |
| 127 | usr/lib64/libclang.so.22.1.8.debug | PASS | 9022 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/127-debug_line.txt.gz) |
| 128 | usr/bin/llvm-exegesis.debug | DIFFERENT 4 | 20780 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/128-debug_line.txt.gz) / [info](../../tools/bolt/results/tu-dwarf-20261106/contexts/128-debug_info.txt.gz) |
| 129 | usr/lib64/libclang-cpp.so.22.1.debug | PASS | 16094 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/129-debug_line.txt.gz) |
| 130 | usr/bin/lld.debug | DIFFERENT 4 | 38234 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/130-debug_line.txt.gz) / [info](../../tools/bolt/results/tu-dwarf-20261106/contexts/130-debug_info.txt.gz) |
| 131 | usr/lib64/libLLVM.so.22.1.debug | DIFFERENT 4 | 41430 | [line](../../tools/bolt/results/tu-dwarf-20261106/contexts/131-debug_line.txt.gz) / [info](../../tools/bolt/results/tu-dwarf-20261106/contexts/131-debug_info.txt.gz) |

## 7. 结束记录与结论

```text
ITEM2 已结束 2026-11-06T10:43:48.484380+08:00 status=ok reason=90-SHA-matched-copies-restored;4-tests-pass;no-TU-recompile
ITEM3 已结束 2026-11-06T13:14:16.107261+08:00 status=partial reason=streaming-DWARF-check;see-per-file-results
```

第三项的 status=partial 表示严格文本未达到全部 PASS；132/132 已完整检查，不是漏跑。单文件没有超时、MemoryError 或 OOM。全部成果与历史产物保留。

结论：90 TU 输入恢复完成，现用入口已改接并通过 4 项测试；132 对调试文件的差异已逐项定位，行号程序及要求保持一致的其他节全部相同，但按指定的严格文本规则仍保留 132 个 DIFFERENT。

## 8. 规则更新与复验（2026-11-06；用户裁决已确认）

**用户已确认 comp_dir 等长条件的适用范围，规则现已启用。** 132/132 对 .debug 和 132/132 个 debuglink 按该口径正式记录为 PASS；23 包中 21 包 PASS，源码包和 debugsource 包的既有差异仍 FAIL。新增反例及回归共 9 项通过；本次启用的五个文件与先前复验所用候选文件 SHA 完全相同，因此按用户裁决沿用包级结果，没有重跑构建、90 TU 或 23 包比较。上一轮的暂停及原始证据保留为历史记录。

### 8.1 用户规则与已确认的 comp_dir 裁决

- .debug_line：逐个单元检查。格式和版本前缀相同；目录表和文件表在源码前缀替换后逐字节相同；行号程序逐字节相同；total_length 和 prologue_length 的增量，都必须正好等于“本单元表头里的替换次数 ×（QB 前缀长度 − 本地前缀长度）”。前缀长度差由两边的实际 release 字符串计算，不写死 2。
- .debug_info：先按原有规则替换源码前缀；只有替换后仍有差异的 DW_AT_comp_dir 才适用额外的等长、连续斜杠、POSIX 词法等价检查。其他属性仍严格比较。
- .debug_aranges、节数量/名称/顺序、其余各节逐字节相同；两类之外仍 FAIL。

指定正例 libRemarks.so.22.1.debug 的原文为：

~~~text
local: DW_AT_comp_dir ("/usr/src/debug/llvm-22.1.8-1.x86_64/build")
QB:    DW_AT_comp_dir ("/usr/src/debug/llvm-22.1.8-2.1.x86_64/build")
UTF-8 bytes: local=41, QB=43
~~~

上例仅 release 前缀不同，替换后相同，按本次裁决直接判相同，不要求 41/43 字节等长。libomp.so.debug 同时有这类常规值和 §6 的连续斜杠值，后者适用额外条件。

用户裁决原文（三条）：

> 前缀替换后完全相同的 comp_dir（如 libRemarks 的 41/43 字节），按原有前缀替换规则判相同，不要求原始字节等长。这类长度不同是正常的：debugedit 改写 .debug_str 里的字符串时可以改变长度。
>
> 前缀替换后只差连续斜杠个数的 comp_dir（那 8 个文件的 19 处），才额外要求：原始字节等长，且按 POSIX 词法归一化后相同。这类是内联字符串，debugedit 原地改写时不能改变长度，只能用斜杠补齐，等长正是它的特征。
>
> 前缀替换后还有其他差异的，一律 FAIL。


### 8.2 已启用的实现与证据

证据目录：[dwarf-rule-20261106](../../tools/bolt/results/dwarf-rule-20261106/)。先前候选完整文件仍保存在 proposed/；已恢复到现用入口，逐文件同 SHA 记录在 approved/activation.json；[tracked 代码 diff](../../tools/bolt/results/dwarf-rule-20261106/validator.diff)，新增解析模块全文 new-module.py。未改 LLVM 源码、spec、helper；未重新构建、未重跑 90 TU。

实现细节：

1. 复用 classify_dwarf.py 的 DWARF32/64 line-unit 解析，分别验证版本/格式前缀、完整表头、完整行号程序、两个长度字段与实际前缀增长值。每个单元保留旧/新偏移、长度、替换次数和期望增量。
2. .debug_info 复用 §4 已完成的全量逐行比较。只在当前输入 SHA 与既有 manifest 完全对应，并重新核对原始/归一化 gzip 的 SHA 后使用旧输出；manifest 自身固定 SHA 为 95f3a2094b83a9c8d4a7e311f839d4b54397787ba32b3945855d37bfa3654c47。完整差异上下文也校验 SHA 和差异条数。未知输入通过平台 loader 调用原构建根 llvm-dwarfdump --debug-info，逐行处理；不调用宿主 LLVM。
3. .debug_str 完整字符串池也比较，不能只忽略该节。只接受前缀替换以及被 comp_dir 检查明确证明的那一对字符串。其他节（包括 .debug_aranges）、程序头、节元数据、ALLOC 节、非节非零字节继续严格检查。
4. validation_common.py 和 20261103/validate.py 接入同一 .debug 函数；compare_rules.py 的任意 debuglink 检查先验证配对符号文件，再验证文件名、实际 CRC、剩余 ELF 内容。
5. 包级比较支持只读复用旧提取文件，每个文件仍和 RPM manifest 的 SHA 核对；新结果全部放 W/temp/dwarf-rule-20261106/packages/。单文件 30 分钟，超时 UNKNOWN 并继续；MemoryError 不吞作普通 FAIL。此次无超时、MemoryError 或 OOM。

每个命令串行处于 8 GiB、swap0、400%、nice19、idle I/O 的独立 systemd 用户服务。active-service-resource-limits.json 的运行中核对原文为 memory.max=8589934592，memory.swap.max=0，cpu.max="400000 100000"，nice=19；oom/oom_kill 均为 0。复验服务 llvm-nov06b-053 退出 0，耗时 14min 40.848s。历史 dwarf-check-20261106/ 未删除或修改。

### 8.3 测试（已确认规则）

原有 8 项通过记录保留在 tests.stdout；本次补充反例后，在启用的实际模块上运行 9 项：

~~~text
Ran 9 tests in 2.443s
OK
~~~

test_dwarf_release.py、tests.stdout、tests-observed.json 保存全部正反例：

| 用例 | 结果 |
|---|---|
| 真实 libRemarks.so.22.1.debug | PASS；仅前缀变化，41/43 字节不要求等长 |
| 真实 libomp.so.debug | PASS；剩余斜杠差异满足等长及 POSIX 条件 |
| 行号程序改一个字节 | FAIL: line program bytes |
| prologue_length 增量多 1 / 少 1 | 两者 FAIL |
| comp_dir 非斜杠字符改变 | FAIL: comp_dir non-slash difference |
| comp_dir 长度不同（原测试） | 等长函数断言 FAIL；真实副本还触发 dwarfdump warning，被拒绝 |
| 前缀替换后仅剩斜杠差异，但原始长度 45/46 字节（新增） | FAIL: comp_dir byte length；测试 PASS |
| .debug_aranges 改一个字节 | FAIL: strict section bytes .debug_aranges |
| 实际前缀长度差 3 的合成 line-unit | PASS，证明没有写死长度差 2 |

原文件不改；原反例副本保留在 W/temp/dwarf-rule-20261106/tests/，本次回归使用全新 tests-approved/。新增反例通过实际 info_difference 入口调用 comp_dir，不依赖解析器报错：旧值 /usr/src/debug/llvm-22.1.8-1.x86_64/////build（45 字节），新值 /usr/src/debug/llvm-22.1.8-2.1.x86_64////build（46 字节）；前缀替换后仅斜杠数不同、POSIX 路径相同，但等长断言必须失败。完整测试与原文在 approved/test_dwarf_release.py、approved/tests.stdout、approved/tests-observed.json。没有删除文件。

### 8.4 包级复验结果（按用户确认口径）

完整 23 包重新读取 RPM 清单；132 对 .debug PASS，132 个仅 debuglink CRC 不同的二进制 PASS。对应 131 组唯一 SHA（同一 liblldb 载荷在两个包路径中复用），按文件计 88987 个行号单元；19 处剩余 comp_dir 斜杠差异，涉及 8 文件。输入、证明、旧/新值与规则路径记录在 dwarf-pair-proofs.json.gz、proof-summary.json、qb-rpm-comparison.json.gz。

| 包 | 已确认口径结果 | .debug | debuglink | 其他差异 |
|---|---|---:|---:|---|
| clang / x86_64 | PASS | 0 | 23 | 无 |
| clang-debuginfo / x86_64 | PASS | 23 | 0 | 无 |
| clang-devel / x86_64 | PASS | 0 | 1 | 无 |
| clang-devel-debuginfo / x86_64 | PASS | 1 | 0 | 无 |
| compiler-rt / x86_64 | PASS | 0 | 10 | 无 |
| compiler-rt-debuginfo / x86_64 | PASS | 10 | 0 | 无 |
| libllvm / x86_64 | PASS | 0 | 1 | 无 |
| libllvm-debuginfo / x86_64 | PASS | 1 | 0 | 无 |
| libomp / x86_64 | PASS | 0 | 3 | 无 |
| libomp-debuginfo / x86_64 | PASS | 3 | 0 | 无 |
| libomp-devel / x86_64 | PASS | 0 | 0 | 无 |
| lldb / x86_64 | PASS | 0 | 5 | 无 |
| lldb-debuginfo / x86_64 | PASS | 5 | 0 | 无 |
| lldb-devel / x86_64 | PASS | 0 | 3 | 无 |
| lldb-devel-debuginfo / x86_64 | PASS | 3 | 0 | 无 |
| llvm / src | FAIL | 0 | 0 | 17 个文件权限；其中 spec 内容也不同 |
| llvm / x86_64 | PASS | 0 | 82 | 无 |
| llvm-debuginfo / x86_64 | PASS | 82 | 0 | 无 |
| llvm-debugsource / x86_64 | FAIL | 0 | 0 | 新增/移除各 12142 个 release 路径 |
| llvm-devel / x86_64 | PASS | 0 | 4 | 无 |
| llvm-devel-debuginfo / x86_64 | PASS | 4 | 0 | 无 |
| llvm-static-devel / x86_64 | PASS | 0 | 0 | 无 |
| python-clang / x86_64 | PASS | 0 | 0 | 无 |

剩余 FAIL 不放宽：

- llvm.src：17 个载荷文件全部为本地 0664、QB 0644（其他类型/属主字段见 source-rpm-differences.json）。其中 16 个文件 SHA 相同；llvm.spec 内容另有三类差异：VCS 的本地路径对平台仓库路径、Release 1 对 2.1、八处 %patch -P N 对 %patchN。完整 diff 为 source-spec.diff。没有据此修改规则。
- llvm-debugsource.x86_64：release 前缀使路径新增/移除各 12142 项。额外只读归因表明一一替换 release 路径并去除载荷 mtime 后，内容和其余元数据全部相同（debugsource-attribution.json）；这是归因证据，不是放行规则，包结论仍 FAIL。

比较器原始结束行：

~~~text
ITEM2 已结束 2026-11-06T15:39:34.677607+08:00 status=differences reason=comparison-complete
~~~

### 8.5 发布状态

上一轮曾暂停规则发布，四个 tracked 入口恢复原状，以下停止行保留为历史记录。本次用户裁决后，已启用原候选五个文件，并逐个确认 SHA 与完成包级复验的版本一致；两个入口共用同一规则。结果核对及裁决原文见 approved/decision-and-result.json。

~~~text
ITEM2 已结束 2026-11-06T15:47:26.559813+08:00 status=stopped reason=comp_dir-raw-length-rule-conflict-awaiting-user
~~~

本次结束行：

~~~text
ITEM2 已结束 2026-11-06T16:03:11.571544+08:00 status=ok reason=approved-comp-dir-rule-enabled;debug-132-of-132;debuglink-132-of-132;two-existing-package-failures-retained
~~~

结论：规则已按用户裁决启用；132/132 对调试文件、132/132 个 debuglink 检查 PASS，21/23 包 PASS。剩余源码包与 debugsource 包保持 FAIL，不放宽规则。
