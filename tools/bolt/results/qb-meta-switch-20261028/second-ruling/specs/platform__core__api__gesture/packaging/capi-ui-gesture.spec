Name:       capi-ui-gesture
Summary:    Gesture client library and daemon
Version:    1.60.2
Release:    1
Group:      Graphics & UI Framework/Input
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    capi-ui-gesture.service
Source2:    org.tizen.gesture.server.service
Source3:    capi-ui-gesture.conf
BuildRequires:  cmake, coreutils
BuildRequires:  pkgconfig(capi-appfw-app-common)
BuildRequires:  pkgconfig(capi-appfw-app-control)
BuildRequires:  pkgconfig(capi-appfw-app-manager)
BuildRequires:  pkgconfig(capi-appfw-package-manager)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-session)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(aul)
Requires:       security-config
Requires(post): /sbin/ldconfig
Requires(post): dbus
Requires(postun): /sbin/ldconfig

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
Gesture client library and daemon

%package devel
Summary:    Gesture client library and daemon (Development)
Group:      Graphics & UI Framework/Input
Requires:   %{name} = %{version}-%{release}

%description devel
Gesture client library and daemon (Development)

%if 0%{?gcov:1}
%package gcov
Summary:  Gesture client library and daemon (gcov)
Group:      Graphics & UI Framework/Input
%description gcov
Gesture client library and daemon (gcov)
%endif

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE2} .

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

export CFLAGS+=" -DTIZEN_DEBUG_ENABLE -fvisibility=hidden -Werror"
export CXXFLAGS+=" -DTIZEN_DEBUG_ENABLE -fvisibility=hidden -Werror"
export FFLAGS+=" -DTIZEN_DEBUG_ENABLE -fvisibility=hidden"

%cmake . -DCMAKE_INSTALL_PREFIX=/usr -DLIBDIR=%{_libdir} -DBINDIR=%{_bindir} -DINCLUDEDIR=%{_includedir} \
         -DTZ_SYS_RO_SHARE=%TZ_SYS_RO_SHARE -DTZ_SYS_BIN=%TZ_SYS_BIN -DTZ_SYS_SHARE=%TZ_SYS_SHARE
make %{?jobs:-j%jobs}

%if 0%{?gcov:1}
mkdir -p gcov-obj
find . -name '*_dbus.c.gcno' -exec rm {} \;
find . -name '*.gcno' -exec cp '{}' gcov-obj ';'
%endif

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}%{_prefix}/lib/systemd/system
install -m 0644 %SOURCE1 %{buildroot}%{_unitdir}/capi-ui-gesture.service

mkdir -p %{buildroot}%{_datadir}/dbus-1/system-services
install -m 0644 %SOURCE2 %{buildroot}%{_datadir}/dbus-1/system-services/org.tizen.gesture.server.service

mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
install -m 0644 %SOURCE3 %{buildroot}%{_sysconfdir}/dbus-1/system.d/capi-ui-gesture.conf

%if 0%{?gcov:1}
mkdir -p %{buildroot}%{_datadir}/gcov/obj
install -m 0644 gcov-obj/* %{buildroot}%{_datadir}/gcov/obj
%endif

#%if 0%{?gcov:1}
#lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d . -o gcov.info
#genhtml gcov.info
#%endif

mkdir -p %{buildroot}/etc/dbus-1/system.d/
cp %{SOURCE3} %{buildroot}/etc/dbus-1/system.d/capi-ui-gesture.conf

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/lib*.so
%attr(0755,ui_fw,ui_fw) %{_bindir}/gesture-server
%attr(0644,root,root) %{_datadir}/gesture/capi-ui-gesture-gdbus.xml
%attr(0644,root,root) %{_unitdir}/capi-ui-gesture.service
%attr(0644,root,root) %{_datadir}/dbus-1/system-services/org.tizen.gesture.server.service
%config %{_sysconfdir}/dbus-1/system.d/capi-ui-gesture.conf

%files devel
%manifest %{name}-devel.manifest
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/capi-ui-gesture-client.pc
%{_libdir}/pkgconfig/capi-ui-gesture-engine.pc
%{_includedir}/gesture.h
%{_includedir}/gesture_internal.h
%{_includedir}/gesture_engine.h
%{_includedir}/gesture_common.h
%{_includedir}/gesture_common_internal.h
%{_includedir}/gesture_data_info.h

%config(noreplace) /etc/dbus-1/system.d/capi-ui-gesture.conf

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
