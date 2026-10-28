Name: capi-location-manager
Summary: A Location Manager library in Tizen Native API
Version: 0.8.4
Release: 1
Group: Location/API
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(lbs-location)
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(libtzplatform-config)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%if 0%{?gcov:1}
BuildRequires:  lcov
%endif

%description
A Location Manager library in Tizen Native API


%package devel
Summary:  A Location Manager library in Tizen Native API (Development)
Group:    Location/Development
Requires: %{name} = %{version}-%{release}

%description devel
A Location Manager library in Tizen Native API (Development)

#################################################
# gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:    Location Manager (gcov)
Group:      Service Framework/Testing
%description gcov
gcov objects for coverage test
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
cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DLIBDIR=%{_libdir} -DINCLUDEDIR=%{_includedir} \
-DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DTZ_SYS_RO_PACKAGES=%{TZ_SYS_RO_PACKAGES} -DTZ_SYS_BIN=%{TZ_SYS_BIN} \

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
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
%license LICENSE
%{_libdir}/libcapi-location-manager.so.*

%files devel
%{_includedir}/location/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-location-manager.so

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
