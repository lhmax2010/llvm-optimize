%define _initrd_dir     /initrd
%define _mnt_initrd_dir /mnt/initrd

Name:           initrd
Summary:        Tizen Initial ramdisk
Version:        2.5
Release:        1
License:        MIT
Group:          System/Utilities
Source:         %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest
Source1:        ramdisk-flush.service

BuildRequires:  cmake

Requires(posttrans): /bin/sh
Requires(posttrans): grep
Requires(posttrans): findutils
Requires(posttrans): util-linux
Requires(posttrans): e2fsprogs
Requires(posttrans): btrfs-progs
Requires(posttrans): f2fs-tools
Requires(posttrans): kmod-compat
%if "%{tizen_profile_name}" != "tv" && "%{mv_prj}" != "1"
Requires(posttrans): nbd-client
%endif
Requires(posttrans): bow-restore
Requires(post):      /sbin/ldconfig
Requires(postun):    /sbin/ldconfig
Requires:            upgrade-parse-dynparts

%description
initial ramdisk. initrd does mount filesystems(/, /opt, /proc, /sys, /lib/modules).

%package init-wrapper
Summary:   Support init.wrapper booting
Requires:  systemd
BuildArch: noarch

%description init-wrapper
This package provides init.wrapper and init symlink file for init wrapper booting.

%package -n verity-tools
Summary:   A tool for dm-verity
License:   MIT
Provides:  veritytool
Requires:  /bin/sh
Requires:  gawk
Requires:  grep
Requires:  e2fsprogs
Requires:  cryptsetup
Requires:  util-linux
Requires:  device-mapper
Requires:  openssl3

%description -n verity-tools
verityctl tool for dm-verity. Similar with veritysetup of cryptsetup
but it can handle with verity meta data block.

%package -n initrd-repack
Summary:   Auto repack and update ramdisk partition on target
Group:     System/Utilities
License:   MIT
Requires:  initrd
Requires:  cpio
Requires:  gzip
Requires:  util-linux
Requires:  /bin/sh
BuildArch: noarch

%description -n initrd-repack
Trigger package that uncompacts the active ramdisk partition to /mnt/initrd,
updates init.sh and files listed in initrd-file.list, and repacks it back
to the ramdisk partition on target installation.

%prep
%setup -q

%build
cp %{SOURCE1001} .

%cmake . \
		-DINITRD_DIR=%{_initrd_dir} \
		-DREBOOT_SRC_DIR=src
make %{_smp_mflags}

%install
%make_install

mkdir -p %{buildroot}%{_initrd_dir}
cp -f data/initrd-file.list %{buildroot}%{_initrd_dir}
%ifarch aarch64 x86_64 riscv64
cp -f data/initrd-file-64bit.list %{buildroot}%{_initrd_dir}
%endif
cp -f data/initrd-file-dmverity.list %{buildroot}%{_initrd_dir}

# Remove nbd-client from initrd-file.list
%if "%{tizen_profile_name}" == "tv" || "%{mv_prj}" == "1"
sed -i "/nbd-client/d" %{buildroot}%{_initrd_dir}/initrd-file.list
%endif

%if 0%{?asan}
_libdir_string=$(echo %{_libdir} | sed 's_/_\\/_g')
sed -i "s/@INITRD_LIB_DIR@/${_libdir_string}/g" data/initrd-file-asan.list.in
cp -f data/initrd-file-asan.list.in %{buildroot}%{_initrd_dir}/initrd-file-asan.list
sed -i "s/@ASAN_FILE_LIST@/\/initrd\/initrd-file-asan.list/g" scripts/mkinitrd.sh
%else
sed -i "s/@ASAN_FILE_LIST@//g" scripts/mkinitrd.sh
%endif
cp -f scripts/mkinitrd.sh %{buildroot}%{_initrd_dir}
cp -f scripts/init.sh %{buildroot}%{_initrd_dir}
mkdir -p %{buildroot}/sbin
install -m 0755 scripts/init.sh %{buildroot}/sbin/init.wrapper

mkdir -p %{buildroot}%{_mnt_initrd_dir}

