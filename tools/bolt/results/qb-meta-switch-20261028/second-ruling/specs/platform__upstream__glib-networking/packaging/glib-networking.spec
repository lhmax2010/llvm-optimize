%bcond_with libproxy
Name:           glib-networking
Version:        2.72.alpha
Release:        0
License:        LGPL-2.1+
Summary:        Network-related GIO modules for glib
Group:          System/Libraries
Source:         http://download.gnome.org/sources/glib-networking/2.72/%{name}-%{version}.tar.xz
Source99:       baselibs.conf
Source1001:     glib-networking.manifest
Url:            http://www.gnome.org
BuildRequires:  intltool
BuildRequires:  libgcrypt-devel
BuildRequires:  meson
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(gio-2.0) >= 2.46.0
BuildRequires:  pkgconfig(openssl3)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  ca-certificates-devel
Requires: ca-certificates
%if %{with libproxy}
BuildRequires:  pkgconfig(libproxy-1.0)
%endif

%description
This package contains network-related GIO modules for glib.

Currently, there is only a proxy module based on libproxy.

%lang_package

%prep
%setup -q
cp %{SOURCE1001} .

%build
meson --prefix /usr/ --libdir %{_libdir} build \
		  -Dstatic_modules=false \
		  -Dgnutls=disabled \
		  -Dopenssl=enabled \
		  -Ddefault_ca_file=%{TZ_SYS_RO_CA_BUNDLE} \
		  -Dtizen_ext=true \
		  -Dtizen_debug=true
ninja -C build all

%install
export DESTDIR=%{buildroot}
ninja -C build install

%find_lang %{name}

%files
%manifest %{name}.manifest
%defattr(-, root, root)
%license COPYING
%{_libdir}/gio/modules/libgioopenssl.so
%if %{with libproxy}
%{_libdir}/gio/modules/libgiolibproxy.so
%{_libexecdir}/glib-pacrunner
%{_datadir}/dbus-1/services/org.gtk.GLib.PACRunner.service
%endif
