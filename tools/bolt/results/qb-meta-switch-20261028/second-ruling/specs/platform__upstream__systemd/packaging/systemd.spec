# "enable foo" will turn into --enable-foo or --disable-foo
# depending "with_foo" macro
%define enable() %{expand:%%{?with_%{1}:--enable-%{1}}%%{!?with_%{1}:--disable-%{1}}}

%if "%{mv_prj}" == "1"
%define WITH_VD_MV 1
%else
%define WITH_VD_MV 0
%endif

%define WITH_RANDOMSEED 0
%define WITH_BASH_COMPLETION 0
%define WITH_ZSH_COMPLETION 0
%define WITH_COREDUMP 0
%define WITH_BACKLIGHT 0
%define WITH_TIMEDATED 0
%define WITH_RFKILL 0
%define WITH_MACHINED 0
%define WITH_DOC 0
%define WITH_HOSTNAMED 0
%define WITH_VIRT 1
%if "%{dev_wos}" == "1"
%define WITH_SMACK 0
%else
%define WITH_SMACK 1
%endif
%define WITH_GETTY 1
%if "%{WITH_VD_MV}" == "1"
%define WITH_FIRMWARE_DIRECTORY 0
%else
%define WITH_FIRMWARE_DIRECTORY 1
%endif

%define WITH_UDEV_RULES_FLATTEN 1
%define WITH_UDEV_RESOLVE_NAMES_LATE 1

%define WITH_LOGIND 0

%define build_dir _build
%define dbuspolicydir %{_datadir}/dbus-1

# The 'meson' macro is defined in rpm macros, but it uses features from rpm 4.15 ({shrink, set_build_flags)
# Below is a version suitable for our purposes
%define meson \
	CFLAGS="${CFLAGS:-%optflags}" \
	export CFLAGS \
	%{__meson} \\\
		--buildtype=plain \\\
		--prefix=%{_prefix} \\\
		--libdir=%{_libdir} \\\
		--libexecdir=%{_libexecdir} \\\
		--bindir=%{_bindir} \\\
		--sbindir=%{_sbindir} \\\
		--includedir=%{_includedir} \\\
		--datadir=%{_datadir} \\\
		--mandir=%{_mandir} \\\
		--infodir=%{_infodir} \\\
		--localedir=%{_datadir}/locale \\\
		--sysconfdir=%{_sysconfdir} \\\
		--localstatedir=%{_localstatedir} \\\
		--sharedstatedir=%{_sharedstatedir} \\\
		--wrap-mode=%{__meson_wrap_mode} \\\
		%{_vpath_builddir}

# Ninja macros below are defined for ninja in e.g. fedora distro, but
# so far they are not provided by Tizen's ninja package.
%define __ninja %{_bindir}/ninja
%define __ninja_common_opts -v %{?_smp_flags}
%define ninja_build %{__ninja} %{__ninja_common_opts}
%define ninja_install DESTDIR=%{buildroot} %{__ninja} install %{__ninja_common_opts}

Name:           systemd
Version:        244
Release:        0%{?release_flags}
# For a breakdown of the licensing, see README
License:        LGPL-2.1+ and GPL-2.0+
Summary:        A System and Service Manager
Url:            http://www.freedesktop.org/wiki/Software/systemd
Group:          Base/Startup
Source0:        https://github.com/systemd/systemd/archive/v%{version}.tar.gz
Source2:        %{name}-rpmlintrc
Source3:        test-runner.c
Source4:        wait-default-target.sh
Source5:        wait-delayed-target.sh
Source6:        org.tizen.system.conf
Source7:        send-booting-done.c
Source8:        wait-target-done.c
Source9:        delayed-target-trigger.sh
Source1001:     systemd.manifest
BuildRequires:  gperf
BuildRequires:  intltool >= 0.40.0
BuildRequires:  libacl-devel
BuildRequires:  libblkid-devel >= 2.20
BuildRequires:  libcap-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libkmod-devel >= 14
%if 0%{?WITH_DOC}
BuildRequires:  xsltproc
BuildRequires:  docbook-xsl-stylesheets
%endif
BuildRequires:  pam-devel
BuildRequires:  pkgconfig
# BuildRequires:  pkgconfig(dbus-1)     # for remove circular dependency on OBS
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libkmod)
BuildRequires:  pkgconfig(mount)
BuildRequires:  pkgconfig(libdbuspolicy1)
BuildRequires:  pkgconfig(dlog-redirect-stdout)
BuildRequires:  meson
BuildRequires:  acl
BuildRequires:  python
BuildRequires:  rsync
# Requires:       dbus                  # for remove circular dependency on OBS
Requires:       acl
Requires:       filesystem
Requires(post): coreutils
Requires(pre):  coreutils
Requires(pre):  /usr/bin/getent
Requires(pre):  /usr/sbin/groupadd
Requires(post): %{_sbindir}/update-alternatives
Requires(preun): %{_sbindir}/update-alternatives

Obsoletes:      SysVinit < 2.86-24
Obsoletes:      sysvinit < 2.86-24
Provides:       SysVinit = 2.86-24
Provides:       sysvinit = 2.86-24
Provides:       /bin/systemctl
Provides:       /sbin/shutdown
Provides:       udev = %{version}
Obsoletes:      udev < 183

