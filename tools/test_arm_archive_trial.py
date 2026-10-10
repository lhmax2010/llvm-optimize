#!/usr/bin/env python3
"""ARM policy draft fixtures and x86 dispatch invariance; no package builds."""
import ast
import importlib.util
from pathlib import Path
import struct
import unittest
from unittest import mock
import llvm_static_archives_arm_trial as trial


# Independent ELF fixture: NULL, target, symbols, relocations, strings, names.
def reloc_elf(arch, kinds, writable=False, absolute=False, debug=False, rela=None,
              extended=False, xindex=None, symbol_name='external', mapping=None):
    bits,machine=(1,40) if arch=='armv7l' else (2,183)
    hs,ss,symsz=(52,40,16) if bits==1 else (64,64,24)
    sfmt='<IIIIIIIIII' if bits==1 else '<IIQQQQIIQQ'
    rela=(bits==2) if rela is None else rela
    sections=[[0]*10 for _ in range(6)]
    payloads={1:b'\0'*max(64,len(kinds)*4)}
    strings=bytearray(b'\0'); symbols=[(0,0,0,0,0,0)]
    def symbol(name,info,ndx,value=0):
        no=len(strings);strings.extend(name.encode()+b'\0');symbols.append((no,value,0,info,0,ndx))
    symbol(symbol_name,0x10,0xffff if xindex is not None else 0xfff1 if absolute else 1)
    if mapping is not None:
        for section_name,entries in mapping:
            idx=len(sections);sections.append([0,1,6,0,0,64,0,0,1,0]);payloads[idx]=b'\0'*64
            for value,name in entries:symbol(name,0,idx,value)
    payloads[2]=b''.join(struct.pack('<IIIBBH',*x) if bits==1 else struct.pack('<IBBHQQ',x[0],x[3],x[4],x[5],x[1],x[2]) for x in symbols)
    rf=('<IIi' if rela else '<II') if bits==1 else ('<QQq' if rela else '<QQ')
    payloads[3]=b''.join(struct.pack(rf,*([i*4,(1<<8)|k] if bits==1 else [i*4,(1<<32)|k]),*([0] if rela else [])) for i,k in enumerate(kinds))
    payloads[4]=bytes(strings)
    names=bytearray(b'\0');sec_names=['','.text','.symtab','.reloc','.strtab','.shstrtab']
    if mapping is not None:sec_names.extend(x[0] for x in mapping)
    if xindex is not None:
        while len(sections)<=xindex:sections.append([0]*10);sec_names.append('')
        ei=len(sections);sections.append([0,18,0,0,0,len(symbols)*4,2,0,4,4]);sec_names.append('.symtab_shndx')
        payloads[ei]=struct.pack('<'+'I'*len(symbols),0,xindex,*([0]*(len(symbols)-2)))
    for sec,name in zip(sections,sec_names):
        sec[0]=len(names);names.extend(name.encode()+b'\0')
    sections[0][0]=0
    payloads[5]=bytes(names)
    sections[1][1:]=[1,0 if debug else 2|int(writable),0,0,len(payloads[1]),0,0,1,0]
    sections[2][1:]=[2,0,0,0,len(payloads[2]),4,1,4,symsz]
    sections[3][1:]=[4 if rela else 9,0,0,0,len(payloads[3]),2,1,4,struct.calcsize(rf)]
    sections[4][1:]=[3,0,0,0,len(payloads[4]),0,0,1,0]
    sections[5][1:]=[3,0,0,0,len(payloads[5]),0,0,1,0]
    off=hs+len(sections)*ss;parts=[]
    for idx,payload in sorted(payloads.items()):sections[idx][4]=off;parts.append(payload);off+=len(payload)
    count=len(sections)
    use_ext=extended or count>=0xff00
    if use_ext:sections[0][5]=count;sections[0][6]=5
    ident=b'\x7fELF'+bytes([bits,1,1])+b'\0'*9
    args=(1,machine,1,0,0,hs,0,hs,0,0,ss,0 if use_ext else count,0xffff if use_ext else 5)
    hdr=struct.pack('<HHIIIIIHHHHHH' if bits==1 else '<HHIQQQIHHHHHH',*args)
    return ident+hdr+b''.join(struct.pack(sfmt,*x) for x in sections)+b''.join(parts)


