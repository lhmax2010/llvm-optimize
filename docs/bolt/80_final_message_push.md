# 80. 最终提交说明改写、sandbox推送与r7评审包

结论：**PASS**。新HEAD为 4e80f54e10fe920439455123f0ac2cb8af5ab924，sandbox已核对一致；三个对应代码树全部不变，作者与作者日期不变，Change-Id及Signed-off-by不变。未构建、未访问QB，未推送refs/for或其他LLVM远端分支。

## 1. 前置核对

- 证据草稿固定读取bolt-v4提交c413b67e7d884775214dbcb1376718739f6f6936，工作树文件与该版本逐字节相同。
- 原链8a50d712 → 1e415935 → fea0fe46，底父13c3e223，三棵树与授权值一致，原工作树干净。
- 0001/0002/0003草稿的Change-Id分别与对应原提交相同；0002与原BOLT说明全文逐字节相同。
- tizen_base HEAD=61ef5d31ca91025c414c748477bef0c64ddfa67c，tree=087e06cf9c79c571c711af8a07057496940ae73d；tree与13c3e223相同，**verdict B**。
- Gerrit只使用完整URL与SSH BatchMode，无终端密码输入。[前置检查JSON](../../tools/bolt/results/final-message80-20261112/preflight.json)、[tizen_base提交信息](../../tools/bolt/results/final-message80-20261112/tizen-base-show.txt)、[只读fetch输出](../../tools/bolt/results/final-message80-20261112/fetch-tizen-base.stderr)。

前置ls-remote原文：

~~~text
fea0fe464d56e17f2c7588c557bfffd9f6ac352b	refs/heads/sandbox/lhmax2025/bolt_pgo
61ef5d31ca91025c414c748477bef0c64ddfa67c	refs/heads/tizen_base
~~~

## 2. 重建与树核对

在独立游离工作树 /home/linhao/Toolchain/development/llvm-optimize/temp/final-message-20261112/source 中操作，不新建分支；原bolt-on-359934工作树HEAD仍为fea0fe46。使用原tree对象、原作者头、原作者日期，git -c user.name="Hao Lin" -c user.email=hao.lin@samsung.com commit-tree从13c3e223逐个重建。工作树先取原最终树，再只移动其游离HEAD到新链；文件内容未改变。提交者为Hao Lin。

|序号|原SHA|新SHA|新旧共同tree|
|---|---|---|---|
|1|8a50d7122346258fd1171d270861a4ae28a8717c|8e35d0c90d5d87924b2f268b5ef20317e6b805d8|3d961cbb04f5446f84d2089b4f65f3178f2bd7fa|
|2|1e415935a83a187aab7c41f9713115a0974a0365|51417b0fa060154ad887e362235c68488003d009|c23914776684bf94fdd5961f447f7c24e7bb79bc|
|3|fea0fe464d56e17f2c7588c557bfffd9f6ac352b|4e80f54e10fe920439455123f0ac2cb8af5ab924|b2e8af2477cf623a945aa80bf8288a262dd4a5a9|

|序号|原样保留的作者头（含时间戳/时区）|标题列数|最大行列数|草稿字节/代码补丁/树核对|
|---|---|---:|---:|---|
|1|Hao Lin <hao.lin@samsung.com> 1792065558 +0800|40|72|PASS|
|2|Hao Lin <hao.lin@samsung.com> 1793251341 +0800|42|72|PASS|
|3|Hao Lin <hao.lin@samsung.com> 1793947765 +0800|46|72|PASS|

三份新消息均与指定草稿字节完全相同；trailer解析结果与原提交相同。无QB编号、内部绝对路径、docs/引用。没有禁止作为代码文件说明出现的项目相对路径（如packaging/clang-bolt-helper.py）。

