Name:       minicontrol
Summary:    Library packaes for minicontrol
Version:    0.2.2
Release:    1
Group:      Application Framework/Other
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(elementary)
BuildRequires: pkgconfig(evas)
BuildRequires: pkgconfig(ecore-evas)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(gmock)
BuildRequires: cmake
Requires(post): /sbin/ldconfig
requires(postun): /sbin/ldconfig

%if 0%{?gcov:1}
BuildRequires: lcov
BuildRequires: zip
%endif

%description
Minicontrol is a small control panel on notification panel or lock screen. This package supports to develop minicontrols.

%prep
%setup -q

%package devel
Summary:    Minicontrol library (devel)
Group:      Development/Libraries
Requires:   %{name} = %{version}

%description devel
Minicontrol library (devel).

%package unittests
Summary:    %{name} unittests binary

%description unittests
unittests binary

%if 0%{?gcov:1}
%package gcov
Summary:  Minicontrol Library(gcov)
Group:    Application Framework/Other

%description gcov
gcov objects of Minicontrol Library
%endif

%build
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export FFLAGS="$FFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

export LDFLAGS="$LDFLAGS -Wl,--rpath=%{_prefix}/lib -Wl,--as-needed"
LDFLAGS="$LDFLAGS"

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%if %{with wayland}
%cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DHAVE_WAYLAND=On -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DBIN_INSTALL_DIR:PATH=%{_bindir}
%else
%cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DHAVE_X11=On -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DBIN_INSTALL_DIR:PATH=%{_bindir}
%endif
make %{?jobs:-j%jobs}

%install
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
    /usr/bin/minicontrol-unittest
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
(cd unittests && LD_LIBRARY_PATH=../ ctest -V)
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused,inconsistent --no-external -q -d . -o minicontrol.info
genhtml minicontrol.info -o minicontrol.out
zip -r minicontrol.zip minicontrol.out
install -m 0644 minicontrol.zip %{buildroot}%{_datadir}/gcov/obj/
%endif

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest minicontrol.manifest
%defattr(-,root,root,-)
%{_libdir}/libminicontrol-provider.so.*
%{_libdir}/libminicontrol-viewer.so.*
%{_libdir}/libminicontrol-monitor.so.*
%license LICENSE

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/*.h
%{_libdir}/pkgconfig/minicontrol-provider.pc
%{_libdir}/pkgconfig/minicontrol-monitor.pc
%{_libdir}/pkgconfig/minicontrol-viewer.pc
%{_libdir}/libminicontrol-provider.so
%{_libdir}/libminicontrol-viewer.so
%{_libdir}/libminicontrol-monitor.so

%files unittests
%{_bindir}/minicontrol-unittest
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
