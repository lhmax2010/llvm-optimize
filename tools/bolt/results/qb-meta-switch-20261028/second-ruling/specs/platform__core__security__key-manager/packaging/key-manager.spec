%global watchdog_enabled 1
%global watchdog_timeout_sec 60
%global watchdog_notify_sec  20
%{!?build_type:%global build_type RELEASE}
%if "%{?dev_wos}" != "1" && "%{?uid_app_sandboxing}" != "1"
    %global use_smack 1
%endif

Name:       key-manager
Summary:    Central Key Manager and utilities
Version:    0.2.2
Release:    1
Group:      Security/Secure Storage
License:    Apache-2.0 and BSD-3-Clause
Source0:    %{name}-%{version}.tar.gz
Source1001: key-manager-pam-plugin.manifest
Source1002: libkey-manager-client.manifest
Source1003: libkey-manager-client-devel.manifest
Source1004: libkey-manager-common.manifest
BuildRequires: cmake
BuildRequires: zip
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(openssl3)
BuildRequires: libattr-devel
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(security-manager)
BuildRequires: pkgconfig(cynara-client-async)
BuildRequires: pkgconfig(cynara-creds-socket)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(pkgmgr)
BuildRequires: pkgconfig(pkgmgr-info)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(sqlcipher)
%if 0%{?watchdog_enabled}
BuildRequires: pkgconfig(argos_watchdog)
%endif
BuildRequires: boost-devel
BuildRequires: ca-certificates-devel
BuildRequires: pkgconfig(hal-api-security)
Requires: libkey-manager-common = %{version}-%{release}
%if "%{build_type}" == "COVERAGE"
BuildRequires: lcov
%endif
BuildRequires: pkgconfig(capi-system-resource)
BuildRequires: liboqs
%if "%{?use_smack}" == "1"
Requires:      smack
%endif

%{?systemd_requires}

%global user_name key-manager
%global group_name security_fw
%global supplementary_group_names key-manager
%global service_name key-manager
%global smack_domain_name System
%global old_rw_data_dir /opt/data/ckm
%global rw_data_dir %{?TZ_SYS_DATA:%TZ_SYS_DATA/ckm}%{!?TZ_SYS_DATA:%old_rw_data_dir}
%global ro_data_dir %{?TZ_SYS_RO_SHARE:%TZ_SYS_RO_SHARE/ckm}%{!?TZ_SYS_RO_SHARE:%_datadir/ckm}
%global unit_tests_dir %{?TZ_SYS_DATA:%TZ_SYS_DATA/ckm-unit-tests}%{!?TZ_SYS_DATA:%/opt/data/ckm-unit-tests}
%global misc_dir %{?TZ_SYS_DATA:%TZ_SYS_DATA/ckm-misc}%{!?TZ_SYS_DATA:%/opt/data/ckm-misc}
%global coverage_dir %{?TZ_SYS_DATA:%TZ_SYS_DATA/ckm-coverage}%{!?TZ_SYS_DATA:%/opt/data/ckm-coverage}
%global bin_dir %{?TZ_SYS_BIN:%TZ_SYS_BIN}%{!?TZ_SYS_BIN:%_bindir}
%global ro_etc_dir %{?TZ_SYS_RO_ETC:%TZ_SYS_RO_ETC}%{!?TZ_SYS_RO_ETC:/etc}
%global run_dir %{?TZ_SYS_RUN:%TZ_SYS_RUN}%{!?TZ_SYS_RUN:/var/run}
%global initial_values_dir_ro %{ro_data_dir}/initial_values
%global initial_values_dir_rw %{rw_data_dir}/initial_values
%global ca_certs_dir %{?TZ_SYS_CA_CERTS:%TZ_SYS_CA_CERTS}%{!?TZ_SYS_CA_CERTS:%ro_etc_dir/ssl/certs}
%global dump_legacy_db_libname key-manager-dump-legacy-database

%description
Central Key Manager daemon could be used as secure storage
for certificate and private/public keys. It gives API for
application to sign and verify (DSA/RSA/ECDSA) signatures.

%package -n libkey-manager-common
Summary:    Central Key Manager (common libraries)
Group:      Security/Libraries
License:    Apache-2.0
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n libkey-manager-common
Central Key Manager package (common library)

