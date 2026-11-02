from common import *
import sys
D=Path(sys.argv[1]);rows=json.loads((D/'training-commands.json').read_text());out=D/'evidence/B'
for i,row in enumerate(rows):
 env=os.environ.copy();env['LLVM_PROFILE_FILE']=row['LLVM_PROFILE_FILE']
 call(row['argv'],out/(str(i)+'-'+row['name']+'.stdout'),env=env)
 p=Path(row['argv'][-1]);assert p.is_file() and p.stat().st_size
 assert list((D/'profiles').glob(str(i)+'-*.profraw')), 'missing profile for '+row['name']
 print('PGO_TRAIN',i,row['name'],'PASS',flush=True)
