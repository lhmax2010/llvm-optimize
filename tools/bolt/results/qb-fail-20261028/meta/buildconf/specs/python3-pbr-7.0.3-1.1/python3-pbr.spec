Name:           python3-pbr
VCS:            platform/upstream/python3-pbr#0a1c154b12b5e0e73f42d9f48d1d21ff533ba95e
Version:        7.0.3
Release:        1.1
Summary:        Python Build Reasonableness
License:        Apache-2.0
Group:          Development/Languages/Python
Url:            http://pypi.python.org/pypi/pbr
Source:         %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3-setuptools

BuildArch:      noarch

%description
PBR is a library to automatically do a bunch of standard
things you want in your setup.py without you having to repeat
them every time. It will set versions, process requirements
files and generate AUTHORS and ChangeLog file all from git
information.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

# Get rid of ugly build-time deps that require network:
sed -i "s/, 'sphinx\.ext\.intersphinx'//" doc/source/conf.py

%build
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

# %check
# %{_bindir}/python3 %{_bindir}/testr init
# %{_bindir}/python3 %{_bindir}/testr run --parallel

%files
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/pbr
%{python3_sitelib}/pbr
%{python3_sitelib}/pbr-%{version}-py%{python3_version}.egg-info

