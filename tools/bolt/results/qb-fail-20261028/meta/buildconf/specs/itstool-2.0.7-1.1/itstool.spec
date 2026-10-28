#
# spec file for package itstool
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
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
#


Name:           itstool
VCS:            platform/upstream/itstool#51dae7d37ae60e428ac6a55c2770d37641bdac24
Version:        2.0.7
Release:        1.1
Summary:        Tool to translate XML documents using PO files
License:        GPL-3.0+
Group:          Development/Tools/Other
Url:            http://itstool.org
Source:         %{name}-%{version}.tar.bz2
Source1000:     itstool.manifest
BuildRequires:  python
BuildRequires:  python-libxml2
Requires:       python-libxml2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
ITS Tool extracts messages from XML files and outputs PO template files, then
merges translations from MO files to create translated XML files. It determines
what to translate and how to chunk it into messages using the W3C
Internationalization Tag Set (ITS).

%prep
%setup -q
cp %{SOURCE1000} .

%build
%configure
make %{?_smp_mflags}

%install
%make_install
%remove_docs

%files
%license COPYING COPYING.GPL3
%{_bindir}/%{name}
%{_datadir}/%{name}/

