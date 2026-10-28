Name:           util-linux
VCS:            platform/upstream/util-linux#87a36ce91d6ddff60e2be7470d95765a1dd29e2d
Version:        2.41.2
Release:        1.7
# util-linux is a base package and uuidd pre-requiring pwdutils pulls
# that into the core build cycle.  pwdutils also pulls in the whole
# ldap stack into it.  Avoid this whole mess which is done only to
# make the rpm install check of uuidd happy which has support to work without
# these tools as well
#!BuildIgnore:  pwdutils
Url:            https://github.com/karelzak/util-linux
Summary:        A collection of basic system utilities
License:        GPL-2.0-only
Group:          Base/Utilities
Source:         ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.30/%{name}-%{version}.tar.gz
Source1:        util-linux-rpmlintrc
# XXX: make nologin part of util-linux upstream
Source2:        nologin.c
Source3:        nologin.8
Source6:        etc_filesystems
Source7:        baselibs.conf
Source8:        login.pamd
Source9:        remote.pamd
Source14:       su.pamd
Source15:       su.default
Source51:       blkid.conf
Source1001: 	util-linux.manifest
Source1002:     Add_comment_sys_mount.patch
Source1003:     util-linux-2.41.1_loop-AES-v3.8g.patch
Source1004:     create_losetup_ori.patch
Source1005:     disable_getrandom_api.patch

BuildRequires:  binutils-devel
BuildRequires:  fdupes
BuildRequires:  gettext-devel
BuildRequires:  libtool
BuildRequires:  ncurses-devel
BuildRequires:  pam-devel
BuildRequires:  pkg-config
BuildRequires:  readline-devel
BuildRequires:  sqlite-devel
BuildRequires:  zlib-devel

Requires(pre):         /usr/bin/sed
Provides:       eject
Provides:       base = %{version}
Provides:       login = 4.0-33.7
Provides:       util = %{version}
Provides:       uuid-runtime = %{version}
Obsoletes:      base < %{version}
Obsoletes:      login < 4.0-33.7
Obsoletes:      util < %{version}
Obsoletes:      uuid-runtime < %{version}

%description
This package contains a large variety of low-level system utilities
that are necessary for a Linux system to function. It contains the
mount program, the fdisk configuration tool, and more.

%package -n libblkid
Summary:        Filesystem detection library
Group:          Base/File Systems
License:        LGPL-2.1-only

%description -n libblkid
Library for filesystem detection.

%package -n libblkid-devel
Summary:        Development files for the filesystem detection library
Group:          Development/Libraries
License:        LGPL-2.1-only
Requires:       libblkid = %{version}

%description -n libblkid-devel
Files needed to develop applications using the library for filesystem
detection.

%package -n uuidd
Summary:        Helper daemon to guarantee uniqueness of time-based UUIDs
Group:          Base/File Systems

%description -n uuidd
The uuidd package contains a userspace daemon (uuidd) which guarantees
uniqueness of time-based UUID generation even at very high rates on
SMP systems.

%package -n libuuid
Summary:        Library to generate UUIDs
Group:          Base/File Systems
License:        LGPL-2.1-only

%description -n libuuid
A library to generate universally unique IDs (UUIDs).

%package -n libuuid-devel
Summary:        Development files for libuuid1
Group:          Development/Libraries
License:        LGPL-2.1-only
Requires:       libuuid = %{version}

%description -n libuuid-devel
Files to develop applications using the library to generate universally
unique IDs (UUIDs).

%package -n libmount
Summary:        Device mount library
Group:          Base/File Systems
License:        LGPL-2.1-only

%description -n libmount
Library designed to be used in low-level utils like
mount(8) and /usr/sbin/mount.<type> helpers.

%package -n libmount-devel
Summary:        Development files for libmount
Group:          Development/Libraries
License:        LGPL-2.1-only
Requires:       libmount = %{version}

