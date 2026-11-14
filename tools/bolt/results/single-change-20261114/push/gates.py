from pathlib import Path
import subprocess,json,re,os,hashlib,difflib,datetime
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.parent/'llvm-optimize';E=Path(__file__).resolve().parent
N=W/'temp/single-change-20261114/source';X=N.parent
R=W/'temp/review-20261103/config-root/local/BUILD-ROOTS/scratch.x86_64.0'
M=B/'tools/bolt/results/fifth-review-20261111/rerun4/parse'
def now():return datetime.datetime.now().astimezone().isoformat(timespec='seconds')
def run(name,args,cwd=N,env=None):
 p=subprocess.run(args,cwd=cwd,env=env,capture_output=True)
 (E/(name+'.stdout')).write_bytes(p.stdout);(E/(name+'.stderr')).write_bytes(p.stderr)
 (E/(name+'.json')).write_text(json.dumps({'argv':args,'cwd':str(cwd),'rc':p.returncode,'time':now()},indent=2)+'\n')
 if p.returncode:raise RuntimeError(name+': rc='+str(p.returncode)+' '+p.stderr.decode(errors='replace'))
 return p.stdout

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def compare(label,old,new):
 maps=[]
 for root in [old,new]:
  d={str(p.relative_to(root)):{'sha256':digest(p),'bytes':p.stat().st_size,'mode':p.stat().st_mode&0o7777} for p in root.rglob('*') if p.is_file()}
  maps.append(d)
 a,b=maps;pa=next(old.glob('0008-*.patch'));pb=next(new.glob('0008-*.patch'))
 assert set(a)-{pa.name}==set(b)-{pb.name},'file set'
 report=[]
 for name in sorted(a):
  other=pb.name if name==pa.name else name
  aa=(old/name).read_bytes();bb=(new/other).read_bytes()
  assert a[name]['mode']==b[other]['mode'],('mode',name)
  category='identical'
  if aa!=bb:
   if name in ['llvm.spec','libcxx-runtimes.spec']:
    def normalize(data,newname):
     lines=data.decode().splitlines(True)
     for i,line in enumerate(lines):
      if re.match(r'^VCS\s*:',line):lines[i]='VCS: #IDENTITY\n'
      elif re.match(r'^Patch7\s*:',line) or line.strip()=='# '+newname:lines[i]=line.replace(newname,pa.name)
     return ''.join(lines)
    assert normalize(aa,pa.name)==normalize(bb,pb.name),('spec unexpected',name)
    category='R2(e): VCS and Patch7/comment filename only'
   elif name==pa.name:
    i=aa.index(b'diff --git ');j=bb.index(b'diff --git ')
    assert aa[i:]==bb[j:],'0008 code'
    assert aa.split(b'Subject:',1)[0]==bb.split(b'Subject:',1)[0],'0008 prefix outside Subject/message'
    category='R2(e): patch filename and Subject/message only'
   else:raise AssertionError(('unallowed changed file',name))
   (E/(label+'-'+name+'.diff')).write_text(''.join(difflib.unified_diff(aa.decode().splitlines(True),bb.decode().splitlines(True),fromfile=str(old/name),tofile=str(new/other))))
  report.append({'old':name,'new':other,'category':category,'old_file':a[name],'new_file':b[other]})
 (E/(label+'-comparison.json')).write_text(json.dumps({'PASS':True,'rows':report,'patch_code_sha256':hashlib.sha256(pa.read_bytes().split(b'diff --git ',1)[1]).hexdigest()},indent=2)+'\n')
 return pa.name,pb.name

