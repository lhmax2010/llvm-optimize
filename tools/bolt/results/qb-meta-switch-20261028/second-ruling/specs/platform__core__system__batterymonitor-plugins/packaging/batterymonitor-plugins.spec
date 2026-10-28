Name:       batterymonitor-plugins
Summary:    Battery-Monitor plugins
Version:    0.1
Release:    1
Group:      Service/Battery
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(lbs-dbus)

Requires(post):  /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

%define BATTERY_MONITOR_LIBDIR %{_libdir}/batterymonitor/plugins

%description
Battery-Monitor plugins

%package cpu
Summary:  Battery-Monitor CPU plugin
BuildRequires:  pkgconfig(capi-appfw-app-manager)
BuildRequires:  pkgconfig(capi-system-runtime-info)
BuildRequires:  pkgconfig(sqlite3)

%description cpu
CPU plugin for Battery-Monitor

%package display
Summary: Battery-Monitor display plugin

%description display
Display plugin for Battery-Monitor

%package wifi
Summary:  Battery-Monitor device network plugin

%description wifi
Device network plugin for Battery-Monitor

%package device-network
Summary:  Battery-Monitor device network plugin

%description device-network
Device network plugin for Battery-Monitor

%package bluetooth
Summary:  Battery-Monitor device bluetooth plugin
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(capi-network-bluetooth)

%description bluetooth
Battery-Monitor bt plugin

%package gps
Summary: Battery-Monitor GPS plugin
BuildRequires: pkgconfig(capi-location-manager)

%description gps
GPS plugin for Battery-Monitor

%prep
%setup -q
cp %{SOURCE1001} .

%build
CFLAGS=$(echo $CFLAGS | sed 's/-O2/-O0/' | sed 's/-O1/-O0/' | sed 's/-Wp,-D_FORTIFY_SOURCE=2//')
CXXFLAGS=$(echo $CXXFLAGS | sed 's/-O2/-O0/' | sed 's/-O1/-O0/' | sed 's/-Wp,-D_FORTIFY_SOURCE=2//')
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
cmake .	\
	-DFULLVER=%{version}	\
	-DMAJORVER=${MAJORVER}	\
	-DBATTERY_MONITOR_LIBDIR=%{BATTERY_MONITOR_LIBDIR}

make %{?jobs:-j%jobs}

%install
mkdir -p %{buildroot}%{BATTERY_MONITOR_LIBDIR}
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files cpu
%manifest %{name}.manifest
%license LICENSE
%{BATTERY_MONITOR_LIBDIR}/lib%{name}-cpu*

%files display
%manifest %{name}.manifest
%license LICENSE
%{BATTERY_MONITOR_LIBDIR}/lib%{name}-display*

%files wifi
%manifest %{name}.manifest
%license LICENSE
%{BATTERY_MONITOR_LIBDIR}/lib%{name}-wifi*

%files device-network
%manifest %{name}.manifest
%license LICENSE
%{BATTERY_MONITOR_LIBDIR}/lib%{name}-device-network*

%files bluetooth
%manifest %{name}.manifest
%license LICENSE
%{BATTERY_MONITOR_LIBDIR}/lib%{name}-bluetooth*

%files gps
%manifest %{name}.manifest
%license LICENSE
%{BATTERY_MONITOR_LIBDIR}/lib%{name}-gps*
