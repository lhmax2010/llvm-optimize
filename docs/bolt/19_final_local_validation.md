# 19 周三续跑七：完成文本门禁与候选验证执行记录

## 人工裁决与文本门禁

PM将乙类扩展为CMake重跑簿记语句对：RERUN_CMAKE依赖列表，以及无输入/隐式或order-only依赖/变量绑定的多输出phony兜底；后者输出增删集合必须与前者依赖增删完全相同。第7438块逐项PASS：before/after均只有一行，冒号右侧仅phony，无任何依赖或变量；输出删除88、增加20，与RERUN_CMAKE精确集合相等。原文、所有输出、增删和SHA见finish-text-gate.json。18的甲类证明沿用且字节SHA绑定：7421块、6838普通语句、两个PDB变量、2454规则中0引用。

PM归因：删除88项是首次配置的编译器检测/ABI/try_compile模块或源；缓存重配不再读取。新增20项为BOLT配置文件，说明首次/缓存重配区别而非普通构建变化。按PM取消对照，不执行新的CMake配置；不是声称做过对照实证。原树所有cmake/ninja/-P禁用继续有效。Quickbuild现场tool-plan仍最终把关。

|最终类别|块数|判定|
|---|---:|---|
|BOLT构建边|9|PASS|
|BOLT规则|1|PASS|
|聚合新增BOLT依赖|5|PASS|
|BOLT/聚合混合|1|PASS|
|甲：未引用变量|7421|PASS|
|乙：RERUN_CMAKE依赖|1|PASS|
|乙：配对phony输出|1|PASS|
|合计|7439|全部PASS|

源a1410e3d14b8836e3f9be5a1b4380f914dc2e705父cb67996861d070d68fec2b4c623eed7d20ba2e23，草案不改。后续步骤逐项更新，不将文本PASS代替对象/双模式/RPM/DWARF/性能资格。候选历史工具后备SHA4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9。

## 两模式展开 PASS

当前a1410e3d spec在debug（_toolchain=clang）与release（取消_toolchain）宏下rpmspec展开PASS，BOLT段逐字节相同/SHA 298c888296a30801ca79590543110014ae753a8a391065283711a8547a0b8dd9；两边均只有1次普通-P安装，无ordinary-exports/prune；pipeline < compare-root < candidate install次序PASS。完整展开和参数/env记录见finish-expansion及finish-*-expanded.spec。PATH均/usr/local/bin:/bin:/usr/bin:/usr/local/sbin，which clang=/bin/clang、clang++=/bin/clang++。未运行cmake/ninja，轻4GiB scope/proc已回收。一次准备性路径修正：支持脚本record_call.py位于先前根内专用工作目录，错误宿主temp查询后定位原保存文件，不涉及产品门禁。对象/后处理/包清单/性能尚待。

## 输入准备与第二次路径错误STOP

实际收尾时间：2026-10-15T00:12:31.578639+08:00。任务名称仍为周三续跑七。

30历史输入与90资产共120份保存.ii SHA逐份PASS，已复制到本会话专用目录，共901,204,757B；候选与普通compiler SHA也相符。计划使用同一实体路径compiler/clang-22依次替换普通/候选，再比较完整.o，不移除.GCC.command.line；但本轮尚未开始任何对象编译，不能将准备PASS写成对象PASS。prepare-objects为4GiB轻scope，无锁、无chroot；大输入与参数清单留E和根内本会话专用工作目录。

停止原因属于准备性错误而非产品门禁FAIL：先在宿主temp查询record_call.py路径错误，已用根内原保存位置修正一次、展开PASS。后来只读查阅assets90-stage.py时又猜错保存文件名，第二次同类“已保存辅助脚本路径”错误；按PM同类第二次错误即停，不再修正、不继续产品实验。原文两路径及处理见finish-stop.json。未把第二次只读错误隐去或改记其他类别。本任务动用1次修正，发生同类2次错误。

30/90对象 NOT RUN（compiled=0）；双模式小spec NOT RUN；22RPM/DWARF实际预期差异清单 NOT RUN；30×5性能 NOT RUN，几何平均未知；sandbox NOT ATTEMPTED/远端未查。准许差异政策仍为clang实体/别名规范化，以及有普通DWARF逐项证据的debug专属缺失；无新增BOLT产物许可。本次未据22RPM生成并认证具体预期清单。没有本轮编译/链接/cmake/ninja/重阶段/共享锁。

展开原文保留rpmspec生成的末尾空行，git diff --check曾提示两个新展开文件EOF空行；未修改展开原文或草案以消除此格式提示，不将它声称为PASS。产品展开四项条件全部PASS。

## 保护审计与资源

22普通RPM及普通clang等完整SHA/大小、归档证据元数据、原源码元数据PASS；原树坏CMakeCache/build.ninja指纹保持，未配置或恢复。原ThinLTO缓存47,987文件/96,881,772,832B，零新增/本轮未写；源a1410e3d工作树干净，spec/helper SHA不变；候选SHA4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9保持历史工具后备路线。只有展开轻任务临时proc mount，finally卸载，前/中/后mountinfo留E；结束无proc挂载。没有绑定/namespace或ARM根访问，没有改W tracked/llvm。

|轻阶段|scope秒|cgroup峰GiB|最大采样VmHWM kB|
|---|---:|---:|---:|
| text-gate | 2.028 | 0.057 | 44044 |
| expansion | 1.524 | 0.039 | 17844 |
| prepare-objects | 27.283 | 1.763 | 23612 |
| final-audit | 363.245 | 1.434 | 178104 |

均4GiB/swap0/nice19/ionice3，scope全部回收；无单次>10GiB写入，原根free58027347968B。文本bd3c3c5、展开9c173d0已分步推GitHub bolt-v4；停止材料与raw索引收尾继续推送。完整原始E= W/temp/bolt-v4-20261014-finish。

## 周四六项实物核对

Quickbuild匹配统计同量级且R、S/N双5% PASS；现场tool-plan PASS；compare-root PASS；Quickbuild clang性能复核；debugsource包清单与上一快照对照；不比较本地/Quickbuild clang SHA。原树继续禁CMake/Ninja/-P。当前sandbox前提未满足，Gerrit评审及tizen_base均未推送。
