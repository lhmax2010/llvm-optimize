Name:       factory-reset
Summary:    factory-reset scripts and uitls
Version:    1.1
Release:    2
Group:      Applications/Core Applications
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    factory-reset.service
Source2:    factory-reset-launch.service
Source3:    org.tizen.factory-reset.service
Source4:    org.tizen.factory-reset.conf
ExclusiveArch: %{arm} aarch64 riscv64
BuildRequires: cmake
BuildRequires: pkgconfig(libsmack)
BuildRequires: pkgconfig(libsystemd)
Requires: %{name}-userdata-backup
Requires: rstsmack
Requires: /usr/bin/rm
Requires: /usr/bin/ls
Requires: /usr/bin/ps
Requires: /usr/bin/tr
Requires: /usr/bin/tar
Requires: /usr/bin/pwd
Requires: /usr/bin/cat
Requires: /usr/bin/awk
Requires: /usr/bin/expr
Requires: /usr/bin/echo
Requires: /usr/bin/grep
Requires: /usr/bin/sync
Requires: /usr/bin/mkdir
Requires: /usr/bin/unzip
Requires: /usr/bin/sleep
Requires: /usr/bin/mount
Requires: /usr/bin/umount
Requires: /usr/bin/md5sum
Requires: /usr/bin/killall
Requires: /usr/bin/readlink
Requires: /usr/bin/dbus-send
Requires: /usr/sbin/blkid
Requires: /usr/sbin/reboot
Requires: /usr/sbin/mkfs.ext4
Requires: /usr/sbin/mkfs.f2fs
Requires: /usr/sbin/mkfs.btrfs

%description
Factory-reset is for returning the phone to the initial state. This makes the
data of the phone to the default state and (if required) writes default
preconfiguration
It would be not only called by testers after many kind of verification tests
but it also be called by Manufacture Steps for all products.

%package userdata-backup
Summary:    Vconf internal keys (devel)
Group:      Application Framework/Configuration
Requires: /usr/bin/tar
Requires: /usr/bin/zip
Requires: /usr/bin/sed
Requires: /usr/bin/mkdir
Requires: /usr/bin/bash
Requires: /usr/bin/chmod

%description userdata-backup
userdata-backup make a backup data for user r/w data area by archieving with tar/zip.

%package -n rstsmack
Summary:    Utility to restore smack attributes
Group:      Application Framework/Configuration

%description -n rstsmack
rstsmack is small utility to set Smack labels from configuration file.

%prep
%setup -q

%build
cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix}
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

install -D -m 0700 script/build-backup-data.sh %{buildroot}%{_bindir}/build-backup-data.sh
install -D -m 0700 script/run-factory-reset.sh %{buildroot}%{_bindir}/run-factory-reset.sh
install -D -m 0700 script/factoryreset-verify.sh %{buildroot}%{_bindir}/factoryreset-verify.sh
install -D -m 0700 script/dump-frlog.sh %{buildroot}/opt/etc/dump.d/module.d/dump-frlog.sh

install -D -m 0644 %SOURCE1 %{buildroot}%{_unitdir}/factory-reset.service
install -D -m 0644 %SOURCE2 %{buildroot}%{_unitdir}/factory-reset-launch.service
%install_service delayed.target.wants factory-reset.service

install -D -m 0644 %SOURCE4 %{buildroot}%{_sysconfdir}/dbus-1/system.d/org.tizen.factory-reset.conf
install -D -m 0644 %SOURCE3 %{buildroot}%{_datadir}/dbus-1/system-services/org.tizen.factoryreset.service

%files
%manifest factory-reset.manifest
%license LICENSE.Apache-2.0
%{_unitdir}/factory-reset.service
%{_unitdir}/factory-reset-launch.service
%{_unitdir}/delayed.target.wants/factory-reset.service
%{_sysconfdir}/dbus-1/system.d/org.tizen.factory-reset.conf
%{_datadir}/dbus-1/system-services/org.tizen.factoryreset.service

%{_bindir}/run-factory-reset.sh
%{_bindir}/factoryreset-verify.sh
%attr(700,root,root) %{_bindir}/factory-reset
%attr(100,root,root) /opt/etc/dump.d/module.d/dump-frlog.sh

%files userdata-backup
%manifest factory-reset.manifest
%license LICENSE.Apache-2.0
%{_bindir}/build-backup-data.sh

%files -n rstsmack
%manifest factory-reset.manifest
%license LICENSE.Apache-2.0
%attr(700,root,root) %{_bindir}/rstsmack
