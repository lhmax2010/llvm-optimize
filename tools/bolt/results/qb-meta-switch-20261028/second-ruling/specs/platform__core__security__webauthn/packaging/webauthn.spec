%{!?build_type:%global build_type RELEASE}
%if "%{?dev_wos}" != "1" && "%{?uid_app_sandboxing}" != "1"
    %global use_smack 1
%endif

%global version_major   1
%global version_minor   0
%global version_patch   14
%global version_release 1

Name:    webauthn
Summary: Web Authentication Service
Version: %{version_major}.%{version_minor}.%{version_patch}
Release: %{version_release}
Group:   Security/Authentication
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz

Requires:   lib%{name}-common = %{version}-%{release}
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(cynara-client)
BuildRequires: pkgconfig(cynara-creds-socket)

%description
Web Authentication Service

%package -n lib%{name}-common
Summary:    Web Authentication Service (common libraries)
Group:      Security/Libraries
License:    Apache-2.0
BuildRequires: pkgconfig(capi-base-common)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n lib%{name}-common
Web Authentication Service (common libraries)

%package -n lib%{name}-client
Summary:    Web Authentication Service (client)
Group:      Security/Libraries
License:    Apache-2.0
Requires:   %{name} = %{version}-%{release}
Requires:   lib%{name}-common = %{version}-%{release}
BuildRequires: pkgconfig(capi-system-info)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n lib%{name}-client
Web Authentication Service (client)

%package -n lib%{name}-client-devel
Summary:    Web Authentication Service (development files)
License:    Apache-2.0
Group:      Security/Development
Requires:   %{name} = %{version}-%{release}

%description -n lib%{name}-client-devel
Web Authentication Service (development files)

%package -n %{name}-hal-devel
Summary:    HAL API of Web Authentication Service (development files)
License:    Apache-2.0
Group:      Security/Development

%description -n %{name}-hal-devel
HAL API of Web Authentication Service (development files)

%package unittests
Summary:    Web Authentication Service (unit tests)
License:    Apache-2.0
Group:      Security/Development
BuildRequires: pkgconfig(gtest)
BuildRequires: pkgconfig(cynara-admin)
%if "%{?use_smack}" == "1"
BuildRequires: pkgconfig(libsmack)
%endif
Requires:      %{name} = %{version}-%{release}

%description unittests
Web Authentication Service (unit tests)

# gcov
%if 0%{?gcov:1}
%package gcov
Summary:    %{name} gcov data
BuildRequires: lcov
Requires:   %{name}-unittests = %{version}-%{release}
Requires:   %{name}-debugsource = %{version}-%{release}

%description gcov
Base utils gcov objects
%endif

%define user_name          security_fw
%define group_name         security_fw
%define smack_domain       System
%define bin_dir            %TZ_SYS_BIN
%define rw_share_dir       %TZ_SYS_SHARE
%define service_name       %{name}

%global rw_data_dir /opt/data/
%global bin_dir %{?TZ_SYS_BIN:%TZ_SYS_BIN}%{!?TZ_SYS_BIN:%_bindir}
%global lib_dir %{?TZ_SYS_LIB:%TZ_SYS_LIB}%{!?TZ_SYS_LIB:%_libdir}
%global ro_etc_dir %{?TZ_SYS_RO_ETC:%TZ_SYS_RO_ETC}%{!?TZ_SYS_RO_ETC:/etc}
%global run_dir %{?TZ_SYS_RUN:%TZ_SYS_RUN}%{!?TZ_SYS_RUN:/var/run}

# Macros for plugin SO path
%define plugin_dir                 %{lib_dir}
%define hybrid_plugin_so_name      webauthn_plugin_hybrid.so
%define hybrid_plugin_so_path      %{plugin_dir}/%{hybrid_plugin_so_name}
%define macro_file_path %{ro_etc_dir}/rpm/macros.%{name}

%prep
%setup -q

%global coverage_dir %{_datadir}/%{name}-coverage

