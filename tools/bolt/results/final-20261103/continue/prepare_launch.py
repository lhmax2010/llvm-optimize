from pathlib import Path
import json,hashlib,shutil,subprocess,difflib
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=W/'temp/final-20261103';E=D/'continue-20261103';T=B/'tools/bolt/final-launch-20261103';T.mkdir(exist_ok=True)
old=B/'tools/bolt/debuglink-launch-20261030';s=(old/'launcher.py').read_text()
s=s.replace("SOURCE = W / 'temp/debuglink-tb20261026/source'", "SOURCE = W / 'temp/review-20261102/source'")
s=s.replace('3ee2d84719e4bd358c0b2366161f70f2eb788313','a379c766e17d12ba7738ff6079adb39645c0a740').replace('43d60f7523439fa0ccf4a61f668dd60622554606','37c8c6d3f249b5948db1517d84a79a4d53c9a112')
a=s.index('CONFIG = ');z=s.index('LOCK = ',a)
s=s[:a]+'''PROJECT = os.environ.get('FINAL_PROJECT', 'toolchain')
assert PROJECT in ('toolchain', 'basedev')
CONFIG = W / ('temp/final-20261103/configs/' + PROJECT + '/gbs.conf')
BUILDCONF = CONFIG.parent / 'build.conf'
BUILD_SHA = {'toolchain':'e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945',
             'basedev':'8ace286a5f98f2e02a79be275a64c22a86ea2b0034174c1e293381e181ce3f6a'}[PROJECT]
'''+s[z:]
s=s.replace("    save(D / 'export-command.json', export)","    export[export.index('-c') + 1] = str(CONFIG)\n    save(D / 'export-command.json', export)")
s=s.replace("    D = W / ('temp/debuglink-20261028/' + mode + '-20261030')", "    D = W / ('temp/final-20261103/' + (PROJECT if mode == 'full' else PROJECT + '-rehearsal'))")
s=s.replace("'debuglink-' + mode", "'final-flags-' + PROJECT + '-' + mode").replace("'-prep-20261030'", "'-prep-20261103'").replace("'-20261030' + suffix", "'-20261103' + suffix").replace("'-controller-20261030'", "'-controller-20261103'")
s=s.replace("'--setenv=TMPDIR=' + str(D / 'tmp'),", "'--setenv=FINAL_PROJECT=' + PROJECT, '--setenv=TMPDIR=' + str(D / 'tmp'),")
s=s.replace("print('DEBUGLINK FINISHED',", "print('FINAL_PROJECT_FLAGS 已结束',")
# Parameterize only the local identity monitor: Base-Dev release is not claimed to
# have Toolchain's identity. Production helper gates remain untouched.
needle='        (D / name).write_text(text)'
s=s.replace(needle,"        if name == 'run.py' and PROJECT == 'basedev':\n            text = text.replace(\"if file.exists() and reason is None:\", \"if False and file.exists() and reason is None:\")\n"+needle)
(T/'launcher.py').write_text(s);compile(s,str(T/'launcher.py'),'exec')
(T/'launch.sh').write_text('''#!/bin/sh
set -eu
case ${1-} in toolchain|basedev) FINAL_PROJECT=$1; export FINAL_PROJECT ;; *) echo 'usage: launch.sh toolchain|basedev rehearsal|full' >&2; exit 2 ;; esac
shift
exec python3 -B "$(dirname "$0")/launcher.py" "$@"
''')
(T/'provenance.json').write_bytes((old/'provenance.json').read_bytes())
(E/'launcher.diff').write_text(''.join(difflib.unified_diff((old/'launcher.py').read_text().splitlines(True),s.splitlines(True),fromfile=str(old/'launcher.py'),tofile=str(T/'launcher.py'))))
for project,path in [('toolchain',W/'temp/bolt-v4-20261021-disk-footprint/build.conf'),('basedev',B/'tools/bolt/results/qb-20261102/configs/base-dev-build.conf')]:
 c=D/'configs'/project;c.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,c/'build.conf')
 branch,snap=('Tizen-Base-Toolchain','tizen-base-toolchain_20261013.024319') if project=='toolchain' else ('Tizen-Base-Dev','tizen-base-dev_20261030.061217')
 url='http://download.tizen.org/snapshots/TIZEN/Tizen/'+branch+'/'+snap+'/repos/standard/'
 # Retain established driver profile key; repository URLs and build.conf carry project identity.
 (c/'gbs.conf').write_text('[general]\nprofile = profile.tizen-base-toolchain_standard\nbuildroot = '+str(D/project/'gbs-driver')+'\n\n[profile.tizen-base-toolchain_standard]\nbuildconf = '+str(c/'build.conf')+'\nrepos = repo.base_0,repo.base_debug_0\n\n[repo.base_0]\nurl = '+url+'packages/\n\n[repo.base_debug_0]\nurl = '+url+'debug/\n')
subprocess.run(['/bin/sh','-n',str(T/'launch.sh')],check=True)
free=shutil.disk_usage('/home').free;peak=68252237824;reserve=20*1024**3
# Both complete measured roots +20% estimate margin +20 GiB runtime reserve.
need=(2*peak*120+99)//100+reserve
row={'historical_root_peak_bytes':peak,'two_roots_bytes':2*peak,'margin_percent':20,'reserve_bytes':reserve,'required_bytes':need,'available_bytes':free,'PASS':free>=need}
(E/'disk-budget.json').write_text(json.dumps(row,indent=2)+'\n');print(row);assert row['PASS']
