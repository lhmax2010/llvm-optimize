# 23 续跑十三A：闭包修复、完整载荷与post链认证

PASS；源提交 ad8a2606ec3c9e53b657f3f8261be9f7d63b23c8，sandbox已快进推送并核对；QB未启动。本轮不含overlay或真实树演练，另待用户prompt。

## 人工裁决与发布顺序

以未推Gerrit的d08b54d为起点，修复两个PM指定问题：闭包解析误把隐式输出分隔符当输出，漏掉BOLT VCS头；反向检查只对CMake元数据解析链接。post捕获计次重新开始；允许脚本捕获后仅因空BUILDROOT文件清单失败。作者/提交者/Signed-off-by均Hao Lin <hao.lin@samsung.com>，每次git -c，不改全局配置。

保持原树禁cmake/ninja/-P、受保护树/RPM/归档证据只读；只写B、本轮E与根内专用工作目录。E=W/temp/bolt-v4-20261015-review3，根内为/home/abuild/bolt-work/bolt-v4-20261015-review3。shell用POSIX sh。资源/锁/磁盘与准备错误规则沿用，无完整LLVM构建、重链或候选生成。

源提交本地amend后，0003完整补丁、helper/spec、214项stdout/stderr、新闭包/111描述、历史126逐行表、22RPM根结果、四份post完整脚本与比对先发布GitHub **0ac1113e8b3bbb66340c0c9573458f0f57a3e64e**，68个branch/pinned URL逐个HTTP200且SHA等于本地。之后才fast-forward推sandbox；本23、STATUS和索引在推送后补完。sandbox不授权启动QB，PM审完patch与证据后由用户启动。

## 逐项结果

|项目|结果|证据（tools/bolt/results/，补丁在patches/bolt/）|
|---|---|---|
|1 归一输出与离线闭包|PASS|review-closure-v2.py、review-closure-v2.json.xz、review-tool-descriptions-v2.json|
|1 构建目录外部输入|PASS|review3-external-input-audit.json|
|2 历史126项对账|PASS，未归因0|review3-history-reconciliation.json/.md、review3-history-current-plan.txt|
|3 helper限定修复|PASS|bolt_helper.py、test_third_review.py|
|4 22RPM完整合并载荷反向检查|PASS|review3-full-payload.json|
|5 四份实际生成post脚本|PASS|review3-post-debug/release-baseline/candidate.sh、review3-post-capture.json|
|6 原202保留+新增12|PASS，214/214|review3-tests.stdout/stderr.txt、review3-tests-result.json|
|6 spec未改/OFF展开沿用|PASS|review3-draft.spec，review2-macro-result.json|
|6 ordinary/candidate安全/tiny/双根post|PASS|review3-real-gates.json|
|保护审计|PASS|review3-protection.json|
|7 amend/0003/apply/tree|PASS|draft-manifest.json、0003-clang-bolt-second-review.patch|
|7 GitHub材料先发布、sandbox快进核对|PASS|review3-sandbox.json、review3-sandbox-push.txt|
|真实树演练、QB|NOT RUN，本轮明确不含/用户启动|不以本认证冒充这些步骤|

## 1–2 根因、外部输入与历史任务

原解析器把输出列表中的`|`也放入旧图输出集合，导致只要新边有隐式输出，就被all(x not in old)误判。新版移除|/||（亦移除|@分隔符），将${cmake_ninja_workdir}与对应绝对构建前缀归一，去重同一输出的双写；递归遍历全部显式/隐式/order-only依赖，不调用Ninja。1911闭包边不变，仅tools/bolt/lib/Utils/VCSVersion.inc的new标志false→true；普通1792→1791，新phony9不变，实际BOLT110→111。没有其他分类变化或旧边丢失。旧110描述JSON与旧闭包文件保持原字节。

上述结论只覆盖保存的静态 Ninja 图；未加载 .ninja_deps/depfile，未做完整 dirty 判定。未知真实任务继续失败关闭，不能将离线闭包称为完整 Ninja 实际执行认证。

