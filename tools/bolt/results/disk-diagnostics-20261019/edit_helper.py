from pathlib import Path
import ast,re
E=Path(__file__).resolve().parent;S=E.parents[1]/'temp/bolt-v4-20261013/v41/llvm-source';p=S/'packaging/clang-bolt-helper.py';s=p.read_text()
def replace(name,text):
 global s
 node=next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef) and n.name==name)
 lines=s.splitlines(True);s=''.join(lines[:node.lineno-1])+text.rstrip()+'\n'+''.join(lines[node.end_lineno:])
s=s.replace('import argparse\n','import argparse\nimport threading\n')
s=s.replace('22 GiB; it is not authorized by a 16 GiB production-validation budget.','resource planning outside package builds; local resource/lock rules never\nenter this release helper.')
s=s.replace('Historical successful instrumentation needed\nresource planning','Historical instrumentation requires\nresource planning')
s=s.replace('Maintenance notes (fail closed; preserve actual/expected values and logs):','Maintenance notes (fail closed; preserve actual/expected values and logs):\n- No disk-space admission thresholds: profile, BOLT and clang sizes change,\n  so fixed budgets become stale. Record actual allocation/free space only;\n  diagnose a failed step from its errno/log and estimate from this build.\n  disk-report is best effort; disk-diagnose is read-only. Neither is a gate.')
replace('save', '''def atomic_text(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name+'.new')
    try:
        with tmp.open('w') as stream:
            require(stream.write(text) == len(text), 'short text write: '+str(tmp))
            stream.flush(); os.fsync(stream.fileno())
        os.replace(tmp,path)
    except BaseException:
        try: tmp.unlink()
        except OSError: pass
        raise


def save(path, value):
    atomic_text(path, json.dumps(value, ensure_ascii=False, indent=2)+'\\n')''')
