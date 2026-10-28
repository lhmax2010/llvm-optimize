# enable debug features such as control environment variables
# WARNING! do not use for production builds as it will break security

Name:    tlm
Summary: Login manager for Tizen
Version: 1.0.3
Release: 1
Group:   System/Service
License: LGPL-2.1+
URL:     https://github.com/01org/tlm
Source:     %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
Requires(post): /sbin/ldconfig
Requires(post): systemd
Requires(postun): /sbin/ldconfig
Requires(postun): systemd
Requires(post): tizen-platform-config
Requires: libsystemd
Requires: pam-modules-extra
BuildRequires: python3-setuptools
BuildRequires: pkgconfig(glib-2.0) >= 2.38
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(gmodule-2.0)
BuildRequires: pkgconfig(libgum)
BuildRequires: pam-devel
BuildRequires:  pkgconfig(libtzplatform-config)

%description
TLM is a daemon that handles user logins in a multi-user, multi-seat system by
authenticating the users through PAM, and setting up, launching, and tracking
user sessions.

%package devel
Summary:    Dev files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for %{name}.


%package doc
Summary:    Doc files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description doc
Documentation files for %{name}.


%package config-common
Summary:    Common configuration files
Group:      System/Service
Requires:   %{name} = %{version}-%{release}
Provides:   %{name}-config

%description config-common
Tiny Login Manager common configuration files.

%package config-common-singleseat
Summary:    Common configuration files with single seat
Group:      System/Service
Requires:   %{name} = %{version}-%{release}
Provides:   %{name}-config

%description config-common-singleseat
Tiny Login Manager common configuration files with signle seat.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .


%build
# for Address space layout randomization
export CFLAGS="$CFLAGS -fPIE"
export LDFLAGS="$LDFLAGS -pie"

export GTKDOCIZE=echo
%reconfigure --enable-gum \
             %{?extra_config_options1:%extra_config_options1} \
             %{?extra_config_options2:%extra_config_options2}
%__make %{?_smp_mflags}


%install
rm -rf %{buildroot}
%make_install
rm -f %{buildroot}%{_sysconfdir}/tlm.conf
install -m 755 -d %{buildroot}%{_unitdir}
install -m 644 data/tlm.service %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_unitdir}/multi-user.target.wants
ln -s ../tlm.service %{buildroot}%{_unitdir}/multi-user.target.wants/tlm.service
install -m 755 -d %{buildroot}%{_sysconfdir}/pam.d
install -m 644 data/tlm-login %{buildroot}%{_sysconfdir}/pam.d/
install -m 644 data/tlm-default-login %{buildroot}%{_sysconfdir}/pam.d/
install -m 644 data/tlm-system-login %{buildroot}%{_sysconfdir}/pam.d/
install -m 755 -d %{buildroot}%{_sysconfdir}/session.d
install -m 644 data/tizen-common/etc/tlm*.conf %{buildroot}%{_sysconfdir}
install -m 755 data/tizen-common/etc/session.d/* %{buildroot}%{_sysconfdir}/session.d/
chmod 700 %{buildroot}%{_bindir}/%{name}
chmod 700 %{buildroot}%{_bindir}/%{name}-sessiond
chmod 700 %{buildroot}%{_bindir}/%{name}-launcher

%if "%{asan}" == "1"
mkdir -p %{buildroot}%{_unitdir}/tlm.service.d
install -m 644 data/tlm.asan.conf %{buildroot}%{_unitdir}/tlm.service.d
%endif

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig


%post config-common
if [ ! -e /etc/tlm.conf ] || [ -h /etc/tlm.conf ]; then
	ln -s -f /etc/tlm-default.conf /etc/tlm.conf
fi
systemctl enable tlm
systemctl daemon-reload

%preun config-common
if [ $1 == 0 ]; then
	systemctl disable tlm
	systemctl daemon-reload
fi

%postun config-common
if [ -h /etc/tlm.conf ] && [ $1 == 0 ]; then
	rm -f /etc/tlm.conf
fi


%post config-common-singleseat
if [ ! -e /etc/tlm.conf ] || [ -h /etc/tlm.conf ]; then
	ln -s -f /etc/tlm-singleseat.conf /etc/tlm.conf
fi
#systemctl enable tlm
#systemctl daemon-reload

#%preun config-common-singleseat
#if [ $1 == 0 ]; then
	#systemctl disable tlm
	#systemctl daemon-reload
#fi

%postun config-common-singleseat
if [ -h /etc/tlm.conf ] && [ $1 == 0 ]; then
	rm -f /etc/tlm.conf
fi

%files
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license COPYING
%doc AUTHORS NEWS README
%{_bindir}/%{name}
%{_bindir}/%{name}-sessiond
%{_bindir}/%{name}-client
%{_bindir}/%{name}-launcher
%{_libdir}/lib%{name}*.so.*
%{_libdir}/%{name}/plugins/*.so*
%{_unitdir}/tlm.service
%{_unitdir}/multi-user.target.wants/tlm.service
%config %{_sysconfdir}/pam.d/tlm-login
%config %{_sysconfdir}/pam.d/tlm-default-login
%config %{_sysconfdir}/pam.d/tlm-system-login
%if "%{asan}" == "1"
%{_unitdir}/tlm.service.d/tlm.asan.conf
%endif


%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/*.h
%{_libdir}/lib%{name}*.so
%{_libdir}/pkgconfig/%{name}.pc

%files doc
%defattr(-,root,root,-)
%{_datadir}/gtk-doc/html/tlm/*


%files config-common
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license COPYING
%config(noreplace) %{_sysconfdir}/tlm-default.conf
%config(noreplace) %{_sysconfdir}/session.d/*

%files config-common-singleseat
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license COPYING
%config(noreplace) %{_sysconfdir}/tlm-singleseat.conf
