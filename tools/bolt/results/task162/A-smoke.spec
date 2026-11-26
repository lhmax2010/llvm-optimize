Name:       llvm-analyzer-smoke
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
    printf 'TASK162_CHECK %s %s rc=%s\n' "$1" "$2" "$3"
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
        printf 'TASK162_REPORT %s\n' "$index"
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
for tool in analyze-build intercept-build scan-build-py scan-view; do
    printf 'TASK162_HELP_BEGIN %s\n' "$tool"
    rc=0
    LC_ALL=C "$tool" --help || rc=$?
    printf 'TASK162_HELP_END %s\n' "$tool"
    if test "$rc" = 0; then
        emit "$tool" PASS "$rc"
    else
        emit "$tool" FAIL "$rc"
        fail=1
    fi
done
exit "$fail"

%install
install -d "%{buildroot}%{_datadir}/%{name}"
cp -a report "%{buildroot}%{_datadir}/%{name}/"

%files
%{_datadir}/%{name}/
