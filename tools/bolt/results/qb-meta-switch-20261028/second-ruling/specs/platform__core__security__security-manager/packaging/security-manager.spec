%{!?build_type:%global build_type RELEASE}

%if "%{?dev_sel}" == "1"
    # we have UID sandboxing and we don't have Smack
    %global dev_wos 1
%endif
%if "%{?dev_wos}" == "1"
    # we do have UID sandboxing for sure
    %global uid_app_sandboxing 1
%endif

Name:       security-manager
Summary:    Security manager and utilities
Version:    2.6.2
Release:    0
Group:      Security/Service
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    security-manager.manifest
Source2:    libsecurity-manager-client.manifest
Source3:    libsecurity-manager-client-devel.manifest
Source4:    libnss-security-manager.manifest
Source5:    security-manager-tests.manifest
Source6:    security-manager-policy.manifest
Source7:    security-license-manager.manifest
Source8:    security-manager-iptables-load.service
Source9:    security-manager-iptables.rules
Source10:   security-manager-ip6tables.rules
Source11:   security-manager-iptables-nosmack.rules
Source12:   security-manager-ip6tables-nosmack.rules
Source13:   711.security-manager-migration-from-product-partition.sh
Requires:   security-manager-policy
Requires:   security-license-manager
Requires:   libnss-security-manager
%if "%{?uid_app_sandboxing}" == "1"
Requires:   security-manager-policy-iptables
%endif
Requires:   libcynara-admin >= 0.24.0
Requires:   libcynara-client >= 0.24.0
Requires:   libcynara-creds-pid >= 0.24.0
Requires:   libcynara-creds-socket >= 0.24.0
Requires:   libcynara-uid >= 0.24.0
Requires:   libcynara-uid-creds >= 0.24.0
%if "%{build_type}" == "VALGRIND"
Requires: valgrind
%endif
Requires(post): sqlite3
BuildRequires: cmake
BuildRequires: zip
BuildRequires: pkgconfig(dlog)
BuildRequires: libattr-devel
BuildRequires: pkgconfig(capi-system-resource)
%if "%{?dev_wos}" != "1"
BuildRequires: pkgconfig(libsmack)
Requires(post): smack
%endif
%if "%{dev_sel}" == "1"
BuildRequires: pkgconfig(libselinux)
Requires(post): libselinux
%endif
BuildRequires: pkgconfig(libcap)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: tizen-platform-config-tools
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(cynara-admin) >= 0.24.0
BuildRequires: pkgconfig(cynara-client) >= 0.24.0
BuildRequires: pkgconfig(cynara-creds-pid) >= 0.24.0
BuildRequires: pkgconfig(cynara-creds-socket) >= 0.24.0
BuildRequires: pkgconfig(cynara-uid) >= 0.24.0
BuildRequires: pkgconfig(cynara-uid-creds) >= 0.24.0
BuildRequires: pkgconfig(security-privilege-manager)
BuildRequires: pkgconfig(mount)
BuildRequires: boost-devel
BuildRequires: pkgconfig(libsessiond)
%if "%{build_type}" == "COVERAGE"
BuildRequires: lcov
%endif
%{?systemd_requires}
BuildRequires: pkgconfig(libacl)

%description
Tizen security manager and utilities

%package -n libsecurity-manager-client
Summary:    Security manager (client)
License:    Apache-2.0
Group:      Security/Libraries
Requires:   security-manager = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n libsecurity-manager-client
Tizen Security manager client library

%package -n libsecurity-manager-client-devel
Summary:    Security manager (client-devel)
License:    Apache-2.0
Group:      Security/Development
Requires:   libsecurity-manager-client = %{version}-%{release}

%description -n libsecurity-manager-client-devel
Development files needed for using the security manager client

%package -n libnss-security-manager
Summary:    Security Manager NSS library
License:    MIT
Group:      Security/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n libnss-security-manager
Tizen Security Manager NSS library