def change_section(data,index,field,value):
    data=bytearray(data);bits=data[4];hs,ss=(52,40) if bits==1 else (64,64)
    fmt='<IIIIIIIIII' if bits==1 else '<IIQQQQIIQQ'
    fields=list(struct.unpack_from(fmt,data,hs+index*ss));fields[field]=value
    struct.pack_into(fmt,data,hs+index*ss,*fields);return bytes(data)


TLS_ALLOW={'armv7l':{104,105,106},'aarch64':{562,563,564,569}}
TLS_LE={'armv7l':{108,110},'aarch64':{544,545,546,547,548,549,550,551,552,553,554,555,556,557,558,559,570,571}}
TLS_STOP={'armv7l':{13,17,18,19,90,91,92,93,107,109,111,129,130,165,166,167},
'aarch64':{512,513,514,515,516,517,518,519,520,521,522,523,524,525,526,527,528,529,530,531,532,533,534,535,536,537,538,539,540,541,542,543,560,561,565,566,567,568,572,573}}
TARGETS={
'armv7l':('generic','+armv7-a,+d32,+dsp,+fp64,+neon,+read-tp-tpidruro,+thumb-mode,+vfp2,+vfp2sp,+vfp3,+vfp3d16,+vfp3d16sp,+vfp3sp,-aes,-fp-armv8,-fp-armv8d16,-fp-armv8d16sp,-fp-armv8sp,-fp16,-fp16fml,-fullfp16,-sha2,-vfp4,-vfp4d16,-vfp4d16sp,-vfp4sp',None),
'aarch64':('generic','+aes,+crc,+crypto,+fp-armv8,+neon,+outline-atomics,+sha2,+v8a,-fmv','cortex-a53')}


def target_ir(arch,values=None):
    values=TARGETS[arch] if values is None else values
    attrs=' '.join('"'+key+'"="'+value+'"' for key,value in zip(('target-cpu','target-features','tune-cpu'),values) if value is not None)
    return ['define void @f() #0 {','ret void','}','attributes #0 = { '+attrs+' }']


