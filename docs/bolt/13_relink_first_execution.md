# 13 周三修正顺序：原地重链后匹配

本任务按用户新裁决从12停止点恢复；旧失败记录不改。开工三个关键SHA复核PASS，完整交接沿用。取消无emit-relocs普通clang单独探测，先同树emit-relocs重链→LLVM strip-debug→历史工具完整重写作早期计数（产物用后删）→通过后本树新llvm-bolt→正式重写/strip-all/三目标/SHA链→30/90完整对象→双模式小spec/22RPM DWARF预期清单→30×5性能→满足全部门禁后sandbox直推。

历史工具仅早期资格，正式候选不可复用；两个匹配检查都R≤5%且S/N≤5%，禁infer-stale。配置bolt前后clang唯一链接字串逐字相同，CMake差异仅bolt相关、只构建llvm-bolt、独立DESTDIR差集与exports恢复门禁均保留。性能geom(candidate/ordinary)≥0.98不推；Gerrit拒绝原样停，不拆profile、不换方案。当前重链与早期匹配PASS，第三步CMake配置门禁FAIL并停止；下面给实际结果，不继承R1 PASS。

E=W/temp/bolt-v4-20261014-relink-first；根内新/home/abuild/bolt-work/bolt-v4-20261014-relink-first；共享锁、16GiB/swap0/nice15/ionice3、入口12GiB/运行3GiB、60分钟持锁、>10GiB写入后30GiB磁盘底线均沿用，内存不足按5分钟/最多60分钟复查。只在交接x86树和授权B/E工作，不改归档证据/22RPM，不进入两棵ARM树。

第一步PASS：唯一原链接字串已保存（SHA352a6f57…），只改输出/depfile、保留原cache字串并追加emit-relocs；链接8.840s、LLVM strip-debug5.376s、scope17.571s，kernel峰13.071GiB、最大采样VmHWM10211668kB。去debug输入SHA158275040dbaa71999f60a4b62e4dd9a23a58b4d72e7ff85fb3c5f5ebff064e4，226,738,888B；之前完整ELF3,560,483,168B。普通clang未变，cache仍47107/96877810360B，free60,410,531,840B；锁/proc/scope均回收。早期匹配下一步，不把本重链PASS冒充匹配PASS。

第二步早期匹配PASS：历史SHA1da7bb73…工具以全部正式参数对去debug的重链输入完整重写，N=23592/M=144032/S=0/U=1/Q=383，R=0.004238545%、S/N=0%，整数5%双门禁PASS，禁infer-stale。scope26.075s、kernel峰3.809GiB；早期产物用后已删除（非候选），日志/输出SHA保留；共享锁/proc/scope均回收。只有下一步本树新工具的正式产物可以成为候选。

## 第三步配置门禁失败：STOP_CMAKE_NON_BOLT_CHANGES

一次同树cmake按草案追加bolt、BOLT_BUILD_TOOLS=OFF/runtime OFF/tests OFF/X86，rc0、18.107s；但日志明确自动删cache并二次配置：

```text
You have changed variables that require your cache to be deleted.
Configure will be re-run and you may have to reset some variables.
CMAKE_C_COMPILER= clang
CMAKE_CXX_COMPILER= clang++
```

前后缓存681个键改变，678个不是BOLT键/项目列表；不是允许的bolt相关差异。关键实物变化：

|键|之前|之后|
|---|---|---|
|LLVM_ENABLE_PROJECTS|clang;lldb;clang-tools-extra;lld;compiler-rt;openmp|空|
|LLVM_ENABLE_LTO|Thin|OFF|
|LLVM_TARGETS_TO_BUILD|X86;ARM;AArch64;BPF|all|
|CMAKE_INSTALL_PREFIX|/usr|/usr/local|
|CMAKE_C_COMPILER（含类型）|UNINITIALIZED=clang|STRING=/usr/bin/clang|
|CMAKE_CXX_COMPILER（含类型）|UNINITIALIZED=clang++|STRING=/usr/bin/clang++|

启动器CC/CXX环境均未设置。原cache编译器记录为相对名称/UNINITIALIZED，日志证实编译器变量变化引起自动重配置；更细的触发机制未另行重现实验，不猜测为ambient CC污染。最终build.ninja已没有bin/clang-22链接边，因此配置后逐字一致性不能通过；在cache硬门禁先失败处即停，没有运行后续ninja -t query、dry-run或ninja llvm-bolt，也没有构建新LLVM。完整before/after缓存差异及CMake原输出已公开，before/停止时的cache/ninja/install脚本快照留E。

