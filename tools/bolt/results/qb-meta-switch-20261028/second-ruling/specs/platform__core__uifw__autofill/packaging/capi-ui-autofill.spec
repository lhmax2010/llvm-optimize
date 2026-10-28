Name:       capi-ui-autofill
Summary:    Autofill Library
Version:    0.11.2
Release:    1
Group:      Graphics & UI Framework/Input
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  tidl
BuildRequires:  gawk
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-appfw-service-application)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(rpc-port)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-session)
BuildRequires:  pkgconfig(cynara-creds-self)
BuildRequires:  pkgconfig(capi-appfw-app-manager)
BuildRequires:  pkgconfig(gmock)

Requires: org.tizen.autofilld
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
Autofill Library


%package devel
Summary:  Autofill Library (Development)
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Autofill Library (Development)

%if 0%{?gcov:1}
%package gcov
Summary:  Autofill Library (gcov)
Group:      Graphics & UI Framework/Input
%description gcov
Autofill gcov objects
%endif

%package -n capi-ui-autofill-common
Summary:  Autofill Common Library
Group:    Graphics & UI Framework/Input
Requires: %{name} = %{version}-%{release}

%description -n capi-ui-autofill-common
Autofill Common Library

%package -n capi-ui-autofill-common-devel
Summary:  Autofill Common Library (Development)
Group:    Graphics & UI Framework/Input
Requires: %{name} = %{version}-%{release}

%description -n capi-ui-autofill-common-devel
Autofill Common Library (Development)

%package -n capi-ui-autofill-service
Summary:  Autofill Service Library
Group:    Graphics & UI Framework/Input
Requires: %{name} = %{version}-%{release}

%description -n capi-ui-autofill-service
Autofill Service Library

%package -n capi-ui-autofill-service-devel
Summary:  Autofill Service Library (Development)
Group:    Graphics & UI Framework/Input
Requires: %{name} = %{version}-%{release}

%description -n capi-ui-autofill-service-devel
Autofill Service Library (Development)

%package -n capi-ui-autofill-manager
Summary:  Autofill Manager Library
Group:    Graphics & UI Framework/Input
Requires: %{name} = %{version}-%{release}

%description -n capi-ui-autofill-manager
Autofill Manager Library

%package unittests
Summary:    autofill tests
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description unittests
GTest for autofill


%package -n capi-ui-autofill-manager-devel
Summary:  Autofill Manager Library (Development)
Group:    Graphics & UI Framework/Input
Requires: %{name} = %{version}-%{release}

%description -n capi-ui-autofill-manager-devel
Autofill Manager Library (Development)

%prep
%setup -q

tidlc -p -l C -i tidl/autofill.tidl -o autofill_proxy
mv autofill_proxy.h ./client/
mv autofill_proxy.c ./client/

tidlc -s -l C -i tidl/autofill_service.tidl -o autofill_service_stub
mv autofill_service_stub.h ./service_lib/
mv autofill_service_stub.c ./service_lib/

tidlc -p -l C -i tidl/autofill_manager.tidl -o autofill_manager_proxy
mv autofill_manager_proxy.h ./manager/
mv autofill_manager_proxy.c ./manager/

%build
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export FFLAGS="$FFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE -fvisibility=hidden -Werror"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE -fvisibility=hidden -Werror"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE -fvisibility=hidden"

rm -rf CMakeFiles
rm -rf CMakeCache.txt
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DLIBDIR=%{_libdir} -DTEST_TYPE=%{test_type}
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%if 0%{?gcov:1}
find . -name '*_proxy.c.gcno' -exec rm {} \;
find . -name '*_stub.c.gcno' -exec rm {} \;

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
	/usr/bin/capi-ui-autofill-unittests
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
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/%{name}

%check
%if 0%{?gcov:1}
%if 0%{?run_unittest:1}
ctest --output-on-failure %{?_smp_mflags}
lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d . -o %{name}.info
genhtml %{name}.info -o %{name}.out
zip -r %{name}.zip %{name}.out %{name}.info
install -m 0644 %{name}.zip %{buildroot}%{_datadir}/gcov/
%endif
%endif

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest client/capi-ui-autofill.manifest
%{_libdir}/libcapi-ui-autofill.so.*
%{_libdir}/libcapi-ui-autofill.so
%{_libdir}/libcapi-ui-autofill-common.so.*
%{_libdir}/libcapi-ui-autofill-common.so
%{_libdir}/libcapi-ui-autofill-service.so.*
%{_libdir}/libcapi-ui-autofill-service.so
%{_libdir}/libcapi-ui-autofill-manager.so.*
%{_libdir}/libcapi-ui-autofill-manager.so
%license LICENSE

%files -n capi-ui-autofill-common
%manifest common/capi-ui-autofill-common.manifest
%license LICENSE

%files -n capi-ui-autofill-common-devel
%{_includedir}/autofill_common*.h
%{_includedir}/autofill_error.h
%{_libdir}/pkgconfig/capi-ui-autofill-common.pc

%files devel
%{_includedir}/autofill.h
%{_libdir}/pkgconfig/capi-ui-autofill.pc

%files -n capi-ui-autofill-service
%manifest service_lib/capi-ui-autofill-service.manifest
%license LICENSE

%files -n capi-ui-autofill-service-devel
%{_includedir}/autofill_service*.h
%{_libdir}/pkgconfig/capi-ui-autofill-service.pc

%files -n capi-ui-autofill-manager
%manifest manager/capi-ui-autofill-manager.manifest
%license LICENSE

%files -n capi-ui-autofill-manager-devel
%{_includedir}/autofill_error.h
%{_includedir}/autofill_manager*.h
%{_libdir}/pkgconfig/capi-ui-autofill-manager.pc

%files unittests
%{_bindir}/capi-ui-autofill-unittests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif
