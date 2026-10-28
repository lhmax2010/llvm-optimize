Name:       capi-network-mtp
Summary:    A MTP library in Native API
Version:    1.3.21
Release:    1
Group:      Network & Connectivity/Other
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(sqlite3)
Buildrequires:  pkgconfig(libtzplatform-config)
BuildRequires:  python
Buildrequires:  python-xml

%if 0%{?gcov:1}
BuildRequires:  gtest-devel
BuildRequires:  lcov
%endif

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description

%package devel
Summary:  A MTP library in Native API (Development)
Group:    Network & Connectivity/Other
Requires: %{name} = %{version}-%{release}

%description devel

%prep
%setup -q

%build

%if 0%{?gcov:1}
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DFULLVER=%{version} \
	-DMAJORVER=${MAJORVER}\
	-DBUILD_GCOV=%{?gcov:1}%{!?gcov:0}

make %{?jobs:-j%jobs}

%if 0%{?gcov:1}
mkdir -p gcov-obj
find . -name '*.gcno' -exec cp '{}' gcov-obj ';'
%endif

%install
rm -rf %{buildroot}

%make_install

%check
%if 0%{?gcov:1}
pushd unittest
./run_coverage.sh
popd
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest capi-network-mtp.manifest
%license LICENSE.APLv2
%{_libdir}/libcapi-network-mtp.so*

%files devel
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-network-mtp.so
%{_bindir}/mtp_unit_test
