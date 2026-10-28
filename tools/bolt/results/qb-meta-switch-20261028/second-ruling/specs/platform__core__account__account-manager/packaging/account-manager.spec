Name:       account-manager
Summary:    Account Manager
Version:    0.1.23
Release:    1
Group:      Social & Content/Other
License:    Apache-2.0
Source0:    account-manager-%{version}.tar.gz
Source1:    org.tizen.account.manager.service
Source2:    org.tizen.account.manager.conf
Source3:    accounts-service.service

BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(db-util)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:	pkgconfig(glib-2.0) >= 2.26
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-session)
BuildRequires:  pkgconfig(cynara-creds-gdbus)
BuildRequires:  pkgconfig(cynara-uid)
BuildRequires:  pkgconfig(account-common)
BuildRequires:  pkgconfig(libtzplatform-config)

Requires(post): /sbin/ldconfig
Requires(post): /usr/bin/sqlite3
Requires(postun): /sbin/ldconfig

%define upgrade_script_path		/usr/share/upgrade/scripts

%description
Account Daemon: no

%prep
%setup -q
cp %{SOURCE1} .

%build
#export   CFLAGS+=" -Wextra -Wcast-align -Wcast-qual -Wshadow -Wwrite-strings -Wswitch-default"
#export CXXFLAGS+=" -Wextra -Wcast-align -Wcast-qual -Wshadow -Wwrite-strings -Wswitch-default -Wnon-virtual-dtor -Wno-c++0x-compat"
#export   CFLAGS+=" -Wno-unused-parameter -Wno-empty-body"
#export CXXFLAGS+=" -Wno-unused-parameter -Wno-empty-body"

#export   CFLAGS+=" -fno-omit-frame-pointer -fno-optimize-sibling-calls -fno-strict-aliasing -fno-unroll-loops -fsigned-char -fstrict-overflow -fno-common"
#export CXXFLAGS+=" -fno-omit-frame-pointer -fno-optimize-sibling-calls -fno-strict-aliasing -fno-unroll-loops -fsigned-char -fstrict-overflow"

export CFLAGS="${CFLAGS} -fvisibility=hidden -fPIE"
export LDFLAGS="${LDFLAGS} -pie"
cmake . -DCMAKE_INSTALL_PREFIX=/usr -DLIBDIR=%{_libdir}

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

rm -rf %{buildroot}/usr/lib/account-manager

mkdir -p %{buildroot}/usr/share/dbus-1/system-services
install -m 0644 %SOURCE1 %{buildroot}/usr/share/dbus-1/system-services/org.tizen.account.manager.service

mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/dbus-1/system.d/

mkdir -p %{buildroot}%{_unitdir}/delayed.target.wants
install -m 644 %SOURCE3 %{buildroot}%{_unitdir}/accounts-service.service
%install_service delayed.target.wants accounts-service.service

mkdir -p %{buildroot}%{upgrade_script_path}
cp -f scripts/500.account-manager.sh %{buildroot}%{upgrade_script_path}

mkdir -p %{buildroot}%{_datadir}/upgrade/vd_scripts/additional_scripts
install -p -m 500 scripts/account-manager.sh %{buildroot}%{_datadir}/upgrade/vd_scripts/additional_scripts/account-manager.sh

