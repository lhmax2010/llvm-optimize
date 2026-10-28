%define udev_dir %{_prefix}/lib/udev

Name:           libinput
Version:        1.31.3
Release:        0
License:        MIT and Apache-2.0
Summary:        Input devices for display servers and other applications
Url:            http://www.freedesktop.org/software/libinput/libinput-%{version}.tar.xz
Group:          System/Libraries
Source:         %{name}-%{version}.tar.gz
Source1001:		%name.manifest
#X-Vcs-Url:      git://anongit.freedesktop.org/wayland/libinput

BuildRequires:  meson
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libevent)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(mtdev)
BuildRequires:  pkgconfig(ttrace)
BuildRequires:  pkgconfig(gmock)

%global TZ_SYS_RO_SHARE  %{?TZ_SYS_RO_SHARE:%TZ_SYS_RO_SHARE}%{!?TZ_SYS_RO_SHARE:/usr/share}

%description

libinput is a library that handles input devices for display servers and
other applications that need to directly deal with input devices.

It provides device detection, device handling, input device event
processing and abstraction so minimize the amount of custom input
code the user of libinput need to provide the common set of
functionality that users expect.


%package devel
Summary:    Input devices for display servers and other applications
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel

libinput is a library that handles input devices for display servers and
other applications that need to directly deal with input devices.

It provides device detection, device handling, input device event
processing and abstraction so minimize the amount of custom input
code the user of libinput need to provide the common set of
functionality that users expect.

%package tools
Summary:    Command line tools for libinput
Group:      System/Tools
Requires:   %{name} = %{version}-%{release}

%description tools
This package contains command line tools to debug, analyze, and test
libinput and input devices.

%package haltests
Summary:    Input HAL Test Cases
Requires:   %{name} = %{version}-%{release}

%description haltests
Input device HAL test cases


%prep
%setup -q
cp %{SOURCE1001} .

%build
meson setup \
    -Dlibwacom=false \
    -Ddocumentation=false \
    -Ddebug-gui=false \
    -Dtests=false \
    -Dudev-dir=%{udev_dir} \
    -Dzshcompletiondir=no \
    -Dtools-enable=true \
    -Dudev-enable=false \
    -Dquirks-enable=false \
    -Dlua-plugins=disabled \
    --prefix /usr \
    --libdir %{_libdir} \
    --bindir %{_bindir} \
    builddir
ninja -C builddir all

%install
export DESTDIR=%{buildroot}
ninja -C builddir install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING doc/api/style/LICENSE
%{_libdir}/*.so.*

## disable udev ##
#%{udev_dir}/%{name}*
#%{udev_dir}/rules.d/*%{name}*

#%doc %{_mandir}/man?/*

## disable quirks data ##
#%{TZ_SYS_RO_SHARE}/libinput/*

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files tools
%manifest %{name}.manifest
%defattr(-,root,root)
%{_bindir}/libinput
/usr/libexec/libinput/*

%files haltests
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bindir}/hal/input-haltests
