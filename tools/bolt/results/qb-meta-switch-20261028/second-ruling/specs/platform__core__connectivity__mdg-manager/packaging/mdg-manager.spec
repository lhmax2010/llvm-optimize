Name:       mdg-manager
Summary:    Multi Device Group Manager
Version:    0.0.1
Release:    0
Group:      Network & Connectivity/Other
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
Source2:    mdgd.service
Source3:    net.mdgd.service

BuildRequires: cmake
BuildRequires: pkgconfig(iotivity)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(json-glib-1.0)
BuildRequires: pkgconfig(uuid)
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(boost)
BuildRequires: pkgconfig(capi-network-wifi-manager)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(gmock)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(capi-system-system-settings)
BuildRequires: pkgconfig(storage)
Requires: capi-system-system-settings
%description
Multi Device Group Manager

%prep
%setup -q
chmod 644 %{SOURCE0}
chmod 644 %{SOURCE1}
chmod 644 %{SOURCE2}
chmod 644 %{SOURCE3}

cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .

%build
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

# Check whether iotivity support MULTIPLE_OWNER feature
mot_support=`/usr/bin/nm -D -C %{_libdir}/liboctbstack.so | awk '/IsSubOwner/{print $3}'`
%define NETWORK_FW_DATADIR %{TZ_SYS_GLOBALUSER_DATA}/network
%define DBDIR %{TZ_SYS_GLOBALUSER_DATA}/

%cmake . \
    -DMAJORVER=${MAJORVER} \
	-DFULLVER=%{version} \
	-DLIB_DIR=%{_libdir} \
	-DBIN_DIR=%{_bindir} \
	-DSBIN_DIR=%{_sbindir} \
	-DNETWORK_FW_DATADIR=%{NETWORK_FW_DATADIR} \
	-DISSUBOWNER=${mot_support} \
	-DDBDIR=%{DBDIR} \

%install
rm -rf %{buildroot}/BUILD/%{name}*

mkdir -p %{buildroot}/etc/dbus-1/system.d/
mkdir -p %{buildroot}/opt/usr/data/network/lib
cp -af %{_builddir}/%{name}-%{version}/packaging/org.tizen.mdg.conf %{buildroot}/etc/dbus-1/system.d/

%make_install

mkdir -p %{buildroot}%{_datadir}/dbus-1/system-services/

cp %{SOURCE3} %{buildroot}%{_datadir}/dbus-1/system-services/net.mdgd.service
mkdir -p %{buildroot}%{_unitdir}
cp %{SOURCE2} %{buildroot}%{_unitdir}/mdgd.service

mkdir -p %{buildroot}%{_unitdir}

%postun
rm -rf %{NETWORK_FW_DATADIR}/*.db
rm -rf %{NETWORK_FW_DATADIR}/*.db-journal
rm -rf /opt/usr/dbspace/.mdgd.db
rm -rf /opt/usr/dbspace/.mdgd.db-journal

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_bindir}/mdgd
%attr(644,root,root) %{_datadir}/dbus-1/system-services/*
%attr(644,root,root) %{_unitdir}/mdgd.service
%attr(644,network_fw,network_fw) %{NETWORK_FW_DATADIR}/oic_svr_db_mdgd_manager.dat
%attr(644,root,root) /etc/dbus-1/system.d/org.tizen.mdg.conf
