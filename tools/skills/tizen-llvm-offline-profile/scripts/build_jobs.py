#!/usr/bin/python3
"""Apply a scheduling profile to LLVM's pinned Ninja configuration."""
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys


COMPILE = "LLVM_PARALLEL_COMPILE_JOBS"
LINK = "LLVM_PARALLEL_LINK_JOBS"
LINK_FLAGS = tuple(f"CMAKE_{kind}_LINKER_FLAGS" for kind in ("EXE", "SHARED", "MODULE"))
THIN_FLAG = re.compile(r"(?<!\S)-Wl,--thinlto-jobs=\S+")
LEGACY_FLAG = re.compile(r"(?<!\S)-Wl,[^\s]*(?:thinlto-jobs|plugin-opt(?:=|,)jobs)[^\s]*")


def schedule_flags(flags, jobs):
    result = THIN_FLAG.sub(f"-Wl,--thinlto-jobs={jobs}", flags)
    if LEGACY_FLAG.search(THIN_FLAG.sub("", result)) or len(THIN_FLAG.findall(result)) > 1:
        raise ValueError("conflicting ThinLTO scheduling flags")
    if THIN_FLAG.search(result):
        return result
    return " ".join(value for value in (flags, f"-Wl,--thinlto-jobs={jobs}") if value)


def schedule_defines(values, counts):
    jobs, thinlto, link = counts
    updated = {key: schedule_flags(values[key], thinlto) for key in LINK_FLAGS}
    updated.update({COMPILE: str(jobs), LINK: str(link)})
    return updated


def definition(argument):
    return argument[2:].partition("=")[0].split(":", 1)[0] if argument.startswith("-D") else ""


def initial_args(argv, counts, ldflags):
    if not any(definition(arg) == COMPILE for arg in argv):
        return None
    if "-DLLVM_ENABLE_LTO=Thin" not in argv:
        raise ValueError("LLVM job policy requires ThinLTO for this configuration")
    selected = {}
    for argument in argv:
        key = definition(argument)
        if key in (*LINK_FLAGS, COMPILE, LINK):
            if key in selected:
                raise ValueError(f"duplicate configuration setting: {key}")
            selected[key] = argument.split("=", 1)[1]
    if not all(key in selected for key in (COMPILE, LINK, *LINK_FLAGS[:2])):
        raise ValueError("missing job pool or linker settings")
    if "-fuse-ld=lld" not in shlex.split(selected[LINK_FLAGS[0]]):
        raise ValueError("the LLVM executable linker is not lld")
    selected.setdefault(LINK_FLAGS[2], ldflags)
    updated = schedule_defines(selected, counts)
    return [arg for arg in argv if definition(arg) not in updated] + arguments(updated)


def arguments(values):
    return [f"-D{key}={value}" for key, value in values.items()]


def read_cache(directory):
    values = {}
    for line in (directory / "CMakeCache.txt").read_text().splitlines():
        match = re.fullmatch(r"([A-Z0-9_]+):[^=]+=(.*)", line)
        if match:
            values[match[1]] = match[2]
    return values


def verify(directory, counts, phase):
    jobs, thinlto, link = counts
    values = read_cache(directory)
    if (values[COMPILE] != str(jobs) or values[LINK] != str(link) or
            any(THIN_FLAG.findall(values[key]) != [f"-Wl,--thinlto-jobs={thinlto}"]
                for key in LINK_FLAGS)):
        raise ValueError("LLVM CMake cache did not retain the requested scheduling values")
    rules = (directory / "CMakeFiles/rules.ninja").read_text()
    for name, size in (("compile", jobs), ("link", link)):
        if not re.search(rf"(?m)^pool {name}_job_pool\n +depth = {size}$", rules):
            raise ValueError(f"LLVM Ninja {name} pool did not retain depth {size}")
    print(f"LLVM_BUILD_JOBS phase={phase} compile={jobs} thinlto={thinlto} link={link}", flush=True)


def from_environment():
    counts = tuple(int(os.environ[key]) for key in ("PROFILE_JOBS", "PROFILE_THINLTO_JOBS", "PROFILE_LINK_JOBS"))
    if counts not in ((2, 2, 1), (4, 4, 1), (6, 6, 1)):
        raise ValueError(f"invalid LLVM scheduling profile: {counts}")
    return counts


def install(root, counts):
    if not root.is_absolute() or not (root / "var/tmp").is_dir():
        raise ValueError("an absolute, prepared RPM build root is required")
    inner = Path("/var/tmp/llvm-stage-jobs")
    dest = root / inner.relative_to("/")
    if not dest.parent.resolve(strict=True).is_relative_to(root.resolve(strict=True)):
        raise ValueError("RPM shell destination escapes the prepared root")
    dest.mkdir()
    shutil.copyfile(Path(__file__).resolve(), dest / "cmake")
    (dest / "cmake").chmod(0o755)
    shell = dest / "build-shell"
    with shell.open("x") as stream:
        stream.write(
            "#!/bin/sh\n"
            f"export PATH={inner}:\"$PATH\"\n"
            f"export PROFILE_JOBS={counts[0]} PROFILE_THINLTO_JOBS={counts[1]} PROFILE_LINK_JOBS={counts[2]}\n"
            "exec /bin/sh \"$@\"\n"
        )
    shell.chmod(0o755)
    return str(inner / shell.name)


def require_rpm_log(path, counts):
    jobs, thinlto, link = counts
    marker = f"LLVM_BUILD_JOBS phase=configure compile={jobs} thinlto={thinlto} link={link}"
    configured = ninja = False
    with path.open(errors="replace") as stream:
        for line in stream:
            configured |= line.rstrip().endswith(marker)
            ninja |= bool(re.search(rf"\b(?:/usr/bin/)?ninja\s+.*?-j(?:\s+)?{jobs}(?:\s|$)", line))
    if not (configured and ninja):
        raise ValueError("missing effective LLVM build jobs marker or Ninja -j in the RPM build log")
    print(f"LLVM_BUILD_JOBS phase=rpm ninja={jobs}", flush=True)


def main():
    argv = sys.argv[1:]
    if Path(sys.argv[0]).name == "cmake":
        counts = from_environment()
        forwarded = initial_args(argv, counts, os.environ.get("LDFLAGS", ""))
        if forwarded is None:
            os.execv("/usr/bin/cmake", ["/usr/bin/cmake", *argv])
        directory = Path.cwd()
        subprocess.run(["/usr/bin/cmake", *forwarded], check=True)
        verify(directory, counts, "configure")
    elif len(argv) == 2 and argv[0] == "install":
        print(install(Path(argv[1]), from_environment()))
    elif len(argv) >= 3 and argv[0] == "reconfigure":
        directory, cmake = Path(argv[1]), Path(argv[2])
        if not directory.is_absolute() or not cmake.is_absolute():
            raise ValueError("absolute CMake and build directory paths are required")
        counts = from_environment()
        values = schedule_defines(read_cache(directory), counts)
        subprocess.run([str(cmake), *argv[3:], *arguments(values)], cwd=directory, check=True)
        verify(directory, counts, "reconfigure")
    else:
        raise ValueError("use install ROOT or reconfigure BUILD_DIRECTORY CMAKE [ARG ...]")


if __name__ == "__main__":
    main()