%description -n libmount-devel
Files to develop applications using the libmount library.

%package -n liblastlog2
Summary: lastlog database library and PAM module
License:        BSD-2-Clause

%description -n liblastlog2
This is the lastlog database library and PAM module, part of util-linux.


%package -n liblastlog2-devel
Summary: lastlog database library
License:        BSD-2-Clause
Requires:       liblastlog2 = %{version}
Requires:       pkgconfig

%description -n liblastlog2-devel
This is the lastlog database development library and headers,
part of util-linux.

%package -n libsmartcols
Summary:        Column-based text sort engine
Group:          Base/File Systems
License:        LGPL-2.1-only

%description -n libsmartcols
Library to sort human readable column-based text output.

%package -n libsmartcols-devel
Summary:        Development files for libsmartcols
Group:          Development/Libraries
License:        LGPL-2.1-only
Requires:       libsmartcols = %{version}

%description -n libsmartcols-devel
Files to develop applications using the libsmartcols library.

%package -n libfdisk
Summary:        Filesystem detection library
Group:          System/Filesystems
License:        LGPL-2.1-only

%description -n libfdisk
Library for filesystem detection.

%package -n libfdisk-devel
Summary:        Development files for the filesystem detection library
Group:          Development/Libraries/C and C++
License:        LGPL-2.1-only
Requires:       libfdisk = %{version}

%description -n libfdisk-devel
Files needed to develop applications using the library for filesystem
detection.

%package -n util-linux-su
Summary:        su - run a command with substitute user and group ID
Group:          Base/File Systems
Requires:       %{name}

%description -n util-linux-su
su - run a command with substitute user and group ID


%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .
#
# nologin
cp %{S:2} %{S:3}   .
%{__patch} -p1 < %{SOURCE1002}
%{__patch} -p1 < %{SOURCE1003}
%{__patch} -p1 < %{SOURCE1004}
%{__patch} -p1 < %{SOURCE1005}

%build
export GTKDOCIZE="echo"
autoreconf -fi
export CFLAGS="$CFLAGS -Wno-error=implicit-function-declaration "
export CFLAGS="$CFLAGS -fPIE -flto "
export LDFLAGS="$LDFLAGS -pie -flto "
%configure \
  --disable-raw \
  --enable-mesg \
  --enable-partx \
  --disable-kill \
  --enable-write \
  --enable-line \
  --enable-new-mount \
  --disable-libmount-mountfd-support \
  --enable-login-utils \
  --enable-mountpoint \
  --enable-fdformat \
  --disable-use-tty-group \
  --disable-static \
  --disable-silent-rules \
  --disable-rpath \
  --disable-makeinstall-chown \
  --disable-hwclock-gplv3

#
make %{?_smp_mflags}
#
%{__cc} -fwhole-program %{optflags} -fPIE -pie -o nologin nologin.c

