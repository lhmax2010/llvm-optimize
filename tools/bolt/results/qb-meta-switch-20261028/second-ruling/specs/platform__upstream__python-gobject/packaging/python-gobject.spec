%define local_py_requires %{py_requires}
%define local_py_sitedir  %{py_sitedir}
%define local_py_suffix   2
%define local_lib_ver     0

Name:           python-gobject
%define _name   pygobject
Summary:        Python bindings for GObject
License:        LGPL-2.1+
Group:          Development/Libraries
Version:        3.36.1
Release:        0
Url:            http://ftp.gnome.org/pub/GNOME/sources/pygobject/
Source:         http://download.gnome.org/sources/pygobject/3.8/%{_name}-%{version}.tar.xz
Source1001: 	python-gobject.manifest
BuildRequires:  fdupes
BuildRequires:  glib2-devel >= 2.48.0
BuildRequires:  gobject-introspection-devel >=  1.46.0
BuildRequires:  libffi-devel
BuildRequires:  python-cairo-devel
BuildRequires:  python-devel
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(cairo-gobject)
BuildRequires:  python
Provides:       pygobject3

%description
Pygobjects is an extension module for python that gives you access to
GLib's GObjects.

%package cairo
Summary:        Python bindings for GObject -- Cairo bindings
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description cairo
Pygobjects is an extension module for python that gives you access to
GLib's GObjects.

This package contains the Python Cairo bindings for GObject.

%package pygtkcompat
Summary:        Python bindings for GObject -- PyGTK Backwards Compatibility
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description pygtkcompat
Pygobjects is an extension module for python that gives you access to
GLib's GObjects.

This package contains a module providing backwards compatibility to
pygtk.

%package devel
Summary:        Python bindings for GObject
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description devel
This package contains files required to build wrappers for gobject
addon libraries such as pygtk.

%prep
%setup -q -n %{_name}-%{version}
cp %{SOURCE1001} .

%build
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build \
		--install-base=%{buildroot} \
        --install-lib=%{buildroot}%{python_sitearch} \
        --install-purelib=%{buildroot}%{_libdir} \
        --install-scripts=%{buildroot}%{_bindir} \
        --install-headers=%{buildroot}%{_includedir} \
        --install-data=%{buildroot}%{_usr}
%py_compile %{buildroot}/%{python_sitearch}
%py_compile -O %{buildroot}/%{python_sitearch}
%fdupes %{buildroot}/%{python_sitearch}

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{local_py_sitedir}/gi/
%{local_py_sitedir}/PyGObject-*.egg-info
# Lives in cairo subpackage
%exclude %{local_py_sitedir}/gi/_gi_cairo.so
# Lives in pygtkcompat subpackage
%exclude %{local_py_sitedir}/gi/pygtkcompat.py

%files cairo
%manifest %{name}.manifest
%defattr(-,root,root)
%{local_py_sitedir}/gi/_gi_cairo.so

%files pygtkcompat
%manifest %{name}.manifest
%defattr(-,root,root)
#%{local_py_sitedir}/gi/pygtkcompat.py
%{local_py_sitedir}/pygtkcompat

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_includedir}/pygobject-3.0/
%{_libdir}/pkgconfig/pygobject-3.0.pc