%package -n libkey-manager-client
Summary:    Central Key Manager (client)
Group:      Security/Libraries
License:    Apache-2.0
Requires:   key-manager = %{version}-%{release}
Requires:   libkey-manager-common = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n libkey-manager-client
Central Key Manager package (client)

%package -n libkey-manager-client-devel
Summary:    Central Key Manager (client-devel)
Group:      Security/Development
License:    Apache-2.0
BuildRequires: pkgconfig(capi-base-common)
Requires:   pkgconfig(capi-base-common)
Requires:   libkey-manager-client = %{version}-%{release}

%description -n libkey-manager-client-devel
Central Key Manager package (client-devel)

%package -n key-manager-unit-tests
Summary:    Unit tests for key-manager
Group:      Security/Testing
License:    Apache-2.0 and BSL-1.0
BuildRequires: pkgconfig(libxml-2.0)
Requires:   boost-test

%description -n key-manager-unit-tests
Unit tests for key-manager.

%package -n key-manager-misc
Summary:    Miscellaneous tools and tests for key-manager
Group:      Security/Testing
License:    Apache-2.0 and BSL-1.0
Requires:   boost-test
Requires:   key-manager = %{version}-%{release}
%if "%{?use_smack}" == "1"
BuildRequires: pkgconfig(libsmack)
%endif


%description -n key-manager-misc
Miscellaneous tools and tests for key-manager.

%package -n key-manager-pam-plugin
Summary:    CKM login/password module to PAM
Group:      Security/Libraries
License:    Apache-2.0
BuildRequires: pam-devel
Requires:   key-manager = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n key-manager-pam-plugin
CKM login/password module to PAM. Used to monitor user login/logout
and password change events from PAM

%package -n key-manager-initial-values
Summary:    CKM initial values tool
Group:      Security/Libraries
License:    Apache-2.0
BuildRequires: cmake
BuildRequires: pkgconfig(openssl3)
BuildRequires: pkgconfig(libxml-2.0)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n key-manager-initial-values
Includes ckm_initial_values tool for initial values XML generation

%if "%{build_type}" == "COVERAGE"

%package -n key-manager-coverage
Summary:    Central Key Manager code coverage data
Group:      Security/Testing
License:    Apache-2.0
Requires:   key-manager-unit-tests = %{version}-%{release}
Requires:   key-manager-debugsource = %{version}-%{release}
Requires:   lcov
Requires:   gcc

%description -n key-manager-coverage
Central Key Manager code coverage data

%endif

%prep
%setup -q

%build
export LDFLAGS="$LDFLAGS -Wl,--rpath=%{_libdir},-Bsymbolic-functions"

%cmake . -DVERSION=%{version} \
        -DCMAKE_BUILD_TYPE=%{build_type} \
        -DCMAKE_VERBOSE_MAKEFILE=ON \
        -DSYSTEMD_UNIT_DIR=%{_unitdir} \
        -DSYSTEMD_ENV_FILE=%{ro_etc_dir}"/sysconfig/central-key-manager" \
        -DRUN_DIR:PATH=%{run_dir} \
        -DSERVICE_NAME=%{service_name} \
        -DUSER_NAME=%{user_name} \
        -DGROUP_NAME=%{group_name} \
        -DSUPPLEMENTARY_GROUP_NAMES="%{supplementary_group_names}" \
        -DSMACK_DOMAIN_NAME=%{smack_domain_name} \
        -DOLD_RW_DATA_DIR=%{old_rw_data_dir} \
        -DRW_DATA_DIR=%{rw_data_dir} \
        -DRO_DATA_DIR=%{ro_data_dir} \
        -DRW_ETC_DIR=%{rw_etc_dir} \
        -DRO_ETC_DIR=%{ro_etc_dir} \
        -DBIN_DIR=%{bin_dir} \
        -DINITIAL_VALUES_DIR_RW=%{initial_values_dir_rw} \
        -DINITIAL_VALUES_DIR_RO=%{initial_values_dir_ro} \
        -DCA_CERTS_DIR=%{ca_certs_dir} \
%if 0%{?watchdog_enabled}
        -DWATCHDOG_ENABLED=%{watchdog_enabled} \
        -DWATCHDOG_TIMEOUT_SEC=%{watchdog_timeout_sec} \
        -DWATCHDOG_NOTIFY_SEC=%{watchdog_notify_sec} \
