"""RPATH in-place CMake edits, unordered tool progress, and real object gates."""
import json,shutil,subprocess,unittest
from pathlib import Path
from unittest.mock import patch
import bolt_helper as h
from test_bolt_helper import Base
from test_second_review import LINK,TF,plan_text
import test_second_review as second

class RunpathTests(Base):
    def setup_elf(self,old):
        src=self.d/'probe.c';src.write_text('int main(void) { return 0; }\n')
        cc=shutil.which('cc');self.assertIsNotNone(cc)
        self.candidate=self.d/'candidate';self.root=self.d/'root';(self.root/'usr/bin').mkdir(parents=True)
        subprocess.run([cc,str(src),'-Wl,-rpath,'+old,'-o',str(self.candidate)],check=True,capture_output=True)
        self.baseline=self.d/'baseline.json';entity=self.root/'usr/bin/clang-22';shutil.copyfile(self.candidate,entity)
        script=self.d/'baseline.cmake';script.write_text('file(RPATH_CHANGE FILE '+h.cmake_literal(str(entity))+' OLD_RPATH '+h.cmake_literal(old)+' NEW_RPATH '+h.cmake_literal('$ORIGIN/../lib64')+')\n')
        subprocess.run(['cmake','-P',str(script)],check=True,capture_output=True)
        h.installed_baseline(self.root,self.baseline)
    def adjust(self):
        with patch.object(h,'validate_identity'):
            return h.adjust_rpath(self.candidate,self.baseline,self.d,{})
    def test_build_path(self):
        self.setup_elf('$ORIGIN/../lib64:/build/lib64:');before=h.digest(self.candidate);r=self.adjust()
        self.assertNotEqual(r['after_sha256'],before);self.assertEqual(r['strip_all_sha256'],before)
        self.assertEqual(r['rpath']['after'],{'DT_RPATH':None,'DT_RUNPATH':'$ORIGIN/../lib64'})
        self.assertEqual(r['rpath_adjusted_sha256'],h.digest(self.candidate))
    def test_trailing_empty(self):
        self.setup_elf('$ORIGIN/../lib64:');self.adjust();self.assertEqual(h.security_properties(self.candidate)['DT_RUNPATH'],'$ORIGIN/../lib64')
    def test_already_identical(self):
        self.setup_elf('$ORIGIN/../lib64');old=h.digest(self.candidate);self.adjust();self.assertEqual(h.digest(self.candidate),old)
        self.assertFalse((self.d/'candidate-rpath.cmake').exists())
    def test_cmake_failure(self):
        self.setup_elf('$ORIGIN/../lib64:')
        with patch.object(h,'call',side_effect=h.GateError('cmake failed')),self.assertRaisesRegex(h.GateError,'cmake failed'):self.adjust()
    def test_layout_change(self):
        self.setup_elf('$ORIGIN/../lib64:')
        with patch.object(h,'rpath_layout',side_effect=[{'bytes':1},{'bytes':2}]),self.assertRaisesRegex(h.GateError,'layout'):self.adjust()
    def test_missing_baseline(self):
        with self.assertRaisesRegex(h.GateError,'installed-baseline missing'):h.adjust_rpath(self.d/'none',self.d/'missing',self.d,{})
    def test_installed_non_path_security_failure(self):
        self.setup_elf('$ORIGIN/../lib64');v=json.loads(self.baseline.read_text());v['security_properties']['DT_BIND_NOW']=not v['security_properties']['DT_BIND_NOW'];self.baseline.write_text(json.dumps(v))
        with self.assertRaisesRegex(h.GateError,'DT_BIND_NOW'):self.adjust()
    def test_only_path_excluded_ordinary(self):
        self.setup_elf('$ORIGIN/../lib64:');a=self.root/'usr/bin/clang-22'
        with self.assertRaisesRegex(h.GateError,'DT_RUNPATH'):h.security_compare(a,self.candidate)
        self.assertTrue(h.security_compare(a,self.candidate,ignore_paths=True)['security_preserved'])
    def test_readelf_disagreement(self):
        self.setup_elf('$ORIGIN/../lib64');real=h.call
        def call(args,log,**kw):
            if args[0]=='readelf':Path(log).write_text(' 0x000000000000001d (RUNPATH) Library runpath: [/wrong]\n')
            else:real(args,log,**kw)
        with patch.object(h,'call',side_effect=call),self.assertRaisesRegex(h.GateError,'readelf'):self.adjust()

class ParallelTests(Base):
    def test_shuffled_plan(self):
        ds=sorted(h.BOLT_TASK_DESCRIPTIONS|h.TF_REFRESH_DESCRIPTIONS)
        text=plan_text(ds);lines=text.splitlines();lines=lines[::2]+lines[1::2]
        self.assertEqual(set(h.tool_plan('\n'.join(lines))['descriptions']),set(ds))
    def test_shuffled_execution(self):
        p,s=second.SecondBuildTests.setup_build(self,True)
        lines=plan_text(TF+[LINK]).splitlines();lines=[lines[2],lines[0],lines[1]]
        r=h.tool_verify(self.d,p,'\n'.join(lines)+'\n'+h.BUILD_SUCCESS,s);self.assertEqual(r['executed_tasks'],3)
    def test_missing_execution(self):
        p,s=second.SecondBuildTests.setup_build(self,True)
        with self.assertRaises(h.GateError):h.tool_verify(self.d,p,'[1/3] '+LINK+'\n'+h.BUILD_SUCCESS,s)
    def test_duplicate_counter(self):
        with self.assertRaises(h.GateError):h.tool_plan('[1/2] '+TF[0]+'\n[1/2] '+LINK)

class RealGateTests(Base):
    def run_gate(self,action):
        a=self.d/'ordinary';b=self.d/'candidate';a.write_bytes(b'A');b.write_bytes(b'B');work=self.d/'gate'
        args=[('real.c','x86_64-tizen-linux-gnu',['-c','real.c'])]
        with patch.object(h,'real_commands',return_value=args),patch.object(h,'call',side_effect=action):
            return h.real_gate(a,b,self.d/'build',work,self.d/'resource')
    def test_real_compile_failure(self):
        def action(*args,**kw):raise h.GateError('real compiler failed')
        with self.assertRaisesRegex(h.GateError,'compiler failed'):self.run_gate(action)
    def test_real_object_difference(self):
        def action(args,*unused,**kw):Path(args[-1]).write_bytes(Path(args[0]).read_bytes())
        with self.assertRaisesRegex(h.GateError,'real object bytes differ'):self.run_gate(action)
    def test_real_equal(self):
        seen=[]
        def action(args,*unused,**kw):seen.append(args[0]);Path(args[-1]).write_bytes(b'identical')
        self.assertTrue(self.run_gate(action)['real_pass']);self.assertEqual(len(set(seen)),1)
    def test_real_missing_object(self):
        with self.assertRaisesRegex(h.GateError,'nonempty'):self.run_gate(lambda *args,**kw:None)
