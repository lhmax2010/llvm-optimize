# 49 续三：调试无关性最终判据与后续执行

日期：2026-10-13；开场 Git `c38bc2ae25bc9ab530f80965479b1fb7f5757e44`。**进行中：比较器41测试PASS，实物尚未重判。** 本页承接[docs/49 §0–§19](49_round4_revision_and_x86_build.md)，旧停止记录原样保留；因主文接近50KB，§20起完整记录单列本文件，每个大步骤同时更新主文状态与STATUS。

宿主恢复命令：`sudo sysctl -w vm.mmap_min_addr=65536`，重启也会恢复。本任务不修改宿主配置；/proc只临时挂载并回收。不开Gerrit，不访问BOLT工作树/分支/证据，不清理磁盘，不改两份Source或Commands。

## 20. 完整性、用户裁决与执行边界

证据目录 H=`temp/release-contract-final-20261013`。`initial-integrity.json`核对当前两份Source、候选补丁、原LLVM spec与用户配置摘要PASS；工作树只存在用户的`gbs_llvm.conf`修改。两把项目锁由`hold_lock.py`持有。重阶段共用`/home/linhao/Toolchain/development/heavy-stage.lock`，flock排队最长2h；轻/重阶段准入6/10GiB，18GiB cap、swap0、nice15/ionice3、30s采样与宿主可用2GiB保护沿用docs/49 §1（H/initial-integrity.json、lock-acquired.json、run_stage.py）。

用户最新确认：Quickbuild当前在Tizen-Base-Toolchain构建LLVM，定义`_toolchain`，走debug分支；未来进入Tizen-Base时未定义该宏，走发布分支。本次认证因此是未来实际交付前提。发布模式完整构建仍挂账，优先级提高，待PM安排；不能以调试无关性夹具代替发布完整构建（本轮用户裁决）。

### 20.1 事前冻结的最终十项规则

1. ELF class、字节序、machine、e_flags相同。
2. SHF_ALLOC身份为节名、类型、COMDAT签名及SHF_LINK_ORDER目标的递归身份。按身份多重集合比较，逐身份比较flags/size/alignment/entsize/内容，NOBITS只比大小。
3. `.init_array/.fini_array/.preinit_array/.ctors/.dtors`及其点后缀、合法C标识符节名，分别按节名保持身份序列。
4. 同身份重复节保持内部顺序与内容。
5. 每一目标节内部重定位顺序相同，跨目标节/重定位节文件顺序不比较。比较offset/type/addend/规范符号身份；SECTION用节身份，LOCAL用名+所在节身份+值，其余用符号名。REL隐式addend由目标节原始字节相同比较覆盖，RELA显式比较。
6. 符号作为多重集合，比较全部非LOCAL及有名非`.L` LOCAL；排除SECTION/FILE、无名LOCAL、`.L` LOCAL、定义在.debug*的LOCAL以及仅由debug重定位引用的未定义符号。不豁免可加载节中的映射符号。
7. COMDAT组按签名/flags/有序成员身份多重集合，去掉debug及其重定位成员。
8. `.llvm_addrsig`的ULEB128索引解析成规范符号身份集合，排除第6项debug专用符号。
9. 发布产物无.debug*节。
10. 文件节顺序有变化时，用同一llvm-dis记录两路bitcode去调试信息后的函数/全局定义顺序；只诊断，不作门禁。直接非LTO对比也只诊断。

实现：`tools/check_release_debug_independence.py`。本轮没有另外增加豁免（用户本轮裁决；实现与测试）。

## 21. 比较器与夹具

原25项全部保留，新增16项，**41/41 PASS**；执行0.085s，scope peak 24,391,680 B，exit0（H/comparison-tests-scope/build.log、memory-summary.json）。本步骤无失败、未使用辅助缺陷重跑条款。

|新增固定ELF夹具|预期与实测|
|---|---|
|COMDAT节换序|PASS|
|普通非组节换序|PASS|
|同名.init_array两节换序|FAIL，被拒绝|
|同名C标识符节换序|FAIL，被拒绝|
|同身份重复节换序|FAIL，被拒绝|
|跨目标节重定位换序|PASS|
|同目标节内重定位换序|FAIL，被拒绝|
|SHF_LINK_ORDER目标不同|FAIL，被拒绝|
|e_flags不同|FAIL，被拒绝|
|debug内增加LOCAL映射符号|PASS|
|ALLOC中映射符号变化|FAIL，被拒绝|
|仅debug引用的未定义符号增加（含addrsig引用）|PASS|
|ALLOC引用的未定义符号变化|FAIL，被拒绝|
|addrsig集合变化|FAIL，被拒绝|
|addrsig仅索引/记录顺序变化|PASS|
|额外：LOCAL重定位目标值变化|FAIL，被拒绝|

旧夹具变化逐项：`test_alloc_order`由普通节反序FAIL改为PASS，落实第2项；`test_section_relocation_target_canonical_name`的预期由节名改为SECTION+完整身份，落实第5项；`test_comdat_debug_only_member_difference_passes`预期成员由节名改为完整身份，落实第7项。其余原测试语义保留；测试入口移到新增类之后保证命令行执行覆盖所有41项（H/tests-before.py与当前测试diff，H/comparison-tests-scope/build.log）。

## 22. 后续执行

40对SHA核对与重判、AArch6420对、两次x86全量回归、补丁再生成、完整构建及验收、BOLT交接、两ARM全量/根内限制、bash清单/LLVM23探测：尚未执行。后续依此顺序；产品门禁任一失败即停止，不改判据重试。
