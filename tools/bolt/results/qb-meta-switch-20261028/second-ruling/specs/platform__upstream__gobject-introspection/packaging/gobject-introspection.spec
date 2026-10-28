Name:           gobject-introspection
Version:        1.80
Release:        0
Summary:        GObject Introspection Tools
License:        GPL-2.0-or-later
Group:          Development/Libraries
Url:            http://live.gnome.org/GObjectIntrospection
Source0:        %{name}-%{version}.tar.gz
Source1:        gi-find-deps.sh
Source2:        gobjectintrospection.attr
Source3:        gobject-introspection-typelib.template
Source4:        doctool_disable.patch
Source5:        add_pie_compile_option.patch
Source6:        cairo_disabled.patch
Source7:        install_glib_gmodule_gobject_gir.patch
Source8:        gi_scanner_dumper_pie.patch
Source99:       %{name}-rpmlintrc
Source1001: 	gobject-introspection.manifest

BuildRequires:  bison
BuildRequires:  fdupes
BuildRequires:  flex
BuildRequires:  libffi-devel
BuildRequires:  libtool

BuildRequires:  meson
BuildRequires:  ninja
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-mako
BuildRequires:  python3-markdown
BuildRequires:  python3-xml
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm

Requires:       libgirepository = %{version}
Requires:       python3-xml

%description
The goal of the project is to describe the APIs and collect them in
a uniform, machine readable format.

%package -n libgirepository
Summary:        GObject Introspection Library
License:        LGPL-2.1-or-later
Group:          System/Libraries
Requires:       girepository >= %{version}

%description -n libgirepository
The goal of the project is to describe the APIs and collect them in
a uniform, machine readable format.

%package -n girepository
Summary:        Base GObject Introspection Bindings
License:        LGPL-2.1-or-later
Group:          System/Libraries
Requires:       libgirepository >= %{version}
%(cat %{S:3} | awk '{ print "Provides: " $0}')

%description -n girepository
The goal of the project is to describe the APIs and collect them in
a uniform, machine readable format.

%package devel
Summary:        GObject Introspection Development Files
License:        LGPL-2.1-or-later
Group:          Development/Libraries
# Note: the devel package requires the binaries, not just the library
Requires:       %{name} = %{version}
Requires:       libffi-devel

%description devel
The goal of the project is to describe the APIs and collect them in
a uniform, machine readable format.

%prep
%setup -q
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE4}
%{__patch} -p1 < %{SOURCE5}
%{__patch} -p1 < %{SOURCE6}
%{__patch} -p1 < %{SOURCE7}
%{__patch} -p1 < %{SOURCE8}

%build
CFLAGS="$CFLAGS -fPIC"
chmod +x tools/g-ir-tool-template.in

%meson
%meson_build

# %check
# meson test -C armv7l-tizen-linux

%install
%meson_install

install -D %{S:1} %{buildroot}%{_rpmconfigdir}/gi-find-deps.sh
install -D %{S:2} -m 0644 %{buildroot}%{_rpmconfigdir}/fileattrs/gobjectintrospection.attr

# ls %{buildroot}%{_libdir}/girepository-1.0/*.typelib | sh %{S:1} -P > gobject-introspection-typelib.installed
# diff -s %{S:3} gobject-introspection-typelib.installed

%fdupes %{buildroot}

%post -n libgirepository -p /sbin/ldconfig

%postun -n libgirepository -p /sbin/ldconfig

%docs_package

%files
%manifest %{name}.manifest
%license COPYING COPYING.GPL
%{_bindir}/g-ir-annotation-tool
%{_bindir}/g-ir-compiler
%{_bindir}/g-ir-generate
%{_bindir}/g-ir-scanner
%{_bindir}/g-ir-inspect
%{_datadir}/aclocal/introspection.m4
%{_datadir}/gir-1.0/*.gir
%{_datadir}/gir-1.0/gir-1.2.rnc
%dir %{_libdir}/gobject-introspection
%{_libdir}/gobject-introspection/giscanner/
%dir %{_datadir}/gobject-introspection-1.0
%{_datadir}/gobject-introspection-1.0/Makefile.introspection
%{_datadir}/gobject-introspection-1.0/tests/
%{_datadir}/gobject-introspection-1.0/gdump.c
%{_rpmconfigdir}/gi-find-deps.sh
%{_rpmconfigdir}/fileattrs/gobjectintrospection.attr

%files -n libgirepository
%manifest %{name}.manifest
%license COPYING.LGPL
%dir %{_datadir}/gir-1.0
%{_libdir}/libgirepository-1.0.so.*
%dir %{_libdir}/girepository-1.0

%files -n girepository
%manifest %{name}.manifest
%license COPYING.LGPL
%{_libdir}/girepository-1.0/*.typelib

%files devel
%manifest %{name}.manifest
%{_includedir}/gobject-introspection-1.0/
%{_libdir}/libgirepository-1.0.so
%{_libdir}/pkgconfig/gobject-introspection-1.0.pc
%{_libdir}/pkgconfig/gobject-introspection-no-export-1.0.pc
