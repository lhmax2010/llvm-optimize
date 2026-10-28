Name:       download-provider
Summary:    Download the contents in background
Version:    2.4.4
Release:    0
Group:      Development/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Requires(post): sqlite
Requires(post): connman
Requires: security-config
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(xdgmime)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-appfw-app-manager)
BuildRequires:  pkgconfig(capi-appfw-application)
BuildRequires:  pkgconfig(capi-network-connection)
BuildRequires:  pkgconfig(appsvc)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(capi-content-mime-type)
BuildRequires:  gettext-devel
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(capi-network-wifi-direct)
%if "%{?profile}" != "wearable"
BuildRequires:  pkgconfig(notification)
%endif
BuildRequires:  pkgconfig(storage)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-client-async)
BuildRequires:  pkgconfig(cynara-creds-socket)
BuildRequires:  pkgconfig(cynara-creds-dbus)
BuildRequires:  pkgconfig(cynara-creds-pid)
BuildRequires:  pkgconfig(cynara-uid)
BuildRequires:  pkgconfig(libtzplatform-config)

%if 0%{?gtests:1}
BuildRequires:  pkgconfig(gmock)
%endif

%description
Description: Download the contents in background

%package devel
Summary:    download-provider
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Description: Download the contents in background (development files)

%prep
%setup -q

%define _data_install_path %{TZ_SYS_DATA}/%{name}
%define _resource_install_path /usr/share/%{name}
%define _imagedir %{_resource_install_path}/images
%define _localedir %{_resource_install_path}/locales
%define _databasedir %{_data_install_path}/database
%define _database_client_dir %{_databasedir}/clients
%define _notifydir %{_data_install_path}/notify
%define _ipc_socket /tmp/.download-provider.sock
%define _logdump_script_dir %{TZ_SYS_ETC}/dump.d/module.d
%define _http_lib libcurl
%define _manifest_name %{name}.manifest
%if "%{?tizen_profile_name}" == "tv"
%define _ca_cert /opt/data/cert/vdca.pem
%define _ca_path /opt/data/cert/user/
%define max_concurrent_downloads 15
%else
%define max_concurrent_downloads 50
%endif

%build
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"

%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

%cmake -DTZ_SYS_GLOBALUSER_DATA=%TZ_SYS_GLOBALUSER_DATA \
	-DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
	-DBIN_INSTALL_DIR:PATH=%{_bindir} \
	-DLIB_INSTALL_DIR:PATH=%{_libdir} \
	-DLIB_AGENT_PATH="/usr/%{?_lib}/libdownloadagent2.so.0.1.0" \
	-DLIB_CACHE_AGENT_PATH="/usr/%{?_lib}/libcacheagent.so.0.1.0" \
	-DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
	-DPKG_NAME=%{name} \
	-DPKG_VERSION=%{version} \
	-DPKG_RELEASE=%{release} \
	-DIPC_SOCKET:PATH=%{_ipc_socket} \
	-DPROVIDER_DIR:PATH=%{_data_install_path} \
	-DNOTIFY_DIR:PATH=%{_notifydir} \
	-DDATABASE_DIR:PATH=%{_databasedir} \
	-DDATABASE_CLIENT_DIR:PATH=%{_database_client_dir} \
	-DIMAGE_DIR:PATH=%{_imagedir} \
	-DLOCALE_DIR:PATH=%{_localedir} \
	-DSUPPORT_WIFI_DIRECT:BOOL=OFF \
	-DSUPPORT_DOWNLOAD_BOOSTER:BOOL=OFF \
%if "%{?profile}" == "wearable"
	-DSUPPORT_NOTIFICATION:BOOL=OFF \
%else
	-DSUPPORT_NOTIFICATION:BOOL=ON \
%endif
	-DSUPPORT_LOG_MESSAGE:BOOL=ON \
	-DSUPPORT_OMA_DRM:BOOL=OFF \
	-DSUPPORT_COMPANION_MODE:BOOL=OFF \
