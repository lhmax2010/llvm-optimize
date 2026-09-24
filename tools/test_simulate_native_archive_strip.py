#!/usr/bin/env python3
import copy
import unittest
from simulate_native_archive_strip import compare


class StripGateTests(unittest.TestCase):
    def setUp(self):
        self.record=dict(thin=False,bitcode=0,other=0,index_equals_machine_symbols=True,
            index=[['sym',0,'duplicate.o',1],['sym',1,'duplicate.o',2]],
            members=[dict(ordinal=i,name='duplicate.o',occurrence=i+1,debug_sections=[]) for i in range(2)])
    def test_full_mapping_and_duplicate_members_pass(self):
        before=copy.deepcopy(self.record);before['members'][0]['debug_sections']=['.debug_info']
        compare(before,self.record)
    def test_corruption_rejected(self):
        for kind in ('order','symbol','debug','bitcode','index','thin'):
            with self.subTest(kind=kind):
                bad=copy.deepcopy(self.record)
                if kind=='order':bad['members'].reverse()
                elif kind=='symbol':bad['index'][1][0]='wrong'
                elif kind=='debug':bad['members'][0]['debug_sections']=['.debug_info']
                elif kind=='bitcode':bad['bitcode']=1
                elif kind=='index':bad['index_equals_machine_symbols']=False
                else:bad['thin']=True
                with self.assertRaises(ValueError):compare(self.record,bad)


if __name__=='__main__':unittest.main(verbosity=2)