%package policy
Summary:    Security manager policy
License:    Apache-2.0
Group:      Security/Access Control
Requires:   sed
Requires(post): security-manager = %{version}-%{release}
Requires(post): cyad
Requires(post): sqlite
Requires(post): tizen-platform-config-tools
Requires(post): security-config

%description policy
Set of security rules that constitute security policy in the system

%package policy-iptables
Summary:    Security manager iptables policy
License:    Apache-2.0
Group:      Security/Access Control
Requires:   security-manager = %{version}-%{release}
Requires:   iptables

%description policy-iptables
Set of iptables rules governing the internet related priviledges

%package -n security-manager-tests
Summary:    Security manager unit test binaries
License:    Apache-2.0 and BSL-1.0
Group:      Security/Development
Requires:   boost-iostreams
Requires:   boost-test
Requires:   boost-filesystem

%description -n security-manager-tests
Internal test for security manager implementation.

%package -n security-license-manager
Summary:    Plugins for cynara service and client
License:    Apache-2.0
Group:      Security/Development
BuildRequires: pkgconfig(openssl3)
Requires:   cynara

%description -n security-license-manager
Package with plugins for cynara.

%if "%{build_type}" == "COVERAGE"

%package -n security-manager-coverage
Summary:    Security Manager code coverage data
Group:      Security/Testing
Requires:   security-manager-tests = %{version}-%{release}
Requires:   security-manager-debugsource = %{version}-%{release}
Requires:   lcov
Requires:   gcc

%description -n security-manager-coverage
Security Manager code coverage data

%endif

%prep
%setup -q

%build

%{?asan:
export CFLAGS="$CFLAGS -Wno-stringop-overread"
}
export LDFLAGS="$LDFLAGS -Wl,--rpath=%{_libdir}"

%global db_test_dir %{_datadir}/sm-db-test
%global coverage_dir %{_datadir}/security-manager-coverage

%cmake . \
       -DVERSION=%{version} \
       -DBIN_INSTALL_DIR=%{_bindir} \
       -DSYSTEMD_INSTALL_DIR=%{_unitdir} \
       -DLOCAL_STATE_INSTALL_PREFIX=%{TZ_SYS_VAR} \
       -DDB_INSTALL_DIR=%{TZ_SYS_DB} \
       -DDB_TEST_INSTALL_DIR=%{db_test_dir} \
       -DDB_LOGS=OFF \
       -DCMAKE_BUILD_TYPE=%{build_type} \
       -DCMAKE_VERBOSE_MAKEFILE=ON \
%if "%{?dev_wos}" != "1"
       -DSUPPORT_SMACK="ON"\
%endif
%if "%{?dev_sel}" == "1"
       -DSUPPORT_SELINUX="ON"\
%endif
%if "%{?uid_app_sandboxing}" == "1"
       -DSUPPORT_UID_SANDBOXING="ON"\
%endif
       -DCOVERAGE_DIR=%{coverage_dir}
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}/%{_unitdir}/sockets.target.wants
mkdir -p %{buildroot}/%{_unitdir}/basic.target.wants
mkdir -p %{buildroot}/%{_unitdir}/cynara.service.wants
ln -s ../security-manager.socket %{buildroot}/%{_unitdir}/sockets.target.wants/security-manager.socket
ln -s ../security-manager-cleanup.service %{buildroot}/%{_unitdir}/basic.target.wants/security-manager-cleanup.service
ln -s ../security-manager-rules-loader.service %{buildroot}/%{_unitdir}/basic.target.wants/security-manager-rules-loader.service
ln -s ../license-manager-agent.service %{buildroot}/%{_unitdir}/cynara.service.wants/license-manager-agent.service

mkdir -p %{buildroot}/%{TZ_SYS_DB}
touch %{buildroot}/%{TZ_SYS_DB}/.security-manager.db
touch %{buildroot}/%{TZ_SYS_DB}/.security-manager.db-journal

