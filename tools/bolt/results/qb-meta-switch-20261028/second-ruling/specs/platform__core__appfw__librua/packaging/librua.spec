Name:           librua
Version:        0.5.17
Release:        0
License:        Apache-2.0
Summary:        Recently used application
Group:          Application Framework/Libraries
Source0:        librua-%{version}.tar.gz
Source1001:     librua.manifest
BuildRequires:  cmake
BuildRequires:  sqlite3
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(capi-appfw-app-control)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(libtzplatform-config)

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
Recently used application library

%package devel
Summary:        Recently used application (devel)
Requires:       %{name} = %{version}

%description devel
Recently used application library (devel)

%package unittests
Summary:        Recently used application (test)
Requires:       %{name} = %{version}

%description unittests
Recently used application library (test)

%prep
%setup -q
cp %{SOURCE1001} .

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake -DFULLVER=%{version} \
	-DMAJORVER=${MAJORVER} \
	.

make %{?_smp_mflags}

%check
(cd tests && cd unittest && LD_LIBRARY_PATH=../../ ctest -V)
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d . -o rua.info
genhtml rua.info -o rua.out
zip -r rua.zip rua.out
install -m 0644 rua.zip %{buildroot}%{_datadir}/gcov/
%endif

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
    /usr/bin/rua-test
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

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/librua.so.*
%license LICENSE

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%dir %{_includedir}/rua
%{_includedir}/rua/*.h
%{_libdir}/librua.so
%{_libdir}/pkgconfig/rua.pc

%files unittests
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bindir}/rua-test
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

#################################################
# rua-gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:    Simple string key-val dictionary ADT (gcov)
Group:      Application Framework/Testing

%description gcov
Simple string key-val dictionary ADT gcov objects
%endif

%if 0%{?gcov:1}
%files gcov
%defattr(-,root,root,-)
%{_datadir}/gcov/*
%endif
