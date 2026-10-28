Name:      system-plugin
Summary:   Target specific system configuration files
Version:   0.1
Release:   1
Group:     System/Configuration
License:   Apache-2.0
Source0:   %{name}-%{version}.tar.bz2
Source1:   %{name}.manifest

Requires(post): /usr/bin/systemctl
Requires(post): /usr/bin/udevadm
BuildRequires: cmake
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(libtzplatform-config)

%description
This package provides target specific system configuration files.

%package device-spreadtrum
Summary:  Spreadtrum specific system configuration files
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description device-spreadtrum
This package provides Spreadtrum specific system configuration files.

%package device-circle
Summary:  Circle specific system configuration files
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description device-circle
This package provides Circle specific system configuration files.

%package feature-image-reduction
Summary:  System configuration files for reducing image size
Requires: %{name} = %{version}-%{release}
Requires: dbus
Requires: e2fsprogs
BuildArch: noarch

%description feature-image-reduction
This package provides system configuration files for reducing image size.

%package feature-namespace
Summary:  System configuration files for namespace separation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description feature-namespace
This package provides namespace separation of user sessions.

%package feature-session-bind
Summary:  System utils for mounting user session contents
Requires: %{name} = %{version}-%{release}

%description feature-session-bind
This package provides a mount utils for user sessions.

%package feature-container-adaptor
Summary:  Plugin files for supporting container-based Tizen guest OS

%description feature-container-adaptor
This package includes plugin files for supporting container(e.g., Docker)-based Tizen guest OS

%package config-env-headless
Summary:  System configuration files for headless images
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description config-env-headless
This package provides system configuration files for headless images.

%package config-udev-sdbd
Summary: System configuration files to trigger sdb with udev rule
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description config-udev-sdbd
This package provides configuration files to trigger sdb with udev rule.

%package config-2parts
Summary: System configuration files for storage partitions
Requires: %{name} = %{version}-%{release}
Requires: f2fs-tools
BuildArch: noarch

%description config-2parts
This package provides configuration files for storage partitions

%package config-3parts
Summary: System configuration files for storage partitions
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description config-3parts
This package provides configuration files for storage partitions

%package config-3parts-lzuser
Summary: System configuration files for storage partitions
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description config-3parts-lzuser
This package provides configuration files for storage partitions

%package config-stability-monitor
Summary: System configuration file for stability-monitor
Requires: stability-monitor
BuildArch: noarch

%description config-stability-monitor
This package provides configuration file for stability-monitor

%package config-dlconf
Summary: System configuration file for dynamic loader
Requires: glibc
BuildArch: noarch

%description config-dlconf
This package provides configuration file for dynamic loader

%package system-tests
Summary: System testsuite
BuildRequires: deviced-auto-test
BuildRequires: feedbackd-auto-test
BuildRequires: storaged-auto-test
BuildRequires: hal-api-device-haltests
Requires: capi-system-info-tool

%description system-tests
This package provides system testsuites

%prep
%setup -q
cp %{SOURCE1} .

%build
%cmake .

%install
rm -rf %{buildroot}
%{make_install}

# create default directories
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_userunitdir}
mkdir -p %{buildroot}/csa
mkdir -p %{buildroot}/initrd
mkdir -p %{buildroot}%{_prefix}/lib/udev/rules.d/
mkdir -p %{buildroot}%{_sysconfdir}/profile.d

mkdir -p %{buildroot}/opt/container_guest_plugin%{_unitdir}

# tizen-system-env
install -m 644 units/tizen-system-env.service %{buildroot}%{_unitdir}

# csa mount
install -m 644 units/csa.mount %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_unitdir}/local-fs.target.wants
ln -s ../csa.mount %{buildroot}%{_unitdir}/local-fs.target.wants/csa.mount

# tizen-system-env.service
mkdir -p %{buildroot}%{_unitdir}/basic.target.wants
ln -s ../tizen-system-env.service %{buildroot}%{_unitdir}/basic.target.wants/tizen-system-env.service

