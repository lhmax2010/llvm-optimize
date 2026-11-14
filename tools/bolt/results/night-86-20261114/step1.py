import pathlib,ast,struct,itertools,json,datetime,difflib,hashlib
E=pathlib.Path(__file__).resolve().parent;B=E.parents[3]
mods={};texts={}
for tag in ['ps10','fea']:
 t=(E/(tag+'-converter.py.txt')).read_text();texts[tag]=t;ns={'__name__':'readonly_'+tag};exec(compile(t,tag,'exec'),ns);mods[tag]=ns
 lines=t.splitlines();tree=ast.parse(t);chunks=[]
 for f in ast.walk(tree):
  if isinstance(f,ast.FunctionDef) and (f.name in ('pic_relocations','ir_settings') or f.name=='process'):
   chunks.append('\n'.join(str(i)+': '+lines[i-1] for i in range(f.lineno,f.end_lineno+1)))
 (E/(tag+'-full-paths.txt')).write_text('\n\n'.join(chunks)+'\n')
def elf(k,tf,rf,absolute,reltype):
 b=bytearray(512);b[:16]=b'\x7fELF\x02\x01\x01'+b'\0'*9
 struct.pack_into('<HHIQQQIHHHHHH',b,16,1,62,1,0,0,256,0,64,0,0,64,4,0)
 struct.pack_into('<IBBHQQ',b,152,0,0x10,0,0xfff1 if absolute else 1,0,8)
 if reltype==4:struct.pack_into('<QQq',b,192,0,(1<<32)|k,0)
 else:struct.pack_into('<QQ',b,192,0,(1<<32)|k)
 secs=[(0,0,0,0,0,0,0,0,0,0),(0,1,tf,0,64,64,0,0,8,0),(0,2,0,0,128,48,0,0,8,24),(0,reltype,rf,0,192,24 if reltype==4 else 16,2,1,8,24 if reltype==4 else 16)]
 for i,s in enumerate(secs):struct.pack_into('<IIQQQQIIQQ',b,256+i*64,*s)
 return bytes(b)
rows=[]
for k,tf,rf,ab,rt in itertools.product([1,10,11],range(4),range(4),[False,True],[4,9]):
 b=elf(k,tf,rf,ab,rt);old=mods['ps10']['pic_relocations'](b);new=mods['fea']['pic_relocations'](b)
 expected=bool(tf&2 and not ab and (k in (10,11) or (k==1 and not tf&1)))
 assert old==new,(k,tf,rf,ab,rt,old,new)
 assert bool(old['forbidden'])==expected
 rows.append(dict(kind=k,target_flags=tf,relocation_section_flags=rf,SHN_ABS=ab,section_type=rt,old=old,new=new,converted_gate={str(pic):bool(pic and expected) for pic in (0,1,2)},native_forbidden_gate=False))
(E/'pic-path-matrix.json').write_text(json.dumps(rows,indent=2)+'\n')
msg='''# PS10→fea0fe46：forbidden全路径核对

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
'''
(E/'claims-path-review.md').write_text(msg)
p=B/'tools/bolt/results/qb-1226850-1226851/commit-message-drafts/0003-claims-to-code.md'
old=p.read_text();assert '补充（2026-11-14）' not in old
needle='32/64位条件与60fabc72逐字相同。'
assert old.count(needle)==1
new=old.replace(needle,needle+'\n\n相对上传父提交 PS10 的对照见文末补充。')
assert '## “既有32/64位检查”的历史对照' in new
# This is the last section in the existing document.
pos=new.index('## “既有32/64位检查”的历史对照');assert '\n## ' not in new[pos+4:]
new+='\n\n补充（2026-11-14）：上传链的父提交是 PS10（13c3e223），不是 60fabc72；60fabc72 已含本系列新增的 8/16 位类型，上面的对照只说明本系列内部未变。PS10 第376行的类型集合为 (10, 11)，fea0fe46 第533行为 (10, 11, 12, 14)；新增的 12/14 即 R_X86_64_16/R_X86_64_8。到达该判断前的过滤条件逐项对照见[全路径复核证据](../../night-86-20261114/claims-path-review.md)，32、32S、64 位三条路径的有效条件与 PS10 等价。结论不变：句4与代码相符。\n'
(E/'claims-before.md').write_text(old)
(E/'claims-addition.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='before',tofile='after')))
p.write_text(new)
result=dict(status='PASS',matrix_cases=len(rows),policy_equal=True,validator_acceptance_equal=False,claims_modified=True,time=datetime.datetime.now().astimezone().isoformat(),original_sha256=hashlib.sha256(old.encode()).hexdigest(),new_sha256=hashlib.sha256(new.encode()).hexdigest())
(E/'step1-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(result);print('86步骤1 已结束 '+result['time']+' status=PASS')
