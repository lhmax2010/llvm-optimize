
Name:       capi-ui-efl-util
Summary:    An EFL utility library in Tizen C API
Version:    0.9.1
Release:    1
Group:      Graphics & UI Framework/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: 	capi-ui-efl-util.manifest
Source1002: 	run-unittest.sh
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-tbm-client)
BuildRequires:  pkgconfig(screenshooter-client)
BuildRequires:  pkgconfig(tizen-extension-client)
BuildRequires:  pkgconfig(ecore-wl2)
BuildRequires:  pkgconfig(elementary)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  gtest-devel

%{!?TZ_SYS_RO_SHARE: %global TZ_SYS_RO_SHARE /usr/share}

%description
An EFL utility library in SLP C API.


%package devel
Summary:  An EFL utility library in Tizen C API (Development)
Requires: %{name} = %{version}-%{release}

%description devel
%devel_desc

%package unittests
Summary: Tizen EFL utility library unit tests package
Group: Development/Libraries

%description unittests
Test module for testing efl-util APIs

%if 0%{?gcov:1}
%package -n capi-ui-efl-util-gcov
Summary: efl-util gcov data package
Group: Development/Libraries

%description -n capi-ui-efl-util-gcov
efl-util gcno data for gcov
%endif

%prep
%setup -q
cp %{SOURCE1001} .

%build

%{?_toolchain:
%if %{toolchain_is clang}
export CFLAGS="$CFLAGS -Wno-error=implicit-enum-enum-cast "
%endif
}

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -DEFL_BETA_API_SUPPORT -fPIC -fprofile-arcs -ftest-coverage -DTIZEN_TEST_GCOV "
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DEFLUTILGCOV=ON \
%else
export CFLAGS="$CFLAGS -DEFL_BETA_API_SUPPORT "
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DEFLUTILGCOV=OFF \
%endif

make %{?jobs:-j%jobs}

%install
%make_install

%if 0%{?gcov:1}
find test/ -name '*.gcno' -exec rm {} \;

builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

mkdir -p %{buildroot}%{_bindir}/tizen-unittests/%{name}
install -m 0755 %SOURCE1002 %{buildroot}%{_bindir}/tizen-unittests/%{name}/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%license LICENSE.APLv2
%{_libdir}/libcapi-ui-efl-util.so.*

%files devel
%manifest %{name}.manifest
%{_includedir}/ui/efl_util.h
%{_includedir}/ui/efl_util_screenshot_extension.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-ui-efl-util.so
%exclude %{_includedir}/ui/config.h

%files unittests
%defattr(-,root,root,-)
%{_bindir}/capi-ui-efl-util-unittests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

%if 0%{?gcov:1}
%files -n capi-ui-efl-util-gcov
%{_datadir}/gcov/obj/*
%endif
