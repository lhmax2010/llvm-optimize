# PS10→fea0fe46：forbidden全路径核对

读取两个git对象的完整pic_relocations、ir_settings及所有process调用点；逐行快照见ps10-full-paths.txt、fea-full-paths.txt；未运行归档转换或构建。192个合法内存ELF组合（kind=1/10/11；目标节标志0/WRITE/ALLOC/ALLOC|WRITE；重定位节同样4种标志；SHN_ABS/普通符号；REL/RELA）直接调用两版函数，返回checked和forbidden完全一致。pic_level=0/1/2与原生成员分支另外按原代码逐项核对。不是所有输入接受集合相同的证明。

|环节|PS10行|fea行|结论|
|---|---|---|---|
|ELF64 LE、ET_REL、x86_64入口|355–356|481–483|同一有效输入域；fea增加短文件/表结构检查|
|REL/RELA|364–365|500–501|处理SHT_RELA=4、SHT_REL=9；重定位节自身SHF_ALLOC/WRITE均非PIC过滤依据|
|目标节ALLOC|366–368|504、529–530|两版均过滤非ALLOC目标，PS10在节循环外层，fea在逐条结构检查之后|
|目标节WRITE|376|533|只影响kind=1(64位)：WRITE则不加入forbidden；kind10/11无此例外|
|SHN_ABS|373、376|528、533|st_shndx==0xfff1不加入forbidden|
|类型集合|376|533|PS10(10,11)，fea(10,11,12,14)；新增12/14为16/8位|
|PIC来源|324–326|354–356|PIC/PIE值0/1/2及组合一致；生成flags见340–341/375–376|
|原生machine成员|652–658|850–856|检查/记录relocations；不以forbidden非空报错，与pic_level无关|
|转换成员|670–673|868–871|仅settings.pic_level非零且forbidden非空，抛non-PIC relocation|
|其他门禁|668–669|866–867|release调试节检查相同；fea另有声明debug-info一致性，不混作PIC条件|

有效条件：target.ALLOC && symbol!=SHN_ABS && (kind为32/32S，或kind为64且target非WRITE)。kind=1/10/11的PIC禁止路径等价；转换成员pic_level非零时该门禁报错条件相同。原生成员仅记录；解析错误仍可能使其失败，不能写“原生成员从不拒绝”。

**校验域有意加固，不可称整个函数等价：** PS10跳过CREL/其他非REL/RELA节，对表外类型没有显式拒绝；fea495–496拒绝CREL，522–523拒绝宽度表外类型（七种动态专用类型未登记），并在ALLOC过滤前检查索引、记录大小、r_offset及目标解压声明大小。PS10可跳过的畸形非ALLOC记录，fea也可能先报结构错误。NONE偏移例外见fea524；压缩目标见506–509。上述是解析/认证加固，不是32/32S/64 PIC政策收窄或放宽。有效合法表结构/类型域内，192组合无差异。

句4“retain the existing 32- and 64-bit PIC checks”准确，需按转换成员PIC政策理解，不是旧版对任意畸形输入的接受行为全部保留。85要求整条类型集合相等的STOP正确，PM已明确该前提错误；本次不计准备错误。因有效PIC路径等价，不触发“不等价时查询真实命中”的分支；本次没有重新扫描78/79实物归档。
