Name:       capi-system-sensor
Summary:    A Sensor library in TIZEN C API
Version:    0.2.5
Release:    1
Group:      System/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

%if "%{?profile}" != "tv" && "%{mv_prj}" != "1"
%define SENSOR_RECORDER on
%else
%define SENSOR_RECORDER off
%endif

BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(sensor)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(hal-api-sensor)
%if "%{?SENSOR_RECORDER}" == "on"
BuildRequires:  pkgconfig(context-sensor-recorder-client)
%endif
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: %{name}-isu

Provides: %{name}-profile_common = %{version}-%{release}
Provides: %{name}-profile_mobile = %{version}-%{release}
Provides: %{name}-profile_wearable = %{version}-%{release}
Provides: %{name}-profile_tv = %{version}-%{release}
Provides: %{name}-profile_ivi = %{version}-%{release}

%description
A Sensor Library in TIZEN C API package.

%package devel
Summary:  A Sensor library in TIZEN C API (Development)
Group:    System/Development
Requires: %{name} = %{version}-%{release}

%description devel
A Sensor library in TIZEN C API package (Development).
%devel_desc

%package test
Summary:    Tizen Sensor Test Programs (test)
Group:      System & System Tools/Testing
Requires:   %{name} = %{version}-%{release}

%description test
Tizen Sensor Test Programs (test)

%package tools
Summary:  Sensor command line tool package
Group:    System & System Tools
Requires: %{name} = %{version}-%{release}

%description tools
Sensor command line tools

%if 0%{?gcov:1}
%package gcov
Summary:    Tizen Sensor Library API (gcov)
Group:      Service Framework/Testing

%description gcov
gcov objects for coverage test
%endif

%isu_package

%prep
%setup -q

%build
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DSENSOR_RECORDER=%{SENSOR_RECORDER}
%__make %{?_smp_mflags}

%install
%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest packaging/capi-system-sensor.manifest
%{_libdir}/libcapi-system-sensor.so.*
%license LICENSE.APLv2

%files devel
%manifest packaging/capi-system-sensor.manifest
%{_libdir}/pkgconfig/*.pc
%{_includedir}/sensor/*.h
%{_libdir}/libcapi-system-sensor.so

%files test
%manifest packaging/capi-system-sensor.manifest
%defattr(-,root,root,-)
%{_bindir}/sensor-test

%files tools
%{_bindir}/sensor-tool

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
