from pathlib import Path
import difflib,itertools,json,os,re,subprocess
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
B=W.with_name('llvm-optimize-bolt')
T=W/'temp/task133-d'; S=W/'temp/task131/pgo-dev'
E=B/'tools/bolt/results/task133-d'
M=B/'tools/bolt/results/fifth-review-20261111/rerun4/parse'
R=W/'temp/review-20261103/config-root/local/BUILD-ROOTS/scratch.x86_64.0'
L=[str(R/'usr/lib64/ld-linux-x86-64.so.2'),'--library-path',str(R/'usr/lib64')]
N=T/'parse'
N.mkdir(exist_ok=False)
old=N/'ps5.spec'
sha='7b05a13744d1cf81a5e9cff22a27eb037bf1b6a8'
old.write_bytes(subprocess.check_output(['/usr/bin/git','-C',str(S),'show',sha+':packaging/llvm.spec']))
new=S/'packaging/llvm.spec'
env={**os.environ,'RPM_CONFIGDIR':str(R/'usr/lib/rpm'),'LC_ALL':'C'}
show=subprocess.check_output(L+[str(R/'usr/bin/rpmspec'),'--showrc'],env=env,text=True)
base=next(l.split(': ',1)[1] for l in show.splitlines() if l.startswith('Macro path:'))
base=':'.join(x for x in base.split(':') if x.startswith(str(R)))
print(subprocess.check_output(L+[str(R/'usr/bin/rpmspec'),'--version'],env=env,text=True),flush=True)
def expand(spec,arch,opts=()):
    key='toolchain-'+('x86-debug' if arch=='x86_64' else arch)
    args=['--define','_topdir '+str(N/'rpm'),'--define','_builddir '+str(N/'rpm/BUILD'),
          '--macros',base+':'+str(M/(key+'.macros')),'--target',arch+'-tizen-linux',
          '--define','_sourcedir '+str(S/'packaging'),'--define','_toolchain clang']
    return subprocess.run(L+[str(R/'usr/bin/rpmspec'),'-P',*args,*opts,str(spec)],capture_output=True,text=True,env=env)
parsed=[]
defaults={}
for arch in ('x86_64','aarch64','armv7l'):
    a=expand(old,arch);b=expand(new,arch)
    delta=''.join(difflib.unified_diff(a.stdout.splitlines(True),b.stdout.splitlines(True),'PS5','pgo-dev'))
    (E/('default-'+arch+'.diff')).write_text(delta)
    no_blank=lambda x:''.join(l for l in x.splitlines(keepends=True) if l.rstrip('\r\n'))
    defaults[arch]={'ps5_rc':a.returncode,'pgo_dev_rc':b.returncode,'byte_identical':a.stdout==b.stdout,
                    'nonblank_equal':no_blank(a.stdout)==no_blank(b.stdout),
                    'raw_delta':delta[:5000],'stderr':a.stderr+b.stderr}
    for values in itertools.product((0,1),repeat=4):
        opts=[]
        for macro,v in zip(('llvm_speedup','hybrid_link','clang_bolt','clang_pgo'),values):
            opts+=['--define',f'_{("with" if v else "without")}_{macro} 1']
        r=expand(new,arch,opts)
        code=''.join(map(str,values))
        (N/f'{arch}-{code}.stdout').write_text(r.stdout)
        (N/f'{arch}-{code}.stderr').write_text(r.stderr)
        should=bool(arch=='x86_64' and values[0] and values[3])
        seen=bool(re.search(r'(?m)^Source1202:',r.stdout) and '-DLLVM_PROFDATA_FILE=' in r.stdout and ' pgo-check-ninja ' in r.stdout)
        pgo_parts=[k for k in ('Source1202:', 'Source1203:', 'Source1204:', ' pgo-prepare ', '-DLLVM_PROFDATA_FILE=', ' pgo-check-ninja ') if k in r.stdout]
        good=r.returncode==0 and len(pgo_parts)==(6 if should else 0)
        # All four toggles checked, including master gate and the ARM restriction.
        hybrid='-DTIZEN_HYBRID_LINK=ON' in r.stdout
        bolt='BOLT_PROFILE_SOURCE=' in r.stdout
        good=good and hybrid==bool(arch=='x86_64' and values[0] and values[1]) and bolt==bool(arch=='x86_64' and values[0] and values[2])
        row={'arch':arch,'switches':code,'expected_pgo':should,'seen_pgo':seen,'pgo_parts':pgo_parts,'hybrid':hybrid,
             'bolt':bolt,'rc':r.returncode,'pass':good,'stderr':r.stderr}
        parsed.append(row)
        print(arch,code,'PASS' if good else 'FAIL',r.stderr[:300],flush=True)
(E/'spec-matrix.json').write_text(json.dumps({'matrix':parsed,'defaults':defaults},indent=2)+'\n')
print('matrix',sum(x['pass'] for x in parsed),len(parsed))
for k,v in defaults.items(): print('default',k,v)
