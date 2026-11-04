from pathlib import Path
import os,json,hashlib,shutil,subprocess,ast,datetime
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';P=W/'temp/pgo-bolt-followup-20261105';E=B/'tools/bolt/results/pgo-bolt-followup-20261105'
P.mkdir(exist_ok=False);D=W/'temp/pgo-resource-20261102/full/stage-D/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';b=D/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build';rows=[]
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
for src in [b/'clang-bolt/reference-relocs-clang-22',b/'bin/llvm-bolt']:
 dst=P/src.name;shutil.copyfile(src,dst);os.chmod(dst,src.stat().st_mode&0o777);a=sha(src);assert sha(dst)==a;rows.append({'source':str(src),'copy':str(dst),'bytes':src.stat().st_size,'sha256':a})
scan=subprocess.run(['find',str(D),'-name','merge-fdata','-o','-name','libbolt_rt*'],capture_output=True,text=True);(E/'tool-search.stdout').write_text(scan.stdout);(E/'tool-search.stderr').write_text(scan.stderr)
found=[{'path':p,'is_file':Path(p).is_file(),'executable':os.access(p,os.X_OK)} for p in scan.stdout.splitlines()]
source=W/'temp/debuglink-tb20261026/source/packaging/clang-bolt-helper.py';tree=ast.parse(source.read_text());opts=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='OPTIONS' for t in n.targets))
(E/'identities.json').write_text(json.dumps(rows,indent=2)+'\n');(E/'options.json').write_text(json.dumps({'helper':str(source),'helper_sha256':sha(source),'OPTIONS':opts,'pipeline_input_argv':json.loads((b/'clang-bolt/rewrite/bolt.log.argv.json').read_text()),'reference_strip_argv':json.loads((b/'clang-bolt/reference-strip.log.argv.json').read_text()),'search':found,'search_rc':scan.returncode},indent=2)+'\n')
training=W/'temp/pgo-resource-20261102/preflight/training.json';shutil.copyfile(training,E/'training.json')
result={'status':'stopped','reason':'D-root lacks executable merge-fdata and BOLT instrumentation runtime; no tool substitution or rebuild authorized','not_run':['BOLT instrumentation','training','merge','optimized rewrite'],'copies':rows}
(E/'result.json').write_text(json.dumps(result,indent=2)+'\n');line='ITEM1 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status=stopped reason=missing-D-root-merge-fdata-and-instrumentation-runtime';(E/'end.txt').write_text(line+'\n');print(line,flush=True)
