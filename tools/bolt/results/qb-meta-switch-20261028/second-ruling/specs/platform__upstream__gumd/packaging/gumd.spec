# define used dbus type [p2p, system]
%define dbus_type system
# enable debug features such as control environment variables
# WARNING! do not use for production builds as it will break security
%define debug_build 0

%define GUMD_DBUS_SERVICE "src/daemon/dbus/services/org.O1.SecurityAccounts.gUserManagement.service"

Name:    gumd
Summary: User management daemon and client library
Version: 1.0.8
Release: 0
Group:   Security/Accounts
License: LGPL-2.1+
URL:     https://github.com/01org/gumd
Source:  %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest
Source1002:     libgum.manifest
Requires:       libgum = %{version}-%{release}
Conflicts: gum
%if %{dbus_type} != "p2p"
Requires: dbus-1
%endif
Requires(post):   /sbin/ldconfig
Requires(post):   /usr/bin/getent
Requires(post):   /usr/sbin/groupadd
Requires(postun): /sbin/ldconfig
BuildRequires: python3-setuptools
BuildRequires: pkgconfig(systemd)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(gtk-doc)
BuildRequires: pkgconfig(glib-2.0) >= 2.38
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(gmodule-2.0)
BuildRequires: pkgconfig(libtzplatform-config)
Requires:      security-config
Requires:      tizen-platform-config
Provides:      gumd-profile_common = %{version}-%{release}
Provides:      gumd-profile_mobile = %{version}-%{release}
Provides:      gumd-profile_tv = %{version}-%{release}
Provides:      gumd-profile_ivi = %{version}-%{release}

%description
%{summary} files

%package profile_wearable
Summary:	GUMD extension for Tizen Wearable
Requires:	gumd = %{version}-%{release}

%description profile_wearable
GUMD extension for Tizen Wearable.
This extension supports wearable specific gumd.service file.

%package -n libgum
Summary:    User management client library
Group:      Security/Libraries
Requires:   %{name} = %{version}-%{release}


%description -n libgum
%{summary} files


%package -n gum-utils
Summary:    User management utility tool
Group:      Security/Libraries
Requires:   libgum = %{version}-%{release}


%description -n gum-utils
%{summary} files


%package -n libgum-devel
Summary:    Development files for user management client library
Group:      Security/Libraries
Requires:   libgum = %{version}-%{release}


%description -n libgum-devel
%{summary} files


%package doc
Summary:    Documentation files for %{name}
Group:      Security/Documentation
Requires:   libgum = %{version}-%{release}


%description doc
%{summary} files


%prep
%setup -q -n %{name}-%{version}
cp -a %{SOURCE1001} %{name}.manifest
cp -a %{SOURCE1002} libgum.manifest
cp data/gumd.service data/gumd.service.wearable
%ifarch x86_64
%define emul_arch x86_64
%endif

%if "%{tizen_profile_name}" == "tv" && "%{emul_arch}" != "x86_64"
mv "%{GUMD_DBUS_SERVICE}".vd.in "%{GUMD_DBUS_SERVICE}".in
%else
mv "%{GUMD_DBUS_SERVICE}".common.in "%{GUMD_DBUS_SERVICE}".in

# wearable
echo "CapabilityBoundingSet=~CAP_MAC_ADMIN" >> data/gumd.service.wearable
echo "SmackProcessLabel=System" >> data/gumd.service.wearable
# non-wearable
echo "SmackProcessLabel=System::Privileged" >> data/gumd.service
%endif

%build
autoreconf -ivf
%if %{debug_build} == 1
%configure --enable-dbus-type=%{dbus_type} --enable-debug
%else
%configure --enable-dbus-type=%{dbus_type}
%endif
%__make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install
rm -f %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -m 755 -d %{buildroot}%{_sysconfdir}/%{name}
install -m 644 data/tizen/etc/%{name}/%{name}-tizen-common.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -m 755 -d %{buildroot}%{_unitdir}
install -m 644 data/gumd.service.wearable %{buildroot}%{_unitdir}
%if "%{tizen_profile_name}" == "tv" && "%{emul_arch}" == "x86_64"
install -m 644 data/gumd.service %{buildroot}%{_unitdir}
%endif
%if "%{tizen_profile_name}" != "tv"
install -m 644 data/gumd.service %{buildroot}%{_unitdir}
install -m 755 -d %{buildroot}/usr/share/platform-extension
install -m 755 scripts/700.gumd-platform-extension-migration.sh %{buildroot}/usr/share/platform-extension/
%endif

%post
ldconfig
getent group gumd > /dev/null || groupadd -r -g 205 gumd
install -d -m 755 %{_sysconfdir}/%{name}/useradd.d
install -d -m 755 %{_sysconfdir}/%{name}/userdel.d
install -d -m 755 %{_sysconfdir}/%{name}/groupadd.d
install -d -m 755 %{_sysconfdir}/%{name}/groupdel.d
install -d -m 755 %{_localstatedir}/lib/%{name}/user
touch /opt%{_sysconfdir}/.pwd.lock
if [ -e "%{_sysconfdir}/.pwd.lock" ]; then
    rm -f %{_sysconfdir}/.pwd.lock
fi
ln -s /opt%{_sysconfdir}/.pwd.lock %{_sysconfdir}/.pwd.lock

%postun -p /sbin/ldconfig

%post -n libgum -p /sbin/ldconfig
%postun -n libgum -p /sbin/ldconfig

%post profile_wearable
# Uses different service file (overwrite non wearable)
mv %{_unitdir}/gumd.service.wearable %{_unitdir}/gumd.service
# This does not support complete unisntall because gumd.service
# is not going to be recovered. Users should reinstall gumd
# to get it recovered after uninstalling profile_wearable

%files -n libgum
%defattr(-,root,root,-)
%manifest libgum.manifest
%license COPYING.LIB
%{_libdir}/libgum*.so.*

%files -n gum-utils
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license COPYING.LIB
%{_bindir}/gum-utils

%files -n libgum-devel
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_includedir}/gum/*
%{_libdir}/libgum*.so
%{_libdir}/pkgconfig/libgum.pc
%if %{dbus_type} != "p2p"
%{_datadir}/dbus-1/interfaces/*UserManagement*.xml
%endif

%files
%defattr(-,root,root,-)
%manifest %{name}.manifest
%doc AUTHORS COPYING.LIB NEWS README
%license COPYING.LIB
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%if %{dbus_type} == "system"
%dir %{_datadir}/dbus-1/system-services
%{_datadir}/dbus-1/system-services/*UserManagement*.service
%dir %{_sysconfdir}/dbus-1
%dir %{_sysconfdir}/dbus-1/system.d
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/gumd-dbus.conf
%if "%{tizen_profile_name}" == "tv" && "%{emul_arch}" == "x86_64"
%{_unitdir}/gumd.service
%endif
%if "%{tizen_profile_name}" != "tv"
%{_unitdir}/gumd.service
/usr/share/platform-extension/700.gumd-platform-extension-migration.sh
%endif
%endif

%files profile_wearable
%license COPYING.LIB
%{_unitdir}/gumd.service.wearable

%files doc
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_datadir}/gtk-doc/html/gumd/*
