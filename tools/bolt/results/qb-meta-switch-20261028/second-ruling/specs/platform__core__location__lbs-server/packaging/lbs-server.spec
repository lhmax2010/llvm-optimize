Name:    lbs-server
Summary: LBS Server for Tizen
Version: 1.3.8
Release: 1
Group:   Location/Service
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz
Source1: lbs-server.service
Source2: lbs-server.manifest
Source3: location-lbs-server.manifest
Source4: lbs-server.asan.conf
BuildRequires: cmake
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(tapi)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(lbs-location)
BuildRequires: pkgconfig(lbs-dbus)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(capi-network-wifi-manager)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(vconf-internal-keys)
BuildRequires: pkgconfig(gthread-2.0)
BuildRequires: pkgconfig(gmodule-2.0)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(capi-network-connection)
BuildRequires:  pkgconfig(hal-api-common)
BuildRequires:  pkgconfig(hal-api-location)
BuildRequires:	pkgconfig(gmock)
BuildRequires:	pkgconfig(deviced)

%description
LBS Server for Tizen
LBS Server provides geographical location information


%package -n location-lbs-server
Summary:    Client of LBS Server for Tizen
Group:      Location/Libraries
Requires:   %{name} = %{version}-%{release}

%description -n location-lbs-server
Client of LBS Server for Tizen
This package provides geographical location information received from LBS Server


%package -n lbs-server-plugin-devel
Summary:    LBS Server plugin for Tizen (Development)
Group:      Location/Development
Requires:   %{name} = %{version}-%{release}

%description -n lbs-server-plugin-devel
LBS Server plugin for Tizen (Development)
This package provides header files and pkgconfig file for LBS Server plugin

%package -n location-haltests
Summary:        Location HAL(Hardware Abstraction Layer) Test Cases
Requires:       %{name} = %{version}-%{release}

%description -n location-haltests
Location HAL(Hardware Abstraction Layer) Test Cases

%prep
%setup -q
cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .
cp %{SOURCE4} .


%build
%define _prefix /usr

%ifarch %arm aarch64
export CFLAGS="$CFLAGS -DTIZEN_DEVICE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEVICE"
export FFLAGS="$FFLAGS -DTIZEN_DEVICE"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \
        -DLIB_DIR=%{_libdir} -DINCLUDE_DIR=%{_includedir} -DSYSCONF_DIR=%{_sysconfdir} \

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}%{TZ_SYS_SHARE}/location
mkdir -p %{buildroot}%{TZ_SYS_SHARE}/location/nmea

mkdir -p %{buildroot}%{_unitdir}/delayed.target.wants
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/lbs-server.service
%install_service delayed.target.wants lbs-server.service
%if "%{asan}" == "1"
mkdir -p %{buildroot}%{_unitdir}/lbs-server.service.d
install -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/lbs-server.service.d/lbs-server.asan.conf
%endif

chmod 755 %{buildroot}/etc/rc.d/init.d/lbs-server
mkdir -p %{buildroot}/etc/rc.d/rc5.d
ln -sf ../init.d/lbs-server %{buildroot}/etc/rc.d/rc5.d/S90lbs-server

%define GPS_DUMP_DIR /opt/etc/dump.d/module.d

mkdir -p %{buildroot}/%{GPS_DUMP_DIR}
cp -a lbs-server/script/dump_gps.sh %{buildroot}/%{GPS_DUMP_DIR}/dump_gps.sh


%clean
rm -rf %{buildroot}


%post


%post -n location-lbs-server


%postun -p /sbin/ldconfig

%files
%manifest lbs-server.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_bindir}/lbs-server
/usr/share/dbus-1/system-services/org.tizen.lbs.Providers.LbsServer.service
%config %{_sysconfdir}/dbus-1/system.d/lbs-server.conf
/etc/rc.d/init.d/lbs-server
/etc/rc.d/rc5.d/S90lbs-server
%{_unitdir}/lbs-server.service
%{_unitdir}/delayed.target.wants/lbs-server.service
%if "%{asan}" == "1"
%{_unitdir}/lbs-server.service.d/lbs-server.asan.conf
%endif
/opt/etc/dump.d/module.d/dump_gps.sh

%defattr(-,location,location,-)
%{TZ_SYS_SHARE}/location/nmea

%files -n location-lbs-server
%manifest location-lbs-server.manifest
%license LICENSE
%{_libdir}/location/module/libgps.so*
%{_libdir}/location/module/libwps.so*
%{_libdir}/location/module/libpassive.so*
%{_libdir}/location/module/libfused.so*

%files -n lbs-server-plugin-devel
%{_libdir}/pkgconfig/lbs-server-plugin.pc
%{_includedir}/lbs-server-plugin/*.h

%files -n location-haltests
%manifest %{name}.manifest
%{_bindir}/hal/location-haltests