# ramdisk flush service
mkdir -p %{buildroot}%{_unitdir}
install -m 0644 %SOURCE1 %{buildroot}%{_unitdir}
%install_service delayed.target.wants ramdisk-flush.service

# verity-tools
mkdir -p %{buildroot}%{_bindir}
cp -f scripts/verityctl %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_datadir}/initrd-recovery/initrd.list.d
cp ./data/initrd-file-dmverity-upgrade.list %{buildroot}%{_datadir}/initrd-recovery/initrd.list.d

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%posttrans
%{_initrd_dir}/mkinitrd.sh
rm -rf %{_initrd_dir}

%files
%manifest initrd.manifest
%license LICENSE.MIT
%defattr(-,root,root,-)
%{_initrd_dir}/mkinitrd.sh
%{_initrd_dir}/initrd-file.list
%ifarch aarch64 x86_64 riscv64
%{_initrd_dir}/initrd-file-64bit.list
%endif
%{_initrd_dir}/initrd-file-dmverity.list
%if 0%{?asan}
%{_initrd_dir}/initrd-file-asan.list
%endif
%{_initrd_dir}/init.sh
%{_unitdir}/ramdisk-flush.service
%{_unitdir}/delayed.target.wants/ramdisk-flush.service

%files init-wrapper
%manifest initrd.manifest
%license LICENSE.MIT
%defattr(-,root,root,-)
/sbin/init.wrapper

%posttrans init-wrapper
rm -f /sbin/init
ln -s /sbin/init.wrapper /sbin/init

%files -n verity-tools
%manifest initrd.manifest
%license LICENSE.MIT
%{_bindir}/verityctl
%{_datadir}/initrd-recovery/initrd.list.d/*.list
%attr(0775,root,root)%{_initrd_dir}/usr/sbin/reboot

%post -n initrd-repack
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

RAMDISK_DEV="/dev/disk/by-partlabel/ramdisk${SLOT}"
if [ ! -b "$RAMDISK_DEV" ]; then
    RAMDISK_DEV="/dev/disk/by-partlabel/ramdisk_a"
fi
if [ ! -b "$RAMDISK_DEV" ]; then
    RAMDISK_DEV="/dev/disk/by-partlabel/ramdisk"
fi

if [ ! -b "$RAMDISK_DEV" ]; then
    echo "ERROR: Cannot find ramdisk partition device!" >&2
    exit 0
fi

echo "Updating ramdisk on $RAMDISK_DEV..."

mkdir -p /mnt/initrd
if [ ! -f /mnt/initrd/init ]; then
    echo "Unpacking current $RAMDISK_DEV into /mnt/initrd..."
    (cd /mnt/initrd && gzip -cd "$RAMDISK_DEV" | cpio -imd)
fi

INIT_SRC=""
if [ -f %{_initrd_dir}/init.sh ]; then
    INIT_SRC="%{_initrd_dir}/init.sh"
elif [ -f /sbin/init.wrapper ]; then
    INIT_SRC="/sbin/init.wrapper"
fi

if [ -n "$INIT_SRC" ]; then
    echo "Updating /mnt/initrd/sbin/init with $INIT_SRC..."
    cp -f "$INIT_SRC" /mnt/initrd/sbin/init
    chmod 755 /mnt/initrd/sbin/init
fi

# 2. Synchronize files from all list files (preserve symlinks)
for list in %{_initrd_dir}/*.list; do
    [ -f "$list" ] || continue
    (
        PROGS=
        VERBATIMS=
        . "$list"
        for item in $PROGS $VERBATIMS; do
            [ -f "$item" ] || continue
            dest="/mnt/initrd${item}"

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

echo "Repacking /mnt/initrd to $RAMDISK_DEV..."
(
    cd /mnt/initrd && sync
    find . | cpio -H newc -o | gzip -9 -n > "$RAMDISK_DEV"
    sync
)

echo "SUCCESS: $RAMDISK_DEV repacked successfully."

%files -n initrd-repack
%manifest initrd.manifest
%license LICENSE.MIT
%defattr(-,root,root,-)
