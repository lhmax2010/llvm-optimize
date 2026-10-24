from pathlib import Path
import hashlib,json,subprocess,os,time,shutil

W=Path('/home/linhao/Toolchain/development/llvm-optimize')
E=Path(__file__).resolve().parent
D=W/'temp/perf-c-o2-os-20261025'
R=W/'temp/bolt-on-hybrid-20261024/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
RESOURCE=R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64/clang/22'
Z=Path('/home/linhao/Toolchain/libtool/codes/zlib')
def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
D.mkdir(exist_ok=True)
units=json.loads((W/'docs/53_hybrid_local_validation_evidence/tu-inputs.json').read_text())
groups={}
expected={'static':['06c940726269210ce3655e17366820a080bfe236a3adc24622958e6a6709e309','4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9'], 'hybrid':['d5090159915657b235b96f1202c058e1efd1647d6a2225ac8fdb2906aeaa501d','8b799f18e2bc37269385db125c881609e8457de1dd179f5d9d0ff9f557b58d16']}
for group,prefix in [('static','bolt-v4-20261022-cache-release/baseline-products'),('hybrid','bolt-on-hybrid-20261024/products')]:
    groups[group]={}
    for i,(role,name) in enumerate([('ordinary','ordinary-clang-22'),('candidate','clang.candidate')]):
        p=W/'temp'/prefix/'binaries'/name; h=sha(p);assert h==expected[group][i],(p,h)
        groups[group][role]=dict(path=str(p),sha256=h,bytes=p.stat().st_size)
save(E/'compiler-identities.json',groups)
loader=[str(R/'lib64/ld-linux-x86-64.so.2'),'--library-path',str(R/'lib64')+':'+str(R/'usr/lib64')]
precompiler=groups['static']['ordinary']['path']
targets=sorted(set(u['target'] for u in units));cases=[];sources=sorted(Z.glob('*.c'))+[Z/'contrib/minizip'/n for n in ['ioapi.c','mztools.c','unzip.c','zip.c','minizip.c']];assert len(sources)==20
sources_meta=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in sources]
save(E/'c-source-selection.json',dict(repository=str(Z),commit=subprocess.check_output(['git','-C',str(Z),'rev-parse','HEAD'],text=True).strip(),sources=sources_meta))
for target in targets:
    us=[u for u in units if u['target']==target]; seen=set();unique=[]
    for u in us:
        name=u['key'].split('/')[1].split('-',1)[1]
        if name not in seen:seen.add(name);unique.append(u)
    assert len(unique)==20
    sysroot=next(a.split('=',1)[1] for a in us[0]['provenance']['asset_preprocessing_argv'] if a.startswith('--sysroot='))
    assert Path(sysroot).is_dir()
    cpu_flags=[a for a in us[0]['original_argv'] if a.startswith('-m')];assert cpu_flags==[]
    for u in unique:
        assert sha(u['copy'])==u['sha256']
        for opt in ['-O2','-Os','-O3']:
            a=u['original_argv'][1:];a=['--no-default-config']+[opt if x in ['-O3','-O2','-Os'] else '--sysroot='+sysroot if x.startswith('--sysroot=') else '-resource-dir='+str(RESOURCE) if x.startswith('-resource-dir=') else x for x in a]
            a[a.index('-c')+1]=u['copy'];a[a.index('-o')+1]=str(D/'same.o')
            cases.append(dict(language='C++',option=opt,target=target,name=u['key'].split('/')[1],cohort=u['provenance']['cohort'],input=u['copy'],input_sha256=u['sha256'],argv=a,source_record=u))
    for opt in ['-O2','-Os']:
        for n,p in enumerate(sources):
            out=D/'inputs'/target/opt[1:]/(str(n).zfill(2)+'-'+p.stem+'.i');out.parent.mkdir(parents=True,exist_ok=True)
            common=['--no-default-config','--target='+target,'--sysroot='+sysroot,'-resource-dir='+str(RESOURCE),opt,'-g','-gdwarf-4','-fPIC','-fno-common','-fexceptions','-fasynchronous-unwind-tables','-frecord-gcc-switches','-D_GNU_SOURCE','-D_LARGEFILE64_SOURCE=1','-DHAVE_UNISTD_H','-I'+str(Z),'-I'+str(Z/'contrib/minizip')]
            argv=loader+[precompiler]+common+['-E',str(p),'-o',str(out)]
            t=time.time();r=subprocess.run(argv,capture_output=True,text=True);record=dict(argv=argv,rc=r.returncode,stdout=r.stdout,stderr=r.stderr,seconds=time.time()-t)
            save(E/('preprocess-'+target+'-'+opt[1:]+'-'+str(n)+'.json'),record)
            assert r.returncode==0,(p,r.stderr)
            cases.append(dict(language='C',option=opt,target=target,name=p.relative_to(Z).as_posix(),cohort='zlib/minizip',input=str(out),input_sha256=sha(out),source=str(p),source_sha256=sha(p),argv=common+['-x','cpp-output','-c',str(out),'-o',str(D/'same.o')]))
    print('PREPARED',target,flush=True)
assert len(cases)==300
save(E/'cases.json',cases)
save(E/'config.json',dict(work=str(D),root=str(R),resource=str(RESOURCE),loader=loader,groups=groups,cases=len(cases),source_modified=False,preprocessing='host execution with Tizen root runtime and per-target read-only Tizen sysroot; no chroot privilege available',cpu=2,parallel_compiles=1))
print('PREPARE_PASS',len(cases),flush=True)
