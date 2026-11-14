import datetime,json
from pathlib import Path
B=Path.cwd();E=B/'tools/bolt/results/night-92-20261114';stamp=datetime.datetime.now().astimezone().isoformat()
t=json.loads((E/'toolchain-forms-summary.json').read_text());d=json.loads((E/'basedev-forms-summary.json').read_text());scan=json.loads((E/'secret-scan-result.json').read_text());ad=json.loads((E/'report-stale-admission.json').read_text())
report=f'''# 92号：TLS 松弛形式、已推送提交秘密扫描和 report-stale 准入

结论：**步骤1已完成只读分类，结论待验证；步骤2 STOP；步骤3 SKIPPED**。T 的2804条中有 **1536 IE、1252 LE、16其他**，没有检测到仍调用 `__tls_get_addr` 的未松弛GD/LD序列；另有 **1951条 PLT32** 通过输入筛选，不能使用“全部LE且无残留”的放行结论。秘密扫描命中2处，均是旧报告/日志引用的扫描断言文字；不是发现了私钥正文，但不在PM指定的脚本排除范围，按指令STOP待PM处理。机器仍有其他GBS任务，未运行report-stale。

[全部证据 raw 索引](../../tools/bolt/results/night-92-20261114/README.md)。所有旧结果只读；新结果均在 `tools/bolt/results/night-92-20261114/`。没有构建、访问QB/Gerrit、修改LLVM或删除文件。分析与交付在串行用户服务 `llvm-task92-light-20261114.service` 内完成，4GiB、swap0、Nice19、IO idle；资源原文见 `service-properties.txt`。时间为 America/Los_Angeles（UTC−08:00）。

## 1. TLS 指令形式

### 1.1 身份与 ELF 头

重算两份输入SHA，与88号相同：

|项目|输入大小|SHA256|ELF类型|PT_TLS memsz / align / filesz|
|---|---:|---|---|---|
|T|226816920|ae3d837d862673b03c3c4718f6746f6986d8abe2078bad426b97905258b91a5c|ET_DYN=3，有PT_INTERP（PIE可执行文件）|65 / 8 / 4 B|
|D|226782848|bf15cf062439714651809cd3b5ca82619407081adca64ceb65699e6ccae50501|ET_DYN=3，有PT_INTERP（PIE可执行文件）|65 / 8 / 4 B|

路径为 `W/temp/local-full-r6-20261111-materials/{{toolchain,basedev}}/reference-relocs-clang-22`。完整程序头在两个 `*-forms-summary.json`。只读平台 llvm-objdump 由对应74号构建根的 loader 和库路径启动，路径、SHA及argv见 `*-disassembly-command.json`；未使用宿主工具链。

### 1.2 全部2804条分类及样例

`tls_forms.py` 直接解析ELF定位重定位，平台objdump输出流式处理，仅保留每个offset附近的指令，不保存整个.text的反汇编。T全量；D按各类型offset排序取前5条，共15条样本，不声称D全量分类。基于实际解码指令及固定松弛序列字节判断，没有凭旧重定位类型直接推断LE/IE。

|原类型|当前实际形式|T条数|D抽样条数|
|---|---|---:|---:|
|TLSGD(19)|IE：`movq %fs:0, %rax` 后接 `addq disp32(%rip), %rax`|1536|5|
|TLSLD(20)|LE：三个data16前缀填充，随后 `movq %fs:0, %rax`|415|5|
|DTPOFF32(21)|LE局部形式：固定立即数/基址位移，不含RIP操作数|837|4|
|DTPOFF32(21)|其他：disp32后还有imm8的cmp/mov指令；保守不纳入以上固定模板|16|1|
|TLSGD/TLSLD|未松弛、仍call `__tls_get_addr`|0|0|

“其他”16条的实际指令已全部列入 `other-16-instructions.json`：12条cmpq、2条cmpl、1条cmpb、1条movb；均不含RIP操作数。这16条不是无法解码，而是初始保守模板要求disp32位于指令末尾，未覆盖其后的imm8；没有改模板重跑或把它们悄悄算作LE。对所有控制流下TLS基址来源的证明不在这次局部解码结果内。

每种分类有5组完整原文样例（D按可用样本数），见 `toolchain-examples.txt` / `basedev-examples.txt`；每条2804记录的输入offset、符号、当前指令、附近支持类记录见 `toolchain-forms-full.json.gz`。代表性原文：

```text
IE（原TLSGD @0x27e3525）：
27e3521: 64 48 8b 04 25 00 00 00 00  movq %fs:0x0, %rax
27e352a: 48 03 05 af 67 d8 05        addq 0x5d867af(%rip), %rax # 0x8569ce0
LE（原TLSLD @0x27cb8d0）：
27cb8cd: 66 66 66 64 48 8b 04 25 00 00 00 00  movq %fs:0x0, %rax
其他（DTPOFF32 @0x27cb8dc）：
27cb8d9: 48 83 b8 e8 ff ff ff 00    cmpq $0x0, -0x18(%rax)
```

### 1.3 同序列支持类重定位与源码处理

按88号同一筛选链（ALLOC、特殊目标节、NONE、converted-bit、TLS特例、动态地址、支持表）重新扫描原ELF；只统计固定TLS松弛序列范围内的记录，按地址去重：

|范围|通过筛选的记录|数量|当前落在的实际指令|
|---|---|---:|---|
|1536个GD→IE序列|PLT32(4)，符号 `__tls_get_addr`|1536|RIP相对addq的disp32字段|
|415个LD→LE序列|PLT32(4)，符号 `__tls_get_addr`|415|填充后的fs:0加载指令字段|
|合计|全部为PLT32；本范围内GOTPCRELX为0|1951|详见逐项压缩JSON|

D样本15条中，GD/LD序列各5条PLT32，共10条。`supported-sequence-records.json.gz` 包含T的1951条唯一记录和指令位置。这里的“通过”仅指输入筛选/支持表，**不是证明1951条全都被最终注册或应用**。

只依据 fea0fe46 的源码摘录（`source-handling-excerpts.txt`）：

- `RewriteInstance.cpp:2549–2557` 注释明确GOT/TLS松弛可能改写指令，读取出的值可与原符号不同；GOT/TLS令SkipVerification=true，将信息交给反汇编器决定操作数符号化。`2586–2587` 对PLT32也跳过值一致断言。
- `RewriteInstance.cpp:3024–3047` 对x86 PC-relative处理分支，代码来自函数、非节重定位且能找到ReferencedSymbol时才登记；否则输出调试信息并返回。本轮不运行BOLT，无法仅凭输入记录证明每条记录走了哪个后续分支。
- `X86MCSymbolizer.cpp:95–128` 对GOTPCRELX特别按整条指令范围查找重定位；若当前仍是PC-relative，使用当前解码地址，不依赖旧重定位的addend；已转绝对地址则按绝对地址处理。
- `X86MCSymbolizer.cpp:130–137` 无操作数字段重定位时尝试按当前PC-relative操作数符号化；`151–173` 对保留重定位计算SymbolValue/addend并构造符号操作数。GOTPCRELX特例不能直接套用到这批PLT32。

因此，关于本批“旧调用位置变为fs:0或RIP相对addq”的**最终BOLT注册/应用路径为UNKNOWN，待验证**。有IE形式和残留支持类记录，按PM规则不能写“指令与代码布局无关，BOLT移动代码不改变TLS偏移”，也不写“无害”。

### 1.4 既有运行门禁的旁证（不重跑）

- [07号](07_r1_rehearsal.md)“历史30对象/最终重测”：同一实体编译器路径的30对完整.o逐字节相同，原路径差异FAIL保留。这是历史R1结果，不当作本次输入的独立认证。
- [39号§3–4](39_use_old_text_final.md)、[43号§9](43_debuginfo_symbols.md)：tiny、三处real通过；30个历史TU×3目标的90对完整.o相同，保留.GCC.command.line。
- [74号§8.2](74_local_full_build_fa4f9978.md)：本地fea0fe46 T/D自动90TU均PASS。重读74号已保存日志提取本次real门禁：T L24083/L24087/L25162、D L24028/L24030/L24902，各8用例；post门禁T L25165、D L24905。见 `existing-runtime-gates.json`。本轮未从74号日志中找到名为BOLT_TINY_GATE_PASS的独立输出，不能据此虚构该行；tiny旁证直接引用39/43号已记录结论。

这些只是有限负载的运行层面旁证，不能替代对全部TLS重写路径的证明，也不把历史30与90说成120个互不重叠的输入。

```text
{(E/'step1.stdout').read_text().splitlines()[-1]}
{(E/'supplement.stdout').read_text().strip()}
```

## 2. 已推送提交秘密扫描：STOP（引用文字命中）

按PM定性，88号扫描脚本命中自身标记是误报，不是凭据泄漏。此次使用全新 `secret_scan.py`，读取8d1137fd和21dcb101两个提交相对其父提交的全部新增/修改文件；同路径同blob去重，变化版本分别扫描。压缩包在内存中逐个成员读取，不落盘解包或执行。累计扫描 **{scan['files_scanned_including_tar_members']} 个文件/版本或压缩成员记录**，原始blob与解压成员逐项SHA/大小在 `secret-scan-inventory.json`。

检查私钥头、password/token等赋值、Authorization头、SSH路径、Gerrit HTTP密码常见形式。唯一排除是PM指定的88号两版打包脚本及本轮扫描脚本（后者本就不在目标提交内），只登记身份及原因。没有额外排除文档、stderr或diff，也没有排除压缩包内容。

命中2行，均为21dcb101中的同一条扫描断言引用：

|文件|行号|命中类别|核对|
|---|---:|---|---|
|docs/bolt/88_entry_sync_reloc_stats_report_stale.md|98|private_key_header|错误报告中引用的Python断言行|
|tools/bolt/results/night-88-20261114/packaging-v2.stderr|3|private_key_header|同一断言的traceback源代码行|

没有匹配到其他凭据类别或压缩成员。上述2行只有签名字符串，未发现对应私钥正文；不过按本次“命中即STOP”要求，**不标PASS，也不自行增加引用文字白名单**。命中结果仅公开位置/规则/行SHA，避免扫描器把潜在凭据重新写入报告。旧提交、旧结果和扫描规则均未改写/重跑。

STOP原文：

```text
{(E/'step2.stdout').read_text().strip()}
```

## 3. D report-stale：SKIPPED

一次准入检查时间：{ad['time']}。

|条件|观测|结果|
|---|---|---|
|无其他gbs/rpmbuild/ninja/llvm-bolt|PID29234/34255/41183；`profgen-release-build-20261114c.scope`|不满足|
|MemAvailable≥20GiB|{ad['MemAvailable']} B（{ad['MemAvailable']/1024**3:.3f}GiB）|满足|
|/home available≥30GiB|{ad['home_free_bytes']} B（{ad['home_free_bytes']/1024**3:.3f}GiB）|满足|
|共享锁立即可取|其他条件已失败，未尝试获取|NOT ATTEMPTED|

按指令SKIPPED，**不是STOP**。没有等锁、等待其他构建结束或重试；未创建output root，未启动16GiB服务、未运行llvm-bolt，未删除任何文件。原始进程/cgroup、用户unit列表、df、meminfo见 `admission-*`，准入JSON含全部条件。87号计划仍有效，但本轮没有新stale名单、N/M/S/U/Q/R或资源峰值，不能引用旧值充作新运行结果。

```text
{(E/'step3.stdout').read_text().splitlines()[-1]}
```

## 4. 读取范围与交付

已读：88号报告和两个census JSON；87号report-stale计划及保存的BOLT源码；fea0fe46 Git对象中的X86MCSymbolizer.cpp；T/D输入ELF头、程序头、重定位、符号表和对应平台反汇编；两提交全部变化文件和fixtures.tar.gz成员；07/39/43/74号相关门禁记录、74号保存的构建日志；/proc现场和systemd/df/meminfo。

未读/未执行：QB/Gerrit网络、LLVM写操作、完整构建、任何新的tiny/real/30/90编译、BOLT重写/report-stale、运行时最终重定位应用追踪、D全部2804条指令分类（只抽15条）。本轮没有新性能或安全放行结论。

文档整理：{stamp}。下一步由PM裁决两处引用签名命中的扫描口径；TLS的IE与PLT32后续路径仍待定向验证。report-stale待下一次满足准入条件时再启动。
'''
p=B/'docs/bolt/92_tls_relocs_secret_scan.md';assert not p.exists();p.write_text(report)
with (B/'docs/bolt/STATUS.md').open('a') as f:f.write(f'''\n\n## 2026-11-14：92号\n\n[92号](92_tls_relocs_secret_scan.md)：T2804条全量指令分类：1536 IE、1252 LE、16其他（已解码的cmp/mov disp32+imm8）；D抽15条。两边ET_DYN/PIE、PT_TLS memsz65 align8。1951条同序列PLT32(__tls_get_addr)通过输入筛选，最终注册/应用路径UNKNOWN，不能使用“全LE且无残留”结论，标待验证。\n\n秘密扫描456个文件/版本或压缩成员记录，命中2处：21dcb101的88号报告L98和packaging-v2.stderr L3，都是引用扫描断言签名文字、不是私钥正文。按指定排除范围仍STOP，未扩大白名单、未改历史。88号原扫描误报的PM定性保留。\n\nreport-stale在{ad['time']}准入SKIPPED：仍有profgen-release-build-20261114c.scope的gbs/rpmbuild/ninja；MemAvailable{ad['MemAvailable']}B、/home available{ad['home_free_bytes']}B。未取锁、不等、不重试、未运行BOLT。全部原文见新证据目录night-92-20261114。\n''')
print('92文档 已结束',stamp,'status=待PM裁决')