class DispatchTests(unittest.TestCase):
    def test_original_functions_are_identical(self):
        def defs(path):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(path.read_text()).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
        old=defs(Path(trial.__file__).with_name('llvm_static_archives_source.py'));new=defs(Path(trial.__file__))
        for name in old:
            if name not in ('convert','install_main'):
                self.assertEqual(old[name],new[name],name)

    def test_x86_never_reaches_arm(self):
        with mock.patch.object(trial,'arm_ir_settings',side_effect=AssertionError('ARM reached')),mock.patch.object(trial,'arm_pic_relocations',side_effect=AssertionError('ARM reached')):
            p=trial.policy_for_arch('x86_64')
            self.assertIs(p['relocations'],trial.pic_relocations)
            from test_static_archives_source_v2 import module
            self.assertEqual(p['settings'](module()),trial.ir_settings(module()))
        with self.assertRaises(ValueError):trial.policy_for_arch('riscv64')

    def test_arm_exact_options_and_cross_target_rejection(self):
        common=['clang','-gdwarf-4','-ffunction-sections','-fdata-sections','-flto=thin','-fstack-protector']
        for arch,opt in trial.ARM_OPTIMIZATION.items():
            argv=common+[opt]+sorted(trial.ARM_EXACT_TOKENS[arch])
            self.assertEqual(trial.arm_classify_options(argv,arch)['optimization'],opt)
            for bad in ('-mcpu=cortex-a9','-marm','-mfloat-abi=hard','--target=x86_64-tizen-linux-gnu','-fno-unroll-loops'):
                with self.subTest(arch=arch,bad=bad),self.assertRaises(ValueError):trial.arm_classify_options(argv+[bad],arch)

    def test_arm_ir_and_explicit_abi(self):
        for arch,opt in trial.ARM_OPTIMIZATION.items():
            flags=['clang',opt,'-gdwarf-4','-ffunction-sections','-fdata-sections']+sorted(trial.ARM_EXACT_TOKENS[arch])
            text='target triple = "'+next(iter(trial.ARM_IR_TRIPLES[arch]))+'"\n!llvm.commandline = !{!0}\n!0 = !{!"'+' '.join(flags)+'"}\n!1 = !{i32 8, !"PIC Level", i32 2}\n'
            r=trial.policy_for_arch(arch)['settings'](text.splitlines(True))
            self.assertEqual(r['pic_level'],2);self.assertIn(opt,r['flags']);self.assertNotIn('-flto=thin',r['flags'])
            if arch=='armv7l':self.assertIn('-mfloat-abi=softfp',r['flags'])
            with self.assertRaisesRegex(ValueError,'type metadata'):
                trial.arm_ir_settings((text+'declare i1 @llvm.type.test(ptr, metadata)\n').splitlines(True),arch)

    def test_arm_pic_rel_and_aarch64_rela(self):
        for arch,absrel,safe in [('armv7l',2,[24,26,27,42]),('aarch64',0x101,[0x113,0x115,0x137,0x138])]:
            self.assertTrue(trial.arm_pic_relocations(reloc_elf(arch,[absrel]),arch)['forbidden'])
            for data in (reloc_elf(arch,[absrel],absolute=True),reloc_elf(arch,[absrel],writable=True),reloc_elf(arch,[absrel],debug=True),reloc_elf(arch,safe)):
                self.assertFalse(trial.arm_pic_relocations(data,arch)['forbidden'])
            with self.assertRaisesRegex(ValueError,'uncertified'):
                trial.arm_pic_relocations(reloc_elf(arch,[255]),arch)

    def test_narrow_absolute_writable_rejected(self):
        for arch,kind in [('armv7l',5),('aarch64',0x102)]:
            self.assertTrue(trial.arm_pic_relocations(reloc_elf(arch,[kind],writable=True),arch)['forbidden'])

