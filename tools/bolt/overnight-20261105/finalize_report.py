from pathlib import Path
import datetime,json,shutil,subprocess
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');E=B/'tools/bolt/results/baseline-attribution-20261105';p=B/'docs/bolt/60_baseline_attribution.md';s=p.read_text()
s=s.replace('210条例外全部来自ompdModule.so及其.debug的.dynsym：','210条例外分别来自ompdModule.so的.dynsym（84条）和其.debug的.symtab（126条）：').replace('[`symbol-exceptions.tsv`](../../tools/bolt/results/baseline-attribution-20261105/symbol-exceptions.tsv)','[`module-symbol-exceptions.tsv`](../../tools/bolt/results/baseline-attribution-20261105/module-symbol-exceptions.tsv)')
s=s.replace('全449文件范围，共269文件、5,066个ELF有ALLOC节头/位置差异，5,083处变化中5,072处内容相同；11处实际内容变化全部在下面的ompdModule.so。不能把“ALLOC section changed”直接译为代码被改变。','全449文件范围，共269文件、5,066个ELF有ALLOC节头/位置差异。排除两个节顺序改变的MODULE文件后，5,064个ELF的5,064处ALLOC变化内容全部相同。两个MODULE必须按节名对齐复核，最终确认8个ALLOC节内容不同。初次按节次序配对得出的11处不是最终结论；两版原始证据保留。不能把“ALLOC section changed”直接译为代码被改变。')
s=s.replace('完整逐文件结果、CRC和证明/错误在cert-debuglink-recheck.json。','完整逐文件证明/错误在cert-debuglink-recheck.json。另独立计算了全部133对符号文件的CRC，两边存储CRC、实际CRC及文件名/填充全部匹配（cert-all-crc.json，133/133）；所以48项失败不能归咎于错误CRC。')
s=s.replace('下面11个实际加载节的所有差异范围保存在unexplained-ranges.jsonl.gz，含旧/新节文件偏移和节内半开区间[start,end)，可直接换算文件偏移。','最终按节名对齐后的全部差异范围保存在module-named-sections.json，含旧/新节文件偏移和节内半开区间[start,end)，可直接换算文件偏移。all-section-audits和unexplained-ranges是初次按序遍历的原始记录；MODULE节序变化时，以module-named-sections为准，非MODULE原审计不受影响。')
a=s.index('|usr/share/gdb/python/ompd/ompdModule.so|',s.index('### 3.7'));b=s.index('\n\n实际ALLOC内容差异',a)
s=s[:a]+'''|usr/share/gdb/python/ompd/ompdModule.so|.dynamic、.dynsym、.eh_frame、.eh_frame_hdr、.init、.rela.dyn、.rodata、.text；程序头/节顺序|未解释：MODULE链接变化有证据，精确因果未隔离|
|usr/lib/debug/usr/share/gdb/python/ompd/ompdModule.so.debug|.debug_aranges、.debug_info、.debug_line、.debug_loc、.debug_ranges、.shstrtab、.symtab；程序头/节顺序|未解释：地址/布局及调试记录变化；.GCC.command.line另列记录节|'''+s[b:]
s=s.replace('`.dynsym, .rela.dyn, .rodata, .eh_frame_hdr, .eh_frame, .text, .init, .fini, .dynamic, .data, .tm_clone_table`','`.dynsym, .rela.dyn, .rodata, .eh_frame_hdr, .eh_frame, .text, .init, .dynamic`')
s=s.replace('|all-changed-names.jsonl.gz / symbol-exceptions.tsv|全量名字变化和全部210条属性例外|','|all-changed-names.jsonl.gz / module-symbol-exceptions.tsv|全量名字变化和全部210条属性例外|').replace('|unexplained-ranges.jsonl.gz|未解释节的差异范围（也保留原始CRC差异行，最终结果看debuglink重判）|','|module-named-sections.json / module-named-summary.json|最终MODULE按名字对齐的完整差异范围、节头和符号记录|\n|unexplained-ranges.jsonl.gz|初次顺序遍历原始范围；MODULE以named结果为准，CRC以debuglink重判为准|')
s=s.replace('源码原件和git diff也随证据提交。','两边打包文件的SHA还分别与各自构建树的源码文件SHA完全相同；源码原件和git diff也随证据提交。')
old=(E/'item3-end.txt').read_text().strip();shutil.copyfile(E/'item3-end.txt',E/'item3-end-initial.txt');new='ITEM3 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status=partial reason=449-files-audited-module-byte-causality-unproven';(E/'item3-end.txt').write_text(new+'\n');s=s.replace(old,new)
(E/'df-final.txt').write_text(subprocess.check_output(['df','-B1','/home'],text=True))
p.write_text(s);print(new)
