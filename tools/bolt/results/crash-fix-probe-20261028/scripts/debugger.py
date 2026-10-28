from common import *
cmd=D/'objcopy.gdb'
cmd.write_text('set pagination off\nset confirm off\nset debuginfod enabled off\nset auto-load python-scripts off\nset debug-file-directory /nonexistent\nrun\nbt\ninfo registers\nframe 1\ninfo registers\ndisassemble\ninfo proc mappings\n')
print(run('objcopy-gdb',['gdb','-nx','-batch','-x',cmd,'--args',*tool('llvm-objcopy'),'--only-keep-debug',WORK/'clang.bolt',D/'gdb.debug'],timeout=120),flush=True)
print(run('lldb-version',[*LD,R/'usr/bin/lldb-instr','--version'],env={**os.environ,'LLVM_PROFILE_FILE':str(D/'lldb.profraw')}),flush=True)
print(run('lldb-deps',[*LD,'--list',R/'usr/bin/lldb-instr']),flush=True)
