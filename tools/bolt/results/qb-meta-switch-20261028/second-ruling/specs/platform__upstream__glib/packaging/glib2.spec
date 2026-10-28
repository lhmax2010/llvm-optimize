%if "%{?_with_da_profile}" == "1"
%define WITH_DA 1
%else
%define WITH_DA 0
%endif

%define provide_exclude_format ^(.*\.\extension-kdbus|.*\.\extension-symbolic)$
%define build_dir_kdbus _build_kdbus

%global build_glib_kdbus() \
    %define _vpath_builddir %{build_dir_kdbus} \
    %meson --default-library=both -Dkdbus=true -Dlibdbuspolicy=true -Dintrospection=disabled -Dman-pages=false -Dselinux=disabled -Db_pie=true \
    %meson_build

# kdbus extension install and gather required files
%global install_glib_kdbus() \
    %define _vpath_builddir %{build_dir_kdbus} \
    %meson_install \
    for FILE in %{buildroot}%{_libdir}/libgio*[0-9a] %{buildroot}%{_libdir}/libglib*[0-9a]; do mv "$FILE" "$FILE.extension-kdbus"; done

%global exclude_libglib_kdbus() \
    %exclude %{_libdir}/libglib*.so.*.extension-kdbus

%global exclude_libgio_kdbus() \
    %exclude %{_libdir}/libgio*.so.*.extension-kdbus

%global include_glib_kdbus_files() \
    %{_libdir}/lib*.a.extension-kdbus

# Do not create provides from extension .so files because the main package
# should anchor any reverse-dependencies
%global __provides_exclude_from %{provide_exclude_format}

%define baseline 2.80.5
%define with_systemtap 0
%define keepstatic 1
%define build_dir _build
%define build_dir_symbolic _build_symbolic

%define relative_dbus_tests_base_dir %{_libdir}/dbus-tests

Name:           glib2
Version:        2.80.5
Release:        0
# FIXME: find out if tapsets should really be in devel package or in main package
Summary:        General-Purpose Utility Library
License:        LGPL-2.1-or-later
Group:          Base/Libraries
Url:            http://www.gtk.org/
Source:         http://download.gnome.org/sources/glib/%{baseline}/%{name}-%{version}.tar.xz
Source1:        glib2.sh
Source2:        glib2.csh
Source3:        test-runner.c
# Not upstream file. Only proposes upstream packages:
Source4:        glib2-upstream-gnome_defaults.conf
Source6:        macros.glib2
# Not depending on gtk-doc shortens bootstrap compilation path.
# Please update this file from the latest gtk-doc package:
Source7:        gtk-doc.m4
Source8:        LICENSE.MIT
Source99:       baselibs.conf
Source1001: 	glib2.manifest
Source1002:     0001-Disabled-close-range-for-kernel-5.8-below.patch
BuildRequires:  automake
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  m4
BuildRequires:  cmake
BuildRequires:  meson >= 0.49.2
BuildRequires:  pkg-config
BuildRequires:  python3
BuildRequires:  gettext-tools
# gdbus-codegen is run during the build, so we need python-xml
BuildRequires:  python3-xml
BuildRequires:  python3-packaging
%if 0%{?with_systemtap}
BuildRequires:  systemtap-sdt-devel
%endif
# Needed for gresource
BuildRequires:  pkgconfig(libelf) >= 0.8.12
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pcre2-devel
BuildRequires:  pkgconfig(mount) >= 2.28
BuildRequires:  pkgconfig(zlib)
%if %{?WITH_DA}
BuildRequires:  libdbuspolicy-header-devel
%else
BuildRequires:  pkgconfig(libdbuspolicy1)
%endif

%description
GLib is a general-purpose utility library, which provides many useful
data types, macros, type conversions, string utilities, file utilities,
a main loop abstraction, and so on.

%package tools
Summary:        General-Purpose Utility Library -- Tools

%description tools
GLib is a general-purpose utility library, which provides many useful
data types, macros, type conversions, string utilities, file utilities,
a main loop abstraction, and so on.

%package -n gio-branding-upstream
Summary:        Upstream definitions of default settings and applications
Requires:       libgio = %{version}
Provides:       %{name}-branding-upstream = %{version}
Obsoletes:      %{name}-branding-upstream < %{version}
Provides:       gio-branding = %{version}
Conflicts:      otherproviders(gio-branding)
Supplements:    packageand(libgio:branding-upstream)
BuildArch:      noarch
#BRAND: The /etc/gnome_defaults.conf allows to define arbitrary
#BRAND: applications as preferred defaults.
#BRAND: A /usr/share/glib-2.0/schemas/$NAME.gschema.override file can
#BRAND: be used to override the default value for GSettings keys. See
#BRAND: README.Gsettings-overrides for more details. The branding
#BRAND: package should then have proper Requires for features changed
#BRAND: with such an override file.
# NOTE: gnome_defaults is not an upstream feature, but a SuSE
# enhancement, but to conform branding conventions, the package is named
# as gio-branding-upstream.