这是实际配置门禁失败。按规则不修参数重试、不恢复后再配置、不继续任何产品实验；源spec/helper/patch/profile未改，仍d6ddbff5…父cb679968。本树新llvm-bolt未构建、SHA未知，不能用历史早期产物顶替正式候选。第三步独立DESTDIR/install差集未执行。

**树状态：失败的cmake已改写原CMakeCache.txt和build.ninja，尚未恢复。** 停止时cache SHAbd8ad3aacdf9a9f2c4be66a9ea7617cd958343d8c30712ae526d3e687a9877be，ninja SHAa37efa6aeb4872e56f88ac34f7559b7848db971e0d03b08b7e1e43eeda12e361；开工前的原件快照在E/CMakeCache.txt.before及build.ninja.before，其他配置生成文件也已受cmake影响，不能只假定覆盖两文件便完整恢复。后续不可直接ninja续跑，应先按新的恢复安排处理配置。本轮没有擅自恢复或重跑。

## 本次阶段资源与边界

|阶段|worker/命令耗时(s)|scope wall(s)|kernel峰GiB|最大采样VmHWM(kB)|结论|
|---|---:|---:|---:|---:|---|
|重链+strip-debug|link8.840 / strip5.376|17.571|13.071|10211668|PASS|
|历史工具早期完整重写|见JSON|26.075|3.809|3868076|R/SN PASS，输出已删除|
|同树BOLT配置|18.107|19.065|0.677|328736|rc0但cache门禁FAIL；不构建|

上述各段16GiB/swap0/nice15/ionice3、入口≥12GiB/运行≥3GiB，共享锁持17.628/26.107/19.100s均释放；proc与scope全部回收。kernel峰含文件页缓存，VmHWM为0.5秒采样逐进程峰，不混用。新树重链peak13.071GiB已超过旧R1估6.04GiB，不能沿用旧估作为新树实测；温cache链接8.840s也不是Quickbuild或安静环境编译性能数据。未出现OOM、内存准入等待或磁盘底线不足。

重链前16GiB写入预算预检free60,637,306,880B、预算后43,457,437,696B≥30GiB；去debug产物SHA158275040dbaa71999f60a4b62e4dd9a23a58b4d72e7ff85fb3c5f5ebff064e4，226,738,888B。早期工具输入就是它，profile/工具SHA核验、正式参数完整重写后N23592/M144032/S0/U1/Q383，R=0.004238545%、S/N0%，实际PASS；其产物06d644a0…用后删除，日志保留。正式新工具的匹配度NOT RUN。

停止后的轻审计PASS：22普通RPM再次完整SHA/大小一致，普通clang仍7df0ff90…、生产Source/spec/ar/lld等原件SHA相同，review49-independent-install元数据一致。原cache仍47107文件/96877810360B，name/size规模未变，部分mtime受原地LLD访问而变（完整manifest不等于交接时；这是用户明确允许的cache写入，不误报不变）。未手工复制、删除或prune原cache；仅按裁决删除早期专用重写产物。未进入两棵/var/tmp ARM树，W tracked既有gbs改动保留、不写W/llvm。

## 后续未执行与推送

正式重写/strip-all/三目标/SHA链、30历史+90资产完整对象、双模式小spec/22RPM逐项DWARF预期差异、30文件各5次性能复核全部NOT RUN；没有正式候选，没有性能几何均值或<0.98结论，不声称历史结果等于本次通过。sandbox推送NOT ATTEMPTED，未核对Gerrit推前/推后指向，未推refs/for/tizen_base；现有本地源草案d6ddbff5…不是经全部门禁审核的交付提交。

如果tizen_base之后合入归档补丁，周五定稿需在新tizen_base变基并处理llvm.spec冲突；本轮未做。唯一重链和早期匹配分别已提交2bc142d/59899b7到GitHub bolt-v4。本次STOP来自用户的真实cache/配置保持门禁，不是审批、外部评审或资源豁免。

材料归档中一次git提交命令误用W cwd，pathspec未找到，未暂存/修改W文件，随后在B完成59899b7提交；未因此重跑任何实验。大ELF/cache/配置快照留E，公开relink-first各JSON、early-bolt.txt、configure.txt与cache.diff；完整raw分支与钉提交链接见10。
