%define baseline 2.16
Name:           atk
Version:        2.36.0
Release:        0
License:        LGPL-2.0+
Summary:        An Accessibility ToolKit
Url:            http://www.gtk.org/
Group:          System/Libraries
Source:         http://download.gnome.org/sources/%{name}/%{baseline}/%{name}-%{version}.tar.xz
Source98:       baselibs.conf
Source1001:     %{name}.manifest

BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  meson >= 0.46.0
BuildRequires:  glib2-devel >= 2.35.2
BuildRequires:  intltool
BuildRequires:  which
BuildRequires:  gobject-introspection
BuildRequires:  gobject-introspection-devel
%if %{with introspection}
BuildRequires:  gobject-introspection-devel
%endif
Requires:       libatk

%description
The ATK library provides a set of accessibility interfaces. By
supporting the ATK interfaces, an application or toolkit can be used
with screen readers, magnifiers, and alternate input devices.

%package -n libatk
Summary:        An Accessibility ToolKit
Group:          System/Libraries
Provides:       %{name} = %{version}
Obsoletes:      %{name} < %{version}

%description -n libatk
The ATK library provides a set of accessibility interfaces. By
supporting the ATK interfaces, an application or toolkit can be used
with screen readers, magnifiers, and alternate input devices.

%package -n typelib-Atk
Summary:        An Accessibility ToolKit -- Introspection bindings
Group:          System/Libraries

%description -n typelib-Atk
The ATK library provides a set of accessibility interfaces. By
supporting the ATK interfaces, an application or toolkit can be used
with screen readers, magnifiers, and alternate input devices.

This package provides the GObject Introspection bindings for ATK.

%package devel
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Libraries/GNOME
Requires:       libatk = %{version}

%description devel
This package contains all necessary include files and libraries needed
to develop applications that require these.

%prep
%setup -q
cp %{SOURCE1001} .

%build
meson --prefix /usr --libdir %{_libdir} build
ninja -C build all

%install

export DESTDIR=%{buildroot}
ninja -C build install

%fdupes %{buildroot}

%post -n libatk -p /sbin/ldconfig

%postun -n libatk -p /sbin/ldconfig

%files -n libatk
%manifest %{name}.manifest
%defattr(-, root, root)
%doc COPYING
%license COPYING
%{_libdir}/libatk*.so.*
%{_datadir}/locale/
%{_libdir}/girepository*/Atk*.typelib
%{_datadir}/gir*/Atk*.gir

%files devel
%manifest %{name}.manifest
%defattr(-, root, root)
%{_includedir}/atk-1.0
%{_libdir}/libatk*.so
%{_libdir}/pkgconfig/*.pc

