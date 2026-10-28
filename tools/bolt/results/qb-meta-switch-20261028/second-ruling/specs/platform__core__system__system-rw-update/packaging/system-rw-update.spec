Name:       system-rw-update
Summary:    System RW Update Manager
Version:    1.3.0
Release:    0
Group:      Base/Startup
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.bz2
Source1001: %{name}.manifest

BuildRequires: cmake
BuildRequires: pkgconfig(libtzplatform-config)

# rstsmack is provided by Public factory-reset
# Please consider it when you migrate this package
Requires:      %{_bindir}/rstsmack

%define upgrade_dir %TZ_SYS_UPGRADE

%description
System RW update manager provides interface for running platform/application update scripts
after software is updated to new version which is implemented by using systemd offline update.

%prep
%setup -q

%build
cp %{SOURCE1001} .

LDFLAGS+=" -Wl,--rpath=%{_prefix}/lib -Wl,--as-needed"
cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DTZ_SYS_VAR=%TZ_SYS_VAR \
	-DTZ_SYS_UPGRADE=%TZ_SYS_UPGRADE \
	-DTZ_SYS_UPGRADE_SCRIPTS=%TZ_SYS_UPGRADE_SCRIPTS
%__make %{?_smp_mflags}

%install
%make_install

mkdir -p %{buildroot}%{upgrade_dir}
cp upgrade/99-sdb-switch.rules %{buildroot}%{upgrade_dir}
cp upgrade/install-sdb-rule.sh %{buildroot}%{upgrade_dir}
cp upgrade/record-version.sh %{buildroot}%{upgrade_dir}
cp upgrade/rw-update-macro.inc %{buildroot}%{upgrade_dir}
cp upgrade/update-init.sh %{buildroot}%{upgrade_dir}
cp upgrade/update.sh %{buildroot}%{upgrade_dir}
cp upgrade/update-checkpoint-create.sh %{buildroot}%{upgrade_dir}
cp upgrade/update-post.sh %{buildroot}%{upgrade_dir}
cp upgrade/update-finalize.sh %{buildroot}%{upgrade_dir}
cp upgrade/run-with-timeout.sh %{buildroot}%{upgrade_dir}
mkdir -p %{buildroot}%{_unitdir}/system-update.target.wants
install -m 644 units/offline-update.service %{buildroot}%{_unitdir}
ln -s ../offline-update.service %{buildroot}%{_unitdir}/system-update.target.wants/
ln -s ../getty.target %{buildroot}%{_unitdir}/system-update.target.wants
ln -s ../cynara.socket %{buildroot}%{_unitdir}/system-update.target.wants
ln -s ../dbus.socket %{buildroot}%{_unitdir}/system-update.target.wants
ln -s system-update.target %{buildroot}%{_unitdir}/offline-update.target

# SDB debugging
install -m 644 units/udev-sdb-init.service %{buildroot}%{_unitdir}
ln -s ../udev-sdb-init.service %{buildroot}%{_unitdir}/system-update.target.wants

# DM-BOW device prepare
install -m 644 units/udev-trigger-dmbow@.service %{buildroot}%{_unitdir}
ln -s ../udev-trigger-dmbow@.service %{buildroot}%{_unitdir}/system-update.target.wants/udev-trigger-dmbow@user.service

# data checkpoint target
install -m 644 units/data-checkpoint.target %{buildroot}%{_unitdir}
install -m 644 units/data-checkpoint.service %{buildroot}%{_unitdir}
ln -s ../data-checkpoint.target %{buildroot}%{_unitdir}/system-update.target.wants
mkdir -p %{buildroot}%{_unitdir}/data-checkpoint.target.wants
ln -s ../data-checkpoint.service %{buildroot}%{_unitdir}/data-checkpoint.target.wants/data-checkpoint.service

# RW-Update finalize
install -m 644 units/update-post.service %{buildroot}%{_unitdir}
ln -s ../update-post.service %{buildroot}%{_unitdir}/system-update.target.wants

# Update finalize
mkdir -p %{buildroot}%{_unitdir}/delayed.target.wants
install -m 644 units/update-finalize.service %{buildroot}%{_unitdir}
ln -s ../update-finalize.service %{buildroot}%{_unitdir}/delayed.target.wants

%clean
rm -rf %{buildroot}

%posttrans
if [ -e /usr/lib/udev/rules.d/99-sdb-switch.rules ]; then
	echo "Exist 99-sdb-switch.rules, Skip!"
else
	mkdir -p /usr/lib/udev/rules.d
	ln -s /opt/data/update/99-sdb-switch.rules /usr/lib/udev/rules.d
fi

%files
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%TZ_SYS_UPGRADE/*
%{_unitdir}/offline-update.service
%{_unitdir}/offline-update.target
%{_unitdir}/update-post.service
%{_unitdir}/update-finalize.service
%{_unitdir}/system-update.target.wants
%{_unitdir}/udev-sdb-init.service
%{_unitdir}/udev-trigger-dmbow@.service
%{_unitdir}/data-checkpoint.target
%{_unitdir}/data-checkpoint.service
%{_unitdir}/data-checkpoint.target.wants/data-checkpoint.service
%{_unitdir}/delayed.target.wants/update-finalize.service
/etc/upgrade/conf.d/rw-upgrade-scripts.conf
