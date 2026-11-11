from pathlib import Path
import subprocess,json,os,hashlib,difflib,re,time
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';E=Path(__file__).parent;P=E/'parse';P.mkdir(exist_ok=True)
S=W/'temp/rebase-359934-20261106/source';R=W/'temp/review-20261103/config-root/local/BUILD-ROOTS/scratch.x86_64.0'
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
for label,rev in [('new','HEAD'),('parent','60fabc723f30c5cc04146a9dd83487ebed63f259')]:
 (P/(label+'.spec')).write_bytes(subprocess.check_output(['git','show',rev+':packaging/llvm.spec'],cwd=S))
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
   diff=''.join(difflib.unified_diff(outputs['parent'].splitlines(True),outputs['new'].splitlines(True),fromfile='60fabc72',tofile='fifth-review-fixed'))
   (P/(key+suffix+'.diff')).write_text(diff)
   if arch!='x86_64' or off:
    assert outputs['new']==outputs['parent'],key+suffix+' spec expansion changed'
   else:
    restored=outputs['new']
    lines=restored.splitlines(True)
    count=0
    for i,line in enumerate(lines):
     if 'disk-diagnose' in line and '|| bolt_status_exit $?' in line:
      lines[i]=line.replace('|| bolt_status_exit $?','|| true');count+=1
    assert count==2,(key,count)
    restored=''.join(lines)
    assert restored==outputs['parent'],key+suffix+' unexpected spec expansion changed'
   if name=='toolchain' and case=='x86-debug' and not off:
    post_spec=E/'post-expanded.spec'
    post_spec.write_text((P/'new.spec').read_text()+'\n%check\n%{__spec_install_post}\n')
    post=run('post-expanded',loader+[str(R/'usr/bin/rpmspec'),'-P',*common,str(post_spec)])
    (E/'post-expanded.stdout').write_text(post)
    optional=[{'line':i,'text':line} for i,line in enumerate(post.splitlines(),1) if line.strip().startswith('bolt_optional python3 -B ')]
    (E/'optional-calls.json').write_text(json.dumps(optional,indent=2)+'\n')
    assert len(optional)==5,optional
    for row in optional:print(str(row['line'])+': '+row['text'])
    if os.environ.get('PREPARE_ONLY')=='1':raise SystemExit(0)
   rows.append({'config':name,'case':case,'bolt':'off' if off else 'on','PASS':True,'byte_identical':not diff,'difference':'two diagnostic calls propagate cancellation status' if diff else 'none'})
(P/'expansion-summary.json').write_text(json.dumps(rows,indent=2)+'\n')
print('EXPANSIONS_PASS',len(rows),'ALL_BYTE_IDENTICAL',all(r['byte_identical'] for r in rows))

# Five parse checks use the current spec, with unchanged sources from the preserved GBS export.

x=W/'temp/rebase-359934-20261106-r2/export';(P/'rollback.spec').write_text((P/'new.spec').read_text().replace('%bcond_without clang_bolt','%bcond_with clang_bolt',1))
expected_patch_count=len(re.findall(r'^Patch\d+:.*$',(P/'new.spec').read_text(),re.M))
# This worktree exports a native source tarball (GBS log), not an 8-patch series.
five=[]
for name,arch,off,rollback in [('x86-on','x86_64',False,False),('x86-off','x86_64',True,False),('x86-rollback','x86_64',False,True),('armv7l','armv7l',False,False),('aarch64','aarch64',False,False)]:
 common=['--define','_topdir '+str(P/'rpmbuild'),'--macros',macrobase+':'+str(P/('toolchain-'+('x86-debug' if arch=='x86_64' else arch)+'.macros')),'--target',arch+'-tizen-linux','--define','_sourcedir '+str(x),'--define','_toolchain clang']
 specpath=P/'rollback.spec' if rollback else P/'new.spec'
 run('five-'+name,loader+[str(R/'usr/bin/rpmbuild'),'-bp','--nodeps','--nobuild',*common,*(['--without','clang_bolt'] if off else []),str(specpath)])
 text=run('five-'+name+'-expanded',loader+[str(R/'usr/bin/rpmspec'),'-P',*common,*(['--define','_without_clang_bolt 1'] if off else []),str(specpath)])
 patches=re.findall(r'^Patch\d+:.*$',text,re.M);assert len(patches)==expected_patch_count,(name,patches)
 five.append({'case':name,'PASS':True,'patches':patches})
(P/'five-summary.json').write_text(json.dumps(five,indent=2)+'\n')
print('EXPANSIONS_PASS',len(rows),'FIVE_PARSE_PASS',len(five))
