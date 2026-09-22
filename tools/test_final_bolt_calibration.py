#!/usr/bin/env python3
"""Preregistered protocol controls. Mocks only: never execute a compiler."""
import contextlib
import copy
import io
import json
from pathlib import Path
import re
import tempfile
import sys
import unittest
from unittest.mock import Mock, patch

import run_final_bolt_calibration as final


class AcceptanceRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        doc = (final.bench.WORKSPACE/'docs/20_spec_integration_v2.md').read_text()
        code = next(c for c in re.findall(r'```python\n(.*?)\n```',doc,re.S) if 'def aa_preflight(' in c)
        cls.rules = {}
        exec(compile(code,'docs/20 §6.3','exec'),cls.rules)

    def test_11_percent_aborts_before_any_later_measurements(self):
        result = self.rules['paired_gate']([100,111])
        self.assertEqual(result['status'],'ABORT_ENVIRONMENT')
        self.assertFalse(result['established'])

    def test_9_percent_continues_with_original_paired_threshold(self):
        result = self.rules['paired_gate']([100,109,100,81,81,100,100,81])
        self.assertEqual(result['status'],'EVALUATED')
        self.assertEqual(result['threshold'],.82)
        self.assertTrue(result['established'])
        result = self.rules['paired_gate']([100,109,100,82,81,100,100,81])
        self.assertFalse(result['established'])  # Equality is not sufficient.

    def test_boundary_and_any_metric(self):
        gate = self.rules['aa_preflight']
        self.assertEqual(gate({'wall':[100,110],'cpu':[100,90]})['status'],'CONTINUE')
        self.assertEqual(gate({'wall':[100,109],'peak':[100,111]})['status'],'ABORT_ENVIRONMENT')
        for pair in ([100,0],[100,float('nan')]):
            with self.assertRaises(ValueError):gate({'wall':pair})
        with self.assertRaises(ValueError):gate({})


