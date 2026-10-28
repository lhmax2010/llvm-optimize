%if "%{_with_da_profile}" == "1"
%define WITH_DA 1
%else
%define WITH_DA 0
%endif

%if "%{tizen_profile_name}" == "tv"
%define WITH_VD 1
%else
%define WITH_VD 0
%endif

%if "%{mv_prj}" == "1"
%define WITH_VD_MV 1
%else
%define WITH_VD_MV 0
%endif

%define enable_system_server 0

Name:       sensord
Summary:    Sensor daemon
Version:    10.0.0
Release:    1
Group:      System/Sensor Framework
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    sensord.service
Source2:    sensord.socket

BuildRequires:  cmake
BuildRequires:  libattr-devel
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libsyscommon)
BuildRequires:  pkgconfig(cynara-creds-socket)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-session)
BuildRequires:  pkgconfig(hal-api-sensor)
BuildRequires:  pkgconfig(hal-api-common)
%if %{enable_system_server}
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(tizen-core)
BuildRequires:  pkgconfig(united-service)
%endif

Provides:   %{name}-profile_mobile = %{version}-%{release}
Provides:   %{name}-profile_wearable = %{version}-%{release}
Provides:   %{name}-profile_ivi = %{version}-%{release}
Provides:   %{name}-profile_common = %{version}-%{release}
%global __provides_exclude ^.*-genuine\\.so.*$

%description
This package provides the fully functional internal API library and the service daemon
of the Sensor Framework. The library replaces the dummy library installed by %{name}-dummy.


%package    dummy
Summary:    Sensor Framework 'dummy' library
Provides:   %{name}-profile_tv = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
# To support old-snapshot-based package builds
Provides:   libsensor.so.2


%description dummy
This package provides the dummy library of the sensor internal API.
Installing %{name} replaces this dummy library with the actually functional library.


%package    devel
Summary:    Internal Sensor API (Development)
Group:      System/Development
Requires:   %{name} = %{version}-%{release}
# To support old-snapshot-based package builds
#Provides:   libsensord-devel

%description devel
Internal Sensor API (Development)

%package -n sensor-test
Summary:    Sensord library
Group:      System/Testing

%description -n sensor-test
Sensor functional testing

%isu_package

%prep
%setup -q

%build
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%cmake . \
	-DMAJORVER=${MAJORVER} \
	-DFULLVER=%{version} \
	-DCMAKE_HAL_LIBDIR_PREFIX=%{_hal_libdir} \
%if %{enable_system_server}
	-DSYSTEM_SERVER_DIR=%{_system_server_dir} \
%endif
	-DENABLE_SYSTEM_SERVER=%{enable_system_server}
make %{?_smp_mflags}

%install
%make_install

mkdir -p %{buildroot}%{_unitdir}

%if "%{enable_system_server}" != "1"
install -m 0644 %SOURCE1 %{buildroot}%{_unitdir}
%install_service multi-user.target.wants sensord.service
%else
install -m 0644 system-server/systemd/sensord.service %{buildroot}%{_unitdir}
%endif

install -m 0644 %SOURCE2 %{buildroot}%{_unitdir}
%install_service sockets.target.wants sensord.socket
mkdir -p %{buildroot}%{_sysconfdir}/sensord
install -m 644 conf/auto_rotation.conf   %{buildroot}/etc/sensord/auto_rotation.conf

ln -s libsensor.so.%{version} %{buildroot}/%{_libdir}/libsensor.so.2
ln -s libsensor.so.%{version} %{buildroot}/%{_libdir}/libsensor.so.1

%post
pushd %{_libdir}
chsmack -a "_" libsensor.so.%{version}
popd
/sbin/ldconfig

%preun
echo "You need to reinstall %{name}-dummy to keep using the APIs after uninstalling this."

%files
%manifest packaging/sensord.manifest
%{_libdir}/libsensor.so.*
%{_libdir}/libsensord-shared.so
%{_libdir}/sensor/fusion/libsensor-fusion.so
%{_libdir}/sensor/physical/libsensor-physical.so
%if %{enable_system_server}
%{_system_server_dir}/mod/libsystem-server-sensord.so
%{_system_server_dir}/conf/system-server-sensord.service
%else
%{_bindir}/sensord
%{_unitdir}/multi-user.target.wants/sensord.service
%endif
%{_unitdir}/sensord.socket
%{_unitdir}/sockets.target.wants/sensord.socket
%{_unitdir}/sensord.service
%config %{_sysconfdir}/sensord/auto_rotation.conf
%license LICENSE.APLv2


%post   dummy
pushd %{_libdir}
ln -sf libsensor-dummy.so libsensor.so.%{version}
chsmack -a "_" libsensor.so.%{version}
popd
# Remove sensord files
rm -f %{_libdir}/libsensord-shared.so
rm -f %{_libdir}/sensor/fusion/libsensor-fusion.so
rm -f %{_libdir}/sensor/physical/libsensor-physical.so
rm -f %{_bindir}/sensord
rm -f %{_unitdir}/sensord.service
rm -f %{_unitdir}/sensord.socket
rm -f %{_unitdir}/multi-user.target.wants/sensord.service
rm -f %{_unitdir}/sockets.target.wants/sensord.socket
/sbin/ldconfig


%files  dummy
%manifest packaging/sensord.manifest
%{_libdir}/libsensor-dummy.so
%license LICENSE.APLv2


%files  devel
%manifest packaging/sensord.manifest
%{_includedir}/sensor/*.h
%{_libdir}/libsensor.so
%{_libdir}/pkgconfig/sensor.pc


%files -n sensor-test
%{_bindir}/sensorctl
%{_bindir}/sensord-ondemand-test
%{_bindir}/run_ondemand_test.sh


# Dummy packages for Tizen 3.0.
# When building other packages on Tizen 3.0, after building sensord first,
# some dependency conflicts may occur. These dummy packages may fix such
# dependency issues.
%package -n libsensord
Summary:    Dummy libsensord
Requires:   sensord-dummy
Group:      System/Sensor Framework

%description -n libsensord
Dummy libsensord

%files -n libsensord

%package -n libsensord-devel
Summary:    Dummy libsensord-devel
Requires:   sensord-devel
Group:      System/Sensor Framework

%description -n libsensord-devel
Dummy libsensord-devel

%files -n libsensord-devel
