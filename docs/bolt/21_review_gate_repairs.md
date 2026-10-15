# 21 续跑九：外部评审门禁修复

## 人工裁决与边界

Quickbuild 旧 tool-plan 会误拒绝 BOLT 静态库；用户取消该轮。本轮不推任何 Gerrit 分支，只更新 GitHub bolt-v4。候选生成命令及参数不改，历史后备候选 SHA256 4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9 必须保持。新源提交以 a1410e3d 为父，周五再整理。

Quickbuild 参数及项目配置不可改，x86_64 保持 `%bcond_without clang_bolt` 默认开启；本地 `--without clang_bolt` 用于零影响核对。Quickbuild 回退须提交 spec 新提交，将 x86_64 改为 `%bcond_with clang_bolt`，正式提交说明必须包含该方式。

沿用锁/资源/磁盘/保护规则；不在原树运行 cmake/ninja/-P，不进行新配置，不进入 ARM 树。查找先 rg/find；产品准备错误每类只准修正一次；产品门禁失败立即停止。

## 第一步 tool-plan

保存的配置快照离线递归遍历 llvm-bolt 全部显式、隐式与 order-only 依赖，展开 rule/edge 的 description 变量，没有运行 Ninja。闭包 1911 条边：普通 1792（含有 command 的 1715）；新增 BOLT phony 9；新增实际任务 110。普通边在 Quickbuild 应已最新，出现在 dry-run 一律拒绝。

描述全集：102 个 `Building CXX object tools/bolt/...`；7 个 `Linking CXX static library lib64/libLLVMBOLT{Core,Passes,Profile,Rewrite,RuntimeLibs,TargetX86,Utils}.a`；1 个 `Linking CXX executable bin/llvm-bolt`。逐条原文与边见 review-tool-descriptions.json 和 review-closure.json.xz。

helper 用全集的精确字符串白名单。每行必须完整匹配 `[f/t] 描述`，计数有效，不允许噪声、未知 Generating/Creating、普通任务或伪造包含 bin/llvm-bolt 的字符串；计划非空且包含最终链接。返回对象/静态库/可执行文件真实计数。spec 固定 `LC_ALL=C NINJA_STATUS='[%%f/%%t] ' ninja -n llvm-bolt`。

夹具 109/109 PASS（原103+新增6个测试方法，全集110项逐条subTest）；包含全部负例。根因由旧 helper 对静态库的拒绝及新全集夹具确认。

准备记录：执行编辑脚本时 cwd 指向 tools/bolt，误用了相对的 E 路径；改成已定位的绝对路径一次。该次未编辑 helper，随后新回归夹具对旧 helper 报错；修正入口后109项通过。属本轮一次命令工作目录准备修正，不隐藏失败记录。

后续步骤尚待，源提交与文本补丁暂不生成最终版。
