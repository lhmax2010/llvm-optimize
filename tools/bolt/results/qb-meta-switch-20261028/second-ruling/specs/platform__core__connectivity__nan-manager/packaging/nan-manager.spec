%bcond_without hal_plugin_bcm

Name:		nan-manager
Summary:	NAN (Neighbor Awareness Networking) manager (Wi-Fi Aware)
Version:	0.2.2
Release:	1
Group:		Network & Connectivity
License:	Apache-2.0
Source0:	%{name}-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:	python3-setuptools
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(dlog)
BuildRequires:	pkgconfig(libtzplatform-config)
#%if %{with hal_plugin_bcm}
#Requires:  pkgconfig(wifi-hal-bcm)
#%endif


%if 0%{?gtests:1}
BuildRequires:	pkgconfig(gmock)
%endif


%description
NAN (Neighbor Awareness Networking) manager to manage NAN cluster, NAN discovery and data path.


%prep
%setup -q
chmod 644 %{SOURCE0}

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
cp resources/dbus/net.nan.service %{buildroot}%{_datadir}/dbus-1/system-services/
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d/
cp resources/dbus/dbus-nan-manager.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/nan-manager.conf
mkdir -p %{buildroot}%{_unitdir}
cp resources/systemd/nan-manager.service %{buildroot}%{_unitdir}


%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,network_fw,network_fw,-)
%attr(500,network_fw,network_fw) %{_bindir}/*
%if 0%{?gtests:1}
	%{_bindir}/gtest-asp-manager
%endif
%attr(644,root,root) %{_sysconfdir}/dbus-1/system.d/nan-manager.conf
%attr(644,root,root) %{_datadir}/dbus-1/system-services/net.nan.service
%attr(644,root,root) %{_unitdir}/nan-manager.service
