Name:       smartcard-service
Summary:    Smartcard Service FW
Version:    0.1.59
Release:    0
Group:      Network & Connectivity
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    smartcard-service.service
BuildRequires: cmake
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(openssl3)
BuildRequires: pkgconfig(pkgmgr)
BuildRequires: pkgconfig(pkgmgr-info)
BuildRequires: pkgconfig(cynara-client)
BuildRequires: pkgconfig(cynara-creds-gdbus)
BuildRequires: pkgconfig(cynara-session)
BuildRequires: pkgconfig(capi-system-info)

BuildRequires: python
BuildRequires: python-xml

Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires:         %{name}-common = %{version}-%{release}

%if 0%{?gtests:1}
BuildRequires:  pkgconfig(gmock)
%endif

%description
Smartcard Service FW.

%package    common
Summary:    common smartcard service
Group:      Development/Libraries


%description common
common smartcard service.

%package    common-devel
Summary:    common smartcard service
Group:      Development/Libraries
Requires:   %{name}-common = %{version}-%{release}


%description common-devel
common smartcard service.

%prep
%setup -q


%build
%cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DBUILD_GTESTS=%{?gtests:1}%{!?gtests:0}

%install
%make_install

mkdir -p %{buildroot}/usr/lib/systemd/system/
cp -af %{SOURCE1} %{buildroot}/usr/lib/systemd/system/

mkdir -p %{buildroot}/etc/dbus-1/system.d/
cp -af %{_builddir}/%{name}-%{version}/packaging/org.tizen.SmartcardService.conf %{buildroot}/etc/dbus-1/system.d/

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bindir}/smartcard-daemon
%{_sysconfdir}/dbus-1/system.d/org.tizen.SmartcardService.conf
%{_datadir}/dbus-1/system-services/org.tizen.SmartcardService.service
/usr/lib/systemd/system/%{name}.service
%if 0%{?gtests:1}
%{_bindir}/gtest*
%endif
%license LICENSE.APLv2

%files common
%manifest %{name}-common.manifest
%defattr(-,root,root,-)
%{_libdir}/lib%{name}-common.so.*
%license LICENSE.APLv2

%files common-devel
%manifest %{name}-common-devel.manifest
%defattr(-,root,root,-)
%{_includedir}/%{name}-common/*
%{_libdir}/lib%{name}-common.so
%{_libdir}/pkgconfig/%{name}-common.pc
