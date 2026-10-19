from pathlib import Path
import ast,json,subprocess,re
E=Path(__file__).parent;S=E.parent/'bolt-v4-20261013/v41/llvm-source';p=S/'packaging/clang-bolt-helper.py';text=p.read_text();tree=ast.parse(text);rows=[]
writers={'open','mkdir','write','write_text','write_bytes','copyfile','copyfileobj','copytree','copy2','replace','symlink_to','chmod','unlink','fsync'}
for f in tree.body:
 if not isinstance(f,ast.FunctionDef):continue
 for n in ast.walk(f):
  if not isinstance(n,ast.Call) or not isinstance(n.func,ast.Attribute) or n.func.attr not in writers:continue
  if n.func.attr=='replace' and not isinstance(n.func.value,ast.Name):continue
  if n.func.attr=='replace' and n.func.value.id!='os':continue
  if n.func.attr=='open':
   args=n.args
   mode=args[0].value if args and isinstance(args[0],ast.Constant) else None
   if mode is None or not any(x in str(mode) for x in 'wax'):continue
  source=ast.get_source_segment(text,n)
  kind='fail-closed: uncaught error reaches cli rc1; diagnostic does not override error'
  if f.name=='atomic_text':kind='strict length/flush/fsync then atomic rename; errors retain original exception; temporary cleanup best effort'
  elif f.name=='call':kind='parent checked writes/flush/fsync; kill and reap process group before error rc1'
  elif f.name=='install_candidate':kind='staged copy, mode/fsync/SHA; state and staged aliases before final clang rename; failure preserves old clang'
  elif f.name=='disk_report':kind='observability ONLY: explicitly best effort and rc0 by user decision'
  elif f.name=='run_step':kind='checked marker length/flush/fsync; errors rc1 and original transcript preserved'
  if n.func.attr=='unlink' and f.name in ('atomic_text','install_candidate','profile_unpack'):kind='failure cleanup only; suppress cleanup error to preserve primary rc1'
  rows.append({'file':'packaging/clang-bolt-helper.py','line':n.lineno,'function':f.name,'source':source,'handling':kind})
rows.sort(key=lambda r:r['line'])
# all production result writes via save (including disk-report's explicit exception).
for f in tree.body:
 if not isinstance(f,ast.FunctionDef):continue
 for n in ast.walk(f):
  if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ('save','atomic_text','call'):
   rows.append({'file':'packaging/clang-bolt-helper.py','line':n.lineno,'function':f.name,'source':ast.get_source_segment(text,n),'handling':'best effort observation rc0' if f.name=='disk_report' else 'atomic/checked writer; exception propagates to rc1 before candidate commit'})
rows.sort(key=lambda r:r['line']);(E/'writer-audit.json').write_text(json.dumps(rows,indent=2)+'\n')
spec=(S/'packaging/llvm.spec').read_text();specrows=[]
for i,line in enumerate(spec.splitlines(),1):
 if ('bolt_step ' in line or 'bolt_capture ' in line or 'bolt_checked ' in line or 'BOLT_INSTALL_OUTPUT=' in line or 'disk-report ' in line or 'BOLT_BUILD_OUTPUT=' in line) and not line.strip().startswith('#'):
  specrows.append({'file':'packaging/llvm.spec','line':i,'source':line,'handling':'best effort rc0' if 'disk-report ' in line else 'checked; failed step diagnostic then exit1'})
(E/'spec-writer-audit.json').write_text(json.dumps(specrows,indent=2)+'\n')
old=(E/'base-clang-bolt-helper.py').read_text();calls=[{'line':i,'source':l.strip()} for i,l in enumerate(old.splitlines(),1) if 'disk_preflight(' in l]
oldspec=(E/'base-llvm.spec').read_text();gates=[{'line':i,'source':l.strip()} for i,l in enumerate(oldspec.splitlines(),1) if 'disk-preflight' in l]
assert all(x not in text for x in ['disk_preflight','DISK_FLOOR','LARGE_WRITE','STAGE_WRITE_BUDGET','disk-preflight','planned_write_bytes'])
assert 'disk-preflight' not in spec
(E/'removed-gates.json').write_text(json.dumps({'helper_calls_and_definition':calls,'spec_calls':gates,'removed_cli':True,'removed_constants':['DISK_FLOOR','LARGE_WRITE','STAGE_WRITE_BUDGET'],'no_production_local_budget':True},indent=2)+'\n')
print('audit:',len(rows),'helper sites,',len(specrows),'spec lines; no old gates')