%post
/sbin/ldconfig
#if [ ! -d /opt/usr/dbspace ]
#then
#        mkdir -p /opt/usr/dbspace
#fi
mkdir -p %{TZ_SYS_DB}
if [ ! -f %{TZ_SYS_DB}/.account.db ]
then
        sqlite3 %{TZ_SYS_DB}/.account.db 'PRAGMA journal_mode = PERSIST;
        CREATE TABLE if not exists label (AppId TEXT, Label TEXT, Locale TEXT);
        CREATE TABLE if not exists account_type (_id INTEGER PRIMARY KEY AUTOINCREMENT, AppId TEXT,
        ServiceProviderId TEXT, IconPath TEXT, SmallIconPath TEXT, MultipleAccountSupport INT);
        CREATE TABLE if not exists account_custom (AccountId INTEGER, AppId TEXT, Key TEXT, Value TEXT);
        CREATE TABLE if not exists account (_id INTEGER PRIMARY KEY AUTOINCREMENT, user_name TEXT, email_address TEXT, display_name TEXT, icon_path TEXT,
        source TEXT, package_name TEXT, access_token TEXT, domain_name TEXT, auth_type INTEGER, secret INTEGER, sync_support INTEGER,
        txt_custom0 TEXT, txt_custom1 TEXT, txt_custom2 TEXT, txt_custom3 TEXT, txt_custom4 TEXT,
        int_custom0 INTEGER, int_custom1 INTEGER, int_custom2 INTEGER, int_custom3 INTEGER, int_custom4 INTEGER);
        CREATE TABLE if not exists capability (_id INTEGER PRIMARY KEY AUTOINCREMENT, key TEXT, value INTEGER,
	package_name TEXT, user_name TEXT,  account_id INTEGER, FOREIGN KEY (account_id) REFERENCES account(_id));
	CREATE TABLE if not exists provider_feature (app_id TEXT, key TEXT);
	CREATE TABLE if not exists deleted_account (_id INTEGER, user_name TEXT, email_address TEXT, display_name TEXT, icon_path TEXT, source TEXT,
	package_name TEXT, access_token TEXT, domain_name TEXT, auth_type INTEGER, secret INTEGER, sync_support INTEGER, txt_custom0 TEXT, txt_custom1 TEXT,
	txt_custom2 TEXT, txt_custom3 TEXT, txt_custom4 TEXT, int_custom0 INTEGER, int_custom1 INTEGER, int_custom2 INTEGER, int_custom3 INTEGER, int_custom4 INTEGER);
	CREATE TABLE if not exists deleted_capability (_id INTEGER, key TEXT, value INTEGER, package_name TEXT, user_name TEXT, account_id INTEGER);
	CREATE TABLE if not exists deleted_account_custom (AccountId INTEGER, AppId TEXT, Key TEXT, Value TEXT);
	CREATE TRIGGER if not exists aft_acc_del AFTER DELETE ON account BEGIN INSERT INTO deleted_account VALUES (old._id, old.user_name, old.email_address,
	old.display_name, old.icon_path, old.source, old.package_name, old.access_token, old.domain_name, old.auth_type, old.secret, old.sync_support,
	old.txt_custom0, old.txt_custom1, old.txt_custom2, old.txt_custom3, old.txt_custom4, old.int_custom0, old.int_custom1, old.int_custom2,
	old.int_custom3, old.int_custom4); END;
	CREATE TRIGGER if not exists aft_capa_del AFTER DELETE ON capability BEGIN INSERT INTO deleted_capability VALUES (old._id, old.key, old.value, old.package_name,
	old.user_name, old.account_id); END;
	CREATE TRIGGER if not exists aft_cust_del AFTER DELETE ON account_custom BEGIN INSERT INTO deleted_account_custom VALUES (old.AccountId, old.AppId,
	old.Key, old.Value); END;
'
fi

chown service_fw:service_fw %{TZ_SYS_DB}/.account.db
chown service_fw:service_fw %{TZ_SYS_DB}/.account.db-journal

chmod 644 %{TZ_SYS_DB}/.account.db
chmod 644 %{TZ_SYS_DB}/.account.db-journal

#smack labeling
chsmack -a 'System' %{TZ_SYS_DB}/.account.db-journal
chsmack -a 'System' %{TZ_SYS_DB}/.account.db
%postun -p /sbin/ldconfig


%files
%manifest account-svcd.manifest
#%defattr(-,system,system,-)
%config %{_sysconfdir}/dbus-1/system.d/org.tizen.account.manager.conf
%license LICENSE.APLv2
%{_bindir}/account-svcd
%{upgrade_script_path}/500.account-manager.sh
%{_datadir}/upgrade/vd_scripts/additional_scripts/account-manager.sh
%attr(0644,root,root) %{_unitdir}/accounts-service.service
%attr(0644,root,root) %{_unitdir}/delayed.target.wants/accounts-service.service
%attr(0644,root,root) /usr/share/dbus-1/system-services/org.tizen.account.manager.service

