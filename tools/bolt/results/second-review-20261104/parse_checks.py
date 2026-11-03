from pathlib import Path
import subprocess,json,os,hashlib,difflib,re,time
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';E=Path(__file__).parent;P=E/'parse-ruling';P.mkdir(exist_ok=True)
S=W/'temp/review-20261102/source';R=W/'temp/review-20261103/config-root/local/BUILD-ROOTS/scratch.x86_64.0'
conf={'toolchain':W/'temp/bolt-v4-20261021-disk-footprint/build.conf','basedev':B/'tools/bolt/results/qb-20261102/configs/base-dev-build.conf'}
expected={'toolchain':'e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945','basedev':'8ace286a5f98f2e02a79be275a64c22a86ea2b0034174c1e293381e181ce3f6a'}
env=dict(os.environ,RPM_CONFIGDIR=str(R/'usr/lib/rpm'),LC_ALL='C',HOME=str(P))
loader=[str(R/'usr/lib64/ld-linux-x86-64.so.2'),'--library-path',str(R/'usr/lib64')]
def run(name,args):
 p=subprocess.run(args,env=env,cwd=P,capture_output=True,text=True)
 (P/(name+'.stdout')).write_text(p.stdout);(P/(name+'.stderr')).write_text(p.stderr);(P/(name+'.json')).write_text(json.dumps({'argv':args,'rc':p.returncode,'RPM_CONFIGDIR':env['RPM_CONFIGDIR']},indent=2)+'\n')
 assert p.returncode==0,(name,p.stderr);return p.stdout
show=run('rpm-showrc',loader+[str(R/'usr/bin/rpmspec'),'--showrc'])
macrobase=next(x.split(': ',1)[1] for x in show.splitlines() if x.startswith('Macro path:'))
# Exclude host/user macro overrides. Preserve the Tizen runtime's complete configured macro list.
macrobase=':'.join(x for x in macrobase.split(':') if x.startswith(str(R)))
run('rpm-version',loader+[str(R/'usr/bin/rpm'),'--dbpath',str(R/'var/lib/rpm'),'-q','--qf','%{NAME} %{VERSION}-%{RELEASE}\n','rpm','rpm-build'])
for label,rev in [('new','HEAD'),('parent','5aff6c0c'),('previous','3ee2d847')]:
 (P/(label+'.spec')).write_bytes(subprocess.check_output(['git','show',rev+':packaging/llvm.spec'],cwd=S))
