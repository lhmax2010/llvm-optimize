%{!?build_type:%global build_type RELEASE}

Name:    privilege-checker
Summary: Privilege Management
Version: 1.5.0
Release: 0
Group:   System/Libraries
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz
Source1000: privilege-checker.ini

%description
Package for Privilege Management

%package -n security-privilege-manager
Summary:    Privilege Manager API
BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(iniparser)
BuildRequires: gettext-tools
BuildRequires: pkgconfig(pkgmgr-info)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(libtzplatform-config)
%if "%{build_type}" == "COVERAGE"
BuildRequires: lcov
%endif
Requires: security-config
Requires: tizen-platform-config
Requires: pkgmgr
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires(post): /bin/systemctl
Requires(postun): /bin/systemctl
Recommends: security-privilege-manager-profile_common = %{version}-%{release}

%description -n security-privilege-manager
The Privilege Manager API provides functions to verify privilege information of packages to be installed.

%package -n security-privilege-manager-extension-tv
Summary:    Privilege Manager API extension for Tizen TV profile
Provides:   security-privilege-manager-profile = %{version}-%{release}
Provides:   security-privilege-manager-profile_tv = %{version}-%{release}
Requires:   security-privilege-manager = %{version}-%{release}
Obsoletes:  security-privilege-manager-extension-common
Obsoletes:  security-privilege-manager-extension-iot
Obsoletes:  security-privilege-manager-extension-mobile
Obsoletes:  security-privilege-manager-extension-wearable

%description -n security-privilege-manager-extension-tv
The Privilege Manager API provides functions to verify privilege information of packages to be installed.
This is an extension for privilege manager for Tizen TV profile,
which requires security-profile-manger to be installed before this.

%package -n security-privilege-manager-extension-common
Summary:    Privilege Manager API extension for Tizen Common profile
Provides:   security-privilege-manager-profile = %{version}-%{release}
Provides:   security-privilege-manager-profile_common = %{version}-%{release}
Requires:   security-privilege-manager = %{version}-%{release}
Obsoletes:  security-privilege-manager-extension-tv
Obsoletes:  security-privilege-manager-extension-iot
Obsoletes:  security-privilege-manager-extension-mobile
Obsoletes:  security-privilege-manager-extension-wearable

%description -n security-privilege-manager-extension-common
The Privilege Manager API provides functions to verify privilege information of packages to be installed.
This is an extension for privilege manager for Tizen Common profile,
which requires security-privilege-manager to be installed before this.

%package -n security-privilege-manager-devel
Summary:    Privilege Manager API (Development)
Requires:   security-privilege-manager = %{version}-%{release}

%description -n security-privilege-manager-devel
The Privilege Manager API provides functions to verify privilege information of packages to be installed.

%package -n security-privilege-manager-tests
Summary:    Internal TC for privilege-checker

%description -n security-privilege-manager-tests
Internal TC for privilege-checker APIs

%if "%{build_type}" == "COVERAGE"

%package -n security-privilege-manager-coverage
Summary: Privilege Checker code coverage data
Requires: security-privilege-manager-tests = %{version}-%{release}
Requires: privilege-checker-debugsource = %{version}-%{release}
Requires: lcov
Requires: gcc

%description -n security-privilege-manager-coverage
Privilege Checker code coverage data

%endif

%package -n privilege-verifier
Summary:    Privilege Verification Utility
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(iniparser)

%description -n privilege-verifier
The Privilege Verifier Utility provides functions to verify privilege information of packages to be installed.

%prep
%setup -q
cp %{SOURCE1000} .

%build

%global coverage_dir %{_datadir}/privilege-checker-coverage

%cmake . -DCMAKE_BUILD_TYPE=%{build_type} \
        -DTZ_SYS_DB=%TZ_SYS_DB \
        -DTZ_SYS_SHARE=%TZ_SYS_SHARE \
        -DSYSTEMD_INSTALL_DIR=%{_unitdir} \
        -DCOVERAGE_DIR=%{coverage_dir}

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/privilege-manager
mkdir -p %{buildroot}/%{TZ_SYS_DB}
%make_install

mkdir -p %{buildroot}%{_sysconfdir}
sed "s|@PROFILE@|common|" privilege-checker.ini > %{buildroot}%{_sysconfdir}/privilege-checker.ini.common
sed "s|@PROFILE@|tv|" privilege-checker.ini > %{buildroot}%{_sysconfdir}/privilege-checker.ini.tv

