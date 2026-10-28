Name:           python3-pathspec
VCS:            platform/upstream/python3-pathspec#accc4887d91c3542f465236820c0921ae77f7c07
Version:        1.0.1
Release:        1.3
Summary:        Utility library for gitignore style pattern matching of file paths
License:        MPL-2.0
URL:            https://github.com/cpburnz/python-path-specification
Source0:        pathspec-%{version}.tar.gz
Source1:        %{name}.manifest
Source2:        pathspec-%{version}-py3-none-any.whl

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3
BuildRequires:  python3-pip

BuildArch:      noarch

%description
Pathspec is a utility library for pattern matching of file paths. So
far this only includes Git's wildmatch pattern matching which itself is
derived from Rsync's wildmatch. Git uses wildmatch for its `gitignore`_
files.

%prep
%setup -q -n pathspec-%{version}
cp %{SOURCE1} .

%build
#%%{_bindir}/python3 -m build -n

%install
%{_bindir}/python3 -m pip install --root %{buildroot} %{SOURCE2}

%files 
%manifest %{name}.manifest
%license LICENSE
%{python3_sitelib}/pathspec/*
%{python3_sitelib}/pathspec-%{version}.dist-info/*
