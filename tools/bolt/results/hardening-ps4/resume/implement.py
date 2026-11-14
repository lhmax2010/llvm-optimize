from pathlib import Path
import subprocess
E=Path(__file__).resolve().parent
N=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/hardening-ps4-20261114/source')
p=N/'packaging/llvm-static-archives-native.py';s=p.read_text()
def replace(old,new):
 global s
 assert s.count(old)==1,old
 s=s.replace(old,new)
replace("        if section[1] == 0x40000014:\n", "        if section[1] == 19:  # SHT_RELR is not supported in ET_REL members.\n            raise ValueError('unsupported RELR relocation section')\n        if section[1] == 0x40000014:\n")
replace("            limit = struct.unpack_from('<IIQQ', data, target[4])[2]\n", "            compression, reserved, limit, alignment = struct.unpack_from('<IIQQ', data, target[4])\n            if compression not in (1, 2):  # ELFCOMPRESS_ZLIB / ELFCOMPRESS_ZSTD\n                raise ValueError('unsupported ELF compression type: '+str(compression))\n            if alignment and alignment & (alignment - 1):\n                raise ValueError('invalid compressed ELF section alignment: '+str(alignment))\n")
replace("            if kind != 0 and r_offset + X86_64_RELOCATION_WIDTHS[kind] > limit:\n", "            width = X86_64_RELOCATION_WIDTHS[kind]\n            if kind != 0 and (r_offset + width > limit or (width == 0 and r_offset == limit)):\n")
replace("def install_main():\n", '''def log_startup_context():
    """Report exported target options and Python's inherited signal handlers."""
    architecture = {}
    for name in ('CFLAGS', 'CXXFLAGS'):
        try:
            tokens = shlex.split(os.environ.get(name, ''))
        except ValueError as error:
            # Diagnostics must not change conversion of already recorded IR.
            architecture[name] = {'parse_error': str(error)}
            continue
        # Same inherited architecture categories as the packaging flag policy.
        # Keep order and duplicates: the compiler applies last-option semantics.
        architecture[name] = [token for token in tokens if token == '-m64' or
                              token.startswith(('-march=', '-mtune=', '-msse', '-mfpmath='))]
    inherited = {}
    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
        handler = signal.getsignal(sig)
        inherited[signal.Signals(sig).name] = ('ignored' if handler == signal.SIG_IGN else
                                             'default' if handler == signal.SIG_DFL else 'handler')
    print('NATIVE_ARCHIVES_STARTUP', json.dumps({
        'architecture_parameters': architecture, 'signals': inherited}), flush=True)


def install_main():
''')
replace("    _CANCEL_SIGNAL = None\n    if signal.getsignal(signal.SIGCHLD)", "    _CANCEL_SIGNAL = None\n    log_startup_context()\n    if signal.getsignal(signal.SIGCHLD)")
p.write_text(s)
(E/'product.diff').write_bytes(subprocess.check_output(['git','-C',str(N),'diff','--','packaging/llvm-static-archives-native.py']))
print('changed only',subprocess.check_output(['git','-C',str(N),'diff','--name-only'],text=True).strip())