def parse_pair(label,old,new,oldpatch,newpatch):
 P=E/(label+'-parse');P.mkdir()
 env=dict(os.environ,RPM_CONFIGDIR=str(R/'usr/lib/rpm'),LC_ALL='C',HOME=str(P))
 loader=[str(R/'usr/lib64/ld-linux-x86-64.so.2'),'--library-path',str(R/'usr/lib64')]
 show=run(label+'-rpm-showrc',loader+[str(R/'usr/bin/rpmspec'),'--showrc'],P,env).decode()
 macrobase=next(x.split(': ',1)[1] for x in show.splitlines() if x.startswith('Macro path:'))
 macrobase=':'.join(x for x in macrobase.split(':') if x.startswith(str(R)))
 assert macrobase
 results=[]
 for case,arch,off,rollback in [('x86-on','x86_64',False,False),('x86-off','x86_64',True,False),('armv7l','armv7l',False,False),('aarch64','aarch64',False,False),('x86-rollback','x86_64',False,True)]:
  key='toolchain-'+('x86-debug' if arch=='x86_64' else arch)
  macro=P/(key+'.macros')
  if not macro.exists():macro.write_bytes((M/(key+'.macros')).read_bytes())
  outputs={}
  for side,src in [('old',old),('new',new)]:
   sp=src/'llvm.spec'
   if rollback:
    raw=sp.read_text();assert raw.count('%bcond_without clang_bolt')==1
    sp=P/(side+'-rollback.spec');sp.write_text(raw.replace('%bcond_without clang_bolt','%bcond_with clang_bolt',1))
   common=['--define','_topdir '+str(P/side),'--define','_builddir '+str(P/side/'BUILD'),'--macros',macrobase+':'+str(macro),'--target',arch+'-tizen-linux','--define','_sourcedir '+str(src),'--define','_toolchain clang']
   tag=label+'-'+case+'-'+side
   # Parsing only: --nobuild forbids executing prep/build shell stages.
   run(tag+'-nobuild',loader+[str(R/'usr/bin/rpmbuild'),'-bp','--nodeps','--nobuild',*common,*(['--without','clang_bolt'] if off else []),str(sp)],P,env)
   txt=run(tag+'-expanded',loader+[str(R/'usr/bin/rpmspec'),'-P',*common,*(['--define','_without_clang_bolt 1'] if off else []),str(sp)],P,env).decode()
   patchlines=re.findall(r'^Patch(\d+):\s*(.*)$',txt,re.M)
   assert [int(n) for n,_ in patchlines]==list(range(8)),(tag,patchlines)
   # Isolate metadata/path differences before comparing the expanded program.
   norm=re.sub(r'^VCS\s*:.*$', 'VCS: #IDENTITY',txt,flags=re.M)
   norm=norm.replace(str(src),'EXPORT_SOURCE').replace(str(P/side),'PARSE_TOPDIR')
   if side=='new':
    norm=''.join(line.replace(newpatch,oldpatch) if re.match(r'^Patch7\s*:',line) or line.strip()=='# '+newpatch else line for line in norm.splitlines(True))
   outputs[side]=norm
   results.append({'case':case,'side':side,'patches':patchlines,'nobuild_rc':0,'parse_rc':0})
  diff=''.join(difflib.unified_diff(outputs['old'].splitlines(True),outputs['new'].splitlines(True),fromfile='old-normalized',tofile='new-normalized'))
  (E/(label+'-'+case+'-expanded.diff')).write_text(diff)
  assert not diff,(label,case,'expanded program differs beyond Patch7 filename and approved metadata/path identity')
 (E/(label+'-five-parse-summary.json')).write_text(json.dumps({'PASS':True,'paired_cases':5,'parses':results,'normalization':'VCS metadata already checked by export gate; _sourcedir/_topdir execution paths; only Patch7 filename in expanded program'},indent=2)+'\n')
 print(label,'5 paired parses PASS',flush=True)

if __name__=='__main__':
 try:
  pa,pb=compare('PS3',X/'export-old',X/'export-PS3')
  parse_pair('PS3',X/'export-old',X/'export-PS3',pa,pb)
  for label,rev in [('PS2','d0b2e82aa90b11251a13b67d890642bf2fa6f66c'),('old-PS2','bde009d1197a09f7b7b76382a0166e03c841bdb9')]:
   out=X/('export90-'+label);assert not out.exists()
   run(label+'-export',['gbs','export','--commit',rev,'--outdir',str(out),'--outdir-directly',str(N)])
  pa,pb=compare('PS2',X/'export90-old-PS2',X/'export90-PS2')
  parse_pair('PS2',X/'export90-old-PS2',X/'export90-PS2',pa,pb)
  (E/'local-gates-PASS.json').write_text(json.dumps({'PASS':True,'time':now(),'export_pairs':2,'paired_parse_cases':10},indent=2)+'\n')
  print('90步骤1本地核对 已结束',now(),'status=PASS',flush=True)
 except Exception:
  print('90步骤1本地核对 已结束',now(),'status=STOP',flush=True)
  raise
