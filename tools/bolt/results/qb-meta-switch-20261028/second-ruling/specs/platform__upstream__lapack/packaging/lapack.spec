Name:           lapack
Summary:        Linear Algebra Package
Version:        3.7.1
Release:        1
License:        Public Domain, Freeware
Group:          Development/Libraries/Parallel
Source0:        %{name}-%{version}.tar.bz2
Url:            http://www.netlib.org/lapack/
Source1001:     1001-TIZEN-LAPACK-GCC13.patch

BuildRequires:  cmake
BuildRequires:  gcc-fortran
Requires:       blas  = %{version}

%define _toolchain_override gcc

%description
LAPACK provides routines for solving systems of simultaneous linear
equations, least-squares solutions of linear systems of equations,
eigenvalue problems, and singular value problems. The associated matrix
factorizations (LU, Cholesky, QR, SVD, Schur, generalized Schur) are
also provided, as are related computations such as reordering of the
Schur factorizations and estimating condition numbers. Dense and banded
matrices are handled, but not general sparse matrices. In all areas,
similar functionality is provided for real and complex matrices, in
both single and double precision.

%package devel
Summary:        LAPACK development libraries
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       blas-devel = %{version}-%{release}
 
%description devel
LAPACK development libraries (shared).

%package -n liblapacke3
Summary:        LAPACKE development files
Group:          Development/Libraries/C and C++

%description -n liblapacke3
This library provides a native C interface to LAPACK routines available
at www.netlib.org/lapack to facilitate usage of LAPACK functionality
for C programmers.

%package     -n lapacke-devel
Summary:        LAPACKE development files
Group:          Development/Libraries/C and C++
Requires:       liblapacke3 = %{version}
Provides:       lapacke = %{version}

%description -n lapacke-devel
LAPACKE headers and development files.

%package -n blas
License:        Public Domain, Freeware
Summary:        Basic Linear Algebra Subprograms
Group:          Productivity/Scientific/Math
Requires:       libblas3 >= %{version}

%description -n blas
BLAS (Basic Linear Algebra Subprograms) is a standard library for
numerical algebra. BLAS provides a number of basic algorithms for
linear algebra. BLAS is fast and well-tested, was written in FORTRAN 77
and built with gfortran. BLAS manual pages are available in the
blas-man package.

%package -n blas-devel
Summary:        BLAS development libraries
Group:          Development/Libraries
Requires:       blas = %{version}-%{release}

%description -n blas-devel
BLAS development libraries (shared).

%package -n cblas
License:        Public Domain, Freeware
Summary:        A standard C language APIs for BLAS
Group:          Productivity/Scientific/Math

%description -n cblas
This library provides a native C interface to BLAS routines available
to facilitate usage of BLAS functionality for C programmers.

%package -n cblas-devel
Summary:        BLAS development libraries
Group:          Development/Libraries
Requires:       cblas = %{version}-%{release}

%description -n cblas-devel
CBLAS development libraries (shared).

%package -n liblapack3
License:        Public Domain, Freeware
Summary:        LAPACK Shared Library
Group:          Development/Libraries/Parallel

%description -n liblapack3
LAPACK provides routines for solving systems of simultaneous linear
equations, least-squares solutions of linear systems of equations,
eigenvalue problems, and singular value problems. The associated matrix
factorizations (LU, Cholesky, QR, SVD, Schur, generalized Schur) are
also provided, as are related computations such as reordering of the
Schur factorizations and estimating condition numbers. Dense and banded
matrices are handled, but not general sparse matrices. In all areas,
similar functionality is provided for real and complex matrices, in
both single and double precision.

%package -n libblas3
License:        Public Domain, Freeware
Summary:        BLAS Shared Library
Group:          Productivity/Scientific/Math

%description -n libblas3
BLAS (Basic Linear Algebra Subprograms) is a standard library for
numerical algebra.  BLAS provides a number of basic algorithms for
linear algebra.

%prep
%setup -q

cp %{SOURCE1001} .
patch -p1 < %{SOURCE1001}

%build

mkdir -p build
cd build

%cmake .. -DLAPACKE_WITH_TMG=YES \
        -DCBLAS=ON \
        -DCMAKE_INSTALL_PREFIX=%{_prefix} \
        -DCMAKE_INSTALL_LIBDIR=%{_libdir}
make %{?_smp_mflags}

%install

cd build
%make_install

# Remove unnecessary files
rm -rf %{buildroot}%{_libdir}/cmake

%post -n libblas3 -p /sbin/ldconfig

%postun -n libblas3 -p /sbin/ldconfig

%post -n liblapack3 -p /sbin/ldconfig

%postun -n liblapack3 -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/liblapack.so.*
%{_libdir}/liblapacke.so.*

%files devel
%{_libdir}/liblapack.so
%{_libdir}/libtmglib.so

%files -n liblapack3
%defattr(-,root,root)
%{_libdir}/liblapack.so.%version
%{_libdir}/liblapack.so.3

%files -n liblapacke3
%defattr(-,root,root,-)
%{_libdir}/liblapacke.so.%{version}
%{_libdir}/liblapacke.so.3

%files -n lapacke-devel
%defattr(-,root,root,-)
%{_libdir}/liblapacke.so
%{_includedir}/lapacke*.h
%{_libdir}/pkgconfig/lapacke.pc
%{_libdir}/pkgconfig/lapack.pc

%files -n blas
%defattr(-,root,root)
%{_libdir}/libblas.so.*

%files -n blas-devel
%{_libdir}/libblas.so
%{_libdir}/pkgconfig/blas.pc

%files -n cblas
%defattr(-,root,root)
%{_libdir}/libcblas.so.*

%files -n cblas-devel
%{_includedir}/cblas*.h
%{_libdir}/libcblas.so
%{_libdir}/pkgconfig/cblas.pc

%files -n libblas3
%defattr(-,root,root)
%{_libdir}/libblas.so.%version
%{_libdir}/libblas.so.3

%changelog
