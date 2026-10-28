Name:       capi-network-thread
Summary:    Network Thread Framework
Version:    0.9.0
Release:    2
Group:      Connectivity/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001:	%{name}.manifest
Source1002:	%{name}-devel.manifest
#Requires(post): /sbin/ldconfig
#Requires(postun): /sbin/ldconfig

BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(capi-appfw-app-control)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(gtest)
BuildRequires:  cmake

%description
Network Thread Framework

%package devel
Summary:    Network Thread Framework (DEV)
Group:      Development/Connectivit
Requires:   %{name} = %{version}-%{release}

%description devel
Network Thread Framework.

%devel_desc

%package test
Summary: Network Thread Framework test application
Group:   TO_BE/FILLED
Requires: %{name} = %{version}-%{release}

%description test
This package is for Network Thread Framework CAPI test application

%prep
%setup -q
cp %{SOURCE1001} %{SOURCE1002} .

%ifarch aarch64
echo arch64
export CFLAGS+=" -DARCH64"
export CXXFLAGS+=" -DARCH64"
export FFLAGS+=" -DARCH64"
%endif

%ifarch x86_64
echo x86_64
export CFLAGS+=" -DARCH64"
export CXXFLAGS+=" -DARCH64"
export FFLAGS+=" -DARCH64"
%endif

%build

%cmake

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . \
        -DFULLVER=%{version} \
        -DMAJORVER=${MAJORVER} \
        -DBIN_DIR:PATH=%{_bindir}

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/libcapi-network-thread.so.*

%files devel
%manifest %{name}-devel.manifest
%{_includedir}/network/*
%{_libdir}/pkgconfig/%{name}.pc

%{_libdir}/pkgconfig/capi-network-thread.pc
%{_libdir}/libcapi-network-thread.so

%files test
%manifest %{name}.manifest
%attr(777,network_fw,network_fw) %{_bindir}/thread-test
