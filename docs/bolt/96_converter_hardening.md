# 96号：转换器加固

> 最新停点见文末“96号续”：PM已解除原文前提；83项运行、82通过、1个源码计数断言失败，未推送sandbox。

**STOP，停在步骤1范围核对；没有产品修改、本地产品提交或sandbox推送。** 任务四项与设计v9摘要一致，但未找到第六轮评审原文，无法完成要求的逐条对应。这不是产品失败，也不是已经证实清单与原文不一致。

已向用户请求原文的本地或证据仓库路径。提供后可从范围核对继续；不能把本轮读到的设计摘要冒充评审原文。

## 1. 已读证据

- STATUS长期署名、远端授权、对外文本规则。
- 设计v9 §6第一批上传后的跟进（L565）、§7.18（L598）、风险中的复验要求（L604）；SHA及摘录见scope-design.json。
- 81号§6实际sandbox推送记录：完整SSH地址`ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm`，ref为`refs/heads/sandbox/lhmax2025/bolt_pgo`。本任务示例中省略sandbox前缀的ref不直接采用。
- 本地PS3对象ecb2dec72ec5afde9c6c70f166e2ac12b47c093e的转换器原文，只读导出为baseline-converter.py，查看pic_relocations与信号相关调用位置，没有修改LLVM文件。
- 85号已记录的加固NOT STARTED状态；78号既有测试环境和499项记录的索引，没有执行或沿用其测试结果作为本轮通过结论。

## 2. 原文定位范围与准备记录

检索了B已跟踪docs及tools/bolt/results中不超过200000字节的.md/.txt文本；用户附件与Downloads中不超过1000000字节的.md/.txt文本；并按文件名检查W的docs、temp中评审相关路径。命中设计v8/v9摘要、claims文档、第五轮任务附件；未定位第六轮评审原文。`scope-external-search.json`只保留相关命中的位置和摘录，没有把无关Downloads内容提交。

这不是全盘无原文的证明：没有检索所有大文件/压缩包/其他会话记录，也没有访问QB、Gerrit或远端文档。

首次使用rg报`rg: not found`，按长期规则修正一次为grep/find，原文与修正记录保留。最初跨docs/results递归搜索遍历时间较长，停止了本任务自己的服务，随后改为有文件类型/大小范围的只读搜索；没有终止其他任务。两次用户服务串行，均MemoryMax4GiB、swap0、Nice19、IO idle。未出现产品门禁失败。

## 3. 各步状态

|步骤|结论|
|---|---|
|1 范围|STOP：设计摘要匹配，评审原文未定位，逐条对应未完成|
|2 实现|NOT RUN；未创建游离工作树，未改转换器或spec|
|3 测试|NOT RUN；运行0项，不能称通过|
|4 提交说明/两版草稿|NOT RUN；没有本地产品提交或说明草稿|
|5 sandbox|NOT RUN；前后远端SHA未查询，无推送|
|6 真实输入重放|NOT RUN：前置步骤未通过，未进行空闲准入检查；不是机器准入SKIPPED或重放PASS|
|7 证据交付|仅交付停止记录到bolt-v4|

本轮没有使sandbox领先Gerrit PS3一个提交；不能写成已完成该状态。真实输入重放PASS之前不得触发QB。本轮也未访问QB。

## 4. STOP原文

```text
STOP: sixth-round review original text not located; cannot complete step 1 item-by-item correspondence. No product implementation, commit, tests, or sandbox push performed.
96步骤1 已结束 2026-11-14T03:28:37.828078-08:00 status=STOP
```

[证据索引](../../tools/bolt/results/hardening-ps4/README.md)。既有结果和历史构建根均未修改。


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
======================================================================
FAIL: test_converter_sighup (test_r3.R3.test_converter_sighup)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/linhao/Toolchain/development/llvm-optimize/temp/hardening-ps4-20261114/environment/test_r3.py", line 218, in test_converter_sighup
    self.assertEqual(source.count('for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP)'),2)
AssertionError: 3 != 2

----------------------------------------------------------------------
Ran 5 tests in 0.159s

FAILED (failures=1)
96测试 已结束 2026-11-14T03:38:14.706197-08:00 status=STOP
```

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

96续 已结束 2026-11-14T03:39:46.459382-08:00 status=STOP


### 7. 证据发布补记

首次交付git add因*.log忽略规则未收5份原始测试日志并返回1；交互shell仍继续提交其余32文件为0f9431ec8ed74f11f0dc5572bd8f35f6ec828249。交付准备修正一次：显式git add -f补交这5份日志，核对暂存清单和单文件大小；后续命令以check=True衔接，保留原提交不重写。错误关键原文和修改记录见publication-error.txt/publication-fix.diff。产品测试FAIL保持不变，未改代码或重跑。
