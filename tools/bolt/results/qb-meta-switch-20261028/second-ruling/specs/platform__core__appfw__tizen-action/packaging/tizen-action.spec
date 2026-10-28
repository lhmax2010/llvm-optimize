Name:       tizen-action
Summary:    Tizen Action Framework
Version:    1.9.2
Release:    1
Group:      Application Framework / Application Launcher
License:    Apache-2.0 and MIT
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
Source1002:  tizen-action-plugin-launcher.service
Source1003:  tizen-action-plugin-launcher.socket
Source1004:  amd-tizen-action-service.socket
BuildRequires:  cmake
BuildRequires:  tidl
BuildRequires:  pkgconfig(amd)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(capi-appfw-app-common)
BuildRequires:  pkgconfig(capi-appfw-app-control)
BuildRequires:  pkgconfig(capi-appfw-app-manager)
BuildRequires:  pkgconfig(capi-appfw-package-manager)
BuildRequires:  pkgconfig(capi-appfw-service-application)
BuildRequires:  pkgconfig(capi-message-port)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(libsmack)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(pkgmgr)
BuildRequires:  pkgconfig(pkgmgr-parser)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(pkgmgr-installer)
BuildRequires:  pkgconfig(rpc-port)
BuildRequires:  pkgconfig(tizen-core)
BuildRequires:  pkgconfig(tizen-database)
BuildRequires:  pkgconfig(libcurl)

# requires for platform-default-actions
BuildRequires:  pkgconfig(capi-appfw-alarm)
BuildRequires:  pkgconfig(capi-appfw-package-manager)
BuildRequires:  pkgconfig(capi-system-system-settings)
BuildRequires:  pkgconfig(capi-appfw-tizen-theme)
BuildRequires:  pkgconfig(jsoncpp)
BuildRequires:  pkgconfig(notification)
BuildRequires:  pkgconfig(rua)
BuildRequires:  pkgconfig(capi-network-bluetooth)
BuildRequires:  pkgconfig(capi-network-wifi-manager)

%if 0%{?gcov:1}
BuildRequires:  lcov
%endif

%description
Tizen Action Framework

%package -n capi-appfw-tizen-action
Summary:  Tizen Action Framework API
Group:    Application Framework/Development
Requires: %{name} = %{version}-%{release}
Requires: amd-mod-tizen-action = %{version}-%{release}

%description -n capi-appfw-tizen-action
Tizen Action Framework API

%package -n capi-appfw-tizen-action-devel
Summary:  Tizen Action Framework API (Development)
Group:    Application Framework/Development
Requires: %{name} = %{version}-%{release}

%description -n capi-appfw-tizen-action-devel
Tizen Action Framework API (Development)

%package tool
Summary:  Tizen Action Framework Tools
Group:    Application Framework/Development
Requires: %{name} = %{version}-%{release}

%description tool
Tizen Action Framework Tools.

%package plugin-launcher
Summary:  Tizen Action Framework Plugin Launcher
Group:    Application Framework/Service
Requires: %{name} = %{version}-%{release}

%description plugin-launcher
Tizen Action Framework Plugin Launcher

%define amd_modules_dir %{_datadir}/amd
%package -n amd-mod-tizen-action
Summary:  Tizen Action Framework action DB writer module
Group:    Application Framework/Service
Requires: %{name} = %{version}-%{release}
Requires: amd
Requires: rpc-port

%description -n amd-mod-tizen-action
Application management daemon module that hosts the Action Framework RPC
services and owns writes to the action database.

%define plugin_sample_pkgid org.example.plugin-action-sample
%package -n %{plugin_sample_pkgid}
Summary:  Tizen Action Framework Sample Plugin
Requires: %{name} = %{version}

%description -n %{plugin_sample_pkgid}
Tizen Action Framework Sample Plugin.

%define tidl_sample_pkgid org.example.tidlactionsample
%package -n %{tidl_sample_pkgid}
Summary:  Tizen Action Framework TIDL Action Sample
Requires: %{name} = %{version}

%description -n %{tidl_sample_pkgid}
Tizen Action Framework TIDL-type action sample application.