%endif
        -DUNIT_TESTS_DIR=%{unit_tests_dir} \
        -DMISC_DIR=%{misc_dir} \
        -DCOVERAGE_DIR=%{coverage_dir} \
%if "%{?use_smack}" == "1"
        -DSMACK_ENABLED=ON \
%endif
        -DDUMP_LEGACY_DB_LIBNAME=%{dump_legacy_db_libname}

make %{?jobs:-j%jobs}

%install
%make_install

%install_service multi-user.target.wants central-key-manager.service
%install_service sockets.target.wants central-key-manager-api-control.socket
%install_service sockets.target.wants central-key-manager-api-storage.socket
%install_service sockets.target.wants central-key-manager-api-extended.socket
%install_service sockets.target.wants central-key-manager-api-ocsp.socket
%install_service sockets.target.wants central-key-manager-api-encryption.socket
cp -a %{SOURCE1001} %{SOURCE1002} %{SOURCE1003} %{SOURCE1004} %{buildroot}%{_datadir}/

%pre
# tzplatform-get sync breaked because of on-development situation. comment out just for temporary
# fail if runtime dir variable is different than compilation time variable
#if [ `tzplatform-get TZ_SYS_DATA | cut -d'=' -f2` != %{TZ_SYS_DATA} ]
#then
#    echo "Runtime value of TZ_SYS_DATA is different than the compilation time value. Aborting"
#    exit 1
#fi
#if [ `tzplatform-get TZ_SYS_RO_SHARE | cut -d'=' -f2` != %{TZ_SYS_RO_SHARE} ]
#then
#    echo "Runtime value of TZ_SYS_RO_SHARE is different than the compilation time value. Aborting"
#    exit 1
#fi

## backup plan for manage key-manager user/group is deprecated b/c pwdutils package
## would be excluded from binary
# User/group (key-manager/key-manager) should be already added in passwd package.
# This is our backup plan if passwd package will not be configured correctly.
#id -g %{group_name} > /dev/null 2>&1
#if [ $? -eq 1 ]; then
#    groupadd %{group_name} -r > /dev/null 2>&1
#fi
#
#id -u %{user_name} > /dev/null 2>&1
#if [ $? -eq 1 ]; then
#    useradd -d /var/lib/empty -s /sbin/nologin -r -g %{group_name} %{user_name} > /dev/null 2>&1
#fi

%post
# move data from old path to new one
# we have to assume that in case of TZ_SYS_DATA change some upgrade script will move all the data
if [ -d "%{old_rw_data_dir}" ] && [ "%{rw_data_dir}" != "%{old_rw_data_dir}" ]
then
    echo "Migrating old rw data to new rw data dir"
    cp -a %{old_rw_data_dir}/. %{rw_data_dir}/ && rm -rf %{old_rw_data_dir}
fi

systemctl daemon-reload
if [ $1 = 1 ]; then
    # installation
    systemctl start central-key-manager.service
fi

if [ $1 = 2 ]; then
    # update

    # In ckm version <= 0.1.18 all files were owned by root.
%if "%{?use_smack}" == "1"
    find %{rw_data_dir} -exec chsmack -a %{smack_domain_name} {} \;
%endif
    chown %{user_name}:%{group_name} -R %{rw_data_dir}
    systemctl restart central-key-manager.service
fi


%preun
if [ $1 = 0 ]; then
    # unistall
    systemctl stop central-key-manager.service
fi

%postun
if [ $1 = 0 ]; then
    # unistall
    systemctl daemon-reload
fi

%post -n libkey-manager-common -p /sbin/ldconfig
%post -n libkey-manager-client -p /sbin/ldconfig
%postun -n libkey-manager-common -p /sbin/ldconfig
%postun -n libkey-manager-client -p /sbin/ldconfig

