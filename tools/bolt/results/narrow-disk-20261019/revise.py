from pathlib import Path
import subprocess,ast,re,json,shutil
E=Path(__file__).parent;W=E.parents[1];S=W/'temp/bolt-v4-20261013/v41/llvm-source';B=W.parent/'llvm-optimize-bolt';base='e2463165829cc91b0a1d60a3e0f915a587865f70'
def get(*args):return subprocess.check_output(['git',*args],cwd=S)
assert get('status','--porcelain')==b''
oldhelper=get('show','e97171ff:packaging/clang-bolt-helper.py').decode();basehelper=get('show',base+':packaging/clang-bolt-helper.py').decode();spec=get('show',base+':packaging/llvm.spec').decode()
(E/'base-llvm.spec').write_text(spec);(E/'e971-helper.py').write_text(oldhelper);(E/'base-helper.py').write_text(basehelper)
remote=get('ls-remote','origin','refs/heads/sandbox/lhmax2025/bolt_pgo');(E/'remote-before.txt').write_bytes(remote);assert remote.decode().split()[0]==base
subprocess.run(['git','checkout','--detach',base],cwd=S,check=True)
def function(text,name):
 node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name==name)
 return '\n'.join(text.splitlines()[node.lineno-1:node.end_lineno])
def replace_function(text,name,new):return text.replace(function(text,name),new,1)
call=function(basehelper,'call')
call=call.replace("        return log.read_text(errors='replace')", "        text = log.read_text(errors='replace')\n        metadata = log.with_suffix(log.suffix+'.argv.json')\n        invocation = json.loads(metadata.read_text())\n        save(metadata, dict(invocation,completed=True,rc=0))\n        return text")
call=call.replace('        raise GateError(message) from error', "        failure = GateError(message)\n        failure.bolt_log = str(log)\n        raise failure from error")
helper=replace_function(oldhelper,'call',call).replace('import threading\n','')
peek=function(basehelper,'peek_child_exit').replace('deadline = time.monotonic()+timeout','deadline = time.monotonic()+timeout if timeout is not None else None').replace('if time.monotonic() >= deadline:', 'if deadline is not None and time.monotonic() >= deadline:')
helper=replace_function(helper,'peek_child_exit',peek)
# Consume a failure log only once, including /dev/stdin.
needle='def disk_evidence(log, error=None):'
helper=helper.replace(needle,"""def disk_failure_log(log):
    try:
        text = Path(log).read_text(errors='replace') if log and str(log) != '-' else ''
        return text, bool(text.strip())
    except (OSError, ValueError):
        return '', False


def disk_evidence(log, error=None, log_text=None):""",1)
old="""    try:
        text = Path(log).read_text(errors='replace') if log and str(log) != '-' else ''
        evidence += [pattern for pattern in DISK_LOG_MATCHES if re.search(pattern, text, re.I)]
    except Exception: pass
"""
new="""    text = disk_failure_log(log)[0] if log_text is None else log_text
    evidence += [pattern for pattern in DISK_LOG_MATCHES if re.search(pattern, text, re.I)]
"""
assert old in helper;helper=helper.replace(old,new,1)
diag=function(helper,'disk_diagnose')
diag=diag.replace("    cause = 'disk' if disk_evidence(log, error) else 'not-disk'", "    text, available = disk_failure_log(log)\n    evidence = disk_evidence(log,error,log_text=text)\n    cause = 'disk' if evidence else ('not-disk' if available else 'unknown')")
diag=diag.replace("    value = {'cause': cause, 'step': step, 'free_bytes': None}","    value = {'cause': cause, 'step': step, 'free_bytes': None}\n    if cause == 'unknown':\n        value.update(used_bytes=None,reason='日志不可用，无法判定原因')")
diag=diag.replace("        if cause == 'disk':\n            value.update", "        if cause in ('disk','unknown'):\n            value.update",1)
diag=diag.replace('evidence=disk_evidence(log,error),','evidence=evidence,').replace("for item in disk_evidence(log,error) if item.startswith('errno=')", "for item in evidence if item.startswith('errno=')")
# Unknown does not include forecast, or a misleading estimated-size note.
diag=diag.replace("            if baseline is None:\n                value.update", "            if cause == 'unknown':\n                for key in ('evidence','estimate_note','errno_messages','cache_delta_known','filesystem_device'):\n                    value.pop(key,None)\n            elif baseline is None:\n                value.update",1)
diag=diag.replace("        if cause == 'disk':\n            value['degraded']=str(failure)", "        if cause in ('disk','unknown'):\n            value['degraded']=str(failure)")
helper=replace_function(helper,'disk_diagnose',diag)
# Restore baseline spec; only explicitly allowed BOLT commands receive wrappers.
functions='''BOLT_BUILD="$PWD"
BOLT_WORK="$PWD/clang-bolt"
BOLT_INSTALL_ROOT="%{buildroot}"
BOLT_PROFILE_SOURCE="%{SOURCE1200}"
export BOLT_BUILD BOLT_WORK BOLT_INSTALL_ROOT BOLT_PROFILE_SOURCE
bolt_fail() {
  python3 -B %{SOURCE1201} disk-diagnose "$1" "$2" || true
  exit 1
}
bolt_checked() {
  bolt_stage=$1
  bolt_log=$2
  shift 2
  if bolt_output=$("$@" 2>&1); then
    printf '%%s\\n' "$bolt_output" || bolt_fail "$bolt_stage-output" -
  else
    printf '%%s\\n' "$bolt_output" || true
    printf '%%s\\n' "$bolt_output" | python3 -B %{SOURCE1201} disk-diagnose "$bolt_stage" /dev/stdin || true
    exit 1
  fi
}
bolt_step() {
  bolt_stage=$1
  shift
  bolt_checked "$bolt_stage" "$BOLT_WORK/$bolt_stage.log" python3 -B %{SOURCE1201} run-step "$bolt_stage" "$BOLT_WORK/$bolt_stage.log" -- "$@"
}
python3 -B %{SOURCE1201} disk-report begin
'''
spec=spec.replace('echo "BOLT_BUILDROOT_OK %{buildroot}"\n',functions+'echo "BOLT_BUILDROOT_OK %{buildroot}"\n',1)
spec=spec.replace('# Default 16 GiB BOLT-stage write budget must leave 30 GiB on this filesystem.\nBOLT_WORK="$PWD/clang-bolt"\n','')
spec='\n'.join(l for l in spec.split('\n') if ' disk-preflight ' not in l)
spec=spec.replace('python3 %{SOURCE1201}', 'python3 -B %{SOURCE1201}')
spec=spec.replace('cp install_manifest.txt "$BOLT_WORK/install-manifest-before.txt" || exit 1','bolt_step manifest-copy cp install_manifest.txt "$BOLT_WORK/install-manifest-before.txt"')
spec=spec.replace('cp -p bin/clang-22 "$BOLT_WORK/ordinary-clang-22" || exit 1','bolt_step ordinary-copy cp -p bin/clang-22 "$BOLT_WORK/ordinary-clang-22"')
spec=spec.replace('ninja -t commands -s bin/clang-22 > "$BOLT_WORK/link.original" || exit 1', 'bolt_checked link-command "$BOLT_WORK/link-command.log" python3 -B %{SOURCE1201} run-step link-command "$BOLT_WORK/link-command.log" --output "$BOLT_WORK/link.original" -- ninja -t commands -s bin/clang-22')
spec=spec.replace('cmake -S ../llvm -B . \\\n','bolt_step configure cmake -S ../llvm -B . \\\n',1)
spec=spec.replace('-DBOLT_INCLUDE_TESTS=OFF -DBOLT_TARGETS_TO_BUILD=X86 || exit 1','-DBOLT_INCLUDE_TESTS=OFF -DBOLT_TARGETS_TO_BUILD=X86',1)
start=spec.index("if LC_ALL=C NINJA_STATUS='[%%f/%%t] ' ninja -n llvm-bolt")
end=spec.index('python3 -B %{SOURCE1201} tool-plan',start)
spec=spec[:start]+'''bolt_step dry-run-begin /bin/echo BOLT_TOOL_DRY_RUN_BEGIN
LC_ALL=C NINJA_STATUS='[%%f/%%t] ' bolt_checked tool-dry-run "$BOLT_WORK/tool-dry-run.log" python3 -B %{SOURCE1201} run-step tool-dry-run "$BOLT_WORK/tool-dry-run.log" --output "$BOLT_WORK/tool-dry-run.txt" -- ninja -n llvm-bolt
bolt_step dry-run-end /bin/echo BOLT_TOOL_DRY_RUN_END
'''+spec[end:]
start=spec.index("if LC_ALL=C NINJA_STATUS='[%%f/%%t] ' ninja -j 1 llvm-bolt")
end=spec.index('python3 -B %{SOURCE1201} tool-verify',start)
spec=spec[:start]+'''LC_ALL=C NINJA_STATUS='[%%f/%%t] ' bolt_checked tool-build "$BOLT_WORK/tool-build.txt" python3 -B %{SOURCE1201} run-step tool-build "$BOLT_WORK/tool-build.txt" --success-marker BOLT_NINJA_EXIT_0 -- ninja -j 1 llvm-bolt
'''+spec[end:]
spec=spec.replace('python3 -B %{SOURCE1201} pipeline', 'python3 -B %{SOURCE1201} disk-report tool-built\npython3 -B %{SOURCE1201} pipeline',1)
spec=spec.replace('echo BOLT_PIPELINE_PASS\n','echo BOLT_PIPELINE_PASS\npython3 -B %{SOURCE1201} disk-report pipeline\n',1)
spec=spec.replace('    echo BOLT_POST_GATE_PASS\n', '    echo BOLT_POST_GATE_PASS \\\n    python3 -B %{SOURCE1201} disk-report post\n',1)
assert '__bolt_disk_reporting' not in spec and 'bolt_capture' not in spec and spec.count('disk-report ')==4
(S/'packaging/llvm.spec').write_text(spec);(S/'packaging/clang-bolt-helper.py').write_text(helper);(B/'tools/bolt/bolt_helper.py').write_text(helper)
(E/'spec.diff').write_bytes(get('diff','--','packaging/llvm.spec'));(E/'helper.diff').write_bytes(get('diff','--','packaging/clang-bolt-helper.py'))
print('base reconstructed, helper direct-output call restored')
