Name:       libcryptsvc
Summary:    Crypto Service Library
Version:    0.0.2
Release:    6
Group:      Security/Libraries
License:    Apache-2.0 and BSL-1.0
Source0:    %{name}-%{version}.tar.gz
Source1001: libcryptsvc.manifest
BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(openssl3)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(libtzplatform-config)

%description
Crypto Service Library.

%package devel
Summary:    Crypto Service Library (Development)
Group:      Security/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Crypto Service Library (Development).

%package test
Summary:    Testing for Crypto Service
Group:      Security/Testing
BuildRequires: boost-devel
Requires:   boost-test
Requires:   %{name} = %{version}-%{release}

%description test
Testing for Crypto Service.

%prep
%setup -q

%build
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"

export CFLAGS="$CFLAGS -DTIZEN_ENGINEER_MODE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_ENGINEER_MODE"
export FFLAGS="$FFLAGS -DTIZEN_ENGINEER_MODE"

%ifarch %ix86
export CFLAGS="$CFLAGS -DTIZEN_EMULATOR_MODE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_EMULATOR_MODE"
export FFLAGS="$FFLAGS -DTIZEN_EMULATOR_MODE"
%endif

%{!?build_type:%define build_type "Release"}
%cmake . \
    -DCMAKE_BUILD_TYPE=%build_type \
%ifarch %ix86 x86_64
    -DARCH=x86 \
%else
    -DARCH=arm \
%endif
    -DVERSION=%version \
    -DDESCRIPTION="%summary" \
    -DTZ_SYS_ETC=%TZ_SYS_ETC

make %{?jobs:-j%jobs}

%install
%make_install
mkdir -p %{buildroot}%{_datadir}/
cp -a %{SOURCE1001} %{buildroot}%{_datadir}/


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{_datadir}/%{name}.manifest
%license LICENSE
%license LICENSE.BSL-1.0
%{_libdir}/libcryptsvc.so.*
%{_libdir}/libdevice_info.so.*
%{TZ_SYS_ETC}/duid-gadget

%files devel
%{_includedir}/*
%{_libdir}/libcryptsvc.so
%{_libdir}/libdevice_info.so
%{_libdir}/pkgconfig/cryptsvc.pc

%files test
%{_bindir}/cryptsvc-test
