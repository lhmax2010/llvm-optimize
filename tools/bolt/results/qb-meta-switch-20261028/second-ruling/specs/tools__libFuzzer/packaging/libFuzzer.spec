Name:           libFuzzer
Version:        5.0
Release:        0
License:        University of Illinois/NCSA Open Source License
Summary:        libFuzzer
Url:            http://llvm.org/docs/LibFuzzer.html
Group:          Development/Testing
Source0:        %{name}-%{version}.tar.xz

# disable debuginfo stripping
%define __strip /bin/true

%description
LibFuzzer is in-process, coverage-guided, evolutionary fuzzing engine.

%prep
%setup -q

%build
cd lib/Fuzzer
CXX=gcc ./build.sh

%install
mkdir -p %{buildroot}%{_libdir}
cp lib/Fuzzer/libFuzzer.a %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_prefix}/bin
cp scripts/sancov.py %{buildroot}%{_prefix}/bin
cp scripts/sancov_symbolize.py %{buildroot}%{_prefix}/bin
cp scripts/coverage-report-dump.py %{buildroot}%{_prefix}/bin
cp scripts/merge_symcov.py %{buildroot}%{_prefix}/bin

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE.TXT
%{_libdir}/libFuzzer.a

%package -n fuzz-asan-force-options
Summary:    Scripts to enable automatic package sanitization with ASan for fuzzing
Group:      System Environment
# Need to have gcc installed before running the force-options script
Requires:   asan-force-options

%description -n fuzz-asan-force-options
Compiler wrappers for ASan and SanCov instrumentation needed for fuzzing.

%post -n fuzz-asan-force-options
/usr/bin/gcc-unforce-options
/usr/bin/gcc-force-options -fsanitize-coverage=trace-pc -fsanitize=address -fsanitize-recover=address -fno-common -fno-omit-frame-pointer -U_FORTIFY_SOURCE -pthread -lm -ldl

%preun -n fuzz-asan-force-options
/usr/bin/gcc-unforce-options
chmod a-w /usr/bin

%files -n fuzz-asan-force-options
# no files

%package -n fuzz-ubsan-force-options
Summary:    Scripts to enable automatic package sanitization with UBSan for fuzzing
Group:      System Environment
# Need to have gcc installed before running the force-options script
Requires:   ubsan-force-options

%description -n fuzz-ubsan-force-options
Compiler wrappers for UBSan and SanCov instrumentation needed for fuzzing.

%post -n fuzz-ubsan-force-options
/usr/bin/gcc-unforce-options
/usr/bin/gcc-force-options -fsanitize-coverage=trace-pc -fsanitize=undefined,bounds-strict,float-divide-by-zero,float-cast-overflow -fno-common -fno-omit-frame-pointer -U_FORTIFY_SOURCE -pthread -lm -ldl

%preun -n fuzz-ubsan-force-options
/usr/bin/gcc-unforce-options
chmod a-w /usr/bin

%files -n fuzz-ubsan-force-options
# no files

%package -n sancov
Summary:    Scripts to process coverage information
Group:      System Environment
Requires:   python binutils

%description -n sancov
Scripts to process coverage information collected with SanitizerCoverage

%files -n sancov
%manifest sancov.manifest
%license LICENSE.TXT
%{_prefix}/bin/sancov.py
%{_prefix}/bin/sancov_symbolize.py
%{_prefix}/bin/coverage-report-dump.py
%{_prefix}/bin/merge_symcov.py
