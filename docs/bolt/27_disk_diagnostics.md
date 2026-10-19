# 27 磁盘门槛移除、实际用量观测和失败诊断（本地通过，发布暂停）

最终本地源 `e97171ff28b085a200ad1dbe69c1292e42b28ec7`；父 `67619ec8bbbac7238a6cfc33a481ccfbcd12206f`；BASE/当前远端 `e2463165829cc91b0a1d60a3e0f915a587865f70`。署名均 Hao Lin <hao.lin@samsung.com>，Change-Id 保持。285 项本地测试 PASS；gbs export PASS。唯一一次图形密码认证失败，sudo 原文 `sudo: 1 incorrect password attempt`，包装器未启动；Tizen rpm 4.14.1.1 五项解析及可选真实 tmpfs 写满 NOT RUN，不重试、不换提权方式，故 **未推 sandbox**。主机 rpm 4.18.2 补充五项解析 PASS，不能替代构建根认证。没有 refs/for、QB、新分支或完整 LLVM 构建操作。

## 用户裁决、QB 原因及适用边界

1. 发布代码不设磁盘空间门槛：profile、BOLT、clang 变化会改变用量，固定门槛无法长期认证。
2. 确认磁盘失败后才按本次实际数据估算需求/缺口；不以 free 低判磁盘原因。
3. 长期规则：发布代码不设磁盘空间门槛，只记录剩余空间；磁盘失败的诊断值必须在失败后由本次构建实际数据计算。
4. 长期规则：本地开发机的资源、锁、磁盘规则只约束本地操作，不得进入发布代码。

用户交接 QB e2463165 在 %install 第5340秒：

```text
BOLT_GATE_FAILED: SKIP_DISK: write/reserve would leave -1765326848 bytes; require 32212254720 bytes (planned 17179869184)
```

W/temp/qb-e2463165/ 开工时不存在，收尾复核亦未收到日志，因此这是用户提供的原文，不能声称已用QB日志核实。未操作QB。

## 删除清单（行号均相对 BASE）

|文件/原行号|删除内容|
|---|---|
|spec:438、461|两处16GiB disk-preflight 调用及预算注释|
|helper:595|install_candidate 的安装预检|
|helper:656|rewrite 的四倍输入预算预检|
|helper:803|pipeline 的默认预算预检及 disk-admission.json|
|helper:847|cache_copy 的缓存大小+4GiB预留|
|helper:885|strip_all 的复制预检|
|helper:770–790、952–954、973|GIB/DISK_FLOOR/LARGE_WRITE/STAGE_WRITE_BUDGET、函数、CLI及分派；pipeline planned-write-bytes 参数|

完整逐项原文见 removed-gates.json。发布代码不包含本地 cgroup、共享锁、30GiB/10GiB底线；不改变候选重链、strip-debug、BOLT OPTIONS、strip-all 参数或 profile。

## 观测与诊断设计

`python3 -B helper disk-report STAGE` 在 begin（BOLT动作开始）、tool-built、pipeline、post 各一次。输出设备号、time_ns、free_bytes、明确的 owned_paths；同时原子保存 disk-baseline.json 与 disk-STAGE.json。**观测永远rc0**，包括目录尚不存在、空间零、记录写失败；唯一的持久写入非门禁例外。保存失败会注明 report_error，不能声称记录已落盘。

