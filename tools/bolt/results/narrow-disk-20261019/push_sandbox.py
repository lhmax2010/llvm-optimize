from pathlib import Path
import subprocess,json,sys
E=Path(__file__).resolve().parent;W=E.parents[1];S=W/'temp/bolt-v4-20261013/v41/llvm-source';release=json.loads((E/'release.json').read_text());new=release['commit'];base=release['base'];ref='refs/heads/sandbox/lhmax2025/bolt_pgo'
assert json.loads((E/'structure-result.json').read_text())['PASS']
assert json.loads((E/'shell-failure.json').read_text())['PASS']
assert json.loads((E/'material-verification.json').read_text())['PASS']
parse=json.loads((E/'parse-results.json').read_text());assert parse['status']=='PASS' and parse['lower_unchanged'] and len(parse['matrix'])==5 and all(r['PASS'] for r in parse['matrix'])
assert 'Ran 289 tests' in (E/'tests.stderr').read_text() and (E/'tests.stderr').read_text().rstrip().endswith('OK')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=S,text=True).strip()==new
assert subprocess.check_output(['git','status','--porcelain'],cwd=S)==b''
def query(label):
 a=['git','ls-remote','origin',ref];p=subprocess.run(a,cwd=S,capture_output=True,text=True);(E/(label+'.stdout')).write_text(p.stdout);(E/(label+'.stderr')).write_text(p.stderr)
 assert p.returncode==0,p.stderr
 return p.stdout.split()[0] if p.stdout.strip() else None
before=query('push-before');assert before==base,repr(before)
argv=['git','push','--force-with-lease='+ref+':'+base,'origin',new+':'+ref];p=subprocess.run(argv,cwd=S,capture_output=True,text=True)
(E/'push.stdout').write_text(p.stdout);(E/'push.stderr').write_text(p.stderr)
value={'argv':argv,'rc':p.returncode,'before':before,'expected':new,'stdout':p.stdout,'stderr':p.stderr,'after':None}
(E/'push-result.json').write_text(json.dumps(value,indent=2)+'\n');print(p.stdout,end='');print(p.stderr,end='',file=sys.stderr)
if p.returncode:sys.exit(p.returncode)
value['after']=query('push-after');value['PASS']=value['after']==new;(E/'push-result.json').write_text(json.dumps(value,indent=2)+'\n');assert value['PASS'];print('REMOTE_VERIFIED '+value['after'])
