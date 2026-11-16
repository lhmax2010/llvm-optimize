361624 是独立后续 WIP，不是 H1–H5 修复补丁。以下是待 HQ 自己改接时核对的最小方向，不是可直接应用的补丁：
- 在进入各 add_subdirectory 之前，根据 BOLT_BUILT_STANDALONE 定义链接策略参数；仅 standalone 可移除 DISABLE_LLVM_LINK_LLVM_DYLIB。在每个原调用点保留 in-tree 现有策略。
- runtime 清空 C/CXX flags 同样按 standalone/目标需求隔离，避免隐式改变既有 in-tree 构建。
- build-id、armv7l 的额外 AArch64/X86 目标、DESTDIR/删除 libgomp/libiomp5 链接属于独立 recipe 行为变更，不能当作 H 修复的验证等价项；需单列基线和包内容验收。
- 新子包 spec 的 LLVM_LIBDIR_SUFFIX=64 对 armv7l 的配置应按平台目录宏重新核对；当前未构建，不能断言已经失败。
- X86 helper mirrors 需要与同一版本 upstream 函数逐条比较及 standalone 链接验证；本次只完成源码阅读，不给“链接正确”结论。
- 新 spec 关于 llvm-static-devel “not installed here”的注释与已列的 BuildRequires 相矛盾；应修正文案。
- 新说明标题75列，采用本系列72列规则时需折行/缩短标题；Change-Id、作者以及两条 Signed-off-by 是独立 change 的身份，不能替换 I28171720…。
未应用上述任何方向；本次候选完全不含361624。
