#!/usr/bin/env python3
"""Offline negative controls: final BOLT allowance cannot relax build admission."""
import contextlib
import copy
import io
import json
import unittest

import bolt_final_attempt as final
import build_llvm_x86_64 as build
import finish_bolt_final as continuation


class FinalBoltPolicy(unittest.TestCase):
    def test_bolt_allowance_does_not_leak_into_full_build(self):
        configuration = json.loads(build.BASELINE_PROFILE.read_text())['configuration']
        first = build.resource_plan(24*build.GIB, 100*build.GIB, 20, configuration)
        self.assertEqual(final.final_plan()['memory_max_gib'], 22)
        self.assertEqual(continuation.rewrite_plan()['memory_max_gib'], 22)
        # A mutated caller-owned BOLT plan also cannot mutate build policy.
        experiment = final.final_plan()
        experiment['memory_max_gib'] = 64
        second = build.resource_plan(24*build.GIB, 100*build.GIB, 20, configuration)
        for plan in [first, second]:
            self.assertEqual(plan['memory_max_gib'], 18)
            self.assertEqual([plan[k] for k in ['ninja_jobs','compile_jobs','link_jobs','debuginfo_jobs']], [4,4,1,4])
        for key, value in [('LLVM_BUILD_INSTRUMENTED', 'IR'), ('compile_jobs', 8), ('debuginfo_jobs', 40)]:
            other = copy.deepcopy(configuration)
            other[key] = value
            with self.assertRaisesRegex(RuntimeError, 'capacity evidence does not cover'):
                build.resource_plan(64*build.GIB, 100*build.GIB, 20, other)

    def test_final_entry_cannot_accept_build_command_or_cap_override(self):
        for argv in [['--run','--','gbs','build'], ['--memory-max','64'], ['--root','/a/root']]:
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
                final.parser().parse_args(argv)
            self.assertEqual(error.exception.code, 2)

    def test_only_thread_argument_changes(self):
        previous = ['/lib64/ld-linux-x86-64.so.2','--library-path','/runtime','/B/bin/llvm-bolt',
                    '/input','-instrument','--thread-count=4','-runtime-instrumentation-lib=/runtime.a',
                    '-instrumentation-file=/profiles/clang','-instrumentation-file-append-pid',
                    '-instrumentation-binpath=/output','-o','/output']
        command = final.single_thread_command(previous)
        self.assertEqual([(x,y) for x,y in zip(previous,command) if x != y],
                         [('--thread-count=4','--thread-count=1')])
        self.assertEqual(previous[6], '--thread-count=4')
        previous[3] = '/usr/bin/gbs'
        with self.assertRaises(ValueError):
            final.single_thread_command(previous)


if __name__ == '__main__':
    unittest.main(verbosity=2)
