%define _sbindir /sbin
%define _moduledir %{_libdir}/security
%define _secconfdir %{_sysconfdir}/security
%define _pamconfdir %{_sysconfdir}/pam.d

%if "%{_with_da_profile}" == "1"
%define WITH_DA 1
%else
%define WITH_DA 0
%endif

Name:           pam
Version:        1.7.2
Release:        0
License:        BSD-3-Clause or GPL-2.0+
Summary:        A Security Tool that Provides Authentication for Applications
Url:            http://www.linux-pam.org/
Group:          Security/Access Control
Source0:        Linux-PAM-%{version}.tar.bz2
Source1:        system-auth
Source2:        other
Source1001:     pam.manifest

BuildRequires:  meson >= 0.62.0
BuildRequires:  gcc
BuildRequires:  zlib-devel
BuildRequires:  gettext-tools
BuildRequires:  pkgconfig
Requires(post): /sbin/ldconfig
Requires(post): /usr/bin/install
Requires(postun): /sbin/ldconfig

%description
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication.

%package -n pam-modules-extra
Summary:        Extra modules provided by PAM not used in the base system
Group:          Security/Access Control
Requires:       %{name} = %{version}

%description -n pam-modules-extra
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication. This package
contains extra modules for use by programs that are not used in the
default Tizen install.

%package -n pam-modules-debug
Summary:        Debugging tools and modules provided by PAM not used in the base system
Group:          Security/Access Control
Requires:       %{name} = %{version}

%description -n pam-modules-debug
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication. This package
contains security-sensitive debugging tools and modules for use by
programs that are not used in the default Tizen install.

%package devel
Summary:        Files needed for developing PAM-aware applications and modules for PAM
Requires:       %{name} = %{version}

%description devel
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication. This package
contains header files and static libraries used for building both
PAM-aware applications and modules for use with PAM.

%prep
%setup -q -n Linux-PAM-%{version}
cp %{SOURCE1001} .

%build
%meson \
        --libdir=%{_libdir} \
        --includedir=%{_includedir} \
        -Disadir=../..%{_moduledir} \
        -Daudit=disabled \
        -Ddb-uniquename=_pam \
        -Dread-both-confs=true \
        -Dpwaccess=disabled \
        -Deconf=disabled \
        -Dselinux=disabled \
        -Dlogind=disabled \
        -Delogind=disabled \
        -Dpam_userdb=disabled \
        -Dnis=disabled \
        -Ddocs=disabled \
        -Dpam_lastlog=enabled \
        -Dvendordir=/etc \
        -Dpam_unix-try-getspnam=true
%meson_build

%install
%meson_install

# RPM uses docs from source tree
rm -rf %{buildroot}%{_datadir}/doc/Linux-PAM
# Included in setup package
rm -f %{buildroot}%{_sysconfdir}/environment

for phase in auth acct passwd session ; do
    ln -sf pam_unix.so %{buildroot}%{_moduledir}/pam_unix_${phase}.so
done

# Install default pam configuration files
install -d -m 0755 %{buildroot}%{_pamconfdir}
install -m 0644 %{SOURCE1} %{buildroot}%{_pamconfdir}/
install -m 0644 %{SOURCE2} %{buildroot}%{_pamconfdir}/

%find_lang Linux-PAM

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%lang_package -f Linux-PAM
%license Copyright

%files
%manifest %{name}.manifest
%license Copyright
%attr(0755,root,root) %{_sbindir}/mkhomedir_helper
%attr(0755,root,root) %{_sbindir}/pam_namespace_helper
%config %{_sysconfdir}/security/limits.conf
%{_libdir}/libpam.so.*
%{_libdir}/libpam_misc.so.*
%{_libdir}/libpamc.so.*
%{_moduledir}/pam_deny.so
%{_moduledir}/pam_env.so
%{_moduledir}/pam_keyinit.so
%{_moduledir}/pam_limits.so
%{_moduledir}/pam_loginuid.so
%{_moduledir}/pam_namespace.so
%{_moduledir}/pam_nologin.so
%{_moduledir}/pam_permit.so
%{_moduledir}/pam_lastlog.so
%{_moduledir}/pam_rootok.so
%{_moduledir}/pam_securetty.so
%{_moduledir}/pam_succeed_if.so
%{_moduledir}/pam_unix.so
%{_moduledir}/pam_unix_optfiles.so
%{_moduledir}/pam_wheel.so
%{_moduledir}/pam_xauth.so
%{_moduledir}/pam_filter
%{_moduledir}/pam_mkhomedir.so
%dir %{_secconfdir}
%config(noreplace) %{_secconfdir}/access.conf
%config(noreplace) %{_secconfdir}/group.conf
%config(noreplace) %{_secconfdir}/namespace.conf
%attr(755,root,root) %config(noreplace) %{_secconfdir}/namespace.init
%config(noreplace) %{_secconfdir}/pam_env.conf
%config(noreplace) %{_secconfdir}/time.conf
%dir %{_pamconfdir}
%config %{_pamconfdir}/system-auth
%config %{_pamconfdir}/other
%{_unitdir}/pam_namespace.service

%files -n pam-modules-extra
%manifest %{name}.manifest
%license Copyright
%{_moduledir}/pam_access.so
%{_moduledir}/pam_canonicalize_user.so
%{_moduledir}/pam_echo.so
%{_moduledir}/pam_exec.so
%{_moduledir}/pam_faildelay.so
%{_moduledir}/pam_faillock.so
%{_moduledir}/pam_filter.so
%if "%{WITH_DA}" == "1"
%exclude %{_moduledir}/pam_ftp.so
%else
%{_moduledir}/pam_ftp.so
%endif
%{_moduledir}/pam_group.so
%{_moduledir}/pam_issue.so
%{_moduledir}/pam_listfile.so
%{_moduledir}/pam_localuser.so
%if "%{WITH_DA}" == "1"
%exclude %{_moduledir}/pam_mail.so
%else
%{_moduledir}/pam_mail.so
%endif
%{_moduledir}/pam_motd.so
%{_moduledir}/pam_pwhistory.so
%{_moduledir}/pam_rhosts.so
%{_moduledir}/pam_setquota.so
%{_moduledir}/pam_shells.so
%{_moduledir}/pam_stress.so
%{_moduledir}/pam_time.so
%{_moduledir}/pam_timestamp.so
%{_moduledir}/pam_umask.so
%{_moduledir}/pam_unix_acct.so
%{_moduledir}/pam_unix_auth.so
%{_moduledir}/pam_unix_passwd.so
%{_moduledir}/pam_unix_session.so
%{_moduledir}/pam_usertype.so
%{_moduledir}/pam_warn.so
%config(noreplace) %{_secconfdir}/faillock.conf
%config(noreplace) %{_secconfdir}/pwhistory.conf
%attr(0755,root,root) %{_sbindir}/faillock
%attr(0755,root,root) %{_sbindir}/pwhistory_helper

%files -n pam-modules-debug
%{_moduledir}/pam_debug.so
%attr(4755,root,root) %{_sbindir}/pam_timestamp_check
%attr(4755,root,root) %{_sbindir}/unix_chkpwd

%files devel
%manifest %{name}.manifest
%{_includedir}/security/*
%{_libdir}/libpam.so
%{_libdir}/libpam_misc.so
%{_libdir}/libpamc.so
%{_libdir}/pkgconfig/pam.pc
%{_libdir}/pkgconfig/pam_misc.pc
%{_libdir}/pkgconfig/pamc.pc

%docs_package
