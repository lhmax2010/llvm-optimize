# 17 单次普通安装草案与严格文本门禁停止

2026-10-14，周三续跑五。已完成草案编辑、103夹具与新源提交/封套；为完成第一步后续读取审核，提前执行依赖的第二步全量文本比对，结果FAIL。随后停止产品实验，未执行修正草案的两模式rpmspec展开、30/90对象、双模式小spec、RPM/DWARF预期清单、性能或sandbox。不是全部第一步认证PASS。

## 最新人工裁决

追加bolt后的第二次完整安装必然带入7个BOLT静态库、两个未登记manifest的工具别名和改写的LLVMConfig.cmake；prune拒绝未登记别名。采用删除第二次安装，不给prune加特例。普通安装已完成，由原候选install子命令单独替换clang-22；改用更严格的构建根清单不变门禁。前轮原cache新增361文件1674072B由PM接受为交接cache正常变动；以后若临时配置，用专用cache。本轮只读现有快照，不执行新配置；原树禁cmake/ninja（含-n/-P安装）不变。文本分类覆盖所有build/rule及无输入CUSTOM_COMMAND，不用compdb。产品失败即停、每类准备性错误最多一次修正与资源/保护规则沿用。

## 草案修正及夹具

删除ordinary-exports目录/备份/恢复、第二次安装及其写预算、prune调用；原普通CMake安装仍仅一次。保留旧prune函数/CLI供原有历史夹具与审计，生产不调用；不是增加别名特例。新增compare-root子命令：重新取构建根清单，保存install-after-pipeline.json，逐路径检查新增、删除、类型、权限、大小、SHA、软链接目标，以及目录/链接权限与根目录权限；报错指明第一个不同的相对路径。snapshot CLI新增完整权限metadata，原inventory文件形状保持，避免改变旧RPM清单协议。

门禁位于pipeline之后、原普通安装整理之前；候选安装仍在原%install末尾，以避免之后的原ln命令覆盖已规范化别名。该门禁证明BOLT配置/构建/pipeline未改变普通CMake安装；门禁之后原有普通安装整理与末尾candidate install保持原顺序。没有把平台正常整理的变化当BOLT副作用。其余生产重链/重写参数、匹配/note/strip-all/微型/单次原post尾检不变。

103/103夹具PASS：原95不变，新增8（不变通过；新增文件/软链接、删除文件、内容/文件权限/链接目标/目录权限变化均失败，错误包含路径）。Python3.9 parse及helper镜像一致。fixtures净0.581s/轻scope1.527s。当前草案只有静态源码检查确认一个-P安装、无ordinary-exports/prune及有compare-root；**本次debug/release rpmspec展开未执行**，不能拿16的旧草案展开顶替。

新源提交a1410e3d14b8836e3f9be5a1b4380f914dc2e705，父cb67996861d070d68fec2b4c623eed7d20ba2e23，tree33b4e9f84cec3336878501d55fe243b41c092c80；spec SHA14d17a60369a2c05661037583740b410f0fd710aef2c0c78de08175a57bb6c0c，helper SHA7614228b5da020fd1ae08eaef0ebaf096c317f21a370e249285ee632711888e7。完整binary patch留E；公开review.patch+不变profile.xz封套静态apply/整树PASS。新源码尚未具备推sandbox资格。no-reinstall-draft-change.diff给相对d6ddbff5的全部改动；manifest给源码身份与封套哈希。