install -m 0755 -d %{buildroot}%{TZ_SYS_VAR}/%{name}
%if "%{?dev_wos}" != "1" && "%{?uid_app_sandboxing}" != "1"
install -m 0444 /dev/null %{buildroot}%{TZ_SYS_VAR}/%{name}/apps-labels
%endif
install -m 0444 /dev/null %{buildroot}%{TZ_SYS_VAR}/%{name}/policy-version

mkdir -p %{buildroot}/%{db_test_dir}
sqlite3 %{buildroot}/%{db_test_dir}/.security-manager-test.db  <  db/db.sql
sqlite3 %{buildroot}/%{db_test_dir}/.security-manager-test-v0.db  <  db/db_test_v0.sql
dd bs=1K count=$(($(stat -c%s %{buildroot}/%{db_test_dir}/.security-manager-test.db) / 1024 - 1)) if=%{buildroot}/%{db_test_dir}/.security-manager-test.db of=%{buildroot}/%{db_test_dir}/.security-manager-test-corrupted.db
cp -a %{buildroot}/%{db_test_dir}/.security-manager-test.db-journal %{buildroot}/%{db_test_dir}/.security-manager-test-corrupted.db-journal
echo -n > %{buildroot}/%{db_test_dir}/.security-manager-test-empty.db
echo -n > %{buildroot}/%{db_test_dir}/.security-manager-test-empty.db-journal
sqlite3 %{buildroot}/%{db_test_dir}/.security-manager-test-wrong-schema.db < db/db.sql
sqlite3 %{buildroot}/%{db_test_dir}/.security-manager-test-wrong-schema.db "drop view client_license_view"
cp -a test/data/.security-manager-test-rules*.db test/data/.security-manager-test-rules*.txt %{buildroot}/%{db_test_dir}

cp -a %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} %{buildroot}%{_datadir}/

install -m 644 %{SOURCE8} %{buildroot}%{_unitdir}/security-manager-iptables.service

%if "%{?dev_wos}" != "1" && "%{?uid_app_sandboxing}" != "1"
install -m 600 %{SOURCE9} %{buildroot}%{_sysconfdir}/security-manager-iptables.rules
install -m 600 %{SOURCE10} %{buildroot}%{_sysconfdir}/security-manager-ip6tables.rules
%else
install -m 600 %{SOURCE11} %{buildroot}%{_sysconfdir}/security-manager-iptables.rules
install -m 600 %{SOURCE12} %{buildroot}%{_sysconfdir}/security-manager-ip6tables.rules
%endif
install -D -m 700 %{SOURCE13} %{buildroot}/usr/share/platform-extension/711.security-manager-migration-from-product-partition.sh

ln -sf ../security-manager-iptables.service %{buildroot}%{_unitdir}/basic.target.wants/

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
systemctl daemon-reload
if [ $1 = 1 ]; then
    # installation
    security-manager-rules-loader --no-load
    systemctl start security-manager.service security-manager.socket
fi

if [ $1 = 2 ]; then
    # update
    systemctl stop security-manager.service security-manager.socket
    security-manager-rules-loader --no-load
    systemctl start security-manager.service security-manager.socket
fi

%if "%{?dev_wos}" != "1"
chsmack -a System %{TZ_SYS_DB}/.security-manager.db
chsmack -a System %{TZ_SYS_DB}/.security-manager.db-journal

chsmack -r -a _ %{TZ_SYS_VAR}/%{name}/
%endif

%preun
if [ $1 = 0 ]; then
    # unistall
    systemctl stop security-manager.service
fi

%postun
/sbin/ldconfig
if [ $1 = 0 ]; then
    # unistall
    systemctl daemon-reload
fi

%post -n libsecurity-manager-client -p /sbin/ldconfig

%postun -n libsecurity-manager-client -p /sbin/ldconfig

%post -n libnss-security-manager -p /sbin/ldconfig

%postun -n libnss-security-manager -p /sbin/ldconfig

%post -n security-license-manager
/sbin/ldconfig
systemctl daemon-reload
if [ $1 = 1 ]; then
    # installation
    systemctl start license-manager-agent.service
fi

if [ $1 = 2 ]; then
    # update
    systemctl restart license-manager-agent.service
