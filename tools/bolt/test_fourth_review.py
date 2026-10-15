"""Review fourteen: complete logs, preconditions, semantic ELF and strict graph inputs."""
import importlib.util,json,shutil,struct,sys,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import bolt_helper as h
from test_bolt_helper import Base,EDGE,log
from test_security_properties import security_elf
import test_second_review as second
from test_second_review import LINK,TF,plan_text
spec=importlib.util.spec_from_file_location('closure_v3',Path(__file__).parent/'results/review-closure-v3.py')
graph=importlib.util.module_from_spec(spec);spec.loader.exec_module(graph)

class FourthBuildTests(Base):
    def setup_build(self,tf=False):return second.SecondBuildTests.setup_build(self,tf)
    def verify(self,text,plan=None,state=None):
        p,s=self.setup_build() if plan is None else (plan,state)
        return h.tool_verify(self.d,p,text,s)
    def test_valid_marker(self):
        r=self.verify('[1/1] '+LINK+'\n'+h.BUILD_SUCCESS)
        self.assertEqual((r['planned_tasks'],r['executed_tasks']),(1,1));self.assertTrue(r['executable_before']);self.assertTrue(r['executable_produced_by_this_build'])
    def test_empty_log(self):
        with self.assertRaises(h.GateError):self.verify('')
    def test_missing_marker(self):
        with self.assertRaises(h.GateError):self.verify('[1/1] '+LINK)
    def test_duplicate_marker(self):
        with self.assertRaises(h.GateError):self.verify('[1/1] '+LINK+'\n'+h.BUILD_SUCCESS+'\n'+h.BUILD_SUCCESS)
    def test_marker_not_last(self):
        with self.assertRaises(h.GateError):self.verify('[1/1] '+LINK+'\n'+h.BUILD_SUCCESS+'\ntrailer')
    def test_no_tasks_build(self):
        with self.assertRaisesRegex(h.GateError,'executed no tasks'):self.verify(h.BUILD_SUCCESS)
    def test_malformed_progress(self):
        p,s=self.setup_build()
        for row in ('[1/1','[1/x] task','[123] fake','[1/2]'):
            with self.subTest(row=row),self.assertRaisesRegex(h.GateError,'malformed'):
                self.verify(row+'\n[1/1] '+LINK+'\n'+h.BUILD_SUCCESS,p,s)
    def test_valid_restat(self):
        r=self.verify('[1/9] '+LINK+'\n'+h.BUILD_SUCCESS);self.assertEqual(r['executed_tasks'],1)
    def test_up_to_date_marker(self):
        p,s=self.setup_build();p=h.tool_plan('ninja: no work to do.')
        r=self.verify('ninja: no work to do.\n'+h.BUILD_SUCCESS,p,s);self.assertEqual(r['executed_tasks'],0)
    def test_absent_executable_before(self):
        p,s=self.setup_build();exe=self.d/'bin/llvm-bolt';exe.unlink();s=h.tool_prepare(self.d,p,self.d/'state');exe.write_text('new');exe.chmod(0o755)
        r=self.verify('[1/1] '+LINK+'\n'+h.BUILD_SUCCESS,p,s);self.assertFalse(r['executable_before']);self.assertIsNone(r['executable_before_sha256'])

class FourthPlanTests(unittest.TestCase):
    def test_warning_no_work(self):
        p=h.tool_plan('ninja: warning: fixture\nninja: no work to do.');self.assertEqual(p['tasks'],0);self.assertEqual(len(p['ninja_diagnostics']),1)
    def test_warning_plan(self):self.assertEqual(h.tool_plan('ninja: warning: fixture\n[1/1] '+LINK)['tasks'],1)
    def test_unknown_line(self):
        with self.assertRaises(h.GateError):h.tool_plan('unknown\n[1/1] '+LINK)
    def test_regeneration_anywhere(self):
        for text in ('[0/1] Re-running CMake...','[1/2] '+LINK+'\n[2/2] Re-running CMake...','ninja: warning: hi\n[0/1] Re-running CMake...'):
            with self.subTest(text=text),self.assertRaisesRegex(h.GateError,'real plan is not visible'):h.tool_plan(text)
    def test_certified_counts(self):
        c=h.certified();self.assertEqual(c['bolt_task_count'],len(h.BOLT_TASK_DESCRIPTIONS));self.assertEqual(c['tf_refresh_task_count'],len(h.TF_REFRESH_DESCRIPTIONS));self.assertEqual(h.PROFILE_SHA,c['profile_sha256'])
    def test_remedy_tool(self):
        with self.assertRaisesRegex(h.GateError,'actual=.*expected=.*remedy:.*recertify'):h.certified_version('LLVM version 99.0.0')
    def test_remedy_task(self):
        with self.assertRaisesRegex(h.GateError,'actual=.*expected=.*remedy:.*never expand'):h.tool_plan('[1/1] ordinary')
    def test_remedy_match(self):
        with self.assertRaisesRegex(h.GateError,'actual=.*expected=.*remedy:.*never raise'):h.match_counts(log(s=6),[],True,True)