%files -n key-manager
%manifest key-manager.manifest
%license LICENSE
%license LICENSE.BSD-3-Clause
%{bin_dir}/key-manager
%{_libdir}/lib%{dump_legacy_db_libname}.so
%{_unitdir}/multi-user.target.wants/central-key-manager.service
%{_unitdir}/central-key-manager.service
%{_unitdir}/sockets.target.wants/central-key-manager-api-control.socket
%{_unitdir}/central-key-manager-api-control.socket
%{_unitdir}/sockets.target.wants/central-key-manager-api-storage.socket
%{_unitdir}/central-key-manager-api-storage.socket
%{_unitdir}/sockets.target.wants/central-key-manager-api-extended.socket
%{_unitdir}/central-key-manager-api-extended.socket
%{_unitdir}/sockets.target.wants/central-key-manager-api-ocsp.socket
%{_unitdir}/central-key-manager-api-ocsp.socket
%{_unitdir}/sockets.target.wants/central-key-manager-api-encryption.socket
%{_unitdir}/central-key-manager-api-encryption.socket
%dir %{ro_data_dir}
%{ro_data_dir}/*
%dir %attr(770, %{user_name}, %{group_name}) %{rw_data_dir}
%dir %attr(550, %{user_name}, %{group_name}) %{initial_values_dir_ro}
%dir %attr(770, %{user_name}, %{group_name}) %{initial_values_dir_rw}

%{ro_etc_dir}/gumd/userdel.d/10_key-manager.post
%{bin_dir}/ckm_tool

%files -n key-manager-pam-plugin
%manifest %{_datadir}/key-manager-pam-plugin.manifest
%license LICENSE
%{_libdir}/security/pam_key_manager_plugin.so*

%files -n libkey-manager-common
%manifest %{_datadir}/libkey-manager-common.manifest
%license LICENSE
%{_libdir}/libkey-manager-common.so.*

%files -n libkey-manager-client
%manifest %{_datadir}/libkey-manager-client.manifest
%license LICENSE
%{_libdir}/libkey-manager-client.so.*
%{_libdir}/libkey-manager-control-client.so.*

%files -n libkey-manager-client-devel
%manifest %{_datadir}/libkey-manager-client-devel.manifest
%license LICENSE
%{_libdir}/libkey-manager-client.so
%{_libdir}/libkey-manager-control-client.so
%{_libdir}/libkey-manager-common.so
%{_includedir}/ckm/ckm/ckm-manager.h
%{_includedir}/ckm/ckm/ckm-manager-async.h
%{_includedir}/ckm/ckm/ckm-certificate.h
%{_includedir}/ckm/ckm/ckm-control.h
%{_includedir}/ckm/ckm/ckm-error.h
%{_includedir}/ckm/ckm/ckm-key.h
%{_includedir}/ckm/ckm/ckm-password.h
%{_includedir}/ckm/ckm/ckm-pkcs12.h
%{_includedir}/ckm/ckm/ckm-raw-buffer.h
%{_includedir}/ckm/ckm/ckm-type.h
%{_includedir}/ckm/ckm/ckm-zero-memory.h
%{_includedir}/ckm/ckmc/ckmc-manager.h
%{_includedir}/ckm/ckmc/ckmc-control.h
%{_includedir}/ckm/ckmc/ckmc-error.h
%{_includedir}/ckm/ckmc/ckmc-type.h
%{_includedir}/ckm/ckmc/ckmc-extended.h
%{_includedir}/ckm/ckmc/ckmc-attestation.h
%{_libdir}/pkgconfig/*.pc

%files -n key-manager-initial-values
%license LICENSE
%{bin_dir}/ckm_initial_values

%files -n key-manager-misc
%manifest key-manager-misc.manifest
%license LICENSE
%license LICENSE.BSL-1.0
%if "%{?use_smack}" == "1"
    %{bin_dir}/ckm-scheme-test
    %{bin_dir}/ckm_generate_db
    %misc_dir
%endif
%{bin_dir}/ckm_so_loader
%{bin_dir}/ckm_db_tool
%{bin_dir}/ckm_db_merge
%{bin_dir}/ckm_db_perf
%{bin_dir}/ckm_enc_perf
%{bin_dir}/ckm_update_perf

%files -n key-manager-unit-tests
%manifest key-manager-unit-tests.manifest
%license LICENSE
%license LICENSE.BSL-1.0
%{bin_dir}/ckm-unit-tests
%unit_tests_dir

%if "%{build_type}" == "COVERAGE"

%files -n key-manager-coverage
%license LICENSE
%{bin_dir}/key-manager-coverage.sh
%coverage_dir

%endif
