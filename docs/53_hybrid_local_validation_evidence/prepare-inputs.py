import hashlib,json,shutil,time
from pathlib import Path
W=Path('/home/linhao/Toolchain/development/llvm-optimize');D=Path(__file__).resolve().parent;E=W/'docs/53_hybrid_local_validation_evidence';units=json.loads((W/'temp/bolt-v4-20261015-validation/object-units.json').read_text());units=[u for u in units if u['kind']=='assets90'];assert len(units)==90
out=[]
for i,u in enumerate(units):
 src=Path(u['original_host_dir'])/'input.ii';want=u['input_sha256'];assert hashlib.sha256(src.read_bytes()).hexdigest()==want
 dest=D/'tu-inputs'/f'{i:03d}.ii';dest.parent.mkdir(exist_ok=True);shutil.copyfile(src,dest);assert hashlib.sha256(dest.read_bytes()).hexdigest()==want
 out.append({'index':i,'key':u['key'],'target':u['target'],'source':str(src),'copy':str(dest),'sha256':want,'bytes':dest.stat().st_size,'original_argv':u['argv'],'provenance':u['provenance']})
(E/'tu-inputs.json').write_text(json.dumps(out,indent=2)+'\n');print('INPUTS_PASS',len(out))
