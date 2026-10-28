Name: mobileap-agent
Summary: Mobile AP daemon for setting tethering environments
Version: 1.1.10
Release: 1
Group: System/Network
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz
Source1: mobileap-agent.service
Source2: org.tizen.MobileapAgent.service
BuildRequires: pkgconfig(alarm-service)
BuildRequires: pkgconfig(capi-network-connection)
BuildRequires: pkgconfig(capi-network-wifi-manager)
BuildRequires: pkgconfig(capi-network-wifi-direct)
BuildRequires: pkgconfig(capi-system-device)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(deviced)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gthread-2.0)
BuildRequires: pkgconfig(key-manager)
BuildRequires: pkgconfig(yaca)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(vconf)
BuildRequires: cmake
BuildRequires: python3-setuptools
Requires: iproute2
Requires: iptables
Requires: dnsmasq

%description
Mobile AP daemon for setting tethering environments

%package extension-headed
Summary: Extension for headed profile
BuildRequires: pkgconfig(appcore-common)
BuildRequires: pkgconfig(appsvc)
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(capi-network-bluetooth)
BuildRequires: pkgconfig(notification)
BuildRequires: pkgconfig(syspopup-caller)
Requires: %{name} = %{version}-%{release}
%description extension-headed
Mobile AP daemon for setting tethering environments for headed profile

%package extension-da
Summary: Extension for appliance devices
BuildRequires: pkgconfig(appcore-common)
BuildRequires: pkgconfig(appsvc)
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(capi-network-bluetooth)
BuildRequires: pkgconfig(notification)
BuildRequires: pkgconfig(syspopup-caller)
Requires: %{name} = %{version}-%{release}
%description extension-da
Mobile AP daemon for setting tethering environments for digital appliance

%if 0%{?gtests:1}
%package unittest
Summary: Unnit test for mobileap
BuildRequires: pkgconfig(appcore-common)
BuildRequires: pkgconfig(appsvc)
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(capi-network-connection)
BuildRequires: pkgconfig(capi-network-bluetooth)
BuildRequires: pkgconfig(notification)
BuildRequires: pkgconfig(syspopup-caller)
BuildRequires: pkgconfig(gmock)
Requires: %{name} = %{version}-%{release}
%description unittest
Unnit test for mobileap
%endif

%prep
%setup -q

%build
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"

# Build for headed
%cmake -DCMAKE_BUILD_TYPE="HEADED" \
	-DTIZEN_FEATURE_ENABLE_IPV6=1 \
	-DTIZEN_FEATURE_HEADLESS=0 \
	-DTIZEN_DA=0 \
	-DBUILD_GTESTS=0 \
	.

%make_install
mv %{buildroot}%{_bindir}/mobileap-agent %{_builddir}/%{name}-%{version}/mobileap-agent.headed

make %{?jobs:-j%jobs}

%if 0%{?gtests:1}
%cmake -DCMAKE_BUILD_TYPE="HEADED" \
   -DTIZEN_FEATURE_ENABLE_IPV6=1 \
   -DTIZEN_FEATURE_HEADLESS=0 \
   -DTIZEN_DA=0 \
   -DBUILD_GTESTS=1 \
   .

%make_install
rm %{buildroot}%{_bindir}/mobileap-agent

make %{?jobs:-j%jobs}
%endif

# Build for DA
%cmake -DCMAKE_BUILD_TYPE="DA" \
   -DTIZEN_FEATURE_ENABLE_IPV6=1 \
   -DTIZEN_FEATURE_HEADLESS=1 \
   -DTIZEN_DA=1 \
   -DBUILD_GTESTS=0 \
   .

%make_install
mv %{buildroot}%{_bindir}/mobileap-agent %{_builddir}/%{name}-%{version}/mobileap-agent.da

make %{?jobs:-j%jobs}

# Build for base rpm
%cmake -DCMAKE_BUILD_TYPE="BASE" \
	-DTIZEN_FEATURE_ENABLE_IPV6=0 \
   -DTIZEN_FEATURE_HEADLESS=1 \
	-DTIZEN_DA=0 \
	-DBUILD_GTESTS=0 \
	.

make %{?jobs:-j%jobs}

%install
%make_install

mv %{_builddir}/%{name}-%{version}/mobileap-agent.headed %{buildroot}%{_bindir}
mv %{_builddir}/%{name}-%{version}/mobileap-agent.da %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
cp mobileap-agent.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/mobileap-agent.conf
mkdir -p %{buildroot}%{_unitdir}
cp %{SOURCE1} %{buildroot}%{_unitdir}/mobileap-agent.service
mkdir -p %{buildroot}%{_datadir}/dbus-1/system-services/
cp %{SOURCE2} %{buildroot}%{_datadir}/dbus-1/system-services/org.tizen.MobileapAgent.service
%if 0%{?gtests:1}
cp %{_builddir}/%{name}-%{version}/unittest/gtest-mobileap-agent %{buildroot}%{_bindir}

mkdir -p %{buildroot}/var/lib/misc
cp unittest/resource/dnsmasq.leases %{buildroot}/var/lib/misc
%endif


%post
/bin/chmod +x /opt/etc/dump.d/module.d/tethering_dump.sh

%post extension-headed
pushd %{_bindir}
mv mobileap-agent.headed mobileap-agent
popd
%preun extension-headed
rm %{_bindir}/mobileap-agent

%post extension-da
pushd %{_bindir}
mv mobileap-agent.da mobileap-agent
popd
%preun extension-da
rm %{_bindir}/mobileap-agent

%files
%manifest mobileap-agent.manifest
%defattr(-,root,root,-)
%{_unitdir}/mobileap-agent.service
%{_datadir}/dbus-1/system-services/org.tizen.MobileapAgent.service
%attr(644,root,root) %{_sysconfdir}/dbus-1/system.d/mobileap-agent.conf
%{_bindir}/mobileap-agent
%attr(755,root,root) %{_bindir}/mobileap-agent-cmd.sh
/opt/etc/dump.d/module.d/tethering_dump.sh
%license LICENSE.APLv2.0

%files extension-headed
%defattr(-,root,root,-)
%{_bindir}/mobileap-agent.headed

%files extension-da
%defattr(-,root,root,-)
%{_bindir}/mobileap-agent.da

%if 0%{?gtests:1}
%files unittest
%{_bindir}/gtest-mobileap-agent
%attr(755,nework_fw,nework_fw)
/var/lib/misc/dnsmasq.leases
%endif
