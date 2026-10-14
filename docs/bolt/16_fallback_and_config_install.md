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

## 第二步：正式后备候选PASS

本次重新rpmspec展开debug/release草案，均调用同一Source1201 pipeline，helper镜像SHA与源提交一致；正式OPTIONS为ext-tsp、cdsort、split-functions/all-cold/eh、dyno-stats、thread-count=1、stale-threshold=5，不含infer-stale。历史工具按这些参数完整重写保留输入，匹配 N=23592/M=144032/S=0/U=1/Q=383；R=0.004238545%、S/N=0.000000000%，5%双门禁PASS。

前BOLT标识节与完整ELF审计PASS；strip-all前及后各三目标微型对象字节门禁PASS。BOLT输出SHAf5e665fb2d2b77b512ce71b38d639ebcaa470369153b7a352a8246b13866c83d；最终完全strip候选SHA4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9；输入/profile/tool身份链见fallback-candidate.json，其中identity明确strip前BOLT节存在、前后SHA与strip工具SHA。候选留根内本轮工作目录clang.candidate，历史工具路线不冒充本树新工具。

草案会在rpmbuild stdout打印匹配统计：pipeline返回counts(N/M/S/U/Q/R/S_over_N)，main JSON打印整个result；BOLT原始详细日志存work/rewrite/bolt.log。无需修改草案；周四可从构建日志读JSON数值与双门禁结果（未通过会BOLT_GATE_FAILED且退出）。重阶段scope26.620s、kernel峰4.030GiB、最大采样VmHWM3850992 kB，原RPM入口PATH与which见JSON；共享锁/proc/scope已回收。第三步静态配置/安装核对尚待。