BOLT自有集合：build/clang-bolt/**、build/tools/bolt/**、build/lib64/libLLVMBOLT*.a、build/bin/llvm-bolt，及链接命令 ThinLTO 缓存相对begin快照的正向分配增量。通过lstat/st_blocks*512度量实际分配，同设备+inode去重硬链接；不跟随软链接。目录占用包括在内。缓存每个条目取 max(当前分配-基线分配,0)，新条目取当前分配；LLD清理旧条目不会抵消新增长。额外记录净变化，仅供核对。普通缓存原有内容不算BOLT新增。

`python3 -B helper disk-diagnose STEP LOG` 只读、不写任何文件，包括无pyc；优先本步骤Python OSError errno28/122，另处理 copytree 保留的本步骤结构化文件错误列表。日志匹配表（re.I）：

|匹配|含义|
|---|---|
|No space left on device|写满原文|
|Disk quota exceeded|配额原文|
|\bENOSPC\b|错误名|
|\bEDQUOT\b|配额错误名|

不读取无关步骤日志，不用低剩余空间判定。not-disk 只一行 cause/step/free_bytes，不预测。disk 输出固定 BOLT_DISK_DIAGNOSIS JSON 段，注明“估计值，依据本次构建实际文件大小”。报告/诊断错误不替代原失败，helper与spec原始stderr保留并exit1。损坏记录降级为当前free与实际自有占用，明确标degraded，禁止填造固定需求。未知数据也明确列unknown_components/incomplete_estimate；EDQUOT的真实配额余量不可由statvfs推断，单独标注。

spec 每步由 bolt_checked/bolt_step/bolt_capture 捕获同一步的原始输出；regular日志写满时输出仍在内存，失败后把它交给disk-diagnose /dev/stdin，随后exit1。平台post是原链在一个shell heredoc内执行一次，由checked runner监督；尾检和最后观测顺序保留。原%install的关闭开关路径不加wrapper，主机展开字节相同比较PASS；构建根验证未运行。

## 失败后公式与边界

以失败文件系统为范围；used_bytes 为当前实际分配及已观测缓存正向增量；estimated_remaining_bytes 为剩余保留产物增长加各阶段临时副本的最大同时占用；estimated_total_bytes=used_bytes+estimated_remaining_bytes；shortfall_bytes=max(estimated_remaining_bytes-free_bytes,0)。不同设备分开记录，当前缺口只比较失败设备。

- 工具：ceil(已完成任务实际输出文件总字节 / 已完成任务数 × 剩余任务数)，再扣已有未完成输出分配。任务来自本次tool-plan与真实日志；FAILED的上一任务不算完成。零完成任务或无法量出产物时注明未知，不能除零或套默认预算。
- 重链：max(本次ordinary clang实际大小, 已观测重链部分大小)-已存在分配。
- strip-debug：重链完成大小（未完成时用上项实际数据估计）作为临时副本峰值。
- BOLT：max(本次输入大小, 已观测BOLT部分大小)-已存在分配；完成后用实测完整大小。
- strip-all：本次BOLT输出/候选实际大小推算候选副本和strip临时峰值；不是固定倍数预算。保存与临时副本按顺序计算峰值，不把不同时存在的临时文件相加。
- profile未解包：只读流式解压本次压缩Source并计数，不写新文件。
- cache-copy（R1类可选能力）：本次源文件实测大小减目标已分配；新树仍原地缓存，不复制。
- ThinLTO：实测正向增长已经计入used一次，不再重复叠加；未来未观测的增长不可从旧预算得知，明确标为未知。故不完整估计是可观测下界，**不承诺预测全部未来缓存增长**。
- 写失败的原子JSON/文本：异常附本次UTF-8序列化真实字节数；临时文件删除后把该值计入仍需写入部分。

已知大小夹具（B）：ordinary16384；完成工具输出4096+8192、完成2/剩余2，预测12288；未完成工具已分配4096，新增8192；重链已有4096，新增12288；后续重写16384、候选16384保留，加最大临时16384，剩余峰值=8192+12288+16384+16384+16384=69632，实测算法69632。详情 FORMULA_FIXTURE 原文见release-tests.stdout。注入测试free4096为mock值，非宿主真剩余；install注入used81920、总151552、短缺65536。

## 写满必停审计与25处加固

25处为“缺少显式立即错误检查、写出完整性或最终提交顺序”的加固计数，**不表示旧版25处都会静默成功**（RPM -e、后续门禁可能已有保护）：普通CMake安装1处；后续17个ln/mkdir/mv/cp/rm命令17处；clang.cfg heredoc1处；成功标记追加1处；子进程日志写入1处；临时clang SHA核对1处；install-state前移1处；别名写入前移1处；JSON/文本原子写长度及fsync1处。合计25。原转换器已有exit1，这次只补同一步诊断，不重复计数。profile失败清理不遮蔽原错另作健壮性修正。

安装顺序：审计ELF/身份/别名 → 同目录临时复制 → chmod、fsync、大小+SHA → 准备别名 → 原子保存state并发布结果 → 改名别名（此时仍解析为普通clang） → **最后一次可失败文件操作为clang实体os.replace**。部分复制、JSON失败、别名失败和最终rename失败均保留原clang SHA。若后续平台post失败，构建仍失败；完整安装候选也不会因此成为成功RPM，不能把“原子安装”理解成绕过post门禁。

以下行号针对最终源提交。所有save及原子写经异常传播rc1，call父进程拥有日志写入并监测短写/flush/fsync，写错则kill/reap整个组；清理unlink错误只保留原失败。纯观测save为用户要求的明确例外。源中字符串replace不属于文件写入，未算入表。

### helper写入点、子进程与JSON结果保存

|行|函数|写入/调用原文|失败处置|
|---|---|---|---|
|119|atomic_text|`path.parent.mkdir(parents=True, exist_ok=True)`|strict length/flush/fsync then atomic rename; errors retain original exception; temporary cleanup best effort|
|122|atomic_text|`tmp.open('w',encoding='utf-8')`|strict length/flush/fsync then atomic rename; errors retain original exception; temporary cleanup best effort|
|123|atomic_text|`stream.write(text)`|strict length/flush/fsync then atomic rename; errors retain original exception; temporary cleanup best effort|
|124|atomic_text|`os.fsync(stream.fileno())`|strict length/flush/fsync then atomic rename; errors retain original exception; temporary cleanup best effort|
|125|atomic_text|`os.replace(tmp,path)`|strict length/flush/fsync then atomic rename; errors retain original exception; temporary cleanup best effort|
|130|atomic_text|`tmp.unlink()`|failure cleanup only; suppress cleanup error to preserve primary rc1|
|136|save|`atomic_text(path, json.dumps(value, ensure_ascii=False, indent=2)+'\n')`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|199|call|`log.parent.mkdir(parents=True, exist_ok=True)`|parent checked writes/flush/fsync; kill and reap process group before error rc1|
|207|call|`save(log.with_suffix(log.suffix+'.argv.json'), invocation)`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|208|call|`log.open('wb')`|parent checked writes/flush/fsync; kill and reap process group before error rc1|
|217|call|`output.write(chunk)`|parent checked writes/flush/fsync; kill and reap process group before error rc1|
|230|call|`os.fsync(output.fileno())`|parent checked writes/flush/fsync; kill and reap process group before error rc1|
|235|call|`save(log.with_suffix(log.suffix+'.argv.json'), dict(invocation,completed=True,rc=0))`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|273|profile_unpack|`output.parent.mkdir(parents=True, exist_ok=True)`|fail-closed: uncaught error reaches cli rc1; diagnostic does not override error|
|275|profile_unpack|`output.open('xb')`|fail-closed: uncaught error reaches cli rc1; diagnostic does not override error|
|276|profile_unpack|`shutil.copyfileobj(src, dst, 1024 * 1024)`|fail-closed: uncaught error reaches cli rc1; diagnostic does not override error|
|280|profile_unpack|`output.unlink()`|failure cleanup only; suppress cleanup error to preserve primary rc1|
|522|tiny_gate|`work.mkdir(parents=True, exist_ok=True)`|fail-closed: uncaught error reaches cli rc1; diagnostic does not override error|
|523|tiny_gate|`source.write_text(TINY)`|fail-closed: uncaught error reaches cli rc1; diagnostic does not override error|
|525|tiny_gate|`call([cc, '--version'], work/(label+'-version.log'), timeout=30)`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|533|tiny_gate|`out.unlink()`|fail-closed: uncaught error reaches cli rc1; diagnostic does not override error|
|534|tiny_gate|`call(argv, work/(triple+'-'+label+'.log'), cwd=work, timeout=60)`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|537|tiny_gate|`shutil.copyfile(out, dest)`|fail-closed: uncaught error reaches cli rc1; diagnostic does not override error|
|540|tiny_gate|`save(work/'result.json', rows)`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|579|compare_root|`save(after_path, current)`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|645|install_candidate|`shutil.copyfile(candidate,tmp)`|staged copy, mode/fsync/SHA; state and staged aliases before final clang rename; failure preserves old clang|
|646|install_candidate|`tmp.chmod(stat.S_IMODE(st.st_mode))`|staged copy, mode/fsync/SHA; state and staged aliases before final clang rename; failure preserves old clang|
|647|install_candidate|`os.fsync(stream.fileno())`|staged copy, mode/fsync/SHA; state and staged aliases before final clang rename; failure preserves old clang|
|654|install_candidate|`link.symlink_to('clang-22')`|staged copy, mode/fsync/SHA; state and staged aliases before final clang rename; failure preserves old clang|
|658|install_candidate|`save(state,result)`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|660|install_candidate|`os.replace(link,path)`|staged copy, mode/fsync/SHA; state and staged aliases before final clang rename; failure preserves old clang|
|661|install_candidate|`os.replace(tmp,entity)`|staged copy, mode/fsync/SHA; state and staged aliases before final clang rename; failure preserves old clang|
|665|install_candidate|`path.unlink()`|failure cleanup only; suppress cleanup error to preserve primary rc1|
|717|rewrite|`work.mkdir(parents=True, exist_ok=True)`|fail-closed: uncaught error reaches cli rc1; diagnostic does not override error|
|719|rewrite|`call([bolt, '--version'], work/'bolt-version.log')`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|722|rewrite|`call(argv, work/'bolt.log', timeout=1800)`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|732|rewrite|`save(work/'rewrite-result.json', result)`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|793|tool_prepare|`save(state_path, value)`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|942|disk_report|`save(baseline_path, baseline)`|best effort observation rc0|
|944|disk_report|`save(work/('disk-'+stage+'.json'), record)`|best effort observation rc0|
|1148|run_step|`call(argv,log,timeout=None)`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|1150|run_step|`Path(log).open('a')`|checked marker length/flush/fsync; errors rc1 and original transcript preserved|
|1151|run_step|`os.fsync(stream.fileno())`|checked marker length/flush/fsync; errors rc1 and original transcript preserved|
|1151|run_step|`stream.write(success_marker+'\n')`|checked marker length/flush/fsync; errors rc1 and original transcript preserved|
|1153|run_step|`atomic_text(output,text)`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|1169|pipeline|`atomic_text(script,replay_script(edge,reference,work/'reference-relocs.d',cache))`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|1170|pipeline|`call(['/bin/sh',str(script)],work/'reference-relocs.log',cwd=build,timeout=1800)`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|1171|pipeline|`call([str(build/'bin/llvm-strip'),'--strip-debug',str(reference)],work/'reference-strip.log',timeout=600)`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|1179|pipeline|`save(work/'pipeline-result.json',result)`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|1205|cache_copy|`destination.parent.mkdir(parents=True, exist_ok=True)`|fail-closed: uncaught error reaches cli rc1; diagnostic does not override error|
|1206|cache_copy|`shutil.copytree(source, destination, copy_function=shutil.copy2)`|fail-closed: uncaught error reaches cli rc1; diagnostic does not override error|
|1211|cache_copy|`save(result, value)`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|1243|strip_all|`shutil.copy2(before, after)`|fail-closed: uncaught error reaches cli rc1; diagnostic does not override error|
|1244|strip_all|`call([str(tool), '--strip-all', str(after)], Path(result).with_suffix('.strip.log'), timeout=600)`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|1249|strip_all|`save(result, identity)`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|1356|main|`save(a.result,result)`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|1362|main|`save(a.result,result)`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|1366|main|`Path(a.script).chmod(0o755)`|fail-closed: uncaught error reaches cli rc1; diagnostic does not override error|
|1366|main|`atomic_text(a.script,script)`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|1369|main|`save(a.output,result)`|atomic/checked writer; exception propagates to rc1 before candidate commit|
|1375|main|`save(Path(a.work)/'post-result.json',result)`|atomic/checked writer; exception propagates to rc1 before candidate commit|

### spec中受检查的写入及四次观测

|行|原文|失败处置|
|---|---|---|
|411|`if BOLT_BUILD_OUTPUT=$(ninja -d keeprsp -j %{mlgo_build_jobs} 2>&1); then`|checked; failed step diagnostic then exit1|
|459|`  bolt_checked "$bolt_stage" "$BOLT_WORK/$bolt_stage.log" python3 -B %{SOURCE1201} run-step "$bolt_stage" "$BOLT_WORK/$bolt_stage.log" -- "$@"`|checked; failed step diagnostic then exit1|
|465|`  bolt_checked "$bolt_stage" "$BOLT_WORK/$bolt_stage.log" python3 -B %{SOURCE1201} run-step "$bolt_stage" "$BOLT_WORK/$bolt_stage.log" --output "$bolt_output" -- "$@"`|checked; failed step diagnostic then exit1|
|468|`python3 -B %{SOURCE1201} disk-report begin`|best effort rc0|
|471|`%{?__bolt_disk_reporting:bolt_step ordinary-install }cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}/usr -P cmake_install.cmake`|checked; failed step diagnostic then exit1|
|475|`bolt_step preflight python3 -B %{SOURCE1201} preflight`|checked; failed step diagnostic then exit1|
|476|`bolt_step certified python3 -B %{SOURCE1201} certified`|checked; failed step diagnostic then exit1|
|481|`bolt_step snapshot python3 -B %{SOURCE1201} snapshot "%{buildroot}" "$BOLT_WORK/install-before.json"`|checked; failed step diagnostic then exit1|
|482|`bolt_step manifest-copy cp install_manifest.txt "$BOLT_WORK/install-manifest-before.txt"`|checked; failed step diagnostic then exit1|
|483|`bolt_step ordinary-copy cp -p bin/clang-22 "$BOLT_WORK/ordinary-clang-22"`|checked; failed step diagnostic then exit1|
|484|`bolt_capture link-command "$BOLT_WORK/link.original" ninja -t commands -s bin/clang-22`|checked; failed step diagnostic then exit1|
|485|`bolt_step unpack python3 -B %{SOURCE1201} unpack %{SOURCE1200} "$BOLT_WORK/profile.fdata"`|checked; failed step diagnostic then exit1|
|486|`bolt_step configure cmake -S ../llvm -B .   '-DLLVM_ENABLE_PROJECTS=clang;lldb;clang-tools-extra;lld;compiler-rt;openmp;bolt'   -DBOLT_BUILD_TOOLS=OFF -DBOLT_ENABLE_RUNTIME=OFF   -DBOLT_INCLUDE_TESTS=OFF -DBOLT_TARGETS_TO_BUILD=X86`|checked; failed step diagnostic then exit1|
|489|`LC_ALL=C NINJA_STATUS='[%%f/%%t] ' bolt_capture tool-dry-run "$BOLT_WORK/tool-dry-run.txt" ninja -n llvm-bolt`|checked; failed step diagnostic then exit1|
|491|`bolt_capture tool-plan "$BOLT_WORK/tool-plan.json" python3 -B %{SOURCE1201} tool-plan "$BOLT_WORK/tool-dry-run.txt"`|checked; failed step diagnostic then exit1|
|492|`bolt_step tool-prepare python3 -B %{SOURCE1201} tool-prepare "$PWD" "$BOLT_WORK/tool-plan.json" "$BOLT_WORK/tool-before.json"`|checked; failed step diagnostic then exit1|
|493|`LC_ALL=C NINJA_STATUS='[%%f/%%t] ' bolt_checked tool-build "$BOLT_WORK/tool-build.txt" python3 -B %{SOURCE1201} run-step tool-build "$BOLT_WORK/tool-build.txt" --success-marker BOLT_NINJA_EXIT_0 -- ninja -j 1 llvm-bolt`|checked; failed step diagnostic then exit1|
|494|`bolt_step tool-verify python3 -B %{SOURCE1201} tool-verify "$PWD" "$BOLT_WORK/tool-plan.json" "$BOLT_WORK/tool-build.txt"   "$BOLT_WORK/tool-before.json" "$BOLT_WORK/tool-build-verification.json"`|checked; failed step diagnostic then exit1|
|495|`python3 -B %{SOURCE1201} disk-report tool-built`|best effort rc0|
|496|`bolt_step pipeline python3 -B %{SOURCE1201} pipeline "$PWD" "$BOLT_WORK" "$PWD/bin/llvm-bolt"`|checked; failed step diagnostic then exit1|
|498|`python3 -B %{SOURCE1201} disk-report pipeline`|best effort rc0|
|501|`bolt_step compare-root python3 -B %{SOURCE1201} compare-root "%{buildroot}" "$BOLT_WORK/install-before.json"   "$BOLT_WORK/install-after-pipeline.json"`|checked; failed step diagnostic then exit1|
|506|`%{?__bolt_disk_reporting:bolt_step install-write-1 }ln -sf %{_prefix}/bin/clang++ %{buildroot}%{_prefix}/bin/clang++-%{llvm_version}`|checked; failed step diagnostic then exit1|
|508|`%{?__bolt_disk_reporting:bolt_step install-write-2 }ln -sf clang %{buildroot}%{_prefix}/bin/%{_host}-clang`|checked; failed step diagnostic then exit1|
|509|`%{?__bolt_disk_reporting:bolt_step install-write-3 }ln -sf clang++ %{buildroot}%{_prefix}/bin/%{_host}-clang++`|checked; failed step diagnostic then exit1|
|511|`%{?__bolt_disk_reporting:bolt_step clang-config /bin/sh -c 'cat >> "$1"' sh %{buildroot}/%{_prefix}/bin/clang.cfg}%{!?__bolt_disk_reporting:cat >> %{buildroot}/%{_prefix}/bin/clang.cfg} << EOF`|checked; failed step diagnostic then exit1|
|515|`%{?__bolt_disk_reporting:bolt_step install-write-4 }ln -sf clang.cfg %{buildroot}/%{_prefix}/bin/clang++.cfg`|checked; failed step diagnostic then exit1|
|518|`%{?__bolt_disk_reporting:bolt_step install-write-5 }mkdir -p %{buildroot}%{sdk_bin_dir}`|checked; failed step diagnostic then exit1|
|519|`%{?__bolt_disk_reporting:bolt_step install-write-6 }mkdir -p %{buildroot}%{sdk_lib_dir}`|checked; failed step diagnostic then exit1|
|521|`%{?__bolt_disk_reporting:bolt_step install-write-7 }mv %{buildroot}%{_prefix}/bin/lldb %{buildroot}%{sdk_bin_dir}`|checked; failed step diagnostic then exit1|
|522|`%{?__bolt_disk_reporting:bolt_step install-write-8 }mv %{buildroot}%{_prefix}/bin/lldb-argdumper %{buildroot}%{sdk_bin_dir}`|checked; failed step diagnostic then exit1|
|523|`%{?__bolt_disk_reporting:bolt_step install-write-9 }mv %{buildroot}%{_prefix}/bin/lldb-server %{buildroot}%{sdk_bin_dir}`|checked; failed step diagnostic then exit1|
|525|`%{?__bolt_disk_reporting:bolt_step install-write-10 }ln -sf %{sdk_bin_dir}/lldb %{buildroot}%{_prefix}/bin/`|checked; failed step diagnostic then exit1|
|527|`%{?__bolt_disk_reporting:bolt_step install-write-11 }cp -P %{buildroot}%{_libdir}/liblldb.so* %{buildroot}%{sdk_lib_dir}/`|checked; failed step diagnostic then exit1|
|530|`%{?__bolt_disk_reporting:bolt_step install-write-12 }mkdir -p %{buildroot}%{python3_sitelib}`|checked; failed step diagnostic then exit1|
|531|`%{?__bolt_disk_reporting:bolt_step install-write-13 }cp -a ../clang/bindings/python/clang %{buildroot}%{python3_sitelib}/`|checked; failed step diagnostic then exit1|
|533|`%{?__bolt_disk_reporting:bolt_step install-write-14 }rm -rf %{buildroot}%{_libdir}/debug/*`|checked; failed step diagnostic then exit1|
|534|`%{?__bolt_disk_reporting:bolt_step install-write-15 }rm -rf %{buildroot}/usr/lib/libear/*`|checked; failed step diagnostic then exit1|
|535|`%{?__bolt_disk_reporting:bolt_step install-write-16 }rm -rf %{buildroot}/usr/lib/libscanbuild/*`|checked; failed step diagnostic then exit1|
|540|`%{?__bolt_disk_reporting:bolt_step install-write-17 }rm -rf "%{_builddir}/%{buildsubdir}/build/native-archive-conversion"`|checked; failed step diagnostic then exit1|
|541|`%{?__bolt_disk_reporting:bolt_step install-write-18 }python3 %{SOURCE1005} --root "%{buildroot}" \`|checked; failed step diagnostic then exit1|
|555|`if BOLT_INSTALL_OUTPUT=$(python3 -B %{SOURCE1201} install "%{buildroot}" "$BOLT_WORK/clang.candidate" \`|checked; failed step diagnostic then exit1|
|802|`    bolt_checked platform-post "%{_builddir}/%{buildsubdir}/build/clang-bolt/platform-post.log" python3 -B %{SOURCE1201} run-step platform-post "%{_builddir}/%{buildsubdir}/build/clang-bolt/platform-post.log" -- /bin/sh -e <<'BOLT_PLATFORM_POST' \`|checked; failed step diagnostic then exit1|
|805|`    bolt_checked post "%{_builddir}/%{buildsubdir}/build/clang-bolt/post.log" python3 -B %{SOURCE1201} run-step post "%{_builddir}/%{buildsubdir}/build/clang-bolt/post.log" -- python3 -B %{SOURCE1201} post "%{buildroot}" "%{_builddir}/%{buildsubdir}/build/clang-bolt/install-state.json" "%{_builddir}/%{buildsubdir}/build/clang-bolt/ordinary-clang-22" "%{_builddir}/%{buildsubdir}/build/clang-bolt/post-gate" --resource-dir "%{buildroot}%{_libdir}/clang/%{llvm_version}" \`|checked; failed step diagnostic then exit1|
|807|`    python3 -B %{SOURCE1201} disk-report post`|best effort rc0|

## 全部测试与准备过程

|验证|结果|原始证据|
|---|---|---|
|既有基线257测试（TMPDIR在E/tmp）|257 PASS|baseline-home-tests.stdout/stderr|
|保留/按新语义替换既有测试，加非磁盘AST不变约束|258 PASS|legacy-updated-tests.stdout/stderr|
|最终全部本地测试|285 PASS，15.035秒|release-tests.stdout/stderr|
|复制/JSON/子进程命令/子进程日志/四类install ENOSPC|各真实CLI退出1，cause=disk，字段齐全；原clang不变|injection/* 原文与argv/rc|
|普通门禁非磁盘失败|rc1、cause=not-disk、原始错误不变|injection/not-disk.*|
|诊断自身异常（磁盘与非磁盘）|仍原始rc1及原始错误|injection/*diagnostic-exception.*|
|损坏baseline记录|只报当前free/used、degraded，不抛异常|injection/corrupt-records.*|
|精确已知大小公式|12288及69632符合期望|release-tests.stdout FORMULA_FIXTURE|
|disk-report正常/不存在目录、free=0、观测保存异常|全部rc0|test_disk_diagnostics.py、release-tests.*|
|真实copytree包装异常结构识别|PASS新增1项|CopytreeEvidenceTests|
|发布参数/匹配/ELF/安全/tiny/plan/verify等AST保持|PASS|test_non_disk_gates_unchanged|
|最终spec脚本只捕获、/bin/sh -n|PASS，四次report，无产品命令执行|host-capture/*|
|gbs export最终提交|PASS 7个Patch均声明，49.384秒|gbs-export.json/stdout/stderr；gbs-exported-llvm.spec|
|主机rpm4.18.2补充五项展开|5 PASS，仅补充|host-final-matrix.json及5对原文|
|Tizen rpm4.14.1.1必须五项解析|NOT RUN，唯一图形认证失败|sudo.stderr、privileged-validation.json|
|可选真实tmpfs写满|NOT RUN，同上|privileged-validation.json|
|sandbox推送|NOT RUN，缺必须认证|remote-final.txt仍e2463165|

已有13项“门槛拒绝”相关断言按本轮语义调整：CacheTests两项、DiskTests八项、PipelineTests一项、FourthPrereqTests两项，数量保留。历史“只改文件头AST不变”用例改为比较已保存历史两份helper，避免错误地冻结未来实现；新增当前非磁盘门禁AST逐项不变检查。新磁盘模块27项；总285。没有删掉非磁盘负例门禁。测试stdout含真实故障输出及FORMULA_FIXTURE，并非只有测试汇总；stderr含逐项unittest原文。

准备记录：首次既有测试沿用/tmp导致两个旧预算门禁报错（原始baseline-tests.*保留）；设置TMPDIR=E/tmp后257 PASS。新增故障夹具最初把edge文本而非文件路径传入cache-copy，修正为已保存link.original；子进程心跳/输出夹具用flush=True确保立即触发日志失败。disk-tests.*、disk-tests-fixed.*及随后完整PASS原文均保留，不掩盖早期夹具失败。读文件定位误用了过宽的上级find，遇到无关保护根Permission denied后立即中止，未修改任何树；后改为只查明确父目录AGENTS，不再递归该区域。临时目录/输入均位于本会话E，受保护树未写入。

图形认证只实际弹一次。sudo第一次失败后single-use askpass拒绝后续请求，因此第二次调用仅mkdir报已存在，没有第二个图形框；未切换sudo -n或其他提权。原文另含zenity输入法Gtk warning，不能把它误写为产品失败。root-entry.json不存在，无锁/挂载/根内命令，无需伪造下层前后快照。

## 完整diff、提交说明及发布状态

[完整源码diff（e2463165→新提交）](../../tools/bolt/results/disk-diagnostics-20261019/source.diff)，仅helper与spec；[完整增量补丁](../../patches/bolt/0006-disk-report-and-failure-diagnostics.patch)，独立patch -p1后两文件逐字节等于新提交；[完整压缩文本版0000](../../patches/bolt/0000-clang-bolt-squashed.patch)；profile单独交付且SHA不变。完整源码diff不是从父676计算的旧BOLT全量，增量基点明确e2463165。完整cat-file见new-commit.txt，spec/helper完整文件一并保存。

提交说明只新增磁盘段及替换Still open中的首次install措辞；标题不变42字符、每行≤72，Signed-off-by/Change-Id保持。全文差异：

```diff
--- BASE message
+++ new message
@@ -16,6 +16,11 @@
 while adding these two files to the source package. --without clang_bolt
 is available for local builds. Only enabled %build adds -d keeprsp. No
 project configuration change is required.
+
+No disk-space thresholds are imposed; each stage records free space.
+If a step fails because its disk is full, stop before replacing the
+packaged clang and report current free space, estimated requirements
+and shortfall from actual file sizes measured in this build.
 
 The binary Source is the existing profile v2, trained on 13 ARM plus 10
 AArch64 source files. Compressed size 9,735,212 bytes; SHA256
@@ -57,8 +62,9 @@
 records, the pre-strip BOLT ELF, matching ordinary ELF, tool and profile
 identities.
 
-Still open: full release-mode build; accel/worker identity; first real
-%install execution; cleanup cannot be guaranteed without matching /proc;
+Quickbuild x86_64 completed %install on this same implementation before
+the Source-order fix. Still open: full release-mode build; accel/worker
+identity; cleanup cannot be guaranteed without matching /proc;
 performance outside LLVM workloads. ninja -j1 does not cap linker
 memory. Maintenance notes: header of packaging/clang-bolt-helper.py
 
```

原候选4ec07159及profile未重生成。原树未运行cmake/ninja/-P，未对ARM树执行构建、安装或写入操作；没有新的产品二进制验证或Quickbuild执行。源码最终本地提交已保留，材料在bolt-v4发布供复核，**不能把未推的草案写成远端交付**。后续仍须获可用单次图形授权完成Tizen五项，然后按当时远端SHA复核精确租约；本轮不重试。单次认证失败是当前唯一发布阻塞，非产品门禁FAIL。


## GitHub 材料发布收尾

本轮材料137项固定于 `67b022739befcee5f2d671246d9382498e28385a`；raw续表21–25同时列分支与钉提交。274个raw URL逐个字节数与SHA256核验PASS。完整校验明细 raw-verification.json 与 closing-check.json 随本次索引提交公开。没有sandbox推送尝试；当前远端仍BASE，待Tizen认证完成后方可继续。发布代码/source diff --check PASS；0000历史完整format-patch的空白上下文保留原文，不为消除证据文件的空白提示而修改发布源码。


## 收窄修订（2026-10-19；e97171ff不采用）

PM结论：RPM用`/bin/sh -e`执行脚本段，普通命令失败已有停止机制。e97171ff包装普通LLVM ninja、基线安装和平台post，会使长阶段输出延迟到命令结束，并改变已认证平台链。撤回这些包装，不推e97171ff。

本次直接在BASE `e2463165829cc91b0a1d60a3e0f915a587865f70` 上amend，最终源 `9e5675f57d122549997caffa39b655dfefc46fee`，父仍 `67619ec8bbbac7238a6cfc33a481ccfbcd12206f`，不是在e97171ff上叠加；Hao Lin作者/提交者/Signed-off-by及原Change-Id保留，说明每行≤72。profile、BOLT生成参数、既有4ec候选不变。全部认证与sandbox更新均PASS；先发布材料，再按精确租约推送，原文见本节收尾。

长期规则：**rpm 以 sh -e 执行脚本段；BOLT 改动不得改写普通构建、基线 %install 步骤和平台后处理链的执行方式**。本地资源/锁/磁盘规则仅用于本地执行，不进入发布代码。

### 撤回与保留

- `%build`普通ninja行和全部条件分支恢复BASE；删除BOLT_BUILD_OUTPUT内存捕获，主构建正常即时输出。
- 普通cmake install、所有ln/clang.cfg heredoc/mkdir/mv/cp/rm及静态库转换调用恢复BASE；删除__bolt_disk_reporting全套前缀和宏。
- 平台post恢复原宏原样执行一次，删除platform-post的run-step、内存捕获及嵌套shell/heredoc。BOLT尾检保留原结构，仅helper加-B及最后附一行disk-report post。
- BOLT helper子命令保持BASE直接`python3 ... || exit 1`，只加-B；失败由自身cli先诊断再rc1，不另包一层run-step。
- 只包装下面8个BOLT动作（六类命令加BEGIN/END两个标记）。spec完整diff见下，人工复核差异仅用户1a–e允许范围；普通基线没有新增函数调用。
- call恢复BASE：Popen stdout=日志文件、stderr=STDOUT，无管道/线程，成功不扫描日志字样。只保留成功completed=True侧记录和失败bolt_log。atomic_text/save、临时clang fsync/SHA/最终rename及磁盘实际大小公式保留。

|新spec行|BOLT命令|
|---|---|
|465|`bolt_step manifest-copy cp install_manifest.txt "$BOLT_WORK/install-manifest-before.txt"`|
|466|`bolt_step ordinary-copy cp -p bin/clang-22 "$BOLT_WORK/ordinary-clang-22"`|
|467|`bolt_checked link-command "$BOLT_WORK/link-command.log" python3 -B %{SOURCE1201} run-step link-command "$BOLT_WORK/link-command.log" --output "$BOLT_WORK/link.original" -- ninja -t commands -s bin/clang-22`|
|469|`bolt_step configure cmake -S ../llvm -B . \`|
|474|`bolt_step dry-run-begin /bin/echo BOLT_TOOL_DRY_RUN_BEGIN`|
|475|`LC_ALL=C NINJA_STATUS='[%%f/%%t] ' bolt_checked tool-dry-run "$BOLT_WORK/tool-dry-run.log" python3 -B %{SOURCE1201} run-step tool-dry-run "$BOLT_WORK/tool-dry-run.log" --output "$BOLT_WORK/tool-dry-run.txt" -- ninja -n llvm-bolt`|
|476|`bolt_step dry-run-end /bin/echo BOLT_TOOL_DRY_RUN_END`|
|480|`LC_ALL=C NINJA_STATUS='[%%f/%%t] ' bolt_checked tool-build "$BOLT_WORK/tool-build.txt" python3 -B %{SOURCE1201} run-step tool-build "$BOLT_WORK/tool-build.txt" --success-marker BOLT_NINJA_EXIT_0 -- ninja -j 1 llvm-bolt`|

### 三态原因判定

直接errno28/122，或本步骤日志匹配四类磁盘字样 => disk；日志可读、非空且无磁盘迹象 => not-disk；日志不存在、为空或不可读 => unknown。unknown只报当前free/used，说明“日志不可用，无法判定原因”，不做需求推算。/dev/stdin只读取一次，分类和证据复用同一份文本，避免第二次读取空流造成错误判定。成功命令即使日志出现ENOSPC文本也不失败。

unknown CLI故障注入原文（free4096为夹具值）：

```text
BOLT_DISK_DIAGNOSIS {"cause": "unknown", "step": "snapshot", "free_bytes": 4096, "used_bytes": 69632, "reason": "日志不可用，无法判定原因"}
```

### 逐字节结构比较

`python3 -B structure_check.py`：完整脚本及提取结果随证据公开。%build取`%build`至`%install`全部字节；%install保留BOLT架构/开关双块以外的全部行（包括普通x86静态库转换块）；平台链从两次RPM真正生成但只复制的脚本提取，宏路径完全相同。post尾检另外仅撤销被允许的-B和新增观测后比较，不能声称含允许差异的尾检全文原始字节相同。

|cmp项目|字节|退出码|结论|
|---|---:|---:|---|
|build|9331|0|逐字节相同|
|install-baseline|1895|0|逐字节相同|
|platform-post|304|0|逐字节相同|
|post-tail-allowed-edits-only|489|0|逐字节相同|

实际比较命令和结果（完整argv也见structure-result.json）：

```sh
cmp -- /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/base-build.txt /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/new-build.txt
# exit 0; stdout/stderr empty
cmp -- /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/base-install-baseline.txt /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/new-install-baseline.txt
# exit 0; stdout/stderr empty
cmp -- /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/base-platform-post.txt /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/new-platform-post.txt
# exit 0; stdout/stderr empty
cmp -- /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/base-post-tail-allowed-edits-only.txt /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/new-post-tail-allowed-edits-only.txt
# exit 0; stdout/stderr empty
```

Host两个capture的rpmbuild退出1是copy-only包装之后空BUILDROOT的文件清单失败，不是执行安装失败；两个生成脚本都`/bin/sh -n`通过。没有执行其中任何cmake/ninja命令。完整平台链原文分别见base-platform-post.txt/new-platform-post.txt。

### 本次全部验证

|项目|结果|
|---|---|
|既有测试按新行为更新+新增unknown等|289/289 PASS（49.103秒）|
|ENOSPC复制/JSON/子进程/安装|PASS，rc1，磁盘判定及字段保持；安装原clang SHA不变|
|非磁盘失败|PASS，非空可读本步骤日志，not-disk，原始错误不变|
|诊断自身异常|PASS，原始错误/rc1不变|
|unknown缺失/空/不可读日志|PASS，仅free/used与说明，无推算|
|成功日志含ENOSPC|PASS，命令成功不变成失败|
|/dev/stdin日志一次读取|PASS，分类和evidence保持一致|
|sh -e +仅BOLT函数+失败命令|PASS，诊断后rc1，不运行SHOULD_NOT_RUN|
|结构cmp与完整spec diff|PASS，范围符合用户1a–e|
|gbs export新提交|PASS，命令/版本/导出spec全部保存|
|Tizen rpm x86-default|PASS，主解析rc0，7个Patch，Source/Patch清单保存|
|Tizen rpm x86-without|PASS，主解析rc0，7个Patch，Source/Patch清单保存|
|Tizen rpm x86-rollback|PASS，主解析rc0，7个Patch，Source/Patch清单保存|
|Tizen rpm armv7l|PASS，主解析rc0，7个Patch，Source/Patch清单保存|
|Tizen rpm aarch64|PASS，主解析rc0，7个Patch，Source/Patch清单保存|
|下层完整清单与六SHA|前后完全一致，锁持有171.380秒，卸载错误0|

构建根rpm包版本 `rpm 4.14.1.1-1.4; rpm-build 4.14.1.1-1.4`，CLI显示4.14.1；主解析用rpmbuild -bp --nodeps --nobuild，关闭项确用--without clang_bolt。辅助Source/Patch清单用rpmspec -P，因该rpmspec不支持--without，清单项用等效宏，不替代主解析。五个目标均在同一x86根的rpm完成，不进入ARM树。唯一一次图形认证成功，一次sudo完成overlay/proc/dev挂载、abuild解析、卸载；下层仅只读，未运行原树cmake/ninja/-P。

准备记录：图形包装的启动比gbs导出完成稍早；在任何根内产品操作之前加导出完成等待与rc0核对，实际root-entry发生在最终导出成功之后。没有重复图形认证，没有产品输入/环境重试。既有“线程日志ENOSPC”用例改为直接打开日志ENOSPC，符合恢复后的直接输出方式；非磁盘用例提供真实非空步骤日志，缺失日志另列unknown。其余原测试保留，新增4项，总数从285到289。前半的25处宽泛包装审计属于未采用e971历史方案，不再代表本修订；本修订普通步骤依赖原RPM sh-e停止机制。

### 两份spec完整diff（BASE→本次）

```diff
diff --git a/packaging/llvm.spec b/packaging/llvm.spec
index 2c9b72b126a1..ef2f87843968 100644
--- a/packaging/llvm.spec
+++ b/packaging/llvm.spec
@@ -426,54 +426,68 @@ cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}/usr -P cmake_install.cmake
 case $(printf '%s' '%{buildroot}' | LC_ALL=C tr '[:upper:]' '[:lower:]') in
   *debug*) echo 'BOLT buildroot absolute path contains debug' >&2; exit 1 ;;
 esac
+BOLT_BUILD="$PWD"
+BOLT_WORK="$PWD/clang-bolt"
+BOLT_INSTALL_ROOT="%{buildroot}"
+BOLT_PROFILE_SOURCE="%{SOURCE1200}"
+export BOLT_BUILD BOLT_WORK BOLT_INSTALL_ROOT BOLT_PROFILE_SOURCE
+bolt_fail() {
+  python3 -B %{SOURCE1201} disk-diagnose "$1" "$2" || true
+  exit 1
+}
+bolt_checked() {
+  bolt_stage=$1
+  bolt_log=$2
+  shift 2
+  if bolt_output=$("$@" 2>&1); then
+    printf '%%s\n' "$bolt_output" || bolt_fail "$bolt_stage-output" -
+  else
+    printf '%%s\n' "$bolt_output" || true
+    printf '%%s\n' "$bolt_output" | python3 -B %{SOURCE1201} disk-diagnose "$bolt_stage" /dev/stdin || true
+    exit 1
+  fi
+}
+bolt_step() {
+  bolt_stage=$1
+  shift
+  bolt_checked "$bolt_stage" "$BOLT_WORK/$bolt_stage.log" python3 -B %{SOURCE1201} run-step "$bolt_stage" "$BOLT_WORK/$bolt_stage.log" -- "$@"
+}
+python3 -B %{SOURCE1201} disk-report begin
 echo "BOLT_BUILDROOT_OK %{buildroot}"
-python3 %{SOURCE1201} preflight || exit 1
-python3 %{SOURCE1201} certified || exit 1
+python3 -B %{SOURCE1201} preflight || exit 1
+python3 -B %{SOURCE1201} certified || exit 1
 if [ -r /proc/self/stat ]; then echo BOLT_PROC_OK; else echo BOLT_PROC_MISSING; fi
 # One relink: emit-relocs, then LLVM strip-debug, BOLT and full strip.
 # The handed-off build owns its original ThinLTO cache; do not duplicate it.
-# Default 16 GiB BOLT-stage write budget must leave 30 GiB on this filesystem.
-BOLT_WORK="$PWD/clang-bolt"
 mkdir -p "$BOLT_WORK" || exit 1
-python3 %{SOURCE1201} disk-preflight "$BOLT_WORK" 17179869184 || exit 1
 # File-list baseline is the actual ordinary CMake install, not a name whitelist.
-python3 %{SOURCE1201} snapshot "%{buildroot}" "$BOLT_WORK/install-before.json" || exit 1
-cp install_manifest.txt "$BOLT_WORK/install-manifest-before.txt" || exit 1
-cp -p bin/clang-22 "$BOLT_WORK/ordinary-clang-22" || exit 1
-ninja -t commands -s bin/clang-22 > "$BOLT_WORK/link.original" || exit 1
-python3 %{SOURCE1201} unpack %{SOURCE1200} "$BOLT_WORK/profile.fdata" || exit 1
-cmake -S ../llvm -B . \
+python3 -B %{SOURCE1201} snapshot "%{buildroot}" "$BOLT_WORK/install-before.json" || exit 1
+bolt_step manifest-copy cp install_manifest.txt "$BOLT_WORK/install-manifest-before.txt"
+bolt_step ordinary-copy cp -p bin/clang-22 "$BOLT_WORK/ordinary-clang-22"
+bolt_checked link-command "$BOLT_WORK/link-command.log" python3 -B %{SOURCE1201} run-step link-command "$BOLT_WORK/link-command.log" --output "$BOLT_WORK/link.original" -- ninja -t commands -s bin/clang-22
+python3 -B %{SOURCE1201} unpack %{SOURCE1200} "$BOLT_WORK/profile.fdata" || exit 1
+bolt_step configure cmake -S ../llvm -B . \
   '-DLLVM_ENABLE_PROJECTS=clang;lldb;clang-tools-extra;lld;compiler-rt;openmp;bolt' \
   -DBOLT_BUILD_TOOLS=OFF -DBOLT_ENABLE_RUNTIME=OFF \
-  -DBOLT_INCLUDE_TESTS=OFF -DBOLT_TARGETS_TO_BUILD=X86 || exit 1
+  -DBOLT_INCLUDE_TESTS=OFF -DBOLT_TARGETS_TO_BUILD=X86
 # Only certified BOLT tasks and the paired configure-refreshed TF anchor.
-if LC_ALL=C NINJA_STATUS='[%%f/%%t] ' ninja -n llvm-bolt > "$BOLT_WORK/tool-dry-run.txt" 2>&1; then
-  echo BOLT_TOOL_DRY_RUN_BEGIN
-  cat "$BOLT_WORK/tool-dry-run.txt"
-  echo BOLT_TOOL_DRY_RUN_END
-else
-  cat "$BOLT_WORK/tool-dry-run.txt"
-  exit 1
-fi
-python3 %{SOURCE1201} tool-plan "$BOLT_WORK/tool-dry-run.txt" > "$BOLT_WORK/tool-plan.json" || exit 1
+bolt_step dry-run-begin /bin/echo BOLT_TOOL_DRY_RUN_BEGIN
+LC_ALL=C NINJA_STATUS='[%%f/%%t] ' bolt_checked tool-dry-run "$BOLT_WORK/tool-dry-run.log" python3 -B %{SOURCE1201} run-step tool-dry-run "$BOLT_WORK/tool-dry-run.log" --output "$BOLT_WORK/tool-dry-run.txt" -- ninja -n llvm-bolt
+bolt_step dry-run-end /bin/echo BOLT_TOOL_DRY_RUN_END
+python3 -B %{SOURCE1201} tool-plan "$BOLT_WORK/tool-dry-run.txt" > "$BOLT_WORK/tool-plan.json" || exit 1
 cat "$BOLT_WORK/tool-plan.json"
-python3 %{SOURCE1201} tool-prepare "$PWD" "$BOLT_WORK/tool-plan.json" "$BOLT_WORK/tool-before.json" || exit 1
-python3 %{SOURCE1201} disk-preflight "$PWD" 17179869184 || exit 1
-if LC_ALL=C NINJA_STATUS='[%%f/%%t] ' ninja -j 1 llvm-bolt > "$BOLT_WORK/tool-build.txt" 2>&1; then
-  echo BOLT_NINJA_EXIT_0 >> "$BOLT_WORK/tool-build.txt"
-  cat "$BOLT_WORK/tool-build.txt"
-else
-  cat "$BOLT_WORK/tool-build.txt"
-  exit 1
-fi
-python3 %{SOURCE1201} tool-verify "$PWD" "$BOLT_WORK/tool-plan.json" "$BOLT_WORK/tool-build.txt" \
+python3 -B %{SOURCE1201} tool-prepare "$PWD" "$BOLT_WORK/tool-plan.json" "$BOLT_WORK/tool-before.json" || exit 1
+LC_ALL=C NINJA_STATUS='[%%f/%%t] ' bolt_checked tool-build "$BOLT_WORK/tool-build.txt" python3 -B %{SOURCE1201} run-step tool-build "$BOLT_WORK/tool-build.txt" --success-marker BOLT_NINJA_EXIT_0 -- ninja -j 1 llvm-bolt
+python3 -B %{SOURCE1201} tool-verify "$PWD" "$BOLT_WORK/tool-plan.json" "$BOLT_WORK/tool-build.txt" \
   "$BOLT_WORK/tool-before.json" "$BOLT_WORK/tool-build-verification.json" || exit 1
 cat "$BOLT_WORK/tool-build-verification.json"
-python3 %{SOURCE1201} pipeline "$PWD" "$BOLT_WORK" "$PWD/bin/llvm-bolt" || exit 1
+python3 -B %{SOURCE1201} disk-report tool-built
+python3 -B %{SOURCE1201} pipeline "$PWD" "$BOLT_WORK" "$PWD/bin/llvm-bolt" || exit 1
 echo BOLT_PIPELINE_PASS
+python3 -B %{SOURCE1201} disk-report pipeline
 # BOLT configuration/build/rewrite must not change the ordinary installation.
 # Do not reinstall: that would add BOLT libraries, unregistered aliases and exports.
-python3 %{SOURCE1201} compare-root "%{buildroot}" "$BOLT_WORK/install-before.json" \
+python3 -B %{SOURCE1201} compare-root "%{buildroot}" "$BOLT_WORK/install-before.json" \
   "$BOLT_WORK/install-after-pipeline.json" || exit 1
 echo BOLT_COMPARE_ROOT_PASS
 # Any subsequent buildroot mutation (including native archive conversion) must follow this gate.
@@ -527,7 +541,7 @@ python3 %{SOURCE1005} --root "%{buildroot}" \
 %ifarch x86_64
 %if %{with clang_bolt}
 # Candidate is fully stripped before the one unchanged platform post-processing chain.
-python3 %{SOURCE1201} install "%{buildroot}" "$BOLT_WORK/clang.candidate" \
+python3 -B %{SOURCE1201} install "%{buildroot}" "$BOLT_WORK/clang.candidate" \
   "$BOLT_WORK/install-state.json" "$BOLT_WORK/identity.json" || exit 1
 
 %endif
@@ -769,7 +783,8 @@ echo "plugin load /usr/share/dotnet.tizen/netcoreapp/SOS/libsosplugin.so" > /roo
 %global __bolt_original_spec_install_post %{__spec_install_post}
 %define __spec_install_post \
     %{__bolt_original_spec_install_post} \
-    python3 %{SOURCE1201} post "%{buildroot}" "%{_builddir}/%{buildsubdir}/build/clang-bolt/install-state.json" "%{_builddir}/%{buildsubdir}/build/clang-bolt/ordinary-clang-22" "%{_builddir}/%{buildsubdir}/build/clang-bolt/post-gate" --resource-dir "%{buildroot}%{_libdir}/clang/%{llvm_version}" || exit 1 \
-    echo BOLT_POST_GATE_PASS
+    python3 -B %{SOURCE1201} post "%{buildroot}" "%{_builddir}/%{buildsubdir}/build/clang-bolt/install-state.json" "%{_builddir}/%{buildsubdir}/build/clang-bolt/ordinary-clang-22" "%{_builddir}/%{buildsubdir}/build/clang-bolt/post-gate" --resource-dir "%{buildroot}%{_libdir}/clang/%{llvm_version}" || exit 1 \
+    echo BOLT_POST_GATE_PASS \
+    python3 -B %{SOURCE1201} disk-report post
 %endif
 %endif
```

完整helper/spec总diff见本轮source.diff；0007为e2463165到本修订的真正增量（不是676父提交的全量），独立patch -p1后两文件逐字节等于新提交；0000文本版与profile分开交付。提交说明完整原文和message.diff也一并公开。


### 收窄修订推送结果

第一至第三步全PASS后，以BASE e2463165的完整SHA作为唯一分支租约推送，远端从 `e2463165829cc91b0a1d60a3e0f915a587865f70` 更新为 `9e5675f57d122549997caffa39b655dfefc46fee`，推后查询一致，rc0。没有refs/for、tizen_base、QB或新分支操作；e971未推。材料先发布于 `de32b57d6add455018519fc88a1fe957733aa6ba`，304个raw URL在推送前字节/SHA核验PASS。完整argv、stdout/stderr与两次查询见push-result.json、push-before/after.stdout，Gerrit原文如下：

```text
remote: 
remote: Processing changes: refs: 1        
remote: Processing changes: refs: 1, done            
To ssh://review.tizen.org:29418/platform/upstream/llvm
 + e2463165829c...9e5675f57d12 9e5675f57d122549997caffa39b655dfefc46fee -> sandbox/lhmax2025/bolt_pgo (forced update)
```

供后续使用的软件包标识：`platform/upstream/llvm@9e5675f57d122549997caffa39b655dfefc46fee`。这里仅记录分支更新，未启动QB。收窄修订的SHA、范围、289测试与五项解析认证取代本页前半未采用e971的结论；前半作为历史证据保留。

收尾材料路径记录：补存close_results.py时首次用了相对路径的错误父目录，rg定位后按绝对工作目录修正；只影响附加脚本复制，未影响产品操作、289测试、五项解析或已保存推送原文，不重跑这些步骤。
