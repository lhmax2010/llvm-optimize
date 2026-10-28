Name:       capi-appfw-capmgr
Summary:    Capability Manager Native API
Version:    0.0.4
Release:    1
Group:      Application Framework/Application Communication
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  gtest-devel
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(sqlite3)

%description
Tizen Capability Manager Native API

%package devel
Summary:   Capability Manager development files
Group:     Application Framework/Package Management
Requires:  %{name} = %{version}

%description devel
This package contains header files of capability manager native API

%package tests
Summary:   Unit-tests for capmgr native API
Requires:  %{name} = %{version}

%description tests
Unit-tests for capmgr native API

%prep
%setup -q
cp %{SOURCE1001} .

%build
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DUNITDIR=%{_unitdir} \
         -DFULLVER=%{version} \
         -DMAJORVER=${MAJORVER}

%__make %{?_smp_mflags}

%install
%make_install

%post
/sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/lib%{name}.so.*
%{_bindir}/capmgr-test

%files devel
%{_includedir}/appfw/capability_manager.h
%{_includedir}/appfw/capability_manager_internal.h
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/lib%{name}.so

%files tests
%{_bindir}/capi-appfw-capmgr-ut/*
