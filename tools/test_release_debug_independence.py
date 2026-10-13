#!/usr/bin/env python3
"""Fixed ELF32/ELF64 positive and negative controls for the release gate."""
import copy
from pathlib import Path
import subprocess
import struct
import tempfile
import unittest
import check_release_debug_independence as gate


class ReleaseGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory(prefix='release-gate-')
        root = Path(cls.directory.name)
        cls.root = root
        cls.sequence = 0
        source = root/'fixture.s'
        source.write_text('.text\n.globl test_entry\n.type test_entry,@function\n'
                          'test_entry:\ncall external_function\nret\n'
                          '.size test_entry,.-test_entry\n.data\n.long 17\n.long .text\n')
        cls.assembly = source.read_text()
        cls.pairs = {}
        for bits in (32, 64):
            items = []
            for debug in (True, False):
                target = root/('%d-%s.o' % (bits, debug))
                subprocess.run(['as', '--'+str(bits), *(['-g'] if debug else []),
                                str(source), '-o', str(target)], check=True, capture_output=True)
                items.append(gate.parse(target.read_bytes()))
            cls.pairs[bits] = items

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def test_actual_elf32_rel_and_debug_filter(self):
        a,b = self.pairs[32]
        self.assertTrue(a['debug_sections']); self.assertFalse(b['debug_sections'])
        self.assertEqual(a['relocations'][0]['type'], 2)
        self.assertEqual(a['relocations'][0]['format'], 'REL')
        self.assertEqual(gate.compare(a,b)['status'], 'PASS')

    def test_actual_elf64_rela_and_debug_filter(self):
        a,b = self.pairs[64]
        self.assertEqual(a['relocations'][0]['type'], 4)
        self.assertEqual(a['relocations'][0]['addend'], -4)
        self.assertEqual(gate.compare(a,b)['status'], 'PASS')

    def rejected(self, change, category):
        a,b = copy.deepcopy(self.pairs[64]); change(b)
        result = gate.compare(a,b)
        self.assertEqual(result['status'], 'FAIL')
        self.assertFalse(result['checks'][category])
        self.assertIn(category, result['differences'])

    def test_alloc_contents(self):
        self.rejected(lambda b:b['alloc'][0].update(content=b'changed'), 'alloc')

    def test_alloc_flags(self):
        self.rejected(lambda b:b['alloc'][0].update(flags=3), 'alloc')

    def test_alloc_size(self):
        self.rejected(lambda b:b['alloc'][0].update(size=7), 'alloc')

    def test_alloc_name(self):
        self.rejected(lambda b:b['alloc'][0].update(section='.different'), 'alloc')

    def test_alloc_type_alignment_entsize(self):
        for field,value in [('type',7),('alignment',64),('entsize',16)]:
            with self.subTest(field=field):
                self.rejected(lambda b:b['alloc'][0].update({field:value}), 'alloc')

    def test_alloc_order(self):
        a,b=copy.deepcopy(self.pairs[64]);b['alloc'].reverse()
        self.assertEqual(gate.compare(a,b)['status'],'PASS')

    def test_relocation_fields(self):
        for field, value in [('offset',3),('type',2),('symbol','other'),('addend',-8)]:
            with self.subTest(field=field):
                self.rejected(lambda b:b['relocations'][0].update({field:value}), 'relocations')

    def test_symbol_fields(self):
        for field, value in [('name','other'),('type',1),('binding',2),('visibility',2),
                             ('section','.data'),('value',3),('size',27)]:
            with self.subTest(field=field):
                def change(b):
                    s = next(s for s in b['symbols'] if s['name']=='test_entry')
                    s[field] = value
                self.rejected(change,'symbols')

    @classmethod
    def assemble(cls, extra='', bits=64):
        cls.sequence += 1
        source = cls.root/('extra-%d.s' % cls.sequence)
        target = source.with_suffix('.o')
        source.write_text(cls.assembly+extra)
        subprocess.run(['as','--'+str(bits),'-L',str(source),'-o',str(target)],
                       check=True,capture_output=True)
        return gate.parse(target.read_bytes())

    def test_additional_section_symbol_passes(self):
        a=self.assemble('.section .debug_probe,"",@progbits\n.quad .data\n')
        b=self.assemble()
        self.assertEqual(sum(s['type']==3 for s in a['excluded_symbols']),
                         sum(s['type']==3 for s in b['excluded_symbols'])+1)
        self.assertEqual(gate.compare(a,b)['status'],'PASS')

    def test_unreferenced_dot_l_local_passes(self):
        a=self.assemble('.local .Lunused\n.set .Lunused,19\n');b=self.assemble()
        self.assertTrue(any(s['name']=='.Lunused' for s in a['excluded_symbols']))
        self.assertEqual(gate.compare(a,b)['status'],'PASS')

    def test_named_local_difference_fails(self):
        a=self.assemble('.local bookkeeping\n.set bookkeeping,19\n');b=self.assemble()
        self.assertFalse(gate.compare(a,b)['checks']['symbols'])

    def test_dot_l_global_is_compared(self):
        a=self.assemble('.globl .Lpublic\n.set .Lpublic,19\n');b=self.assemble()
        self.assertFalse(gate.compare(a,b)['checks']['symbols'])

    def test_symbol_order_ignored(self):
        a,b=copy.deepcopy(self.pairs[64]);b['symbols'].reverse()
        self.assertEqual(gate.compare(a,b)['status'],'PASS')

    def test_symbol_multiplicity_checked(self):
        self.rejected(lambda b:b['symbols'].append(copy.deepcopy(b['symbols'][0])), 'symbols')

    def test_section_relocation_target_canonical_name(self):
        for bits in (32,64):
            a=self.assemble(bits=bits)
            r=next(r for r in a['relocations'] if r['target'][0][0]=='.data')
            self.assertEqual(r['symbol'],['SECTION',['.text',1,'',None]])
            b=copy.deepcopy(a)
            next(r for r in b['relocations'] if r['target'][0][0]=='.data')['symbol']='.bss'
            self.assertFalse(gate.compare(a,b)['checks']['relocations'])

    def group_pair(self):
        common=('.section .text.group,"axG",@progbits,group_signature,comdat\n'
                '.globl grouped_function\n.type grouped_function,@function\n'
                'grouped_function: ret\n.size grouped_function,.-grouped_function\n')
        a=self.assemble(common+'.section .debug_group,"G",@progbits,group_signature,comdat\n.long .text.group\n')
        b=self.assemble(common)
        return a,b

    def test_comdat_debug_only_member_difference_passes(self):
        a,b=self.group_pair()
        self.assertEqual(a['groups'],[dict(signature='group_signature',flags=1,members=[['.text.group',1,'group_signature',None]])])
        self.assertEqual(gate.compare(a,b)['status'],'PASS')

    def test_comdat_member_difference_fails(self):
        a,b=self.group_pair();b['groups'][0]['members'].append('.data')
        self.assertFalse(gate.compare(a,b)['checks']['groups'])

    def test_comdat_signature_flags_and_member_order(self):
        for field,value in [('signature','other'),('flags',0),('members',['.other','.text.group'])]:
            with self.subTest(field=field):
                a,b=self.group_pair();b['groups'][0][field]=value
                self.assertFalse(gate.compare(a,b)['checks']['groups'])
        a,b=self.group_pair()
        a['groups'][0]['members']=['.one','.two'];b['groups'][0]['members']=['.two','.one']
        self.assertFalse(gate.compare(a,b)['checks']['groups'])

    def test_comdat_multiset(self):
        a,b=self.group_pair();other=dict(signature='other',flags=1,members=['.data'])
        a['groups'].append(other);b['groups'].insert(0,other)
        self.assertEqual(gate.compare(a,b)['status'],'PASS')
        b['groups'].append(copy.deepcopy(other))
        self.assertFalse(gate.compare(a,b)['checks']['groups'])

    def test_actual_release_debug_section_fails(self):
        a=self.assemble();b=self.assemble('.section .debug_unexpected,"",@progbits\n.byte 0\n')
        self.assertFalse(gate.compare(a,b)['checks']['release_no_debug'])

    def test_release_debug_sections_rejected(self):
        self.rejected(lambda b:b['debug_sections'].append('.debug_info'), 'release_no_debug')

    def test_rel_implicit_addend_bytes(self):
        a,b = copy.deepcopy(self.pairs[32]); b['alloc'][0]['content'] = b'changed'
        self.assertFalse(gate.compare(a,b)['checks']['alloc'])

    def test_truncated_elf_rejected(self):
        with self.assertRaises(ValueError): gate.parse(b'\x7fELF')



