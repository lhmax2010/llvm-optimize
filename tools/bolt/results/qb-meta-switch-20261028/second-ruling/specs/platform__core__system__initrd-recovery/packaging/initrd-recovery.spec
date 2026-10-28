Name:           initrd-recovery
Summary:        Tools for system recovery
Version:        7.5.5
Release:        0
Group:          System/Utilities
License:        Apache-2.0

Source0:        %{name}-%{version}.tar.gz
Source1001:     initrd-recovery.manifest

BuildRequires:  cmake

# Needed to be installed for fota initrd copy list (40-fota.list)
Requires: util-linux
Requires: grep
Requires: /bin/sh
Requires: procps
Requires: device-mapper
Requires: verity-tools
Requires: upgrade-parse-dynparts
Requires: bow-restore

%description
This is a special booting mode and executes system recovery mode on user
selection like safe mode or phone initialization.

%package -n reboot-param-helper
Summary:        Reboot Param Helper Using Inform Partition
Group:          System/Utilities
License:        Apache-2.0
%description -n reboot-param-helper
A reboot helper to use reboot parameter by inform partition

%package -n bow-restore
Summary:        A tool to restore data on partitions containing a dm-bow data checkpoint.

%description -n bow-restore
bow-restore is a tool to restore data on partitions containing a dm-bow datacheckpoint.

%package -n initrd-recovery-repack
Summary:        Auto repack and update ramdisk-recovery partition on target
Group:          System/Utilities
License:        Apache-2.0
Requires:       cpio
Requires:       gzip
Requires:       util-linux
Requires:       /bin/sh
BuildArch:      noarch

%description -n initrd-recovery-repack
Trigger package that uncompacts the active ramdisk-recovery partition to
/mnt/initrd-recovery, updates recovery scripts and binaries from
initrd.list.d, and repacks it back to the ramdisk-recovery partition on target installation.

%prep
%setup -q

%define initrd_recovery_libexec_dir %{_libexecdir}/initrd-recovery
%define initrd_recovery_install_dropin_dir %{_datadir}/initrd-recovery/initrd.list.d
%define minireboot_binary_name minireboot

%ifarch aarch64 x86-64 riscv64
	%define ARCH_BIT 64
%else
	%define ARCH_BIT 32
%endif

%if 0%{?asan}
	%define ASAN_BUILD 1
%else
	%define ASAN_BUILD 0
%endif

%build
cp %{SOURCE1001} .

%cmake . \
		-DARCH_BIT=%{ARCH_BIT} \
		-DINITRD_RECOVERY_LIBEXEC_DIR=%{initrd_recovery_libexec_dir} \
		-DINITRD_RECOVERY_INSTALL_DROPIN_DIR=%{initrd_recovery_install_dropin_dir} \
		-DASAN_BUILD=%{ASAN_BUILD} \
		-DINITRD_LIB_DIR=%{_libdir} \
		-DUNIT_DIR=%{_unitdir}

make %{?_smp_mflags}

%install
%make_install

# reboot-param-helper
%define inform_path /mnt/inform
mkdir -p %{buildroot}%{inform_path}
mkdir -p %{buildroot}%{_unitdir}/local-fs.target.wants
ln -s ../mnt-inform.mount %{buildroot}%{_unitdir}/local-fs.target.wants

mkdir -p %{buildroot}/opt/data/update

# recovery
mkdir -p %{buildroot}%{_unitdir}/recovery.target.wants
ln -s ../recovery-reboot.service %{buildroot}%{_unitdir}/recovery.target.wants
ln -s ../recovery.service %{buildroot}%{_unitdir}/recovery.target.wants

%post
chsmack -e "System::Privileged" %{initrd_recovery_libexec_dir}/progress_restart.sh

%posttrans
%{initrd_recovery_libexec_dir}/mkinitrd-recovery.sh
rm -rf %{initrd_recovery_libexec_dir}
rm -rf %{_datadir}/initrd-recovery
rm -rf %{_libdir}/initrd-recovery

