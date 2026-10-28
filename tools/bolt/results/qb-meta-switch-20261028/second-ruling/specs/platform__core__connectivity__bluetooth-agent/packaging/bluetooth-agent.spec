%define _usrlibdir /usr/lib

Name:       bluetooth-agent
Summary:    Bluetooth agent packages that support various external profiles
Version:    0.10.0
Release:    1
Group:      Network & Connectivity/Bluetooth
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: 	bluetooth-agent.manifest

BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(bluetooth-api)
BuildRequires:  pkgconfig(capi-media-audio-io)

# The profile macro usage with the following comments may be removed after
# Tizen OBS build projects are merged. However, each vendor may keep using
# such if/endif statement to skip building profiles not interested

# This usage of profile macro does NOT conflict 4.0 configurability.
%if "%{?profile}" != "mobile" && "%{?profile}" != "tv"
# Original: wearable, ivi. Added: common, "undefined"
BuildRequires:  pkgconfig(alarm-service)
BuildRequires:  pkgconfig(capi-appfw-app-manager)
BuildRequires:  pkgconfig(capi-system-device)
%endif
# This usage of profile macro does NOT conflict 4.0 configurability.
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(tapi)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(appsvc)
BuildRequires:  pkgconfig(capi-appfw-application)
BuildRequires:  pkgconfig(capi-network-connection)
BuildRequires:  pkgconfig(capi-network-bluetooth)
BuildRequires:  pkgconfig(capi-media-image-util)
BuildRequires:  pkgconfig(contacts-service2)
BuildRequires:  pkgconfig(libexif)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  cmake
Requires: security-config
%if 0%{?gcov:1}
BuildRequires:  gtest-devel
BuildRequires:  lcov
%endif

#Requires:	%{name}-compat = %{version}-%{release}
#Recommends:	%{name}-profile_common = %{version}-%{release}

%description
Bluetooth agent packages that support various external profiles

%package hfp_ag
Summary:	Bluetooth agent for HFP(Hands-Free Profile)'s AG(Audio Gate) role
Requires:   %{name} = %{version}-%{release}
Group:      Network & Connectivity/Bluetooth
%description hfp_ag
Bluetooth agent binary compiled for HFP(Hands-Free Profile)'s AG(Audio Gate) role

%package hfp_hf
Summary:	Bluetooth agent for HFP(Hands-Free Profile)'s HF(Hands-Free) role
Requires:   %{name} = %{version}-%{release}
Group:      Network & Connectivity/Bluetooth
%description hfp_hf
Bluetooth agent binary compiled for HFP(Hands-Free Profile)'s HF(Hands-Free) role

%package pbap
Summary:	Bluetooth agent for PBAP(PhoneBook Access Profile) server
Requires:   %{name} = %{version}-%{release}
Group:      Network & Connectivity/Bluetooth
%description pbap
Bluetooth agent binary compiled for PBAP(PhoneBook Access Profile) server

%package hid
Summary:	Bluetooth agent for HID(Human Interface Device)'s device role
Requires:   %{name} = %{version}-%{release}
Group:      Network & Connectivity/Bluetooth
%description hid
Bluetooth agent binary compiled for HID(Human Interface Device)'s device role

%package ipsp
Summary:	Bluetooth agent for IPSP(Internet Protocol Support Profile)
Requires:   %{name} = %{version}-%{release}
Group:      Network & Connectivity/Bluetooth
%description ipsp
Bluetooth agent binary compiled for IPSP(Internet Protocol Support Profile)

%package tool
Summary:       Test Application for HF

%description tool
Test Application for HF

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
export CFLAGS="$CFLAGS -DTIZEN_FEATURE_BT_MEDIA_ENHANCE"
export CFLAGS="$CFLAGS -DTIZEN_FEATURE_BT_HFP_AG"
export CFLAGS="$CFLAGS -DTIZEN_SUPPORT_DUAL_HF"

%ifarch aarch64 x86_64 riscv64
echo arch64
export CFLAGS="$CFLAGS -DARCH64"
export CXXFLAGS="$CXXFLAGS -DARCH64"
export FFLAGS="$FFLAGS -DARCH64"
%endif

export CFLAGS="$CFLAGS -fpie -DTIZEN_FEATURE_BP_PBAP_SIM -fvisibility=hidden "
export CXXFLAGS="$CXXFLAGS -fpie -DTIZEN_FEATURE_BP_PBAP_SIM -fvisibility=hidden "

export LDFLAGS="$LDFLAGS -Wl,--rpath=/usr/lib -Wl,--as-needed -Wl,--unresolved-symbols=ignore-in-shared-libs -pie"

export CFLAGS_DEFAULT="$CFLAGS"

%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export FFLAGS="$FFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