class TLSThumbTests(unittest.TestCase):
    def test_tls_allowed_each_type_readonly_and_writable(self):
        for arch, kinds in TLS_ALLOW.items():
            for kind in sorted(kinds):
                for writable in (False, True):
                    with self.subTest(arch=arch, kind=kind, writable=writable):
                        self.assertFalse(trial.arm_pic_relocations(reloc_elf(arch,[kind],writable=writable),arch)['forbidden'])

    def test_local_exec_forbidden_even_debug_writable_and_absolute(self):
        for arch, kinds in TLS_LE.items():
            for kind in sorted(kinds):
                for kwargs in ({}, {'writable':True}, {'debug':True}, {'absolute':True}):
                    with self.subTest(arch=arch, kind=kind, kwargs=kwargs),self.assertRaisesRegex(ValueError,'forbidden .* TLS local-exec'):
                        trial.arm_pic_relocations(reloc_elf(arch,[kind],**kwargs),arch)

    def test_initial_exec_arm_descriptors_and_unknown_stop(self):
        for arch, kinds in TLS_STOP.items():
            for kind in sorted(kinds):
                for debug in (False,True):
                    with self.subTest(arch=arch, kind=kind),self.assertRaisesRegex(ValueError,'uncertified'):
                        trial.arm_pic_relocations(reloc_elf(arch,[kind],debug=debug),arch)
        for arch,kind in [('armv7l',41),('aarch64',0x253)]:
            with self.assertRaisesRegex(ValueError,'uncertified'):
                trial.arm_pic_relocations(reloc_elf(arch,[kind]),arch)

    def test_thumb_restore_and_reference_arguments(self):
        argv=['clang','-Os','-gdwarf-4','-ffunction-sections','-fdata-sections',*sorted(trial.ARM_EXACT_TOKENS['armv7l']),'-flto=thin','-D','NAME.cpp','-I','path','-MT','target','-MF','deps','-MD','-o','a.o','-c','a.cpp']
        policy=trial.arm_classify_options(argv,'armv7l')
        self.assertEqual(next(x['category'] for x in policy['tokens'] if x['token']=='-mthumb'),'restore')
        ref=trial.arm_reference_flags({'recorded_command':argv})
        self.assertIn('-mthumb',ref);self.assertIn('NAME.cpp',ref)
        for x in ['-flto=thin','a.cpp','a.o','-MD','deps','target']:self.assertNotIn(x,ref)
        text=['target triple = "thumbv7-tizen-linux-gnueabi"','!llvm.commandline = !{!0}','!0 = !{!"'+' '.join(argv)+'"}']
        self.assertIn('-mthumb',trial.arm_ir_settings(text,'armv7l')['flags'])
        with self.assertRaisesRegex(ValueError,'reference driver'):
            trial.arm_reference_flags({'recorded_command':[x for x in argv if x!='-mthumb']})

    def test_override_warning_is_a_failure(self):
        trial.arm_reject_triple_override({'stderr':''})
        for message in ['[-Woverride-module]','warning: overriding the module target triple with armv7']:
            with self.assertRaisesRegex(ValueError,'changed module target triple'):
                trial.arm_reject_triple_override({'stderr':message})

    def test_module_asm_section_tracking(self):
        lines=['module asm ".text"','module asm ".thumb"','module asm ".pushsection .text.helper,\\22ax\\22"','module asm "nop"','module asm ".popsection"']
        self.assertEqual(trial.arm_module_asm_sections(lines),['.text','.text.helper'])
        self.assertEqual(trial.arm_module_asm_sections([]),[])
        with self.assertRaisesRegex(ValueError,'unbalanced'):
            trial.arm_module_asm_sections(['module asm ".popsection"'])

    def test_thumb_gate_rejects_attribute_mismatch(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);src=root/'input.bc';src.write_bytes(b'bc');target=root/'actual.o';target.write_bytes(b'obj')
            def run(argv,prefix,stdout=None):
                if stdout is not None:
                    stdout.write(b'Attribute Section: aeabi\n  Tag_CPU_arch: v7\n  Tag_THUMB_ISA_use: Thumb-2\n' if 'actual.o' in argv[-1] else b'Attribute Section: aeabi\n  Tag_CPU_arch: v7\n  Tag_THUMB_ISA_use: Thumb-1\n')
                else:Path(argv[-1]).write_bytes(b'reference')
                return {'stderr':''}
            with mock.patch.object(trial,'arm_reference_flags',return_value=['-mthumb']),mock.patch.object(trial,'arm_mapping_modes',return_value={}):
                with self.assertRaisesRegex(ValueError,'Thumb/ABI/module-asm'):
                    trial.arm_thumb_gate('clang',src,target,{'module_asm_sections':[],'target_cpu':[],'target_features':[]},mock.Mock(run=run))



