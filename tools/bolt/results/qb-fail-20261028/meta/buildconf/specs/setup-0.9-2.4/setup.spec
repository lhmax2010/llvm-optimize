Name:           setup
VCS:            platform/upstream/setup#70262d16a0a4277ec8fbff99c7aa9ce6535cd684
Version:        0.9
Release:        2.4
License:        PD
Summary:        A set of system configuration and setup files
Url:            https://fedorahosted.org/setup/
Group:          Base/Configuration
Source0:        %{name}-%{version}.tar.bz2
Source1001:     setup.manifest
BuildRequires:  bash
%if 0%{?hwasan_build:1}%{?asan:1} == 0
BuildArch:      noarch
%endif

%{?hwasan:
Requires: hwasan-runtime-env
}

%{?asan:
Requires: asan-runtime-env
}

%description
The setup package contains a set of important system configuration and
setup files, such as passwd, group, and profile.

%package misc
Summary:    Misc. basic tools and scripts
Requires:   setup
%description misc
Misc. basic tools and scripts.


%prep
%setup -q

cp %{SOURCE1001} .
./shadowconvert.sh

%build

%check
# Run any sanity checks.
make check

%install

%{?hwasan:
echo 'export QEMU_GUEST_BASE=0x5500000000' >>  files/etc/profile
}

cp -ar files/* %{buildroot}
touch %{buildroot}%{_sysconfdir}/environment
chmod 0644 %{buildroot}%{_sysconfdir}/environment
chmod 0400 %{buildroot}%{_sysconfdir}/{shadow,gshadow} %{buildroot}/opt/etc/shadow
ln -nsf /proc/self/mounts %{buildroot}%{_sysconfdir}/mtab

rm %{buildroot}/%{_sysconfdir}/filesystems

#throw away useless and dangerous update stuff until rpm will be able to
#handle it ( http://rpm.org/ticket/6 )
%post -p <lua>
for i, name in ipairs({"passwd", "shadow", "group", "gshadow"}) do
     os.remove("/etc/"..name..".rpmnew")
end
%files
%manifest %{name}.manifest
%manifest setup.manifest
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/passwd
%verify(not md5 size mtime) %config(noreplace) /opt/etc/passwd
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/group
%verify(not md5 size mtime) %attr(0000,root,root) %config(noreplace,missingok) %{_sysconfdir}/shadow
%verify(not md5 size mtime) %attr(0000,root,root) %config(noreplace,missingok) /opt/etc/shadow
%verify(not md5 size mtime) %attr(0000,root,root) %config(noreplace,missingok) %{_sysconfdir}/gshadow
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/services
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/exports
%config(noreplace) %{_sysconfdir}/aliases
%config(noreplace) %{_sysconfdir}/environment
%config(noreplace) %{_sysconfdir}/host.conf
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/hosts
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/hosts.allow
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/hosts.deny
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/motd
%config(noreplace) %{_sysconfdir}/printcap
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/inputrc
%config(noreplace) %{_sysconfdir}/bashrc
%config(noreplace) %{_sysconfdir}/profile
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/protocols
%attr(0600,root,root) %config(noreplace,missingok) %{_sysconfdir}/securetty
%dir %{_sysconfdir}/profile.d
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/shells
%ghost %verify(not md5 size mtime) %config(noreplace,missingok) %{_sysconfdir}/mtab
/etc/profile.d/*

%files misc
%manifest %{name}.manifest
%{_bindir}/*
%{_sbindir}/*
%docs_package
%changelog
* Mon Mar 17 2014 Patrick McCarty <patrick.mccarty@linux.intel.com> 83b9d99
- Add a buxton user and group, required for the buxton daemon
* Fri Jan 24 2014 Patrick McCarty <patrick.mccarty@linux.intel.com> d9be8fb
- Add a user and group for polkitd, needed by the polkit package.
- Make /etc/mtab a symbolic link to /proc/self/mounts, as systemd and
  util-linux tools expect.
- Added missing systemd-journal group, required to fix systemd tmpfiles.d
  functionality.
* Mon Sep 16 2013 Anas Nashif <anas.nashif@intel.com> submit/tizen/20130916.050249@02f23a6
- use an existing directory for user nobody
* Thu Jul 25 2013 Anas Nashif <anas.nashif@intel.com> accepted/tizen/20130710.214706@a7fc922
- Add system users
- resetting manifest requested domain to floor
* Fri Jun 28 2013 Anas Nashif <anas.nashif@intel.com> accepted/tizen/20130520.094322@c92e2f6
- Add system users
* Sat May 11 2013 Anas Nashif <anas.nashif@intel.com> submit/tizen/20130509.184218@6ec72c0
- Set license using %%license
* Fri Mar 22 2013 Anas Nashif <anas.nashif@intel.com> submit/trunk/20130222.002810@738735b
- Fixed package groups
* Thu Feb 21 2013 Anas Nashif <anas.nashif@intel.com> 03cc1b1
- Update to 0.9
