#
# spec file for package python3-appdirs
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


Name:           python3-appdirs
VCS:            platform/upstream/python3-appdirs#da916cda66177c5dad2fd69164f328c7f6b7b8ad
Version:        1.4.4
Release:        1.1
Summary:        A small Python module for determining platform-specific dirs
License:        MIT
Group:          Development/Languages/Python
Url:            http://github.com/ActiveState/appdirs
Source:         https://pypi.python.org/packages/source/a/appdirs/appdirs-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

BuildArch:      noarch

%description
``appdirs`` will
help you choose an appropriate:

- user data dir (``user_data_dir``)
- user cache dir (``user_cache_dir``)
- site data dir (``site_data_dir``)
- user log dir (``user_log_dir``)


%prep
%setup -q -n appdirs-%{version}

%build
cp %{SOURCE1001} .
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
chmod a+x %{buildroot}%{python3_sitelib}/appdirs.py

%pre
# previous versions of the package installed .egg-info as a directory,
# the new update now installs it as a file. Clean out the directory, should it exist.
if [ -d %{python3_sitelib}/appdirs-%{version}-py%{py_ver}.egg-info ]; then
  rm -rf %{python3_sitelib}/appdirssix-%{version}-py%{py_ver}.egg-info
fi

%files
%manifest %{name}.manifest
%license LICENSE.txt
%{python3_sitelib}/*

%changelog

