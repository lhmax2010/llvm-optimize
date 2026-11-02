from pathlib import Path, PurePosixPath
import subprocess, json, re, os, shlex, stat, hashlib, posixpath
D=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-20261028/full-20261030')
C=D/'install-test-root'; E=D/'evidence/install-test-20261102-resume'
raw=E/'elf-readelf-final';raw.mkdir(exist_ok=True)
def resolve(rel):
    queue=list(PurePosixPath(rel).parts);parts=[];hops=0
    while queue:
        x=queue.pop(0)
        if x in ('/','','.'):continue
        if x=='..':
            if parts:parts.pop()
            continue
        p=C.joinpath(*parts,x)
        if p.is_symlink():
            hops+=1;assert hops<50
            target=os.readlink(p)
            if target.startswith('/'):parts=[]
            queue=list(PurePosixPath(target).parts)+queue
        else:parts.append(x)
    return C.joinpath(*parts)
cache={}
def elf(rel,physical=None):
    key=(rel,str(physical))
    if key in cache:return cache[key]
    p=physical or resolve(rel)
    r={'path':rel,'physical':str(p),'exists':p.is_file()}
    if not p.is_file():r['PASS']=False;r['error']='missing executable';return r
    r['mode']=oct(p.stat().st_mode&0o777);r['executable']=bool(p.stat().st_mode&0o111)
    if physical is not None:
        r['mode']=json.loads((E/'rpm-clang-metadata.json').read_text())['mode'];r['executable']=bool(int(r['mode'],8)&0o111);r['provenance']='RPM payload; not installed yet'
    q=subprocess.run(['readelf','-W','-l','-d',str(p)],capture_output=True,text=True)
    name=rel.strip('/').replace('/','__')
    (raw/(name+'.stdout')).write_text(q.stdout);(raw/(name+'.stderr')).write_text(q.stderr)
    r['readelf_rc']=q.returncode
    if q.returncode!=0:r['PASS']=False;r['error']='ELF inspection failed';return r
    m=re.search(r'Requesting program interpreter: (.*?)\]',q.stdout)
    r['interpreter']=m[1] if m else None
    r['needed']=re.findall(r'\(NEEDED\).*?\[(.*?)\]',q.stdout)
    r['runpath']=re.findall(r'\(RUNPATH\).*?\[(.*?)\]',q.stdout)
    r['rpath']=re.findall(r'\(RPATH\).*?\[(.*?)\]',q.stdout)
    r['PASS']=os.access(p,os.R_OK);cache[key]=r;return r

def closure(rel,physical=None):
    found={};errors=[];entry=posixpath.normpath(rel)
    def visit(rel,physical=None,inherited=()):
        rel=posixpath.normpath(rel)
        if rel in found:return
        info=dict(elf(rel,physical));found[rel]=info
        if not info.get('PASS'):errors.append({'requester':rel,'error':info.get('error','not executable')});return
        if rel==entry and not info['executable']:errors.append({'requester':rel,'error':'entry program is not executable'})
        interp=info.get('interpreter')
        if interp:
            p=resolve(interp);ok=p.is_file() and bool(p.stat().st_mode&0o111)
            info['interpreter_resolved']={'path':str(p),'PASS':ok}
            if not ok:errors.append({'requester':rel,'interpreter':interp,'error':'missing interpreter'})
            else:visit(interp)
        origin=str(PurePosixPath(rel).parent)
        def expand(items):
            return [x.replace('${ORIGIN}',origin).replace('$ORIGIN',origin) for s in items for x in s.split(':') if x]
        rpaths=expand(info['rpath']) if not info['runpath'] else []
        dirs=rpaths+list(inherited)+expand(info['runpath'])+['/lib64','/usr/lib64','/lib','/usr/lib']
        # The pristine test root has no ld.so.cache and no LD_LIBRARY_PATH is set.
        info['dependency_search_dirs']=dirs;info['resolved_needed']=[]
        for name in info['needed']:
            choices=[name] if '/' in name else [str(PurePosixPath(d)/name) for d in dirs]
            match=next((p for p in choices if resolve(p).is_file()),None)
            info['resolved_needed'].append({'name':name,'path':match,'physical':str(resolve(match)) if match else None})
            if match is None:errors.append({'requester':rel,'needed':name,'error':'missing library'})
            else:visit(match,inherited=tuple(rpaths)+inherited)
    visit(rel,physical)
    return {'program':rel,'PASS':not errors,'errors':errors,'closure':list(found.values())}
