Name:       libcynara-creds-dbus
Summary:    Cynara credentials helpers library for dbus clients
Version:    0.27.0
Release:    1
Group:      Security/Application Privilege
License:    Apache-2.0 or MIT
Source0:    cynara-%{version}.tar.gz
Source1000:    %{name}-rpmlintrc
Source1008:    libcynara-creds-dbus.manifest
Source1009:    libcynara-creds-gdbus.manifest
Source1010:    libcynara-creds-sd-bus.manifest
Requires:      default-ac-domains
Requires:      libcynara-commons = %{version}
Requires:      dbus
Requires:      libcynara-creds-commons = %{version}
Requires:      libcynara-uid-creds = %{version}
Requires(pre): cynara-db-migration >= %{version}
Requires(postun): cynara-db-migration >= %{version}
BuildRequires: cmake
BuildRequires: zip
BuildRequires: pkgconfig(cynara-creds-commons)
BuildRequires: pkgconfig(cynara-uid-creds)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(dbus-1)

# alternatives: DLOG, JOURNAL, NONE, (otherwise SYSLOG is used)
%if !%{defined log_type}
%define log_type "DLOG"
%endif

%global project_name cynara

%if !%{defined build_type}
%define build_type RELEASE
%endif

%package -n libcynara-creds-dbus-devel
Summary:    Development files for dbus helpers library
Requires:   cynara-devel = %{version}
Requires:   libcynara-creds-dbus = %{version}
Requires:   pkgconfig(dbus-1)

%description -n libcynara-creds-dbus-devel
Development files for dbus helpers library

%package -n libcynara-creds-gdbus-devel
Summary:    Development files for gdbus helpers library
Requires:   cynara-devel = %{version}
Requires:   libcynara-creds-gdbus = %{version}
Requires:   pkgconfig(glib-2.0)

%description -n libcynara-creds-gdbus-devel
Development files for gdbus helpers library

%description -n libcynara-creds-dbus
Cynara credentials helpers library for dbus clients

%package -n libcynara-creds-gdbus
Summary:    Cynara credentials helpers library for gdbus client
BuildRequires: pkgconfig(gio-2.0)
Requires:   libcynara-creds-commons = %{version}
Requires:   libcynara-uid-creds = %{version}

%description -n libcynara-creds-gdbus
Cynara credentials helpers library for gdbus clients

%package -n libcynara-creds-sd-bus-devel
Summary:    Development files for sd-bus helpers library
Requires:   cynara-devel = %{version}
Requires:   libcynara-creds-sd-bus = %{version}
Requires:   pkgconfig(libsystemd)

%description -n libcynara-creds-sd-bus-devel
Development files for sd-bus helpers library

%package -n libcynara-creds-sd-bus
Summary:    Cynara credentials helpers library for sd-bus client
BuildRequires: pkgconfig(libsystemd)
Requires:   libcynara-creds-commons = %{version}
Requires:   libcynara-uid-creds = %{version}

%description -n libcynara-creds-sd-bus
Cynara credentials helpers library for sd-bus clients

%prep
%setup -q -n cynara-%{version}
cp -a %{SOURCE1008} .
cp -a %{SOURCE1009} .
cp -a %{SOURCE1010} .

%build
export CXXFLAGS+=" -Wl,-z,relro,-z,now"

%if %{?build_type} == "DEBUG"|| %{?build_type} == "COVERAGE"
export CXXFLAGS+=" -Wp,-U_FORTIFY_SOURCE"
%endif

export LDFLAGS+=" -Wl,--rpath=%{_libdir}"

%cmake . \
        -DBUILD_TESTS=OFF \
        -DLOG_TYPE=%{log_type} \
        -DCMAKE_BUILD_TYPE=%{?build_type} \
        -DCMAKE_VERBOSE_MAKEFILE=ON \
        -DLIB_DIR:PATH=%{_libdir} \
        -DBIN_DIR:PATH=%{_bindir} \
        -DSBIN_DIR:PATH=%{_sbindir} \
        -DSYS_CONFIG_DIR:PATH=%{_sysconfdir} \
        -DINCLUDE_DIR:PATH=%{_includedir} \
        -DLOCAL_STATE_DIR:PATH=%{_localstatedir} \
        -DDATA_ROOT_DIR:PATH=%{_datadir} \
        -DSYSTEMD_UNIT_DIR:PATH=%{_unitdir} \
        -DSOCKET_DIR:PATH=/run/%{project_name} \
%if "%{?dev_wos}" != "1"
        -DSMACK_ENABLED="ON" \
%endif
%if "%{?dev_wos}" == "1" || "%{?uid_app_sandboxing}" == "1"
        -DUID_SANDBOXING_ENABLED="ON" \
%endif
        -DMONITORING=ON
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%post -n libcynara-creds-dbus -p /sbin/ldconfig

%postun -n libcynara-creds-dbus -p /sbin/ldconfig

%post -n libcynara-creds-gdbus -p /sbin/ldconfig

%postun -n libcynara-creds-gdbus -p /sbin/ldconfig

%files -n libcynara-creds-dbus-devel
%license LICENSE LICENSE.MIT
%{_includedir}/cynara/cynara-creds-dbus.h
%{_libdir}/pkgconfig/cynara-creds-dbus.pc
%{_libdir}/libcynara-creds-dbus.so

%files -n libcynara-creds-gdbus-devel
%license LICENSE LICENSE.MIT
%{_includedir}/cynara/cynara-creds-gdbus.h
%{_libdir}/pkgconfig/cynara-creds-gdbus.pc
%{_libdir}/libcynara-creds-gdbus.so

%files -n libcynara-creds-sd-bus-devel
%license LICENSE LICENSE.MIT
%{_includedir}/cynara/cynara-creds-sd-bus.h
%{_libdir}/pkgconfig/cynara-creds-sd-bus.pc
%{_libdir}/libcynara-creds-sd-bus.so

%files -n libcynara-creds-dbus
%manifest libcynara-creds-dbus.manifest
%license LICENSE LICENSE.MIT
%{_libdir}/libcynara-creds-dbus.so.*

%files -n libcynara-creds-gdbus
%manifest libcynara-creds-gdbus.manifest
%license LICENSE LICENSE.MIT
%{_libdir}/libcynara-creds-gdbus.so.*

%files -n libcynara-creds-sd-bus
%manifest libcynara-creds-sd-bus.manifest
%license LICENSE LICENSE.MIT
%{_libdir}/libcynara-creds-sd-bus.so.*