%define tidl_custom_sample_pkgid org.example.tidlcustomactionsample
%package -n %{tidl_custom_sample_pkgid}
Summary:  Tizen Action Framework App-defined TIDL Action Sample
Requires: %{name} = %{version}

%description -n %{tidl_custom_sample_pkgid}
Complete app-defined TIDL Action and Entity sample application.

# Default content packages, split out of the service package so a product image
# can include or drop them independently. Change these pkgids in one place to
# rename the packages everywhere (manifest, install paths, %%files).
%define platform_actions_pkgid org.tizen.action-framework.platform-actions
%package -n %{platform_actions_pkgid}
Summary:  Tizen Action Framework Platform Default Actions
Requires: %{name} = %{version}

%description -n %{platform_actions_pkgid}
Platform default plugin actions (theme, alarm, app, notification, connectivity)
for the Tizen Action Framework.

%define default_actions_pkgid org.tizen.action-framework.default-actions
%package -n %{default_actions_pkgid}
Summary:  Tizen Action Framework Default Actions and Entities
Requires: %{name} = %{version}

%description -n %{default_actions_pkgid}
Default action definitions and entity schemas for the Tizen Action Framework.

%package -n tizen-action-smoketests
Summary:  Tizen Action Framework Smoke Tests and Integration Fixtures
Requires: %{name} = %{version}-%{release}
Requires: capi-appfw-tizen-action = %{version}-%{release}
Requires: amd-mod-tizen-action = %{version}-%{release}
Requires: %{default_actions_pkgid} = %{version}-%{release}
Requires: %{tidl_sample_pkgid} = %{version}-%{release}
Requires: %{tidl_custom_sample_pkgid} = %{version}-%{release}

%description -n tizen-action-smoketests
Smoke tests and integration fixtures for the Tizen Action Framework.

%define tizen_action_db_version 4

%prep
%setup -q
cp %{SOURCE1001} .
/bin/bash ./tidl/prebuild.sh

%build
%{?asan:
export CXXFLAGS="$CXXFLAGS -Wno-maybe-uninitialized"
}

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DCMAKE_VERBOSE_MAKEFILE:BOOL=%{?verbose_make:ON}%{!?verbose_make:OFF} \
         -DUNITDIR=%{_unitdir} \
         -DFULLVER=%{version} \
         -DMAJORVER=${MAJORVER} \
         -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
         -DPLUGIN_SAMPLE_PKGID=%{plugin_sample_pkgid} \
         -DTIDL_SAMPLE_PKGID=%{tidl_sample_pkgid} \
         -DTIDL_CUSTOM_SAMPLE_PKGID=%{tidl_custom_sample_pkgid} \
         -DPLATFORM_ACTIONS_PKGID=%{platform_actions_pkgid} \
         -DDEFAULT_ACTIONS_PKGID=%{default_actions_pkgid} \
         -DTIZEN_ACTION_DB_VERSION=%{tizen_action_db_version} \
         -DTZ_SYS_DB=%{TZ_SYS_DB} \
         -DAMD_MODULES_DIR=%{amd_modules_dir} \
         -DTIZEN_FEATURE_SMACK_DISABLE:BOOL=%{?dev_wos:ON}%{!?dev_wos:OFF}
%__make %{?_smp_mflags}

%check
export LD_LIBRARY_PATH="../../src/action:../../src/common:../../src/pkgmgr_plugin_parser"
ctest -V %{?_smp_mflags}

%install
%make_install

mkdir -p %{buildroot}%{_libdir}/tizen-action/plugins
mkdir -p %{buildroot}%{_unitdir}/sockets.target.wants
install -m 0644 %SOURCE1002 %{buildroot}%{_unitdir}/tizen-action-plugin-launcher.service
install -m 0644 %SOURCE1003 %{buildroot}%{_unitdir}/tizen-action-plugin-launcher.socket
ln -sf ../tizen-action-plugin-launcher.socket %{buildroot}%{_unitdir}/sockets.target.wants/tizen-action-plugin-launcher.socket

