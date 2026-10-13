# 05 v4.1 草案、静态验证与停止记录

日期：2026-10-13（Asia/Shanghai）；本轮E=`/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41`。**本轮已按用户“规定之外的情况停止”规则停止产品实验：R1私有挂载准备失败且临时根绑定传播到宿主；本次绑定已精确卸载，未继续重链/重写。停止后仅封存已有草案、归档验证、设计和状态。草案不可发货，不推Gerrit。**

## 1. 当前完成范围

| 步骤 | 实际状态 | 证据 |
|---|---|---|
| 1 新sandbox/环境调查 | 完成，原样cb679968已推；metadata基线/项目宏/磁盘/应急估算完成 | 04；E/gerrit-branch-result.json、qb-scan.json、disk-opening.json |
| 2 v4.1/helper/spec草案 | 已封存本地提交；59夹具PASS、静态apply/整树PASS；完整spec宏与pipeline集成未认证 | 本文§2–3；E/helper-tests.stderr、draft-freeze.json |
| 3 旧树流水线预演 | 未启动任何重链/BOLT；因准备异常停止 | 本文§4；E/stop-and-recovery.json |
| 4 standalone配置/ninja-n | 未执行 | 停止后未继续产品实验；R1 LLVMConfig.cmake存在只是路径事实 |
| 5 90对验证资产 | 0/90新预处理文件 | 停止后未继续；没有把历史30对当新90对 |
| 6 profile压缩 | 完成并解压SHA核对 | E/profile-compression-final.json |
| 7 周三预注册 | 文档更新，不能当执行授权或验收 | 01 v4.1附录；本轮未执行 |
| 8 收尾 | 临时挂载/所有scope回收，封存并推GitHub | E/stop-and-recovery.json及最终发布记录 |

## 2. 草案身份及交付封套

本地LLVM提交 `b3ec4f03259e695bb2e6c64d7b61474380eaaa38`，父 `cb67996861d070d68fec2b4c623eed7d20ba2e23`，作者FatTank <hao.lin@samsung.com>，中文说明列目的、x86-only、失败门禁与“本地验证待补/不可发货”。仅修改packaging/llvm.spec，新增packaging/clang-bolt-helper.py及packaging/clang-bolt-v2.fdata.xz；**没有356627/356639，没有推这个提交到Gerrit**。源副本E/llvm-source工作树已提交干净。

完整format-patch E/0001-clang-bolt-draft.patch为12579316B，SHA040d45fd31b2221fea53d7778f662afc0babcc4b94d7e2ce765fb88860898f26；完整patch.xz仍10128312B，超过本证据仓库10000000B文件上限，因此保留E，不拆片或上传超限文件。

可完整重建草案的公开封套：

- [文本评审format-patch](../../patches/bolt/0001-clang-bolt-draft-review.patch)：31684B，包含spec/helper全部变更，明确不含profile二进制块，不能直接git am它冒充完整提交。
- [profile Source](../../patches/bolt/clang-bolt-v2.fdata.xz)：9735212B，SHA52fd8522b8cceadebfb6bfc0a19f721f1072cff95c682b12b2c4dd5b0cc1e27f。
- [draft-manifest.json](../../patches/bolt/draft-manifest.json)：base/本地commit/完整tree/文件大小与SHA、两部分重建方式。
- [helper](../../tools/bolt/bolt_helper.py)及[fixtures](../../tools/bolt/test_bolt_helper.py)：原样Source辅助代码与本地测试入口。

完整patch在私有Git index中git apply --cached --check通过，apply后write-tree `d2f7657e1c9ae9691ffe9b81807ae796df15dcb9`与本地提交整树相同。公开文本patch+上述Source同样重建该tree（E/public-envelope-check.json）；不会以“不含profile的文本patch”声称整树独立可用。

POSIX重建示例，只供未来隔离源副本，不在W/llvm执行：

