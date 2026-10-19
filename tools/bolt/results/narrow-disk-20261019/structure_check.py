from pathlib import Path
import subprocess,json,re,hashlib,os
E=Path(__file__).resolve().parent;W=E.parents[1];S=W/'temp/bolt-v4-20261013/v41/llvm-source';a=(E/'base-llvm.spec').read_text();b=(S/'packaging/llvm.spec').read_text()
def build(s):return s.split('\n%build\n',1)[1].split('\n%install\n',1)[0]
def install(s):return s.split('\n%install\n',1)[1].split('\n%post -n clang',1)[0]
def baseline(s):
 lines=s.splitlines(True);out=[];i=0
 while i<len(lines):
  if lines[i].strip()=='%ifarch x86_64' and i+1<len(lines) and lines[i+1].strip()=='%if %{with clang_bolt}':
   depth=2;i+=2
   while depth:
    line=lines[i].strip()
    if line.startswith('%if'):depth+=1
    elif line.startswith('%endif'):depth-=1
    i+=1
  else:out.append(lines[i]);i+=1
 return ''.join(out)
checks={}
def compare(name,x,y):
 (E/('base-'+name+'.txt')).write_text(x);(E/('new-'+name+'.txt')).write_text(y)
 argv=['cmp','--',str(E/('base-'+name+'.txt')),str(E/('new-'+name+'.txt'))];r=subprocess.run(argv,capture_output=True,text=True)
 checks[name]={'argv':argv,'rc':r.returncode,'bytes':len(x.encode()),'sha256':hashlib.sha256(x.encode()).hexdigest(),'stdout':r.stdout,'stderr':r.stderr};assert r.returncode==0,name
compare('build',build(a),build(b));compare('install-baseline',baseline(install(a)),baseline(install(b)))
old_tail=a[a.index('%global __bolt_original_spec_install_post'):]
new_tail=b[b.index('%global __bolt_original_spec_install_post'):]
normalized=new_tail.replace('python3 -B %{SOURCE1201} post','python3 %{SOURCE1201} post').replace('    echo BOLT_POST_GATE_PASS \\\n    python3 -B %{SOURCE1201} disk-report post\n','    echo BOLT_POST_GATE_PASS\n')
compare('post-tail-allowed-edits-only',old_tail,normalized)
# Actual host-generated scripts, with shared macro paths; wrapper copies, never runs product commands.
C=E/'capture';C.mkdir(exist_ok=True)
for n in ['BUILD','BUILDROOT','tmp']:(C/n).mkdir(exist_ok=True)
wrapper=C/'copy-shell.sh';wrapper.write_text('#!/bin/sh\nset -eu\nfor script do :; done\ncp "$script" "$BOLT_CAPTURE"\n');wrapper.chmod(0o755)
for label,spec in [('base',E/'base-llvm.spec'),('new',S/'packaging/llvm.spec')]:
 env=os.environ.copy();env['BOLT_CAPTURE']=str(E/(label+'-install.sh'))
 argv=['rpmbuild','-bi','--short-circuit','--nodeps','--define','_toolchain clang','--define','_topdir '+str(C),'--define','_builddir '+str(C/'BUILD'),'--define','_buildrootdir '+str(C/'BUILDROOT'),'--define','_tmppath '+str(C/'tmp'),'--define','_sourcedir '+str(S/'packaging'),'--define','__spec_install_cmd '+str(wrapper)+' %{___build_args}',str(spec)]
 r=subprocess.run(argv,env=env,capture_output=True,text=True);(E/(label+'-capture.stdout')).write_text(r.stdout);(E/(label+'-capture.stderr')).write_text(r.stderr)
 script=(E/(label+'-install.sh')).read_text();syntax=subprocess.run(['/bin/sh','-n',str(E/(label+'-install.sh'))],capture_output=True,text=True);assert syntax.returncode==0
 checks[label+'-capture']={'argv':argv,'rc':r.returncode,'syntax_rc':syntax.returncode,'product_script_executed':False,'expected_filelist_failure':True}
 anchor='  "$BOLT_WORK/install-state.json" "$BOLT_WORK/identity.json" || exit 1\n'
 tail=script.split(anchor,1)[1]
 stop=re.search(r'    python3(?: -B)? [^\n]+ post ',tail);assert stop
 (E/(label+'-platform-post.txt')).write_text(tail[:stop.start()])
compare('platform-post',(E/'base-platform-post.txt').read_text(),(E/'new-platform-post.txt').read_text())
# Only these shell actions are wrapped; helper calls stay direct (only -B differs).
wrappers=[{'line':i,'text':line} for i,line in enumerate(b.splitlines(),1) if re.match(r'^(?:LC_ALL=C .* )?bolt_(?:step|checked) ',line)]
assert len(wrappers)==8,wrappers
for name in ['preflight','certified','snapshot','unpack','tool-plan','tool-prepare','tool-verify','pipeline','compare-root','install','post']:
 pattern=r'python3 %\{SOURCE1201\} '+name+r'(?: [^\n]*)?(?:\\\n[^\n]*)*'
 old=re.findall(pattern,a);new=re.findall(pattern,b.replace('python3 -B %{SOURCE1201}','python3 %{SOURCE1201}'))
 assert old==new,(name,old,new)
(E/'structure-result.json').write_text(json.dumps({'PASS':True,'checks':checks,'wrapped_BOLT_actions':wrappers,'no_ordinary_wrappers':True},indent=2)+'\n')
# sh -e sees diagnostic and exits 1 for the BOLT-only failing command.
functions=b[b.index('bolt_fail() {'):b.index('python3 -B %{SOURCE1201} disk-report begin')].replace('%{SOURCE1201}',str(S/'packaging/clang-bolt-helper.py')).replace('%%','%')
script=E/'shell-failure.sh';script.write_text('#!/bin/sh\n'+functions+"bolt_step fixture-step /bin/sh -c 'echo fixture failure >&2; exit 7'\necho SHOULD_NOT_RUN\n")
env=os.environ.copy();env.update(BOLT_BUILD=str(E/'shell-build'),BOLT_WORK=str(E/'shell-build/clang-bolt'));r=subprocess.run(['/bin/sh','-e',str(script)],env=env,capture_output=True,text=True)
(E/'shell-failure.stdout').write_text(r.stdout);(E/'shell-failure.stderr').write_text(r.stderr);(E/'shell-failure.json').write_text(json.dumps({'argv':['/bin/sh','-e',str(script)],'rc':r.returncode,'PASS':r.returncode==1 and 'BOLT_DISK_DIAGNOSIS ' in r.stdout and 'SHOULD_NOT_RUN' not in r.stdout},indent=2)+'\n')
assert r.returncode==1 and 'BOLT_DISK_DIAGNOSIS ' in r.stdout and 'SHOULD_NOT_RUN' not in r.stdout
print(json.dumps({'structure':'PASS','checks':{k:v['rc'] for k,v in checks.items()},'wrapped_actions':len(wrappers),'sh_e_failure':'PASS rc1'},indent=2))