%description -n gio-branding-upstream
This package provides upstream defaults for settings stored with
GSettings and applications used by the MIME system.

%package devel
#'
Requires:       %{name} = %{version}
Requires:       glibc-devel
Requires:       pkg-config
# Now require the subpackages too
Requires:       glib2-tools = %{version}
Requires:       libgio = %{version}
Requires:       libglib = %{version}
Requires:       libgmodule = %{version}
Requires:       libgobject = %{version}
Requires:       libgthread = %{version}
# Required by gdbus-codegen
Requires:       python3-packaging
Requires:       python3-xml
Requires:       python3
Requires:       python3-setuptools
Provides:       glib2-doc = 2.19.6
Obsoletes:      glib2-doc < 2.19.6
Summary:        General-Purpose Utility Library -- Development Files

%description devel
GLib is a general-purpose utility library, which provides many useful
data types, macros, type conversions, string utilities, file utilities,
a main loop abstraction, and so on.

This package contains the development files for GLib.

%package devel-static
Summary:        Static libraries for glib, a general-purpose utility library
Group:          Development/Libraries/C and C++
Requires:       %{name}-devel = %{version}

%description devel-static
GLib is a general-purpose utility library, which provides many useful
data types, macros, type conversions, string utilities, file utilities,
a main loop abstraction, and so on.

This package contains static versions of the GLib libraries.

%package -n libglib
Summary:        General-Purpose Utility Library
Provides:       %{name} = %{version}
Obsoletes:      %{name} < %{version}

%description -n libglib
GLib is a general-purpose utility library, which provides many useful
data types, macros, type conversions, string utilities, file utilities,
a main loop abstraction, and so on.

%package -n libgmodule
Summary:        General-Purpose Utility Library -- Library for Modules

%description -n libgmodule
The libgmodule library provides a portable way to dynamically load
object files (commonly known as 'plug-ins').

%package -n libgio
Summary:        General-Purpose Utility Library -- Library for VFS
Requires:       gio-branding = %{version}
# bnc#555605: shared-mime-info is required by libgio to properly detect mime types.
Requires:       shared-mime-info
# bnc#678518: libgio interacts with others by means of dbus-launch
#Requires:       dbus-1-x11
Provides:       gio = %{version}

%description -n libgio
GIO provides a modern, easy-to-use VFS API.

%package -n libglib-extension-symbolic
Summary:	Extension for libglib to allow the override of internal defined global function.
Requires:	libglib = %{version}-%{release}
Conflicts:	libglib-extension-kdbus

%package -n libgio-extension-kdbus
Summary:	Extension for libgio to support KDBUS in Tizen
Requires:	libgio = %{version}-%{release}

%description -n libgio-extension-kdbus
This modifies libgio to support KDBUS in Tizen.

%package -n libglib-extension-kdbus
Summary:	Extension for libgio to support KDBUS in Tizen
Requires:	libgio-extension-kdbus = %{version}-%{release}
Conflicts:	libglib-extension-symbolic

%description -n libglib-extension-kdbus
This modifies libgio to support KDBUS in Tizen.

%description -n libglib-extension-symbolic
This modifies libglib to allow the override of internal defined global function.

%package -n libgthread
Summary:        General-Purpose Utility Library -- Library for Threads

%description -n libgthread
The libgthread library provides a portable way to write multi-threaded
software.

%package -n libgobject
Summary:        General-Purpose Utility Library -- Object-Oriented Framework for C

%description -n libgobject
The GObject library provides an object-oriented framework for C.

%package -n libgirepository2
Summary:        General-Purpose Utility Library -- GObject Introspection
Requires:	libgobject = %{version}-%{release}

%description -n libgirepository2
The GObject Introspection library provides an interface for writing
bindings in other languages.

%package tests
License:        LGPL-2.0+ and MIT
Summary:        Set of tests for gdbus component
Requires:       %{name} = %{version}

%description tests
This package is part of 'dbus-integration-tests' framework and contains set of tests
for gdbus component.

%prep
%setup -q -n %{name}-%{version}
%{__patch} -p1 < %{SOURCE1002}

%build
cp %{SOURCE3} .
cp %{SOURCE8} .
cp %{SOURCE1001} .
cp -a %{SOURCE1} %{SOURCE2} .
cp -a %{SOURCE4} gnome_defaults.conf
if ! test -f %{_datadir}/aclocal/gtk-doc.m4 ; then
    cp -a %{SOURCE7} m4macros/