class AcceptanceRulesV3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc=(final.bench.WORKSPACE/'docs/21_spec_integration_v3.md').read_text()
        code=next(c for c in re.findall(r'```python\n(.*?)\n```',cls.doc,re.S) if 'def resource_gate(' in c)
        cls.rules={};exec(compile(code,'docs/21 §6.3','exec'),cls.rules)
        # Synthetic test policy, not recommended production acceptance values.
        cls.rules.update(FLOOR=.03, ENV_ABORT=.10, WALL_NOISE=.06)
        cls.rules['TOL'].update(compile_memory=.05, runtime_wall=.02, runtime_cpu=.02,
                                runtime_memory=.03, runtime_rss=.03)

    def test_unfrozen_internal_policy_is_refused(self):
        with patch.dict(self.rules, FLOOR=None):
            with self.assertRaisesRegex(ValueError, 'not been frozen'):
                self.rules['aa_preflight'](self.metrics())

    def metrics(self):
        r={n:dict(values=[100,100,100,80,80,100,100,80],delta=.2)
           for n in self.rules['BENEFIT']}
        r.update({n:dict(values=[100,100,100,99,99,100,100,99]) for n in self.rules['TOL']})
        return r

    def test_resource_positive(self):
        self.assertEqual(self.rules['resource_gate'](self.metrics(),'compile_memory')['status'],'NONREGRESSION')

    def test_resource_within_tolerance_but_geomean_regresses(self):
        m=self.metrics();m['runtime_wall']['values']=[100,100,100,101,101,100,100,101]
        self.assertEqual(self.rules['resource_gate'](m,'runtime_wall')['status'],'REGRESSION_OR_NOT_CONFIRMED')

    def test_resource_noise_is_not_permission_to_ship(self):
        m=self.metrics();m['compile_memory']['values'][1]=103
        self.assertEqual(self.rules['resource_gate'](m,'compile_memory')['status'],'INCONCLUSIVE_NOISE')

    def test_paired_gate_checks_every_metric_first(self):
        m=self.metrics();m['build_cpu']['values'][1]=111
        self.assertEqual(self.rules['paired_gate'](m,'unit_compile')['status'],'ABORT_ENVIRONMENT')
        m.pop('runtime_rss')
        with self.assertRaises(ValueError): self.rules['paired_gate'](m,'unit_compile')

    def test_9_percent_can_continue_when_delta_is_frozen_large_enough(self):
        m=self.metrics();m['unit_compile']['values'][1]=109
        self.assertEqual(self.rules['aa_preflight'](m)['status'],'CONTINUE')
        r=self.rules['paired_gate'](m,'unit_compile')
        self.assertEqual(r['threshold'],.82);self.assertTrue(r['established'])
        m['unit_compile']['values'][3]=82
        self.assertFalse(self.rules['paired_gate'](m,'unit_compile')['established'])

    def test_dead_zone_at_three_percent_floor(self):
        m=self.metrics();m['build_wall']['delta']=.03
        r=self.rules['aa_preflight'](m)
        self.assertEqual(r['status'],'INSUFFICIENT_RESOLUTION');self.assertIn('build_wall',r['dead_zone'])

    def test_dead_zone_above_floor_can_continue(self):
        m=self.metrics();m['build_wall']['delta']=.031
        self.assertEqual(self.rules['aa_preflight'](m)['status'],'CONTINUE')

    def test_drift_aa_larger_is_preserved(self):
        m=self.metrics();m['unit_compile']['values'][1]=102
        self.assertEqual(self.rules['paired_gate'](m,'unit_compile')['d'],.02)

    def test_drift_a_pairs_larger_is_used(self):
        m=self.metrics();m['unit_compile']['values'][6]=104
        self.assertAlmostEqual(self.rules['paired_gate'](m,'unit_compile')['d'],.04)

    def test_drift_uses_both_ratio_directions(self):
        m=self.metrics();m['unit_compile']['values'][6]=99
        self.assertAlmostEqual(self.rules['paired_gate'](m,'unit_compile')['d'],100/99-1)

    def test_drift_can_end_wall_as_unresolved_noise(self):
        m=self.metrics();m['build_wall']['values'][6]=104
        self.assertEqual(self.rules['paired_gate'](m,'build_wall')['status'],'NOISE_EXCEEDS_DETECTABLE_EFFECT')

    def identity_template(self, rc, text):
        code=re.search(r"<<'PYIDENTITY'\n(.*?)\nPYIDENTITY",self.doc,re.S).group(1)
        with tempfile.TemporaryDirectory(dir=final.bench.WORKSPACE/'temp') as td:
            path=Path(td)/'identity.txt';path.write_text(text)
            with patch.object(sys,'argv',['template',str(rc),str(path)]):
                exec(compile(code,'docs/21 §6.1 identity template','exec'),{})

    def identity_ok(self):
        return '\n'.join(['EXPECTED_SHA256=PASS','EXPECTED_BOLT=PASS','IDENTITY_STABILITY=PASS',
            'EXECUTABLE=YES','VERSION_EXIT=0','ARCH_MISMATCH=NO','BINFMT_REGISTRY_OVERRIDDEN=NO',
            'BINFMT_DISPATCH_POSSIBLE=NO'])

    def test_identity_template_accepts_only_complete_success(self):
        self.identity_template(0,self.identity_ok())
        with self.assertRaises(AssertionError):self.identity_template(1,self.identity_ok())

    def test_identity_template_missing_pass_rejected(self):
        for marker in ['EXPECTED_SHA256=PASS','EXPECTED_BOLT=PASS','IDENTITY_STABILITY=PASS','EXECUTABLE=YES']:
            with self.subTest(marker=marker),self.assertRaises(AssertionError):
                self.identity_template(0,self.identity_ok().replace(marker,''))


