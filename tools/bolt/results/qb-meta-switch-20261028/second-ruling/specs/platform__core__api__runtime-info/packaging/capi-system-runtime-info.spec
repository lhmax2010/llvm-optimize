Name:       capi-system-runtime-info
Summary:    A Runtime Information library in Core API
Version:    0.5.2
Release:    1
Group:      System/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001:	%{name}.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libsyscommon)
BuildRequires:  pkgconfig(hal-api-common)
BuildRequires:  pkgconfig(hal-api-device)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description


%package devel
Summary:  A Runtime Information library in Core API (Development)
Group:    Development/System
Requires: %{name} = %{version}-%{release}
Requires:  pkgconfig(capi-base-common)

%description devel
%devel_desc


%package test
Summary:  A Runtime Information test binary
Requires: %{name} = %{version}-%{release}
Requires: memps

%description test
Binary for testing Runtime-info APIs


%if 0%{?gcov:1}
%package gcov
Summary:  A Runtime Information gcov test file
%description gcov
gcno files for Runtime-info line coverage test
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
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DGCOV=%{?gcov:1}%{!?gcov:0}

make %{?jobs:-j%jobs}

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
%license LICENSE.APLv2
%{_libdir}/lib*.so.*

%files devel
%{_includedir}/system/runtime_info.h
%{_includedir}/system/runtime_info-internal.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib*.so

%files test
%attr(700,root,root) %{_bindir}/runtime-info-test

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
