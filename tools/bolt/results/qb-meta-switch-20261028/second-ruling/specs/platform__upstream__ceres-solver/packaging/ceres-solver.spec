Name:           ceres-solver
Version:        2.2.0
Release:        1
Summary:        C++ library for modeling and solving optimization problems
License:        BSD-3-Clause
URL:            https://ceres-solver.org/
Group:          Development/Libraries/C and C++

Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.manifest
Source2:        COPYING.LGPL-2.1
Source3:        0001-Fix-to-make-dependency-to-glog-instead-of-making-it-.patch

# ==========================================================
# BuildRequires
# specifies build-time dependencies for the package
# ==========================================================
BuildRequires:  cmake
BuildRequires:  eigen-devel
BuildRequires:  pkgconfig(libglog)
BuildRequires:  CXSparse-devel

%description
Ceres Solver is a C++ library for modeling and solving large,
complicated optimization problems. It can be used to solve Non-linear Least
Squares problems with bounds constraints and general unconstrained optimization
problems.


%package -n libceres
Summary:	Ceres Solver shared library
Group:      System/Libraries
License:	LGPL-2.1

%description -n libceres
Ceres Solver is a C++ library for modeling and solving large,
complicated optimization problems. It can be used to solve Non-linear Least
Squares problems with bounds constraints and general unconstrained optimization
problems.

%package -n libceres-devel
Summary:	Ceres Solver header files
Group:		Development/Libraries/C and C++
Requires:	libceres = %{version}

%description -n libceres-devel
Ceres Solver is a C++ library for modeling and solving large,
complicated optimization problems. It can be used to solve Non-linear Least
Squares problems with bounds constraints and general unconstrained optimization
problems.


%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1} .
cp %{SOURCE2} .
%{__patch} -p1 < %{SOURCE3}


%build
mkdir -p build
cd build
%cmake .. \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DBUILD_SHARED_LIBS=ON \
    -DBUILD_TESTING=OFF \
    -DBUILD_EXAMPLES=OFF \
    -DBUILD_BENCHMARKS=OFF \
    -DBUILD_DOCUMENTATION=OFF \
    -DCXSPARSE=ON \
    -DSUITESPARSE=OFF \
    -DEIGENSPARSE=ON \
    -DGFLAGS=OFF \
    -DMINIGLOG=OFF \
    -DLAPACK=OFF \
    -DUSE_CUDA=OFF

%{__make}


%install
cd build
%{make_install}

# Remove static libraries and .la files
find %{buildroot} -name "*.a" -delete
find %{buildroot} -name "*.la" -delete

# Remove documentation and man pages (Tizen recommendation)
%remove_docs

%post -n libceres -p /sbin/ldconfig

%postun -n libceres -p /sbin/ldconfig

# ==========================================================
# files section
# The list of files that will be installed in the end
# user’s system.
# ==========================================================

%files -n libceres
%manifest %{name}.manifest
%license COPYING.LGPL-2.1
%{_libdir}/*.so.*

%files -n libceres-devel
%manifest %{name}.manifest
%license LICENSE
%{_includedir}/ceres/*.h
%{_includedir}/ceres/internal/*.h
%{_libdir}/cmake/Ceres/*.cmake
%{_libdir}/*.so

%changelog