# udev rules
install -m 644 rules/51-system-plugin-spreadtrum.rules %{buildroot}%{_prefix}/lib/udev/rules.d/

# fstrim
mkdir -p %{buildroot}%{_unitdir}/delayed.target.wants
install -m 644 units/tizen-fstrim-user.timer %{buildroot}%{_unitdir}
ln -s ../tizen-fstrim-user.timer %{buildroot}%{_unitdir}/delayed.target.wants/tizen-fstrim-user.timer
install -m 644 units/tizen-fstrim-user.service %{buildroot}%{_unitdir}
install -m 755 scripts/tizen-fstrim-on-charge.sh %{buildroot}%{_bindir}

# headless
install -m 755 scripts/sdb-mode.sh %{buildroot}%{_bindir}
install -m 755 scripts/headless_env.sh %{buildroot}%{_sysconfdir}/profile.d

# config-2parts
install -m 755 scripts/2parts_env.sh %{buildroot}%{_sysconfdir}/profile.d

# config-udev-sdbd
install -m 644 rules/99-sdb-extcon.rules %{buildroot}%{_prefix}/lib/udev/rules.d/

# /opt/usr lazy mount
mkdir -p %{buildroot}%{_unitdir}/local-fs.target.wants
mkdir -p %{buildroot}%{_unitdir}/wait-mount@opt-usr.service.d
mkdir -p %{buildroot}%{_userunitdir}/basic.target.wants
mkdir -p %{buildroot}%{_userunitdir}/wait-mount@opt-usr.service.d
install -m 644 units/opt-usr.mount %{buildroot}%{_unitdir}
install -m 644 units/opt-usr.mount.container %{buildroot}/opt/container_guest_plugin%{_unitdir}/opt-usr.mount
install -m 644 units/wait-mount@.service %{buildroot}%{_unitdir}
install -m 644 units/wait-mount-session@.service %{buildroot}%{_userunitdir}/wait-mount@.service
install -m 644 units/no-wait.conf %{buildroot}%{_unitdir}/wait-mount@opt-usr.service.d
install -m 644 units/no-wait.conf %{buildroot}%{_userunitdir}/wait-mount@opt-usr.service.d
ln -s ../opt-usr.mount %{buildroot}%{_unitdir}/local-fs.target.wants/opt-usr.mount
ln -s ../wait-mount@.service %{buildroot}%{_unitdir}/local-fs.target.wants/wait-mount@opt-usr.service
ln -s ../wait-mount@.service %{buildroot}%{_userunitdir}/basic.target.wants/wait-mount@opt-usr.service

install -m 644 units/opt.mount.container %{buildroot}/opt/container_guest_plugin%{_unitdir}/opt.mount

# namespace
mkdir -p %{buildroot}%{_unitdir}/user@.service.d
install -m 644 units/namespace.conf %{buildroot}%{_unitdir}/user@.service.d/

# session-bind
mkdir -p %{buildroot}%{_userunitdir}/basic.target.wants
install -m 644 units/session-bind.service %{buildroot}%{_userunitdir}
ln -s ../session-bind.service %{buildroot}%{_userunitdir}/basic.target.wants/session-bind.service

# stability-monitor
mkdir -p %{buildroot}/etc/stability-monitor.d
cp conf/stability-monitor-public.conf %{buildroot}/etc/stability-monitor.d/01-public.conf

# dlconf
mkdir -p %{buildroot}/etc/dl.conf.d
cp conf/dl.conf %{buildroot}/etc/dl.conf

# test
mkdir -p %{buildroot}%{_bindir}/hal
install -m 755 tests/system-test %{buildroot}%{_bindir}
cp %{_bindir}/deviced-auto-test %{buildroot}%{_bindir}
cp %{_bindir}/feedbackd-auto-test %{buildroot}%{_bindir}
cp %{_bindir}/storaged-auto-test %{buildroot}%{_bindir}
cp %{_bindir}/hal/device-haltests %{buildroot}%{_bindir}/hal

%clean
rm -rf %{buildroot}

%post
systemctl daemon-reload