old=(P/'parent.spec').read_text();new=(P/'new.spec').read_text()
# Bound only the x86 flag-normalization block, with byte-identical surrounding text.
start=old.index('%ifarch x86_64\n',old.index('%build'))+len('%ifarch x86_64\n')
end=old.index('%endif',start)
oldblock=old[start:end]
newstart=new.index('TIZEN_LLVM_RELEASE=',new.index('%ifarch x86_64',new.index('%build')))
newend=new.index('%endif',newstart)
newblock=new[newstart:newend]
# Changes are independently bounded below in each expanded spec.
rows=[]
for name,c in conf.items():
 assert hashlib.sha256(c.read_bytes()).hexdigest()==expected[name]
 for case,arch,mode in [('x86-debug','x86_64','debug'),('x86-release','x86_64','release'),('armv7l','armv7l',None),('aarch64','aarch64',None)]:
  key=name+'-'+case
  raw=run(key+'-rawmacros',['/usr/lib/build/queryconfig','--dist',str(c),'--archpath',arch,'rawmacros'])
  (P/(key+'.macros')).write_text(raw)
  opt=run(key+'-optflags',['/usr/lib/build/queryconfig','--dist',str(c),'--archpath',arch,'optflags','debug'])
  # Use rpmrc for architecture-specific optflags, just as /usr/lib/build does.
  (P/(key+'.rpmrc')).write_text(opt)
  common=['--rcfile',str(R/'usr/lib/rpm/rpmrc')+':'+str(P/(key+'.rpmrc')),'--macros',macrobase+':'+str(P/(key+'.macros')),'--target',arch+'-tizen-linux']
  if mode=='debug':common+=['--define','_toolchain clang']
  if mode=='release':common+=['--undefine','_toolchain']
  for off in ([False,True] if arch=='x86_64' else [False]):
   suffix='-off' if off else '-on'; outputs={}
   for label in ('new','parent'):
    args=loader+[str(R/'usr/bin/rpmspec'),'-P',*common,*(['--define','_without_clang_bolt 1'] if off else []),str(P/(label+'.spec'))]
    outputs[label]=run(key+suffix+'-'+label,args)
   diff=''.join(difflib.unified_diff(outputs['parent'].splitlines(True),outputs['new'].splitlines(True),fromfile='5aff6c0c',tofile='second-review'))
   (P/(key+suffix+'.diff')).write_text(diff)
   if arch!='x86_64':assert outputs['new']==outputs['parent'],key
   else:
    def canonical(text, fresh):
     a=text.index('for hybrid_tool in ');b=text.index('echo TIZEN_HYBRID_LINK_OK',a)
     text=text[:a]+'HYBRID_GATE\n'+text[b:]
     if fresh:
      a=text.index('TIZEN_LLVM_RELEASE=');b=text.index('# END TIZEN_LLVM_FIXED_FLAGS',a)+len('# END TIZEN_LLVM_FIXED_FLAGS\n')
      text=text[:a]+'FLAGS\n'+text[b:]
      text=text.replace('# readelf from binutils-devel also checks the hybrid linkage contract.\n','')
      text=text.replace('# LC_ALL=C applies only to this ninja invocation.\n','')
      text=re.sub(r'^    --debug-info (yes|no) \\\n','',text,flags=re.M)
     else:
      assert oldblock in text
      text=text.replace(oldblock,'FLAGS\n',1)
     return text
    aa=canonical(outputs['parent'],False);bb=canonical(outputs['new'],True)
    (P/(key+suffix+'-unexpected.diff')).write_text(''.join(difflib.unified_diff(aa.splitlines(True),bb.splitlines(True))))
    assert aa==bb,key+suffix+' unexpected expansion delta'
   rows.append({'config':name,'case':case,'bolt':'off' if off else 'on','PASS':True,'byte_identical':not diff,'difference':'flags, hybrid gate, ninja-only comments, explicit debug-info' if diff else 'none'})
(P/'expansion-summary.json').write_text(json.dumps(rows,indent=2)+'\n')
# Exported spec: real GBS Patch declarations and five target parses.
x=E/'export-ruling';(P/'rollback.spec').write_text((x/'llvm.spec').read_text().replace('%bcond_without clang_bolt','%bcond_with clang_bolt',1))
five=[]
for name,arch,off,rollback in [('x86-on','x86_64',False,False),('x86-off','x86_64',True,False),('x86-rollback','x86_64',False,True),('armv7l','armv7l',False,False),('aarch64','aarch64',False,False)]:
 common=['--macros',macrobase+':'+str(P/('toolchain-'+('x86-debug' if arch=='x86_64' else arch)+'.macros')),'--target',arch+'-tizen-linux','--define','_sourcedir '+str(x),'--define','_toolchain clang']
 specpath=P/'rollback.spec' if rollback else x/'llvm.spec'
 run('five-'+name,loader+[str(R/'usr/bin/rpmbuild'),'-bp','--nodeps','--nobuild',*common,*(['--without','clang_bolt'] if off else []),str(specpath)])
 text=run('five-'+name+'-expanded',loader+[str(R/'usr/bin/rpmspec'),'-P',*common,*(['--define','_without_clang_bolt 1'] if off else []),str(specpath)])
 patches=re.findall(r'^Patch\d+:.*$',text,re.M);assert len(patches)==8,(name,patches)
 five.append({'case':name,'PASS':True,'patches':patches})
(P/'five-summary.json').write_text(json.dumps(five,indent=2)+'\n')
print('EXPANSIONS_PASS',len(rows),'FIVE_PARSE_PASS',len(five))