```sh
git checkout --detach cb67996861d070d68fec2b4c623eed7d20ba2e23
git apply --check /path/0001-clang-bolt-draft-review.patch
git apply /path/0001-clang-bolt-draft-review.patch
cp /path/clang-bolt-v2.fdata.xz packaging/clang-bolt-v2.fdata.xz
git add packaging/llvm.spec packaging/clang-bolt-helper.py packaging/clang-bolt-v2.fdata.xz
git write-tree
# 期望tree=d2f7657e1c9ae9691ffe9b81807ae796df15dcb9；本地原commit身份仍以上述SHA为准。
```

## 3. 草案机制、夹具覆盖与未闭合项

新草案：x86默认%bcond_without clang_bolt，其他arch默认关闭且不运行BOLT；Source1200压缩profile、1201 helper，避开归档Source1005；debug包未定义时清楚失败。

正常LLVM先按原项目列表构建/安装记录普通清单，之后同树列表追加bolt，BOLT_BUILD_TOOLS=OFF、runtime OFF，只ninja llvm-bolt，避免要求install未构建的merge-fdata等工具；再次install后按manifest差集精确删全部新增文件/空目录，不用硬编码产物名glob。普通LLVM CMake导出metadata先备份后恢复，防止引用已删BOLT库。实际install别名是否进入CMake manifest、所有非BOLT文件是否保持相同仍未实测。

helper实现唯一链接边限定重放（保持原$ORIGIN引号，不eval，改输出/depfile且追加两个flags）；双flags对emit-relocs→LLVM strip-debug对照，严格比较非debug ALLOC/type/flags/address/size/payload与顺序符号/重定位记录；不一致按PM允许选预剥离候选并保留差异，不自动降低一致性判据。完整pipeline分支未做集成夹具或实机运行。

匹配parser：N/M/S/U/Q、R=(S+U)/(N+U)与S/N均整数≤5%，禁infer-stale；失败/截断/重复/异常计数拒绝。三目标微型逻辑比较完整对象，同源/cwd/output；真实clang并未运行，这一轮是fixture逻辑PASS。

安装helper支持安装根内绝对链接解析、循环/逃逸拒绝、硬链接/相同旧副本族发现、全组相对clang-22软链接、SHA不变post门禁。无brp-strip包装器；BOLT ELF不得含debug节且root绝对路径不得含debug。

**59/59 fixture PASS**（0.466s，运行在4GiB/nice19/ionice3 scope；初53项PASS后补tool-plan与debug所有权6项再次全套通过）：replay十项、匹配十五项、压缩SHA四项、ELF比较七项、清单/alias/post十四项、微型逻辑三项、tool-plan五项、旧debug删除一项。测试不编译LLVM、不执行真实clang/BOLT/linker。仍欠整个pipeline分支fixture、完整spec预处理、生产工具图及真实完整post，因此不能称“每个helper集成全部认证”。

草案为取得严格ordinary-final参考，暂在完整原__spec_install_post之后先存普通参考，然后换候选、移除旧clang debug、再跑完整原链并最终检查。晚定义宏意在保留原debug/arch/os/ISU/hal/app全部阶段，实际RPM宏展开未验证，不声称已成功挂接。

**严格清单的待裁决点**：ordinary debug链若产生clang专用.debug/build-id条目，而候选必须无旧DWARF且FD跳过，移除旧条目将与普通final清单不同。helper不豁免debug树，会失败；这由59项中清单反例确保，真实新配方差集尚未取得。不能保留错误旧DWARF、不能自动把“clang实体/别名除外”扩为整个debug树。需要PM明确clang专用调试产物是否也在例外范围，或给保持严格最终清单的合法方案；草案不是对此的默许放行。两次post的额外成本也未认证，恢复后应先评审这项结构。

## 4. 私有挂载异常、停止与回收

R1=`W/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0`。允许的只读metadata chroot已确认Python3.14.2、unshare/mount/rpmspec存在、原/proc未挂载、LLVMConfig.cmake路径存在；rpm4.14的macrobody扩展未识别，原post完整展开含FD、check-buildroot、compress、archive strip、python-hardlink、find-docs、ISU、hal/app检查，不能省略。

