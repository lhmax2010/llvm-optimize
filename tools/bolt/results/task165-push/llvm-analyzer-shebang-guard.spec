Name:       llvm-analyzer-shebang-guard
Version:    1
Release:    1
Summary:    Clang analyzer package smoke test
License:   MIT
Source0:    %{name}-%{version}.tar.gz
BuildRequires: clang
BuildRequires: perl
BuildRequires: python3
BuildArch:  noarch

%description
Check the analyzer tools in a build root using the installed Clang packages.

%prep
%setup -q

%build
fail=0
emit() {
    printf 'TASK163_CHECK %s %s rc=%s\n' "$1" "$2" "$3"
}
rc=0
LC_ALL=C rpm -q llvm-devel > llvm-devel.txt 2>&1 || rc=$?
cat llvm-devel.txt
if test "$rc" = 1 && grep -Fxq 'package llvm-devel is not installed' llvm-devel.txt; then
    emit llvm-devel-absent PASS "$rc"
else
    emit llvm-devel-absent FAIL "$rc"
    exit 1
fi

for pkg in clang llvm libllvm; do
    identity=$(rpm -q --qf '%%{NAME} %%{VERSION}-%%{RELEASE} %%{VCS}\n' "$pkg") || fail=1
    printf '%s\n' "$identity"
    case "$identity" in
        *'#2960ffa545a38ee71dbb38861af7831933033089') emit "provider-$pkg" PASS 0 ;;
        *) emit "provider-$pkg" FAIL 1; fail=1 ;;
    esac
done
if test "$fail" != 0; then
    exit 1
fi

rc=0
LC_ALL=C scan-build -o "$PWD/report" clang -c null.c -o null.o || rc=$?
if test "$rc" = 0 && test -s null.o; then
    emit scan-build PASS "$rc"
else
    emit scan-build FAIL "$rc"
    fail=1