%{?_toolchain:
%if %{toolchain_is clang}
export CFLAGS="$CFLAGS -Wno-error=implicit-enum-enum-cast "
%endif
}

# Build All (wearalbe/ivi/common/tv/mobile)
%cmake . -DCMAKE_INSTALL_PREFIX=/usr \
	-DTIZEN_FEATURE_BT_HFP_AG=1 \
	-DBUILD_GTESTS=%{?gcov:1}%{!?gcov:0} \
	-DBUILD_GCOV=%{?gcov:1}%{!?gcov:0}

make VERBOSE=1

%if 0%{?gcov:1}
mkdir -p gcov-obj
find . -name '*.gcno' -exec cp '{}' gcov-obj ';'
%endif

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}%{_unitdir}/multi-user.target.wants/

# This usage of profile macro does NOT conflict 4.0 configurability.
#%if "%{?profile}" != "mobile" && "%{?profile}" != "tv"
# Original: wearable, ivi. Added: common, "undefined"
#mkdir -p %{buildroot}%{_datadir}/dbus-1/system-services
#mkdir -p %{buildroot}%{_bindir}/
#install -D -m 0644 %{buildroot}/usr/share/dbus-1/system-services/org.bluez.hf_agent.service %{buildroot}%{_datadir}/dbus-1/system-services/
#install -D -m 0644 %{buildroot}/usr/share/dbus-1/system-services/org.bluez.ipsp_agent.service %{buildroot}%{_datadir}/dbus-1/system-services/
#install -D -m 0644 %{buildroot}/usr/bin/bluetooth-hf-agent %{buildroot}%{_bindir}/
#install -D -m 0644 %{buildroot}/usr/bin/bluetooth-ipsp-agent %{buildroot}%{_bindir}/
#%endif
install -D -m 0644 packaging/bluetooth-pbap-agent.service %{buildroot}%{_unitdir}/bluetooth-pbap-agent.service
install -D -m 0644 packaging/bluetooth-ag-agent.service %{buildroot}%{_unitdir}/bluetooth-ag-agent.service
install -D -m 0644 packaging/bluetooth-hf-agent.service %{buildroot}%{_unitdir}/bluetooth-hf-agent.service
install -D -m 0644 packaging/bluetooth-hid-agent.service %{buildroot}%{_unitdir}/bluetooth-hid-agent.service
ln -s ../bluetooth-hf-agent.service %{buildroot}%{_unitdir}/multi-user.target.wants/bluetooth-hf-agent.service

%if 0%{?gcov:1}
mkdir -p %{buildroot}%{_datadir}/gcov/obj/%{name}
install -m 0644 gcov-obj/* %{buildroot}%{_datadir}/gcov/obj/%{name}/
%endif

%check
%if 0%{?gcov:1}
cd unittest
./run_coverage.sh
cd ..
%endif

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-, root, root)
%exclude %{_bindir}/gtest-bluetooth-agent
%exclude %{_libdir}/lib*
%exclude %{_datadir}/gcov/obj/*

%files hfp_ag
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/bluetooth-ag-agent
%attr(0666,-,-) /var/lib/bluetooth/voice-recognition-blacklist
%{_datadir}/dbus-1/system-services/org.bluez.ag_agent.service
%{_sysconfdir}/dbus-1/system.d/bluetooth-ag-agent.conf
%{_unitdir}/bluetooth-ag-agent.service
#%exclude %{_unitdir}/bluetooth-map-agent.service
#%exclude %{_unitdir}/bluetooth-pbap-agent.service

%files hfp_hf
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/bluetooth-hf-agent
%{_datadir}/dbus-1/system-services/org.bluez.hf_agent.service
%{_sysconfdir}/dbus-1/system.d/bluetooth-hf-agent.conf
%{_unitdir}/bluetooth-hf-agent.service
%{_unitdir}/multi-user.target.wants/bluetooth-hf-agent.service
#%exclude %{_unitdir}/bluetooth-map-agent.service
#%exclude %{_unitdir}/bluetooth-pbap-agent.service

%files pbap
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/bluetooth-pb-agent
%{_datadir}/dbus-1/system-services/org.bluez.pb_agent.service
%{_unitdir}/bluetooth-pbap-agent.service
%{_sysconfdir}/dbus-1/system.d/bluetooth_pb_agent.conf

%files hid
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/bluetooth-hid-agent
%{_datadir}/dbus-1/system-services/org.bluez.hid_agent.service
%{_unitdir}/bluetooth-hid-agent.service
%{_sysconfdir}/dbus-1/system.d/bluetooth-hid-agent.conf

%files ipsp
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/bluetooth-ipsp-agent
%{_datadir}/dbus-1/system-services/org.bluez.ipsp_agent.service
%{_sysconfdir}/dbus-1/system.d/bluetooth-ipsp-agent.conf

%files tool
%{_bindir}/hf-test