# A small ELF writer provides fixed, independently specified section identities;
# unlike GNU as it can represent duplicate section names in any desired order.
def fixture(secs, syms=(), relocs=(), groups=(), addrsig=None, flags=0):
    secs=copy.deepcopy(secs);syms=copy.deepcopy(list(syms))
    rows=[dict(id='null',name='',type=0,flags=0,data=b'')]+secs
    for i,(target,entries) in enumerate(relocs):
        rows.append(dict(id='rel'+str(i),name='.rela'+next(s['name'] for s in secs if s['id']==target),type=4,flags=0,
                         data=b'',target=target,entries=entries,alignment=8,entsize=24))
    for i,(signature,members) in enumerate(groups):
        rows.append(dict(id='group'+str(i),name='.group',type=17,flags=0,data=b'',signature=signature,members=members,alignment=4,entsize=4))
    if addrsig is not None:rows.append(dict(id='addrsig',name='.llvm_addrsig',type=0x6fff4c03,flags=0,data=b'',entsize=0))
    rows+= [dict(id='symtab',name='.symtab',type=2,flags=0,data=b'',alignment=8,entsize=24),
            dict(id='strtab',name='.strtab',type=3,flags=0,data=b''),dict(id='shstrtab',name='.shstrtab',type=3,flags=0,data=b'')]
    ids={r['id']:i for i,r in enumerate(rows)};symbolids={s['id']:i+1 for i,s in enumerate(syms)}
    names=bytearray(b'\0');strings=bytearray(b'\0');symdata=bytearray(b'\0'*24)
    for s in syms:
        offset=len(strings);strings.extend(s.get('name',s['id']).encode()+b'\0')
        idx=ids[s['section']] if s.get('section') else 0
        symdata.extend(struct.pack('<IBBHQQ',offset,s.get('binding',1)*16+s.get('type',0),s.get('visibility',0),idx,s.get('value',0),s.get('size',0)))
    def uleb(n):
        r=bytearray()
        while n>=128:r.append((n&127)|128);n>>=7
        r.append(n);return r
    for r in rows:
        r['nameoff']=len(names);names.extend(r['name'].encode()+b'\0')
        if 'entries' in r:
            r['link']=ids['symtab'];r['info']=ids[r['target']]
            r['data']=b''.join(struct.pack('<QQq',off,(symbolids[sym]<<32)|kind,add) for off,kind,sym,add in r['entries'])
        if 'members' in r:
            r['link']=ids['symtab'];r['info']=symbolids[r['signature']]
            r['data']=struct.pack('<'+'I'*(1+len(r['members'])),1,*[ids[x] for x in r['members']])
        if r['id']=='symtab':r['data']=bytes(symdata);r['link']=ids['strtab'];r['info']=1
        if r['id']=='strtab':r['data']=bytes(strings)
        if r['id']=='addrsig':r['data']=b''.join(uleb(symbolids[x]) for x in addrsig);r['link']=ids['symtab']
        if r.get('link_order'):r['link']=ids[r['link_order']]
    rows[-1]['data']=bytes(names);blob=bytearray(b'\0'*64);headers=[]
    for r in rows:
        off=len(blob);blob.extend(r['data'])
        headers.append(struct.pack('<IIQQQQIIQQ',r['nameoff'],r.get('type',1),r.get('flags',2),0,off,len(r['data']),r.get('link',0),r.get('info',0),r.get('alignment',1),r.get('entsize',0)))
    shoff=len(blob);blob.extend(b''.join(headers));blob[:16]=b'\x7fELF'+bytes([2,1,1])+b'\0'*9
    struct.pack_into('<HHIQQQIHHHHHH',blob,16,1,62,1,0,0,shoff,flags,64,0,0,64,len(rows),ids['shstrtab'])
    return gate.parse(bytes(blob))


