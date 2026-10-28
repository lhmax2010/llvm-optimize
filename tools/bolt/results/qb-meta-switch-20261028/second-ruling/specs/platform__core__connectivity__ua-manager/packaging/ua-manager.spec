Name:       ua-manager
Summary:    User awareness manager
Version:    0.14.18
Release:    1
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:	ua-manager.conf
Source2:	net.uamd.service
Source3:	ua-manager.service
Source1001: ua-manager.manifest

%define database_full_path /opt/dbspace/.ua-manager-data.db
#%define config_file_path /opt/usr/data/ua

BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-creds-gdbus)

%if 0%{?gtests:1}
BuildRequires:  pkgconfig(gmock)
%endif

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
User awareness manager

%package devel
Summary:    User awareness manager APIs.
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
This package contains User Awareness manager APIs.

%package plugins
Summary:    UA framework plugin interface
Requires:   %{name} = %{version}-%{release}

%description plugins
This package contains User Awareness plugin interfaces.

%prep
%setup -q
cp -a %{SOURCE1} .
cp -a %{SOURCE2} .
cp -a %{SOURCE3} .
cp %{SOURCE1001} .

%build

%if 0%{?gcov:1}
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DBIN_INSTALL_DIR=%{_bindir} \
	-DINCLUDE_INSTALL_DIR=%{_includedir} \
	-DLIB_PATH=%{_lib} \
	-DFULLVER=%{version} \
	-DMAJORVER=${MAJORVER} \
	-DDBPATH=%{database_full_path} \
	-DBUILD_GCOV=%{?gcov:1}%{!?gcov:0} \
	-DBUILD_GTESTS=%{?gtests:1}%{!?gtests:0}

%install
%make_install

mkdir -p %{buildroot}%{_datadir}
install -p -m 500 ua-manager.sh %{buildroot}%{_datadir}/ua-manager.sh

#database initialization
mkdir -p %{buildroot}/opt/dbspace
sqlite3 %{buildroot}%{database_full_path} < %{buildroot}/usr/share/ua_db.sql
mkdir -p %{buildroot}/opt/usr/share/data/network/ua/share
#rm %{buildroot}/usr/share/ua_db.sql

mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
cp ua-manager.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/ua-manager.conf
mkdir -p %{buildroot}%{_datadir}/dbus-1/system-services/
cp net.uamd.service %{buildroot}%{_datadir}/dbus-1/system-services/net.uamd.service
mkdir -p %{buildroot}%{_unitdir}
cp ua-manager.service %{buildroot}%{_unitdir}/ua-manager.service

%post
/sbin/ldconfig

/usr/bin/chsmack -a 'System' %{database_full_path}
/usr/bin/chsmack -a 'System' %{database_full_path}-journal

if [ -d /usr/share/upgrade/vd_scripts/additional_scripts ]; then
    mv /usr/share/ua-manager.sh /usr/share/upgrade/vd_scripts/additional_scripts/
else
    rm /usr/share/ua-manager.sh
fi

%postun
/sbin/ldconfig
rm /usr/share/upgrade/vd_scripts/additional_scripts/ua-manager.sh

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-, root, root)
%attr(644,-,-) %{_libdir}/libua-api.so.*
%attr(755,network_fw,network_fw) %{_bindir}/ua-manager
%config %{_sysconfdir}/dbus-1/system.d/ua-manager.conf
%attr(644,root,root) %{_datadir}/dbus-1/system-services/*
%attr(644,root,root) %{_unitdir}/ua-manager.service
%config %attr(660, network_fw, network_fw) %{database_full_path}
%config %attr(660, network_fw, network_fw) %{database_full_path}-journal
%config %attr(660, network_fw, network_fw) /usr/share/ua_db.sql
%attr(770, network_fw, network_fw) /opt/data/network/ua/share/create-ua-db.sh
%attr(755,-,-) %{TZ_SYS_UPGRADE_SCRIPTS}/500.%{name}_upgrade.sh
%{_datadir}/ua-manager.sh

%files devel
%defattr(-, root, root)
%{_includedir}/ua-manager/ua-api.h
%{_includedir}/ua-manager/ua-api-product.h
%{_libdir}/pkgconfig/ua-api.pc
%%attr(644,-,-) %{_libdir}/libua-api.so

%files plugins
%defattr(-, root, root)
%{_includedir}/ua-manager/plugins/ua-plugin-type.h
%{_includedir}/ua-manager/plugins/ua-plugin.h
%{_includedir}/ua-manager/plugins/ua-vendor-plugin.h
%{_includedir}/ua-manager/plugins/ua-cloud-plugin.h
%{_libdir}/pkgconfig/ua-plugins.pc
