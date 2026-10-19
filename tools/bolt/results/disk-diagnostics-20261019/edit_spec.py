from pathlib import Path
E=Path(__file__).resolve().parent;p=E.parents[1]/'temp/bolt-v4-20261013/v41/llvm-source/packaging/llvm.spec';s=p.read_text()
start=s.index('%install\n');end=s.index('# File-list baseline',start)
setup='''%install
cd build
%ifarch x86_64
%if %{with clang_bolt}
%global __bolt_disk_reporting 1
# Reject debug-named buildroots before any BOLT action.
case $(printf '%s' '%{buildroot}' | LC_ALL=C tr '[:upper:]' '[:lower:]') in
  *debug*) echo 'BOLT buildroot absolute path contains debug' >&2; exit 1 ;;
esac
BOLT_BUILD="$PWD"
BOLT_WORK="$PWD/clang-bolt"
BOLT_INSTALL_ROOT="%{buildroot}"
export BOLT_BUILD BOLT_WORK BOLT_INSTALL_ROOT
bolt_fail() {
  python3 -B %{SOURCE1201} disk-diagnose "$1" "$2" || true
  exit 1
}
bolt_step() {
  bolt_stage=$1
  shift
  python3 -B %{SOURCE1201} run-step "$bolt_stage" "$BOLT_WORK/$bolt_stage.log" -- "$@" || bolt_fail "$bolt_stage" "$BOLT_WORK/$bolt_stage.log"
}
bolt_capture() {
  bolt_stage=$1
  bolt_output=$2
  shift 2
  python3 -B %{SOURCE1201} run-step "$bolt_stage" "$BOLT_WORK/$bolt_stage.log" --output "$bolt_output" -- "$@" || bolt_fail "$bolt_stage" "$BOLT_WORK/$bolt_stage.log"
}
# Observability only: sizes vary with this build, so no disk admission budget.
python3 -B %{SOURCE1201} disk-report begin
%endif
%endif
%{?__bolt_disk_reporting:bolt_step ordinary-install }cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}/usr -P cmake_install.cmake
%ifarch x86_64
%if %{with clang_bolt}
echo "BOLT_BUILDROOT_OK %{buildroot}" || bolt_fail buildroot-output -
bolt_step preflight python3 -B %{SOURCE1201} preflight
bolt_step certified python3 -B %{SOURCE1201} certified
if [ -r /proc/self/stat ]; then echo BOLT_PROC_OK; else echo BOLT_PROC_MISSING; fi
# One relink: emit-relocs, then LLVM strip-debug, BOLT and full strip.
# The package build owns its original ThinLTO cache; do not duplicate it.
'''
s=s[:start]+setup+s[end:]
start=s.index('# File-list baseline');end=s.index('# Any subsequent buildroot mutation',start)
block='''# File-list baseline is the actual ordinary CMake install, not a name whitelist.
bolt_step snapshot python3 -B %{SOURCE1201} snapshot "%{buildroot}" "$BOLT_WORK/install-before.json"
bolt_step manifest-copy cp install_manifest.txt "$BOLT_WORK/install-manifest-before.txt"
bolt_step ordinary-copy cp -p bin/clang-22 "$BOLT_WORK/ordinary-clang-22"
bolt_capture link-command "$BOLT_WORK/link.original" ninja -t commands -s bin/clang-22
bolt_step unpack python3 -B %{SOURCE1201} unpack %{SOURCE1200} "$BOLT_WORK/profile.fdata"
bolt_step configure cmake -S ../llvm -B . \
  '-DLLVM_ENABLE_PROJECTS=clang;lldb;clang-tools-extra;lld;compiler-rt;openmp;bolt' \
  -DBOLT_BUILD_TOOLS=OFF -DBOLT_ENABLE_RUNTIME=OFF \
  -DBOLT_INCLUDE_TESTS=OFF -DBOLT_TARGETS_TO_BUILD=X86
# Only certified BOLT tasks and the paired configure-refreshed TF anchor.
echo BOLT_TOOL_DRY_RUN_BEGIN || bolt_fail dry-run-output -
LC_ALL=C NINJA_STATUS='[%%f/%%t] ' bolt_capture tool-dry-run "$BOLT_WORK/tool-dry-run.txt" ninja -n llvm-bolt
echo BOLT_TOOL_DRY_RUN_END || bolt_fail dry-run-output -
bolt_capture tool-plan "$BOLT_WORK/tool-plan.json" python3 -B %{SOURCE1201} tool-plan "$BOLT_WORK/tool-dry-run.txt"
bolt_step tool-prepare python3 -B %{SOURCE1201} tool-prepare "$PWD" "$BOLT_WORK/tool-plan.json" "$BOLT_WORK/tool-before.json"
LC_ALL=C NINJA_STATUS='[%%f/%%t] ' python3 -B %{SOURCE1201} run-step tool-build "$BOLT_WORK/tool-build.txt" --success-marker BOLT_NINJA_EXIT_0 -- ninja -j 1 llvm-bolt || bolt_fail tool-build "$BOLT_WORK/tool-build.txt"
bolt_step tool-verify python3 -B %{SOURCE1201} tool-verify "$PWD" "$BOLT_WORK/tool-plan.json" "$BOLT_WORK/tool-build.txt" \
  "$BOLT_WORK/tool-before.json" "$BOLT_WORK/tool-build-verification.json"
python3 -B %{SOURCE1201} disk-report tool-built
bolt_step pipeline python3 -B %{SOURCE1201} pipeline "$PWD" "$BOLT_WORK" "$PWD/bin/llvm-bolt"
echo BOLT_PIPELINE_PASS || bolt_fail pipeline-output -
python3 -B %{SOURCE1201} disk-report pipeline
# BOLT configuration/build/rewrite must not change the ordinary installation.
# Do not reinstall: that would add BOLT libraries, unregistered aliases and exports.
bolt_step compare-root python3 -B %{SOURCE1201} compare-root "%{buildroot}" "$BOLT_WORK/install-before.json" \
  "$BOLT_WORK/install-after-pipeline.json"
echo BOLT_COMPARE_ROOT_PASS || bolt_fail compare-root-output -
'''
s=s[:start]+block+s[end:]
# Route all later ordinary-install writes through checked commands only when BOLT is on.
start=s.index('ln -sf %{_prefix}/bin/clang++',s.index('%install\n'));end=s.index('%post -n clang',start)
part=s[start:end];lines=part.splitlines(True);count=0;out=[]
for line in lines:
 if line.startswith(('ln ','mkdir ','mv ','cp ','rm ','python3 %{SOURCE1005}')):
  count+=1;line='%{?__bolt_disk_reporting:bolt_step install-write-'+str(count)+' }'+line
 out.append(line)