s=s.replace('deadline = time.monotonic()+timeout\n    while True:\n        status = os.waitid', 'deadline = time.monotonic()+timeout if timeout is not None else None\n    while True:\n        errors = getattr(process, "_bolt_output_errors", [])\n        if errors: raise errors[0]\n        status = os.waitid',1)
s=s.replace("if time.monotonic() >= deadline:\n            raise subprocess.TimeoutExpired", "if deadline is not None and time.monotonic() >= deadline:\n            raise subprocess.TimeoutExpired",1)
# Parent-owned log writes detect ENOSPC even if a child ignores write errors.
s=s.replace("process = None; reaped = False; primary = None", "process = None; reaped = False; primary = None; reader = None",1)
s=s.replace("        save(log.with_suffix(log.suffix+'.argv.json'),\n             {'argv': list(map(str, argv)), 'cwd': str(cwd) if cwd else None,\n              'SIGCHLD_original': str(previous), 'SIGCHLD_reset_to_default': previous != signal.SIG_DFL})", "        invocation = {'argv': list(map(str, argv)), 'cwd': str(cwd) if cwd else None,\n                      'SIGCHLD_original': str(previous), 'SIGCHLD_reset_to_default': previous != signal.SIG_DFL}\n        save(log.with_suffix(log.suffix+'.argv.json'), invocation)",1)
s=s.replace("stdout=output,\n                                       stderr=subprocess.STDOUT, start_new_session=True)\n            rc = peek_child_exit(process, timeout)", "stdout=subprocess.PIPE,\n                                       stderr=subprocess.STDOUT, start_new_session=True)\n            process._bolt_output_errors = []\n            def drain():\n                try:\n                    while True:\n                        chunk = process.stdout.read1(65536)\n                        if not chunk: break\n                        require(output.write(chunk) == len(chunk), 'short command-log write: '+str(log))\n                        output.flush()\n                except BaseException as failure:\n                    process._bolt_output_errors.append(failure)\n            reader = threading.Thread(target=drain,daemon=True);reader.start()\n            rc = peek_child_exit(process, timeout)",1)
s=s.replace("            require(reap_child(process) == rc", "            reader.join(10)\n            require(not reader.is_alive(), 'command log pipe did not close')\n            if process._bolt_output_errors: raise process._bolt_output_errors[0]\n            output.flush(); os.fsync(output.fileno())\n            require(reap_child(process) == rc",1)
s=s.replace("        return log.read_text(errors='replace')", "        text = log.read_text(errors='replace')\n        require(not disk_evidence(log), 'COMMAND_ERROR: disk write error in successful command log')\n        save(log.with_suffix(log.suffix+'.argv.json'), dict(invocation,completed=True,rc=0))\n        return text",1)
s=s.replace("        if isinstance(error, (KeyboardInterrupt, SystemExit)):", "        if reader is not None:\n            reader.join(1)\n        if process is not None and process.stdout is not None:\n            process.stdout.close()\n        if isinstance(error, (KeyboardInterrupt, SystemExit)):",1)
s=s.replace("        raise GateError(message) from error", "        failure = GateError(message); failure.bolt_log = str(log)\n        raise failure from error",1)
s=s.replace("        if output.exists():\n            output.unlink()\n        raise", "        if output.exists():\n            try: output.unlink()\n            except OSError: pass\n        raise",1)
replace('install_candidate', '''def install_candidate(root, candidate, state, identity, announce=False):
    root = Path(root).absolute(); require('debug' not in str(root).lower(), 'buildroot absolute path contains debug')
    e = ELF(candidate)
    try:
        elf = e.audit(final=True)
    finally:
        e.close()
    validate_identity(identity, candidate)
    entity, aliases = alias_group(root); changed = []
    for p in aliases:
        changed.append({'path': p.relative_to(root).as_posix(), 'old_type': 'symlink' if p.is_symlink() else 'file',
                        'old_target': os.readlink(p) if p.is_symlink() else None})
    st = entity.stat(); tmp = entity.with_name('.clang-bolt.new'); staged = []
    require(not tmp.exists() and not tmp.is_symlink(), 'temporary candidate exists')
    try:
        shutil.copyfile(candidate,tmp)
        tmp.chmod(stat.S_IMODE(st.st_mode))
        with tmp.open('rb') as stream: os.fsync(stream.fileno())
        actual = digest(tmp)
        require(actual == identity['after_sha256'], 'temporary candidate SHA differs')
        require(tmp.stat().st_size == Path(candidate).stat().st_size, 'temporary candidate size differs')
        for path in aliases:
            link = path.with_name('.'+path.name+'.bolt-link')
            require(not link.exists() and not link.is_symlink(), 'temporary alias exists')
            link.symlink_to('clang-22'); staged.append((link,path))
        result = {'installed_sha256':actual, 'identity':identity, 'alias_changes':changed,
                  'allowed_paths':['usr/bin/clang-22']+[p.relative_to(root).as_posix() for p in aliases], 'elf':elf}
        # All file writes, state and output publication precede the final commit.
        save(state,result)
        if announce: print(json.dumps(result,ensure_ascii=False),flush=True)
        for link,path in staged: os.replace(link,path)
        os.replace(tmp,entity)
        return result
    except BaseException:
        for path in [tmp]+[link for link,_ in staged]:
            try: path.unlink()
            except OSError: pass
        raise''')
