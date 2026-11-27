#!/usr/bin/env python3
"""Expand the RPM switch matrix and validate packaging helper argv."""
import argparse
import contextlib
import hashlib
import importlib.util
import io
from itertools import product
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
from unittest.mock import patch

POST_BEGIN = "ARGV_CHECK_POST_BEGIN"
POST_END = "ARGV_CHECK_POST_END"
HELPER_NAME = "clang-bolt-helper.py"
PYTHON = re.compile(r"(?<!\S)python3\s+-B\s+")
PARAMETER = re.compile(r"\$(?:[A-Za-z_]\w*|[1-9@?]|\{[A-Za-z_]\w*\})")


class CapturedParser(BaseException):
    pass


def helper_parser(path):
    spec = importlib.util.spec_from_file_location("packaging_helper_for_argv", path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot import helper {path}")
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, {spec.name: module}):
        spec.loader.exec_module(module)

        def capture(parser, *args, **kwargs):
            raise CapturedParser(parser)

        # The helper currently builds its parser in main. Intercept parse_args
        # before dispatch and use that same parser for the observed argv.
        with patch.object(argparse.ArgumentParser, "parse_args", capture):
            try:
                module.main()
            except CapturedParser as captured:
                return captured.args[0]
    raise ValueError("helper did not construct an argparse parser")


def arguments_only(fragment):
    """Preserve quotes and expansion while cutting redirections/control tail."""
    if any(ch in fragment for ch in ("\n", "\r", "\0")):
        raise ValueError("multiline or NUL-containing helper argument fragment")
    quote = ""
    i = 0
    while i < len(fragment):
        ch = fragment[i]
        if quote == "'":
            if ch == quote:
                quote = ""
        elif ch == "\\":
            i += 1
        elif ch in '\"\'' and (not quote or ch == quote):
            quote = "" if quote else ch
        elif not quote and (ch in "|&;<>" or ch == "#" and (i==0 or fragment[i-1].isspace())):
            return fragment[:i]
        elif ch == chr(96) or (ch in "(){}" and not quote):
            raise ValueError(f"unsupported shell syntax in helper arguments: {fragment}")
        elif ch == "$":
            m = PARAMETER.match(fragment, i)
            if not m:
                raise ValueError(f"unsupported shell expansion in helper arguments: {fragment}")
            i = m.end()
            continue
        i += 1
    if quote or i > len(fragment):
        raise ValueError(f"unterminated shell argument: {fragment}")
    return fragment


def shell_words(fragment, cwd, variables=None, positional=()):
    tokens = arguments_only(fragment)
    proc = subprocess.run(
        ["/bin/bash", "--noprofile", "--norc", "-c",
         'set -uf\nset -- ' + tokens + '\nfor arg; do printf "%s\\0" "$arg"; done',
         "helper-argv-check", *positional],
        env={"PATH":"/nonexistent","LC_ALL":"C",**(variables or {})},
        cwd=cwd, capture_output=True, check=True, timeout=10,
    )
    return [os.fsdecode(word) for word in proc.stdout.split(b"\0")[:-1]]


def logical_lines(text):
    pending = ""
    for number, line in enumerate(text.splitlines(), 1):
        if not pending:
            start = number
        if line.endswith("\\"):
            pending += line[:-1]
        else:
            yield start, pending + line
            pending = ""
    if pending:
        raise ValueError("unterminated spec line continuation")


def invocations(expanded, helper, cwd):
    lines = list(logical_lines(expanded))
    bolt_work = [line.split("=",1)[1] for _, line in lines if line.startswith("BOLT_WORK=")]
    variables = {"bolt_stage":"fixture-stage"}
    if bolt_work:
        (fragment,) = bolt_work
        (variables["BOLT_WORK"],) = shell_words(fragment,cwd)
    step_calls = [(n, line.lstrip()[len("bolt_step "):]) for n,line in lines
                  if line.lstrip().startswith("bolt_step ")]
    step_template_seen = False
    for number, line in lines:
        if not line.lstrip() or line.lstrip().startswith(("#","Source")) or HELPER_NAME not in line:
            continue
        prog = PYTHON.search(line)
        if not prog or len(PYTHON.findall(line)) != 1 or line.count(HELPER_NAME) != 1:
            raise ValueError(f"line {number}: unrecognized helper call: {line}")
        fragment = line[prog.end():]
        if '"$@"' in fragment:
            if step_template_seen or ' run-step "$bolt_stage" ' not in fragment or not step_calls:
                raise ValueError(f"line {number}: unknown forwarded helper arguments")
            step_template_seen = True
            for called_at, call in step_calls:
                stage, *child = shell_words(call,cwd,variables)
                args = shell_words(fragment,cwd,{**variables,"bolt_stage":stage},child)
                yield called_at, number, line, checked_helper(args,helper)
        else:
            args=shell_words(fragment,cwd,variables,("fixture-stage","fixture.log"))
            yield number, None, line, checked_helper(args,helper)
    if step_calls and not step_template_seen:
        raise ValueError("missing helper invocation in bolt_step")


def checked_helper(args, source):
    if not args or args[0] != str(source):
        raise ValueError(f"unexpected helper executable word: {args}")
    return args[1:]


