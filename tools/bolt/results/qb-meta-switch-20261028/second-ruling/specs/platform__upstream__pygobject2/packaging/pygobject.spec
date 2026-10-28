Name:           pygobject2
Version:        3.55.0
Release:        1
Summary:        Python bindings for GObject
License:        LGPL-2.1-or-later
URL:            http://www.pygtk.org/
Source0:        %{name}-%{version}.tar.gz
Source1001:     pygobject.manifest

# SPDX License Compliance: Using current non-deprecated identifiers
# License: LGPL-2.1-or-later is already in current SPDX format
# Tizen Policy: LGPL-2.1-or-later is compatible with Tizen

BuildRequires:  meson
BuildRequires:  python3-devel
BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  libffi-devel
BuildRequires:  python3-cairo-devel
BuildRequires:  pkgconfig

Requires:       python3
Requires:       glib2
Requires:       gobject-introspection

%description
The %{name} package provides a convenient wrapper for the GObject library
for use in Python programs. This is version 3.55.0, an upgrade from the
Tizen base version 3.46.0.

%package devel
Summary:        Development files for building add-on libraries
Requires:       %{name} = %{version}-%{release}
Requires:       glib2-devel
Requires:       pkgconfig

%description devel
This package contains files required to build wrappers for %{name}-based
libraries such as pygtk2.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

%build
# Meson build with Tizen-compatible options
%meson \
    -Dpycairo=enabled \
    -Dtests=false \
    -Dwheel=false

%meson_build

%install
%meson_install

# Remove documentation and man pages (Tizen policy)
%remove_docs

%files
%manifest pygobject.manifest
%license COPYING
%{python3_sitearch}/gi/*
%{python3_sitearch}/PyGObject-%{version}.dev0.dist-info

%files devel
%manifest pygobject.manifest
%{_libdir}/pkgconfig/pygobject-3.0.pc
%{_includedir}/pygobject-3.0/pygobject.h
%{_includedir}/pygobject-3.0/pygobject-types.h
