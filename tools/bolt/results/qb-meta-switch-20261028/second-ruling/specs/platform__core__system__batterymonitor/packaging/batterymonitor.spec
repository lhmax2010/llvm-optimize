Name:		batterymonitor
Summary:	batterymonitor service daemon
Version:	0.0.7
Release:	1
License:	Apache-2.0
Source0:	%{name}-%{version}.tar.gz
Source1:	org.tizen.battery.monitor.service
Source2:	org.tizen.battery.monitor.conf
Source3:	batterymonitor.service
Source4:	batterymonitor.manifest

BuildRequires:  cmake
BuildRequires:  python3-setuptools
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(capi-system-runtime-info)
BuildRequires:  pkgconfig(glib-2.0) >= 2.26
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(db-util)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-session)
BuildRequires:  pkgconfig(cynara-creds-gdbus)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(json-c)
BuildRequires:  pkgconfig(capi-appfw-job-scheduler)
BuildRequires:  pkgconfig(capi-system-device)
BuildRequires:  pkgconfig(dumpsys-system)
BuildRequires:  pkgconfig(capi-network-wifi-manager)
BuildRequires:  pkgconfig(capi-network-bluetooth)
BuildRequires:  pkgconfig(capi-network-connection)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(tapi)
BuildRequires:  pkgconfig(capi-appfw-app-manager)
BuildRequires:  pkgconfig(libsyscommon)

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%define power_profile_config_path /usr/etc/batterymonitor/config

%define dump_dummy OFF

%description
Battery-Monitor Service Daemon


%prep
%setup -q
cp -a %{SOURCE1} .
cp -a %{SOURCE2} .
cp -a %{SOURCE3} .
cp %{SOURCE4} .

%build
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} \
		-DLIB_INSTALL_DIR=%{_libdir} \
		-DBIN_INSTALL_DIR=%{_bindir} \
		-DINCLUDE_INSTALL_DIR=%{_includedir} \
		-DLIB_PATH=%{_lib} \
		-DFULLVER=%{version} \
		-DMAJORVER=${MAJORVER} \
		-DDUMP_DUMMY=%{dump_dummy}

%install
%make_install
mkdir -p %{buildroot}/usr/etc/batterymonitor/config
cp config/bm_params.json %{buildroot}%{power_profile_config_path}
cp config/bm_power_profile_params_*.json %{buildroot}%{power_profile_config_path}

mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
cp org.tizen.battery.monitor.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/org.tizen.battery.monitor.conf

mkdir -p %{buildroot}%{_datadir}/dbus-1/system-services/
cp org.tizen.battery.monitor.service %{buildroot}%{_datadir}/dbus-1/system-services/org.tizen.battery.monitor.service

mkdir -p %{buildroot}%{_unitdir}/multi-user.target.wants
cp batterymonitor.service %{buildroot}%{_unitdir}/batterymonitor.service
ln -s ../batterymonitor.service %{buildroot}%{_unitdir}/multi-user.target.wants/batterymonitor.service

rm %{buildroot}%{_includedir}/battery_monitor_stub.h


%post
/sbin/ldconfig