%description
systemd is a system and service manager for Linux, compatible with
SysV and LSB init scripts. systemd provides aggressive parallelization
capabilities, uses socket and D-Bus activation for starting services,
offers on-demand starting of daemons, keeps track of processes using
Linux cgroups, supports snapshotting and restoring of the system
state, maintains mount and automount points and implements an
elaborate transactional dependency-based service control logic. It can
work as a drop-in replacement for sysvinit.

%package -n libsystemd
License:        LGPL-2.1+
Summary:        Systemd libraries
Group:          Base/Startup
Obsoletes:      libudev < 183
Provides:       libudev = %{version}
Obsoletes:      systemd < 185-4
Conflicts:      systemd < 185-4

%description -n libsystemd
Libraries for systemd and udev, as well as the systemd PAM module.

%package devel
License:        LGPL-2.1+
Summary:        Development headers for systemd
Requires:       %{name} = %{version}
Requires:       libsystemd = %{version}
Provides:       libudev-devel = %{version}
Obsoletes:      libudev-devel < 183

%description devel
Development headers and auxiliary files for developing applications for systemd.

%package analyze
License:        LGPL-2.1+
Summary:        Tool for processing systemd profiling information
Requires:       %{name} = %{version}
Obsoletes:      systemd < 38-5

%description analyze
'systemd-analyze blame' lists which systemd unit needed how much time to finish
initialization at boot.
'systemd-analyze plot' renders an SVG visualizing the parallel start of units
at boot.

%package tests
License:        LGPL-2.1+ and BSD-2-Clause
Summary:        Set of tests for sd-bus component
Requires:       %{name} = %{version}

%description tests
This package is part of 'dbus-integratnion-tests' framework and contains set of tests
for sd-bus component (DBUS API C library).

%package extension-kdbus
Summary:        Extension for systemd to support KDBUS in Tizen
Requires:       %{name} = %{version}-%{release}

%description extension-kdbus
This modifies systemd to support KDBUS in Tizen.

%package boot
License:        LGPL-2.1+
Summary:        systemd-boot EFI bootloader
Requires:       %{name} = %{version}

%description boot
This package is provides systemd-boot as well as the bootctl command to control
the bootloader.

%prep
%setup -q

%build
cp %{SOURCE1001} .
cp %{SOURCE3} .
cp %{SOURCE7} .
cp %{SOURCE8} .

# Build GNU EFI first #
(
cd vendor/gnu-efi
GNU_EFI_CFLAGS=$(echo "$CFLAGS" | sed 's/ -fstack-protector-strong//g')
GNU_EFI_CXXFLAGS=$(echo "$CXXFLAGS" | sed 's/ -fstack-protector-strong//g')
CFLAGS="$GNU_EFI_CFLAGS" \
CXXFLAGS="$GNU_EFI_CXXFLAGS" \
%__make %{?_smp_mflags} \
    PREFIX=%{_prefix} LIBDIR=%{_libdir} RANLIB="${RANLIB:-ranlib}" AR="${AR:-ar}" CC="${CC:-cc}" mkvars

CFLAGS="$GNU_EFI_CFLAGS" \
CXXFLAGS="$GNU_EFI_CXXFLAGS" \
%__make %{?_smp_mflags} \
    PREFIX=%{_prefix} LIBDIR=%{_libdir} RANLIB="${RANLIB:-ranlib}" AR="${AR:-ar}" CC="${CC:-cc}"

CFLAGS="$GNU_EFI_CFLAGS" \
CXXFLAGS="$GNU_EFI_CXXFLAGS" \
%__make V=1 install INSTALLROOT=%{buildroot}/../gnu-efi/ \
    PREFIX=%{_prefix} LIBDIR=%{_libdir} RANLIB="${RANLIB:-ranlib}" AR="${AR:-ar}" CC="${CC:-cc}"
)
###

%define _vpath_srcdir .
%define _vpath_builddir %{build_dir}
%meson \
	-Dkdbus=true \
%if 0%{?WITH_UDEV_RULES_FLATTEN}
	-Dudev-rules-flatten=true \
%else
	-Dudev-rules-flatten=false \
%endif
%if 0%{?WITH_UDEV_RESOLVE_NAMES_LATE}
	-Dudev-resolve-names=late \
%endif
%if 0%{?WITH_LOGIND}
	-Dlogind=true \
%else
	-Dlogind=false \
%endif
%if ! 0%{?WITH_SMACK}
	-Dsmack=false \
%endif
%if ! 0%{?WITH_VIRT}
	-Dvirt=false \
%endif
%if ! 0%{?WITH_RANDOMSEED}
	-Drandomseed=false \
%endif
%if ! 0%{?WITH_COREDUMP}
	-Dcoredump=false \
%endif
%if ! 0%{?WITH_BACKLIGHT}
	-Dbacklight=false \
%endif
%if ! 0%{?WITH_TIMEDATED}
	-Dtimedated=false \
%endif
%if ! 0%{?WITH_RFKILL}
	-Drfkill=false \
%endif
	-Dgnu-efi=true \
	-Defi-includedir=%{buildroot}/../gnu-efi/%{_includedir}/efi/ \
	-Defi-libdir=%{buildroot}/../gnu-efi/%{_libdir}/ \
	-Dhibernate=false \
	-Dldconfig=false \
	-Dhwdb=false \
	-Dsysusers=false \
	-Dfirstboot=false \
	-Dpolkit=false \
	-Dtimesyncd=false \
	-Dresolve=false \
	-Dnetworkd=false \
