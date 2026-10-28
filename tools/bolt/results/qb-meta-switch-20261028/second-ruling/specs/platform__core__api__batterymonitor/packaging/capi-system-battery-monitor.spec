Name:    capi-system-battery-monitor
Summary: Battery Monitor Framework CAPI
Version: 0.1
Release: 1
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(capi-appfw-app-manager)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(aul)

%if 0%{?gcov:1}
BuildRequires:  lcov
%endif

%define BATTERY_MONITOR_LIBDIR %{TZ_SYS_GLOBALUSER_DATA}/battery-monitor

%description

%package devel
Summary: Battery Monitor Framework CAPI (Development)
Requires: %{name} = %{version}

%description devel
%devel_desc

%package test
Summary: Battery Monitor Framework test application
Requires: %{name} = %{version}-%{release}

%description test
This package is for Battery Monitor Framework CAPI test application

%if 0%{?gcov:1}
%package gcov
Summary:    Battery Monitor Library (gcov)
Group:      Service Framework/Testing
%description gcov
gcov objects for coverage test
%endif

%prep
%setup -q

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DBIN_INSTALL_DIR=%{_bindir} \
	-DINCLUDE_INSTALL_DIR=%{_includedir} \
	-DLIB_PATH=%{_lib} \
	-DFULLVER=%{version} \
	-DMAJORVER=${MAJORVER}

make %{?jobs:-j%jobs}
%if 0%{?gcov:1}
mkdir -p gcov-obj
find . -name '*.gcno' -exec cp '{}' gcov-obj ';'
%endif

%install
%make_install

%if 0%{?gcov:1}
mkdir -p %{buildroot}%{_datadir}/gcov/obj
install -m 0644 gcov-obj/* %{buildroot}%{_datadir}/gcov/obj
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE
%attr(644,-,-) %{_libdir}/lib%{name}.so.*

%files devel
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/system/*.h

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

%files test
%manifest %{name}.manifest
%attr(777, service_fw, service_fw) %{_bindir}/bm-test
