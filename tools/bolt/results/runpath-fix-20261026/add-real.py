from pathlib import Path
p=Path(__file__).resolve().parent/'source/packaging/clang-bolt-helper.py';s=p.read_text()
new='''# Real implementation files, not synthetic tiny probes. C uses compiler resource
# headers only; freestanding + nostdinc prevents accidental cross-target sysroots.
REAL_C_SOURCES = ('compiler-rt/lib/builtins/bswapsi2.c', 'compiler-rt/lib/builtins/bswapdi2.c')
REAL_CXX_SOURCES = ('llvm/lib/Support/SmallVector.cpp', 'llvm/lib/Support/StringRef.cpp')


def real_commands(build, resource_dir):
    build = Path(build).absolute(); source = build.parent
    cases = []
    for relative in REAL_C_SOURCES:
        for target in TRIPLES:
            cases.append((relative, target, ['--no-default-config', '--target='+target,
                          '-resource-dir='+str(resource_dir), '-ffreestanding', '-nostdinc',
                          '-isystem', str(Path(resource_dir)/'include'), '-O2', '-g', '-c',
                          str(source/relative)]))
    for relative in REAL_CXX_SOURCES:
        cases.append((relative, 'x86_64-tizen-linux-gnu', ['--no-default-config',
                      '--target=x86_64-tizen-linux-gnu', '-resource-dir='+str(resource_dir),
                      '-O2', '-g', '-std=c++17', '-I'+str(source/'llvm/include'),
                      '-I'+str(build/'include'), '-c', str(source/relative)]))
    return cases


def real_gate(ordinary, candidate, build, work, resource_dir):
    started = time.monotonic(); work = Path(work); work.mkdir(parents=True, exist_ok=True)
    # Both roles use the same physical compiler/output paths, including strings
    # emitted into .GCC.command.line. No stripping or object normalization.
    compiler = work/'same-clang'; output = work/'same.o'; rows = []
    cases = real_commands(build, resource_dir)
    for role, executable in (('ordinary', ordinary), ('candidate', candidate)):
        shutil.copyfile(executable, compiler); compiler.chmod(0o755)
        for index, (relative, target, args) in enumerate(cases):
            output.unlink(missing_ok=True)
            start = time.monotonic()
            call([str(compiler), *args, '-o', str(output)], work/('%s-%02d.log' % (role,index)), timeout=120)
            require(output.is_file() and not output.is_symlink() and output.stat().st_size > 0,
                    'real compile did not produce a nonempty regular object: '+relative)
            sha = digest(output)
            if role == 'ordinary':
                rows.append({'source': relative, 'target': target, 'ordinary_sha256': sha,
                             'ordinary_seconds': time.monotonic()-start})
            else:
                rows[index].update(candidate_sha256=sha, candidate_seconds=time.monotonic()-start)
                require(sha == rows[index]['ordinary_sha256'], 'real object bytes differ: '+relative+' '+target)
                rows[index]['byte_equal'] = True
    result = {'real_pass': True, 'seconds': time.monotonic()-started, 'cases': rows}
    save(work/'real-result.json', result)
    print('BOLT_REAL_GATE_PASS '+json.dumps({'work': str(work), 'cases': len(rows), 'seconds': result['seconds']}), flush=True)
    return result


'''
s=s.replace('def tiny_gate(',new+'def tiny_gate(',1)
s=s.replace("rows = tiny_gate(ordinary, str(entity), candidate_work, resource_dir)","rows = tiny_gate(ordinary, str(entity), candidate_work, resource_dir)\n    real = real_gate(ordinary, str(entity), Path(ordinary).parent.parent,\n                     Path(candidate_work)/'real', resource_dir)")
s=s.replace("'strip_identity_pass': True, 'security': security, 'installed_security': installed}","'strip_identity_pass': True, 'security': security, 'installed_security': installed, 'real': real}")
s=s.replace("identity = strip_all(str(build/'bin/llvm-strip')", "real_prestrip = real_gate(work/'ordinary-clang-22',work/'clang.bolt',build,work/'prestrip-real',build/'lib64/clang/22')\n    identity = strip_all(str(build/'bin/llvm-strip')",1)
s=s.replace("result.update(identity=identity, security=security, input_policy", "real_final = real_gate(work/'ordinary-clang-22',work/'clang.candidate',build,work/'preinstall-real',build/'lib64/clang/22')\n    result.update(real_prestrip=real_prestrip, real_final=real_final, identity=identity, security=security, input_policy",1)
p.write_text(s)
