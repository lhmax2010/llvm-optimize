from pathlib import Path
import difflib,shutil,json
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';E=W/'temp/final-20261103/continue-20261103';p=B/'tools/bolt/final-launch-20261103/launcher.py';s=p.read_text();(E/'launcher.attempt1.py').write_text(s)
R=W/'temp/final-20261103/basedev-rehearsal/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
shutil.copyfile(R/'.build.log',E/'basedev-attempt1-authoritative-build.log')
# Track the last read bytes as well as length: GBS can truncate/regrow the same inode.
needle='            marker = "    if b\'BOLT_GATE_FAILED:\' in b and reason is None:"'
addition='''            text = text.replace(" position=0\\n", " position=0;anchor=b''\\n")
            text = text.replace("    src.seek(position);b=src.read();position+=len(b)",
                                "    src.seek(max(0,position-len(anchor)))\\n"
                                "    if src.read(len(anchor))!=anchor or p.stat().st_size<position:\\n"
                                "     append('log-restarts.jsonl',{'time_ns':time.time_ns(),'old_position':position});position=0\\n"
                                "    src.seek(position);b=src.read();position+=len(b)\\n"
                                "    src.seek(max(0,position-128));anchor=src.read(min(position,128))")
'''
assert needle in s;s=s.replace(needle,addition+needle)
needle="     append('cmake-stop.jsonl',{'stop_rc':result.returncode,'stdout':result.stdout,'stderr':result.stderr,'time_ns':time.time_ns()})\n     return"
assert needle in s
s=s.replace(needle,"     append('cmake-stop.jsonl',{'stop_rc':result.returncode,'stdout':result.stdout,'stderr':result.stderr,'time_ns':time.time_ns()})\n     shutil.copyfile(p,E/'rpm-build-final.log')\n     return")
s=s.replace("log = (E / 'rpm-build.log').read_text(errors='replace')", "log = (E / 'rpm-build-final.log').read_text(errors='replace')")
p.write_text(s);compile(s,str(p),'exec')
(E/'launcher-logging-fix.diff').write_text(''.join(difflib.unified_diff((E/'launcher.attempt1.py').read_text().splitlines(True),s.splitlines(True),fromfile='attempt1',tofile='retry')))
# Keep an overall readable diff from the certified launcher as well.
old=B/'tools/bolt/debuglink-launch-20261030/launcher.py'
(E/'launcher-final.diff').write_text(''.join(difflib.unified_diff(old.read_text().splitlines(True),s.splitlines(True),fromfile=str(old),tofile=str(p))))
# Verify materialized run.py syntax without starting any service.
import importlib.util
spec=importlib.util.spec_from_file_location('local_launcher',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
probe=E/'launcher-syntax-probe';probe.mkdir();(probe/'evidence').mkdir()
m.materialize(probe,{'prep_unit':'syntax-prep.service','build_unit':'syntax-build.service'})
assert "anchor=b''" in (probe/'run.py').read_text() and "rpm-build-final.log" in (probe/'run.py').read_text()
print('LOGGING_FIX_MATERIALIZATION_SYNTAX_PASS')
