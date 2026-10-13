# 08 双模式小 spec：完全 strip 选择器试验

两模式实际 rpmbuild -bb、完整原平台后处理各一次，最终判据均PASS。第二步30对象资格尚未完成，因此按裁决使用历史BOLT v2（f26b6562…）经同树llvm-strip --strip-all的专用副本；不是声称新cb候选已发货。该副本strip后SHA575fc9db9a18c28ad7d8ae12c999ca52b01bc3662fa13b68cedebe89a0b01965，与R1本轮重写strip后SHA相同。

## 实际环境与方法

R1普通chroot，1000:1000、4GiB/swap0/nice19/ionice3；临时/proc每段finally卸载，三份mountinfo封存，无bind/unshare。sudo保留HOME=/root，所以显式使用原默认RPM宏路径并把最后~/.rpmmacros解析为现存/home/abuild/.rpmmacros；不改HOME或平台宏文件。所加载R1项目为Tizen-Unified-Toolchain，继承Tizen-Base-Toolchain。当前Quickbuild项目仍以用户确认的Tizen-Base-Toolchain为准；本试验只认证R1当前宏。

全部TOPDIR、BUILD、BUILDROOTS、SOURCES、TMPDIR、RPM数据库均在新BOLT目录；未使用原RPM数据库。已有Root构建文件只读。最小spec %install仅安装fully stripped clang-22及带调试信息普通ELF控制；debug展开%debug_package，release定义debug_package nil；set-x保留完整平台链，额外strace只记录execve。strace及依赖只复制到新工作目录，不安装包/不改Root工具。

## 判据与执行证据

| 模式 | clang选择器 | 控制程序 | RPM clang SHA | 微型对象 |
| --- | --- | --- | --- | --- |
| debug | FD没有向clang调用eu-strip/strip；brp-strip按原debug条件不调用 | find-debuginfo调用/usr/bin/eu-strip --remove-comment -f .../bolt-control.debug .../bolt-control | 575fc9db… | 三目标全部完整字节一致 |
| release | GNU brp-strip执行但未选择clang；FD按原release条件不调用 | /bin/strip -g .../bolt-control | 575fc9db… | 三目标全部完整字节一致 |

普通控制程序先经GCC -g/-O0/--build-id构造，该小链接另持共享锁按16GiB/nice15运行；未构建LLVM。debug提取后的control无.debug_*，但有正常.gnu_debuglink；release的control被GNU strip -g去debug。两模式RPM解包后clang完整SHA均等于strip后候选，版本存活与armv7l/aarch64/x86_64微型门禁均PASS，file原文：

```
/home/abuild/bolt-work/bolt-v4-20261014/clang.smoke-fallback.candidate: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, stripped
```

完整execve正负证据、两spec和dual-mode-smoke.json已公开tools/bolt/results。debug小包还产出debuginfo和空debugsource包（平台允许，日志warning Empty %files），不将此当完整LLVM debugsource清单证明。主包RPM SHA分别为debug ec4a6bb3a694ada9395ab2f318b7808fc239a76b5cd54609f5f05e719789f236，release 61ae8813cfbe8be5a8569c3118b462b3fc06af8b72f8e7db3b8ceb2fa35f0311.

## 测量脚本错误、资源与证据边界

首版测量把.gnu_debuglink也计作“仍有调试信息”，在debug RPM已成功、clang SHA/三目标/execve均通过后错误断言。已改为实际.debug_*/.zdebug_*/.gdb_index，复核**同一debug RPM**，没有重新跑debug完整post。恢复脚本第一次因误重建已有strip输出被helper“output must be new”拒绝，尚未创建release RPM；随后验证已有身份链并复用候选，正常构建release一次。两个失败scope/日志保留，不把第一次写成通过。

Debug实际构建所在scope110.430s、峰1.577GiB（包含最后错误测量）；无release构建的保护失败scope11.548s、峰0.426GiB；release成功scope30.601s、峰1.666GiB。逐进程VmHWM完整数据在JSON，皆未触发OOM/低内存，scope与proc均回收。

真实草案在原Root项目宏下debug/release rpmspec --parse均PASS（18155/18642B），这是解析检查，不冒充完整LLVM spec安装执行。小spec没有执行生产helper的最终安装tail，也未验证同树新工具/完整RPM所有其他payload。

发布分支进入Tizen-Base前仍需要对应真实宏、完整不开/开BOLT构建、最终SHA/90对象/alias/仅(a)的逐字节清单、子包/SDK/CMake消费者和资源认证；设计01附录列明。原始E=/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261014，fallback-identity、两rpmbuild/xtrace、execve、RPM、解包/tiny与scope/mountinfo均在E或R1新工作目录。