part=''.join(out)
part=part.replace('cat >> %{buildroot}/%{_prefix}/bin/clang.cfg << EOF', '''%{?__bolt_disk_reporting:bolt_step clang-config /bin/sh -c 'cat >> "$1"' sh %{buildroot}/%{_prefix}/bin/clang.cfg}%{!?__bolt_disk_reporting:cat >> %{buildroot}/%{_prefix}/bin/clang.cfg} << EOF''')
part=part.replace('python3 %{SOURCE1201} install ', 'python3 -B %{SOURCE1201} install ')
part=part.replace('"$BOLT_WORK/install-state.json" "$BOLT_WORK/identity.json" || exit 1', '"$BOLT_WORK/install-state.json" "$BOLT_WORK/identity.json" || bolt_fail install "$BOLT_WORK/install.log"')
s=s[:start]+part+s[end:]
start=s.index('%define __spec_install_post \\\n',s.index('%global __bolt_original_spec_install_post'))
end=s.index('%endif',start)
post=r'''%define __spec_install_post \
    python3 -B %{SOURCE1201} run-step platform-post "%{_builddir}/%{buildsubdir}/build/clang-bolt/platform-post.log" -- /bin/sh -e <<'BOLT_PLATFORM_POST' || { python3 -B %{SOURCE1201} disk-diagnose platform-post "%{_builddir}/%{buildsubdir}/build/clang-bolt/platform-post.log" || true; exit 1; } \
    %{__bolt_original_spec_install_post} \
BOLT_PLATFORM_POST \
    python3 -B %{SOURCE1201} run-step post "%{_builddir}/%{buildsubdir}/build/clang-bolt/post.log" -- python3 -B %{SOURCE1201} post "%{buildroot}" "%{_builddir}/%{buildsubdir}/build/clang-bolt/install-state.json" "%{_builddir}/%{buildsubdir}/build/clang-bolt/ordinary-clang-22" "%{_builddir}/%{buildsubdir}/build/clang-bolt/post-gate" --resource-dir "%{buildroot}%{_libdir}/clang/%{llvm_version}" || { python3 -B %{SOURCE1201} disk-diagnose post "%{_builddir}/%{buildsubdir}/build/clang-bolt/post.log" || true; exit 1; } \
    echo BOLT_POST_GATE_PASS || exit 1 \
    python3 -B %{SOURCE1201} disk-report post
'''
s=s[:start]+post+s[end:]
assert 'disk-preflight' not in s and '17179869184' not in s
p.write_text(s);print('spec changed, ordinary-install write sites checked:',count)
