Name: system-plugin-emulator
Version: 0.1.12
Release: 1
Summary: System plugin for emulator
License: Apache-2.0
Group: System/Configuration
Requires: udev
Requires: util-linux
Requires: sysvinit
Requires: alsa-utils
Requires(post): setup
Requires(post): coreutils
BuildRequires: pkgconfig(systemd)
Source0: %{name}-%{version}.tar.gz
Source1001: packaging/%{name}.manifest
ExclusiveArch: %{ix86} x86_64

%description
System plugin files for emulator

%package config-2parts
Summary: System configuration files for storage partitions
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description config-2parts
This package provides configuration files for storage partitions

%prep

%setup -q

%build

%install
find . -name .gitignore -exec rm -f {} \;
cp -arf filesystem/* %{buildroot}

# to remount /mnt here
mkdir -p %{buildroot}/opt/mnt

# for systemd unit
mkdir -p %{buildroot}%{_unitdir}/wait-mount@opt-usr.service.d
mkdir -p %{buildroot}%{_userunitdir}/wait-mount@opt-usr.service.d
%install_service basic.target.wants emulator_preinit.target
%install_service emulator_preinit.target.wants emul-setup-audio-volume.service
%install_service emulator_preinit.target.wants emul-common-preinit.service
%install_service emulator_preinit.target.wants dev-disk-by\\x2dlabel-emulator\\x2dswap.swap
%install_service emulator_preinit.target.wants mnt.mount
%install_service multi-user.target.wants emulator.target
%install_service local-fs.target.wants wait-mount@opt-usr.service
install -m 644 units/no-wait.conf %{buildroot}%{_unitdir}/wait-mount@opt-usr.service.d
install -m 644 units/no-wait.conf %{buildroot}%{_userunitdir}/wait-mount@opt-usr.service.d
mkdir -p %{buildroot}%{_userunitdir}/basic.target.wants
ln -s ../wait-mount@opt-usr.service %{buildroot}%{_userunitdir}/basic.target.wants/wait-mount@opt-usr.service

%files
%license LICENSE
/etc/emulator/prerun
/etc/emulator/prerun.d/set-model-config.sh
/etc/emulator/prerun.d/generate-emulator-env.sh
/etc/inittab
/etc/preconf.d/emulator_ns.preinit
/etc/preconf.d/systemd_conf.preinit
/etc/rc.d/rc.emul
/etc/rc.d/rc.firstboot
/etc/rc.d/rc.shutdown
/etc/rc.d/rc.sysinit
%{_unitdir}/emulator_preinit.target
%{_unitdir}/emulator.target
%{_unitdir}/basic.target.wants/emulator_preinit.target
%{_unitdir}/multi-user.target.wants/emulator.target
%{_unitdir}/emul-setup-audio-volume.service
%{_unitdir}/emul-common-preinit.service
%{_unitdir}/dev-disk-by\x2dlabel-emulator\x2dswap.swap
%{_unitdir}/mnt.mount
%{_unitdir}/wait-mount@opt-usr.service
%{_unitdir}/local-fs.target.wants/wait-mount@opt-usr.service
%{_userunitdir}/wait-mount@opt-usr.service
%{_userunitdir}/basic.target.wants/wait-mount@opt-usr.service
%{_unitdir}/emulator_preinit.target.wants/emul-setup-audio-volume.service
%{_unitdir}/emulator_preinit.target.wants/emul-common-preinit.service
%{_unitdir}/emulator_preinit.target.wants/dev-disk-by\x2dlabel-emulator\x2dswap.swap
%{_unitdir}/emulator_preinit.target.wants/mnt.mount
%{_prefix}/lib/udev/rules.d/51-tizen-udev-default.rules
%{_prefix}/lib/udev/rules.d/95-tizen-emulator.rules
/opt/mnt

%files config-2parts
%license LICENSE
%{_unitdir}/wait-mount@opt-usr.service.d/no-wait.conf
%{_userunitdir}/wait-mount@opt-usr.service.d/no-wait.conf

%posttrans
#run emulator_ns.preinit script after all packages have been installed.
/etc/preconf.d/emulator_ns.preinit
