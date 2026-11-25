"""Run config probes that combine cc1 and linking as two driver commands."""
from pathlib import Path
import subprocess
import sys
import tempfile

from configure_corpus import LAUNCHER, ROOT, TOOLCHAIN, V0

mode, *args = sys.argv[1:]
argv = LAUNCHER + ["--driver-mode=" + mode, "-fuse-ld=/usr/bin/ld", "-B" + str(TOOLCHAIN)]
unit = [arg for arg in args if not arg.startswith("-") and Path(arg).suffix in (".c", ".cc", ".cpp", ".cxx")
        and Path(arg).is_file()]
if len(unit) != 1 or any(arg in args for arg in ("-c", "-E", "-S", "-M", "-MM")):
    raise SystemExit(subprocess.call(argv + args))

with tempfile.TemporaryDirectory(dir=".") as directory:
    obj = str(Path(directory) / "probe.o")
    compile_args = []
    it = iter(args)
    for arg in it:
        if arg == "-o":
            next(it, None)
        elif not arg.startswith(("-l", "-L", "-Wl,")) and arg not in ("-pie", "-shared", "-rdynamic"):
            compile_args.append(arg)
    first = subprocess.call(argv + compile_args + ["-c", "-o", obj])
    if first:
        raise SystemExit(first)
    link_args = [obj if arg == unit[0] else arg for arg in args]
    link_args += ["-Wl,--dynamic-linker=" + str(V0 / "lib64/ld-linux-x86-64.so.2"),
                  "-Wl,-rpath," + ":".join(str(ROOT / p) for p in ("lib64", "usr/lib64"))]
    raise SystemExit(subprocess.call(argv + link_args))
