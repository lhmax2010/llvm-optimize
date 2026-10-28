%define name		hal-api-common
%define devel_name	hal-api-common-devel
%define test_name	hal-api-common-haltests

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

%if "%{_with_da_profile}" == "1"
%define WITH_DA 1
%else
%define WITH_DA 0
%endif

%if "%{WITH_VD}" != "1" && "%{WITH_VD_MV}" != "1"
%define enable_halcc 1
%define enable_hal_backend_service 1
%else
%define enable_halcc 0
%define enable_hal_backend_service 0
%endif

### main package #########
Name:       %{name}
Summary:    %{name} interface
Version:    2.0.0
Release:    2
Group:      Development/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
Source2:    libhal-api.conf
Source3:    systemd-hal-firmware-generator
Source5:    macros.hal-api
Source6:    haltest.target
Source7:    reboot-haltest
Source8:    reboot-normal

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: cmake
BuildRequires: python3
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(gmock)
BuildRequires: pkgconfig(systemd)
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(rpc-port)
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(tizen-core)

%description
%{name} interface

### devel package #########
%package -n	%{devel_name}
Summary:	%{name} interface
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n	%{devel_name}
%{name} Interface for product vendor developer

### test package #########
%package -n %{test_name}
Summary: tests for hal-api-common
Requires: hal-api-common = %{version}

%description -n %{test_name}
Haltests for hal-api-common

### build and install #########
%prep
%setup -q

%define halcc_default_compatibility_cache_directory		/opt/etc/hal
%define halcc_default_compatibility_cache_file			/opt/etc/hal/.hal-compatibility-cache
%define halcc_default_compatibility_cache_initialized_file	/opt/etc/hal/.hal-compatibility-cache-initialized

%if %{enable_hal_backend_service}
	# Use different json config file depending on the build profile
	%define hal_backend_service_config "hal-backend-service-config.json"

	%if "%{WITH_DA}" == "1"
		%define hal_backend_service_config "hal-backend-service-config-da.json"
	%endif

	%if "%{WITH_VD}" == "1" || "%{WITH_VD_MV}" == "1"
		%define hal_backend_service_config "hal-backend-service-config-vd.json"
	%endif

	hal-backend-service/hal-backend-service-generator.py \
		--enable \
		--config=%{hal_backend_service_config}
%else
	hal-backend-service/hal-backend-service-generator.py --disable
%endif

cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_LIBDIR_PREFIX=%{_libdir} \
	-DENABLE_HALCC=%{enable_halcc} \
	-DHALCC_DEFAULT_COMPATIBILITY_CACHE_DIRECTORY=%{halcc_default_compatibility_cache_directory} \
	-DHALCC_DEFAULT_COMPATIBILITY_CACHE_FILE=%{halcc_default_compatibility_cache_file} \
	-DHALCC_DEFAULT_COMPATIBILITY_CACHE_INITIALIZED_FILE=%{halcc_default_compatibility_cache_initialized_file} \
	-DHALCC_SYSTEMD_UNIT_INSTALL_DIR=%{_unitdir} \
	-DHALCC_SYSTEMD_TMPFILES_CONF_INSTALL_DIR=%{_tmpfilesdir} \
	-DHALCC_UPGRADE_SCRIPTS_INSTALL_DIR=%{_datadir}/upgrade/scripts \
	-DENABLE_HAL_BACKEND_SERVICE=%{enable_hal_backend_service} \
	-DENABLE_DLOG=1

%build
cp %{SOURCE1} .
make %{?jobs:-j%jobs}

%check
(cd tests/unittest && LD_LIBRARY_PATH=../../ ctest -V)

%install
rm -rf %{buildroot}
%make_install

%if %{enable_halcc}
mkdir -p %{buildroot}%{_unitdir}
%endif

mkdir -p %{buildroot}/hal
install -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/ld.so.conf.d/libhal-api.conf
install -D -m 0755 %{SOURCE3} %{buildroot}%{_systemdgeneratordir}/systemd-hal-firmware-generator
install -D -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/rpm/macros.hal-api
install -D -m 0644 %{SOURCE6} %{buildroot}%{_unitdir}/haltest.target
install -D -m 0755 %{SOURCE7} %{buildroot}%{_bindir}/reboot-haltest
install -D -m 0755 %{SOURCE8} %{buildroot}%{_bindir}/reboot-normal

%if %{enable_hal_backend_service}

for HAL_BACKEND_SERVICE_SERVICE in $(ls hal-backend-service/hal-backend-service*.service); do
HAL_BACKEND_SERVICE_SERVICE=$(basename ${HAL_BACKEND_SERVICE_SERVICE})
%install_service basic.target.wants ${HAL_BACKEND_SERVICE_SERVICE}
done

for HAL_BACKEND_SERVICE_SOCKET in $(ls hal-backend-service/hal-backend-service*.socket); do
HAL_BACKEND_SERVICE_SOCKET=$(basename ${HAL_BACKEND_SERVICE_SOCKET})
%install_service sockets.target.wants ${HAL_BACKEND_SERVICE_SOCKET}
done

%endif

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
ln -sf %{_unitdir}/hal-compatibility-checker.service %{_unitdir}/sysinit.target.wants/
%{_bindir}/lshal --reset

%postun
/sbin/ldconfig
rm -f %{_unitdir}/sysinit.target.wants/hal-compatibility-checker.service

### contain files to package #########
%files	-n %{name}
%license LICENSE
%manifest %{name}.manifest
%defattr(-,root,root,-)
%dir /hal
%{_libdir}/hal/*.so*
%{_bindir}/lshal
%{_sysconfdir}/ld.so.conf.d/libhal-api.conf
%{_systemdgeneratordir}/systemd-hal-firmware-generator
%if %{enable_halcc}
%{_bindir}/hal-compatibility-checker
%{_unitdir}/hal-compatibility-checker.service
%{_tmpfilesdir}/hal-compatibility-checker.conf
%endif
%{_datadir}/upgrade/scripts/500.%{name}.sh
%if %{enable_hal_backend_service}
%{_bindir}/hal/hal-backend-service
%{_unitdir}/sockets.target.wants/hal-backend-service*.socket
%{_unitdir}/basic.target.wants/hal-backend-service*.service
%{_unitdir}/hal-backend-service*.socket
%{_unitdir}/hal-backend-service*.service
%endif

%files	-n %{devel_name}
%defattr(-,root,root,-)
%{_includedir}/hal/*.h
%{_libdir}/pkgconfig/*.pc
%{_sysconfdir}/rpm/macros.hal-api

%files -n %{test_name}
%{_unitdir}/haltest.target
%{_bindir}/reboot-haltest
%{_bindir}/reboot-normal