class ReviewRelocationTests(unittest.TestCase):
    def test_tls_literal_sets_and_disjointness(self):
        self.assertEqual(trial.ARM_TLS_ALLOWED,TLS_ALLOW)
        self.assertEqual(trial.ARM_TLS_LOCAL_EXEC,TLS_LE)
        self.assertEqual(trial.ARM_TLS_PENDING,TLS_STOP)
        tree=ast.parse(Path(trial.__file__).read_text())
        fun=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='arm_pic_relocations')
        branches=next(n for n in fun.body if isinstance(n,ast.If))
        for arch,branch in [('armv7l',branches.body),('aarch64',branches.orelse)]:
            scope={'set':set,'range':range}
            for node in branch:
                if isinstance(node,ast.Assign) and node.targets[0].id in ('absolute','allowed','narrow'):
                    scope[node.targets[0].id]=eval(compile(ast.Expression(node.value),'fixture','eval'),scope)
            self.assertLessEqual(scope['narrow'],scope['absolute'])
            for a,b in ((TLS_ALLOW[arch],TLS_LE[arch]),(TLS_ALLOW[arch],TLS_STOP[arch]),(TLS_LE[arch],TLS_STOP[arch])):self.assertFalse(a & b)
            for kinds in (TLS_ALLOW[arch],TLS_LE[arch],TLS_STOP[arch]):self.assertFalse(kinds & (scope['absolute']|scope['allowed']))

    def test_tls_boundary_numbers(self):
        for number,outcome in [(538,'stop'),(539,'stop'),(559,'le'),(560,'stop'),(561,'stop'),(562,'allow'),(569,'allow'),(570,'le'),(571,'le'),(572,'stop')]:
            with self.subTest(number=number):
                if outcome=='allow':self.assertEqual(trial.arm_pic_relocations(reloc_elf('aarch64',[number]),'aarch64')['checked'],1)
                else:
                    with self.assertRaisesRegex(ValueError,'local-exec' if outcome=='le' else 'uncertified'):trial.arm_pic_relocations(reloc_elf('aarch64',[number]),'aarch64')

    def test_removed_tls_and_invalid_constants_in_all_contexts(self):
        removed=[512,513,514,515,516,517,518,519,520,521,522,523,524,525,526,527,528,529,530,531,532,533,534,535,536,537,538,560,561,565,566,567,568,572,573,256,317,580]
        for kind in removed:
            for context in ({},{'debug':True},{'absolute':True}):
                with self.subTest(kind=kind,context=context),self.assertRaisesRegex(ValueError,'uncertified'):
                    trial.arm_pic_relocations(reloc_elf('aarch64',[kind],**context),'aarch64')

    def test_nonalloc_known_not_counted_unknown_rejected(self):
        for arch,kind in [('armv7l',104),('aarch64',562)]:
            result=trial.arm_pic_relocations(reloc_elf(arch,[kind],debug=True),arch)
            self.assertEqual((result['checked'],result['types']),(0,{}))
            with self.assertRaisesRegex(ValueError,'uncertified'):trial.arm_pic_relocations(reloc_elf(arch,[255],debug=True),arch)

    def test_writable_instruction_absolute_vs_pointer(self):
        for arch,instructions,pointers in [('armv7l',[43,44,47,48,132,133,134,135],[2,38,55]),('aarch64',[263,264,265,266,267,268,269,270,271,272],[257])]:
            for kind in instructions:self.assertTrue(trial.arm_pic_relocations(reloc_elf(arch,[kind],writable=True),arch)['forbidden'])
            for kind in pointers:self.assertFalse(trial.arm_pic_relocations(reloc_elf(arch,[kind],writable=True),arch)['forbidden'])
        self.assertTrue(trial.arm_pic_relocations(reloc_elf('armv7l',[38]),'armv7l')['forbidden'])