class FinalCalibrationControls(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(dir=final.bench.WORKSPACE/'temp')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.plan = json.loads(final.PLAN.read_text())

    def test_split_commands_freeze_every_other_switch(self):
        for target in ('armv7l','aarch64'):
            for formal in (False,True):
                command = final.commands(self.plan,target,formal)
                self.assertEqual(command[command.index('--compile-target')+1],target)
                self.assertEqual('--calibrate' in command,not formal)
                for flag,expected in [('--cpus','2'),('--runs','5'),('--seed','73419'),
                                      ('--aslr','off'),('--load-threshold','10')]:
                    self.assertEqual(command[command.index(flag)+1],expected)
                self.assertEqual(command[command.index('--scales')+1:command.index('--scales')+4],['1','2','2'])
                self.assertEqual(command[:5],['nice','-n','15','ionice','-c3'])

    def test_quiet_window_positive_negative_and_boundary(self):
        for value in (0,2.99,3):final.require_quiet({'load1':value})
        for value in (3.01,float('nan')):
            with self.assertRaises(RuntimeError):final.require_quiet({'load1':value})

    def test_load_summary_records_observed_period_bounds(self):
        samples=[dict(timestamp=str(i),load1=v) for i,v in enumerate((1,11,12,10,11))]
        result=final.load_summary(samples)
        self.assertEqual(result['max_load1'],12)
        self.assertEqual(len(result['above_10_samples']),3)
        self.assertEqual(result['above_10_observed_periods'][0],dict(
            first_observed='1',last_observed='2',prior_observation='0',next_observation='3'))

    def test_sampler_reaped_on_exception(self):
        with patch.object(final,'load_sample',return_value=dict(timestamp='fixture',load1=1)):
            with self.assertRaisesRegex(RuntimeError,'fixture'):
                with final.LoadMonitor(self.root) as monitor:
                    raise RuntimeError('fixture')
        self.assertFalse(monitor.thread.is_alive())
        self.assertTrue(json.loads((self.root/'loadavg-summary.json').read_text())['sampler_reaped'])

    def test_sampler_failure_terminates_child_and_waits(self):
        child=Mock(pid=12345)
        child.poll.return_value=None
        with patch.object(final.sp,'Popen',return_value=child),patch.object(final.os,'killpg') as kill:
            with self.assertRaisesRegex(RuntimeError,'sampler failed'):
                final.execute(['mock-no-execution'],self.root/'process',Mock(error=RuntimeError('fixture')))
        kill.assert_called_once_with(12345,final.signal.SIGTERM)
        child.wait.assert_called_once_with(timeout=10)

    def test_preregistration_must_be_pushed_clean_exact_commit(self):
        commit='a'*40
        with patch.object(final.sp,'check_output',side_effect=[commit+'\n','',commit+' refs/heads/main\n','metadata']):
            self.assertEqual(final.verify_git(commit),'metadata')
        for responses in ([commit+'\n',' M tools/bench_toolchain.py\n'],
                          [commit+'\n','','b'*40+' refs/heads/main\n']):
            with patch.object(final.sp,'check_output',side_effect=responses):
                with self.assertRaises(RuntimeError):final.verify_git(commit)

    def test_changed_binary_is_refused_without_execution(self):
        with patch.object(final.bench,'digest',return_value='wrong'),patch.object(final,'execute') as execute:
            with self.assertRaisesRegex(RuntimeError,'Frozen input changed'):final.verify_inputs(self.plan)
            execute.assert_not_called()

    def test_no_execution_without_run_and_user_confirmation(self):
        with patch.object(final,'execute') as execute,patch.object(final,'verify_git') as git:
            with contextlib.redirect_stdout(io.StringIO()):self.assertEqual(final.main([]),0)
            with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):final.main(['--run'])
            execute.assert_not_called();git.assert_not_called()

    def test_frozen_identity_protocol_and_case_counts(self):
        original=dict(status='MEASURED', protocol=copy.deepcopy(self.plan['reference_protocol']),
                      toolchains=self.plan['reference_toolchains'],fixture_hash=self.plan['fixture_hash'])
        for target,count in [('armv7l',13),('aarch64',10)]:
            result=copy.deepcopy(original)
            protocol=result['protocol']
            protocol.update(compile_target_filter=target,fixture_target=final.bench.TARGET,
                            harness_hash=final.bench.digest(final.bench.__file__))
            protocol['inputs']=final.bench.select_compile_cases(protocol['inputs'],target)
            self.assertEqual(len(protocol['inputs']),count)
            final.validate_run(copy.deepcopy(result),self.plan,target)
            protocol['memory_limit_bytes']*=2
            with self.assertRaises(RuntimeError):final.validate_run(result,self.plan,target)

    def simulate(self,statuses,load=1):
        plan=copy.deepcopy(self.plan);plan['output']=str(self.root/'attempt')
        plan['reference_toolchains']={}
        path=self.root/'plan.json';path.write_text(json.dumps(plan))
        seen=[]
        def execute(command,directory,monitor):
            target=directory.parent.name;seen.append((target,'--calibrate' in command))
            common=dict(protocol_hash='same',fixture_hash='same',toolchains={},status='MEASURED')
            (directory.parent/'calibration-run1.json').write_text(json.dumps(common))
            if '--calibrate' not in command:
                (directory.parent/'formal.json').write_text(json.dumps(common));return 0
            return 0 if statuses[target]=='PASS' else 2
        def calibration(directory,*_):return dict(status=statuses[directory.name],noise_floor_pct=1)
        class Monitor:
            error=None;samples=[]
            def __init__(self,*_):pass
            def __enter__(self):return self
            def __exit__(self,*_):pass
        with contextlib.ExitStack() as stack:
            for owner,name,value in [(final,'PLAN',path),(final,'LoadMonitor',Monitor)]:
                stack.enter_context(patch.object(owner,name,value))
            stack.enter_context(patch.object(final,'verify_git',return_value='mock commit'))
            stack.enter_context(patch.object(final,'verify_inputs'))
            stack.enter_context(patch.object(final,'load_sample',return_value=dict(timestamp='fixture',load1=load)))
            stack.enter_context(patch.object(final.sp,'check_output',return_value='PID COMM RSS\n1 fake 1\n'))
            stack.enter_context(patch.object(final.bench,'memory_guard',return_value=8*1024**3))
            stack.enter_context(patch.object(final,'execute',side_effect=execute))
            stack.enter_context(patch.object(final,'validate_calibration',side_effect=calibration))
            stack.enter_context(patch.object(final,'validate_run'))
            stack.enter_context(contextlib.redirect_stderr(io.StringIO()))
            rc=final.main(['--run','--quiet-window-confirmed','--preregistered-commit','0'*40])
        return rc,seen,json.loads((Path(plan['output'])/'attempt.json').read_text())

    def test_arm_failure_does_not_block_aarch64_or_trigger_retry(self):
        rc,seen,state=self.simulate({'armv7l':'FAIL','aarch64':'PASS'})
        self.assertEqual(rc,2)
        self.assertEqual(seen,[('armv7l',True),('aarch64',True),('aarch64',False)])
        self.assertFalse(state['targets']['armv7l']['formal_ran'])

    def test_passes_each_get_exactly_one_formal_run(self):
        rc,seen,_=self.simulate({'armv7l':'PASS','aarch64':'PASS'})
        self.assertEqual(rc,0)
        self.assertEqual(seen,[('armv7l',True),('armv7l',False),('aarch64',True),('aarch64',False)])

    def test_both_fail_no_formal_or_retry(self):
        rc,seen,_=self.simulate({'armv7l':'FAIL','aarch64':'FAIL'})
        self.assertEqual(rc,2)
        self.assertEqual(seen,[('armv7l',True),('aarch64',True)])

    def test_high_load_refuses_before_any_command(self):
        rc,seen,state=self.simulate({'armv7l':'PASS','aarch64':'PASS'},load=3.01)
        self.assertEqual(rc,2);self.assertEqual(seen,[])
        self.assertEqual(state['status'],'REFUSED')


if __name__=='__main__':unittest.main()
