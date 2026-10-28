#
# spec file for package python-Mako
#
# Copyright (c) 2014 SUSE LINUX Products GmbH, Nuernberg, Germany.
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

%if "%{run_tests}" == "1" 
    %define __spec_check_pre %___build_pre
    %define check %%check
%endif


%define debug_package %{nil}

Name:           python-mako
VCS:            platform/upstream/python-mako#55113441742681516d3720e38c8cfe7934ca4370
Version:        1.0.6
Release:        1.1
Url:            http://www.makotemplates.org/
Summary:        A super-fast Python templating language
License:        MIT
Group:          Development/Languages/Python
Source:         http://pypi.python.org/packages/source/M/Mako/Mako-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  python-MarkupSafe
BuildRequires:  python-devel
BuildRequires:  python-mock
BuildRequires:  python-setuptools
BuildRequires:  python-nose

Suggests:       python-Beaker >= 1.1
Requires:       python-MarkupSafe

Provides:       python-mako = %{version}
Obsoletes:      python-mako < %{version}

%description
Mako is a template library written in Python. It provides a familiar, non-XML
syntax which compiles into Python modules for maximum performance. Mako's
syntax and API borrows from the best ideas of many others, including Django
templates, Cheetah, Myghty, and Genshi. Conceptually, Mako is an embedded
Python (i.e. Python Server Page) language, which refines the familiar ideas
of componentized layout and inheritance to produce one of the most
straightforward and flexible models available, while also maintaining close
ties to Python calling and scoping semantics.

%prep
%setup -q -n Mako-%{version}

%build
cp %{SOURCE1001} .
%{__python} setup.py build

%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
%{__python} setup.py test || exit 0

%remove_docs

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE
%{_bindir}/mako-render
%{python_sitelib}/mako/
%{python_sitelib}/Mako-%{version}-py%{py_ver}.egg-info

%changelog