class LayoutTests(unittest.TestCase):
    def test_rel_rela_architecture_matrix(self):
        for arch,kind in [('armv7l',104),('aarch64',562)]:
            for rela in (False,True):
                with self.subTest(arch=arch,rela=rela):self.assertEqual(trial.arm_pic_relocations(reloc_elf(arch,[kind],rela=rela),arch)['checked'],1)

    def test_extended_count_names_and_symbol_index(self):
        for arch,kind in [('armv7l',2),('aarch64',257)]:
            data=reloc_elf(arch,[kind],extended=True,xindex=1)
            layout=trial.arm_elf_layout(data,arch)
            self.assertEqual(layout['section_names'][1],'.text')
            self.assertEqual(layout['symbols'][2][1]['section_index'],1)
            self.assertTrue(trial.arm_pic_relocations(data,arch)['forbidden'])

    def test_decoded_65521_is_real_section_not_absolute(self):
        for arch,kind in [('armv7l',2),('aarch64',257)]:
            data=reloc_elf(arch,[kind],xindex=65521)
            self.assertFalse(trial.arm_elf_layout(data,arch)['symbols'][2][1]['is_absolute'])
            self.assertTrue(trial.arm_pic_relocations(data,arch)['forbidden'])
            self.assertFalse(trial.arm_pic_relocations(reloc_elf(arch,[kind],absolute=True),arch)['forbidden'])

    def test_missing_duplicate_badcount_extended_indexes(self):
        for arch in ('armv7l','aarch64'):
            data=reloc_elf(arch,[0],xindex=1)
            broken=[change_section(data,6,1,1),change_section(change_section(data,6,5,4),6,9,4)]
            # Make relocation section a second valid-shaped extension pointing at symtab.
            dup=data
            for field,value in ((1,18),(6,2),(9,4)):dup=change_section(dup,3,field,value)
            broken.append(dup)
            for blob in broken:
                with self.subTest(arch=arch),self.assertRaises(ValueError):trial.arm_elf_layout(blob,arch)

    def test_invalid_links_tables_payloads_and_truncation(self):
        for arch in ('armv7l','aarch64'):
            data=reloc_elf(arch,[0])
            blobs=[data[:8],data[:100],data[:-1]]
            for index,field,value in [(2,6,0),(2,6,900),(2,7,900),(3,6,900),(3,7,900),(1,4,len(data)+1),(1,5,len(data)+1),(2,9,1),(3,9,1),(5,1,1)]:blobs.append(change_section(data,index,field,value))
            for blob in blobs:
                with self.subTest(arch=arch),self.assertRaises(ValueError):trial.arm_elf_layout(blob,arch)

    def test_relocation_offset_and_symbol_boundaries(self):
        for arch in ('armv7l','aarch64'):
            data=reloc_elf(arch,[0]);layout=trial.arm_elf_layout(data,arch);off=layout['sections'][3][4]
            for bad_offset in (64,65):
                blob=bytearray(data);struct.pack_into('<I' if arch=='armv7l' else '<Q',blob,off,bad_offset)
                with self.assertRaisesRegex(ValueError,'offset outside'):trial.arm_elf_layout(blob,arch)
            blob=bytearray(data);struct.pack_into('<I' if arch=='armv7l' else '<Q',blob,off+(4 if arch=='armv7l' else 8),99<<(8 if arch=='armv7l' else 32))
            with self.assertRaisesRegex(ValueError,'symbol outside'):trial.arm_elf_layout(blob,arch)

class MappingReaderTests(unittest.TestCase):
    def test_mapping_thumb_only(self):
        data=reloc_elf('armv7l',[],mapping=[('.asm',[(0,'$t')])])
        self.assertEqual(trial.arm_mapping_modes(data,['.asm']),{'.asm':[['t']]})

    def test_mapping_transition_deduplicated(self):
        data=reloc_elf('armv7l',[],mapping=[('.asm',[(0,'$t'),(4,'$t.1'),(8,'$a'),(12,'$a.2')])])
        self.assertEqual(trial.arm_mapping_modes(data,['.asm']),{'.asm':[['t','a']]})

    def test_mapping_duplicate_section_names_preserved(self):
        data=reloc_elf('armv7l',[],mapping=[('.asm',[(0,'$t')]),('.asm',[(0,'$a')])])
        self.assertEqual(trial.arm_mapping_modes(data,['.asm']),{'.asm':[['t'],['a']]})

    def test_mapping_missing_and_out_of_bounds_rejected(self):
        for mapping in ([('.asm',[])],[('.asm',[(64,'$t')])]):
            with self.assertRaises(ValueError):trial.arm_mapping_modes(reloc_elf('armv7l',[],mapping=mapping),['.asm'])

    def test_reader_empty_no_aeabi_and_bad_format_rejected(self):
        for text in ('','Tag_CPU_arch: v7\n','Attribute Section: aeabi\n','Attribute Section: aeabi\nTag_CPU_arch = v7\n','Attribute Section: aeabi\nTag_CPU_arch: \n'):
            with self.assertRaises(ValueError):trial.arm_attributes(text)

    def test_missing_differs_from_zero_and_missing_vfp_valid(self):
        base='Attribute Section: aeabi\nTag_CPU_arch: v7\n'
        missing=trial.arm_attributes(base);zero=trial.arm_attributes(base+'Tag_ARM_ISA_use: 0\n')
        self.assertIsNone(missing['Tag_ARM_ISA_use']);self.assertIsNone(missing['Tag_ABI_VFP_args'])
        self.assertEqual(zero['Tag_ARM_ISA_use'],'0');self.assertNotEqual(missing,zero)