# Enable the DB integrity check service at boot (enable-by-symlink).
mkdir -p %{buildroot}%{_unitdir}/basic.target.wants
ln -sf ../privilege-checker-integrity.service \
    %{buildroot}%{_unitdir}/basic.target.wants/privilege-checker-integrity.service

%clean
rm -rf %{buildroot}

%post -n security-privilege-manager
/sbin/ldconfig
systemctl daemon-reload

if [ $1 = 1 ]; then
    # installation
    %{_datadir}/privilege-manager/privacy_db_updater.sh --generate
    %{_datadir}/privilege-manager/policy_db_updater.sh --generate
fi

%{_datadir}/privilege-manager/policy_db_updater.sh
# try to create backup - will fail when partition is RO
%{_datadir}/privilege-manager/policy_db_updater.sh --backup || true
%{_datadir}/privilege-manager/privacy_db_updater.sh --backup || true

%postun -n security-privilege-manager
/sbin/ldconfig
if [ $1 = 0 ]; then
    # uninstall
    systemctl daemon-reload
fi

%files -n security-privilege-manager
%license LICENSE.APLv2
%manifest packaging/security-privilege-manager.manifest
%{_libdir}/libsecurity-privilege-manager.so*
%{_datadir}/locale/*
%dir %{_datadir}/privilege-manager
%ghost %attr(0644,root,root) %{_datadir}/privilege-manager/.privilege.db
%{_datadir}/privilege-manager/csv2sql.awk
%attr(750,root,security_fw) %{_datadir}/privilege-manager/policy_db_updater.sh
%attr(755,root,app_fw) %{_datadir}/privilege-manager/privacy_db_updater.sh
%attr(700,root,root) %{_bindir}/privilege-db-update
%attr(775,root,root) %{_sbindir}/privilege-checker-integrity
%{_unitdir}/privilege-checker-integrity.service
%{_unitdir}/basic.target.wants/privilege-checker-integrity.service
%ghost %attr(0660,root,security_fw) /%{TZ_SYS_DB}/.policy.db
%ghost %attr(0660,root,security_fw) /%{TZ_SYS_DB}/.policy.db-journal
%ghost %attr(0664,root,app_fw) /%{TZ_SYS_DB}/.privacy.db
%ghost %attr(0664,root,app_fw) /%{TZ_SYS_DB}/.privacy.db-journal
%ghost %attr(660,root,security_fw) %{_datadir}/privilege-manager/.policy.db.bkup
%ghost %attr(664,root,app_fw) %{_datadir}/privilege-manager/.privacy.db.bkup
%ghost %attr(0644,root,root) %{_sysconfdir}/privilege-checker.ini

%post -n security-privilege-manager-extension-tv
cp %{_datadir}/privilege-manager/.privilege.tv.db %{_datadir}/privilege-manager/.privilege.db
cp %{_sysconfdir}/privilege-checker.ini.tv %{_sysconfdir}/privilege-checker.ini

%files -n security-privilege-manager-extension-tv
%license LICENSE.APLv2
%manifest packaging/security-privilege-manager.manifest
%{_datadir}/privilege-manager/.privilege.tv.db
%{_sysconfdir}/privilege-checker.ini.tv

%post -n security-privilege-manager-extension-common
cp %{_datadir}/privilege-manager/.privilege.common.db %{_datadir}/privilege-manager/.privilege.db
cp %{_sysconfdir}/privilege-checker.ini.common %{_sysconfdir}/privilege-checker.ini

%files -n security-privilege-manager-extension-common
%license LICENSE.APLv2
%manifest packaging/security-privilege-manager.manifest
%{_datadir}/privilege-manager/.privilege.common.db
%{_sysconfdir}/privilege-checker.ini.common

%files -n security-privilege-manager-devel
%{_includedir}/privilegemgr/*.h
%{_libdir}/pkgconfig/security-privilege-manager.pc

%files -n security-privilege-manager-tests
%{_bindir}/privilege-checker-tests

%if "%{build_type}" == "COVERAGE"

%files -n security-privilege-manager-coverage
%{_bindir}/privilege-checker-coverage.sh
%coverage_dir

%endif

%files -n privilege-verifier
%license LICENSE.APLv2
%{_bindir}/privilege-verifier

%files -n privilege-checker
%license LICENSE.APLv2
