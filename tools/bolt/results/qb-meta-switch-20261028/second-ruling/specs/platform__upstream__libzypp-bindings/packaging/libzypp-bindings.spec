# 
# spec file for package libzypp-bindings
#
# Copyright (c) 2007 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
# 
Name:           libzypp-bindings
Version:        0.7.4
Release:        0
License:        GPL-2.0+
Summary:        Bindings for libzypp
Group:          Development/Sources
Source:         %{name}-%{version}.tar.gz
Source1001: 	libzypp-bindings.manifest
Source1002: 	Fix_Swig_Source.patch

BuildRequires:  cmake gcc-c++ python3-devel
BuildRequires:  swig

BuildRequires:  libzypp-devel

%description
This package provides bindings for libzypp, the library for package management.

%prep
%setup -q
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE1002}

%build
mkdir build
cd build
%cmake -DCMAKE_INSTALL_PREFIX=%{prefix} \
      -DPYTHON_SITEDIR=%{python3_sitearch} \
      -DLIB=%{_lib} \
      -DCMAKE_VERBOSE_MAKEFILE=TRUE \
      -DCMAKE_C_FLAGS_RELEASE:STRING="%{optflags}" \
      -DCMAKE_CXX_FLAGS_RELEASE:STRING="%{optflags}" \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_SKIP_RPATH=1 \
      ..
make -j1

%install
cd build
make install DESTDIR=$RPM_BUILD_ROOT

%clean

%package -n python3-zypp
Summary:        Python3 bindings for libzypp
Group:          Development/Languages/Python
Requires:  libzypp

%description -n python3-zypp
Python3 bindings of libzypp


%files -n python3-zypp
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{python3_sitearch}/_zypp.so
%{python3_sitearch}/zypp.py*