class TargetModuleTests(unittest.TestCase):
    def test_certified_function_targets_and_data_modules(self):
        self.assertEqual(trial.ARM_CERTIFIED_FUNCTION_TARGET,TARGETS)
        for arch in TARGETS:
            self.assertEqual(trial.arm_function_targets(target_ir(arch),arch)['definitions'],1)
            self.assertEqual(trial.arm_function_targets(['@x = global i32 0'],arch)['definitions'],0)

    def test_cpu_features_tune_and_missing_groups_rejected(self):
        for arch,(cpu,features,tune) in TARGETS.items():
            variants=[('cortex-a15',features,tune),(cpu,features.split(',',1)[1],tune),(cpu,features+',+extra',tune),(None,features,tune),(cpu,None,tune),(cpu,features,'cortex-a72')]
            for values in variants:
                with self.subTest(arch=arch,values=values),self.assertRaises(ValueError):trial.arm_function_targets(target_ir(arch,values),arch)
            for text in (['define void @f() {'],['define void @f() #99 {'],['define void @f() #0 {','attributes #0 = { nounwind }']):
                with self.assertRaises(ValueError):trial.arm_function_targets(text,arch)

    def test_real_command_literals_and_assembler_escape(self):
        commands={'armv7l':['clang++','-Os','-gdwarf-4','-ffunction-sections','-fdata-sections','-mthumb','-march=armv7-a','-mfpu=neon','-mfloat-abi=softfp','-mlittle-endian','-mtune=cortex-a8'],
                  'aarch64':['clang++','-O3','-gdwarf-4','-ffunction-sections','-fdata-sections','-march=armv8-a+fp+simd+crc+crypto','-mtune=cortex-a53']}
        for arch,argv in commands.items():
            self.assertEqual(len(trial.arm_classify_options(argv,arch)['tokens']),len(argv))
            for suffix in (['-Wa,-defsym'],['-march','armv7-a']):
                with self.assertRaisesRegex(ValueError,'unclassified'):trial.arm_classify_options(argv+suffix,arch)

    def test_module_asm_exact_and_whitespace_only(self):
        self.assertEqual(trial.ARM_CERTIFIED_MODULE_ASM,{'.globl _ZSt21ios_base_library_initv'})
        for value in ('.globl _ZSt21ios_base_library_initv','  .globl _ZSt21ios_base_library_initv  ','\\09.globl _ZSt21ios_base_library_initv\\0A'):
            self.assertEqual(trial.arm_module_asm_whitelist(['module asm "'+value+'"']),['.globl _ZSt21ios_base_library_initv'])
        for arch in ('armv7l','aarch64'):
            self.assertTrue(trial.arm_check_module_asm_symbol(reloc_elf(arch,[],symbol_name='_ZSt21ios_base_library_initv'),arch,['.globl _ZSt21ios_base_library_initv'])['required'])

    def test_module_asm_all_other_statements_rejected(self):
        for value in ('.globl other','.global _ZSt21ios_base_library_initv','.globl _ZSt21ios_base_library_initv;', '.globl _ZSt21ios_base_library_initv; nop','.globl _ZSt21ios_base_library_initv #comment','.text','.section .text','.globl  _ZSt21ios_base_library_initv',''):
            with self.subTest(value=value),self.assertRaisesRegex(ValueError,'module asm'):trial.arm_module_asm_whitelist(['module asm "'+value+'"'])

    def test_module_asm_output_global_symbol_required(self):
        for arch in ('armv7l','aarch64'):
            with self.assertRaisesRegex(ValueError,'global symbol missing'):trial.arm_check_module_asm_symbol(reloc_elf(arch,[]),arch,['.globl _ZSt21ios_base_library_initv'])
            self.assertEqual(trial.arm_check_module_asm_symbol(b'',arch,[]),{'required':False})

