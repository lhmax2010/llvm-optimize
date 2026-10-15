import json,unittest
from pathlib import Path
import bolt_helper as h

LINK='Linking CXX executable bin/llvm-bolt'
DESCRIPTIONS=json.loads((Path(__file__).parent/'results/review-tool-descriptions-v2.json').read_text())
class ReviewToolPlanTests(unittest.TestCase):
    def test_complete_universe(self):
        descriptions=sorted(DESCRIPTIONS)
        self.assertEqual(set(descriptions),h.BOLT_TASK_DESCRIPTIONS)
        text='\n'.join('[%d/%d] %s'%(i+1,len(descriptions),d) for i,d in enumerate(descriptions))
        self.assertEqual(h.tool_plan(text)['categories'], {'objects':102,'static_libraries':7,'executables':1,'generated':1})
    def test_every_description(self):
        for description in DESCRIPTIONS:
            with self.subTest(description=description):
                text='[1/1] '+LINK if description==LINK else '[1/2] '+description+'\n[2/2] '+LINK
                self.assertEqual(h.tool_plan(text)['tasks'],1 if description==LINK else 2)
    def test_rejected_tasks(self):
        for description in ['Building CXX object lib/Support/a.o', 'Linking CXX static library lib64/libLLVMCore.a',
                            'Linking CXX executable bin/clang-22', 'Generating unknown', 'Creating unknown',
                            'Building CXX object lib/Support/bin/llvm-bolt.cpp.o', 'Linking CXX executable bin/llvm-bolt-spoof']:
            with self.subTest(description=description),self.assertRaises(h.GateError):
                h.tool_plan('[1/2] '+description+'\n[2/2] '+LINK)
    def test_nonprogress(self):
        for line in ['ninja: warning: anything','', ' [1/1] '+LINK,'[1/1]  '+LINK]:
            with self.subTest(line=line),self.assertRaises(h.GateError):h.tool_plan(line+'\n[1/1] '+LINK)
    def test_empty(self):
        with self.assertRaises(h.GateError):h.tool_plan('')
    def test_missing_link(self):
        with self.assertRaises(h.GateError):h.tool_plan('[1/1] Linking CXX static library lib64/libLLVMBOLTCore.a')

if __name__=='__main__':unittest.main()
