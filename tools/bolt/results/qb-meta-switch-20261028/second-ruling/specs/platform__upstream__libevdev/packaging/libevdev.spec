Name:           libevdev
Version:        1.13.7
Release:        0
License:        MIT and Apache-2.0
Summary:        wrapper library for evdev input devices
Url:            git://anongit.freedesktop.org/libevdev
Group:          System/Libraries
Source:         %{name}-%{version}.tar.gz
Source1001:		%name.manifest

BuildRequires:  doxygen
BuildRequires:  meson
BuildRequires:  python

%{!?TZ_SYS_RO_SHARE: %global TZ_SYS_RO_SHARE /usr/share}

%description
libevdev is a wrapper library for evdev devices. it moves the common
tasks when dealing with evdev devices into a library and provides a library
interface to the callers, thus avoiding erroneous ioctls, etc.


%package devel
Summary:    wrapper library for evdev input devices
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
libevdev is a wrapper library for evdev devices. it moves the common
tasks when dealing with evdev devices into a library and provides a library
interface to the callers, thus avoiding erroneous ioctls, etc.

%prep
%setup -q
cp %{SOURCE1001} .

%build
meson setup \
    -Ddocumentation=disabled \
    -Dtests=disabled \
    -Dtools=disabled \
    --prefix /usr \
    --libdir %{_libdir} \
    --bindir %{_bindir} \
    builddir
ninja -C builddir all

%install
export DESTDIR=%{buildroot}
ninja -C builddir install
#%fdupes %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING doc/style/LICENSE
%{_libdir}/*.so.*

## disable tools ##
#%{_bindir}/libevdev
#/usr/libexec/libevdev/*
#%doc %{_mandir}/man?/*

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
