Name:       capi-system-device
Summary:    A Device library in TIZEN C API
Version:    0.1.0
Release:    0
Group:      System/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    capi-system-device.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(tracker)
BuildRequires:  pkgconfig(libsyscommon)
BuildRequires:  pkgconfig(hal-api-common)
BuildRequires:  pkgconfig(hal-api-device)
%if 0%{?gcov:1}
BuildRequires:  lcov
%endif
Requires: %{name}-isu

%description
A Device library in TIZEN C API package.

%package devel
Summary:  A Device library in TIZEN C API (Development)
Group:    System/Development
Requires: %{name} = %{version}-%{release}

%description devel
A Device library in TIZEN C API (Development) package.
%devel_desc

%if 0%{?gcov:1}
%package gcov
Summary:    A Device library in TIZEN C API (gcov)
Group:      System/Libraries

%description gcov
A Device library in TIZEN C API (gcov)
%endif

%isu_package

%prep
%setup -q

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

cp %{SOURCE1} .
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%if "%{?profile}" == "tv"
EXCLUDE_INTERNAL_CAPI_SYSTEM_DEVICE=1
%else
EXCLUDE_INTERNAL_CAPI_SYSTEM_DEVICE=0
%endif

%cmake . -DFULLVER=%{version} \
		 -DMAJORVER=${MAJORVER} \
		 -DEXCLUDE_INTERNAL_CAPI_SYSTEM_DEVICE=${EXCLUDE_INTERNAL_CAPI_SYSTEM_DEVICE}

%__make %{?jobs:-j%jobs}

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
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_libdir}/libcapi-system-device.so.*
/etc/deviced/device/*.conf

%files devel
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_includedir}/device/*.h
%{_includedir}/system/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-system-device.so

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif
