Name:           json-glib
Version:        1.8.0
Release:        0
Summary:        Library for JavaScript Object Notation format
License:        LGPL-2.1-or-later
Group:          Development/Libraries/C and C++
Url:            https://wiki.gnome.org/Projects/JsonGlib
Source0:        https://download.gnome.org/sources/json-glib/1.6/%{name}-%{version}.tar.xz
Source99:       baselibs.conf
Source1001:     json-glib.manifest
Source1002:     apply_PIE_option.patch
BuildRequires:  gettext
BuildRequires:  gobject-introspection-devel
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  meson

%description
JSON-GLib provides a parser and a generator GObject classes and various
wrappers for the complex data types employed by JSON, such as arrays
and objects.

JSON-GLib uses GLib native data types and the generic value container
GValue for ease of development. It also provides integration with the
GObject classes for direct serialization into, and deserialization from,
JSON data streams.

%package -n libjson-glib
Summary:        Library for JavaScript Object Notation format
# To make lang subpackage installable
Group:          Development/Libraries/C and C++
Recommends:     %{name}-lang
Provides:       %{name} = %{version}

%description -n libjson-glib
JSON is a lightweight data-interchange format. It is comparatively
easy for humans to read and write, and for machines to parse and generate.

JSON-GLib provides a parser and a generator GObject classes and various
wrappers for the complex data types employed by JSON, such as arrays
and objects.

JSON-GLib uses GLib native data types and the generic value container
GValue for ease of development. It also provides integration with the
GObject classes for direct serialization into, and deserialization from,
JSON data streams.

%package -n typelib-Json
Summary:        Introspection bindings for libjson-glib
Group:          System/Libraries

%description -n typelib-Json
JSON-GLib provides a parser and a generator GObject classes and various
wrappers for the complex data types employed by JSON, such as arrays
and objects.

This package provides the GObject Introspection bindings for JSON-GLib.

%package devel
Summary:        Development files for libjson-glib
Group:          Development/Libraries/C and C++
Requires:       libjson-glib = %{version}
Requires:       typelib-Json = %{version}
#BuildRequires:  gettext
#BuildRequires:  gtk-doc

%description devel
JSON-GLib provides a parser and a generator GObject classes and various
wrappers for the complex data types employed by JSON, such as arrays
and objects.

This package contains development files needed to develop with the
json-glib library.

%lang_package

%prep
%setup -q
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE1002}

%build
export CFLAGS="$CFLAGS -fPIC"

mkdir -p builddir
meson --prefix /usr --libdir %{_libdir} builddir


%check
ninja -C builddir meson-test || exit 0

%install
DESTDIR=%{buildroot} ninja -C builddir install
find %{buildroot}%{_libdir} -name '*.la' -delete -print
%find_lang %{name}-1.0

mv %{name}-1.0.lang %{name}.lang
%__rm -rf %{buildroot}%{_datadir}/gtk-doc

%post -n libjson-glib -p /sbin/ldconfig

%postun -n libjson-glib -p /sbin/ldconfig

%files -n libjson-glib
%license COPYING
%manifest %{name}.manifest
%defattr(-,root,root)
%{_bindir}/json-glib-format
%{_bindir}/json-glib-validate
%{_libdir}/*.so.*

%files -n typelib-Json
%license COPYING
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/girepository-1.0/Json-1.0.typelib

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_includedir}/%{name}-1.0
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/*.gir
%dir %{_datadir}/installed-tests
%dir %{_libexecdir}/installed-tests
%{_datadir}/installed-tests/json-glib-1.0/
%{_libexecdir}/installed-tests/json-glib-1.0/

#%files lang -f %{name}-1.0.lang

%changelog

