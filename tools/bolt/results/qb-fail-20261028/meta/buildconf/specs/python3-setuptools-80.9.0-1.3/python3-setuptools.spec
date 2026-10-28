Name:           python3-setuptools
VCS:            platform/upstream/python3-setuptools#99978c0f981cda97ea9f423d897e2190717912dc
Version:        80.9.0
Release:        1.3
Summary:        Easily download, build, install, upgrade, and uninstall Python packages
License:        MIT
Group:          Development/Languages/Python
Url:            https://github.com/pypa/setuptools
Source:         %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-xml
BuildRequires:  unzip

Requires:       python3
Requires:       python3-xml

Provides:       python3-distribute = %{version}
Obsoletes:      python3-distribute < %{version}

BuildArch:      noarch

%description
setuptools is a collection of enhancements to the Python distutils that
allow you to more easily build and distribute Python packages,
especially ones that have dependencies on other packages.


%prep
%setup -q -n %{name}-%{version}
find . -type f -name "*.orig" -delete
cp %{SOURCE1001} .

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
%{_bindir}/python3 setup.py build

%install
mkdir -p build/scripts-%{python3_version}
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%manifest %{name}.manifest
%license LICENSE
%{python3_sitelib}/setuptools
%{python3_sitelib}/setuptools-%{version}*-py%{python3_version}.egg-info
%{python3_sitelib}/pkg_resources
%{python3_sitelib}/distutils-precedence.pth
%{python3_sitelib}/_distutils_hack/*.py
%{python3_sitelib}/_distutils_hack/__pycache__/*.pyc

%changelog

