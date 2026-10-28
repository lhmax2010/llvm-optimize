%bcond_with emulator

Name:       sdbd
Summary:    SDB daemon
Version:    3.0.50
Release:    0
License:    Apache-2.0
Summary:    SDB daemon
Group:      System/Utilities
Source0:    %{name}-%{version}.tar.gz
Source10:   %{name}.manifest
Source1000:    sdbd.service
Source1004:    sdbd_tcp.socket
Source1007:    sdbd.socket
Source1010:    reset-privs.conf
Source1011:    oom-adj-1000.conf
Source1012:    emulator.conf
Source1013:    restart-on-fail.conf
Source1014:    exec.conf
Source1020:    sdbd-env-generator

BuildRequires: capi-system-info-devel >= 0.2.0
BuildRequires: cmake >= 2.8.3
BuildRequires: pkgconfig
BuildRequires: pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libtzplatform-config)
#BuildRequires: sec-product-features
BuildRequires: pkgconfig(libsmack)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(capi-system-device)

Requires: dbus
Provides:      %{name}-profile_common = %{version}-%{release}
Provides:      %{name}-profile_mobile = %{version}-%{release}
Provides:      %{name}-profile_ivi = %{version}-%{release}
Provides:      %{name}-profile_wearable = %{version}-%{release}

%description
Description: SDB daemon.

%package profile_tv
Summary:   SDB daemon extension for TV
Requires:  %{name} = %{version}-%{release}
%description profile_tv
SDB daemon extension for TV.
This changes the service unit files of the default SDB daemon service files.

%ifarch %{ix86} x86_64
%package extension-emulator
Summary:    SDB daemon for emulator
Requires:   %{name} = %{version}-%{release}
%description extension-emulator
SDB daemon for emulator

%package extension-tv-emulator
Summary:    SDB daemon for tv emulator
Requires:   %{name}-profile_tv = %{version}-%{release}
Requires:   %{name}-extension-emulator = %{version}-%{release}
%description extension-tv-emulator
SDB daemon for tv emulator
%endif // ifarch %{ix86} x86_64

%package -n sdbd-devel
Summary:	SDBD plugin API
Group:		Development/Libraries

%description -n sdbd-devel
SDBD plugin API library

%prep
%setup -q
cp %{SOURCE10} .

%build
cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DLIBDIR=%{_libdir} %{?asan:-DCMAKE_EXE_LINKER_FLAGS="-pthread"}

make %{?jobs:-j%jobs}

%install
mkdir -p %{buildroot}%{_unitdir}/sdbd.service.d/

# extension-*-emulator
%ifarch %{ix86} x86_64
install -m 0644 %SOURCE1010 %{buildroot}%{_unitdir}/sdbd.service.d/
install -m 0644 %SOURCE1011 %{buildroot}%{_unitdir}/sdbd.service.d/
install -m 0644 %SOURCE1012 %{buildroot}%{_unitdir}/sdbd.service.d/
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-generators/
install -m 0755 %SOURCE1020 %{buildroot}%{_prefix}/lib/systemd/system-generators/
mkdir -p %{buildroot}/%{_unitdir}/emulator_preinit.target.wants
ln -s %{_unitdir}/sdbd.service %{buildroot}/%{_unitdir}/emulator_preinit.target.wants/
%endif // ifarch %{ix86} x86_64

%make_install

install -m 0644 %SOURCE1000 %{buildroot}%{_unitdir}/sdbd.service
install -m 0644 %SOURCE1004 %{buildroot}%{_unitdir}/sdbd_tcp.socket
install -m 0644 %SOURCE1013 %{buildroot}%{_unitdir}/sdbd.service.d/restart-on-fail.conf
install -m 0644 %SOURCE1014 %{buildroot}%{_unitdir}/sdbd.service.d/exec.conf
install -m 0755 -d %{buildroot}%{_unitdir}/sockets.target.wants/
ln -s ../sdbd_tcp.socket %{buildroot}%{_unitdir}/sockets.target.wants/

mkdir -p %{buildroot}%{_prefix}/lib/udev/rules.d/
install -m 644 rules/99-sdbd.rules %{buildroot}%{_prefix}/lib/udev/rules.d/
install -m 0644 %SOURCE1007 %{buildroot}%{_unitdir}/sdbd.socket

mkdir -p %{buildroot}%{_prefix}/sbin
install -m 755 script/sdk_launch %{buildroot}%{_prefix}/sbin/

mkdir -p %{buildroot}%{TZ_SYS_BIN}
install -m 755 script/profile_command %{buildroot}%{TZ_SYS_BIN}/

mkdir -p %{buildroot}%{_includedir}/sdb/
install -m 0644 src/sdbd_plugin.h %{buildroot}%{_includedir}/sdb/

mkdir -p %{buildroot}%{_libdir}/pkgconfig/
install -m 0644 packaging/sdbd.pc %{buildroot}%{_libdir}/pkgconfig/

%post
. %{_sysconfdir}/tizen-platform.conf
if ! getent passwd "${TZ_SDK_USER_NAME}" > /dev/null; then
  rm -rf "${TZ_SDK_HOME}"
  useradd -u 5100 -s /bin/false -m -d "${TZ_SDK_HOME}" "${TZ_SDK_USER_NAME}"
  getent group developer > /dev/null || groupadd -g 5100 developer
  for x in app_logging crash developer; do
    usermod -A app_logging "${TZ_SDK_USER_NAME}"
  done
fi

chsmack -a "System" /sbin/sdbd-user
chsmack -e "User::Shell" /sbin/sdbd-user

%files
%manifest sdbd.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_prefix}/sbin/sdbd
%{_prefix}/sbin/sdbd-user
%{_prefix}/sbin/sdbd-service
%{_prefix}/sbin/sdk_launch
%attr(0755, root, root) %{_sysconfdir}/init.d/sdbd
%{_unitdir}/sdbd.service
%{_unitdir}/sdbd.socket
%{_unitdir}/sdbd_tcp.socket
%{_unitdir}/sockets.target.wants/sdbd_tcp.socket
%{_prefix}/lib/udev/rules.d/99-sdbd.rules
%{TZ_SYS_BIN}/profile_command
%{_sysconfdir}/sdbd/descs
%{_sysconfdir}/sdbd/strs

%ifarch %{ix86} x86_64
%files extension-emulator
%manifest sdbd.manifest
%{_unitdir}/sdbd.service.d/emulator.conf
%{_unitdir}/emulator_preinit.target.wants/sdbd.service
%{_prefix}/lib/systemd/system-generators/sdbd-env-generator

%files extension-tv-emulator
%manifest sdbd.manifest
%{_unitdir}/sdbd.service.d/reset-privs.conf
%{_unitdir}/sdbd.service.d/oom-adj-1000.conf
%endif // ifarch %{ix86} x86_64

%files profile_tv
%{_unitdir}/sdbd.service.d/restart-on-fail.conf
%{_unitdir}/sdbd.service.d/exec.conf

%files -n sdbd-devel
%{_includedir}/sdb/sdbd_plugin.h
%{_libdir}/pkgconfig/sdbd.pc

%changelog