准备时采用私有mount namespace，目的是只临时挂/proc、将所有输出留E，且隔离旧cache写入；**第一次未运行Python或spec parser**，unshare报`cannot change root filesystem propagation: Invalid argument`。仅尝试把R1根自绑定后再设private，第二次报`mount: /: mount failed: Unknown error 5005`。当时宿主/proc/self/mountinfo确有本任务新R1根绑定（shared:108），而准备前findmnt -T只显示/home shared；没有继续挂/proc、overlay、执行parser或链接。

本代理立即依据“规定之外停止”规则停后续产品阶段，并精确执行sudo -n /bin/umount -l R1回收**自己的R1根绑定**。随后findmnt -R R1退出1且输出空，宿主mountinfo无R1条目；不是卸载归档根。每个scope cgroup已消失，没有对归档进程/两项目锁发信号或操作。本任务没有改R1已有构建文件、没有运行缓存prune；仅mount准备失败并回收。失败日志完整保留spec-parse-root与spec-parse-fixed-root。

共享heavy-stage.lock现存空文件，未获取、未等待，未运行重阶段；不把环境错误伪装成等锁超时/容量不足。单clang重链时原命令有绝对ThinLTO cache路径，LLVM源码明确可能更新timestamp、cache条目和prune已有条目；无法证明隔离时不能直接在原cache上重放。恢复需要可认证的隔离执行器或允许的缓存快照映射方式，不自行换链接参数或冒险写旧树。

## 5. 请求的预演结果字段

| 字段 | 本轮事实 |
|---|---|
| dual-flags重链/strip-debug一致性/回退内存 | 未执行，UNKNOWN |
| BOLT N/S/U、R、S/N | 未运行，UNKNOWN；不引用历史值冒充本轮结果 |
| 三目标真实门禁 | 未运行；仅fixture逻辑PASS |
| 完整post后真实clang存活 | 未运行 |
| 历史30可用.ii逐字节比较 | 未运行 |
| 每个重阶段wall/cgroup峰值/clang或BOLT VmHWM | 未测，因为没有重阶段 |
| standalone任务数/导出解析/ThinLTO边 | 未配置/未干跑，UNKNOWN；exports文件现存不足以证明find_package成功 |
| 90对资产 | 0/90新文件，源/头完整可用性未作本轮资产普查；不是“确认缺失90项” |

现有scope日志可复核轻量成本；不使用旧9.76GiB/25s数据替代本轮实测。压缩最终xz净38.163s，4GiB scope wall39.108s；纯静态封套检查与压缩归档只处理已有材料，不是恢复产品实验。

## 6. profile Source与发布边界

最终profile压缩参数xz -T1 -9e --lzma2=dict=128MiB，9735212B，压缩SHA52fd8522b8cceadebfb6bfc0a19f721f1072cff95c682b12b2c4dd5b0cc1e27f；解压171232190B，SHAd9b132f9430dfed32e080c65b4422bd76eba4a9c2101a2b18a7f66c94133b326。初始-T1 -6产物10809496B保留E，不混作最终Source。解压器约需128MiB字典预算，构建内stream SHA，不加载全部fdata到Python堆。

Source随本地LLVM草案commit包含；本任务未上传它到Gerrit。未来直推需确认server对象/commit大小限制与Quickbuild Source处理；GitHub每文件10000000B限制已满足Source9.735MB，完整format-patch超限所以由文本patch+Source+tree清单交付，未拆片。GitHub推证据不是BOLT进入Quickbuild。

## 7. 恢复前待明确

安全R1输出/cache隔离与临时挂载方式；实际Quickbuild sandbox项目及合并宏；完整普通与BOLT最终清单中clang专用debug条目的边界；草案双post/manifest兼容性；Gerrit Source大小限制。周三另须origin/main STATUS正式交接新cb树、准确Source/patch/spec/cache身份、共享锁可用和实时磁盘。按无人值守要求本轮仅列问题，不提问、不继续未授权替代方案。
