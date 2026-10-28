Name:		capi-network-tethering
Summary:	Tethering Framework
Version:	1.2.2
Release:	1
Group:		System/Network
License:	Apache-2.0
Source0:	%{name}-%{version}.tar.gz
BuildRequires:	pkgconfig(dlog)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(capi-base-common)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(vconf)
BuildRequires:	pkgconfig(key-manager)
BuildRequires:	pkgconfig(capi-system-info)
BuildRequires:	pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(gmock)
BuildRequires:	cmake
%if 0%{?gcov:1}
BuildRequires: gtest-devel
BuildRequires: lcov
BuildRequires: tar
%endif
Requires(post):		/sbin/ldconfig
Requires(postun):	/sbin/ldconfig

%description
Tethering framework library for CAPI

%package devel
Summary:	Development package for Tethering framework library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%description devel
Development package for Tethering framework library

%package tool
Summary:	Test application for Tethering
%description tool
Test application for Tethering

%package test_application
Summary:	Test application for Tethering Ext
%description test_application
Test application for Tethering Ext

%if 0%{?gcov:1}
%package gcov
Summary:  Tethering Library(gcov)
Group:    Network/Testing
%description gcov
gcov objects for coverage test
%endif

%if 0%{?asan} != 1
%package unittests
Summary: %{name} unittests binary

%description unittests
unittests binary
%endif

%prep
%setup -q


%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
%endif

%if "%{?tizen_profile_name}" == "tv"
export CFLAGS+=" -DTIZEN_TV_EXT"
export CXXFLAGS+=" -DTIZEN_TV_EXT"
%endif

%cmake -DLIB_INSTALL_DIR=%{_libdir} \
       -DBUILD_UNITTEST=%{?asan:0}%{!?asan:1} \
	.
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' ! -path '*/tools/*' -exec cp --parents '{}' "$gcno_obj_dir" ';'
find . -name '*.gcno' ! -path '*/test_application/*' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

%if 0%{?asan} != 1
cat << EOF > run-unittest.sh
#!/bin/sh
setup() {
    echo "setup start"
}

test_main() {
    echo "test_main start"
    /usr/bin/tethering-gtest
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

%check
%if 0%{?gcov:1}
tests/tethering-gtest
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest capi-network-tethering.manifest
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%license LICENSE

%files devel
%defattr(-,root,root,-)
%{_includedir}/network/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%license LICENSE

%files tool
%{_bindir}/tethering_test

%files test_application
%{_bindir}/tethering_ext_test

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

%if 0%{?asan} != 1
%files unittests
%{_bindir}/tethering-gtest
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
%endif