fi

%define _vpath_srcdir .

# Normal build
%define _vpath_builddir %{build_dir}
%meson \
	--default-library=both \
	-Dinstalled_tests=true \
	-Dintrospection=disabled \
	-Dman-pages=false \
	-Dselinux=disabled \
	-Db_pie=true
%meson_build

# Configure symbolic_functions disabled build
%define _vpath_builddir %{build_dir_symbolic}
%meson \
	--default-library=both \
	-Dinstalled_tests=true \
	-Dintrospection=disabled \
	-Dman-pages=false \
	-Dselinux=disabled \
	-Dbsymbolic_functions=false \
	-Db_pie=true
%meson_build

%{?build_glib_kdbus}

# compile test-runner for 'dbus-integration-test' framework
%__cc %{_builddir}/%{name}-%{version}/test-runner.c -DTESTS_DIR='"'%{relative_dbus_tests_base_dir}/test-suites/glib-tests'"' -fPIC -pie -o %{_builddir}/%{name}-%{version}/glib-tests

%install
# symbolic diabled install and gather required files
%define _vpath_builddir %{build_dir_symbolic}
%meson_install
for FILE in %{buildroot}%{_libdir}/libglib*; do mv "$FILE" "$FILE.extension-symbolic"; done

%{?install_glib_kdbus}

# normal install overwriting kdbus extension install
%define _vpath_builddir %{build_dir}
%meson_install
%find_lang glib20 %{?no_lang_C}

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -D -m0644 glib2.sh %{buildroot}%{_sysconfdir}/profile.d/zzz-glib2.sh
install -D -m0644 glib2.csh %{buildroot}%{_sysconfdir}/profile.d/zzz-glib2.csh
install -D -m0644 gnome_defaults.conf %{buildroot}%{_sysconfdir}/gnome_defaults.conf

# gio-querymodules magic
%if "%{_lib}" == "lib64"
mv %{buildroot}%{_bindir}/gio-querymodules %{buildroot}%{_bindir}/gio-querymodules-64
%endif

# prepare tests for 'dbus-integration-test' framework
%define dbus_tests_base_dir %{buildroot}%{relative_dbus_tests_base_dir}

