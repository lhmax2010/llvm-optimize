Summary: Utilities for managing accounts and shadow password files
Name: shadow-utils
Version: 4.20.2
Release: 1
URL: http://pkg-shadow.alioth.debian.org/
License: BSD-3-Clause and GPL-2.0+
Group: System/Base

Source0: http://pkg-shadow.alioth.debian.org/releases/shadow-%{version}.tar.gz
Source1: useradd.default
Source1001:     %{name}.manifest

Requires: setup

%description
The shadow package includes the necessary programs for
converting UNIX password files to the shadow password format, plus
programs for managing user and group accounts. The pwconv command
converts passwords to the shadow password format. The pwunconv command
unconverts shadow passwords and generates an npasswd file (a standard
UNIX password file). The pwck command checks the integrity of password
and shadow files. The lastlog command prints out the last login times
for all users. The useradd, userdel, and usermod commands are used for
managing user accounts. The groupadd, groupdel, and groupmod commands
are used for managing group accounts.

%package -n %{name}-adm
Summary:    Dev tool for developement
Group:      System/Utilities
Requires:   %{name} = %{version}-%{release}

%description -n %{name}-adm
to supply user debugging tool for system

%prep
%setup -q -n shadow-%{version}

%build
export CFLAGS="${CFLAGS} -fPIE"
export LDFLAGS="${LDFLAGS} -pie"

cp %{SOURCE1001} .
%configure --without-libcrack --without-audit --mandir=/usr/share/man --without-libpam --without-selinux --enable-shadowgrp --disable-man --disable-account-tools-setuid --with-group-name-max-length=32 --disable-nls --with-nscd=no --disable-logind --without-libbsd --enable-lastlog

make

%install
make install DESTDIR=%{buildroot}
install -d %{buildroot}/%{_sysconfdir}/default
install -c -m 444 etc/login.defs %{buildroot}/%{_sysconfdir}/login.defs
install -c -m 644 %SOURCE1 %{buildroot}/%{_sysconfdir}/default/useradd
install -d %{buildroot}/sbin

chmod u+s %{buildroot}/%{_bindir}/su

install -d %{buildroot}/bin
mv %{buildroot}/%{_bindir}/su %{buildroot}/bin/
mv %{buildroot}/%{_bindir}/login %{buildroot}/bin/

# remove not needed files
rm %{buildroot}/%{_sysconfdir}/login.access
rm %{buildroot}/%{_sysconfdir}/limits
rm %{buildroot}/%{_bindir}/chfn
rm %{buildroot}/%{_bindir}/chsh
rm %{buildroot}/%{_sbindir}/chgpasswd
rm %{buildroot}/%{_sbindir}/grpck
rm %{buildroot}/%{_sbindir}/grpconv
rm %{buildroot}/%{_sbindir}/grpunconv
rm %{buildroot}/%{_sbindir}/pwck
rm %{buildroot}/%{_sbindir}/pwconv
rm %{buildroot}/%{_sbindir}/pwunconv
rm %{buildroot}/%{_sbindir}/vigr
rm %{buildroot}/%{_sbindir}/vipw
rm %{buildroot}/%{_includedir}/shadow/subid.h
rm %{buildroot}/%{_libdir}/libsubid.a
rm %{buildroot}/%{_libdir}/libsubid.la
rm %{buildroot}/%{_libdir}/libsubid.so

%remove_docs

%files
%manifest %{name}.manifest
%license COPYING.GPL-2.0+ COPYING.BSD-3-Clause
%dir %{_sysconfdir}/default
%attr(0600,root,root)   %config(noreplace) %{_sysconfdir}/default/useradd
%attr(0644,root,root)   %config(noreplace) %{_sysconfdir}/login.defs
/bin/login
%{_bindir}/faillog
%{_bindir}/lastlog
%{_bindir}/sg
%{_sbindir}/chpasswd
%{_sbindir}/groupadd
%{_sbindir}/groupdel
%{_sbindir}/groupmod
%{_sbindir}/newusers
%{_sbindir}/nologin
%{_sbindir}/useradd
%{_sbindir}/userdel
%{_sbindir}/usermod
%exclude /usr/lib/debug
%exclude /bin/login
%exclude %{_sbindir}/nologin

%files -n %{name}-adm
%license COPYING.GPL-2.0+ COPYING.BSD-3-Clause
/bin/su
%{_bindir}/chage
%{_bindir}/gpasswd
%{_bindir}/newgrp
%{_bindir}/passwd
%{_bindir}/newgidmap
%{_bindir}/newuidmap
%{_bindir}/getsubids
%{_libdir}/libsubid.so.*