111描述为102对象+7静态库+1可执行+1 generated（Generating VCSVersion.inc）。同名描述在全图可重复，但llvm-bolt闭包中恰好对应这一条边；独立JSON与完整闭包夹具证明，不从helper常量生成测试全集。

构建目录中未被任何边生产的外部文件只有3个：lib64/tf_runtime/tf_xla_runtime_dummy.c由TF自定义CMakeLists第6–7行file(WRITE)每次刷新，历史下游是TF对象与归档两条；lib/Analysis/InlinerSizeModel.o与lib/CodeGen/RegAllocEvictModel.o由TensorFlowCompile.cmake的override分支configure_file(COPYONLY)产生，覆盖源不变时不重写，现有对象与源模型SHA相同，历史日志没有普通Analysis/CodeGen归档重建。另一个外部节点`.`是目录及phony/order-only锚点，不是生成文件。其他外部输入在源码/MLGO资产目录，不属于构建目录。完整CMake原文、调用处及SHA在external-input-audit。

历史原流126项全部逐行归因：BOLT111、TF2、关闭的bolt_rt runtime8、历史额外请求merge-fdata2、关闭的AArch64 BOLT目标3；未归因0。筛选当前白名单并保留原顺序、去时间戳重新编号，得113行，tool-plan通过，generated=1单列、不计入executables。

## 3–4 反向检查与完整载荷

helper只在.cmake条目上rooted_resolve与可读检查，悬空/越界CMake链接仍拒绝；普通悬空/越界链接不解析也不误拒。BOLT工具路径、libLLVMBOLT*.a、大小写敏感定向导出串规则不变；inventory根非链接目录、遍历错误及特殊文件仍失败关闭且不算SHA。

22个普通RPM逐个SHA与基线相同后解到全新合并根，rpm2cpio/cpio各自rc0，包头路径并集无缺失；检查17722路径、47个.cmake，PASS。同一根运行d08 helper也PASS，不能声称本基准实测旧版误拒；新增普通链接夹具证明本次语义放宽只在指定范围。根保留在E/payload-merged，不上传约50GB实物，仅上传清单结果/日志。

磁盘预检按49.6GB常规载荷加2GiB元数据预算，写后保留≥30GiB；最低逐包采样空闲371802681344 B。共享锁独占约497秒，16GiB/swap0/nice15/ionice3，结束释放；未获取归档项目锁。

## 5 post采集与两类准备纠正

wrapper仅copy rpmbuild生成的%install完整脚本并返回0，未执行其中CMake/Ninja/install/post。使用__spec_install_cmd替换实际执行入口，捕获原脚本shebang/bin/sh及实际-e参数，不用rpmspec --eval。四份最终脚本均非空，rpmbuild各rc1，所有error都只是105条File not found .../BUILDROOT/...，没有Security manifest/Source等其他错误。预先在专用BUILD提供原样安全manifest，Source输入只链接原件或复制不变BOLT文件。

本项PM重新计次后，两类各修正一次：

1. 后处理边界原标记属于%post -n lldb，捕获脚本中不存在；只重做已捕获文件的分析，用第一条实际平台命令行定界，保留行首缩进及以下全部字节，不规范化空白。
2. 发布前完整脚本复核发现第一次标作release的采集实际仍是debug链。根内项目.rpmmacros定义_toolchain，CLI还传_build_create_debug=1；先前release结果不能认证真发布链。只在专用宏副本移除那一行_toolchain定义，并取消release的debug插入参数，原RPM环境前导仍逐字相同、平台/用户原宏不改；重新采集两份release。最终实际命令验证：debug有find-debuginfo且无brp-strip；release无find-debuginfo且有brp-strip。错误模式原件、宏副本/差异和修正调用都在execution包中保存。

最终debug平台段1446 B，SHA d74cb5cd7129884933309c0f82800b707014ac182c4399b10a3927c39a67858b；release平台段879 B，SHA fc4cad45df5ae685d4fd0ee0b3200edba694f9d4bfb9142d5b3c9f2234eb5f94。从首条平台命令行至原末尾逐字节相同；仅末尾追加python post与BOLT_POST_GATE_PASS，尾检最后。首条命令前用于连接install/template的空白不作为平台命令链，完整脚本原件另存供核对。Raw脚本保留RPM生成的尾空白与EOF样式，源码空白检查排除这些原件及format-patch，不能修改原文消除告警。

