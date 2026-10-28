#
# spec file for package glibmm2
#
# Copyright (c) 2016 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/

Name:           glibmm
Version:        2.64.2
Release:        0
Summary:        C++ Interface for Glib
License:        LGPL-2.1+
Group:          System/Libraries
Url:            http://www.gtkmm.org/
Source0:        http://download.gnome.org/sources/glibmm/2.64/%{name}-%{version}.tar.xz
Source1001:     %{name}.manifest
BuildRequires:  fdupes
BuildRequires:  mm-common
BuildRequires:  perl-XML-Parser
BuildRequires:  libxslt-tools
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(sigc++-2.0)

%description
Glibmm is the official C++ interface for the popular cross-platform
library Glib. It provides non-UI API that is not available in standard
C++ and makes it possible for gtkmm to wrap GObject-based APIs.

%package -n libglibmm

Summary:        C++ Interface for Glib
Group:          System/Libraries

%description -n libglibmm
Glibmm is the official C++ interface for the popular cross-platform
library Glib. It provides non-UI API that is not available in standard
C++ and makes it possible for gtkmm to wrap GObject-based APIs.

%package -n libgiomm

Summary:        C++ Interface for Gio
Group:          System/Libraries

%description -n libgiomm
Glibmm is the official C++ interface for the popular cross-platform
library Glib. It provides non-UI API that is not available in standard
C++ and makes it possible for gtkmm to wrap GObject-based APIs.

%package devel
Summary:        C++ Interface for GLib
Group:          Development/Libraries/C and C++
Requires:       libgiomm = %{version}
Requires:       libglibmm = %{version}

%description devel
Glibmm is the official C++ interface for the popular cross-platform
library Glib. It provides non-UI API that is not available in standard
C++ and makes it possible for gtkmm to wrap GObject-based APIs.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

%build

./autogen.sh
chmod +x configure
# %configure --disable-static
%configure --enable-maintainer-mode --disable-static
make %{?jobs:-j%jobs}

%install
%makeinstall
rm %{buildroot}%{_libdir}/*.la
%fdupes %{buildroot}
%remove_docs

%clean
rm -rf %{buildroot}

%post -n libglibmm -p /sbin/ldconfig

%postun -n libglibmm -p /sbin/ldconfig

%post -n libgiomm -p /sbin/ldconfig

%postun -n libgiomm -p /sbin/ldconfig

%files -n libglibmm
%defattr (-, root, root)
%license COPYING
%{_libdir}/libglibmm-2.4.so.*
%{_libdir}/libglibmm_generate_extra_defs-2.4.so.*

%files -n libgiomm
%defattr (-, root, root)
%license COPYING
%{_libdir}/libgiomm-2.4.so.*

%files devel
%defattr (-, root, root)
%license COPYING
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_libdir}/glibmm-2.4
%{_libdir}/giomm-2.4

%changelog

