# 14 CMake 原因诊断与临时布局错误停止

2026-10-14。当前 **STOP_TEMPORARY_SOURCE_LAYOUT_ERROR**，停止在第二步原始临时配置入口；追加bolt、树恢复、候选/验证/性能/推送全部未执行。按用户“规定之外停止”没有补布局重试。归档证据与22RPM未动，失败的原树cache/ninja保持本次开工状态，尚未恢复。

## 人工裁决与任务范围

沿用早期匹配PASS N23592/S0/U1，不改5%双门禁。此次先只读比较原始RPM命令、失败实际命令/环境、spec两模式展开；若草案缺陷则修正并临时验证，若无缺陷只验证。再按original-rpm-build.sh同前导恢复一次，干跑扣除已证明8配置触碰和LLDB头暂存后编译/链接≤50才串行补完；>50不补，允许历史SHA1da7bb73…后备候选，但第二步spec门禁、候选与对象/性能门禁仍需通过。性能geom≥0.98不推，修正源码父cb679968直推sandbox、不推refs/for/tizen_base，Gerrit拒绝原样停、不拆profile。

本次只做轻4GiB/swap0/nice19/ionice3，未取共享锁。原始归档脚本/环境只读，全部新文件在B、E=W/temp/bolt-v4-20261014-cmake-recovery、Root新/home/abuild/bolt-work/bolt-v4-20261014-cmake-recovery，不进入两棵ARM树。

## 第一步：删缓存提示、三组命令与环境

原日志明确：

```text
You have changed variables that require your cache to be deleted.
Configure will be re-run and you may have to reset some variables.
The following variables have changed:
CMAKE_C_COMPILER= clang
CMAKE_CXX_COMPILER= clang++
```

原脚本取自归档续十E10= W/temp/release-x86-full-build-20261013/round2-resume-serial/original-rpm-build.sh；源文件只读未改，完整环境前导及cmake字串在cmake-recovery-diagnosis.json。此前原cache两个compiler字段为UNINITIALIZED相对clang/clang++；原clang规则调用/bin/clang++，失败后解析成/usr/bin/clang++。

|组|cmake参数|环境证据|
|---|---|---|
|(a)原%build|完整-G Ninja、TIZEN、显式clang/clang++、flags、ThinLTO/MLGO/targets/projects等，末尾../llvm|原original-rpm-build.sh RPM前导、已存login-environment.txt|
|(b)失败实际|cmake -S ../llvm -B .，仅追加projects及四BOLT参数|chroot --userspec直接入口，未加载原RPM前导；采集PATH/CC/CXX/CFLAGS/CXXFLAGS/LDFLAGS|
|(c)旧草案|debug与release rpmspec展开后的追加配置都与(b)参数一致|真实RPM阶段继承RPM登录环境，不能拿(b)入口环境冒充它|

关键只读发现：原归档登录PATH为/usr/local/bin:/bin:/usr/bin:/usr/local/sbin；直接userspec入口PATH为/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin。前者先/bin，后者先/usr/bin。两个位置的clang/clang++分别指向同一常规文件inode6308748，工具字节并未换，路径拼写却不同。Root现存CMakeDetermineCompiler.cmake第115–148行对非绝对预设compiler用find_program定位；相对compiler记录与不同PATH组合解释了被记录的编译器变化及删cache，而不是profile错误。

**二选一判断选“本地测试命令/环境与spec正常RPM环境不一致”。** 参数字串本身相同，差异在没有复用原RPM登录PATH与完整前导。最初仅看追加命令缺参数就判spec缺陷，依据不足；取得PATH证据后已撤回，没有据此修改生产spec。这个判断不等于第二步正式临时门禁PASS；spec在原环境下能否无删cache/仅bolt差异/链接逐字相同，仍须成功的临时实验证明，不能把推理当Quickbuild认证。

## 第二步：原始临时配置准备缺陷，未执行追加bolt

