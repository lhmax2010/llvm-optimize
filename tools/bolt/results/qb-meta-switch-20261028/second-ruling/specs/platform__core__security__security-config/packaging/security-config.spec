%if "%{tizen_profile_name}" == "tv"
%define WITH_VD 1
%else
%define WITH_VD 0
%endif

Name:           security-config
Summary:        A set of security configuration files
Version:        1.0
Release:        1
License:        Apache-2.0
Group:          Security/Configuration
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.manifest
BuildRequires:  cmake
Requires:       shadow-utils
Requires:       libcap-tools
Requires:       systemd
Requires:       grep
Requires:       sed
Requires:       util-linux
%if !("%{?dev_wos}" == "1")
Requires:       smack
%endif

%{!?TZ_SYS_RO_SHARE: %global TZ_SYS_RO_SHARE /usr/share}
%global SECURITY_TEST_DIR %{TZ_SYS_RO_SHARE}/security-config/test

%description
set of important system configuration and
setup files, such as passwd, group, and profile.

%package profile_common
Summary:	Additional package for Common Profile
Requires:	security-config = %{version}

%description profile_common
additional security tests and settings for common profile

%package profile_tv
Summary:	Additional package for TV Profile
Requires:	security-config = %{version}

%description profile_tv
additional security tests and settings for tv profile

%prep
%setup -q

%build

%if "%{?dev_wos}" == "1" || "%{?uid_app_sandboxing}" == "1"
config/generate_configure_uid_sandboxing > config/configure_uid_sandboxing
%endif

%cmake . -DARCH=%{_arch} \
%if "%{?dev_wos}" == "1" || "%{?uid_app_sandboxing}" == "1"
	-DUID_SANDBOXING=ON \
%endif
%if "%{?dev_wos}" == "1"
	-DDEV_WOS=ON \
%endif
	-DSYSTEMD_INSTALL_DIR=%{_unitdir} \
	-DWITH_VD=%{WITH_VD}

%install
rm -rf %{buildroot}
%make_install

%if "%{?dev_wos}" != "1"
mkdir -p %{buildroot}/%{_unitdir}/multi-user.target.wants
ln -s ../%{name}.service %{buildroot}/%{_unitdir}/multi-user.target.wants/%{name}.service
%endif

