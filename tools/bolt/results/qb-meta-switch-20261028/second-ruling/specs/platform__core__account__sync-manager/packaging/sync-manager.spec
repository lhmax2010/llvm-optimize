# To not create auto-provides for extension replacement shared objects
%global __provides_exclude_from ^.*\\.extension-calendar

Name:      sync-service
Version:   0.3.47
Release:   1
License:   Apache-2.0
Summary:   Sync manager daemon
Group:     Social & Content/API
Source0:   %{name}-%{version}.tar.gz
Source1:   sync-manager.service
Source2:   org.tizen.sync.service
Source3:   org.tizen.sync.conf

BuildRequires: cmake
BuildRequires: pkgconfig(capi-appfw-app-manager)
BuildRequires: pkgconfig(capi-appfw-application)
BuildRequires: pkgconfig(capi-network-connection)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(appcore-efl)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(db-util)
BuildRequires: pkgconfig(pkgmgr)
BuildRequires: pkgconfig(pkgmgr-info)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(vconf-internal-keys)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(glib-2.0) >= 2.26
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(accounts-svc)
BuildRequires: pkgconfig(alarm-service)
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(cynara-client)
BuildRequires: pkgconfig(cynara-session)
BuildRequires: pkgconfig(cynara-creds-gdbus)
BuildRequires: pkgconfig(calendar-service2)
BuildRequires: pkgconfig(contacts-service2)
BuildRequires: pkgconfig(capi-content-media-content)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: python3-setuptools

%description
sync manager service and sync framework which manages sync of registered applications

%package -n libcore-sync-client
Summary:    Sync manager client library
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description -n libcore-sync-client
sync client provides sync adapter functionality to register sync adapters and to get callbacks.

%package -n libcore-sync-client-devel
Summary:    Sync manager client library (Development)
Group:      Application Framework/Development

%description -n  libcore-sync-client-devel
sync client provides sync adapter functionality to register sync adapters and to get callbacks.

%if 0%{?gcov:1}
%package gcov
Summary:    Sync Manager Framwework library (gcov)
Group:      Service Framework/Testing

%description gcov
gcov objects for coverage test
%endif

%define _pkgdir /usr

%prep
%setup -q
cp %{SOURCE2} .

%build
_FEATURE_CONTAINER_ENABLE=OFF

%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

cmake \
	-DCMAKE_INSTALL_PREFIX=%{_pkgdir} \
	-DPACKAGE_NAME=%{name} \
	-DBINDIR=%{_bindir} \
	-DLIBDIR=%{_libdir} \
	-DINCLUDEDIR=%{_includedir} \
	-D_FEATURE_CONTAINER_ENABLE:BOOL=${_FEATURE_CONTAINER_ENABLE} \
	-DVERSION=%{version}

make %{?jobs:-j%jobs}

%install
%make_install
%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*stub*.gcno' -exec rm {} \;
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

mkdir -p %{buildroot}%{_unitdir_user}/delayed.target.wants
install -m 0644 %SOURCE1 %{buildroot}%{_unitdir_user}/sync-manager.service
ln -s ../sync-manager.service %{buildroot}%{_unitdir_user}/delayed.target.wants/sync-manager.service

mkdir -p %{buildroot}/usr/share/dbus-1/services
install -m 0644 %SOURCE2 %{buildroot}/usr/share/dbus-1/services/org.tizen.sync.service

mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/session.d
install -m 0644 %SOURCE3 %{buildroot}%{_sysconfdir}/dbus-1/session.d/org.tizen.sync.conf

%post -n libcore-sync-client -p /sbin/ldconfig
%post -n libcore-sync-client-devel -p /sbin/ldconfig

%post
/sbin/ldconfig

%postun -n libcore-sync-client -p /sbin/ldconfig
%postun -n libcore-sync-client-devel -p /sbin/ldconfig

%files -n sync-service
%manifest sync-service.manifest
%license LICENSE.APLv2
%defattr(-,root,root,-)
%config %{_sysconfdir}/dbus-1/session.d/org.tizen.sync.conf
%{_bindir}/*
%{_unitdir_user}/sync-manager.service
%{_unitdir_user}/delayed.target.wants/sync-manager.service
%attr(0644,root,root) /usr/share/dbus-1/services/org.tizen.sync.service

%files -n libcore-sync-client
%manifest libcore-sync-client.manifest
%defattr(-,root,root,-)
%{_libdir}/libcore-sync-client.so.*

%license LICENSE.APLv2

%files -n libcore-sync-client-devel
%manifest libcore-sync-client.manifest
%defattr(-,root,root,-)
%{_includedir}/*sync*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcore-sync-client.so

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