%if ! 0%{?WITH_MACHINED}
	-Dmachined=false \
%endif
%if ! 0%{?WITH_HOSTNAMED}
	-Dhostnamed=false \
%endif
	-Dimportd=false \
	-Denvironment-d=false \
	-Dnss-systemd=false \
	-Dgcrypt=false \
%if ! 0%{?WITH_DOC}
	-Dman=false \
%endif
	-Dportabled=false \
	-Dpstore=false \
	-Drpmmacrosdir=%{_sysconfdir}/rpm/ \
	-Dsysvinit-path="" \
	-Dsysvrcnd-path="" \
%if 0%{?WITH_SMACK}
	-Dsmack-run-label=System::Privileged \
%endif
%if "%{mv_prj}" == "1"
        -Dsysctl-use-pid-max-conf=false \
%endif
	-Dinstall-tests=true \
	-Ddefault-hierarchy=legacy \
	-Db_pie=true
%meson_build

# compile test-runner for 'dbus-integration-test' framework
%__cc %{_builddir}/%{name}-%{version}/test-runner.c -o %{_builddir}/%{name}-%{version}/systemd-tests
%__cc -fPIE -pie %{_builddir}/%{name}-%{version}/send-booting-done.c -o %{_builddir}/%{name}-%{version}/send-booting-done -Isrc -L%{_builddir}/%{name}-%{version}/%{build_dir} -lsystemd
%__cc -fPIE -pie %{_builddir}/%{name}-%{version}/wait-target-done.c -o %{_builddir}/%{name}-%{version}/wait-target-done -DRELATIVE_SOURCE_PATH="" -DSIZEOF_TIME_T=4 -Isrc/basic -Isrc/systemd -L%{_builddir}/%{name}-%{version}/%{build_dir} -lsystemd

%install
%meson_install
%find_lang %{name}
cat <<EOF >> systemd.lang
%lang(be) /usr/lib/systemd/catalog/systemd.be.catalog
%lang(be) /usr/lib/systemd/catalog/systemd.be@latin.catalog
%lang(bg) /usr/lib/systemd/catalog/systemd.bg.catalog
%lang(de) /usr/lib/systemd/catalog/systemd.de.catalog
%lang(fr) /usr/lib/systemd/catalog/systemd.fr.catalog
%lang(it) /usr/lib/systemd/catalog/systemd.it.catalog
%lang(pl) /usr/lib/systemd/catalog/systemd.pl.catalog
%lang(pt_BR) /usr/lib/systemd/catalog/systemd.pt_BR.catalog
%lang(ru) /usr/lib/systemd/catalog/systemd.ru.catalog
%lang(zh) /usr/lib/systemd/catalog/systemd.zh_CN.catalog
%lang(zh) /usr/lib/systemd/catalog/systemd.zh_TW.catalog
EOF

# udev links
/usr/bin/mkdir -p %{buildroot}/%{_sbindir}
/usr/bin/ln -sf ../bin/udevadm %{buildroot}%{_sbindir}/udevadm
%if 0%{?WITH_FIRMWARE_DIRECTORY}
/usr/bin/mkdir -p %{buildroot}%{_prefix}/lib/firmware/updates
%endif

# Create SysV compatibility symlinks. systemctl/systemd are smart
# enough to detect in which way they are called.
/usr/bin/ln -s ../lib/systemd/systemd %{buildroot}%{_bindir}/systemd

%if 0%{?WITH_LOGIND}
# legacy links
/usr/bin/ln -s loginctl %{buildroot}%{_bindir}/systemd-loginctl
%endif

# Make sure these directories are properly owned
/usr/bin/mkdir -p %{buildroot}%{_prefix}/lib/systemd/system/basic.target.wants
/usr/bin/mkdir -p %{buildroot}%{_prefix}/lib/systemd/system/default.target.wants
/usr/bin/mkdir -p %{buildroot}%{_prefix}/lib/systemd/system/syslog.target.wants

# Make sure the user generators dir exists too
/usr/bin/mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-generators
/usr/bin/mkdir -p %{buildroot}%{_prefix}/lib/systemd/user-generators

# Create new-style configuration files so that we can ghost-own them
/usr/bin/touch %{buildroot}%{_sysconfdir}/hostname
/usr/bin/touch %{buildroot}%{_sysconfdir}/vconsole.conf
/usr/bin/touch %{buildroot}%{_sysconfdir}/locale.conf
/usr/bin/touch %{buildroot}%{_sysconfdir}/machine-id
/usr/bin/touch %{buildroot}%{_sysconfdir}/machine-info
/usr/bin/touch %{buildroot}%{_sysconfdir}/timezone

/usr/bin/mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-preset/
/usr/bin/mkdir -p %{buildroot}%{_prefix}/lib/systemd/user-preset/

# Make sure the shutdown/sleep drop-in dirs exist
/usr/bin/mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-shutdown/
/usr/bin/mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-sleep/

# Make sure the NTP units dir exists
/usr/bin/mkdir -p %{buildroot}%{_prefix}/lib/systemd/ntp-units.d/

