Name:       stc-iptables
Summary:    STC(Smart Traffic Control) iptables
Version:    0.0.26
Release:    0
Group:      Network & Connectivity/Other
License:    GPL-2.0 and Apache-2.0
Source0:    %{name}-%{version}.tar.gz

Requires:       security-config
BuildRequires:  cmake
BuildRequires:  python3-setuptools
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(libiptc)
BuildRequires:  pkgconfig(libip6tc)
BuildRequires:  pkgconfig(libsystemd)

%if 0%{?gtests:1}
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(gmock)
%endif

%description
A smart traffic control iptables to manage iptables rules using libiptc

%package test
Summary:   STC iptables test binaries

%description test
Test Application for STC Iptables

%prep
%setup -q
chmod 644 %{SOURCE0}

%build

export CFLAGS="$CFLAGS -D_GNU_SOURCE"
export CXXFLAGS="$CXXFLAGS -D_GNU_SOURCE"

%cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DBIN_DIR=%{_bindir} \
	-DLIB_PATH=%{_lib} \
	-DBUILD_GTESTS=%{?gtests:1}%{!?gtests:0} \
	-DBUILD_GCOV=%{?gcov:1}%{!?gcov:0}

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

%make_install

mkdir -p %{buildroot}/%{_localstatedir}/lib/stc

#Systemd iptables service file
mkdir -p %{buildroot}%{_unitdir}
cp resources/systemd/stc-iptables.service %{buildroot}%{_unitdir}/stc-iptables.service

#DBus DAC (stc-iptables.manifest enables DBus SMACK)
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
cp resources/dbus/stc-iptables.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/stc-iptables.conf

mkdir -p %{buildroot}%{_datadir}/dbus-1/system-services/
cp resources/dbus/net.stc-iptables.service %{buildroot}%{_datadir}/dbus-1/system-services/net.stc.iptables.service

%post
#Logs
mkdir -p /opt/data/network
chmod 755 /opt/data/network
chown network_fw:network_fw /opt/data/network
#/usr/sbin/setcap cap_net_bind_service,cap_net_raw,cap_net_admin=ei %{_bindir}/stc-iptables

%files
%manifest %{name}.manifest
%license LICENSE.GPL2 LICENSE.APACHE
%defattr(-,network_fw,network_fw,-)
%attr(500,network_fw,network_fw) %{_bindir}/stc-iptables

%attr(644,root,root) %{_unitdir}/stc-iptables.service

%attr(755,network_fw,network_fw) /%{_localstatedir}/lib/stc

#DBus DAC
%attr(644,root,root) %{_sysconfdir}/dbus-1/system.d/stc-iptables.conf

%attr(644,root,root) %{_datadir}/dbus-1/system-services/net.stc.iptables.service

#Test
%{_bindir}/stc_ipt_test
%attr(755,root,root) %{_bindir}/stc_ipt_test

%if 0%{?gtests:1}
%{_bindir}/gtest*
%endif
