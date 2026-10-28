Name:			wifi-tethering-manager
Version:		1.0.7
Release:		1
License: 		Apache-2.0
Summary:		Wi-Fi tethering manager for P2P extension.
Group:          Network & Connectivity/Connection Management
ExcludeArch:    i586
Source0:		%{name}-%{version}.tar.gz
BuildRequires:	cmake
BuildRequires:	pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(capi-network-wifi-manager)
BuildRequires:	pkgconfig(capi-network-wifi-direct)
BuildRequires:	pkgconfig(capi-network-tethering)
BuildRequires:	pkgconfig(capi-system-device)
BuildRequires:	pkgconfig(key-manager)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(vconf)

%description
Wi-Fi tethering manager.

%define _rodir /usr

%prep
%setup -q

%build
cmake \
	-DCMAKE_INSTALL_PREFIX=%{_rodir} \
	-DBINDIR=%{_bindir} \
	-DVERSION=%{version} \
	.

make %{?jobs:-j%jobs}

%install
%make_install

mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
cp units/wifi-tethering-dbus.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/wifi-tethering-dbus.conf
mkdir -p %{buildroot}%{_unitdir}
cp units/wifi-tethering-manager.service %{buildroot}%{_unitdir}/wifi-tethering-manager.service
mkdir -p %{buildroot}%{_datadir}/dbus-1/system-services/
cp units/net.wifitetheringExt.service  %{buildroot}%{_datadir}/dbus-1/system-services/net.wifitetheringExt.service

mkdir -p %{buildroot}/%{_localstatedir}/lib/wifi-tethering
install -m 0644 units/settings %{buildroot}/%{_localstatedir}/lib/wifi-tethering

mkdir -p %{buildroot}%{_unitdir}/multi-user.target.wants/
ln -s ../net-config.service %{buildroot}%{_unitdir}/multi-user.target.wants/wifi-tethering-manager.service

%clean
rm -rf %{buildroot}

%files
%manifest wifi-tethering-manager.manifest
%license LICENSE
%attr(500,network_fw,network_fw) %{_bindir}/wifi-tethering-manager
%attr(644,root,root) %{_unitdir}/wifi-tethering-manager.service
%attr(644,root,root) %{_unitdir}/multi-user.target.wants/wifi-tethering-manager.service
%attr(644,root,root) %{_localstatedir}/lib/wifi-tethering/settings
%attr(644,root,root) %{_datadir}/dbus-1/system-services/net.wifitetheringExt.service
%attr(644,root,root) %config %{_sysconfdir}/dbus-1/system.d/wifi-tethering-dbus.conf
%defattr(755,network_fw,network_fw,-)
%{_bindir}/wifi-tethering-manager
