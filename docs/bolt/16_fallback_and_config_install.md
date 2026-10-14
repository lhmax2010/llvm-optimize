# 16 历史工具候选与配置级安装核对

2026-10-14，周三续跑四。第一步重链输入核对PASS，后续门禁按本页逐步记录；本轮不再恢复、配置或在原树运行Ninja。

## 最新人工裁决（覆盖此前相应要求）

1. 上轮恢复方法没有先移开污染cache，以正确环境重跑又触发compiler变化/删cache，不是新的产品缺陷。
2. 两次失败配置已刷新llvm-config.h、Targets.def、config.h等生成头；本周放弃原树恢复/树内工具路线。原树只读供已有重链输入与普通clang/strip/resource使用，禁止任何cmake/ninja（包括-n）；周五后决定恢复或废弃。
3. 本周正式本地候选允许历史llvm-bolt SHA1da7bb735f7bc1afab9a863154260699b0b0f88c6fd05b99231dd21ef653fd5a；树内工具构建与安装清理交Quickbuild验证。匹配、note、strip-all、三目标、身份链、对象、双模式/清单与性能门禁不变。
4. Quickbuild用自己的源码，BOLT前clang不与本地输入逐字相同；周四不核对两边clang SHA相等，改核Quickbuild日志N/M/S/U/Q、R、S/N同量级且5%双门禁PASS，并对Quickbuild clang复核性能。

原RPM环境前导用于所有显式cmake/ninja/链接；逐次记录PATH/which。准备性错误每类一次修正；同类第二次或产品门禁失败停止。16GiB重scope/锁≤60分钟、4GiB轻scope、swap0/内存/磁盘底线、原归档证据/22RPM/ARM保护与Gerrit拒绝原文停沿用。

## 第一步：保留输入，不重放

13重链并LLVM strip-debug的输入仍在 /home/abuild/bolt-work/bolt-v4-20261014-relink-first/relinked-clang-22，226,738,888B，SHA158275040dbaa71999f60a4b62e4dd9a23a58b4d72e7ff85fb3c5f5ebff064e4，与relink-first-relink.json一致。不需要链接输入审计或重放，没有在原树调用cmake/ninja/链接。历史tool完整SHA、profile SHA d9b132f9…与普通clang SHA7df0ff90…均复核PASS。

新E=W/temp/bolt-v4-20261014-fallback；根内新/home/abuild/bolt-work/bolt-v4-20261014-fallback。第一步4GiB轻scope12.049s，不取共享锁；source元数据基线保存，无准备性修正。后续候选与配置级四项结果待登记；尚无推送资格。