# Install modprobe fragment
/usr/bin/mkdir -p %{buildroot}%{_sysconfdir}/modprobe.d/

# Fix the dangling /var/lock -> /run/lock symlink
install -Dm644 tmpfiles.d/legacy.conf %{buildroot}%{_prefix}/lib/tmpfiles.d/legacy.conf

install -m 755 -d %{buildroot}/%{_prefix}/lib/systemd/system

rm -rf %{buildroot}/%{_docdir}/%{name}

# Allow replacing systemd-shutdown and some scripts with tizen-specific variant
mv %{buildroot}%{_prefix}/lib/systemd/systemd-shutdown %{buildroot}%{_prefix}/lib/systemd/systemd-shutdown-original
mv %{buildroot}%{_sbindir}/reboot %{buildroot}%{_sbindir}/reboot-original
mv %{buildroot}%{_sbindir}/halt %{buildroot}%{_sbindir}/halt-original
mv %{buildroot}%{_sbindir}/poweroff %{buildroot}%{_sbindir}/poweroff-original
mv %{buildroot}%{_sbindir}/shutdown %{buildroot}%{_sbindir}/shutdown-original
touch %{buildroot}%{_prefix}/lib/systemd/systemd-shutdown
touch %{buildroot}%{_sbindir}/reboot
touch %{buildroot}%{_sbindir}/halt
touch %{buildroot}%{_sbindir}/poweroff
touch %{buildroot}%{_sbindir}/shutdown

# Disable some useless services in Tizen
rm -rf %{buildroot}/%{_prefix}/lib/systemd/system/sysinit.target.wants/dev-hugepages.mount
rm -rf %{buildroot}/%{_prefix}/lib/systemd/system/sysinit.target.wants/sys-fs-fuse-connections.mount
rm -rf %{buildroot}/%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-binfmt.service
rm -rf %{buildroot}/%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-modules-load.service
rm -rf %{buildroot}/%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-ask-password-console.path
rm -rf %{buildroot}/%{_prefix}/lib/systemd/system/sysinit.target.wants/systemd-update-utmp.service
rm -rf %{buildroot}/%{_prefix}/lib/systemd/system/multi-user.target.wants/systemd-ask-password-wall.path
rm -rf %{buildroot}/%{_prefix}/lib/systemd/system/systemd-update-utmp.service
rm -rf %{buildroot}/%{_prefix}/lib/systemd/system/systemd-volatile-root.service
rm -rf %{buildroot}/%{_prefix}/lib/systemd/system/systemd-tmpfiles-clean.timer
rm -rf %{buildroot}/%{_prefix}/lib/systemd/system/systemd-tmpfiles-clean.service
rm -rf %{buildroot}/%{_prefix}/lib/systemd/system/timers.target.wants/systemd-tmpfiles-clean.timer
rm -rf %{buildroot}/%{_prefix}/lib/systemd/user/systemd-tmpfiles-clean.timer
rm -rf %{buildroot}/%{_prefix}/lib/systemd/user/systemd-tmpfiles-clean.service
rm -rf %{buildroot}/%{_prefix}/lib/systemd/user/systemd-tmpfiles-setup.service

# Drop kernel-install as it's not used by Tizen kernel scripts
rm -rf %{buildroot}/%{_bindir}/kernel-install
rm -rf %{buildroot}/%{_prefix}/lib/kernel

# Exclude ELF binaries
rm -f %{buildroot}/%{_prefix}/lib/systemd/systemd-update-utmp
rm -f %{buildroot}/%{_prefix}/lib/systemd/systemd-volatile-root
rm -f %{buildroot}/%{_prefix}/lib/systemd/systemd-remount-fs
rm -f %{buildroot}/%{_prefix}/lib/systemd/system-generators/systemd-fstab-generator
rm -f %{buildroot}/%{_prefix}/lib/systemd/system-generators/systemd-debug-generator
rm -f %{buildroot}/%{_prefix}/lib/systemd/system-generators/systemd-gpt-auto-generator
rm -f %{buildroot}/%{_prefix}/lib/systemd/system-generators/systemd-run-generator

# Marker file for kdbus
touch %{buildroot}/%{_sysconfdir}/systemd/extension-kdbus

# Prepare tests for 'dbus-integration-test' framework
install -D -m 755 %{_builddir}/%{name}-%{version}/systemd-tests %{buildroot}%{_prefix}/lib/dbus-tests/runner/systemd-tests
mkdir -p %{buildroot}%{_prefix}/lib/dbus-tests/test-suites/systemd-tests/
mv %{buildroot}%{_prefix}/lib/systemd/tests/test-bus-* %{buildroot}%{_prefix}/lib/dbus-tests/test-suites/systemd-tests/
# Install send-booting-done helper
install -D -m 755 %{_builddir}/%{name}-%{version}/send-booting-done %{buildroot}%{_prefix}/lib/systemd/
install -D -m 755 %{_builddir}/%{name}-%{version}/wait-target-done %{buildroot}%{_prefix}/lib/systemd/

