# 06 完全 strip 双模式草案修订

用户新裁决覆盖此前 debug 专用/双 post 的暂存草案。Quickbuild 当前 Tizen-Base-Toolchain 已由用户确认；发布分支亦须支持。设计修订见01附录，上一轮停止报告05保持历史事实。

## 草案与验证

- 移除 __debug_package 未定义即失败的分支；BOLT 重写后先审 note、再同树 llvm-strip --strip-all，保留前后对象与 SHA 身份链，构建日志输出记录。
- install 放到正常 %install 最末；候选替换保持实体原权限，整组 alias 改相对软链。原 __spec_install_post 完整链只执行一次，末尾 SHA/存活/三目标/alias；没有普通 final 快照与第二遍 post。
- 完整复制 ThinLTO cache；重放仅改 output/depfile/cache 三路径，其余逐字。cache 副本核对计数、大小、mtime、确定性 SHA 抽样；原 cache 任务前后清单/SHA 抽样不变门禁放 finally。
- snapshot 常规文件增加 SHA；本地 package-compare 分 debug/release，只允许 PM 指定 clang/alias、debug 模式已证明的 clang .debug/build-id/独占 source 缺失。证明 JSON 须从普通 DWARF 和全部其他 debug 输入生成审核，策略 helper 不自动替调用者证明 DWARF。新增、非 clang 改动、未证明缺失和发布模式缺失全部失败。

84/84 夹具 PASS（0.446s；4GiB/nice19/ionice3/swap0 scope wall1.543s），新增缓存正负例、逐字三路径、strip SHA/标识正负例、post SHA 正负例、两模式清单正负例，以及完整 pipeline fast-path/已裁决 fallback 夹具。全部为 fixture，不能代表真实完整 LLVM/RPM。

本地源提交 `e5239cd50dce5e16cb43b99395388b6bb60829f1`，父 `cb67996861d070d68fec2b4c623eed7d20ba2e23`，tree `b16f061e63d7d4f8e0a86d0a1e844d167b9680ec`，作者 FatTank <hao.lin@samsung.com>。完整 format-patch 静态 apply 与整树 PASS，公开文本 patch + Source 重建整树也 PASS。未推 Gerrit。完整 patch 超10MB留 E；公开 manifest 给完整身份，不把文本评审 patch 单独 git am 当完整提交。

## 普通包 strip 状态

只读现有历史 R1 RPM，解包到 E/ordinary-rpm，不改原件：

- RPM SHA `f126062d8ef1f2e95e5a3bdfba3ba02470ad1bfac14b15728a8d334997d5f8cc`，任务前后相同。
- clang-22 139,929,464B，SHA `3283505cdfebae8a211b0d5fb7befbe5295812787554eb1199ee52e3cfc4a61c`。
- ELF 节表无 .symtab；file 原文：

```
/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261014/ordinary-rpm/usr/bin/clang-22: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, stripped
```

所以完全 strip 的 BOLT clang 与普通包在有无符号表上相同；这不是 cb 新普通 RPM 的最终清单验证。此读取首次因本任务脚本把 W/temp 写成 W 而报 FileNotFoundError，尚未打开原 RPM；修正路径后20.062s成功，失败日志保留，不冒充第一次通过。

## 证据位置与剩余边界

E=/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261014。fixtures.log、fixtures-final-scope、ordinary-strip.json、ordinary-fixed-scope、draft-freeze.json、0001-clang-bolt-draft.patch 为本轮原始证据。R1真实预演、小 spec、90资产结果后续登记；同树生产工具图、真实完整宏、完整 cb RPM 清单认证仍不能由上述夹具替代。