%build
%cmake . -DGCOV_BUILD=%{?gcov:1}%{!?gcov:0} \
         -DCOVERAGE_DIR=%{coverage_dir} \
         -DPREFIX=%{_prefix} \
         -DEXEC_PREFIX=%{_exec_prefix} \
         -DINCLUDEDIR=%{_includedir} \
         -DLIB_DIR=%{lib_dir} \
         -DSYSTEMD_UNIT_DIR=%{_unitdir} \
         -DCMAKE_BUILD_TYPE=%{build_type} \
         -DRW_SHARE_DIR=%rw_share_dir \
         -DUSER_NAME=%user_name \
         -DGROUP_NAME=%group_name \
         -DSMACK_DOMAIN=%smack_domain \
         -DSERVICE_NAME=%service_name \
         -DBIN_DIR=%bin_dir \
         -DVERSION_MAJOR=%version_major \
         -DVERSION_MINOR=%version_minor \
         -DVERSION_PATCH=%version_patch \
         -DMANIFESTDIR=%{MANIFESTDIR} \
         -DICONDIR=%{ICONDIR} \
         -DMANTESTBINDIR=%{MANTESTBINDIR} \
%if "%_repository" == "emulator"
         -DEMULATOR_BUILD=1 \
%endif
%if 0%{?no_feature_check:1}
         -DNO_FEATURE_CHECK= \
%endif
%if "%{?use_smack}" == "1"
         -DSMACK_ENABLED=ON \
%endif
         -DHYBRID_PLUGIN_SO_PATH=%{hybrid_plugin_so_path} \

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install
%install_service sockets.target.wants %{name}.socket

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

cat << EOF > run-unittest.sh
#!/bin/sh
setup() {
	echo "setup start"
}

test_main() {
	echo "test_main start"
	/usr/bin/webauthn-unittests
}

teardown() {
	echo "teardown start"
    chown ${user_name}:${group_name} /home/abuild/rpmbuild/BUILD/%{name}-%{version} -R
    /usr/bin/killall %{name}-server
}

main() {
	setup
	test_main
	teardown
}

main "\$*"
EOF

mkdir -p %{buildroot}%{_bindir}/tizen-unittests/%{name}
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/%{name}/

# write macro
mkdir -p %{buildroot}%{ro_etc_dir}/rpm
touch %{buildroot}%{macro_file_path}
echo "%WEBAUTHN_HYBRID_PLUGIN_SO_PATH %{hybrid_plugin_so_path}" >> %{buildroot}%{macro_file_path}

%post
/sbin/ldconfig
systemctl daemon-reload
# Remove any previous multi-user.target.wants symlink to ensure service doesn't start at boot
rm -f %{_unitdir}/multi-user.target.wants/%{name}.service
if [ $1 = 2 ]; then
    # update - stop the service if it's running
    # It will be started on-demand when the socket is activated
    systemctl stop %{name}.service
fi

%postun
/sbin/ldconfig
if [ $1 = 0 ]; then
    # uninstall
    systemctl daemon-reload
fi

%post -n lib%{name}-common -p /sbin/ldconfig
%post -n lib%{name}-client -p /sbin/ldconfig
%postun -n lib%{name}-common -p /sbin/ldconfig
%postun -n lib%{name}-client -p /sbin/ldconfig

%files
%manifest %{name}-server.manifest
%license LICENSE
%{bin_dir}/%{name}-server
%{_unitdir}/%{name}.service
%{_unitdir}/sockets.target.wants/%{name}.socket
%{_unitdir}/%{name}.socket

%files -n lib%{name}-common
%manifest %{name}-common.manifest
%license LICENSE
%{lib_dir}/lib%{name}-common.so.*

%files -n lib%{name}-client
%manifest %{name}-client.manifest
%license LICENSE
%{lib_dir}/lib%{name}-client.so.*

%files -n lib%{name}-client-devel
%license LICENSE
%{_includedir}/webauthn.h
%{_includedir}/webauthn-types.h
%{lib_dir}/pkgconfig/%{name}.pc
%{lib_dir}/lib*.so

%files -n %{name}-hal-devel
%license LICENSE
%config %{macro_file_path}
%{_includedir}/webauthn*.h
%{lib_dir}/pkgconfig/%{name}-hal.pc

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%{_bindir}/%{name}-coverage.sh
%coverage_dir
%endif

%files -n %{name}-unittests
%manifest %{name}-unittests.manifest
%license LICENSE
%{bin_dir}/%{name}-unittests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

