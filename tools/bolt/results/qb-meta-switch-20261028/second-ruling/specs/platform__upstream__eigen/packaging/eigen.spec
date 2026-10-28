#
# spec file for package eigen
#
# Copyright (c) 2018 SUSE LINUX Products GmbH, Nuernberg, Germany.
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


Name:           eigen
Version:        3.4.0
Release:        0
Summary:        Template library for linear algebra
License:        MPL-2.0 and LGPLv2+ and BSD-3-Clause and Minpack
Group:          Development/Libraries/C and C++
URL:            http://eigen.tuxfamily.org/
Source:         http://bitbucket.org/eigen/eigen/get/%{version}.tar.bz2

BuildRequires:  blas-devel
BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gmp-devel
BuildRequires:  pkg-config

# BuildRequires:  graphviz
# BuildRequires:  libqt4-devel
# BuildRequires:  pkgconfig(adolc)
# BuildRequires:  pkgconfig(fftw3)
# BuildRequires:  superlu-devel
# BuildRequires:  texlive-dvips
# BuildRequires:  texlive-latex

BuildArch:      noarch


%description
Eigen is a C++ template library for linear algebra: matrices, vectors, numerical
 solvers, and related algorithms.

%package devel
Summary:        Template library for linear algebra
Group:          Development/Libraries/C and C++

%description devel
Eigen is a C++ template library for linear algebra: matrices, vectors, numerical
 solvers, and related algorithms.

%package devel-doc
Summary:        Documentation for Eigen library
Group:          Development/Libraries/C and C++

%description devel-doc 
Documentation for Eigen, the C++ template library for linear algebra: matrices,
vectors, numerical solvers, and related algorithms.

%prep
%setup -q -n %{name}-%{name}-b3f3d4950030

# remove buildtime from documentation
sed -i 's|^HTML_TIMESTAMP         = YES|HTML_TIMESTAMP         = NO|' doc/Doxyfile.in

%build
mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=%{_prefix}
%{__make} %{?_smp_mflags}
cd -


%install
cd build
%{__make} install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"
cd -

%files devel
%license COPYING.*
%{_includedir}/eigen3/*
%{_datadir}/eigen3/cmake/*.cmake
%{_datadir}/pkgconfig/eigen3.pc