fi
found=0
for index in report/*/index.html; do
    if test -s "$index"; then
        root=${index%/*}
        printf 'TASK163_REPORT %s\n' "$index"
        ls -l "$index" "$root/sorttable.js" "$root/scanview.css" || :
        if test -s "$root/sorttable.js" && test -s "$root/scanview.css" &&
           grep -Fq sorttable.js "$index" && grep -Fq scanview.css "$index"; then
            found=1
        fi
    fi
done
if test "$found" = 1; then
    emit report-html-assets PASS 0
else
    emit report-html-assets FAIL 1
    fail=1
fi

printf 'TASK163_BEFORE_BEGIN %s\n' /usr/bin/scan-view
head -n 1 /usr/bin/scan-view
rc=0
LC_ALL=C /usr/bin/scan-view --help || rc=$?
printf 'TASK163_BEFORE_END %s rc=%s\n' /usr/bin/scan-view "$rc"
test "$(head -n 1 /usr/bin/scan-view)" = '#!/usr/bin/env python'
install -D -m 0755 /usr/bin/scan-view "%{buildroot}/usr/bin/scan-view"
cmp /usr/bin/scan-view "%{buildroot}/usr/bin/scan-view"

printf 'TASK163_BEFORE_BEGIN %s\n' /usr/share/clang/run-find-all-symbols.py
head -n 1 devel-fixture/usr/share/clang/run-find-all-symbols.py
rc=0
LC_ALL=C devel-fixture/usr/share/clang/run-find-all-symbols.py --help || rc=$?
printf 'TASK163_BEFORE_END %s rc=%s\n' /usr/share/clang/run-find-all-symbols.py "$rc"
test "$(head -n 1 devel-fixture/usr/share/clang/run-find-all-symbols.py)" = '#!/usr/bin/env python'
install -D -m 0755 devel-fixture/usr/share/clang/run-find-all-symbols.py "%{buildroot}/usr/share/clang/run-find-all-symbols.py"
cmp devel-fixture/usr/share/clang/run-find-all-symbols.py "%{buildroot}/usr/share/clang/run-find-all-symbols.py"

printf 'TASK163_BEFORE_BEGIN %s\n' /usr/share/opt-viewer/opt-diff.py
head -n 1 devel-fixture/usr/share/opt-viewer/opt-diff.py
rc=0
LC_ALL=C devel-fixture/usr/share/opt-viewer/opt-diff.py --help || rc=$?
printf 'TASK163_BEFORE_END %s rc=%s\n' /usr/share/opt-viewer/opt-diff.py "$rc"
test "$(head -n 1 devel-fixture/usr/share/opt-viewer/opt-diff.py)" = '#!/usr/bin/env python'
install -D -m 0755 devel-fixture/usr/share/opt-viewer/opt-diff.py "%{buildroot}/usr/share/opt-viewer/opt-diff.py"
cmp devel-fixture/usr/share/opt-viewer/opt-diff.py "%{buildroot}/usr/share/opt-viewer/opt-diff.py"

printf 'TASK163_BEFORE_BEGIN %s\n' /usr/share/opt-viewer/opt-stats.py
head -n 1 devel-fixture/usr/share/opt-viewer/opt-stats.py
rc=0
LC_ALL=C devel-fixture/usr/share/opt-viewer/opt-stats.py --help || rc=$?
printf 'TASK163_BEFORE_END %s rc=%s\n' /usr/share/opt-viewer/opt-stats.py "$rc"
test "$(head -n 1 devel-fixture/usr/share/opt-viewer/opt-stats.py)" = '#!/usr/bin/env python'
install -D -m 0755 devel-fixture/usr/share/opt-viewer/opt-stats.py "%{buildroot}/usr/share/opt-viewer/opt-stats.py"
cmp devel-fixture/usr/share/opt-viewer/opt-stats.py "%{buildroot}/usr/share/opt-viewer/opt-stats.py"

printf 'TASK163_BEFORE_BEGIN %s\n' /usr/share/opt-viewer/opt-viewer.py
head -n 1 devel-fixture/usr/share/opt-viewer/opt-viewer.py
rc=0
LC_ALL=C devel-fixture/usr/share/opt-viewer/opt-viewer.py --help || rc=$?
printf 'TASK163_BEFORE_END %s rc=%s\n' /usr/share/opt-viewer/opt-viewer.py "$rc"
test "$(head -n 1 devel-fixture/usr/share/opt-viewer/opt-viewer.py)" = '#!/usr/bin/env python'
install -D -m 0755 devel-fixture/usr/share/opt-viewer/opt-viewer.py "%{buildroot}/usr/share/opt-viewer/opt-viewer.py"
cmp devel-fixture/usr/share/opt-viewer/opt-viewer.py "%{buildroot}/usr/share/opt-viewer/opt-viewer.py"

printf 'TASK163_BEFORE_BEGIN %s\n' /usr/share/opt-viewer/optrecord.py
head -n 1 devel-fixture/usr/share/opt-viewer/optrecord.py
rc=0
LC_ALL=C devel-fixture/usr/share/opt-viewer/optrecord.py --help || rc=$?
printf 'TASK163_BEFORE_END %s rc=%s\n' /usr/share/opt-viewer/optrecord.py "$rc"
test "$(head -n 1 devel-fixture/usr/share/opt-viewer/optrecord.py)" = '#!/usr/bin/env python'
install -D -m 0755 devel-fixture/usr/share/opt-viewer/optrecord.py "%{buildroot}/usr/share/opt-viewer/optrecord.py"
cmp devel-fixture/usr/share/opt-viewer/optrecord.py "%{buildroot}/usr/share/opt-viewer/optrecord.py"

install -d "%{buildroot}/usr/share"
cp -a /usr/share/scan-view "%{buildroot}/usr/share/"
cp -a devel-fixture/usr/share/opt-viewer "%{buildroot}/usr/share/"
install -d "%{buildroot}/usr/lib"
cp -a /usr/lib/libscanbuild /usr/lib/libear "%{buildroot}/usr/lib/"
printf 'TASK165_POSITIVE_BEGIN\n'
sed -i '1s|^#!/usr/bin/env python$|#!/usr/bin/env python3|' "%{buildroot}/usr/bin/scan-view"
sed -i '1s|^#!/usr/bin/env python$|#!/usr/bin/env python3|' "%{buildroot}/usr/share/clang/run-find-all-symbols.py"
sed -i '1s|^#!/usr/bin/env python$|#!/usr/bin/env python3|' "%{buildroot}/usr/share/opt-viewer/opt-diff.py"
sed -i '1s|^#!/usr/bin/env python$|#!/usr/bin/env python3|' "%{buildroot}/usr/share/opt-viewer/opt-stats.py"
sed -i '1s|^#!/usr/bin/env python$|#!/usr/bin/env python3|' "%{buildroot}/usr/share/opt-viewer/opt-viewer.py"
sed -i '1s|^#!/usr/bin/env python$|#!/usr/bin/env python3|' "%{buildroot}/usr/share/opt-viewer/optrecord.py"
for f in usr/bin/scan-view usr/share/clang/run-find-all-symbols.py \
         usr/share/opt-viewer/opt-diff.py usr/share/opt-viewer/opt-stats.py \
         usr/share/opt-viewer/opt-viewer.py usr/share/opt-viewer/optrecord.py; do
    test "$(head -n 1 "%{buildroot}/$f")" = '#!/usr/bin/env python3' ||
        { echo "Unexpected interpreter in $f" >&2; exit 1; }
done
printf 'TASK165_POSITIVE_PASS six scripts\n'
sed -i '1c#!/usr/bin/python' "%{buildroot}/usr/bin/scan-view"
printf 'TASK165_NEGATIVE_BEGIN\n'
set +e
( set -e
sed -i '1s|^#!/usr/bin/env python$|#!/usr/bin/env python3|' "%{buildroot}/usr/bin/scan-view"
sed -i '1s|^#!/usr/bin/env python$|#!/usr/bin/env python3|' "%{buildroot}/usr/share/clang/run-find-all-symbols.py"
sed -i '1s|^#!/usr/bin/env python$|#!/usr/bin/env python3|' "%{buildroot}/usr/share/opt-viewer/opt-diff.py"
sed -i '1s|^#!/usr/bin/env python$|#!/usr/bin/env python3|' "%{buildroot}/usr/share/opt-viewer/opt-stats.py"
sed -i '1s|^#!/usr/bin/env python$|#!/usr/bin/env python3|' "%{buildroot}/usr/share/opt-viewer/opt-viewer.py"
sed -i '1s|^#!/usr/bin/env python$|#!/usr/bin/env python3|' "%{buildroot}/usr/share/opt-viewer/optrecord.py"
for f in usr/bin/scan-view usr/share/clang/run-find-all-symbols.py \
         usr/share/opt-viewer/opt-diff.py usr/share/opt-viewer/opt-stats.py \
         usr/share/opt-viewer/opt-viewer.py usr/share/opt-viewer/optrecord.py; do
    test "$(head -n 1 "%{buildroot}/$f")" = '#!/usr/bin/env python3' ||
        { echo "Unexpected interpreter in $f" >&2; exit 1; }
done
) > negative-raw.txt 2>&1
negative_rc=$?
set -e
cat negative-raw.txt
printf 'TASK165_NEGATIVE_RC %s\n' "$negative_rc"
test "$negative_rc" -eq 1
grep -Fx 'Unexpected interpreter in usr/bin/scan-view' negative-raw.txt
printf 'TASK165_NEGATIVE_PASS\n'
exit "$fail"

%install
install -d "%{buildroot}%{_datadir}/%{name}"
printf 'Guard validation ran in the build stage.\n' > "%{buildroot}%{_datadir}/%{name}/verified.txt"
%files
%{_datadir}/%{name}/