programs=['/usr/bin/rpm','/usr/bin/rpmdb','/sbin/ldconfig','/bin/mknod','/bin/mount','/bin/umount','/bin/sh','/usr/bin/env','/usr/bin/lldb','/usr/bin/lldb-server','/opt/symbolizer/llvm-symbolizer','/usr/bin/clang-22']
checks=[closure(p,E/'rpm-clang-22' if p=='/usr/bin/clang-22' else None) for p in programs]
(E/'program-preflight-final.json').write_text(json.dumps(checks,indent=2)+'\n')
configs=sorted(C.rglob('rpmpopt*'));execs=[];targets={}
for config in configs:
    if not config.is_file():continue
    for line_no,line in enumerate(config.read_text().splitlines(),1):
        if not re.match(r'^\s*\S+\s+exec\s+',line):continue
        tokens=shlex.split(line,comments=True)
        if len(tokens)>=4 and tokens[1]=='exec':
            target=tokens[3];choices=[target] if target.startswith('/') else [d+'/'+target for d in ['/usr/sbin','/usr/bin','/sbin','/bin']]
            targetpath=next((p for p in choices if resolve(p).is_file()),None)
            if target not in targets:targets[target]=closure(targetpath) if targetpath else {'program':target,'PASS':False,'errors':[{'error':'missing exec target','searched':choices}]}
            execs.append({'config':str(config.relative_to(C)),'line':line_no,'original':line,'option':tokens[2],'target':target,'arguments':tokens[4:],'resolved':targetpath,'PASS':targets[target]['PASS']})
(E/'rpmpopt-preflight.json').write_text(json.dumps({'configs':[str(p.relative_to(C)) for p in configs],'exec_entries':execs,'targets':targets},indent=2)+'\n')
p=C/'dev/null';s=p.lstat();dev={'path':str(p),'type':'character' if stat.S_ISCHR(s.st_mode) else 'other','major':os.major(s.st_rdev),'minor':os.minor(s.st_rdev),'mode':oct(stat.S_IMODE(s.st_mode))};dev['PASS']=stat.S_ISCHR(s.st_mode) and (os.major(s.st_rdev),os.minor(s.st_rdev))==(1,3) and stat.S_IMODE(s.st_mode)==0o666
rpmdir=C/'var/lib/rpm';inventory=[]
for p in sorted(rpmdir.rglob('*')):
    s=p.lstat();inventory.append({'path':str(p.relative_to(rpmdir)),'bytes':s.st_size,'mode':oct(stat.S_IMODE(s.st_mode)),'uid':s.st_uid,'gid':s.st_gid})
residual={'dev_null':dev,'rpm_directory_exists':rpmdir.exists(),'rpm_directory_inventory':inventory,'database_for_this_attempt':'/var/lib/rpm-20261102' if inventory else '/var/lib/rpm','mountinfo_matches':[x for x in Path('/proc/self/mountinfo').read_text().splitlines() if str(C) in x]}
(E/'residual-preflight.json').write_text(json.dumps(residual,indent=2)+'\n')
summary={'programs_passed':sum(x['PASS'] for x in checks),'programs_total':len(checks),'exec_entries_passed':sum(x['PASS'] for x in execs),'exec_entries_total':len(execs),'missing_exec_targets':[k for k,v in targets.items() if not v['PASS']],'dev_null_pass':dev['PASS'],'database':residual['database_for_this_attempt'],'ld_so_cache_exists':(C/'etc/ld.so.cache').exists(),'PASS':all(x['PASS'] for x in checks) and all(x['PASS'] for x in execs) and dev['PASS'] and not residual['mountinfo_matches']}
(E/'preflight-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
for x in checks:print(x['program'],x['PASS'],x['errors'])
for x in execs:print(x['line'],x['original'],x['PASS'])
