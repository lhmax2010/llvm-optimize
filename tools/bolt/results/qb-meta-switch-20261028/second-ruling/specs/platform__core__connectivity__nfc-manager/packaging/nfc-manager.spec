Name:       nfc-manager
Summary:    NFC framework manager
Version:    0.2.0
Release:    0
Group:      Network & Connectivity/NFC
License:    Flora-1.1
Source0:    %{name}-%{version}.tar.gz
Source1:    nfc-manager.socket
BuildRequires: cmake
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(tapi)
BuildRequires: pkgconfig(bluetooth-api)
BuildRequires: pkgconfig(capi-network-bluetooth)
BuildRequires: pkgconfig(mm-sound)
BuildRequires: pkgconfig(appsvc)
BuildRequires: pkgconfig(feedback)
BuildRequires: pkgconfig(capi-media-wav-player)
BuildRequires: pkgconfig(openssl3)
BuildRequires: pkgconfig(deviced)
BuildRequires: pkgconfig(mm-keysound)
BuildRequires: pkgconfig(syspopup-caller)
BuildRequires: pkgconfig(notification)
BuildRequires: pkgconfig(capi-network-wifi-manager)
BuildRequires: pkgconfig(capi-network-wifi-direct)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(pkgmgr-info)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(cynara-client)
BuildRequires: pkgconfig(cynara-creds-gdbus)
BuildRequires: pkgconfig(cynara-session)
BuildRequires: pkgconfig(capi-system-device)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(hal-api-common)
BuildRequires: pkgconfig(hal-api-nfc)

BuildRequires: python
BuildRequires: python-xml
BuildRequires: python3-setuptools

%if 0%{?gtests:1}
BuildRequires: pkgconfig(gmock)
%endif

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig


%description
A NFC Service Framework for support Tizen NFC.

%package haltests
Summary: nfc-manager extension for HAL test
BuildRequires: pkgconfig(gmock)
BuildRequires: pkgconfig(capi-system-info)
Requires: %{name} = %{version}-%{release}
%description haltests
TIZEN nfc-manager extension for HAL test.

%prep
%setup -q


%package -n nfc-common-lib
Summary:    NFC common library
Group:      Development/Libraries


%description -n nfc-common-lib
A library for Tizen NFC Framework and Tizen NFC client library.


%package -n nfc-common-lib-devel
Summary:    NFC common library (devel)
Group:      Network & Connectivity/Development
Requires:   nfc-common-lib = %{version}-%{release}


%description -n nfc-common-lib-devel
This package contains the development files for NFC Common library.


%build
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE -Wno-deprecated-declarations"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE -Wno-deprecated-declarations"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
export CFLAGS="$CFLAGS -DTIZEN_TELEPHONY_ENABLED"

%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

export LDFLAGS+=" -Wl,--rpath=%{_prefix}/lib -Wl,--as-needed"
LDFLAGS="$LDFLAGS" cmake . \
		-DLIBDIR=%{_libdir} \
		-DINCLUDE_INSTALL_DIR=%{_includedir} \
		-DTIZEN_ENGINEER_MODE=1 \
		-DCMAKE_INSTALL_PREFIX=%{_prefix} \
		-DTIZEN_TELEPHONY_ENABLED=1 \
		-DBIN_DIR=%{_bindir} \
		-DBUILD_GTESTS=%{?gtests:1}%{!?gtests:0} \
		-DBUILD_GCOV=%{?gcov:1}%{!?gcov:0} \
%ifarch aarch64 x86_64 riscv64
		-DTIZEN_ARCH_64=1 \
%endif
%ifarch %{ix86} x86_64
		-DTIZEN_EMULATOR=1 \
%endif

%install
%make_install

mkdir -p %{buildroot}/usr/lib/systemd/system/multi-user.target.wants
cp -af %{_builddir}/%{name}-%{version}/packaging/%{name}.service %{buildroot}/usr/lib/systemd/system/
cp -af %{SOURCE1} %{buildroot}/usr/lib/systemd/system/

mkdir -p %{buildroot}/usr/lib/systemd/system/multi-user.target.wants
ln -s ../%{name}.service %{buildroot}/usr/lib/systemd/system/multi-user.target.wants/%{name}.service

mkdir -p %{buildroot}/etc/dbus-1/system.d/
cp -af %{_builddir}/%{name}-%{version}/packaging/org.tizen.NetNfcService.conf %{buildroot}/etc/dbus-1/system.d/

%post
/sbin/ldconfig

mkdir -p -m 777 /opt/usr/data/nfc-manager-daemon
chown network_fw:network_fw /opt/usr/data/nfc-manager-daemon
chsmack -a "System" /opt/usr/data/nfc-manager-daemon

mkdir -p -m 744 /opt/usr/share/nfc_debug
chown network_fw:network_fw /opt/usr/share/nfc_debug
chsmack -a "System" /opt/usr/share/nfc_debug

mkdir -p -m 744 /opt/usr/share/nfc-manager-daemon
chown network_fw:network_fw /opt/usr/share/nfc-manager-daemon
chsmack -a "System" /opt/usr/share/nfc-manager-daemon

mkdir -p -m 744 /opt/usr/share/nfc-manager-daemon/message
chown network_fw:network_fw /opt/usr/share/nfc-manager-daemon/message
chsmack -a "System" /opt/usr/share/nfc-manager-daemon/message

systemctl daemon-reload
if [ $1 == 1 ]; then
    systemctl restart %{name}.service
fi

%postun
/sbin/ldconfig

if [ $1 == 0 ]; then
    systemctl stop %{name}.service
fi
systemctl daemon-reload


%post -n nfc-common-lib -p /sbin/ldconfig


%postun -n nfc-common-lib -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%license LICENSE.Flora
%defattr(-,root,root,-)
%{_bindir}/nfc-manager-daemon
/usr/lib/systemd/system/%{name}.service
/usr/lib/systemd/system/%{name}.socket
/usr/lib/systemd/system/multi-user.target.wants/%{name}.service
%{_datadir}/dbus-1/system-services/org.tizen.NetNfcService.service
/etc/dbus-1/system.d/org.tizen.NetNfcService.conf
%if 0%{?gtests:1}
%{_bindir}/gtest*
%endif


%files -n nfc-common-lib
%manifest nfc-common-lib.manifest
%license LICENSE.Flora
%defattr(-,root,root,-)
%{_libdir}/libnfc-common-lib.so
%{_libdir}/libnfc-common-lib.so.*
%{_datadir}/nfc-manager-daemon/sounds/Operation_sdk.wav


%files -n nfc-common-lib-devel
%manifest nfc-common-lib-devel.manifest
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/nfc-common-lib.pc
%{_includedir}/*.h

%files haltests
%manifest %{name}.manifest
%{_bindir}/hal/*haltests
