from pathlib import Path
import sys,json
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.parent/'llvm-optimize';S=W/'temp/rebase-359934-20261106/source'
sys.path.insert(0,str(B/'tools/bolt/night-launch-20261103'))
import validate,release_checks
validate.SOURCE=S
D=W/'temp/night-20261103/basedev';O=W/'temp/third-code-review-20261109/resume/c2';O.mkdir(exist_ok=False)
R,BUILD,WORK=validate.rootpaths(D)
summary=json.loads((BUILD/'native-archive-conversion/summary.json').read_text())
release_checks.real_c2(D,O,summary)
print((O/'real-release-c2/result.json').read_text()[:1500])
