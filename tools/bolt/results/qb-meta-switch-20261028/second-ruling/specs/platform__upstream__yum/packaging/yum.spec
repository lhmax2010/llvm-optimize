%define auto_sitelib 1
%define disable_check 1

# We always used /usr/lib here, even on 64bit ... so it's a bit meh.
%define yum_pluginslib   /usr/lib/yum-plugins
%define yum_pluginsshare /usr/share/yum-plugins

Name:           yum
Version:        3.4.3
Release:        0
License:        GPL-2.0+
Summary:        RPM package installer/updater/manager
Group:          System/Base
Source0:        http://yum.baseurl.org/download/3.4/%{name}-%{version}.tar.gz
Source1:        yum.conf
Source1001: 	yum.manifest

Url:            http://yum.baseurl.org/
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  python-gpgme
BuildRequires:  python >= 2.4
BuildRequires:  python-iniparse
BuildRequires:  python-nose
BuildRequires:  python-urlgrabber >= 3.9.0
BuildRequires:  rpm >= 4.10.0
BuildRequires:  python-rpm
BuildRequires:  yum-metadata-parser >= 1.1.0
Requires:       python-gpgme
Requires:       python >= 2.7
Requires:       python-iniparse
Requires:       python-urlgrabber >= 3.9.0
Requires:       rpm >= 4.10.0
Requires:       python-rpm
Requires:       yum-metadata-parser >= 1.1.0
BuildArch:      noarch

%description
Yum is a utility that can check for and automatically download and
install updated RPM packages. Dependencies are obtained and downloaded
automatically, prompting the user for permission as necessary.

%prep
%setup -q
cp %{SOURCE1001} .

%build
make

%check
make check


%install
make DESTDIR=%{buildroot} UNITDIR=%{_unitdir} install
install -m 644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/yum.conf
mkdir -p %{buildroot}/%{_sysconfdir}/yum/pluginconf.d %{buildroot}/%{yum_pluginslib}
mkdir -p %{buildroot}/%{yum_pluginsshare}

mv %{buildroot}/%{_sysconfdir}/yum/repos.d %{buildroot}/%{_sysconfdir}/yum.repos.d

# yum-updatesd has moved to the separate source version
rm -f %{buildroot}/%{_sysconfdir}/yum/yum.conf
rm -f %{buildroot}/%{_sysconfdir}/yum/yum-updatesd.conf
rm -f %{buildroot}/%{_sysconfdir}/rc.d/init.d/yum-updatesd
rm -f %{buildroot}/%{_sysconfdir}/dbus-1/system.d/yum-updatesd.conf
rm -f %{buildroot}/%{_sbindir}/yum-updatesd
rm -f %{buildroot}/%{_mandir}/man*/yum-updatesd*
rm -f %{buildroot}/%{_datadir}/yum-cli/yumupd.py*

rm -rf %{buildroot}/etc/cron.daily
rm -rf %{buildroot}/etc/sysconfig/yum-cron
rm -rf %{buildroot}/etc/yum/yum-daily.yum
rm -rf %{buildroot}/etc/yum/yum-weekly.yum
rm -rf %{buildroot}/etc/rc.d/init.d

# Ghost files:
mkdir -p %{buildroot}%{_localstatedir}/lib/yum/history
mkdir -p %{buildroot}%{_localstatedir}/lib/yum/plugins
mkdir -p %{buildroot}%{_localstatedir}/lib/yum/yumdb
touch %{buildroot}%{_localstatedir}/lib/yum/uuid

# rpmlint bogus stuff...
chmod +x %{buildroot}/%{_datadir}/yum-cli/*.py
chmod +x %{buildroot}/%{python_sitelib}/yum/*.py
chmod +x %{buildroot}/%{python_sitelib}/rpmUtils/*.py

%find_lang %{name}



%files -f %{name}.lang
%manifest %{name}.manifest
%defattr(-, root, root, -)
%license  COPYING
%config(noreplace) %{_sysconfdir}/yum.conf
%dir %{_sysconfdir}/yum.repos.d
%config(noreplace) %{_sysconfdir}/yum/version-groups.conf
%dir %{_sysconfdir}/yum
%dir %{_sysconfdir}/yum/protected.d
%dir %{_sysconfdir}/yum/vars
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_sysconfdir}/bash_completion.d
%{_datadir}/yum-cli/
%{_bindir}/yum
%{python_sitelib}/yum
%{python_sitelib}/rpmUtils
%dir %{_localstatedir}/cache/yum
%dir %{_localstatedir}/lib/yum
%ghost %{_localstatedir}/lib/yum/uuid
%ghost %{_localstatedir}/lib/yum/history
%ghost %{_localstatedir}/lib/yum/plugins
%ghost %{_localstatedir}/lib/yum/yumdb
%{_mandir}/man*/yum.*
%{_mandir}/man*/yum-shell*
# plugin stuff
%dir %{_sysconfdir}/yum/pluginconf.d
%dir %{yum_pluginslib}
%dir %{yum_pluginsshare}

