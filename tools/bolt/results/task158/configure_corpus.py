"""Prepare build commands from frozen source packages without building them."""
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time

A = Path(__file__).resolve().parent
W = A.parents[1]
B = W.with_name(W.name + "-bolt")
ROOT = W / "temp/rebase-359934-20261111-r6/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0"
V0 = W / "archive/task156/private/V0"
TARGET = "x86_64-tizen-linux-gnu"
TOOLCHAIN = ROOT / "lib64/gcc" / TARGET / "14.2.0"
RESOURCE = ROOT / "usr/lib64/clang/22"
LAUNCHER = [str(V0 / "lib64/ld-linux-x86-64.so.2"), "--library-path",
            ":".join(str(V0 / p) for p in ("lib64", "usr/lib64")), str(V0 / "usr/bin/clang-22"),
            "--no-default-config", "-fintegrated-cc1", "--target=" + TARGET, "--sysroot=" + str(ROOT),
            "-resource-dir=" + str(RESOURCE), "--gcc-install-dir=" + str(TOOLCHAIN)]
BASE = B / "tools/bolt/results/final-20261103/continue/configs/basedev/build.conf"
GLOBAL = next(row.split(" ", 2)[2] for row in BASE.read_text().splitlines() if row.startswith("%define __global_cflags "))
ARCH = next(row.split(" ", 2)[2] for row in BASE.read_text().splitlines() if row.startswith("Optflags: x86_64 "))
FLAGS = shlex.split(ARCH.replace("%{__global_cflags}", GLOBAL))
# The package optflags include one GCC-only driver switch and a GCC
# debug-type switch. Preserve the base optflags receipt and exclude them.
FLAGS = [f for f in FLAGS if not f.startswith("--param=") and f != "-feliminate-unused-debug-types"]
ENV = {**os.environ, "LC_ALL": "C", "LD_LIBRARY_PATH": "", "LD_PRELOAD": ""}
CONF = A / "corpus-config"
CONF.mkdir(exist_ok=True)
CMAKE = [str(ROOT / "usr/lib64/ld-linux-x86-64.so.2"), "--library-path", str(ROOT / "usr/lib64"),
         str(ROOT / "usr/bin/cmake")]
NINJA = W / "temp/task133-d/tizen-tools/bin/ninja"

def pause():
    while next(int(line.split()[1])*1024 for line in Path("/proc/meminfo").read_text().splitlines()
               if line.startswith("MemAvailable:")) < 6*2**30:
        time.sleep(10)

def run(args, directory, name, env=ENV, timeout=180):
    pause()
    d = directory / (name + ".txt")
    (directory / (name + "-argv.json")).write_text(json.dumps(list(map(str, args)), indent=2) + "\n")
    with d.open("wb") as stream:
        p = subprocess.run(list(map(str, args)), cwd=directory, env=env, stdout=stream, stderr=subprocess.STDOUT,
                           timeout=timeout)
    return p.returncode

def source(name):
    root, = (A / "corpus-prep" / name / "BUILD").iterdir()
    return root