# Shell Completion
%if ! 0%{?WITH_BASH_COMPLETION}
rm -rf %{buildroot}/%{_datadir}/bash-completion/*
%endif
%if ! 0%{?WITH_ZSH_COMPLETION}
rm -rf %{buildroot}/%{_datadir}/zsh/site-functions/*
%endif

mkdir -p %{buildroot}/%{_localstatedir}/log/journal

# Delayed target
install -m 0755 %{SOURCE4} %{buildroot}%{_bindir}/wait-default-target.sh
install -m 0755 %{SOURCE5} %{buildroot}%{_bindir}/wait-delayed-target.sh
install -m 0644 %{SOURCE6} %{buildroot}%{dbuspolicydir}/system.d/org.tizen.system.conf
install -m 0755 %{SOURCE9} %{buildroot}%{_bindir}/delayed-target-trigger.sh

# end of install
%pre
/usr/bin/getent group cdrom >/dev/null 2>&1 || /usr/sbin/groupadd -r -g 11 cdrom >/dev/null 2>&1 || :
/usr/bin/getent group tape >/dev/null 2>&1 || /usr/sbin/groupadd -r -g 33 tape >/dev/null 2>&1 || :
/usr/bin/getent group dialout >/dev/null 2>&1 || /usr/sbin/groupadd -r -g 18 dialout >/dev/null 2>&1 || :
/usr/bin/getent group floppy >/dev/null 2>&1 || /usr/sbin/groupadd -r -g 19 floppy >/dev/null 2>&1 || :
/usr/bin/systemctl stop systemd-udevd-control.socket systemd-udevd-kernel.socket systemd-udevd.service >/dev/null 2>&1 || :

# Rename configuration files that changed their names
%if 0%{?WITH_LOGIND}
/usr/bin/mv -n %{_sysconfdir}/systemd/systemd-logind.conf %{_sysconfdir}/systemd/logind.conf >/dev/null 2>&1 || :
%endif
/usr/bin/mv -n %{_sysconfdir}/systemd/systemd-journald.conf %{_sysconfdir}/systemd/journald.conf >/dev/null 2>&1 || :

%post
/usr/bin/systemd-machine-id-setup > /dev/null 2>&1 || :
%if 0%{?WITH_RANDOMSEED}
/usr/lib/systemd/systemd-random-seed save > /dev/null 2>&1 || :
%endif
/usr/bin/systemctl daemon-reexec > /dev/null 2>&1 || :
/usr/bin/systemctl start systemd-udevd.service >/dev/null 2>&1 || :
/usr/bin/mkdir -p /etc/systemd/network
/usr/bin/ln -sf /dev/null /etc/systemd/network/99-default.link

# Set the smack label of executable binary tools
chsmack %{_bindir}/busctl -a "System::Tools"
%if %{?WITH_MACHINED}
chsmack %{_bindir}/machinectl -a "System::Tools"
%endif
chsmack %{_bindir}/systemd-run -a "System::Tools"
%if 0%{?WITH_HOSTNAMED}
chsmack %{_bindir}/hostnamectl -a "System::Tools"
%endif
chsmack %{_bindir}/localectl -a "System::Tools"
%if 0%{?WITH_COREDUMP}
chsmack %{_bindir}/coredumpctl -a "System::Tools"
%endif
%if 0%{?WITH_TIMEDATED}
chsmack %{_bindir}/timedatectl -a "System::Tools"
%endif
chsmack %{_bindir}/systemd -a "System::Tools"
chsmack %{_bindir}/systemctl -a "System::Tools"
chsmack %{_bindir}/systemd-notify -a "System::Tools"
chsmack %{_bindir}/systemd-ask-password -a "System::Tools"
chsmack %{_bindir}/systemd-tty-ask-password-agent -a "System::Tools"
chsmack %{_bindir}/systemd-machine-id-setup -a "System::Tools"
chsmack %{_bindir}/systemd-socket-activate -a "System::Tools"
%if 0%{?WITH_LOGIND}
chsmack %{_bindir}/loginctl -a "System::Tools"
chsmack %{_bindir}/systemd-loginctl -a "System::Tools"
chsmack %{_bindir}/systemd-inhibit -a "System::Tools"
%endif
chsmack %{_bindir}/journalctl -a "System::Tools"
chsmack %{_bindir}/systemd-tmpfiles -a "System::Tools"
chsmack %{_bindir}/systemd-nspawn -a "System::Tools"
chsmack %{_bindir}/systemd-stdio-bridge -a "System::Tools"
chsmack %{_bindir}/systemd-cat -a "System::Tools"
chsmack %{_bindir}/systemd-cgls -a "System::Tools"
chsmack %{_bindir}/systemd-cgtop -a "System::Tools"
chsmack %{_bindir}/systemd-delta -a "System::Tools"
chsmack %{_bindir}/udevadm -a "System::Tools"
chsmack %{_bindir}/systemd-escape -a "System::Tools"
chsmack %{_bindir}/systemd-path -a "System::Tools"
chsmack %{_prefix}/lib/systemd/* -a "System::Tools"
%if 0%{?WITH_VIRT}
chsmack %{_bindir}/systemd-detect-virt -a "System::Tools"
%endif

update-alternatives --install %{_prefix}/lib/systemd/systemd-shutdown systemd-shutdown %{_prefix}/lib/systemd/systemd-shutdown-original 100 || :
update-alternatives --install %{_sbindir}/reboot reboot %{_sbindir}/reboot-original 100 || :
update-alternatives --install %{_sbindir}/halt halt %{_sbindir}/halt-original 100 || :
update-alternatives --install %{_sbindir}/poweroff poweroff %{_sbindir}/poweroff-original 100 || :
update-alternatives --install %{_sbindir}/shutdown shutdown %{_sbindir}/shutdown-original 100 || :

%postun
if [ $1 -ge 1 ] ; then
	/usr/bin/systemctl daemon-reload > /dev/null 2>&1 || :
%if 0%{?WITH_LOGIND}
	/usr/bin/systemctl try-restart systemd-logind.service >/dev/null 2>&1 || :
%endif
fi
if [ $1 -eq 0 ] ; then
	update-alternatives --remove systemd-shutdown %{_prefix}/lib/systemd/systemd-shutdown-original
	update-alternatives --remove reboot %{_sbindir}/reboot-original
	update-alternatives --remove halt %{_sbindir}/halt-original
	update-alternatives --remove poweroff %{_sbindir}/poweroff-original
	update-alternatives --remove shutdown %{_sbindir}/shutdown-original
fi

%preun
if [ $1 -eq 0 ] ; then
	/usr/bin/systemctl disable \
		getty@.service \
		remote-fs.target \
		systemd-readahead-replay.service \
		systemd-readahead-collect.service >/dev/null 2>&1 || :
fi

%post -n libsystemd -p /sbin/ldconfig
%postun -n libsystemd  -p /sbin/ldconfig

%lang_package

%files
%manifest %{name}.manifest
%license LICENSE.LGPL2.1  LICENSE.GPL2
%{_bindir}/busctl
%if 0%{?WITH_MACHINED}
%{_bindir}/machinectl
%endif
%{_bindir}/systemd-run
%if 0%{?WITH_HOSTNAMED}
%{_bindir}/hostnamectl
%endif
%{_bindir}/localectl
%if 0%{?WITH_COREDUMP}
%{_bindir}/coredumpctl
%endif
%if 0%{?WITH_TIMEDATED}
%{_bindir}/timedatectl
%endif
%dir %{_sysconfdir}/systemd
%dir %{_sysconfdir}/systemd/system
%dir %{_sysconfdir}/systemd/user
%dir %{_sysconfdir}/tmpfiles.d
%dir %{_sysconfdir}/sysctl.d
%dir %{_sysconfdir}/modules-load.d
%dir %{_sysconfdir}/binfmt.d
%if 0%{?WITH_BASH_COMPLETION}
%{_datadir}/bash-completion/*
%endif
%if 0%{?WITH_ZSH_COMPLETION}
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/*
%endif
%dir %{_sysconfdir}/udev
%dir %{_sysconfdir}/udev/rules.d
%dir %{_prefix}/lib/systemd
%dir %{_prefix}/lib/systemd/system
%dir %{_prefix}/lib/systemd/system-generators
%dir %{_prefix}/lib/systemd/user-generators
%dir %{_prefix}/lib/systemd/system-preset
%dir %{_prefix}/lib/systemd/user-preset
%dir %{_prefix}/lib/systemd/system-shutdown
%dir %{_prefix}/lib/systemd/system-sleep
%dir %{_prefix}/lib/tmpfiles.d
%dir %{_prefix}/lib/sysctl.d
%dir %{_prefix}/lib/modules-load.d
%dir %{_prefix}/lib/binfmt.d
%if 0%{?WITH_FIRMWARE_DIRECTORY}
%dir %{_prefix}/lib/firmware
%dir %{_prefix}/lib/firmware/updates
%endif
%dir %{_datadir}/systemd
%config(noreplace) %{dbuspolicydir}/system.d/org.freedesktop.systemd1.conf
%if 0%{?WITH_HOSTNAMED}
%config(noreplace) %{dbuspolicydir}/system.d/org.freedesktop.hostname1.conf
%endif
%config(noreplace) %{dbuspolicydir}/system.d/org.freedesktop.locale1.conf
%if 0%{?WITH_TIMEDATED}
%config(noreplace) %{dbuspolicydir}/system.d/org.freedesktop.timedate1.conf
%endif
%if 0%{?WITH_MACHINED}
%config(noreplace) %{dbuspolicydir}/system.d/org.freedesktop.machine1.conf
%endif
%if 0%{?WITH_COREDUMP}
%config(noreplace) %{_sysconfdir}/systemd/coredump.conf
%endif
%config(noreplace) %{_sysconfdir}/systemd/system.conf
%config(noreplace) %{_sysconfdir}/systemd/user.conf
%config(noreplace) %{_sysconfdir}/systemd/journald.conf
%config(noreplace) %{_sysconfdir}/udev/udev.conf
%config(noreplace) %{_sysconfdir}/systemd/sleep.conf
%{_sysconfdir}/xdg/systemd
%ghost %config(noreplace) %{_sysconfdir}/hostname
%ghost %config(noreplace) %{_sysconfdir}/vconsole.conf
%ghost %config(noreplace) %{_sysconfdir}/locale.conf
%ghost %config(noreplace) %{_sysconfdir}/machine-id
%ghost %config(noreplace) %{_sysconfdir}/machine-info
%ghost %config(noreplace) %{_sysconfdir}/timezone
%exclude %{_sysconfdir}/X11/xinit/xinitrc.d/50-systemd-user.sh
%{_bindir}/systemd
%{_bindir}/systemctl
%{_bindir}/systemd-notify
%{_bindir}/systemd-ask-password
%{_bindir}/systemd-tty-ask-password-agent
%{_bindir}/systemd-machine-id-setup
%{_bindir}/systemd-socket-activate
%{_bindir}/journalctl
%{_bindir}/systemd-tmpfiles
%{_bindir}/systemd-nspawn
%{_bindir}/systemd-stdio-bridge
%{_bindir}/systemd-cat
%{_bindir}/systemd-cgls
%{_bindir}/systemd-cgtop
%{_bindir}/systemd-delta
%{_bindir}/systemd-id128
%{_bindir}/udevadm
%{_bindir}/systemd-escape
%{_bindir}/systemd-path
%{_bindir}/systemd-mount
%{_bindir}/systemd-umount
%{_prefix}/lib/sysctl.d/*.conf
%{_prefix}/lib/systemd/systemd
%{_prefix}/lib/systemd/system
%if 0%{?WITH_VIRT}
%{_bindir}/systemd-detect-virt
%endif

%dir %{_prefix}/lib/systemd/system/basic.target.wants
%dir %{_prefix}/lib/systemd/user
%dir %{_prefix}/lib/systemd/network
%dir %{_prefix}/lib/systemd/user/default.target.wants
%{_prefix}/lib/systemd/user/basic.target
%{_prefix}/lib/systemd/user/exit.target
%{_prefix}/lib/systemd/user/printer.target
%{_prefix}/lib/systemd/user/shutdown.target
%{_prefix}/lib/systemd/user/sockets.target
%{_prefix}/lib/systemd/user/sound.target
%{_prefix}/lib/systemd/user/systemd-exit.service
%{_prefix}/lib/systemd/user/paths.target
%{_prefix}/lib/systemd/user/smartcard.target
%{_prefix}/lib/systemd/user/timers.target
%{_prefix}/lib/systemd/user/default.target
%exclude %{_prefix}/lib/systemd/user/graphical-session.target
%exclude %{_prefix}/lib/systemd/user/graphical-session-pre.target
%{_prefix}/lib/systemd/network/99-default.link
%exclude %{_prefix}/lib/systemd/system-preset/90-systemd.preset
%exclude %{_prefix}/lib/systemd/user-preset/90-systemd.preset
%{_prefix}/lib/systemd/user/delayed.target
%{_prefix}/lib/systemd/user/user-delayed-target-trigger.service
%{_prefix}/lib/systemd/user/default.target.wants/user-delayed-target-trigger.service
%{_prefix}/lib/systemd/user/user-default-target-done.service
%{_prefix}/lib/systemd/user/default.target.wants/user-default-target-done.service
%{_prefix}/lib/systemd/user/user-delayed-target-done.service
%{_prefix}/lib/systemd/user/delayed.target.wants/user-delayed-target-done.service
%{dbuspolicydir}/system.d/org.tizen.system.conf
%exclude %{_prefix}/lib/modprobe.d/systemd.conf

%{_prefix}/lib/systemd/libsystemd-shared-%{version}.so
%{_prefix}/lib/systemd/systemd-*
%dir %{_prefix}/lib/systemd/catalog
%{_prefix}/lib/systemd/catalog/systemd.catalog
%{_prefix}/lib/udev
%if 0%{?WITH_GETTY}
%{_prefix}/lib/systemd/system-generators/systemd-getty-generator
%else
%exclude %{_prefix}/lib/systemd/system-generators/systemd-getty-generator
%endif
%{_prefix}/lib/systemd/system-generators/systemd-system-update-generator
%{_prefix}/lib/tmpfiles.d/home.conf
%{_prefix}/lib/tmpfiles.d/journal-nocow.conf
%{_prefix}/lib/tmpfiles.d/legacy.conf
%{_prefix}/lib/tmpfiles.d/systemd.conf
%{_prefix}/lib/tmpfiles.d/systemd-nologin.conf
%if 0%{?WITH_MACHINED}
%{_prefix}/lib/tmpfiles.d/systemd-nspawn.conf
%endif
%{_prefix}/lib/tmpfiles.d/tmp.conf
%{_prefix}/lib/tmpfiles.d/var.conf
%{_prefix}/lib/tmpfiles.d/x11.conf
%{_prefix}/lib/tmpfiles.d/static-nodes-permissions.conf
%{_prefix}/lib/tmpfiles.d/systemd-tmp.conf
%{_sbindir}/init
%ghost %{_prefix}/lib/systemd/systemd-shutdown
%ghost %{_sbindir}/reboot
%ghost %{_sbindir}/halt
%ghost %{_sbindir}/poweroff
%ghost %{_sbindir}/shutdown
%{_sbindir}/reboot-original
%{_sbindir}/halt-original
%{_sbindir}/poweroff-original
%{_sbindir}/shutdown-original
%{_sbindir}/telinit
%{_sbindir}/runlevel
%{_sbindir}/udevadm
%{_datadir}/systemd/graphinfo.gvpr
%{_datadir}/systemd/kbd-model-map
%{_datadir}/systemd/language-fallback-map
%{_datadir}/dbus-1/services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.systemd1.service
%if 0%{?WITH_HOSTNAMED}
%{_datadir}/dbus-1/system-services/org.freedesktop.hostname1.service
%endif
%if 0%{?WITH_LOGIND}
%config %{_sysconfdir}/pam.d/systemd-user
%config(noreplace) %{_sysconfdir}/systemd/logind.conf
%config(noreplace) %{dbuspolicydir}/system.d/org.freedesktop.login1.conf
%{_bindir}/loginctl
%{_bindir}/systemd-loginctl
%{_bindir}/systemd-inhibit
%{_datadir}/dbus-1/system-services/org.freedesktop.login1.service
%exclude %{_datadir}/polkit-1/actions/org.freedesktop.login1.policy
%endif
%{_datadir}/dbus-1/system-services/org.freedesktop.locale1.service
%exclude %{_datadir}/polkit-1/actions/org.freedesktop.systemd1.policy
%exclude %{_datadir}/polkit-1/actions/org.freedesktop.locale1.policy
%if 0%{?WITH_TIMEDATED}
%{_datadir}/dbus-1/system-services/org.freedesktop.timedate1.service
%endif
%if 0%{?WITH_MACHINED}
%{_datadir}/dbus-1/system-services/org.freedesktop.machine1.service
%endif
%dir %{_datadir}/factory/
%dir %{_datadir}/factory/etc
%dir %{_datadir}/factory/etc/pam.d
%{_datadir}/factory/etc/nsswitch.conf
%{_datadir}/factory/etc/pam.d/other
%{_datadir}/factory/etc/pam.d/system-auth
%{_datadir}/factory/etc/issue

%{_localstatedir}/log/journal

%{_bindir}/wait-default-target.sh
%{_bindir}/wait-delayed-target.sh
%{_bindir}/delayed-target-trigger.sh
%exclude %{_prefix}/lib/systemd/system/runlevel0.target
%exclude %{_prefix}/lib/systemd/system/runlevel1.target
%exclude %{_prefix}/lib/systemd/system/runlevel2.target
%exclude %{_prefix}/lib/systemd/system/runlevel3.target
%exclude %{_prefix}/lib/systemd/system/runlevel4.target
%exclude %{_prefix}/lib/systemd/system/runlevel5.target
%exclude %{_prefix}/lib/systemd/system/runlevel6.target
%{_prefix}/lib/systemd/send-booting-done
%{_prefix}/lib/systemd/wait-target-done

%files -n libsystemd
%manifest %{name}.manifest
%license LICENSE.LGPL2.1
%if 0%{?WITH_LOGIND}
%{_libdir}/security/pam_systemd.so
%endif
%{_libdir}/libsystemd.so.*
%{_libdir}/libudev.so.*
%{_libdir}/libnss_myhostname.so.2
%if 0%{?WITH_MACHINED}
%{_libdir}/libnss_mymachines.so.2
%endif

%files extension-kdbus
%manifest %{name}.manifest
%license LICENSE.LGPL2.1  LICENSE.GPL2
%{_sysconfdir}/systemd/extension-kdbus
%{_prefix}/lib/systemd/user/busnames.target
%{_prefix}/lib/systemd/system-generators/systemd-dbus1-generator
%{_prefix}/lib/systemd/user-generators/systemd-dbus1-generator

%files devel
%manifest %{name}.manifest
%{_libdir}/libudev.so
%{_libdir}/libsystemd.so
%dir %{_includedir}/systemd
%{_includedir}/systemd/sd-bus.h
%{_includedir}/systemd/sd-bus-protocol.h
%{_includedir}/systemd/sd-bus-vtable.h
%{_includedir}/systemd/sd-event.h
%{_includedir}/systemd/_sd-common.h
%{_includedir}/systemd/sd-daemon.h
%{_includedir}/systemd/sd-device.h
%{_includedir}/systemd/sd-hwdb.h
%{_includedir}/systemd/sd-id128.h
%{_includedir}/systemd/sd-journal.h
%{_includedir}/systemd/sd-login.h
%{_includedir}/systemd/sd-messages.h
%{_includedir}/libudev.h
%{_libdir}/pkgconfig/libudev.pc
%{_libdir}/pkgconfig/libsystemd.pc
%{_datadir}/pkgconfig/systemd.pc
%{_datadir}/pkgconfig/udev.pc
%{_sysconfdir}/rpm/macros.systemd

%files analyze
%manifest %{name}.manifest
%license LICENSE.LGPL2.1
%{_bindir}/systemd-analyze

%files tests
%manifest %{name}.manifest
%{_prefix}/lib/dbus-tests/test-suites/systemd-tests/
%{_prefix}/lib/dbus-tests/runner/systemd-tests
%{_prefix}/lib/systemd/tests/

%if 0%{?WITH_DOC}
%docs_package
%else
%exclude %{_docdir}
%exclude %{_datadir}/doc/systemd
%endif

%files boot
%manifest %{name}.manifest
%license LICENSE.LGPL2.1 vendor/gnu-efi/LICENSE.BSD2Intel  vendor/gnu-efi/LICENSE.BSD2Linaro  vendor/gnu-efi/LICENSE.BSD3HP  vendor/gnu-efi/LICENSE.Expat
%{_bindir}/bootctl
%exclude %{_prefix}/lib/systemd/boot/efi/linux*.efi.stub
%{_prefix}/lib/systemd/boot/efi/systemd-boot*.efi
%{_prefix}/lib/systemd/system-generators/systemd-bless-boot-generator
