#
# spec file for package python-argparse
#
# Copyright (c) 2015 SUSE LINUX GmbH, Nuernberg, Germany.
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

Name:           python-argparse
VCS:            platform/upstream/python-argparse#10cbbb2ac817fdc39b198e455d015a1c6ff72728
Version:        1.4.0
Release:        1.1
Url:            http://code.google.com/p/argparse/
Summary:        Python command-line parsing library
License:        Python-2.0
Group:          Development/Languages/Python
Source:         https://pypi.python.org/packages/source/a/argparse/argparse-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  python-devel
BuildRequires:  python-setuptools

BuildArch:      noarch

# For some distros, the "python" package provides python-argparse.
# This allows packages to explicitly define that it needs this
# backported version rather than the included version.
Provides:       python-argparse-backport = %{version}
Obsoletes:      python-argparse-backport < %{version}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%description
The argparse module provides an easy, declarative interface for
creating command line tools, which knows how to:

* parse the arguments and flags from sys.argv
* convert arg strings into objects for your program
* format and print informative help messages
* and much more... 

The argparse module improves on the standard library optparse module
in a number of ways including:

* handling positional arguments
* supporting sub-commands
* allowing alternative option prefixes like + and /
* handling zero-or-more and one-or-more style arguments
* producing more informative usage messages
* providing a much simpler interface for custom types and actions 

%prep
%setup -n argparse-%{version}
mkdir html
(cd doc &&
    mv * ../html/
    mv ../html .
 )
sed -i "s/\r//" NEWS.txt # Avoid warning wrong-file-end-of-line-encoding

%build
cp %{SOURCE1001} .
%{__python} setup.py build

%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}

%remove_docs

%files 
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license doc/html/source/Python-License.txt
%python_sitelib/*

%changelog
