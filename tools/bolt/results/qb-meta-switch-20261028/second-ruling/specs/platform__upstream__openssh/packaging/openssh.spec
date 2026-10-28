%define _appdefdir      %{_prefix}/share/X11/app-defaults
%define xversion 1.2.4.1

Name:           openssh
Version:        7.7p1
Release:        0
Summary:        Secure Shell Client and Server (Remote Login Program)
License:        BSD-3-Clause and MIT
Group:          System/Network
URL:            http://www.openssh.com/

Source0:        %{name}-%{version}.tar.gz
Source2:        sshd.pamd
Source8:        ssh-askpass
Source11:       sshd-gen-keys-start
Source12:       sshd.service
Source13:       sshd.socket
Source14:       sshd@.service
Source1001:     openssh.manifest
Patch0:         0001-Local-Fix-link-error-related-to-tun_fwd_ifnames.patch

BuildRequires:  systemd
BuildRequires:  autoconf

BuildRequires:  pkgconfig(openssl3)

# Note that OpenSSH must be used for development period only.
# Let's prevent a trial that includes OpenSSH into a Tizen platform
# image with mic package by requesting the GPL-licensed packages.
Requires:       gcc gdb

BuildRequires:  pam-devel
BuildRequires:  gawk vim
Requires:       /usr/bin/netstat
Requires:       pam-modules-extra
Requires(pre):  shadow-utils coreutils

%{!?_initddir:%global _initddir %{_initrddir}}

%description
SSH (Secure Shell) is a program for logging into and executing commands
on a remote machine. It is intended to replace rsh (rlogin and rsh) and
provides openssl (secure encrypted communication) between two untrusted
hosts over an insecure network.

xorg-x11 (X Window System) connections and arbitrary TCP/IP ports can
also be forwarded over the secure channel.

%prep
%setup -q
%patch0 -p1
cp %{SOURCE1001} .

%build
# https://wiki.tizen.org/ASan#.E2.80.9Cmultiple_definition_of.E2.80.9D_linking_error_due_to_-fno-common
%{?asan:%restore_fcommon}

autoreconf -fiv
PIEFLAGS="-fpie"
export CFLAGS="%{optflags} $PIEFLAGS -fstack-protector -Wno-implicit-function-declaration -Wno-incompatible-pointer-types"
export CXXFLAGS="%{optflags} $PIEFLAGS -fstack-protector"
export LDFLAGS="-pie %{?asan:-ldl} "
%configure \
    --with-ssl-engine \
    --sysconfdir=%{_sysconfdir}/ssh \
    --libexecdir=%{_libexecdir}/ssh \
    --with-pam \
    --without-lastlog \
    --with-privsep-path=%{_localstatedir}/lib/empty \
    --with-sandbox=rlimit \
    --disable-strip \
    --with-xauth=%{_prefix}/bin/xauth \
    --target=%{_target_cpu}-tizen-linux \
    --without-openssl-header-check \
    --without-zlib-version-check \
    --without-hardening \
    --with-pie=no
%__make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot}/ install
install -d -m 755 %{buildroot}%{_sysconfdir}/pam.d
install -d -m 755 %{buildroot}%{_localstatedir}/lib/sshd
install -m 644 %{S:2} %{buildroot}%{_sysconfdir}/pam.d/sshd

# install shell script to automate the process of adding your public key to a remote machine
install -m 755 contrib/ssh-copy-id %{buildroot}%{_bindir}
install -m 644 contrib/ssh-copy-id.1 %{buildroot}%{_mandir}/man1
sed -e "s,@LIBEXEC@,%{_libexecdir},g" < %{S:8} > %{buildroot}%{_libexecdir}/ssh/ssh-askpass
rm -f %{buildroot}%{_datadir}/Ssh.bin
sed -i -e s@/usr/libexec@%{_libexecdir}@g %{buildroot}%{_sysconfdir}/ssh/sshd_config

install -D -m 0755 %{SOURCE11} %{buildroot}%{_sbindir}/sshd-gen-keys-start
# install the service unit for systemd
install -D -m 0644 %{SOURCE12} %{buildroot}%{_unitdir}/sshd.service
install -D -m 0644 %{SOURCE13} %{buildroot}%{_unitdir}/sshd.socket
install -D -m 0644 %{SOURCE14} %{buildroot}%{_unitdir}/sshd@.service

# install the socket unit for systemd
mkdir -p %{buildroot}/%{_unitdir}/sockets.target.wants
ln -s ../sshd.socket %{buildroot}/%{_unitdir}/sockets.target.wants/sshd.socket

# Remove unnecessary files for Tizen platform
rm -rf %{buildroot}/%{_mandir}/cat*
rm -rf %{buildroot}/%{_mandir}/man*

%pre
getent group sshd >/dev/null || %{_sbindir}/groupadd -o -r sshd
getent passwd sshd >/dev/null || %{_sbindir}/useradd -r -g sshd -d %{_localstatedir}/lib/sshd -s /bin/false -c "SSH daemon" sshd

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%dir %attr(755,root,root) %{_localstatedir}/lib/sshd
%attr(0755,root,root) %dir %{_sysconfdir}/ssh
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/moduli
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/ssh_config
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config
%attr(0644,root,root) %config %{_sysconfdir}/pam.d/sshd
%attr(0755,root,root) %{_bindir}/ssh
%{_bindir}/scp
%{_bindir}/sftp
%{_bindir}/ssh-*
%{_sbindir}/*
%attr(0755,root,root) %dir %{_libexecdir}/ssh
%attr(0755,root,root) %{_libexecdir}/ssh/sftp-server
%attr(0755,root,root) %{_libexecdir}/ssh/ssh-keysign
%attr(0755,root,root) %{_libexecdir}/ssh/ssh-pkcs11-helper
%attr(0755,root,root) %{_libexecdir}/ssh/ssh-askpass
%{_sbindir}/sshd-gen-keys-start
%{_unitdir}/sshd.service
%{_unitdir}/sshd@.service
%{_unitdir}/sockets.target.wants/*.socket
%{_unitdir}/sshd.socket

%changelog

* Thu Aug 06 2020 Geunsik Lim <geunsik.lim@samsung.com>
 - Updated the OpenSSH version from 6.6.p1 to 7.7p1 to support OpenSSL 1.1.x

