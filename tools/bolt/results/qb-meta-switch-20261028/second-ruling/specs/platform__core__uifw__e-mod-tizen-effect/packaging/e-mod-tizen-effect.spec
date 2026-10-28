Name: e-mod-tizen-effect
Version: 0.3.9
Release: 1
Summary: The effect module for the enlightenment
URL: http://www.enlightenment.org
Group: Graphics & UI Framework/Other
Source0: %{name}-%{version}.tar.gz
License: BSD-2-Clause
BuildRequires: pkgconfig(enlightenment)
BuildRequires:  gettext
BuildRequires: pkgconfig(wayland-server)
BuildRequires: pkgconfig(tizen-extension-server)
BuildRequires: pkgconfig(wayland-tbm-server)
BuildRequires: pkgconfig(libtdm)

%global TZ_SYS_RO_SHARE  %{?TZ_SYS_RO_SHARE:%TZ_SYS_RO_SHARE}%{!?TZ_SYS_RO_SHARE:/usr/share}

%description
This package provides various window effect(animation)
as one module of enlightenment.

%prep
%setup -q

%build

export GC_SECTIONS_FLAGS="-fdata-sections -ffunction-sections -Wl,--gc-sections"
export CFLAGS="$CFLAGS -Wall -Werror-implicit-function-declaration -g -fPIC -rdynamic ${GC_SECTIONS_FLAGS} -DE_LOGGING=2"
export LDFLAGS="$LDFLAGS -Wl,--hash-style=both -Wl,--as-needed -Wl,--rpath=/usr/lib"

%autogen
%configure --prefix=%{_prefix}
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
%{_libdir}/enlightenment/modules/e-mod-tizen-effect

