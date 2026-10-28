Name:       capi-network-smartcard
Summary:    A Smartcard library in Native API
Version:    0.0.16
Release:    0
Group:      Network & Connectivity/Smartcard
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(smartcard-service-common)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-info)

%if 0%{?gcov:1}
BuildRequires:  gtest-devel
BuildRequires:  lcov
%endif

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description

%package devel
Summary:  A Smartcard library in Native API (Development)
Group:    Network & Connectivity/Development
Requires: %{name} = %{version}-%{release}

%description devel

%prep
%setup -q

%build
%if 0%{?gcov:1}
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

cmake . -DCMAKE_INSTALL_PREFIX=/usr -DFULLVER=%{version} \
        -DMAJORVER=${MAJORVER} -DCMAKE_LIB_DIR=%{_libdir} -DBUILD_GCOV=%{?gcov:1}%{!?gcov:0} \
%ifarch %{arm}
	-DTIZEN_SMARTCARD_SUPPORT=1
%endif


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
%manifest capi-network-smartcard.manifest
%license LICENSE.APLv2
%{_libdir}/libcapi-network-smartcard.so*

%files devel
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-network-smartcard.so
%{_bindir}/smartcard_unit_test
