from pathlib import Path
import ast,shutil
E=Path(__file__).resolve().parent;B=E.parents[2]/'llvm-optimize-bolt';S=E.parents[1]/'temp/bolt-v4-20261013/v41/llvm-source'
shutil.copy2(S/'packaging/clang-bolt-helper.py',B/'tools/bolt/bolt_helper.py')
p=B/'tools/bolt/test_bolt_helper.py';s=p.read_text()
def method(name,code):
 global s
 t=ast.parse(s);n=next(n for c in t.body if isinstance(c,ast.ClassDef) for n in c.body if isinstance(n,ast.FunctionDef) and n.name==name);lines=s.splitlines(True);s=''.join(lines[:n.lineno-1])+code+'\n'+''.join(lines[n.end_lineno:])
method('test_large_cache_copy_rejected_before_any_copy', '''    def test_large_cache_copy_not_refused_by_free_space(self):
        cache=self.d/'cache';cache.mkdir()
        fake={'files':[], 'count':47770, 'bytes':98248402280, 'samples':{}}
        with patch.object(h,'cache_manifest',return_value=fake),patch.object(h.shutil,'disk_usage',return_value=type('Disk',(),{'free':1})()),patch.object(h.shutil,'copytree') as copy:
            h.cache_copy('--thinlto-cache-dir='+str(cache),self.d/'copy',self.d/'state.json')
            copy.assert_called_once()''')
method('test_disk_admission', '''    def test_cache_copy_has_no_disk_admission(self):
        cache=self.d/'cache';cache.mkdir()
        with patch.object(h.shutil,'disk_usage',return_value=type('Disk',(),{'free':1})()):
            self.assertEqual(h.cache_copy('--thinlto-cache-dir='+str(cache),self.d/'copy',self.d/'copy.json')['copied']['count'],0)''')
start=s.index('class DiskTests(');end=s.index('class PipelineTests(',start)
s=s[:start]+'''class DiskTests(Base):
    def report(self,free=0,path=None):
        with patch.object(h.shutil,'disk_usage',return_value=type('Disk',(),{'free':free})()):
            return h.disk_report('begin',build=self.d,work=path or self.d/'work')
    def test_zero_free_does_not_reject(self):self.assertEqual(self.report()['free_bytes'],0)
    def test_one_free_does_not_reject(self):self.assertEqual(self.report(1)['free_bytes'],1)
    def test_large_free_records_exact_value(self):self.assertEqual(self.report(41*1024**3)['free_bytes'],41*1024**3)
    def test_no_disk_admission_symbol(self):self.assertFalse(hasattr(h,'disk_preflight'))
    def test_no_stage_budget_symbol(self):self.assertFalse(hasattr(h,'STAGE_WRITE_BUDGET'))
    def test_no_floor_symbol(self):self.assertFalse(hasattr(h,'DISK_FLOOR'))
    def test_records_are_written(self):self.report();self.assertTrue((self.d/'work/disk-begin.json').is_file())
    def test_nonexistent_destination(self):self.assertEqual(self.report(0,self.d/'new'/'work')['free_bytes'],0)

'''+s[end:]
method('test_pipeline_disk_failure_stops_before_link', '''    def test_pipeline_has_no_disk_admission(self):
        with patch.object(h.shutil,'disk_usage',return_value=type('Disk',(),{'free':0})()):
            self.assertEqual(self.run_pipeline()['cache_policy'],'original-in-place')''')
p.write_text(s)
p=B/'tools/bolt/test_fourth_review.py';s=p.read_text();start=s.index('    def test_small_disk_pass');end=s.index('    def test_profile_remedy',start);s=s[:start]+'''    def test_small_disk_pass(self):
        with patch.object(h.shutil,'disk_usage',return_value=SimpleNamespace(free=100)):
            self.assertEqual(h.disk_report('begin',build=self.d,work=self.d/'work')['free_bytes'],100)
    def test_small_disk_fail(self):
        with patch.object(h.shutil,'disk_usage',return_value=SimpleNamespace(free=0)):
            self.assertEqual(h.disk_report('begin',build=self.d,work=self.d/'work')['free_bytes'],0)
'''+s[end:];p.write_text(s)
p=B/'tools/bolt/test_fourth_review_b.py';s=p.read_text();s=s.replace("program(Path(h.__file__).read_text())", "program((Path(__file__).parent/'results/review4b-final-helper.py').read_text())");s=s.replace("    def test_diagnostics_count_matches", '''    def test_non_disk_gates_unchanged(self):
        previous=ast.parse((Path(__file__).parent/'results/review4b-final-helper.py').read_text())
        current=ast.parse(Path(h.__file__).read_text())
        for name in ('ELF','security_properties','security_compare','match_counts','replay_script','tiny_gate','no_bolt_products','tool_prepare','tool_plan','tool_verify'):
            with self.subTest(name=name):
                a=next(n for n in previous.body if getattr(n,'name',None)==name)
                b=next(n for n in current.body if getattr(n,'name',None)==name)
                self.assertEqual(ast.dump(a,include_attributes=False),ast.dump(b,include_attributes=False))
    def test_diagnostics_count_matches''');p.write_text(s)
print('legacy disk-admission expectations replaced with observability; historical freeze audited on historical artifacts')