class FourthPrereqTests(Base):
    def test_current_preflight(self):self.assertTrue(h.preflight()['preflight_pass'])
    def test_old_python(self):
        with patch.object(sys,'version_info',(3,8,9)),self.assertRaisesRegex(h.GateError,'expected=>=3.9'):h.preflight()
    def test_missing_interface(self):
        with patch.object(h.os,'waitid',create=True) as ignored:
            del h.os.waitid
            with self.assertRaisesRegex(h.GateError,'missing.*waitid'):h.preflight()
    def test_small_disk_pass(self):
        with patch.object(h.shutil,'disk_usage',return_value=SimpleNamespace(free=h.GIB+100)):
            self.assertEqual(h.disk_preflight(self.d,100)['projected_free_bytes'],h.GIB)
    def test_small_disk_fail(self):
        with patch.object(h.shutil,'disk_usage',return_value=SimpleNamespace(free=h.GIB+99)),self.assertRaises(h.GateError):h.disk_preflight(self.d,100)
    def test_profile_remedy(self):
        p=self.d/'profile';p.write_text('wrong')
        with self.assertRaisesRegex(h.GateError,'actual=.*expected=.*remedy: first verify the Source'):h.profile_identity(p)
    def test_replay_shell_and_rsp(self):
        for arg in ('-Wl,@args.rsp','-Wl,--foo,@args.rsp','-Xlinker @args.rsp','a | cat','a & cat','a > x','a < x','a;true','`true`','$(true)'):
            with self.subTest(arg=arg),self.assertRaises(h.GateError):h.replay_script(EDGE.replace('driver.o',arg),'out','dep')
    def test_replay_real_shape(self):self.assertIn('--emit-relocs',h.replay_script(EDGE,'out','dep'))

class FourthELFTests(Base):
    def pair(self):
        a=self.d/'ordinary';b=self.d/'candidate';security_elf(a);shutil.copyfile(a,b);return a,b
    def test_shndx_rejected(self):
        a,b=self.pair();e=h.ELF(b);pos=e.by_name['.dynsym'][4]+24+6;e.close();data=bytearray(b.read_bytes());struct.pack_into('<H',data,pos,0xff00);b.write_bytes(data)
        with self.assertRaisesRegex(h.GateError,'invalid symbol shndx'):h.security_properties(b)
    def test_shndx_abs_common(self):
        a,b=self.pair();e=h.ELF(b);pos=e.by_name['.dynsym'][4]+24+6;e.close()
        for index in (0,2,0xfff1,0xfff2):
            data=bytearray(b.read_bytes());struct.pack_into('<H',data,pos,index);b.write_bytes(data);h.security_properties(b)
    def set_dynamic(self,p,entries):
        e=h.ELF(p);pos=e.by_name['.dynamic'][4];e.close();data=bytearray(p.read_bytes())
        for i,item in enumerate(entries):struct.pack_into('<qQ',data,pos+i*16,*item)
        p.write_bytes(data)
    def test_runpath_change(self):
        a,b=self.pair();self.set_dynamic(a,[(29,1),(0,0)]);self.set_dynamic(b,[(29,10),(0,0)])
        with self.assertRaisesRegex(h.GateError,'DT_RUNPATH'):h.security_compare(a,b)
    def test_rpath_change(self):
        a,b=self.pair();self.set_dynamic(a,[(15,1),(0,0)]);self.set_dynamic(b,[(15,10),(0,0)])
        with self.assertRaisesRegex(h.GateError,'DT_RPATH'):h.security_compare(a,b)
    def test_duplicate_search_tag(self):
        a,b=self.pair()
        for tag in (15,29):
            self.set_dynamic(b,[(tag,1),(tag,1),(0,0)])
            with self.assertRaisesRegex(h.GateError,'duplicate dynamic search'):h.security_properties(b)

class FourthClosureTests(Base):
    def inputs(self,extra='',path='tools/bolt/generated',description='Generating VCSVersion.inc'):
        a=self.d/'before';b=self.d/'after';r=self.d/'rules'
        a.write_text('build ordinary: phony\n')
        b.write_text('include CMakeFiles/rules.ninja\ncmake_ninja_workdir = /work/\nbuild '+path+' | ${cmake_ninja_workdir}'+path+': GEN\nbuild llvm-bolt: phony '+path+'\n'+extra)
        r.write_text('rule GEN\n  command = touch $out\n  description = '+description+'\n')
        return a,b,r
    def test_small_graph(self):self.assertEqual(graph.analyze(*self.inputs(),1)['new_task_edges'],1)
    def test_subninja_rejected(self):
        with self.assertRaisesRegex(graph.GraphError,'subninja'):graph.analyze(*self.inputs('subninja other.ninja\n'),1)
    def test_include_rejected(self):
        with self.assertRaisesRegex(graph.GraphError,'include'):graph.analyze(*self.inputs('include other.ninja\n'),1)
    def test_escape_rejected(self):
        with self.assertRaisesRegex(graph.GraphError,'escaped'):graph.analyze(*self.inputs(path='tools/bolt/a$ b'),1)
    def test_unknown_path_variable(self):
        with self.assertRaisesRegex(graph.GraphError,'unexpanded path'):graph.analyze(*self.inputs(path='$unknown/file'),1)
    def test_unknown_description_variable(self):
        with self.assertRaisesRegex(graph.GraphError,'unexpanded description variable'):graph.analyze(*self.inputs(description='$unknown'),1)
    def test_wrong_task_count(self):
        with self.assertRaisesRegex(graph.GraphError,'task count'):graph.analyze(*self.inputs(),2)

if __name__=='__main__':unittest.main()