git diff fea0fe464d56e17f2c7588c557bfffd9f6ac352b 4e80f54e10fe920439455123f0ac2cb8af5ab924 输出为空，见[空diff证据](../../tools/bolt/results/final-message80-20261112/final-tree.diff)。每个提交相对其父的完整binary/full-index代码补丁也逐字节相同。[创建命令原文](../../tools/bolt/results/final-message80-20261112/rebuild-argv.json)、[核对JSON](../../tools/bolt/results/final-message80-20261112/verification-v2.json)。

## 3. range-diff原文

命令：

~~~sh
git range-diff --no-color 13c3e223d9e1b35e4affb55255c5042f8c940f35..fea0fe464d56e17f2c7588c557bfffd9f6ac352b 13c3e223d9e1b35e4affb55255c5042f8c940f35..4e80f54e10fe920439455123f0ac2cb8af5ab924
~~~

~~~text
1:  8a50d7122346 ! 1:  8e35d0c90d5d cmake: use hybrid LLVM linkage on x86_64
    @@ Commit message
         produced 22 binary RPMs and one source RPM. The 188-entry NEEDED table
         had 183 passes, four non-default targets not produced, and one accepted
         --as-needed exception (AnnotateFunctions.so). Native archives passed
    -    225/225 checks and 90 complete objects were byte-identical. See docs/53
    -    in the validation evidence.
    +    225/225 checks and 90 complete objects were byte-identical.
     
         Add a post-build NEEDED assertion for the three component-linked
         drivers.
