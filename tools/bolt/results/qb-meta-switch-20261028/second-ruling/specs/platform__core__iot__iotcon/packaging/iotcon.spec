Name:       iotcon
Summary:    Tizen IoT Connectivity
Version:    0.4.0
Release:    2
Group:      Network & Connectivity/Service
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  boost-devel
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(iotivity)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(cynara-client)

Requires(post): /usr/bin/chgrp, /usr/bin/chmod, /usr/bin/chsmack


%description
Tizen IoT Connectivity Service & Library(Client) based on Iotivity


%package devel
Summary:    TizenIoT Connectivity(devel)
Group:      Network & Connectivity/Development
Requires:   %{name} = %{version}

%description devel
IoT Connectivity Manager development Kit


%package test
Summary:    Tizen IoT Connectivity(test)
Group:      Network & Connectivity/Testing
Requires:   %{name} = %{version}

%description test
Tizen IoT Connectivity Test Programs

%prep
%setup -q


%build

%if "%{?profile}" == "tv"
%define PRODUCT_TV 1
%else
%define PRODUCT_TV 0
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DMAJORVER=${MAJORVER} \
	-DFULLVER=%{version} \
	-DBIN_INSTALL_DIR:PATH=%{_bindir} \
	-DPRODUCT_TV=%{PRODUCT_TV}

%install
rm -rf %{buildroot}
%make_install

%post
/sbin/ldconfig

%postun
/sbin/ldconfig


%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/lib%{name}.so.*
%license LICENSE.APLv2

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/*.h
%license LICENSE.APLv2

%files test
%manifest %{name}-test.manifest
%defattr(-,root,root,-)
%{_bindir}/iotcon-test-*
%license LICENSE.APLv2