def section(ident,name=None,data=b'abcd',flags=2,**kwargs):
    return dict(id=ident,name=name or '.'+ident,type=1,flags=flags,data=data,**kwargs)


class FinalContractFixtures(unittest.TestCase):
    def status(self,a,b,want,check=None):
        result=gate.compare(a,b);self.assertEqual(result['status'],want,result['differences'])
        if check:self.assertFalse(result['checks'][check])

    def test_comdat_section_reorder_pass(self):
        secs=[section('a',flags=0x202),section('b',flags=0x202)]
        syms=[dict(id='sa'),dict(id='sb')];groups=[('sa',['a']),('sb',['b'])]
        self.status(fixture(secs,syms,groups=groups),fixture(secs[::-1],syms,groups=groups),'PASS')

    def test_ordinary_section_reorder_pass(self):
        secs=[section('a'),section('b')];self.status(fixture(secs),fixture(secs[::-1]),'PASS')

    def ordered(self,name):
        secs=[section('a',name,flags=0x202),section('b',name,flags=0x202)]
        syms=[dict(id='sa'),dict(id='sb')];groups=[('sa',['a']),('sb',['b'])]
        self.status(fixture(secs,syms,groups=groups),fixture(secs[::-1],syms,groups=groups),'FAIL','ordered_sections')

    def test_init_array_reorder_fail(self):self.ordered('.init_array')
    def test_c_identifier_section_reorder_fail(self):self.ordered('runtime_registry')

    def test_duplicate_identity_reorder_fail(self):
        secs=[section('a','.duplicate',b'A'),section('b','.duplicate',b'B')]
        self.status(fixture(secs),fixture(secs[::-1]),'FAIL','alloc')

    def test_cross_target_relocation_reorder_pass(self):
        secs=[section('a'),section('b')];syms=[dict(id='external')]
        rels=[('a',[(0,1,'external',0)]),('b',[(1,2,'external',1)])]
        self.status(fixture(secs,syms,rels),fixture(secs[::-1],syms,rels[::-1]),'PASS')

    def test_same_target_relocation_reorder_fail(self):
        secs=[section('a')];syms=[dict(id='external')];entries=[(0,1,'external',0),(1,2,'external',1)]
        self.status(fixture(secs,syms,[('a',entries)]),fixture(secs,syms,[('a',entries[::-1])]),'FAIL','relocations')

    def test_link_order_target_fail(self):
        a=[section('a'),section('b'),section('order',flags=0x82,link_order='a')];b=copy.deepcopy(a);b[-1]['link_order']='b'
        self.status(fixture(a),fixture(b),'FAIL','alloc')

    def test_e_flags_fail(self):self.status(fixture([section('a')]),fixture([section('a')],flags=0x5000000),'FAIL','header')

    def test_debug_local_mapping_pass(self):
        secs=[section('a'),section('d','.debug_info',flags=0)]
        self.status(fixture(secs,[dict(id='map',name='$d',binding=0,section='d')]),fixture(secs[:1]),'PASS')

    def test_alloc_mapping_symbol_fail(self):
        secs=[section('a')];a=[dict(id='map',name='$d',binding=0,section='a')];b=[{**a[0],'name':'$t'}]
        self.status(fixture(secs,a),fixture(secs,b),'FAIL','symbols')

    def test_debug_only_undefined_pass(self):
        secs=[section('a'),section('d','.debug_info',flags=0)]
        self.status(fixture(secs,[dict(id='debugref')],[('d',[(0,1,'debugref',0)])],addrsig=['debugref']),fixture(secs[:1],addrsig=[]),'PASS')

    def test_alloc_undefined_difference_fail(self):
        secs=[section('a')];a=fixture(secs,[dict(id='x')],[('a',[(0,1,'x',0)])]);b=fixture(secs,[dict(id='y')],[('a',[(0,1,'y',0)])])
        self.status(a,b,'FAIL','relocations')

    def test_addrsig_set_fail(self):
        secs=[section('a')];syms=[dict(id='x'),dict(id='y')]
        self.status(fixture(secs,syms,addrsig=['x']),fixture(secs,syms,addrsig=['y']),'FAIL','addrsig')

    def test_addrsig_symbol_index_only_pass(self):
        secs=[section('a')];syms=[dict(id='x'),dict(id='y')]
        self.status(fixture(secs,syms,addrsig=['x','y']),fixture(secs,syms[::-1],addrsig=['y','x']),'PASS')

    def test_local_relocation_value_fail(self):
        secs=[section('a')];a=[dict(id='local',name='.Lhere',binding=0,section='a',value=0)];b=[{**a[0],'value':1}]
        self.status(fixture(secs,a,[('a',[(0,1,'local',0)])]),fixture(secs,b,[('a',[(0,1,'local',0)])]),'FAIL','relocations')

if __name__ == '__main__':
    unittest.main(verbosity=2)
