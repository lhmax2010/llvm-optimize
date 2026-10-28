%define on_off() %{expand:%%{?with_%{1}:ON}%%{!?with_%{1}:OFF}}

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

%if "%{WITH_VD}" == "1"
%define enable_vconf_activation 1
%define enable_system_worker 0
%define template_args --disable template-fixed
%define mandatory_client_args --mandatory-client buxton
%else
%define enable_vconf_activation 0
%define enable_system_worker 0
%endif

%if 0%{?dev_wos:1} || 0%{?uid_app_sandboxing:1}
%define macpolicy_args --disable copy-smack-attrs
%endif

Name:       sessiond
Summary:    Service to manage subsessions
Version:    11.0.1
Release:    1
Group:      System/Management
License:    MIT
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
BuildRequires: cmake
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: gtest-devel
BuildRequires: pkgconfig(libacl)
BuildRequires: pkgconfig(libsmack)
BuildRequires: pkgconfig(capi-system-resource)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(libsyscommon-plugin-api-sessiond)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(pkgmgr-info)

%if %{enable_system_worker}
BuildRequires:  pkgconfig(system-server-worker)
%endif

# Tools avaliable but cause mic(1) to fail build - disable for now
#Requires:   /sbin/mkfs.ext4
#Requires:   /sbin/fsck.ext4
# Dynamically determined
#Requires:   /sbin/resize2fs

%description

%prep
%setup -q

%build
mkdir -p build
(
cd build
%cmake .. \
	-DVERSION=%{version} \
	-DCMAKE_BUILD_TYPE=Release \
	-DENABLE_SYSTEM_WORKER=%{enable_system_worker} \
	-DDEACTIVATION_DISABLE=0 \
	-DDEFAULT_USER=%TZ_SYS_DEFAULT_USER

make %{?jobs:-j%jobs}
)
cp %{SOURCE1} .

%post
systemctl daemon-reload
systemctl restart sessiond

%postun
systemctl daemon-reload
systemctl stop sessiond

%install
rm -rf %{buildroot}
(cd build && %make_install)

%install_service multi-user.target.wants sessiond.service
%install_service delayed.target.wants sessiond-generate-cache.service

%if %{enable_vconf_activation}
mkdir -p %{buildroot}/usr/lib/systemd/eventd/
ln -sf /usr/lib/systemd/system/sessiond.service %{buildroot}/usr/lib/systemd/eventd/sessiond.service
%endif

sed -i -e '/ExecStart=/ a Environment=SESSIOND_ARGS="%{?mandatory_client_args} %{?template_args} %{?macpolicy_args}"' %{buildroot}/usr/lib/systemd/system/sessiond.service

%files
%manifest sessiond.manifest
%license LICENSE.MIT
%{_bindir}/sessiond
%{_unitdir}/multi-user.target.wants/sessiond.service
%{_unitdir}/sessiond.service
%if %{enable_vconf_activation}
/usr/lib/systemd/eventd/sessiond.service
%endif
%{_unitdir}/sessiond-generate-cache.service
%{_unitdir}/delayed.target.wants/sessiond-generate-cache.service
%{_unitdir}/org.tizen.sessiond.busname
%{_datadir}/dbus-1/system-services/org.tizen.sessiond.service
/etc/dbus-1/system.d/org.tizen.sessiond.conf
/usr/lib/tmpfiles.d/sessiond-run.conf
/usr/lib/sessiond/sessiond-factory-reset.sh
