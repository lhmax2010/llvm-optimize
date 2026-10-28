%bcond_without lws_static
%bcond_without lws_static_prebuilt
%bcond_without use_glib_event_loop
Name:    capi-network-vine
Summary: An service discovery framework
Version: 1.3.5
Release: 0
Group:   Network & Connectivity/API
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz
Source1: %{name}.manifest

BuildRequires: cmake
BuildRequires: pkgconfig(dns_sd)
%if %{with lws_static}
BuildRequires: pkgconfig(openssl3)
%endif
%if %{without lws_static}
BuildRequires: pkgconfig(libwebsockets)
%endif

%if 0%{?_with_tizen:1}
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(dlog)

%ifnarch %i586 i686 x86_64
BuildRequires: pkgconfig(capi-network-wifi-aware)
%endif
%if "%{mv_prj}" != "1"
BuildRequires: pkgconfig(capi-network-bluetooth)
%endif

%endif

%if %{with use_glib_event_loop}
BuildRequires: pkgconfig(glib-2.0)
%endif

BuildRequires: pkgconfig(gmock)

%if 0%{?gcov:1}
BuildRequires: gtest-devel
BuildRequires: lcov
%endif

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
A Vine library is a Tizen Framework to provide service discovery and connection to communicate between devices in a local network

%package devel
Summary: A Vine library in Native API (Development)
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: capi-base-common-devel

%description devel
A Vine library in Native API (Development)

%package test
Summary: Vine - Test binaries

%description test
Test Application for Vine

%if 0%{?gcov:1}
%package gcov
Summary: Coverage Data of %{name}

%description gcov
The %{name}-gcov package contains gcov objects
%endif

%package unittests
Summary: %{name} unittests binary

%description unittests
unittests binary

%prep
%setup -q
chmod 644 %{SOURCE0}
cp %{SOURCE1} ./%{name}.manifest

%ifarch %{arm}
export ARCH=arm
%else
export ARCH=i586
%endif

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
%endif

%cmake . \
        -DTIZEN_OS=%{?_with_tizen} \
%ifarch armv7hl
        -DHW_FP=ON \
%endif
        -DCMAKE_BUILD_TYPE=%{?build_type} \
        -DCMAKE_VERBOSE_MAKEFILE=ON \
        -DLIB_DIR:PATH=%{_libdir} \
        -DBIN_DIR:PATH=%{_bindir} \
        -DINCLUDE_DIR:PATH=%{_includedir} \
        -DUSE_EVENT_LOOP_EPOLL=ON \
%if %{with use_glib_event_loop}
        -DUSE_EVENT_LOOP_EXTERNAL_GLIB=ON \
%else
        -DUSE_EVENT_LOOP_EXTERNAL_GLIB=OFF \
%endif
%if "%{mv_prj}" == "1"
        -DBT_SUPPORT=OFF \
%endif
%if %{with lws_static}
        -DUSE_LIBWEBSOCKETS_STATIC=ON \
%else
        -DUSE_LIBWEBSOCKETS_STATIC=OFF \
%endif
%ifnarch %i586 i686 x86_64
        -DNAN_SUPPORT=ON \
%endif
%if %{with lws_static_prebuilt}
        -DUSE_LIBWEBSOCKETS_STATIC_PREBUILT=ON \
%else
        -DUSE_LIBWEBSOCKETS_STATIC_PREBUILT=OFF \
%endif
%if 0%{?asan} != 1
        -DWITH_UNITTEST=ON \
%endif
        -DENABLE_DATAPATH_PLUGIN_DEBUG=ON \
        -DWITH_VINE_TEST=ON

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%if %{with lws_static}
rm -rf %{buildroot}%{_libdir}/cmake/libwebsockets
%endif

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' ! -path '*/verifier/*' ! -path '*/vine-test/*' ! -path '*/tool/*' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

cat << EOF > run-unittest.sh
#!/bin/sh
setup() {
    echo "setup start"
}

test_main() {
    echo "test_main start"
    /usr/bin/vine-unittest
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
%if 0%{?gcov:1}
LD_LIBRARY_PATH=%{buildroot}%{_libdir} tests/unittest/vine-unittest
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/*.so*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/vine.pc
%{_includedir}/*.h
%if %{with lws_static} && %{without lws_static_prebuilt}
%{_includedir}/libwebsockets/*.h
%{_includedir}/libwebsockets/abstract/*.h
%{_includedir}/libwebsockets/abstract/protocols/*.h
%{_includedir}/libwebsockets/abstract/transports/*.h
%exclude %{_libdir}/pkgconfig/libwebsockets.pc
%exclude %{_libdir}/pkgconfig/libwebsockets_static.pc
%endif
%{_libdir}/*.so

%files test
%manifest %{name}.manifest
%attr(755,root,root) %{_bindir}/*
%attr(644,root,root) %{_datadir}/vine-verifier/certs/rootCA/ca.pem
%attr(644,root,root) %{_datadir}/vine-verifier/certs/server/*

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif


%if 0%{?asan} != 1
%files unittests
%{_bindir}/vine-unittest
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
%endif