2:  1e415935a83a = 2:  51417b0fa060 packaging: optimize x86_64 clang with BOLT
3:  fea0fe464d56 ! 3:  4e80f54e10fe packaging: fix x86 LLVM flags and archive mode
    @@ Metadata
      ## Commit message ##
         packaging: fix x86 LLVM flags and archive mode
     
    -    QB 1214821 inherited GCC project options into a clang build. Source1005
    +    A GCC-based project passed its options into a clang build. Source1005
         rejected -feliminate-unused-debug-types; release commands also lacked
         its previously mandatory DWARF setting.
     
    -    Fix x86_64 compilation flags to the effective Toolchain values recorded
    -    by QB 1215143. Inherit reviewed architecture flags, reject native CPU
    +    Fix x86_64 compilation flags to the effective values of the Toolchain
    +    project. Inherit reviewed architecture flags, reject native CPU
         selection, and warn on debug sequences other than -g2 -gdwarf-4 -g.
    -    Release commands contain no debug flags. Match whole tokens and
    -    preserve the caller's IFS state and shell options.
    +    Release commands contain no debug flags. Match whole tokens and preserve
    +    the caller's IFS state and shell options.
     
         Fix LDFLAGS to the Toolchain value. Executable and shared-library linker
         flags remain explicitly set by the spec; MODULE targets (plugins) take
         LDFLAGS, so Base-Dev plugin links gain -z relro, --as-needed and
         --gc-sections, matching Toolchain. This retains the existing policy of
    -    removing project stack-protector and --param=ssp-buffer-size options;
    -    it does not introduce a new hardening policy.
    +    removing project stack-protector and --param=ssp-buffer-size options; it
    +    does not introduce a new hardening policy.
     
         Print TIZEN_LLVM_NORMALIZED_FLAGS for prior normalization and
         TIZEN_LLVM_DROPPED_FLAGS for the four reviewed extra project options.
    -    Unreviewed project options are dropped with TIZEN_LLVM_FLAGS_WARNING
    -    on stdout and stderr for manual review; they do not interrupt the build.
    +    Unreviewed project options are dropped with TIZEN_LLVM_FLAGS_WARNING on
    +    stdout and stderr for manual review; they do not interrupt the build.
         Uncertified debug sequences also warn. Reject only native CPU selection
         and invalid release mode values. Review warnings before adding options
         to the fixed set or expected-dropped list. Non-x86_64 behavior is kept.
     
    -    Local and QB command strings differ in the placement of section flags.
    -    The prior stripped QB clang equals the local post-RUNPATH clang, as
    -    recorded in docs/bolt/49 section A.4. Recheck the identity chain, RPM
    -    contents and 90 translation units in the next complete build; these
    -    lightweight checks alone do not prove new binary identity.
    +    Local and project-build command strings differ in the placement of
    +    section flags. Prior qualification found the stripped project-build
    +    clang equal to the local post-RUNPATH clang. Identity-chain,
    +    package-content and complete-object comparisons provide the separate
    +    binary qualification evidence; lightweight checks alone do not prove
    +    binary identity.
     
         Require Source1005 --debug-info yes|no and match each converted member's
         recorded command. Release means no debug option in that command; any
         debug option still requires the certified final -gdwarf-4. Reject debug
    -    sections in converted release outputs. Preserve native members as-is
    -    and count them, without applying that assertion to preexisting objects.
    -    All 3853 converted full-20261030 members recorded debug options.
    +    sections in converted release outputs. Preserve native members as-is and
    +    count them, without applying that assertion to preexisting objects. All
    +    3853 members in the debug qualification recorded debug options.
     
         Following review, reject -Wa, options, which PS10 accepted through its
         broad -W branch, and report -Xassembler (already rejected) as an
    @@ Commit message
         archive and relocation parsing against malformed sizes, size fields,
         long-name numbers and offsets, section tables, section payloads and
         indexes. Check each relocation against an explicit x86_64 field width
    -    table taken from LLVM 22.1.8; reject relocation types outside that
    -    table, CREL relocation sections, 8- and 16-bit absolute relocations and
    -    fields outside their target section, bounding compressed sections by
    -    their uncompressed size. Handle SIGHUP and process-group reaping during
    -    conversion, reset an inherited ignored SIGCHLD, keep inherited ignored
    -    TERM, INT and HUP ignored, and exit with 128+signal after cancellation,
    -    deciding the final status after the original handlers are restored. With
    -    BOLT enabled, the spec passes the converter's 129/130/143 through; with
    -    BOLT disabled, the call keeps exit 1 so that expansion is unchanged.
    +    table taken from LLVM 22.1.8, excluding seven dynamic-linking-only
    +    types: COPY, GLOB_DAT, JUMP_SLOT, RELATIVE, DTPMOD64, TLSDESC and
    +    IRELATIVE. Reject types outside the table and CREL sections. For PIC,
    +    reject 8- and 16-bit absolute relocations in allocated sections when
    +    they reference non-absolute symbols; retain the existing 32- and 64-bit
    +    PIC checks. Validate relocation field bounds against the target section;
    +    for compressed targets, use the declared uncompressed size as the bound.
    +    Handle SIGHUP and process-group reaping during conversion, reset an
    +    inherited ignored SIGCHLD, keep inherited ignored TERM, INT and HUP
    +    ignored, and exit with 128+signal after cancellation, deciding the final
    +    status after the original handlers are restored. With BOLT enabled, the
    +    spec passes the converter's 129/130/143 through; with BOLT disabled, the
    +    call keeps exit 1 so that expansion is unchanged.
     
         Based on Change 359934: keeps its token classification, per-switch
         replay and adopted checks; adds the declared debug-info mode with a
~~~

结论：第1/3个提交只变说明，第2个说明及代码均不变；第2/3个SHA也因父链/提交者时间变化而更新。

输出解析准备错误修正1次：最初脚本要求hunk标题含“## Commit message ##”，但Git实际输出“@@ Commit message”，且某个hunk标题为“@@ Metadata”后立即进入“## Commit message ##”。没有实际作者或代码差异；脚本断言误报。修正区块识别后，逐个增删行仍必须处于提交说明区，所有原有树/作者/消息/补丁相等判定均保留并重查。没有修改提交或草稿来满足检查。[原错误](../../tools/bolt/results/final-message80-20261112/verification-failure.txt)、[解析修正diff](../../tools/bolt/results/final-message80-20261112/preparation-fix-01.diff)、[说明](../../tools/bolt/results/final-message80-20261112/preparation-fix-01.txt)。原失败记录保留。

## 4. sandbox推送

推送前再次ls-remote：

~~~text
fea0fe464d56e17f2c7588c557bfffd9f6ac352b	refs/heads/sandbox/lhmax2025/bolt_pgo
~~~