%files
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_unitdir}/tizen-system-env.service
%{_unitdir}/basic.target.wants/tizen-system-env.service

%files device-spreadtrum
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
/initrd
/csa
%{_prefix}/lib/udev/rules.d/51-system-plugin-spreadtrum.rules
%{_unitdir}/tizen-system-env.service
%{_unitdir}/basic.target.wants/tizen-system-env.service
%{_unitdir}/csa.mount
%{_unitdir}/local-fs.target.wants/csa.mount
%{_unitdir}/delayed.target.wants/tizen-fstrim-user.timer
%{_unitdir}/tizen-fstrim-user.timer
%{_unitdir}/tizen-fstrim-user.service
%{_bindir}/tizen-fstrim-on-charge.sh

%files device-circle
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
/initrd
/csa
%{_unitdir}/csa.mount
%{_unitdir}/local-fs.target.wants/csa.mount

%posttrans feature-image-reduction
# platform/upstream/dbus
rm -f %{_bindir}/dbus-cleanup-sockets
rm -f %{_bindir}/dbus-run-session
rm -f %{_bindir}/dbus-test-tool
rm -f %{_bindir}/dbus-update-activation-environment
rm -f %{_bindir}/dbus-uuidgen
# platform/upstream/e2fsprogs
rm -f %{_sbindir}/e4crypt

%files feature-namespace
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_unitdir}/user@.service.d/namespace.conf

%files feature-session-bind
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_bindir}/session-bind
%{_userunitdir}/session-bind.service
%{_userunitdir}/basic.target.wants/session-bind.service

%post feature-session-bind
echo ""
echo "------------------------------------------------------------------------"
echo "When you install this system-plugin-feature-session-bind rpm separately,"
echo "you are required to execute this command"
echo ""
echo "root#) setcap cap_sys_admin=ei /usr/bin/session-bind"
echo "------------------------------------------------------------------------"
echo ""

%files feature-container-adaptor
/opt/container_guest_plugin%{_unitdir}/opt.mount
/opt/container_guest_plugin%{_unitdir}/opt-usr.mount

%posttrans feature-container-adaptor

%files config-env-headless
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_sysconfdir}/profile.d/headless_env.sh

%files config-udev-sdbd
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_bindir}/sdb-mode.sh
%{_prefix}/lib/udev/rules.d/99-sdb-extcon.rules

%files config-2parts
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_sysconfdir}/profile.d/2parts_env.sh
%{_unitdir}/wait-mount@.service
%{_unitdir}/wait-mount@opt-usr.service.d/no-wait.conf
%{_unitdir}/local-fs.target.wants/wait-mount@opt-usr.service
%{_userunitdir}/wait-mount@.service
%{_userunitdir}/wait-mount@opt-usr.service.d/no-wait.conf
%{_userunitdir}/basic.target.wants/wait-mount@opt-usr.service

%files config-3parts
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_unitdir}/opt-usr.mount
%{_unitdir}/wait-mount@.service
%{_unitdir}/local-fs.target.wants/opt-usr.mount
%{_userunitdir}/wait-mount@.service
%{_userunitdir}/basic.target.wants/wait-mount@opt-usr.service

%files config-3parts-lzuser
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_unitdir}/opt-usr.mount
%{_unitdir}/wait-mount@.service
%{_unitdir}/local-fs.target.wants/opt-usr.mount
%{_userunitdir}/wait-mount@.service
%{_userunitdir}/basic.target.wants/wait-mount@opt-usr.service

%files config-stability-monitor
%manifest %{name}.manifest
/etc/stability-monitor.d/01-public.conf

%files config-dlconf
%manifest %{name}.manifest
/etc/dl.conf
%dir %attr(755,root,root)/etc/dl.conf.d

%files system-tests
%defattr(755,root,root,-)
%manifest %{name}.manifest
%{_bindir}/system-test
%{_bindir}/deviced-auto-test
%{_bindir}/feedbackd-auto-test
%{_bindir}/storaged-auto-test
%{_bindir}/hal/device-haltests
