Name:           python3-gobject
Summary:        Python3 bindings for GObject
License:        LGPL-2.1+
Group:          Development/Libraries
Version:        3.46.0
Release:        0
Url:            http://ftp.gnome.org/pub/GNOME/sources/pygobject/
Source:         %{name}-%{version}.tar.xz
Source1001: 	python3-gobject.manifest

BuildRequires:  glib2-devel >= 2.48.0
BuildRequires:  gobject-introspection-devel >= 1.46.0
BuildRequires:  libffi-devel
BuildRequires:  pkgconfig(python3)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(cairo-gobject)
BuildRequires:  python3-cairo-devel
BuildRequires:  python3-setuptools
Provides:       pygobject3

%description
Pygobjects is an extension module for python3 that gives you access to
GLib's GObjects.

%package cairo
Summary:        Python3 bindings for GObject -- Cairo bindings
Group:          Development/Libraries
Requires:       %{name} = %{version}
%define cairo_real_package %(rpm -q --qf '%%{NAME}' --whatprovides cairo)
Supplements:    packageand(%{name}:%{cairo_real_package})

%description cairo
Pygobjects is an extension module for python3 that gives you access to
GLib's GObjects.

This package contains the Python3 Cairo bindings for GObject.

%package pygtkcompat
Summary:        Python3 bindings for GObject -- PyGTK Backwards Compatibility
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description pygtkcompat
Pygobjects is an extension module for python3 that gives you access to
GLib's GObjects.

This package contains a module providing backwards compatibility to
pygtk.

%package devel
Summary:        Python3 bindings for GObject
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description devel
This package contains files required to build wrappers for gobject
addon libraries such as pygtk.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

%build
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --skip-build --root %{buildroot}

%files
%manifest %{name}.manifest
%license COPYING
%{python3_sitearch}/gi/
%{python3_sitearch}/PyGObject-*.egg-info
%exclude %{python3_sitearch}/gi/_gi_cairo*.so
%exclude %{python3_sitearch}/gi/pygtkcompat.py

%files cairo
%manifest %{name}.manifest
%{python3_sitearch}/gi/_gi_cairo*.so

%files pygtkcompat
%manifest %{name}.manifest
%{python3_sitearch}/pygtkcompat

%files devel
%manifest %{name}.manifest
%{_includedir}/pygobject-3.0/
%{_libdir}/pkgconfig/pygobject-3.0.pc
