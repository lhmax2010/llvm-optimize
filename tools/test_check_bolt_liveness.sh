#!/usr/bin/env bash
# Uses existing original and strip-damaged copies; does not strip anything itself.
set -euo pipefail
if (($# != 3)); then
    echo 'Usage: test_check_bolt_liveness.sh ORIGINAL_BOLT GNU_STRIP_COPY NEW_EVIDENCE_DIR' >&2
    exit 2
fi
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
mkdir -p "$3"
"$here/check_bolt_liveness.sh" "$1" --loader /lib64/ld-linux-x86-64.so.2 --output "$3/positive"
"$here/check_bolt_liveness.sh" "$1" --host-arch x86_64 --loader /lib64/ld-linux-x86-64.so.2 --output "$3/override"
set +e
"$here/check_bolt_liveness.sh" "$1" --host-arch aarch64 --output "$3/wrong-override"
wrong_rc=$?
set -e
[[ $wrong_rc == 2 ]] || { echo "Wrong host override must be rejected: $wrong_rc"; exit 1; }
set +e
"$here/check_bolt_liveness.sh" "$2" --loader /lib64/ld-linux-x86-64.so.2 --output "$3/negative"
rc=$?
set -e
[[ $rc == 1 ]] || { echo "Expected a functional FAIL, got $rc"; exit 1; }
python3 - "$3" <<'PY'
import json,sys
from pathlib import Path
p=Path(sys.argv[1])
a=json.loads((p/'positive/result.json').read_text())
b=json.loads((p/'negative/result.json').read_text())
c=json.loads((p/'override/result.json').read_text())
d=json.loads((p/'wrong-override/result.json').read_text())
assert a['status']=='PASS' and a['version_exit']==a['compile_exit']==0
assert a['load_count']>0 and a['entry_in_executable_load'] and a['input_unchanged']
assert b['status']=='FAIL' and b['input_unchanged']
assert b['version_exit']!=0 or b['compile_exit']!=0 or not b['entry_in_executable_load']
assert a['host_arch_override']=='NO' and c['host_arch_override']=='YES'
for key in ('status','load_count','entry_in_executable_load','version_exit','compile_exit','input_unchanged','sha256'):
    assert a[key]==c[key],key
assert d['status']=='ERROR' and d['host_arch_override']=='YES'
assert all(cmd['tag']!='version' for cmd in d['commands'])
print('PASS: native / correct override equivalent; wrong override refused; strip negative; no performance measurement')
PY