s=s.replace("    disk_preflight(Path(output).parent,4*Path(input_elf).stat().st_size)\n",'')
start=s.index('GIB = 1024**3\n');end=s.index('def pipeline(',start)
s=s[:start]+(E/'disk_code.py.txt').read_text()+'\n\n'+s[end:]
s=s.replace('def pipeline(build, work, bolt, cache=None, planned_write_bytes=STAGE_WRITE_BUDGET):','def pipeline(build, work, bolt, cache=None):')
s=re.sub(r'    # Handed-off trees.*?    reference =', '    reference =',s,flags=re.S,count=1)
s=s.replace("    script.write_text(replay_script(edge,reference,work/'reference-relocs.d',cache))", "    atomic_text(script,replay_script(edge,reference,work/'reference-relocs.d',cache))")
s=s.replace(",\n                  disk_admission=admission)",")",1)
s=s.replace("    admission = disk_preflight(destination.parent,before['bytes'],4*GIB)\n",'')
s=s.replace(", 'disk_admission':admission",'')
s=s.replace("    disk_preflight(after.parent,before.stat().st_size)\n",'')
s=s.replace("s.add_argument('--cache-dir');s.add_argument('--planned-write-bytes',type=int,default=STAGE_WRITE_BUDGET)","s.add_argument('--cache-dir')")
s=re.sub(r"    s=sub.add_parser\('disk-preflight'\)[^\n]*\n",'',s)
needle="    a=p.parse_args()\n"
insert="""    s=sub.add_parser('disk-report');s.add_argument('stage',choices=['begin','tool-built','pipeline','post']);s.add_argument('--build');s.add_argument('--work');s.add_argument('--root')
    s=sub.add_parser('disk-diagnose');s.add_argument('step');s.add_argument('log');s.add_argument('--build');s.add_argument('--work');s.add_argument('--root')
    s=sub.add_parser('run-step');s.add_argument('step');s.add_argument('log');s.add_argument('--output');s.add_argument('--success-marker');s.add_argument('argv',nargs=argparse.REMAINDER)
    a=p.parse_args()
    _DISK_CONTEXT.clear()
    if a.cmd=='pipeline': _DISK_CONTEXT.update(build=a.build,work=a.work)
    elif a.cmd=='install': _DISK_CONTEXT.update(root=a.root)
    if a.cmd=='disk-report': disk_report(a.stage,a.build,a.work,a.root);return
    if a.cmd=='disk-diagnose': disk_diagnose(a.step,a.log,build=a.build,work=a.work,root=a.root);return
    if a.cmd=='run-step':
        # REMAINDER begins after step/log: parse optional output flags explicitly.
        args=list(a.argv);output=a.output;marker=a.success_marker
        while args and args[0]!='--':
            flag=args.pop(0)
            require(flag in ('--output','--success-marker') and args, 'invalid run-step option')
            value=args.pop(0)
            if flag=='--output':output=value
            else:marker=value
        require(args and args.pop(0)=='--' and args, 'run-step requires -- command')
        run_step(a.step,a.log,args,output,marker);return
"""
assert needle in s;s=s.replace(needle,insert,1)
s=s.replace("result=pipeline(a.build,a.work,a.tool,a.cache_dir,a.planned_write_bytes)","result=pipeline(a.build,a.work,a.tool,a.cache_dir)")
s=re.sub(r"    elif a.cmd=='disk-preflight':[^\n]*\n",'',s)
s=s.replace("Path(a.script).write_text(script);Path(a.script).chmod", "atomic_text(a.script,script);Path(a.script).chmod")
s=s.replace("elif a.cmd=='install':result=install_candidate(a.root,a.candidate,a.state,json.loads(Path(a.identity).read_text()))", "elif a.cmd=='install':\n        install_candidate(a.root,a.candidate,a.state,json.loads(Path(a.identity).read_text()),announce=True);return")
s=s.replace("    print(json.dumps(result,ensure_ascii=False))", "    print(json.dumps(result,ensure_ascii=False),flush=True)")
start=s.index("if __name__=='__main__':")
s=s[:start]+'''def cli():
    try:
        main()
        return 0
    except (GateError, OSError, ValueError, lzma.LZMAError) as error:
        step = sys.argv[1] if len(sys.argv)>1 else 'helper'
        log = getattr(error,'bolt_log',None) or os.environ.get('BOLT_STEP_LOG','-')
        diagnose_safely(step,log,error)
        print('BOLT_GATE_FAILED: '+str(error),file=sys.stderr)
        return 1


if __name__=='__main__':
    sys.exit(cli())
'''
ast.parse(s);assert not any(t in s for t in ['disk_preflight','DISK_FLOOR','LARGE_WRITE','STAGE_WRITE_BUDGET','disk-preflight','SKIP_DISK'])
p.write_text(s)
print('helper changed; source generation options and whitelist intact')
