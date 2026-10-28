#
# spec file for package gccmakedep
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

Name:           gccmakedep
Version:        1.0.2
Release:        0
License:        MIT
Summary:        Utility to list the resource database of an X application
Url:            http://xorg.freedesktop.org/
Group:          Development/Tools
Source0:        http://xorg.freedesktop.org/releases/individual/util/%{name}-%{version}.tar.bz2
BuildArch:      noarch

%description
The gccmakedep program calls 'gcc -M' to output makefile rules
describing the dependencies of each sourcefile, so that make knows
which object files must be recompiled when a dependency has changed.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
%make_install

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/gccmakedep
%{_mandir}/man1/gccmakedep.1x%{?ext_man}

%changelog