## 6 测试、spec与真实产物

214/214，原202测试方法全部保留，新增12。旧断言只改两组：ReviewToolPlanTests使用独立v2全集并期待generated计数；SecondReverseTests.test_dangling把测试链接改为.cmake，符合新语义。新增生成边唯一性、历史113计划/126归因、TF唯一刷新、普通悬空/越界链接通过、CMake悬空/越界及导出检查。完整stdout为空，stderr包含全部214项原文，不裁剪。

spec SHA04bc88f92c774b5a1d93d88d9ee2b33b808c383c5a7b5b494d749dc3b39ee8fc，与d08完全相同，因此沿用review2关闭开关debug/release各18段与cb679968逐字相同的证明。helper SHA6bea234609785ab47a35d8eaba31371a0f9aac0cce3ad4614be52554e0461e94，Source/B镜像逐字节相同。

ordinary7df与candidate4ec重跑安全属性、三目标tiny、20小RPM根副本的完整双根post和compare-root全部PASS；没有重生成候选或更改profile/重链/BOLT/strip参数。旧22RPM、归档证据、原源码元数据、坏cache/ninja身份保持，原缓存47987/96881772832 B。两个查找路径报告更正不涉及产品输入，未计产品准备重试。没有任何产品门禁失败后的豁免。

## 7 源身份与sandbox

d08b54da276102c2b607fbddd07966111f5147cd直接amend为ad8a2606ec3c9e53b657f3f8261be9f7d63b23c8，父仍b7e61fb92b34795868230e4f9cee8e3ec65496f6，tree62748a008e606fe4c234bc742626c2f76bfd9a3c。0003相对b7的完整format-patch，通过独立index apply/write-tree，等于完整源树。作者/提交者及Signed-off-by均Hao Lin。

材料先发布0ac1113，再只读查sandbox为b7；无force推ad8；再次只读查确为ad8。Gerrit返回成功，完整原文sandbox-push.txt公开；未推refs/for或tizen_base。供PM审核后用户启动QB的软件包写法：

```text
platform/upstream/llvm@ad8a2606ec3c9e53b657f3f8261be9f7d63b23c8
```

本轮不含真实树演练，不能用配置/脚本/小根证据冒充完整%install执行。QB还需现场tool-plan/真实构建复核、TF SHA、pipeline匹配/安全/tiny、compare-root、post尾检与RPM/DWARF清单及性能复核；全量发布构建等长期未验证项继续挂账。

## 资源

wall为scope墙时，VmHWM为采样到的最大进程高水位；memory.peak为实际cgroup峰。所有scope回收，proc挂载前/中/后及卸载原文在execution包；轻任务4GiB/swap0/nice19/ionice3，完整解包16GiB并持共享锁。无>60分钟持锁或低内存底线触发。

|阶段|状态|wall s|cgroup峰 B|采样最大VmHWM KiB|
|---|---|---:|---:|---:|
|review3-closure|PASS|2.525|230469632|224180|
|review3-closure-normalized|PASS|3.023|229933056|224232|
|review3-history-inputs|PASS|1.017|91471872|12624|
|review3-tests|PASS|3.528|93749248|46008|
|review3-full-payload|PASS|496.797|6437068800|48132|
|review3-post-capture|FAIL|1.030|42684416|12604|
|review3-post-analysis|PASS|1.021|18923520|12624|
|review3-real-gates|PASS|9.530|842846208|105052|
|review3-protection|PASS|16.054|668647424|114376|
|review3-release-corrected|PASS|1.027|40935424|12624|
|review3-sandbox-push|PASS|13.544|24354816|107032|

review3-post-capture scope的FAIL仅为上述边界定位准备错误；后续post-analysis通过，但错误release标签随后在发布前复核被撤回，经release-corrected认证真发布链。原始失败/错误模式结果未删除，没有将其冒充最终认证。完整资源/纠正记录见review3-resources、final-resources与corrections，最终post-capture JSON为修正后结果。
