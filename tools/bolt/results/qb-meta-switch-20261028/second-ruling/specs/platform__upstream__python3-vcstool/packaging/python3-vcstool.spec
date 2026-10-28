Name:           python3-vcstool
Version:        0.3.0
Release:        1
Summary:        invoke vcs commands on multiple repositories 
License:        Apache-2.0
Group:          Development/Languages/Python
Source:         vcstool-%{version}.tar.gz
Source1001:     %{name}.manifest
Source1002:     LICENSE

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-setuptools

BuildArch:      noarch

%description
invoke vcs commands on multiple repositories 

%prep
%setup -q -n vcstool-%{version}

%build
cp %{SOURCE1001} .
cp %{SOURCE1002} .
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%license LICENSE
%manifest %{name}.manifest
%{_bindir}/vcs
%{_bindir}/vcs-branch
%{_bindir}/vcs-bzr
%{_bindir}/vcs-custom
%{_bindir}/vcs-diff
%{_bindir}/vcs-export
%{_bindir}/vcs-git
%{_bindir}/vcs-help
%{_bindir}/vcs-hg
%{_bindir}/vcs-import
%{_bindir}/vcs-log
%{_bindir}/vcs-pull
%{_bindir}/vcs-push
%{_bindir}/vcs-remotes
%{_bindir}/vcs-status
%{_bindir}/vcs-svn
%{_bindir}/vcs-validate
%{python3_sitelib}/vcstool-%{version}-py%{python3_version}.egg-info/*
%{python3_sitelib}/vcstool/*.py
%{python3_sitelib}/vcstool/__pycache__/*.cpython-*.pyc
%{python3_sitelib}/vcstool/clients/*.py
%{python3_sitelib}/vcstool/clients/__pycache__/*.cpython-*.pyc
%{python3_sitelib}/vcstool/commands/*.py
%{python3_sitelib}/vcstool/commands/__pycache__/*.cpython-*.pyc
%{_datadir}/vcstool-completion/vcs.bash
%{_datadir}/vcstool-completion/vcs.tcsh
%{_datadir}/vcstool-completion/vcs.zsh
%{_datadir}/vcstool-completion/vcs.fish
