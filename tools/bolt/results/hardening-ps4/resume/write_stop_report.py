from pathlib import Path
import json,datetime,hashlib
B=Path.cwd();E=B/'tools/bolt/results/hardening-ps4/resume';now=datetime.datetime.now().astimezone().isoformat()
s=json.loads((E/'stop.json').read_text());log=(E/'r3-r4-r5.log').read_text();failure=log[log.index('======================================================================'):]
text='''

## 96号续：PM范围裁决、实现与测试停止

**当前结论：实现已在独立游离工作树准备，测试83项运行、82 PASS、1 FAIL；按“任何失败STOP”停止，未创建产品提交、未推送sandbox。** 本节取代此前“缺评审原文”的待办状态，原STOP记录保留。

### 1. PM裁决与范围

评审原文未入库，以设计第18条为准。PM已核对仓库只有v8/v9摘要；本次以v9 §7.18及§6第一批上传后跟进为唯一依据，不再等待原文。今后原文若提供再补对照，不一致另行处理。本次四项细节采用PM补充，不增加第五项。

独立工作树：`W/temp/hardening-ps4-20261114/source`，detached HEAD仍为PS3 `ecb2dec72ec5afde9c6c70f166e2ac12b47c093e`，起始tree为`b2e8af2477cf623a945aa80bf8288a262dd4a5a9`。只有`packaging/llvm-static-archives-native.py`为未提交修改，未改llvm.spec。原工作树HEAD/status与本地分支未改变，见scope-preservation.json。

### 2. 实现（尚未提交产品）

[完整diff](../../tools/bolt/results/hardening-ps4/resume/product.diff)、[修改后全文](../../tools/bolt/results/hardening-ps4/resume/converter-after.py)。

- (a) 在现有压缩目标节使用`ch_size`前，保留24字节可读性检查，再拒绝type非1/2、addralign非0且非2幂。边界仍取声明的解压大小；不解压、不增加reserved字段规则。
- (b) 非NONE的零宽类型在`r_offset == limit`也拒绝，结合原有`>limit`实现严格节内；NONE逻辑不变。
- (c) 在成员全节检查中显式拒绝sh_type19，即使是空节也拒绝；CREL原规则不变。
- (d) 新增单行`NATIVE_ARCHIVES_STARTUP`，在install_main安装信号处理器前打印。包含spec已export的CFLAGS/CXXFLAGS中与现有packaging架构分类相同的`-m64/-march=/-mtune=/-msse*/-mfpmath=`参数，保留顺序和重复，便于按编译器最后选项语义读取；不新增原编译命令白名单，不修改转换flags。信号记录Python入口观察到的SIGTERM/SIGINT/SIGHUP状态（ignored/default/handler）；CPython默认SIGINT处理器会显示handler，不冒充内核原始sigaction快照。
- 日志只读取环境，不将这组参数重新注入编译器。畸形环境引号只在新增日志记parse_error，避免诊断改变已记录IR的转换行为；不会打印整份环境。旧日志行、汇总JSON字段及转换生成命令未编辑。单元测试验证去掉新增行后的模拟旧输出逐字节相同；尚未获得全量实物输出不变证明。

### 3. 测试来源、范围与结果

环境复制自78号已运行版本`W/temp/fifth-review-20261111/rerun3/environment`到本次新目录；只把被测源码路径换到独立工作树。历史目录只读，路径diff见证据；使用原run_preserved.py保留清理对象。未改既有测试输入或期望。四个既有套件为policy（含Source/v2基础夹具）、release、r2、R3/R4/R5；不运行独立helper全套或仅helper的cli套件。

R3.test_messages是旧三提交链/三个Change-Id的身份断言，不是转换器测试，与本次单独提交且不带Change-Id的授权冲突，因此在运行前明确列为不适用并排除；没有改其期望，也没有把它列入PASS。其余R3/R4/R5共40项全部排入，failfast执行。

|套件|计划|实际运行|PASS|FAIL|未运行|
|---|---:|---:|---:|---:|---:|
|新增加固正反例/日志|15|15|15|0|0|
|policy|46|46|46|0|0|
|release|5|5|5|0|0|
|r2|12|12|12|0|0|
|R3/R4/R5（排除旧身份1项）|40|5|4|1|35|
|合计|118|83|82|1|35|

新增15项覆盖：zlib/zstd、align0/1/2/8/2^63合法；type0/3/0xffffffff拒绝；短头、坏align拒绝；解压声明边界；TLSDESC_CALL节内通过/等于或越界拒绝（含压缩目标）；NONE任意offset原结果不变；RELR拒绝与普通REL(A)通过；继承架构参数、三种信号状态、空环境、畸形诊断环境非致命；CLI旧输出和返回码保持。subTest不另算测试数。

### 4. 停止原文与解释

失败来自旧R3.test_converter_sighup的**源码文本计数断言**：

```python
self.assertEqual(source.count('for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP)'),2)
self.command_probe('cancel-hup','hup')
```

原有两个处理器循环仍在；新增只读日志函数使用相同循环文本，使计数为3。断言在实际HUP探针之前失败，因此本次不能把该探针记为通过，也不是已经观察到信号行为错误。按规则不修改断言、不绕过、不修改产品代码后重跑；是否调整这项源码计数检查由PM决定。

```text
'''+failure+f'96测试 已结束 {s["time"]} status=STOP\n```\n'+'''
本次续跑准备修正0次。此前rg缺失的准备修正和范围STOP仍保留。四项实现与新测试无后续修改；没有把此FAIL当作可自修的准备错误。

### 5. 后续步骤状态与发布边界

- 步骤4提交说明、两份合并说明草稿：NOT RUN。没有产品提交SHA，没有产品commit/amend/squash。
- 步骤5sandbox：NOT RUN，未做ls-remote或push，前后SHA为NOT QUERIED；未向Gerrit查询或写入任何内容。
- 步骤6真实450归档＋10调试归档重放：NOT RUN，因为测试门禁失败；未检查空闲准入、未获取锁。不能写成PASS或准入SKIPPED。
- 当前不能声明sandbox领先Gerrit PS3一个提交。真实输入重放PASS之前不得触发QB。
- 仅本次证据提交推送B/bolt-v4；无RPM构建、无QB访问、未改现有LLVM分支或工作树。

### 6. 资源、已读与未读

续跑在独立串行用户服务MemoryMax4GiB、MemorySwapMax0、Nice19、IO idle内完成，属性见service-properties.txt。没有OOM或资源重试。

已读：PM补充、v9范围（此前已读）、PS3转换器和spec的架构参数分类/export位置、78号测试调用与实际脚本、选定测试的新结果、独立工作树diff及原工作区身份。未读第六轮原文（PM确认未入库），未访问QB/Gerrit/sandbox，未执行剩余35项或实物全量重放。

'''+f'96续 已结束 {now} status=STOP\n'
p=B/'docs/bolt/96_converter_hardening.md';old=p.read_text();p.write_text(old.replace('# 96号：转换器加固\n','# 96号：转换器加固\n\n> 最新停点见文末“96号续”：PM已解除原文前提；83项运行、82通过、1个源码计数断言失败，未推送sandbox。\n',1)+text)
with (B/'docs/bolt/STATUS.md').open('a') as f:f.write('''

### 96号续：PM范围裁决与测试停点

评审原文未入库，以设计v9第7节第18条及第6节为准，不再等待原文；原STOP保留，将来原文提供再补对照。本次已在独立detached工作树W/temp/hardening-ps4-20261114/source实现四项，只有转换器未提交修改，spec不变，原分支/工作树未改。

新增15/15通过；既有套件实际68项，67 PASS、1 FAIL；合计83项、82 PASS、1 FAIL，剩余35项未运行。R3.test_converter_sighup在源码中三个信号循环文本计数处失败（3 != 2），新增日志的只读遍历使计数多1，实际HUP探针尚未执行。按任何失败STOP，未改期望或重跑。

没有产品提交、说明草稿、sandbox查询/推送；真实输入重放NOT RUN（测试门禁未通过，不是准入SKIPPED）。不声明sandbox领先PS3；真实输入重放PASS之前不得触发QB。全部证据见96号续节，旧STOP保持。

'''+f'96续 已结束 {now} status=STOP\n')
url='https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/'
(E/'README.md').write_text('# 96号续证据索引\n\n[96号报告]('+url+'docs/bolt/96_converter_hardening.md)\n\n'+'\n'.join('- ['+p.name+']('+url+p.relative_to(B).as_posix()+')' for p in sorted(E.iterdir()) if p.is_file())+'\n')
print('96续 已结束',now,'status=STOP')