%install
mkdir -p %{buildroot}/etc/pam.d %{buildroot}%{_mandir}/man1 %{buildroot}%{_mandir}/man8 %{buildroot}/usr/bin %{buildroot}/usr/sbin %{buildroot}%{_infodir}
mkdir -p %{buildroot}%{_localstatedir}/lib/libuuid/
mkdir -p %{buildroot}%{_localstatedir}/run/uuidd/
install -m 644 %{SOURCE51} %{buildroot}%{_sysconfdir}/blkid.conf
install -m 644 %{SOURCE8} %{buildroot}/etc/pam.d/login
install -m 644 %{SOURCE9} %{buildroot}/etc/pam.d/remote
install -m 644 %{SOURCE14} %{buildroot}/etc/pam.d/su
install -m 644 %{SOURCE14} %{buildroot}/etc/pam.d/su-l
install -d -m 755 %{buildroot}/etc/default
install -m 644 %{S:15} %{buildroot}/etc/default/su
%make_install
install -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/filesystems
install -m 755 nologin %{buildroot}/%{_sbindir}
rm -f %{buildroot}/%{_libdir}/libblkid.la
rm -f %{buildroot}/%{_libdir}/libuuid.la
rm -f %{buildroot}/%{_libdir}/libmount.la
install -m 644 nologin.8 %{buildroot}%{_mandir}/man8
printf '#! /bin/sh\n/sbin/blockdev --flushbufs $1' > %{buildroot}%{_sbindir}/flushb
chmod 755 %{buildroot}%{_sbindir}/flushb
chmod 755 %{buildroot}%{_bindir}/mount
chmod 755 %{buildroot}%{_bindir}/umount
# Stupid hack so we don't have a tcsh dependency
chmod 644 %{buildroot}%{_datadir}/doc/%{name}/getopt-example.*
# Following files we don't want to package, so remove them
rm -f %{buildroot}%{_bindir}/pg
rm -f %{buildroot}%{_mandir}/man1/pg.1*
rm -rf %{buildroot}%{_datadir}/bash-completion
# Do not package these files to get rid of the perl dependency
rm -f %{buildroot}%{_bindir}/chkdupexe
rm -f %{buildroot}%{_mandir}/man1/chkdupexe.1
# we use this tools from pwdutils
rm -f %{buildroot}/%{_bindir}/chfn %{buildroot}/%{_bindir}/chsh %{buildroot}/%{_bindir}/newgrp
rm -f %{buildroot}/%{_sbindir}/vigr %{buildroot}/%{_sbindir}/vipw
rm -f %{buildroot}/%{_mandir}/man1/chfn.1* %{buildroot}/%{_mandir}/man1/chsh.1* %{buildroot}/%{_mandir}/man1/newgrp.1*
rm -f %{buildroot}/%{_mandir}/man8/vigr.8* %{buildroot}/%{_mandir}/man8/vipw.8*

rm -f %{buildroot}%{_bindir}/uclampset

%find_lang %{name} %{name}.lang
# create list of setarch(8) symlinks
find  %{buildroot}%{_bindir}/ -regextype posix-egrep -type l \
  -regex ".*(linux32|linux64|s390|s390x|i386|ppc|ppc64|ppc32|sparc|sparc64|sparc32|sparc32bash|mips|mips64|mips32|ia64|x86_64|parisc|parisc32|parisc64)$" \
  -printf "%{_bindir}/%f\n" >> %{name}.files
# clock.txt from uuidd is a ghost file
touch %{buildroot}%{_localstatedir}/lib/libuuid/clock.txt
# rcuuidd helper

rm -rf %{buildroot}/%{_mandir}/ru

# remove duplicate manpages
%fdupes -s %{buildroot}/%{_mandir}

%{remove_docs}

%post -n libblkid -p /sbin/ldconfig

%postun -n libblkid -p /sbin/ldconfig

%post -n libmount -p /sbin/ldconfig

%postun -n libmount -p /sbin/ldconfig

%post -n libuuid -p /sbin/ldconfig

%postun -n libuuid -p /sbin/ldconfig

%post -n libsmartcols -p /sbin/ldconfig

%postun -n libsmartcols -p /sbin/ldconfig

%post -n libfdisk -p /sbin/ldconfig

%postun -n libfdisk -p /sbin/ldconfig

%lang_package


