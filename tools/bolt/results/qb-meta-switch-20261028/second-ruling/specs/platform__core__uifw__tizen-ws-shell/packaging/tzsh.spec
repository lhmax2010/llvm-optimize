%bcond_with wayland
%bcond_with x

# BUILD_TCORE_ENABLE: 0 (default) = EFL + TCORE backends, 1 = TCORE only (no EFL).
# Example: gbs build ... --define "BUILD_TCORE_ENABLE 1"
%{!?BUILD_TCORE_ENABLE:%global BUILD_TCORE_ENABLE 0}
%if "%{BUILD_TCORE_ENABLE}" != "0" && "%{BUILD_TCORE_ENABLE}" != "1"
%{error:BUILD_TCORE_ENABLE must be 0 or 1}
%endif

# toolkit backends (always built, dlopen()ed by tzsh_create() according to toolkit type)
#   efl   : libtzsh_backend_efl.so   (ecore, ecore-wl2)
#   tcore : libtzsh_backend_tcore.so (tizen-core, tizen-core-wl)

# to build examples
%define with_tests 0

Name:           tzsh
Version:        1.6.1
Release:        0
Summary:        Tizen Window System Shell
License:        MIT
Group:          Graphics & UI Framework/Wayland Window System
Url:            http://www.samsung.com
Source0:        %name-%version.tar.gz
Source1001:     %name.manifest
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(tizen-extension-client)
%if "%{BUILD_TCORE_ENABLE}" != "1"
BuildRequires:  pkgconfig(ecore)
BuildRequires:  pkgconfig(ecore-wl2)
# to include backend packages
Requires:       tzsh-backend-efl
%endif
BuildRequires:  pkgconfig(tizen-core)
BuildRequires:  pkgconfig(tizen-core-wl)
# to include backend packages
Requires:       tzsh-backend-tcore

%description
Description: %{summary}

%package devel
Summary: Development files for package %{name}
Group:   Graphics & UI Framework/Development
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig(capi-base-common)

%description devel
This package provides header files and other developer releated files
for package %{name}.

%if "%{BUILD_TCORE_ENABLE}" != "1"
%package backend-efl
Summary:  EFL backend for tzsh package
Group:    Graphics & UI Framework/Wayland Window System
Requires: %{name} = %{version}-%{release}

%description backend-efl
EFL backend plugin for tzsh
%endif

%package backend-tcore
Summary:  TCore backend for tzsh package
Group:    Graphics & UI Framework/Wayland Window System
Requires: %{name} = %{version}-%{release}

%description backend-tcore
TCore backend plugin for tzsh

%if "%{BUILD_TCORE_ENABLE}" != "1"
%package examples-efl
Summary:  EFL examples for the tzsh package
Group:    Graphics & UI Framework/Testing
Requires: %{name} = %{version}-%{release}
Requires: %{name}-backend-efl = %{version}-%{release}
BuildRequires: pkgconfig(evas)
BuildRequires: pkgconfig(elementary)
BuildRequires: pkgconfig(tizen-remote-surface-client)

%description examples-efl
EFL Example files for the tzsh
%endif

%package examples-tcore
Summary:  TCore examples for the tzsh package
Group:    Graphics & UI Framework/Testing
Requires: %{name} = %{version}-%{release}
Requires: %{name}-backend-tcore = %{version}-%{release}
BuildRequires:  pkgconfig(tizen-core)
BuildRequires:  pkgconfig(tizen-core-wl)

%description examples-tcore
TCore Example files for the tzsh

%package -n tzsh-extension-devel
Group:		Graphics & UI Framework/Wayland Window System
Summary:	Development files for package tzsh-extension
Requires:		%{name}-devel

%description -n tzsh-extension-devel
Tizen-Shell extesion support more APIs for extend specific modules.

%if 0%{?gcov:1}
%package gcov
Summary: tzsh-quickpanel gcov data package
Group: Graphics & UI Framework/Testing

%description gcov
tzsh-quickpanel gcno data for gcov
%endif

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="$CFLAGS -DEFL_BETA_API_SUPPORT "
export CFLAGS="$CFLAGS -fvisibility=hidden -fPIC -Werror-implicit-function-declaration "
export LDFLAGS="$LDFLAGS -fvisibility=hidden -Wl,--hash-style=both -Wl,--as-needed"
%if 0%{?gcov:1}
CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
LDFLAGS="$LDFLAGS -lgcov"
%endif

%if "%{BUILD_TCORE_ENABLE}" == "1"
   %autogen --enable-tcore --enable-build-examples
%else
%if "%{with_tests}" == "1"
   %autogen --enable-build-examples --with-tests=regular
%else
   %autogen --enable-build-examples
%endif
%endif
make %{?jobs:-j%jobs}

%install
%if "%{with_tests}" == "1"
make check
%make_install
%else
%make_install
%endif

%if 0%{?gcov:1}
#builddir=$(basename $PWD)
#gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/src/lib/quickpanel/.libs/
mkdir -p "$gcno_obj_dir"
#find src/lib/quickpanel/.libs/ -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
cp src/lib/quickpanel/.libs/libtzsh_quickpanel_la-tzsh_quickpanel.gcno "$gcno_obj_dir"
cp src/lib/quickpanel/.libs/libtzsh_quickpanel_service_la-tzsh_quickpanel_service.gcno "$gcno_obj_dir"
%endif

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{_libdir}/*.so.*

%files devel
%manifest %{name}.manifest
%{_libdir}/*.so
%exclude %{_libdir}/libtzsh_backend_tcore.so
%if "%{BUILD_TCORE_ENABLE}" != "1"
%exclude %{_libdir}/libtzsh_backend_efl.so
%endif
%{_libdir}/pkgconfig/*.pc
%{_includedir}/%{name}/*
%exclude %{_includedir}/%{name}/tzsh_protocol.h
%exclude %{_includedir}/%{name}/tzsh_extension.h

%if "%{BUILD_TCORE_ENABLE}" != "1"
%files backend-efl
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/libtzsh_backend_efl.so
%endif

%files backend-tcore
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/libtzsh_backend_tcore.so

%if "%{BUILD_TCORE_ENABLE}" != "1"
%files examples-efl
%manifest %{name}.manifest
%defattr(-,root,root)
%{_bindir}/*
%exclude %{_bindir}/kvm-service-tcore
%endif

%files examples-tcore
%manifest %{name}.manifest
%defattr(-,root,root)
%{_bindir}/kvm-service-tcore

%files -n tzsh-extension-devel
%manifest %{name}.manifest
%{_includedir}/%{name}/tzsh_protocol.h
%{_includedir}/%{name}/tzsh_extension.h

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
