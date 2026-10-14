# 13 周三修正顺序：原地重链后匹配

本任务按用户新裁决从12停止点恢复；旧失败记录不改。开工三个关键SHA复核PASS，完整交接沿用。取消无emit-relocs普通clang单独探测，先同树emit-relocs重链→LLVM strip-debug→历史工具完整重写作早期计数（产物用后删）→通过后本树新llvm-bolt→正式重写/strip-all/三目标/SHA链→30/90完整对象→双模式小spec/22RPM DWARF预期清单→30×5性能→满足全部门禁后sandbox直推。

历史工具仅早期资格，正式候选不可复用；两个匹配检查都R≤5%且S/N≤5%，禁infer-stale。配置bolt前后clang唯一链接字串逐字相同，CMake差异仅bolt相关、只构建llvm-bolt、独立DESTDIR差集与exports恢复门禁均保留。性能geom(candidate/ordinary)≥0.98不推；Gerrit拒绝原样停，不拆profile、不换方案。当前原地重链执行中，本页后续填实际结果，不继承R1 PASS。

E=W/temp/bolt-v4-20261014-relink-first；根内新/home/abuild/bolt-work/bolt-v4-20261014-relink-first；共享锁、16GiB/swap0/nice15/ionice3、入口12GiB/运行3GiB、60分钟持锁、>10GiB写入后30GiB磁盘底线均沿用，内存不足按5分钟/最多60分钟复查。只在交接x86树和授权B/E工作，不改归档证据/22RPM，不进入两棵ARM树。

第一步PASS：唯一原链接字串已保存（SHA352a6f57…），只改输出/depfile、保留原cache字串并追加emit-relocs；链接8.840s、LLVM strip-debug5.376s、scope17.571s，kernel峰13.071GiB、最大采样VmHWM10211668kB。去debug输入SHA158275040dbaa71999f60a4b62e4dd9a23a58b4d72e7ff85fb3c5f5ebff064e4，226,738,888B；之前完整ELF3,560,483,168B。普通clang未变，cache仍47107/96877810360B，free60,410,531,840B；锁/proc/scope均回收。早期匹配下一步，不把本重链PASS冒充匹配PASS。