打印并仅执行一次的推送命令：

~~~sh
git push --force-with-lease=refs/heads/sandbox/lhmax2025/bolt_pgo:fea0fe464d56e17f2c7588c557bfffd9f6ac352b ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm 4e80f54e10fe920439455123f0ac2cb8af5ab924:refs/heads/sandbox/lhmax2025/bolt_pgo
~~~

执行环境GIT_SSH_COMMAND='ssh -o BatchMode=yes'、GIT_TERMINAL_PROMPT=0。推送原文（含服务器返回）：

~~~text
remote: 
remote: Processing changes: refs: 1        
remote: Processing changes: refs: 1, done            
To ssh://review.tizen.org:29418/platform/upstream/llvm
 + fea0fe464d56...4e80f54e10fe 4e80f54e10fe920439455123f0ac2cb8af5ab924 -> sandbox/lhmax2025/bolt_pgo (forced update)
~~~

推后ls-remote：

~~~text
4e80f54e10fe920439455123f0ac2cb8af5ab924	refs/heads/sandbox/lhmax2025/bolt_pgo
~~~

远端等于新HEAD；[push-result.json](../../tools/bolt/results/final-message80-20261112/push-result.json)。没有其他LLVM远端写操作，没有修改远端配置。

## 5. r7交付与PM裁决

[评审包README](../../patches/rebase-359934-20261112-r7/README.md)，目录仅有0001.patch、0002.patch、0003.patch及README。三份是完整format-patch文本，包含[PATCH 1/3]–[PATCH 3/3]；0002的profile以Git binary patch文本编码保留。[导出命令](../../tools/bolt/results/final-message80-20261112/r7-format-patch-argv.json)、[文件大小和SHA](../../tools/bolt/results/final-message80-20261112/r7-files.json)。

**PM裁决原文：只改提交说明、树不变，不需要新QB。源码包中0008补丁文件只有提交说明部分和首行提交号会变，代码正文不变；QB 1226850/1226851对新HEAD有效。**

用相同format-patch选项导出新旧混合链接提交，已证明diff --git起至文件尾完全相同；除首行From提交号与说明段落外，邮件头、统计和正文相同。[完整差异](../../tools/bolt/results/final-message80-20261112/hybrid-message-export.diff)、[证明结果](../../tools/bolt/results/final-message80-20261112/0008-code-body-proof.json)。本轮没有生成新源码RPM；源码包适用性是PM裁决，不冒称新的打包实测。

79号B1–B6已最终PASS，源码包原始FAIL及按R2双维度归类后的PASS分开保留。本轮不重跑这些验证。

## 6. 读取范围、资源与结束行

已读：STATUS及79号结论；c413b67e三个草稿；原链与基线的Git提交对象；Gerrit两条分支ref及tizen_base fetch结果；新旧消息、author/tree/trailer；完整代码diff、range-diff、三份导出补丁。

未读/未做：没有访问QB页面或构建、没有重新下载RPM、没有重跑二进制/归档比较、没有构建或安装/LLDB。没有改历史构建根、旧结果或VS Code配置，没有删除文件。源码工作分支保留；只创建游离工作树和新提交对象。

所有命令串行运行于systemd用户服务：MemoryMax=8G、MemorySwapMax=0、CPUQuota=400%、Nice=19、IOSchedulingClass=idle。无OOM，不提高限制、不重试推送。

~~~text
STEP1 已结束 2026-11-12T23:24:44.374870+08:00 status=PASS
STEP2 已结束 2026-11-12T23:25:43.348772+08:00 status=PASS
STEP3 已结束 2026-11-12T23:26:23.451923+08:00 status=FAIL
STEP3_RECHECK 已结束 2026-11-12T23:27:40.784928+08:00 status=PASS
STEP4 已结束 2026-11-12T23:28:21.413679+08:00 status=PASS
STEP5 已结束 2026-11-12T23:29:15.601879+08:00 status=PASS
~~~
