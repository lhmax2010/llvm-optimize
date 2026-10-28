Name:       pkgmgr-info
Summary:    Packager Manager infomation api for package
Version:    0.37.5
Release:    1
Group:      Application Framework/Package Management
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.service
Source2:    %{name}.socket
Source1001: pkgmgr-info.manifest
BuildRequires: cmake
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(capi-system-resource)
BuildRequires: pkgconfig(cynara-client-async)
BuildRequires: pkgconfig(cynara-creds-socket)
BuildRequires: pkgconfig(cynara-session)
BuildRequires: pkgconfig(cynara-uid)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gmock)
BuildRequires: pkgconfig(libcap)
%if "%{?dev_wos}" != "1"
BuildRequires: pkgconfig(libsmack)
%endif
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(minizip)
BuildRequires: pkgconfig(parcel)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(tizen-database)
BuildRequires: pkgconfig(tizen-libopener)
BuildRequires: pkgconfig(vconf)

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
Packager Manager infomation api for packaging

%package devel
Summary:    Packager Manager infomation api (devel)
Requires:   %{name} = %{version}-%{release}
%description devel
Packager Manager infomation api (devel)

%package parser
Summary:    Library for manifest parser
Requires:   %{name} = %{version}-%{release}

%description parser
Library for manifest parser

%package parser-devel
Summary:    Dev package for libpkgmgr-parser
Requires:   %{name}-parser = %{version}-%{release}
Requires:	pkgconfig(libtzplatform-config)

%description parser-devel
Dev package for libpkgmgr-parser

%package common
Summary:    Library for pkgmgr-info-server
Requires:   %{name} = %{version}-%{release}
Requires:   pkgconfig(libsystemd)

%description common
Library for pkgmgr-info-server

%package common-devel
Summary:    Dev package for libpkgmgr_common
Requires:   %{name}-common = %{version}-%{release}

%description common-devel
Dev package for libpkgmgr_common

%if 0%{?asan} != 1
%package unittests
Summary:    %{name} unittests binary

%description unittests
unittest binary
%endif

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
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DUNITDIR=%{_unitdir} \
    -DTIZEN_FEATURE_SMACK_DISABLE:BOOL=%{?dev_wos:ON}%{!?dev_wos:OFF} \
%if 0%{?asan} != 1
	-DASAN_ENABLED=FALSE
%else
	-DASAN_ENABLED=TRUE
%endif

%__make %{?jobs:-j%jobs}

%check
export LD_LIBRARY_PATH=../../src/:../../src/server:../../parser
ctest -V
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%install
%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

%if 0%{?asan} != 1
cat << EOF > run-unittest.sh
#!/bin/sh

setup() {
    echo "setup start"
}

test_main() {
    echo "test_main start"
    /usr/bin/pkgmgr-info-unit-test
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
%endif

mkdir -p %{buildroot}%{_unitdir}/basic.target.wants
ln -sf ../pkg-db-recovery.service %{buildroot}%{_unitdir}/basic.target.wants/pkg-db-recovery.service

mkdir -p %{buildroot}%{_unitdir}/basic.target.wants
mkdir -p %{buildroot}%{_unitdir}/sockets.target.wants
install -m 0644 %SOURCE1 %{buildroot}%{_unitdir}/%{name}.service
install -m 0644 %SOURCE2 %{buildroot}%{_unitdir}/%{name}.socket
ln -s ../%{name}.service %{buildroot}%{_unitdir}/basic.target.wants/%{name}.service
ln -sf ../%{name}.socket %{buildroot}%{_unitdir}/sockets.target.wants/%{name}.socket

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n pkgmgr-info-parser -p /sbin/ldconfig

%postun  -n pkgmgr-info-parser -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/libpkgmgr-info.so.*
%{_libdir}/libpkgmgr-info-server.so.*
%{_bindir}/pkg-db-recovery
%{_bindir}/pkg-db-creator
%{_bindir}/pkginfo-server
%{_unitdir}/pkg-db-recovery.service
%{_unitdir}/basic.target.wants/pkg-db-recovery.service
%{_includedir}/pkgmgr-client/*.hh
%{_unitdir}/%{name}.service
%{_unitdir}/basic.target.wants/%{name}.service
%{_unitdir}/%{name}.socket
%{_unitdir}/sockets.target.wants/%{name}.socket

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/pkgconfig/pkgmgr-info.pc
%{_libdir}/pkgconfig/pkgmgr-info-server.pc
%{_libdir}/libpkgmgr-info.so
%{_libdir}/libpkgmgr-info-server.so
%{_includedir}/pkgmgr-client/*.hh
%{_includedir}/pkgmgr-common/*.hh
%{_includedir}/pkgmgr-server/*.h

%files parser
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/libpkgmgr_parser.so.*
%config %{_sysconfdir}/package-manager/preload/manifest.xsd
%config %{_sysconfdir}/package-manager/preload/xml.xsd
%config %{_sysconfdir}/package-manager/parserlib/metadata/mdparser_list.txt
%config %{_sysconfdir}/package-manager/parserlib/category/category_parser_list.txt
%config %{_sysconfdir}/package-manager/parserlib/tag_parser_list.txt
%config %{_sysconfdir}/package-manager/pkg_db_version.txt

%files parser-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/pkgmgr/*.h
%{_libdir}/pkgconfig/pkgmgr-parser.pc
%{_libdir}/libpkgmgr_parser.so

#################################################
# pkgmgr-info-gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:    Packager Manager information api (gcov)
Group:      Application Framework/Testing

%description gcov
Packager Manager information api gcov objects
%endif

%if 0%{?gcov:1}
%files gcov
%defattr(-,root,root,-)
%{_datadir}/gcov/obj/*
%endif

%if 0%{?asan} != 1
%files unittests
%{_bindir}/pkgmgr-info-unit-test
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
%endif
