Name:       message-port
Summary:    Message Port library
Version:    1.5.2
Release:    0
Group:      Application Framework/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
Source1002: %{name}-benchmark.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(pkgmgr)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(gmock)

%if 0%{?gcov:1}
BuildRequires:  lcov
%endif

Requires(post): /sbin/ldconfig
Requires(post): coreutils
Requires(postun): /sbin/ldconfig

Provides: capi-message-port
Provides: libcapi-message-port.so.1

%description
Message Port library package.

%package devel
Summary:  Message Port library (Development)
Group:    Application Framework/Development
Requires: %{name} = %{version}-%{release}

%description devel
Message Port library (Development) package.

%if 0%{?gcov:1}
%package gcov
Summary:  Message Port API(gcov)
Group:    Application Framework/Libraries

%description gcov
gcov objects of a message port library
%endif

%package unittests
Summary:    %{name} unittests binary

%description unittests
unittests binary

%package -n %{name}-benchmark
Summary:    Benchmark for message-port API
Group:      Application Framework/Testing
Requires:   %{name}

%description -n %{name}-benchmark
Benchmark for message-port API

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \
  %if 0%{?asan} != 1
    -DASAN_ENABLED=FALSE
  %else
    -DASAN_ENABLED=TRUE
  %endif

# Call make instruction with smp support
%__make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

cat << EOF > run-unittest.sh
#!/bin/sh
setup() {
    echo "setup start"
}

test_main() {
    echo "test_main start"
    /usr/bin/message-port-unit-tests
}

teardown() {
    echo "teardown start"
}

main() {
    setup
    test_main
    teardown
}

main "\$*"
EOF

mkdir -p %{buildroot}%{_bindir}/tizen-unittests/%{name}
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/%{name}/

%check
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%{buildroot}%{_libdir}/
ctest -V

%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%attr(0644,root,root) %{_libdir}/lib%{name}.so.*
%attr(0644,root,root) %{_libdir}/libcapi-message-port.so.*
%config %{_sysconfdir}/dbus-1/session.d/message-port.conf
%license LICENSE.APLv2

%files devel
%{_includedir}/appfw/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib%{name}.so

%files unittests
%attr(0755,root,root) %{_bindir}/message-port-unit-test
%attr(0755,root,root) %{_bindir}/tizen-unittests/%{name}/run-unittest.sh

%files -n %{name}-benchmark
%manifest %{name}-benchmark.manifest
%{_bindir}/%{name}-benchmark

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*

%endif
