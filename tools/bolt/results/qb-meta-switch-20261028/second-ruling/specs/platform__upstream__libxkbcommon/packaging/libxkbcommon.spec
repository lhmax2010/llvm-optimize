Name:           libxkbcommon
Version:        1.13.2
Release:        0
License:        BSD-3-Clause and MIT
Summary:        Wayland libxkbcommon library
Url:            http://wayland.freedesktop.org/
Group:          Development/Libraries

Source:         %{name}-%{version}.tar.xz
#X-Vcs-Url:     https://github.com/xkbcommon/libxkbcommon.git
Source1001:     libxkbcommon.manifest
BuildRequires:  meson
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  libtool >= 2
BuildRequires:  pkgconfig(xorg-macros) >= 1.8
BuildRequires:  python3-base
BuildRequires:  xkb-tizen-data
BuildRequires:  gawk

## This BuildRequires is needed when an enable-wayland option is true.
#BuildRequires:  pkgconfig(wayland-client)
#BuildRequires:  wayland-protocols

## This BuildRequires is needed when an enable-xkbregistry option is true.
#BuildRequires:  pkgconfig(libxml-2.0)

%global TZ_SYS_RO_SHARE  %{?TZ_SYS_RO_SHARE:%TZ_SYS_RO_SHARE}%{!?TZ_SYS_RO_SHARE:/usr/share}

%description
Keyboard handling library using XKB data.

%package devel
Summary:        Development files for the Wayland libxkbcommon library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Keyboard handling library using XKB data.

This package contains the development headers for the library found
in %{name}.

%prep
%setup -q
cp %{SOURCE1001} .

# Generate tizen keymap header
export TZ_SYS_RO_SHARE="%{TZ_SYS_RO_SHARE}"
chmod a+x ./make_tizen_keymap.sh
./make_tizen_keymap.sh
chmod a+x ./gen_tables.sh
./gen_tables.sh

%build
meson setup \
    -Denable-x11=false \
    -Denable-docs=false \
    -Denable-wayland=false \
	-Denable-xkbregistry=false \
	-Denable-tools=false \
	--prefix /usr \
	--libdir %{_libdir} \
	builddir
ninja -C builddir all

%install
export DESTDIR=%{buildroot}
ninja -C builddir install

%post  -p /sbin/ldconfig

%postun  -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING LICENSE.BSD-3-Clause
%{_libdir}/libxkbcommon.so.0*

## disable xkbregistry ##
#%{_libdir}/libxkbregistry.so.0*

## diable tools ##
#%{_bindir}/*
#/usr/libexec/xkbcommon/*
#%doc %{_mandir}/man?/*

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_includedir}/xkbcommon
%{_libdir}/libxkbcommon.so
%{_libdir}/pkgconfig/xkbcommon.pc

## disable xkbregistry ##
#%{_libdir}/libxkbregistry.so
#%{_libdir}/pkgconfig/xkbregistry.pc