mkdir -p %{buildroot}%{SECURITY_TEST_DIR}/utils
%ifarch %{arm}
cp -f test/utils/arm/* %{buildroot}%{SECURITY_TEST_DIR}/utils/
%endif
%ifarch x86_64
cp -f test/utils/x86_64/* %{buildroot}%{SECURITY_TEST_DIR}/utils/
%endif
%ifarch aarch64
cp -f test/utils/aarch64/* %{buildroot}%{SECURITY_TEST_DIR}/utils/
%endif
%ifarch %{ix86}
cp -f test/utils/i386/* %{buildroot}%{SECURITY_TEST_DIR}/utils/
%endif
%ifarch riscv64
cp -f test/utils/riscv64/* %{buildroot}%{SECURITY_TEST_DIR}/utils/
%endif

%post
/usr/share/security-config/group_id_setting
%if "%{?dev_wos}" == "1" || "%{?uid_app_sandboxing}" == "1"
/usr/share/security-config/configure_uid_sandboxing
%endif
/usr/share/security-config/set_label
mkdir -p /opt/share/security-config/result
mkdir -p /opt/share/security-config/log
#hard coded as we cannot use system-info-tool here
/usr/share/security-config/configure_askuser.sh DISABLE
rm -r /opt/share/security-config/test
ln -s %{SECURITY_TEST_DIR} /opt/share/security-config/test
touch /opt/share/security-config/dummy_file
chmod 600 /opt/share/security-config/dummy_file
%{SECURITY_TEST_DIR}/new_service_test/create_list.sh COMMON

%post profile_common
mv /usr/share/security-config/mount_list/common/additional_mount_list /usr/share/security-config/additional_mount_list
rm -r /usr/share/security-config/mount_list/
%if "%{?dev_wos}" != "1"
chsmack -a "System::NoUse" /etc/smack/onlycap
%endif
%{SECURITY_TEST_DIR}/new_service_test/create_list.sh COMMON

%post profile_tv
mv /usr/share/security-config/mount_list/tv/additional_mount_list /usr/share/security-config/additional_mount_list
rm -r /usr/share/security-config/mount_list/
%if "%{?dev_wos}" != "1"
chsmack -a "System::NoUse" /etc/smack/onlycap
%endif
%{SECURITY_TEST_DIR}/new_service_test/create_list.sh TV

%files
%manifest %{_datadir}/%{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%attr(755,root,root) /usr/share/security-config/group_id_setting
%attr(755,root,root) /usr/share/security-config/set_label
%attr(755,root,root) /usr/share/security-config/set_capability
%attr(755,root,root) /usr/share/security-config/mdm_blacklist
%attr(755,root,root) /usr/share/security-config/change_permission
%attr(755,root,root) /usr/share/security-config/configure_askuser.sh
%if "%{?dev_wos}" == "1" || "%{?uid_app_sandboxing}" == "1"
%attr(755,root,root) /usr/share/security-config/configure_uid_sandboxing
%attr(755,root,root) %{_sysconfdir}/gumd/useradd.d/92_user-permissions.post
%endif
%attr(700,root,root) /usr/share/security-config/update_privacy_mount_list.sh
%attr(644,root,root) /usr/lib/tmpfiles.d/security-config.conf
%attr(755,root,root) %{SECURITY_TEST_DIR}/image_test.sh
%attr(755,root,root) %{SECURITY_TEST_DIR}/aslr_test/*
%attr(755,root,root) %{SECURITY_TEST_DIR}/utils/*
%attr(755,root,root) %{SECURITY_TEST_DIR}/dep_test/*
%attr(755,root,root) %{SECURITY_TEST_DIR}/smack_rule_test/*
%attr(755,root,root) %{SECURITY_TEST_DIR}/capability_test/*
%attr(755,root,root) %{SECURITY_TEST_DIR}/path_check_test/*
%attr(755,root,root) %{SECURITY_TEST_DIR}/smack_basic_test/*
%attr(755,root,root) %{SECURITY_TEST_DIR}/security_mount_option_test/*
%attr(755,root,root) %{SECURITY_TEST_DIR}/relro_stack_canary_test/*
%attr(755,root,root) %{SECURITY_TEST_DIR}/setuid_test/*
%attr(755,root,root) %{SECURITY_TEST_DIR}/execute_label_check_test/*
%attr(755,root,root) %{SECURITY_TEST_DIR}/new_service_test/*
%attr(755,root,root) /usr/share/upgrade/scripts/201.security_upgrade.sh
%attr(755,root,root) /usr/share/upgrade/scripts/202.privilege_upgrade.sh
%attr(755,root,root) %{_sysconfdir}/gumd/useradd.d/90_user-content-permissions.post
%attr(755,root,root) %{_sysconfdir}/gumd/useradd.d/91_user-dbspace-permissions.post
%if "%{?dev_wos}" != "1" && "%{?uid_app_sandboxing}" != "1"
%attr(644,root,root) /etc/smack/netlabel.d/netlabel_config
%endif

%if "%{?dev_wos}" != "1"
%global smack_files %{expand:
%%attr(-,root,root) %%{_unitdir}/security-config.service
%%attr(-,root,root) %%{_unitdir}/multi-user.target.wants/security-config.service
%%attr(755,root,root) /usr/share/security-config/smack_default_labeling
%%attr(644,root,root) /etc/smack/onlycap}
%else
%global smack_files %{nil}
%endif

%files profile_common
%license LICENSE
%{smack_files}
%attr(644,root,root) /usr/share/security-config/mount_list/common/*

%files profile_tv
%license LICENSE
%{smack_files}
%attr(644,root,root) /usr/share/security-config/mount_list/tv/*

