Name:       capi-network-nfc
Summary:    A NFC library in Native API
Version:    0.4.0
Release:    0
Group:      Network & Connectivity/NFC
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(nfc-common-lib)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(libsystemd)

%if 0%{?gcov:1}
BuildRequires:  gtest-devel
BuildRequires:  lcov
%endif

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
A library for Tizen NFC Native API.

%package devel
Summary:  A NFC library in Native API (Development)
Group:    Network & Connectivity/Development
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the development files for %{name}.

%prep
%setup -q


%build
%if 0%{?gcov:1}
export LDFLAGS+=" -lgcov"
%endif

export CFLAGS="$CFLAGS -DTIZEN_ENGINEER_MODE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_ENGINEER_MODE"
export FFLAGS="$FFLAGS -DTIZEN_ENGINEER_MODE"

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
cmake . -DCMAKE_INSTALL_PREFIX=/usr -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DCMAKE_LIB_DIR=%{_libdir} \
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
%manifest capi-network-nfc.manifest
%license LICENSE.APLv2
%{_libdir}/libcapi-network-nfc.so*

%files devel
%{_includedir}/network/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-network-nfc.so
%{_bindir}/nfc_unit_test