fi

%preun -n security-license-manager
if [ $1 = 0 ]; then
    # unistall
    systemctl stop license-manager-agent.service
fi

%postun -n security-license-manager
/sbin/ldconfig
if [ $1 = 0 ]; then
    # unistall
    systemctl daemon-reload
fi

%pre
### Workaround for invalid policy versioning mechanism
if [ -e %{TZ_SYS_VAR}/%{name}/policy-version ] && [ x`cat %{TZ_SYS_VAR}/%{name}/policy-version` = x"1" ]
then
    ### Restart versioning, let the update scripts do their work
    echo 0 >%{TZ_SYS_VAR}/%{name}/policy-version
fi

%post policy
systemctl stop security-manager.service security-manager.socket
%{_datadir}/%{name}/policy/update.sh
%{_datadir}/%{name}/policy/update_group_id_list.sh
%{_bindir}/security-manager-policy-reload
systemctl start security-manager-rules-loader.service
systemctl start security-manager.service security-manager.socket

%post -n security-manager-tests
%if "%{?dev_wos}" != "1"
chsmack -a System %{db_test_dir}/.security-manager-test.db
chsmack -a System %{db_test_dir}/.security-manager-test.db-journal
chsmack -a System %{db_test_dir}/.security-manager-test-v0.db
chsmack -a System %{db_test_dir}/.security-manager-test-v0.db-journal
chsmack -a System %{db_test_dir}/.security-manager-test-corrupted.db
chsmack -a System %{db_test_dir}/.security-manager-test-corrupted.db-journal
chsmack -a System %{db_test_dir}/.security-manager-test-empty.db
chsmack -a System %{db_test_dir}/.security-manager-test-empty.db-journal
chsmack -a System %{db_test_dir}/.security-manager-test-wrong-schema.db
chsmack -a System %{db_test_dir}/.security-manager-test-wrong-schema.db-journal
chsmack -a System %{db_test_dir}/.security-manager-test-rules.db
chsmack -a System %{db_test_dir}/.security-manager-test-rules*.txt
%endif

%files -n security-manager
%manifest %{_datadir}/security-manager.manifest
%license LICENSE
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/security-manager
%attr(755,root,root) %{_bindir}/security-manager-cmd
%attr(755,root,root) %{_bindir}/security-manager-cleanup
%attr(755,root,root) %{_bindir}/security-manager-rules-loader
%attr(755,root,root) %{_bindir}/sm-db-export
%attr(755,root,root) %{_bindir}/sm-db-merge
%attr(755,root,root) %{_sysconfdir}/gumd/useradd.d/50_security-manager-add.post
%if "%{?uid_app_sandboxing}" == "1"
%attr(755,root,root) %{_sysconfdir}/gumd/useradd.d/51_security-manager-register-paths.post
%endif
%attr(755,root,root) %{_sysconfdir}/gumd/userdel.d/50_security-manager-remove.pre
%if "%{?dev_wos}" != "1" && "%{?uid_app_sandboxing}" != "1"
%config(noreplace) %attr(444,root,root) %{TZ_SYS_VAR}/%{name}/apps-labels
%endif
%dir %attr(711,root,root) %{TZ_SYS_VAR}/%{name}/

%{_libdir}/libsecurity-manager-commons.so.*
%{_libdir}/libsqlite3-sha1-ext.so
%attr(-,root,root) %{_unitdir}/security-manager.*
%attr(-,root,root) %{_unitdir}/security-manager-cleanup.*
%attr(-,root,root) %{_unitdir}/security-manager-rules-loader.service
%attr(-,root,root) %{_unitdir}/basic.target.wants/security-manager-rules-loader.service
%attr(-,root,root) %{_unitdir}/sockets.target.wants/security-manager.*
%attr(-,root,root) %{_unitdir}/basic.target.wants/security-manager-cleanup.service
%config(noreplace) %attr(0600,root,root) %{TZ_SYS_DB}/.security-manager.db
%config(noreplace) %attr(0600,root,root) %{TZ_SYS_DB}/.security-manager.db-journal
%attr(-,root,root) /usr/share/platform-extension/711.security-manager-migration-from-product-partition.sh