%files
%defattr(-,root,root,-)
%manifest initrd-recovery.manifest
%license LICENSE
%{initrd_recovery_install_dropin_dir}/00-initrd-recovery.list
%ifarch aarch64 x86-64 riscv64
%{initrd_recovery_install_dropin_dir}/00-64bit-prepare.list
%endif
%if 0%{?asan}
%{initrd_recovery_install_dropin_dir}/00-asan-prepare.list
%endif
%{initrd_recovery_install_dropin_dir}/40-fota.list
%attr(0775,root,root)%{initrd_recovery_libexec_dir}/init
%attr(0775,root,root)%{initrd_recovery_libexec_dir}/mkinitrd-recovery.sh
%attr(0775,root,root)%{initrd_recovery_libexec_dir}/minireboot
%{initrd_recovery_libexec_dir}/fota-init.sh
%{initrd_recovery_libexec_dir}/progress_restart.sh
%attr(775,system,system) /opt/data/update

%attr(0775,root,root)%{initrd_recovery_libexec_dir}/recovery-init
%{initrd_recovery_libexec_dir}/system-recovery
%{initrd_recovery_install_dropin_dir}/50-recovery.list
%{_unitdir}/recovery.target
%{_unitdir}/recovery-reboot.service
%{_unitdir}/recovery.service
%{_unitdir}/recovery.target.wants/recovery-reboot.service
%{_unitdir}/recovery.target.wants/recovery.service

%files -n reboot-param-helper
%{_unitdir}/mnt-inform.mount
%{_unitdir}/local-fs.target.wants/mnt-inform.mount
%{inform_path}

%files -n bow-restore
%attr(0755,root,root)%{_sbindir}/bow-restore

%post -n initrd-recovery-repack
# Run with POSIX sh (dash compatible)
SLOT=""
if [ -r /proc/cmdline ]; then
    read -r cmdline < /proc/cmdline
    for opt in $cmdline; do
        case "$opt" in
            partition_ab=a|partition_ab=b)
                SLOT="_${opt#*=}"
                break
                ;;
        esac
    done
fi

RAMDISK_DEV="/dev/disk/by-partlabel/ramdisk-recovery${SLOT}"
if [ ! -b "$RAMDISK_DEV" ]; then
    RAMDISK_DEV="/dev/disk/by-partlabel/ramdisk-recovery_a"
fi
if [ ! -b "$RAMDISK_DEV" ]; then
    RAMDISK_DEV="/dev/disk/by-partlabel/ramdisk-recovery"
fi

if [ ! -b "$RAMDISK_DEV" ]; then
    echo "ERROR: Cannot find ramdisk-recovery partition device!" >&2
    exit 0
fi

echo "Updating ramdisk-recovery on $RAMDISK_DEV..."

mkdir -p /mnt/initrd-recovery
if [ ! -f /mnt/initrd-recovery/init ]; then
    echo "Unpacking current $RAMDISK_DEV into /mnt/initrd-recovery..."
    (cd /mnt/initrd-recovery && gzip -cd "$RAMDISK_DEV" | cpio -imd)
fi

# Synchronize files from all drop-in list files (preserve symlinks)
for list in %{initrd_recovery_install_dropin_dir}/*.list; do
    [ -f "$list" ] || continue
    (
        DIRECTORIES=
        DIR_SYMLINKS=
        VERBATIMS=
        WITHLIBS=
        LIBONLYS=
        SYMLINKS=
        MVWITHLIBS=
        . "$list"
        for item in $VERBATIMS $WITHLIBS $MVWITHLIBS; do
            [ -f "$item" ] || continue
            dest="/mnt/initrd-recovery${item}"

            # Skip if destination is already a symlink to preserve symlink structure
            if [ -L "$dest" ]; then
                continue
            fi

            # Prevent same-file conflict and safely update if new
            if [ ! -e "$dest" ] || [ "$item" -nt "$dest" ]; then
                mkdir -p "${dest%/*}"
                cp -f "$item" "$dest"
            fi
        done
    )
done

echo "Repacking /mnt/initrd-recovery to $RAMDISK_DEV..."
(
    cd /mnt/initrd-recovery && sync
    find . | cpio -H newc -o | gzip -9 -n > "$RAMDISK_DEV"
    sync
)

echo "SUCCESS: $RAMDISK_DEV repacked successfully."

%files -n initrd-recovery-repack
%defattr(-,root,root,-)
%manifest initrd-recovery.manifest
%license LICENSE