install -m 0644 %SOURCE1004 %{buildroot}%{_unitdir}/amd-tizen-action-service.socket
ln -sf ../amd-tizen-action-service.socket %{buildroot}%{_unitdir}/sockets.target.wants/amd-tizen-action-service.socket

%post
/sbin/ldconfig

%post tool
%{_bindir}/action-db-recovery
chmod 666 %{TZ_SYS_DB}/.tizen_action.db
chmod 666 %{TZ_SYS_DB}/.tizen_action.db-journal
chsmack -a _ %{TZ_SYS_DB}/.tizen_action.db
chsmack -a _ %{TZ_SYS_DB}/.tizen_action.db-journal

%preun

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE LICENSE.MIT
%{_libdir}/libtizen-action.so*
%{_libdir}/libtizen-action-common.so*
%{_sysconfdir}/package-manager/parserlib/metadata/libtizen-action-plugin.so
%{_datarootdir}/parser-plugins/tizen-action-plugin.info
%{_datarootdir}/parser-plugins/tizen-action-bg-rest-parser.info
%dir %{_datadir}/tizen-action-bg-rest
%{_datadir}/tizen-action-bg-rest/allowlist.json
%attr(0755,root,root) %{_datadir}/upgrade/scripts/501.tizen_action_db_upgrade.sh
%attr(0755,root,root) %{_sysconfdir}/tizen-action/upgrade/scripts/*

%files -n capi-appfw-tizen-action
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_libdir}/libcapi-appfw-tizen-action.so.*

%files -n capi-appfw-tizen-action-devel
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_libdir}/libcapi-appfw-tizen-action.so
%{_includedir}/tizen-action/action.h
%{_includedir}/tizen-action/action_error.h
%{_libdir}/pkgconfig/capi-appfw-tizen-action.pc

%files tool
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_bindir}/action-db-recovery
%{_bindir}/action-tool
%{_bindir}/action-upgrade

%files plugin-launcher
%defattr(-,root,root,-)
%manifest %{name}.manifest
%dir %{_libdir}/tizen-action
%dir %{_libdir}/tizen-action/plugins
%{_unitdir}/tizen-action-plugin-launcher.service
%{_unitdir}/tizen-action-plugin-launcher.socket
%{_unitdir}/sockets.target.wants/tizen-action-plugin-launcher.socket
%{_bindir}/tizen-action-plugin-launcher

%files -n amd-mod-tizen-action
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{amd_modules_dir}/mod/libamd-mod-tizen-action.so
%{_unitdir}/amd-tizen-action-service.socket
%{_unitdir}/sockets.target.wants/amd-tizen-action-service.socket

%files -n %{platform_actions_pkgid}
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_prefix}/apps/%{platform_actions_pkgid}/*
%{_datadir}/packages/%{platform_actions_pkgid}.xml

%files -n %{default_actions_pkgid}
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_prefix}/apps/%{default_actions_pkgid}/*
%{_datadir}/tizen-action/action.seq
%{_datadir}/packages/%{default_actions_pkgid}.xml

%files -n %{plugin_sample_pkgid}
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_prefix}/apps/%{plugin_sample_pkgid}/*
%{_datadir}/packages/%{plugin_sample_pkgid}.xml

%files -n %{tidl_sample_pkgid}
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_prefix}/apps/%{tidl_sample_pkgid}/*
%{_datadir}/packages/%{tidl_sample_pkgid}.xml

%files -n %{tidl_custom_sample_pkgid}
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_prefix}/apps/%{tidl_custom_sample_pkgid}/*
%{_datadir}/packages/%{tidl_custom_sample_pkgid}.xml

%files -n tizen-action-smoketests
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_bindir}/tizen-action-smoke
%{_bindir}/tizen-action-plugin-execution-test
%{_bindir}/tizen-action-plugin-remote-request-test
%{_prefix}/apps/org.tizen.action.smoke.plugin/*
%{_prefix}/apps/org.tizen.action.smoke.appcontrol/*
%{_datadir}/packages/org.tizen.action.smoke.plugin.xml
%{_datadir}/packages/org.tizen.action.smoke.appcontrol.xml
