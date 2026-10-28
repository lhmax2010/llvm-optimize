%define on_off() %{expand:%%{?with_%{1}:ON}%%{!?with_%{1}:OFF}}

%if "%{?profile}" == "tv" || "%{?asan}" == "1"
%undefine _with_tests
%else
%define _with_tests on
%endif

%bcond_with tests

Name:       dumpsys
Summary:    Dumpsys is a framework to get logs from services and applications.
Version:    2.0.16
Release:    1
Group:      Framework/system
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001:    dumpsys.manifest
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  cmake
%if %{with tests}
BuildRequires:  cmocka-devel cmocka
BuildRequires:  lcov
%if %{defined _toolchain}
%if %{toolchain_is clang}
BuildRequires:  compiler-rt
%endif
%endif
%endif
Requires:       dumpsys-common

%description
This package provides dumpsys utility and libraries to allow collecting logs from services and applications.

%package -n dumpsys-common
Summary: DBus policy config files
%description -n dumpsys-common
This package provides DBus configuration files needed by API clients to be able to register their dumpsys providers.

%package -n dumpsys-tools
Summary: dumpsys command line utilies
Requires: dumpsys
%description -n dumpsys-tools
This package provides library and header files.

%package -n dumpsys-devel
Summary: dumpsys development package.
Requires: dumpsys
%description -n dumpsys-devel
This package provides library and header files.

%package -n libdumpsys-system
Summary: Package with dumpsys API library for services.
Requires: dumpsys-common
%description -n libdumpsys-system
This package provides dumpsys API library for services.

%package -n libdumpsys-system-devel
Requires: libdumpsys-system
Summary: libdumpsys-system development package.
%description -n libdumpsys-system-devel
This package provides library and header files.

%package -n libdumpsys-user
Summary: Package with dumpsys API library for services.
Requires: dumpsys-common
BuildRequires: pkgconfig(pkgmgr-info)
%description -n libdumpsys-user
This package provides dumpsys API library for services.

%package -n libdumpsys-user-devel
Requires: libdumpsys-user
Summary: libdumpsys-user development package.
%description -n libdumpsys-user-devel
This package provides library and header files.

%if %{with tests}
%package tests
Summary: Contains scripts for testing dumpsys
%description tests
%endif

%prep
%setup -q

%build
cp %{SOURCE1001} .
export CFLAGS+=" -Werror -fvisibility=hidden"

%cmake . \
    -DVERSION=%{version} \
    -DTESTS=%{on_off tests} \
    -DDUMPSYS_SYSTEM_TESTS_PATH=%{_libdir}/dumpsys_system_tests/ \
    -DDUMPSYS_TESTS_PATH=%{_libdir}/dumpsys_unit_tests/

make %{?jobs:-j%jobs}

%if %{with tests}
test_tool=coverage
    %if %{defined _toolchain}
        %if %{toolchain_is clang}
            test_tool=test
        %endif
    %endif
make $test_tool
%endif

%install
rm -rf %{buildroot}
%make_install

%files
%license LICENSE
%manifest %{name}.manifest
%defattr(0755,root,root)
%{_libdir}/libdumpsys.so.*
%{_libexecdir}/dumpsys-service

%defattr(0644,root,root)
%{_unitdir}/dumpsys-service.service
%{_prefix}/lib/tmpfiles.d/dumpsys-run.conf
%{_prefix}/share/dbus-1/system-services/org.tizen.dumpsys.service.service

%files -n dumpsys-tools
%license LICENSE
%manifest %{name}.manifest
%defattr(0755,root,root)
%{_bindir}/dumpsys

%files -n dumpsys-common
%manifest %{name}.manifest
%defattr(0644,root,root)
%{_sysconfdir}/dbus-1/system.d/dumpsys-service.conf

%files -n dumpsys-devel
%manifest %{name}.manifest
%{_includedir}/libdumpsys.h
%{_libdir}/libdumpsys.so
%{_libdir}/pkgconfig/dumpsys.pc

%files -n libdumpsys-system
%manifest %{name}.manifest
%{_libdir}/libdumpsys-system.so.*

%files -n libdumpsys-system-devel
%manifest %{name}.manifest
%{_includedir}/dumpsys-system.h
%{_libdir}/libdumpsys-system.so
%{_libdir}/pkgconfig/dumpsys-system.pc

%files -n libdumpsys-user
%manifest %{name}.manifest
%{_libdir}/libdumpsys-user.so.*

%files -n libdumpsys-user-devel
%manifest %{name}.manifest
%{_includedir}/dumpsys-user.h
%{_libdir}/libdumpsys-user.so
%{_libdir}/pkgconfig/dumpsys-user.pc

%if %{with tests}
%files tests
%manifest %{name}.manifest
%defattr(0755,root,root)
%{_libdir}/dumpsys_system_tests/utils/dumpsys-utils.sh
%{_libdir}/dumpsys_system_tests/utils/test-app
%{_libdir}/dumpsys_system_tests/run.sh
%{_libdir}/dumpsys_system_tests/dumpsys_system/dumpsys_system.sh
%{_libdir}/dumpsys_system_tests/dumpsys_notfound/dumpsys_notfound.sh
%{_libdir}/dumpsys_unit_tests/test_libdumpsys
%{_libdir}/dumpsys_unit_tests/test_dumpsys_service
%{_libdir}/dumpsys_unit_tests/test_dumpsys_client_user_api
%{_libdir}/dumpsys_unit_tests/test_dumpsys_client_system_api
%endif