%files -f %{name}.files
%manifest %{name}.manifest
%license COPYING
# Common files for all archs
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/filesystems
%config(noreplace) %{_sysconfdir}/blkid.conf
%config(noreplace) /etc/pam.d/login
%config(noreplace) /etc/pam.d/remote
%config(noreplace) /etc/pam.d/su
%config(noreplace) /etc/pam.d/su-l
%{_bindir}/cal
%{_bindir}/eject
%{_bindir}/chmem
%{_bindir}/utmpdump
%{_bindir}/wdctl
%{_sbindir}/resizepart
%{_sbindir}/sulogin
%{_bindir}/login
%{_bindir}/lslogins
%{_bindir}/chrt
%{_bindir}/col
%{_bindir}/colcrt
%{_bindir}/colrm
%{_bindir}/column
%{_bindir}/dmesg
%{_bindir}/fallocate
%{_bindir}/fincore
%{_bindir}/findmnt
%{_bindir}/flock
%{_bindir}/getopt
%{_bindir}/hexdump
%{_bindir}/ionice
%{_bindir}/ipcmk
%{_bindir}/ipcrm
%{_bindir}/ipcs
%{_bindir}/irqtop
%{_bindir}/isosize
%{_bindir}/line
%{_bindir}/logger
%{_bindir}/look
%{_bindir}/lsblk
%{_bindir}/lscpu
%{_bindir}/lsipc
%{_bindir}/lsirq
%{_bindir}/lslocks
%{_bindir}/lsmem
%{_bindir}/lsns
%{_bindir}/mcookie
%{_bindir}/mesg
%{_bindir}/more
%{_bindir}/mount
%{_bindir}/mountpoint
%{_bindir}/namei
%{_bindir}/prlimit
%{_bindir}/rename
%{_bindir}/renice
%{_bindir}/rev
%{_bindir}/script
%{_bindir}/scriptlive
%{_bindir}/scriptreplay
%{_bindir}/setarch
%{_bindir}/uname26
%{_bindir}/setsid
%{_bindir}/taskset
%{_bindir}/ul
%{_bindir}/umount
%{_bindir}/unshare
%{_bindir}/uuidgen
%{_sbindir}/addpart
%{_sbindir}/agetty
%{_sbindir}/blkid
%{_sbindir}/blockdev
%{_sbindir}/chcpu
%{_sbindir}/ctrlaltdel
%{_sbindir}/delpart
%{_sbindir}/findfs
%{_sbindir}/fsck
%{_sbindir}/fsck.minix
%{_sbindir}/fsck.cramfs
%{_sbindir}/fsfreeze
%{_sbindir}/fstrim
%{_sbindir}/ldattach
%{_sbindir}/losetup
%{_sbindir}/losetup_ori
%{_sbindir}/mkfs
%{_sbindir}/mkfs.bfs
%{_sbindir}/mkfs.minix
%{_sbindir}/mkfs.cramfs
%{_sbindir}/mkswap
%{_sbindir}/nologin
%{_sbindir}/partx
%{_sbindir}/pivot_root
%{_sbindir}/rtcwake
%{_sbindir}/swaplabel
%{_sbindir}/swapoff
%{_sbindir}/swapon
%{_sbindir}/switch_root
%{_sbindir}/wipefs
%verify(not mode) %attr(0755,root,tty) %{_bindir}/wall
%{_bindir}/whereis
%verify(not mode) %attr(0755,root,tty) %{_bindir}/write
%{_sbindir}/flushb
%{_sbindir}/readprofile
#XXX: post our patches upstream
#XXX: call fdupes on /usr/share/man
%{_sbindir}/fdisk
%{_sbindir}/cfdisk
%{_sbindir}/sfdisk
%{_sbindir}/fdformat
%{_sbindir}/hwclock
%{_bindir}/setterm
%{_sbindir}/blkdiscard
%{_sbindir}/runuser
%{_bindir}/last
%{_bindir}/lastb
%{_bindir}/nsenter
%{_sbindir}/zramctl
%{_bindir}/choom
%{_bindir}/hardlink
%{_bindir}/uuidparse
%{_sbindir}/rfkill
%{_bindir}/fadvise
%{_bindir}/lsfd
%{_bindir}/pipesz
%{_bindir}/waitpid
%{_sbindir}/blkpr
%{_sbindir}/blkzone
%{_bindir}/bits
%{_bindir}/coresched
%{_bindir}/enosys
%{_bindir}/exch
%{_bindir}/lastlog2
%{_bindir}/lsclocks
%{_bindir}/setpgid