def parse_invocations(expanded, helper, parser, work, project, pgo, bolt, prof, fdata, manifest):
    calls, errors = [], []
    for line, template, invocation, args in invocations(expanded, helper, work):
        row = {"line":line,"template_line":template,"invocation":invocation,"argv":args}
        calls.append(row)
        try:
            diag = io.StringIO()
            with contextlib.redirect_stderr(diag):
                result=parser.parse_args(args)
        except SystemExit as stop:
            errors.append({"line":line,"argv":args,"exit_code":stop.code,"error":diag.getvalue()})
            continue
        row["parsed"]=vars(result)
    expected = {
        "pgo-prepare": int(pgo), "pgo-check-ninja": int(pgo),
        "pipeline": int(bolt), "post": int(bolt), "pgo-post": int(not bolt),
    }
    if not (pgo and bolt):
        expected["unpack"] = int(bolt)
    for cmd,n in expected.items():
        actual=sum(c["argv"][:1]==[cmd] for c in calls)
        if actual!=n:
            errors.append({"error":f"{cmd}: expected {n} invocation(s), got {actual}"})
    for row in calls:
        args=row.get("parsed",{})
        match args.get("cmd"):
            case "pgo-prepare":
                fields={"manifest":str(manifest),"project":project,"work":str(work/"pgo-profiles"),
                        "profile":str(prof),"bolt_profile":str(fdata) if bolt else None}
                expected_argv = ["pgo-prepare", str(manifest), project, fields["work"], str(prof)]
                if bolt:
                    expected_argv += ["--bolt-profile", str(fdata)]
                if row["argv"] != expected_argv:
                    errors.append({"line":row["line"],"error":"profile argv differs from expected words",
                                   "argv":row["argv"],"expected_argv":expected_argv})
            case "pgo-post":
                fields={"enabled":pgo}
            case "pipeline":
                fields={"debug_symbols":project=="T"}
            case _:
                continue
        if any(args[k]!=v for k,v in fields.items()):
            errors.append({"line":row["line"],"expected":fields,"actual":args,
                           "error":"parsed arguments differ from expected values"})
    return calls,errors


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream,"sha256").hexdigest()


def check(spec, helper, rpm_config, output, profile_name, bolt_name, manifest_name):
    spec, helper, output = (p.resolve() for p in (spec,helper,output))
    output.mkdir(parents=True)
    if helper.parent != spec.parent or helper.name != HELPER_NAME:
        raise ValueError("use the spec and helper from the same packaging directory")
    rpmspec = rpm_config["argv"]
    env = {**os.environ, "LC_ALL":"C", **rpm_config.get("env",{})}
    version = subprocess.check_output([*rpmspec,"--version"],env=env,text=True).strip()
    if not re.search(r"\b4\.14\.1\b",version):
        raise ValueError(f"Tizen RPM 4.14.1 is required: {version}")
    print(version,flush=True)
    parser = helper_parser(helper)
    # The macro is defined late in the recipe. Expand it at EOF for inspection
    # because rpmspec -P omits its body from the normal scriptlet output.
    source=output/spec.name
    source.write_text(spec.read_text()+f"\n{POST_BEGIN}\n%{{__spec_install_post}}\n{POST_END}\n")
    work=output/"build-fixture"
    work.mkdir()
    results={}
    for project,pgo,bolt in product(("T","D"),(True,False),(True,False)):
        case=f"{project}-pgo{int(pgo)}-bolt{int(bolt)}"
        switches=[s for enabled, name in ((pgo,"clang_pgo"),(bolt,"clang_bolt"))
                  for s in ("--define", f"_with{'out' if not enabled else ''}_{name} 1")]
        project_args=(["--define","_toolchain clang"] if project=="T" else ["--undefine","_toolchain"])
        argv=[*rpmspec,*rpm_config["base_args"],"--target","x86_64-tizen-linux",
              "--define","_sourcedir "+str(spec.parent),"--define","_topdir "+str(output/"rpmdir"),
              *project_args,*switches,"-P",str(source)]
        p=subprocess.run(argv,env=env,capture_output=True,text=True,timeout=60)
        (output/(case+".spec.txt")).write_text(p.stdout)
        (output/(case+".stderr.txt")).write_text(p.stderr)
        (output/(case+".command.json")).write_text(json.dumps(argv,indent=2)+"\n")
        if p.returncode:
            raise ValueError(f"{case}: rpmspec exited {p.returncode}: {p.stderr}")
        if p.stdout.count(POST_BEGIN)!=1 or p.stdout.count(POST_END)!=1:
            raise ValueError(f"{case}: missing expanded install-post boundaries")
        calls, errors=parse_invocations(p.stdout,helper,parser,work,project,pgo,bolt,
                                       spec.parent/profile_name,spec.parent/bolt_name,spec.parent/manifest_name)
        results[case]={"calls":calls,"errors":errors}
        print(f"{'FAIL' if errors else 'PASS'} {case} helper_calls={len(calls)}",flush=True)
        for e in errors:
            if "argv" in e:
                print("argv",shlex.join(e["argv"]))
            print(e["error"].rstrip())
    result={"status":"PASS" if all(not v["errors"] for v in results.values()) else "FAIL",
            "spec_sha256":sha(spec),"helper_sha256":sha(helper),"rpm_version":version,"matrix":results}
    (output/"result.json").write_text(json.dumps(result,indent=2)+"\n")
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--spec",type=Path,required=True)
    p.add_argument("--helper",type=Path,required=True)
    p.add_argument("--rpm-config",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--profile-name",required=True)
    p.add_argument("--bolt-profile-name",required=True)
    p.add_argument("--manifest-name",default="llvm-profiles.manifest")
    o=p.parse_args()
    try:
        result=check(o.spec,o.helper,json.loads(o.rpm_config.read_text()),o.output,
                     o.profile_name,o.bolt_profile_name,o.manifest_name)
    except (OSError,ValueError,subprocess.SubprocessError) as error:
        p.exit(1,f"FAIL: {error}\n")
    return int(result["status"]!="PASS")


if __name__=="__main__":
    raise SystemExit(main())
