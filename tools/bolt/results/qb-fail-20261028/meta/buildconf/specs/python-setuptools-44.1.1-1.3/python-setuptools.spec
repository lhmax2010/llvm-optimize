#
# spec file for package python-setuptools
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
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

Name:           python-setuptools
VCS:            platform/upstream/python-setuptools#f500c8f6d8737e02c52f6eead629a2fb1257a4d6
Version:        44.1.1
Release:        1.3
Summary:        Easily download, build, install, upgrade, and uninstall Python packages
License:        MIT
Group:          Development/Languages/Python
Source:         https://pypi.io/packages/source/s/setuptools/setuptools-%{version}.zip
Source1001:     %{name}.manifest

BuildRequires:  python-devel
BuildRequires:  python-appdirs
BuildRequires:  python-packaging
BuildRequires:  python-six
BuildRequires:  python-xml
BuildRequires:  unzip

# needed for SLE
Requires:       python
Requires:       python-appdirs
Requires:       python-packaging
Requires:       python-six
Requires:       python-xml

Provides:       python-distribute = %{version}
Obsoletes:      python-distribute < %{version}

BuildArch:      noarch

%description
setuptools is a collection of enhancements to the Python distutils that
allow you to more easily build and distribute Python packages,
especially ones that have dependencies on other packages.


%prep
%setup -q -n setuptools-%{version}
find . -type f -name "*.orig" -delete

# fix rpmlint spurious-executable-perm
chmod -x README.rst

# strip shebangs to fix rpmlint warnings
# "explain the sed":
# 1 = first line only
# s@...@...@ = same as s/.../.../ except with @ instead of /
# ^ = start; #!/ = shebang leading characters; .* = rest of line; $ = end
# replace with nothing
sed -r -i '1s@^#!/.*$@@' setuptools/command/easy_install.py

%build
cp %{SOURCE1001} .
%{__python} bootstrap.py
%{__python} setup.py build

%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE
%{_bindir}/easy_install*
%{python_sitelib}/setuptools
%{python_sitelib}/setuptools-%{version}*-py%{python_version}.egg-info
%{python_sitelib}/easy_install.py*
%{python_sitelib}/pkg_resources

%changelog

