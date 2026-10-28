Name:       stc-manager
Summary:    STC(Smart Traffic Control) manager
Version:    0.1.7
Release:    0
Group:      Network & Connectivity/Other
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:	pkgconfig(vconf)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(yaca)
BuildRequires:  python
BuildRequires:  python-xml
BuildRequires:  python3-setuptools
BuildRequires:	pkgconfig(sqlite3)

%description
A smart traffic control manager to manage traffic counting and bandwidth limitation

%package plugin-appstatus
Summary: STC manager application status plugin
BuildRequires:	pkgconfig(bundle)
BuildRequires:	pkgconfig(syspopup-caller)
Requires:	stc-manager-plugin-monitor

%description plugin-appstatus
A smart traffic control manager extension for application status plugin

%package plugin-exception
Summary: STC manager exception list plugin
BuildRequires:  pkgconfig(pkgmgr-info)
Requires:	stc-manager-plugin-monitor

%description plugin-exception
A smart traffic control manager extension for exception list plugin

%package plugin-procfs
Summary: STC manager exception proc file system plugin
Requires:	stc-manager-plugin-monitor

%description plugin-procfs
A smart traffic control manager extension for proc file system plugin

%package plugin-pcap
Summary: STC manager exception packet capture plugin
BuildRequires:  libpcap-devel

%description plugin-pcap
A smart traffic control manager extension for packet capture plugin

%package plugin-tether
Summary: Tethering plugin for data usage of tethering clients
Requires:	stc-manager-plugin-monitor

%description plugin-tether
A smart traffic control manager extension for tethering client data usage plugin

%package plugin-monitor
Summary: Monitor plugin for data usage of clients
BuildRequires:	pkgconfig(bundle)
BuildRequires:	pkgconfig(syspopup-caller)

%description plugin-monitor
A smart traffic control manager extension for monitoring client data usage plugin

%package plugin-firewall
Summary: Firewall plugin for managing firewall rules

%description plugin-firewall
A smart traffic control manager extension for firewall plugin

%global stc_db_file %{TZ_SYS_DB}/.%{name}-datausage.db
%global stc_backup_db_file %{TZ_SYS_RO_SHARE}/stc/.%{name}-datausage.db

%prep
%setup -q
cp %{SOURCE1001} ./%{name}.manifest

%build
%if "%{tizen_profile_name}" == "tv"
	CFLAGS+=" -DTIZEN_TV_EXT"
%endif

%cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_VERBOSE_MAKEFILE=OFF \
	-DBIN_INSTALL_DIR:PATH=%{_bindir} \
	-DSYSTEMD_DIR:PATH=%{_unitdir} \
	-DSYSCONF_DIR:PATH=%{_sysconfdir} \
	-DSTC_RW_DIR:PATH=%{_localstatedir}/lib/stc \
	-DDATABASE_FULL_PATH=%{stc_db_file} \
	-DDATABASE_BACKUP_PATH=%{stc_backup_db_file} \
	-DLIBDIR=%{_libdir}
make %{?_smp_mflags}

%install
%make_install

#database initialization
mkdir -p %{buildroot}%{TZ_SYS_DB}
sqlite3 %{buildroot}%{stc_db_file} < res/traffic_db.sql
sqlite3 %{buildroot}%{stc_db_file} < res/firewall_db.sql
install -D -m 0660 %{buildroot}%{stc_db_file} %{buildroot}%{stc_backup_db_file}

mkdir -p %{buildroot}%{TZ_SYS_UPGRADE_SCRIPTS}
install -m 0755 res/500.%{name}_upgrade.sh %{buildroot}%{TZ_SYS_UPGRADE_SCRIPTS}

%install_service multi-user.target.wants %{name}.service


%files
%manifest %{name}.manifest
%{_bindir}/*
%{_unitdir}/%{name}.service
%{_unitdir}/multi-user.target.wants/%{name}.service
%{_localstatedir}/lib/stc/exceptions
%{_sysconfdir}/dbus-1/system.d/*
%{_datadir}/dbus-1/system-services/*
%dir %attr(0755,network_fw,network_fw) %{_localstatedir}/lib/stc
%config(noreplace) %{stc_db_file}*
%config(noreplace) %{stc_backup_db_file}
%{TZ_SYS_UPGRADE_SCRIPTS}/500.%{name}_upgrade.sh
%license LICENSE.APLv2

%files plugin-appstatus
%manifest %{name}.manifest
%{_datadir}/icons/*.png
%{_libdir}/stc-plugin-appstatus.so
%license LICENSE.APLv2

%files plugin-exception
%manifest %{name}.manifest
%{_libdir}/stc-plugin-exception.so
%license LICENSE.APLv2

%files plugin-procfs
%manifest %{name}.manifest
%{_libdir}/stc-plugin-procfs.so
%license LICENSE.APLv2

%files plugin-pcap
%manifest %{name}.manifest
%{_libdir}/stc-plugin-pcap.so
%license LICENSE.APLv2

%files plugin-tether
%manifest %{name}.manifest
%{_libdir}/stc-plugin-tether.so
%license LICENSE.APLv2

%files plugin-monitor
%manifest %{name}.manifest
%{_libdir}/stc-plugin-monitor.so
%license LICENSE.APLv2

%files plugin-firewall
%manifest %{name}.manifest
%{_libdir}/stc-plugin-firewall.so
%license LICENSE.APLv2