mkdir -p %{TZ_SYS_DB}
if [ ! -f %{TZ_SYS_DB}/.battery-monitor.db ]
then
	sqlite3 %{TZ_SYS_DB}/.battery-monitor.db 'PRAGMA journal_mode = PERSIST;
	CREATE TABLE if not exists appid_map (id INTEGER PRIMARY KEY AUTOINCREMENT, AppId TEXT);
	CREATE TABLE if not exists appid_usage (AppId TEXT, log_time INT, rId_ble INT, rId_wifi INT, rId_cpu INT, rId_display INT, rId_device_network INT,
	rId_gps INT, rId_battery INT);
	CREATE TABLE if not exists resourceid_usage (ResourceId TEXT, log_time INT, usage INT);
	CREATE TABLE if not exists res_base_usage (ResourceId TEXT, log_time INT, usage INT);
	CREATE TABLE if not exists gble_stat (time_s LONG INT, ble_idle_time INT, ble_rx_time INT, ble_tx_time INT, ble_pwi_val INT);
	CREATE TABLE if not exists gwfl_stat (time_s LONG INT, wifi_on_time INT, wifi_conn_time INT, wifi_idle_time INT,
	wifi_rx_time INT, wifi_tx_time INT, wifi_pwi_val INT);
	CREATE TABLE if not exists gn_stat (time_s LONG INT, dn_rx_byt INT, dn_tx_byt INT, wifi_rx_byt INT, wifi_tx_byt INT,
	dn_rx_pkt INT, dn_tx_pkt INT, wifi_rx_pkt INT, wifi_tx_pkt INT, bt_rx_byt INT, bt_tx_byt INT);
	CREATE TABLE if not exists gbr_stat (time_s LONG INT, dark INT, dim INT, medium INT, light INT, bright INT);
	CREATE TABLE if not exists gsgt_stat (time_s LONG INT, scan_time INT, none_time INT, poor_time INT, med_time INT,
	good_time INT, grt_time INT);
	CREATE TABLE if not exists gwst_stat (time_s LONG INT, wscan_time INT, wnone_time INT, wpoor_time INT, wmed_time INT,
	wgood_time INT, wgrt_time INT);
	CREATE TABLE if not exists gbst_stat (time_s LONG INT, off_time INT, low_time INT, med_time INT, high_time INT);
	CREATE TABLE if not exists gcpu_stat (time_s LONG INT, usr_time INT, sys_time INT);
'
fi

chown service_fw:service_fw %{TZ_SYS_DB}/.battery-monitor.db
chown service_fw:service_fw %{TZ_SYS_DB}/.battery-monitor.db-journal

chmod 644 %{TZ_SYS_DB}/.battery-monitor.db
chmod 644 %{TZ_SYS_DB}/.battery-monitor.db-journal

#smack labeling
chsmack -a "System" %{TZ_SYS_DB}/.battery-monitor.db
chsmack -a "System" %{TZ_SYS_DB}/.battery-monitor.db-journal

%posttrans
# Read model name
while read line; do
	if [[ "${line}" =~ "tizen.org/system/model_name" ]]; then
		model=$(echo ${line} | sed -e 's/<.*>\(.*\)<.*>/\1/' | sed -e 's/[[:space:]]//g')
		echo "model_name =" ${model}

		# If there is power parameter file for this model, link it
		if [ -f %{power_profile_config_path}/bm_power_profile_params_${model}.json ]; then
			echo "Use parameter file for" ${model}
			ln -s %{power_profile_config_path}/bm_power_profile_params_${model}.json %{power_profile_config_path}/bm_power_profile_params.json
		else
			echo "There is no parameter file for" ${model}
		fi
	fi
done < /etc/config/model-config.xml

# Otherwise, link dummy parameter file
if [ ! -L %{power_profile_config_path}/bm_power_profile_params.json ]; then
	echo "Use dummy paremeter file"
	ln -s %{power_profile_config_path}/bm_power_profile_params_dummy.json %{power_profile_config_path}/bm_power_profile_params.json
fi

chsmack -a "_" %{power_profile_config_path}/bm_power_profile_params.json

%postun
/sbin/ldconfig

# Remove symbolic link
if [ -L %{power_profile_config_path}/bm_power_profile_params.json ]; then
	unlink %{power_profile_config_path}/bm_power_profile_params.json
fi

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root)
%attr(755,-,-) %{_bindir}/batterymonitor-svcd
%config %{_sysconfdir}/dbus-1/system.d/org.tizen.battery.monitor.conf
%config %attr(755,root,root) %{power_profile_config_path}/bm_params.json
%config %attr(755,root,root) %{power_profile_config_path}/bm_power_profile_params_*.json
%attr(644,root,root) %{_datadir}/dbus-1/system-services/*
%attr(644,root,root) %{_unitdir}/batterymonitor.service
%attr(644,root,root) %{_unitdir}/multi-user.target.wants/batterymonitor.service
