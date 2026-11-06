"""Continue only release checks blocked by the local payload-overlap bug."""
from pathlib import Path
import sys,json,datetime,traceback
from release_checks import release_checks
from validate import rootpaths
from log_support import canonical_log,log_summary
from checks import save
D=Path(sys.argv[1]);O=D/'validation-02/release-check-resume';O.mkdir(exist_ok=False);status='failed';reason=''
try:
 identity=json.loads((rootpaths(D)[2]/'identity.json').read_text());release_checks(D,O,D.parent/'toolchain',log_summary(canonical_log(D))['selected'],identity);status='ok'
except BaseException as e:
 reason='memory-stop' if isinstance(e,MemoryError) else 'see-failure';(O/'failure.txt').write_text(traceback.format_exc());traceback.print_exc()
finally:
 save(O/'result.json',dict(status=status,reason=reason));line='RELEASE_RECHECK 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status='+status+' reason='+reason;(O/'ended.txt').write_text(line+'\n');print(line,flush=True)
sys.exit(0 if status=='ok' else 1)
