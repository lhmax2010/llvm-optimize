Name:       asp-manager
Summary:    ASP(application service platform) manager
Version:    0.0.36
Release:    1
Group:      Network & Connectivity/Other
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    dbus-asp-manager.conf
Source2:    net.asp.service
Source3:    asp-manager.service

BuildRequires:  cmake
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:	pkgconfig(nsd-dns-sd)
BuildRequires:	pkgconfig(capi-network-wifi-manager)
BuildRequires:	pkgconfig(vconf)
BuildRequires:  python
BuildRequires:  python-xml
BuildRequires:  python3-setuptools
Requires:       security-config

%if 0%{?gtests:1}
BuildRequires: pkgconfig(gmock)
%endif

%description
An application service platform manager to manage services and sessions

%prep
%setup -q
chmod 644 %{SOURCE0}
chmod 644 %{SOURCE1}
chmod 644 %{SOURCE2}
chmod 644 %{SOURCE3}
cp -a %{SOURCE1} ./asp-manager.conf
cp -a %{SOURCE2} .
cp -a %{SOURCE3} .

%build

export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"

%cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} \
-DBUILD_GTESTS=%{?gtests:1}%{!?gtests:0} \
-DBIN_DIR=%{_bindir}

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

%make_install

mkdir -p %{buildroot}%{_datadir}/dbus-1/system-services/
cp net.asp.service %{buildroot}%{_datadir}/dbus-1/system-services/
mkdir -p %{buildroot}%{_unitdir}
cp asp-manager.service %{buildroot}%{_unitdir}

#DBus DAC (net-config.manifest enables DBus SMACK)
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
cp asp-manager.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/asp-manager.conf

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,network_fw,network_fw,-)
%attr(500,network_fw,network_fw) %{_bindir}/*
%if 0%{?gtests:1}
	%{_bindir}/gtest-asp-manager
%endif

#DBus DAC
%attr(644,root,root) %{_sysconfdir}/dbus-1/system.d/asp-manager.conf
%attr(644,root,root) %{_datadir}/dbus-1/system-services/net.asp.service
%attr(644,root,root) %{_unitdir}/asp-manager.service
