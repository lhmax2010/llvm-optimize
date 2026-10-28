
#These options are DEACTIVATED by default.
%bcond_with wayland
%bcond_with emulator

Name:       feedbackd
Summary:    Feedbackd
Version:    1.0.0
Release:    1
Group:      System/Management
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    feedbackd.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(libsyscommon)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(capi-system-device)
BuildRequires:  pkgconfig(hal-api-device)
BuildRequires:  pkgconfig(hal-api-common)

Requires(post): /usr/bin/vconftool

Requires:	configuration-compat = %{version}-%{release}
Recommends:	%{name}-conf-level6 = %{version}-%{release}

%description
feedback daemon

%package feedbackd
Summary:    feedback daemon
Group:      main

%description feedbackd
feedback daemon.

%package conf-level3
Summary:	Feedbackd level configuration file
Provides:	configuration-compat = %{version}-%{release}
Conflicts:	%{name}-conf-level6
%description conf-level3
Feedbackd level configuration file. Required by main feedbackd package

%package conf-level6
Summary:	Feedbackd level configuration file
Provides:	configuration-compat = %{version}-%{release}
Conflicts:	%{name}-conf-level3
%description conf-level6
Feedbackd level configuration file. Required by main feedbackd package

%package auto-test
Summary:  Feedbackd auto test tool
Group:    System/Utilities
%description auto-test
Feedbackd helper programs.
This package can be installed optional for auto dbus test.

%prep
%setup -q

%cmake . \
        -DCMAKE_C_COMPILER=%__cc \
        -DCMAKE_CXX_COMPILER=%__cxx \
        -DCMAKE_INSTALL_PREFIX=%{_prefix} \

%build
cp %{SOURCE1} .
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%install_service delayed.target.wants feedbackd.service

%post
systemctl daemon-reload
if [ "$1" == "1" ]; then
    systemctl restart feedbackd.service
fi

%postun
systemctl daemon-reload

%post conf-level3
mv %{_sysconfdir}/feedbackd/haptic-level3.conf %{_sysconfdir}/feedbackd/haptic.conf

%post conf-level6
mv %{_sysconfdir}/feedbackd/haptic-level6.conf %{_sysconfdir}/feedbackd/haptic.conf

%files -n feedbackd
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%config %{_sysconfdir}/dbus-1/system.d/feedbackd.conf
%{_unitdir}/feedbackd.service
%{_unitdir}/delayed.target.wants/feedbackd.service
%{_datadir}/dbus-1/system-services/org.tizen.system.vibrator.service
%{_bindir}/feedbackd

%files conf-level3
%license LICENSE.Apache-2.0
%manifest %{name}.manifest
%config %{_sysconfdir}/feedbackd/haptic-level3.conf

%files conf-level6
%license LICENSE.Apache-2.0
%manifest %{name}.manifest
%config %{_sysconfdir}/feedbackd/haptic-level6.conf

%files auto-test
%license LICENSE.Apache-2.0
%manifest %{name}.manifest
%{_bindir}/feedbackd-auto-test