def main():
    retry = sys.argv[1:] == ["--retry-autoconf"]
    wrappers = {}
    for key, mode in (("CC", "gcc"), ("CXX", "g++")):
        wrapper = CONF / (key.lower() + ("-configure" if retry else ""))
        args = [sys.executable, "-B", str(A/"configure_driver.py"), mode] if retry else (
            LAUNCHER + ["--driver-mode=" + mode, "-fuse-ld=/usr/bin/ld", "-B" + str(TOOLCHAIN)])
        wrapper.write_text("#!/bin/sh\nexec " + shlex.join(args) + ' "$@"\n')
        wrapper.chmod(0o755)
        wrappers[key] = str(wrapper)
    ninja = CONF / "ninja"
    ninja.write_text("#!/bin/sh\nexec " + shlex.join(CMAKE[:3] + [str(NINJA)]) + ' "$@"\n')
    ninja.chmod(0o755)
    env = {**ENV, **wrappers}
    metadata = {"base_flags_source": str(BASE), "original_global_flags": GLOBAL, "original_arch_flags": ARCH,
                "optflags": FLAGS, "compiler": LAUNCHER, "packages": {}}
    if retry:
        metadata = json.loads((CONF / "configuration.json").read_text())
    for pkg, cfg in {
        "jsoncpp": ["-DJSONCPP_WITH_TESTS=OFF", "-DJSONCPP_WITH_POST_BUILD_UNITTEST=OFF",
                    "-DBUILD_SHARED_LIBS=ON", "-DBUILD_STATIC_LIBS=OFF"],
        "libwebp": [],
    }.items():
        if retry:
            continue
        build = CONF / pkg
        build.mkdir(exist_ok=True)
        f = FLAGS + (["-D__TIZEN__"] if pkg == "libwebp" else [])
        # Generate the native Ninja compile database. No package target is run.
        args = CMAKE + ["-G", "Ninja", "-S", source(pkg), "-B", build,
                        "-DCMAKE_MAKE_PROGRAM=" + str(ninja),
                        "-DCMAKE_INSTALL_PREFIX=/usr", "-DCMAKE_INSTALL_LIBDIR=lib64",
                        "-DCMAKE_FIND_ROOT_PATH=" + str(ROOT), "-DCMAKE_FIND_ROOT_PATH_MODE_LIBRARY=ONLY",
                        "-DCMAKE_FIND_ROOT_PATH_MODE_INCLUDE=ONLY",
                        "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON", "-DCMAKE_BUILD_TYPE=RelWithDebInfo",
                        "-DCMAKE_C_FLAGS_RELWITHDEBINFO=-DNDEBUG", "-DCMAKE_CXX_FLAGS_RELWITHDEBINFO=-DNDEBUG",
                        *cfg]
        result = run(args, build, "configure", {**env, "CFLAGS": shlex.join(f), "CXXFLAGS": shlex.join(FLAGS)})
        metadata["packages"][pkg] = {"configure_rc":result, "method":"CMake compile database"}
    for pkg, extra, args, sub in [
        ("expat", ["-fPIC"], ["--disable-static"], None),
        ("sqlite", ["-fPIC", "-DSQLITE_ENABLE_COLUMN_METADATA", "-DSQLITE_ENABLE_MEMORY_MANAGEMENT",
                    "-DSQLITE_DEFAULT_AUTOVACUUM=1", "-DSQLITE_DEFAULT_PAGE_SIZE=4096", "-Dfdatasync=fdatasync",
                    "-DSQLITE_TIZEN_FEATURE", "-DSQLITE_TEMP_STORE=2", "-DHAVE_USLEEP=1",
                    "-DSQLITE_DEFAULT_JOURNAL_SIZE_LIMIT=4194304", "-DSQLITE_DEFAULT_FILE_FORMAT=4",
                    "-DSQLITE_POWERSAFE_OVERWRITE=1", "-DSQLITE_ENABLE_ATOMIC_WRITE"],
         ["--disable-static", "--soname=legacy", "--disable-readline", "--fts3", "--all"], None),
        ("icu", ["-D_TIZEN_FEATURE_", "-fPIC"], ["--enable-static=no", "--enable-renaming=no", "--enable-shared",
              "--enable-plugins=yes", "--enable-samples=no", "--with-data-packaging=library"], "source"),
    ]:
        build = CONF / pkg
        build.mkdir(exist_ok=True)
        base = source(pkg)
        if sub:
            base /= sub
        e = {**env, "CFLAGS": shlex.join(FLAGS + extra), "CXXFLAGS": shlex.join(FLAGS + extra), "LDFLAGS": "-pie"}
        if retry:
            for name in ("configure.txt", "configure-argv.json", "config.log"):
                path = build / name
                if path.exists():
                    path.replace(build / ("first-" + name))
        result = run([base / "configure", "--prefix=/usr", "--libdir=/usr/lib64", *args], build, "configure", e)
        if result == 0:
            if pkg == "icu":
                # Direct leaf invocation prints compiler commands without running
                # the package's recursive recipe or any target.
                result = run(["/usr/bin/make", "-C", str(build / "common"), "-n"], build, "make-dry", e)
            else:
                result = run(["/usr/bin/make", "-n"], build, "make-dry", e)
        metadata["packages"][pkg] = {"configure_make_dry_rc":result, "method":"configured make -n"}
    pkg = "bzip2"
    build = CONF / pkg
    build.mkdir(exist_ok=True)
    if not retry:
        e = {**env, "CFLAGS": shlex.join(FLAGS + ["-fPIC"]), "LDFLAGS": "-pie"}
        result = run(["/usr/bin/make", "-C", source(pkg), "-f", "Makefile-libbz2_so", "-n",
                      "CC=" + wrappers["CC"]], build, "make-dry", e)
        metadata["packages"][pkg] = {"make_dry_rc":result, "method":"spec Makefile-libbz2_so make -n"}
    (CONF / "configuration.json").write_text(json.dumps(metadata, indent=2) + "\n")

if __name__ == "__main__":
    main()