%files -n libblkid
%license Documentation/licenses/COPYING.LGPL-2.1-or-later
%manifest %{name}.manifest
/%{_libdir}/libblkid.so.1
/%{_libdir}/libblkid.so.1.*

%files -n libblkid-devel
%manifest %{name}.manifest
%license Documentation/licenses/COPYING.LGPL-2.1-or-later
%{_libdir}/libblkid.so
%dir %{_includedir}/blkid
%{_includedir}/blkid/blkid.h
%{_libdir}/pkgconfig/blkid.pc

%files -n libmount
%manifest %{name}.manifest
%license Documentation/licenses/COPYING.LGPL-2.1-or-later
/%{_libdir}/libmount.so.1
/%{_libdir}/libmount.so.1.*

%files -n libmount-devel
%manifest %{name}.manifest
%license Documentation/licenses/COPYING.LGPL-2.1-or-later
%{_libdir}/libmount.so
%dir %{_includedir}/libmount
%{_includedir}/libmount/libmount.h
%{_libdir}/pkgconfig/mount.pc

%files -n liblastlog2
%license Documentation/licenses/COPYING.BSD-2-Clause
%{_libdir}/liblastlog2.so.*
%{_libdir}/security/pam_lastlog2.so

%files -n liblastlog2-devel
%license Documentation/licenses/COPYING.BSD-2-Clause
%{_libdir}/liblastlog2.so
%dir %{_includedir}/liblastlog2
%{_includedir}/liblastlog2/lastlog2.h
%{_libdir}/pkgconfig/lastlog2.pc

%files -n uuidd
%manifest %{name}.manifest
%license COPYING
%verify(not mode) %attr(0755,root,root) %{_sbindir}/uuidd
%attr(-,uuidd,uuidd) %dir %{_localstatedir}/lib/libuuid
%ghost %{_localstatedir}/lib/libuuid/clock.txt
%attr(-,uuidd,uuidd) %ghost %dir %{_localstatedir}/run/uuidd

%files -n libuuid
%manifest %{name}.manifest
%license Documentation/licenses/COPYING.LGPL-2.1-or-later
%{_libdir}/libuuid.so.1
%{_libdir}/libuuid.so.1.*

%files -n libuuid-devel
%manifest %{name}.manifest
%license Documentation/licenses/COPYING.LGPL-2.1-or-later
%{_libdir}/libuuid.so
%dir %{_includedir}/uuid
%{_includedir}/uuid/uuid.h
%{_libdir}/pkgconfig/uuid.pc

%files -n libsmartcols
%manifest %{name}.manifest
%license Documentation/licenses/COPYING.LGPL-2.1-or-later
%{_libdir}/libsmartcols.so.1
%{_libdir}/libsmartcols.so.1.*

%files -n libsmartcols-devel
%manifest %{name}.manifest
%license Documentation/licenses/COPYING.LGPL-2.1-or-later
%{_libdir}/libsmartcols.so
%dir %{_includedir}/libsmartcols
%{_includedir}/libsmartcols/libsmartcols.h
%{_libdir}/pkgconfig/smartcols.pc

%files -n libfdisk
%manifest %{name}.manifest
%license Documentation/licenses/COPYING.LGPL-2.1-or-later
%{_libdir}/libfdisk.so.1
%{_libdir}/libfdisk.so.1.*

%files -n libfdisk-devel
%manifest %{name}.manifest
%license Documentation/licenses/COPYING.LGPL-2.1-or-later
%{_libdir}/libfdisk.so
%dir %{_includedir}/libfdisk
%{_includedir}/libfdisk/libfdisk.h
%{_libdir}/pkgconfig/fdisk.pc

%files -n util-linux-su
%manifest %{name}.manifest
%license COPYING
%config(noreplace) /etc/default/su
%{_bindir}/su