%dir %attr(700,root,root) %{_datadir}/%{name}/dummy/

%files -n libsecurity-manager-client
%manifest %{_datadir}/libsecurity-manager-client.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/libsecurity-manager-client.so.*
%{_libdir}/libsecurity-manager-client-identify-internal.so.*

%files -n libsecurity-manager-client-devel
%manifest %{_datadir}/libsecurity-manager-client-devel.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/libsecurity-manager-client.so
%{_libdir}/libsecurity-manager-client-identify-internal.so
%{_libdir}/libsecurity-manager-commons.so
%{_includedir}/security-manager/*.h
%{_libdir}/pkgconfig/security-manager.pc

%files -n libnss-security-manager
%manifest %{_datadir}/libnss-security-manager.manifest
%license LICENSE.MIT
%defattr(-,root,root,-)
%{_libdir}/libnss_securitymanager.so.*

%files -n security-manager-policy
%manifest %{_datadir}/security-manager-policy.manifest
%license LICENSE
%config(noreplace) %{TZ_SYS_VAR}/%{name}/policy-version
%{_datadir}/%{name}/policy
%attr(755,root,root) %{_bindir}/security-manager-policy-reload
%attr(755,root,root) %{_sysconfdir}/opt/upgrade/241.security-manager.policy-update.sh

%files -n security-manager-policy-iptables
%license LICENSE
%{_unitdir}/security-manager-iptables.service
%{_unitdir}/basic.target.wants/security-manager-iptables.service
%attr(600, root, root) %{_sysconfdir}/security-manager-iptables.rules
%attr(600, root, root) %{_sysconfdir}/security-manager-ip6tables.rules

%files -n security-manager-tests
%manifest %{_datadir}/security-manager-tests.manifest
%license LICENSE
%license LICENSE.BSL-1.0
%attr(755,root,root) %{_bindir}/security-manager-unit-tests
%attr(755,root,root) %{_bindir}/security-manager-performance-tests
%attr(755,root,root) %{_bindir}/security-manager-test-rules-loader
%attr(0600,root,root) %{db_test_dir}/.security-manager-test.db
%attr(0600,root,root) %{db_test_dir}/.security-manager-test.db-journal
%attr(0600,root,root) %{db_test_dir}/.security-manager-test-v0.db
%attr(0600,root,root) %{db_test_dir}/.security-manager-test-v0.db-journal
%attr(0600,root,root) %{db_test_dir}/.security-manager-test-corrupted.db
%attr(0600,root,root) %{db_test_dir}/.security-manager-test-corrupted.db-journal
%attr(0600,root,root) %{db_test_dir}/.security-manager-test-empty.db
%attr(0600,root,root) %{db_test_dir}/.security-manager-test-empty.db-journal
%attr(0600,root,root) %{db_test_dir}/.security-manager-test-wrong-schema.db
%attr(0600,root,root) %{db_test_dir}/.security-manager-test-wrong-schema.db-journal
%attr(0600,root,root) %{db_test_dir}/.security-manager-test-rules.db
%attr(0600,root,root) %{db_test_dir}/.security-manager-test-rules*.txt

%files -n security-license-manager
%manifest %{_datadir}/security-license-manager.manifest
%license LICENSE
%{_libdir}/cynara/plugin/client/liblicense-manager-plugin-client.so
%{_libdir}/cynara/plugin/service/liblicense-manager-plugin-service.so
%{_bindir}/license-manager-agent
%attr(-,root,root) %{_unitdir}/cynara.service.wants/license-manager-agent.service
%attr(-,root,root) %{_unitdir}/license-manager-agent.service

%if "%{build_type}" == "COVERAGE"

%files -n security-manager-coverage
%manifest %{_datadir}/security-manager-tests.manifest
%license LICENSE
%{_bindir}/security-manager-coverage.sh
%coverage_dir

%endif
