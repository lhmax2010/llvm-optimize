%bcond_with x
%bcond_with wayland

Name: e-mod-tizen-processmgr
Version: 0.2.32
Release: 1
Summary: The enlightenment processmgr module for Tizen
Group: Graphics & UI Framework/Other
Source0: %{name}-%{version}.tar.gz
License: BSD-2-Clause
BuildRequires: pkgconfig(enlightenment)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(gio-2.0)
%if %{with x}
BuildRequires: pkgconfig(x11)
Requires: libX11
%endif

%global TZ_SYS_RO_SHARE  %{?TZ_SYS_RO_SHARE:%TZ_SYS_RO_SHARE}%{!?TZ_SYS_RO_SHARE:/usr/share}

%description
This package is a processmgr module for enlightenment.

%prep
%setup -q

%build
export GC_SECTIONS_FLAGS="-fdata-sections -ffunction-sections -Wl,--gc-sections"
CFLAGS="$CFLAGS -Wall -Werror-implicit-function-declaration -g -fPIC -rdynamic ${GC_SECTIONS_FLAGS} -DE_LOGGING=2"
export CFLAGS
LDFLAGS="$LDFLAGS -Wl,--hash-style=both -Wl,--as-needed -Wl,--rpath=/usr/lib"
export LDFLAGS

%if %{with wayland}
%reconfigure --enable-wayland-only
%else
%reconfigure
%endif

make

%install
rm -rf %{buildroot}

# install
make install DESTDIR=%{buildroot}

# clear useless textual files
find  %{buildroot}%{_libdir}/enlightenment/modules/%{name} -name *.la | xargs rm

%files
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/enlightenment/modules/e-mod-tizen-processmgr