class ToolIsolationTests(unittest.TestCase):
    def run_tools(self,arch,dis='22.1.8',nm='22.1.8',reader='GNU readelf (GNU Binutils) 2.43\n'):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'CMakeCache.txt').touch()
            cc=p/'clang';di=p/'llvm-dis';nn=p/'llvm-nm'
            for tool in (cc,di,nn):tool.write_text('fixture');tool.chmod(0o755)
            command=mock.Mock()
            def run(argv,prefix,stdout):
                name=Path(argv[0]).name
                raw='clang version 22.1.8\n' if name=='clang' else 'LLVM version '+(dis if name=='llvm-dis' else nm)+'\n' if name in ('llvm-dis','llvm-nm') else reader
                stdout.write(raw.encode())
            command.run.side_effect=run
            return trial.validate_arm_tools(p,cc,di,nn,command,p,arch)

    def test_matching_full_versions_and_gnu_reader(self):
        for arch in ('armv7l','aarch64'):self.assertEqual(self.run_tools(arch)['arm_full_version'],'22.1.8')

    def test_disassembler_nm_version_mismatch(self):
        for arch in ('armv7l','aarch64'):
            for kwargs in ({'dis':'22.1.7'},{'nm':'21.1.8'},{'dis':'22'}):
                with self.assertRaisesRegex(ValueError,'version differs'):self.run_tools(arch,**kwargs)

    def test_non_gnu_reader_rejected(self):
        with self.assertRaisesRegex(ValueError,'not GNU readelf'):self.run_tools('armv7l',reader='LLVM readelf 22.1.8\n')

    def test_x86_fixed_constants_and_original_function_objects(self):
        self.assertEqual(trial.BACKEND_FLAGS,['-ffunction-sections','-fdata-sections','-funique-section-names','-faddrsig','-g','-gdwarf-4'])
        self.assertEqual(trial.DEFAULTS,{'unique-section-names':True,'addrsig':True,'fp-contract':'on'})
        self.assertEqual(trial.CERTIFIED_TRIPLES,{'x86_64':{'x86_64-tizen-linux-gnu'}})
        self.assertEqual(trial.CERTIFIED_LLVM_MAJOR,22)
        self.assertEqual(trial.CERTIFIED_OPTIMIZATION,{'x86_64':'-O3'})
        self.assertIs(trial.policy_for_arch('x86_64')['settings'],trial.ir_settings)
        self.assertIs(trial.policy_for_arch('x86_64')['relocations'],trial.pic_relocations)
        from test_static_archives_source_v2 import module
        self.assertEqual(trial.policy_for_arch('x86_64')['settings'](module()),trial.ir_settings(module()))

    def test_x86_actual_convert_success_failure_all_arm_functions_blocked(self):
        import contextlib,tempfile
        from test_inspect_llvm_archives import native
        with contextlib.ExitStack() as stack:
            functions=[name for name,obj in vars(trial).items() if callable(obj) and (name.startswith('arm_') or name=='validate_arm_tools')]
            for name in functions:stack.enter_context(mock.patch.object(trial,name,side_effect=AssertionError('ARM reached: '+name)))
            with tempfile.TemporaryDirectory() as tmp:
                p=Path(tmp);root=p/'root';root.mkdir();build=p/'build';build.mkdir();(build/'CMakeCache.txt').touch()
                for label in ('cc','dis','nm'):(p/label).write_text('tool');(p/label).chmod(0o755)
                obj=p/'x.o';obj.write_bytes(native());import subprocess
                subprocess.run(['ar','qcD',str(root/'native.a'),str(obj)],check=True,capture_output=True)
                command=mock.Mock();command.signal_received=None
                command.run.side_effect=lambda argv,prefix,stdout:stdout.write(b'clang version 22.1.8\n')
                result=trial.convert(root,p/'out',p/'cc',p/'dis',p/'nm',build,command=command)
                self.assertEqual(result['status'],'CONVERTED');self.assertNotIn('native_archives_skipped_inventory',result)
                (root/'bad.a').write_bytes(b'!<thin>\n')
                with self.assertRaisesRegex(ValueError,'thin archive'):trial.convert(root,p/'failed',p/'cc',p/'dis',p/'nm',build,command=command)

if __name__=='__main__':unittest.main(verbosity=2)
