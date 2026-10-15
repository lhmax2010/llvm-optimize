# 24 续跑十四：第三轮修复与新基线重新认证

## 人工裁决与边界

保持候选 4ec07159 与生成参数/profile 不变；原树禁止 cmake/ninja/-P，保护归档证据及普通 RPM。本轮只在全部门禁通过后推新 sandbox/lhmax2025/bolt_pgo_v2；QB 与真实树演练由用户在 PM 审核后启动。作者、提交者和 Signed-off-by 均为 Hao Lin <hao.lin@samsung.com>，不改全局配置。

|项目|状态|
|---|---|
|第一步 helper/spec 修复|PASS，源提交 91f2ab3618900bb828a228c274d19004681e6d4d|
|保留214项、新增38项|252/252 PASS|
|真实 link.original 更严格检查|PASS，未重链|
|真实 ELF 新增 shndx/RPATH/RUNPATH 检查|PASS，RPATH 均无，RUNPATH 均为 $ORIGIN/../lib64:|
|严格 CLI 离线闭包|PASS，1911边/1791普通/9新phony/111任务，分类变化0|
|变基、重新认证、文档、sandbox|NOT RUN，后续步骤|

## 准备性修正与断言调整

查找 AGENTS 时一次搜索范围过大，遇到其他目录权限拒绝；未读写其产品文件，随后改为逐级明确路径。既有文件均先用 rg 定位。
首轮测试中旧小写入正例仅留0字节、旧 warning 拒绝断言未同步；作为同类夹具语义准备错误修正一次，保留首轮输出。10GiB 正例改为11GiB可用空间；warning 负例改为 error。其他断言调整：两处重生成错误改英文；原真实构建正例和 TF SHA 负例追加成功标记。原测试方法均保留。没有候选产品门禁失败或参数豁免。

保存静态 Ninja 图认证不加载 .ninja_deps/depfile，不做完整 dirty 判定；未知真实任务仍失败关闭。测试 stdout 为空，stderr 含逐项原文。
