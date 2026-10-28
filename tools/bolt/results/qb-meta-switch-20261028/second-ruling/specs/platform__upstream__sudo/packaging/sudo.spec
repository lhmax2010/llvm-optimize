%if ! %{defined _distconfdir}
%define _distconfdir %{_sysconfdir}
%else
%define use_usretc 1
%endif

Name:           sudo
Version:        1.9.17p2
Release:        0
Summary:        Execute some commands as root
License:        ISC
Group:          System/Utilities
Url:            http://www.sudo.ws/
Source0:        http://sudo.ws/sudo/dist/%{name}-%{version}.tar.gz
Source1:        sudo.pamd
Source1001:     sudo.manifest
Source1002:     add_audit_arch_aarch64.patch
BuildRequires:  groff
BuildRequires:  pam-devel
Requires(pre):  coreutils

%description
Sudo is a command that allows users to execute some commands as root.
The /etc/sudoers file (edited with 'visudo') specifies which users have
access to sudo and which commands they can run. Sudo logs all its
activities to syslogd, so the system administrator can keep an eye on
things. Sudo asks for the password for initializing a check period of a
given time N (where N is defined at installation and is set to 5
minutes by default).

%package devel
Summary:        Header files needed for sudo plugin development
Group:          System/Utilities

%description devel
These header files are needed for building of sudo plugins.

%package rpm
Summary:        Script making possible to run RPM as root from inside build
Group:          System/Utilities
Requires:       sudo

%description rpm
The package will add ALL ALL = (root) NOPASSWD: /usr/bin/rpm to sudoers and
makes possible to install packages from inside build.

%prep
%setup -q
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE1002}

%build
F_PIE=-fpie
export CFLAGS="%{optflags} -Wall $F_PIE"
%{?asan:LDFLAGS+=" -ldl"}
%configure \
--libexecdir=%{_libexecdir}/sudo \
--docdir=%{_docdir}/%{name} \
--with-noexec=%{_libexecdir}/sudo/sudo_noexec.so \
--with-pam \
--with-logfac=auth \
--without-insults \
--with-ignore-dot \
--with-tty-tickets \
--enable-shell-sets-home \
--enable-warnings \
--with-sudoers-mode=0440 \
--with-env-editor \
--without-secure-path \
--with-passprompt='%%p\x27s password:' \
--with-rundir=%{_localstatedir}/lib/sudo \
--enable-pie
%__make %{?_smp_mflags}

%install
#%%make_install
%{__make} \
DESTDIR=%{?buildroot:%{buildroot}} \
INSTALL_ROOT=%{?buildroot:%{buildroot}} \
install install_uid=`id -u` install_gid=`id -g`

rm -f %{?buildroot:%{buildroot}}%{_infodir}/dir
find %{?buildroot:%{buildroot}} -regex ".*\\.la$" | xargs rm -f --
%{!?keepstatic:find %{?buildroot:%{buildroot}} -regex ".*\\.a$" | xargs rm -f --}

install -d -m 755 %{buildroot}%{_sysconfdir}/pam.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/sudo
rm -f %{buildroot}%{_bindir}/sudoedit
ln -sf %{_bindir}/sudo %{buildroot}%{_bindir}/sudoedit
rm -f %{buildroot}%{_docdir}/%{name}/sample.pam
rm -f %{buildroot}%{_docdir}/%{name}/sample.syslog.conf
rm -f %{buildroot}%{_docdir}/%{name}/schema.OpenLDAP
rm -f %{buildroot}%{_libexecdir}/%{name}/sudoers.la
rm -f %{buildroot}%{_sysconfdir}/sudoers.dist
%find_lang %{name}
%find_lang sudoers
cat sudoers.lang >> %{name}.lang

%post
chmod 0440 %{_sysconfdir}/sudoers

%post rpm
echo 'ALL ALL = (root) NOPASSWD: /usr/bin/rpm' >> %{_sysconfdir}/sudoers

%lang_package

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license LICENSE.md
%doc %{_docdir}/%{name}
%{_mandir}/man1/cvtsudoers.1%{?ext_man}
%{_mandir}/man5/sudoers.5%{?ext_man}
%{_mandir}/man5/sudo.conf.5%{?ext_man}
%{_mandir}/man5/sudoers_timestamp.5%{?ext_man}
%{_mandir}/man8/sudo.8%{?ext_man}
%{_mandir}/man8/sudoedit.8%{?ext_man}
%{_mandir}/man8/sudoreplay.8%{?ext_man}
%{_mandir}/man8/visudo.8%{?ext_man}
%{_mandir}/man5/sudo_logsrv.proto.5%{?ext_man}
%{_mandir}/man5/sudo_logsrvd.conf.5%{?ext_man}
%{_mandir}/man8/sudo_logsrvd.8%{?ext_man}
%{_mandir}/man8/sudo_sendlog.8%{?ext_man}

%config(noreplace) %attr(0440,root,root) %{_sysconfdir}/sudoers
%attr(0750,root,root) %dir %{_sysconfdir}/sudoers.d
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sudo.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sudo_logsrvd.conf
%config(noreplace) %{_sysconfdir}/pam.d/sudo
%attr(4755,root,root) %{_bindir}/sudo

%{_bindir}/sudoedit
%{_bindir}/sudoreplay
%{_bindir}/cvtsudoers
%{_sbindir}/visudo
%{_sbindir}/sudo_logsrvd
%{_sbindir}/sudo_sendlog
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/sudo_noexec.so
%dir %{_libexecdir}/%{name}/%{name}
%{_libexecdir}/%{name}/%{name}/sudoers.so
%{_libexecdir}/%{name}/%{name}/group_file.so
%{_libexecdir}/%{name}/%{name}/system_group.so
%{_libexecdir}/%{name}/%{name}/audit_json.so
%{_libexecdir}/%{name}/%{name}/sudo_intercept.so
%{_libexecdir}/%{name}/libsudo_util.so.*
%attr(0711,root,root) %dir %ghost %{_localstatedir}/lib/%{name}
%attr(0700,root,root) %dir %ghost %{_localstatedir}/lib/%{name}/ts


%files devel
%doc plugins/sample/sample_plugin.c
%{_includedir}/sudo_plugin.h
%{_mandir}/man5/sudo_plugin.5%{?ext_man}
%{_libexecdir}/%{name}/libsudo_util.so*


%files rpm
