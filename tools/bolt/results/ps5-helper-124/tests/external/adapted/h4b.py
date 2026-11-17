import importlib.util, sys
spec = importlib.util.spec_from_file_location('conv', sys.argv[1]); c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
d = sys.argv[2]
def hdr(name, size): return (name.ljust(16) + '0'.ljust(12) + '0'.ljust(6)*2 + '644'.ljust(8) + str(size).ljust(10)).encode() + b'`\n'
def entries(data):
    pos = 8
    while pos < len(data):
        name = data[pos:pos+16].decode().rstrip(); size = int(data[pos+48:pos+58])
        stored = size if (data[:8] == b'!<arch>\n' or name in ('/', '//', '/SYM64/')) else 0
        yield name, pos, size, pos + 60 + stored + stored % 2
        pos = pos + 60 + stored + stored % 2
def run(label, path):
    try:
        r = c.inspect(path); print(f'{label:40} ACCEPT names={[m["name"] for m in r["members"]]}')
    except Exception as e: print(f'{label:40} REJECT {type(e).__name__}: {e}')
for n in ('normal', 'thin', 'short'):
    run(n+'.a', f'{d}/{n}.a')
for n in ('normal', 'thin'):
    data = open(f'{d}/{n}.a', 'rb').read()
    (_, p, size, end), = [e for e in entries(data) if e[0] == '//']
    table = data[p+60:p+60+size]
    evil = table.replace(b'a_very_long', b'z_very_long').replace(b'another', b'xnother')
    blob = hdr('//', len(evil)) + evil + (b'\n' if len(evil) % 2 else b'')
    open(f'{d}/{n}-dup.a', 'wb').write(data[:end] + blob + data[end:])
    run(n+' + second same-size // table', f'{d}/{n}-dup.a')
    open(f'{d}/{n}-emptyfirst.a', 'wb').write(data[:p] + hdr('//', 0) + data[p:])
    run(n+' + empty // before the real one', f'{d}/{n}-emptyfirst.a')
data = open(f'{d}/short.a', 'rb').read()
open(f'{d}/short-empty.a', 'wb').write(data[:8] + hdr('//', 0) + data[8:])
run('short names + one empty //', f'{d}/short-empty.a')
