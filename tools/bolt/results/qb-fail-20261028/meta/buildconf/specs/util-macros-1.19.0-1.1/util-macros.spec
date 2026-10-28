Name:	 util-macros
VCS:   platform/upstream/util-macros#5eb8f5eba6ee91c9793badd0292c91e5f7d29b30
Summary: X.Org build utilities
Version: 1.19.0
Release: 1.1
License: MIT/X11
Group:   Development/System
URL:     http://www.x.org
Source: util-macros-%{version}.tar.bz2
Source1001: 	util-macros.manifest

%description
 This package provides build utilties tha ship with the X Window System, including:
  - util-macros, autotools macros for X.Org

%prep
%setup -q -n util-macros-%{version}
cp %{SOURCE1001} .

%build
%autogen
make

%install
%make_install

%remove_docs
rm -rf %{buildroot}/usr/share/util-macros/INSTALL

%files
%manifest %{name}.manifest
%license COPYING
%{_datadir}/aclocal/*
%{_datadir}/pkgconfig/*

%changelog
* Sat May 11 2013 Anas Nashif <anas.nashif@intel.com> submit/tizen/20130509.184708@c389d77
- Set license using %%license