为保持../llvm参数，新临时父目录只放llvm与mlgo_verify_assets的只读源链接；遗漏LLVM依赖的同级cmake及其他项目布局。CMake对路径进行处理后查找temp-debug/cmake/Modules，不能找到原源文件。唯一一次baseline-debug.sh执行退出1，原文：

```text
CMake Error at CMakeLists.txt:7 (include):
  include could not find requested file:
    .../temp-debug/llvm/../cmake/Modules/CMakePolicy.cmake
CMake Error at CMakeLists.txt:19 (include):
  include could not find requested file:
    .../temp-debug/llvm/../cmake/Modules/LLVMVersion.cmake
CMake Error at CMakeLists.txt:46 (project):
  VERSION ".." format invalid.
```

这是本任务准备的临时源布局错误，不是原始recipe/CMake删cache的新失败，也不是spec追加bolt验证结果；失败发生于原始配置，尚未执行追加命令、缓存前后门禁或clang边比较。debug/release宏展开均已成功保存，但release临时配置没有启动。依据停止规则不补symlink、不换源路径重试、不修草案或尝试恢复原树。临时目录生成的失败cache/文件清单已复制到E，然后仅删除自己创建的temp-debug；不跟随源symlink，原源码不动。其他本会话日志与证据保留。

原RPM脚本包含MAKEFLAGS+=写法；测试副本仅将它改为POSIX等价export MAKEFLAGS="${MAKEFLAGS} -k"，环境值及cmake参数不变，原脚本未改。原登录PATH/LC_ALL先显式复用；正常RPM前导及optflags变换保持。没有用bash执行或改HOME。

## 资源、审计与完成边界

诊断scope1.024s、临时验证scope1.029s，均轻cap4GiB；精确peak、VmHWM、入口与退出在cmake-recovery-stop.json。两个proc挂载均finally卸载、scope均回收，未取共享锁。停止后只审计/归档，不跑产品实验。

首版停止审计误把可变.ninja_log与重链前的交接基线比，得到不符；已纠正审计基线范围，只重做必要的保护审计和临时目录清理，不是产品配置重试。两个审计日志保留。正确审计PASS：22RPM完整SHA/大小、普通clang7df0ff90…、源spec/Source/ar/lld等原件SHA、review49-independent-install元数据与原保护记录一致。原树cache仍bd8ad3aa…、ninja仍a37efa6a…，与上轮STOP时相同；本轮未继续改它们，仍未恢复。

|请求项|当前结果|
|---|---|
|原因/两宏展开对照|只读完成；本地PATH/前导差异，原compiler变化提示已定位|
|spec修改与夹具/本地源提交/patch/manifest|未改；源仍d6ddbff5…父cb679968；没有新增或重跑fixtures，不把旧95 PASS当本次PASS|
|临时两次配置/删cache/差异/链接门禁|未完成：baseline准备错误，append未运行；临时目录已删除|
|原树改写清单/恢复/≤50干跑分类|未执行，树保持上轮失败配置；旧快照继续保留|
|同树或历史后备候选及门禁|未执行；后备不能替代第二步未完成门禁|
|30+90完整对象/双模式小spec/DWARF预期差异|未执行，无本次结果|
|30文件各5次性能/几何均值|未执行，不判断≥0.98或加速|
|sandbox推送|NOT ATTEMPTED；未核对远端前后，不推refs/for/tizen_base|

本任务未完成授权目标，当前STOP由临时布局准备错误触发；根源判断与spec认证证据强度已分开。未来Quickbuild SHA与本地后备候选相同的交叉核对条件目前不适用，因为没有生成候选。若tizen_base合归档补丁，周五变基解spec冲突仍挂账，本轮未做。公开本页、diagnosis/stop JSON、baseline-debug.txt；失败临时cache与原RPM脚本/两模式完整展开、完整scope日志留E。全部raw分支/钉提交索引10在收尾更新。