install -D -m 755 %{_builddir}/%{name}-%{version}/glib-tests %{dbus_tests_base_dir}/runner/glib-tests
mkdir -p %{dbus_tests_base_dir}/test-suites/glib-tests/
mv %{buildroot}%{_prefix}/libexec/installed-tests/glib/*gdbus-* %{dbus_tests_base_dir}/test-suites/glib-tests/
# workaround for UNIX fd passing test (gdbus-peer)
echo "Testfile - check for UNIX fd passing" > %{dbus_tests_base_dir}/test-suites/glib-tests/file.c
rm %{dbus_tests_base_dir}/test-suites/glib-tests/gdbus-testserver
rm -Rf %{buildroot}%{_prefix}/libexec/installed-tests/glib/
rm -Rf %{buildroot}%{_prefix}/share/installed-tests/glib/

# Install rpm macros
mkdir -p %{buildroot}%{_sysconfdir}/rpm
cp %{SOURCE6} %{buildroot}%{_sysconfdir}/rpm

mkdir -p %{buildroot}%{_libdir}/gio/modules
mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas/

chmod 755 %{buildroot}%{_bindir}/*

%post -n libglib -p /sbin/ldconfig
%post -n libgobject -p /sbin/ldconfig
%post -n libgthread -p /sbin/ldconfig
%post -n libgio -p /sbin/ldconfig
%post -n libgmodule -p /sbin/ldconfig

%postun -n libglib -p /sbin/ldconfig
%postun -n libgobject -p /sbin/ldconfig
%postun -n libgthread -p /sbin/ldconfig
%postun -n libgio -p /sbin/ldconfig
%postun -n libgmodule -p /sbin/ldconfig

%files tools
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/gresource
%{_datadir}/bash-completion/completions/gsettings
%{_bindir}/gapplication
%{_bindir}/gdbus
%{_bindir}/gio
%{_bindir}/gio-querymodules*
%{_bindir}/glib-compile-schemas
%{_bindir}/gresource
%{_bindir}/gsettings
%{_bindir}/gi-compile-repository
%{_bindir}/gi-decompile-typelib
%{_bindir}/gi-inspect-typelib
%{_libexecdir}/gio-launch-desktop

# We put those files here, but they don't really belong here. They just don't
# have a better home... The zzz-glib2 scripts could arguably be in
# libglib but that would break the shared library policy.
%{_sysconfdir}/profile.d/zzz-glib2.*

%files -n gio-branding-upstream
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%config (noreplace) %{_sysconfdir}/gnome_defaults.conf

%files -n libglib
%manifest %{name}.manifest
%defattr(-, root, root)
%license COPYING
%{?exclude_libglib_kdbus}
%exclude %{_libdir}/libglib*.so.*.extension-symbolic
%{_libdir}/libglib*.so.*

%files -n libgmodule
%manifest %{name}.manifest
%defattr(-, root, root)
%license COPYING
%{_libdir}/libgmodule*.so.*

%files -n libgobject
%manifest %{name}.manifest
%defattr(-, root, root)
%license COPYING
%{_libdir}/libgobject*.so.*

%files -n libgthread
%manifest %{name}.manifest
%defattr(-, root, root)
%license COPYING
%{_libdir}/libgthread*.so.*

%files -n libgirepository2
%manifest %{name}.manifest
%defattr(-, root, root)
%license COPYING
%{_libdir}/libgirepository*.so.*

%files -n libgio
%manifest %{name}.manifest
%defattr(-, root, root)
%license COPYING
%{?exclude_libgio_kdbus}
%{_libdir}/libgio*.so.*
%dir %{_libdir}/gio
%dir %{_libdir}/gio/modules
%ghost %{_libdir}/gio/modules/giomodule.cache
%dir %{_datadir}/glib-2.0/
%dir %{_datadir}/glib-2.0/schemas/
%dir %{_datadir}/glib-2.0/dtds/

%lang_package -f glib20

%post -n libgio-extension-kdbus
for FILE in %{_libdir}/libgio*.so.*.extension-kdbus; do mv "$FILE" "${FILE%.extension-kdbus}"; done

%files -n libgio-extension-kdbus
%manifest %{name}.manifest
%license COPYING
%{_libdir}/libgio*.so.*.extension-kdbus

%post -n libglib-extension-kdbus
for FILE in %{_libdir}/libglib*.so.*.extension-kdbus; do mv "$FILE" "${FILE%.extension-kdbus}"; done

%files -n libglib-extension-kdbus
%manifest %{name}.manifest
%license COPYING
%{_libdir}/libglib*.so.*.extension-kdbus

%post -n libglib-extension-symbolic
for FILE in %{_libdir}/libglib*.so.*.extension-symbolic; do mv "$FILE" "${FILE%.extension-symbolic}"; done

%files -n libglib-extension-symbolic
%manifest %{name}.manifest
%license COPYING
%{_libdir}/libglib*.so.*.extension-symbolic

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING

%{_bindir}/gdbus-codegen
%{_datadir}/bash-completion/completions/*
%_datadir/glib-2.0/codegen

%{_bindir}/glib-compile-resources
%{_bindir}/glib-genmarshal
%{_bindir}/glib-gettextize
%{_bindir}/glib-mkenums
%{_bindir}/gobject-query
%{_bindir}/gtester
%{_bindir}/gtester-report
%dir %{_datadir}/aclocal
%{_datadir}/aclocal/glib-2.0.m4
%{_datadir}/aclocal/glib-gettext.m4
%{_datadir}/aclocal/gsettings.m4
%dir %{_datadir}/glib-2.0/
%{_datadir}/glib-2.0/gdb/
%{_datadir}/glib-2.0/gettext/
%{_datadir}/glib-2.0/schemas/gschema.dtd
%{_datadir}/glib-2.0/dtds/gresource.dtd
%{_datadir}/glib-2.0/valgrind/glib.supp
%{_includedir}/glib-2.0
%{_includedir}/gio-unix-2.0
%{_libdir}/lib*.so
%dir %{_libdir}/glib-2.0/
%{_libdir}/glib-2.0/include/
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gdb/auto-load/%{_libdir}/*-gdb.py
%{_datadir}/gettext/its/gschema.*
%if 0%{?with_systemtap}
%{_datadir}/systemtap/tapset/*.stp
%endif
%{_sysconfdir}/rpm/macros.glib2
# Own these directories to not depend on gdb
%dir %{_datadir}/gdb
%dir %{_datadir}/gdb/auto-load
%dir %{_datadir}/gdb/auto-load%{_prefix}
%dir %{_datadir}/gdb/auto-load%{_libdir}

%files devel-static
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{_libdir}/lib*.a
%{?include_glib_kdbus_files}
%{_libdir}/lib*.a.extension-symbolic

%files tests
%manifest %{name}.manifest
%license COPYING LICENSE.MIT
%{relative_dbus_tests_base_dir}/test-suites/glib-tests/
%{relative_dbus_tests_base_dir}/runner/glib-tests

%changelog