%if "%{?profile}" == "wearable"
	-DSUPPORT_MULTILINGUAL:BOOL=ON \
%else
	-DSUPPORT_MULTILINGUAL:BOOL=OFF \
	-DMAX_CONCURRENT_DOWNLOADS=%{?max_concurrent_downloads}\
%endif
	-DCMAKE_LOG_DUMP_SCRIPT_DIR=%{_logdump_script_dir} \
	-DHTTP_LIB=%{_http_lib} \
%if "%{?_lib}" == "lib64"
	%{?_cmake_lib_suffix64} \
%endif
	%{?_cmake_skip_rpath} \
	-DBUILD_SHARED_LIBS:BOOL=ON \
	-DBUILD_GTESTS=%{?gtests:1}%{!?gtests:0} \
	-DBUILD_GCOV=%{?gcov:1}%{!?gcov:0} \
	-DSUPPORT_LARGE_FILE:BOOL=ON \
%if "%{?tizen_profile_name}" == "tv"
	-DCA_CERT=%{_ca_cert} \
	-DCA_PATH=%{_ca_path} \
%endif
	.

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}/var/lib/download-provider/
install -m 600 res/var/lib/download-provider/settings %{buildroot}/var/lib/download-provider/settings

## container_enable
mkdir -p %{buildroot}/etc/vasum/vsmzone.resource/
mv %{buildroot}/usr/share/download-provider/download-provider.res %{buildroot}/etc/vasum/vsmzone.resource/

mkdir -p %{buildroot}/lib/systemd/system/sockets.target.wants
ln -s ../download-provider.socket %{buildroot}/lib/systemd/system/sockets.target.wants/

%post
#make notify dir in post section for smack
mkdir %{TZ_SYS_DATA}/download-provider
mkdir -p %{_notifydir}
chown -R web_fw:web_fw %{_notifydir}
chsmack -a 'System::Shared' %{_notifydir}
chsmack -t %{_notifydir}
mkdir -p --mode=0700 %{_databasedir}
chown -R web_fw:web_fw %{_databasedir}
chsmack -a 'System' %{_databasedir}
mkdir -p --mode=0700 %{_database_client_dir}
chsmack -a 'System' %{_database_client_dir}
chown -R web_fw:web_fw %{_database_client_dir}
chown -R web_fw:web_fw %{_data_install_path}
chown -R web_fw:web_fw /var/lib/download-provider/
mkdir -p /opt/data/download_cache
chown -R web_fw:web_fw /opt/data/download_cache

%files
%defattr(-,root,root,-)
%manifest %{_manifest_name}
%{_imagedir}/*.png
%{_localedir}/*/*/download-provider.mo
%{_libdir}/*.so.*
%attr(0600,web_fw,web_fw) /var/lib/download-provider/settings
/lib/systemd/system/download-provider.service
/lib/systemd/system/download-provider.socket
/lib/systemd/system/sockets.target.wants/download-provider.socket
%{_bindir}/%{name}
%attr(0544,root,root) %{_logdump_script_dir}/dump-%{name}.sh
## container_enable
%attr(0644,root,root) /etc/vasum/vsmzone.resource/download-provider.res
%license LICENSE.APLv2
%attr(0755,-,-) %{TZ_SYS_UPGRADE_SCRIPTS}/500.download-provider_upgrade.sh

%files devel
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_libdir}/*.so
%{_libdir}/pkgconfig/download-provider.pc
%{_libdir}/pkgconfig/download-provider-interface.pc
%{_libdir}/pkgconfig/download-agent.pc
%{_libdir}/pkgconfig/cache-agent.pc
%{_includedir}/download-provider/download-provider.h
%{_includedir}/download-provider/download-provider-interface.h
%{_includedir}/download-provider/download-agent-interface.h
%{_includedir}/download-provider/cache-agent-interface.h

%if 0%{?gtests:1}
%{_bindir}/gtest*
%endif
