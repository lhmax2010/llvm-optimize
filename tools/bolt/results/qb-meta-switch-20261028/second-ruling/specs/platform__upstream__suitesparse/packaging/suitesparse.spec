Name:       suitesparse
Summary:    A collection of sparse matrix libraries
Version:    5.2.0
Release:    0

# ==========================================================
License:    BSD-3-Clause AND GPL-2.0+ AND LGPL-2.1+
# ==========================================================

Group:      Development/Libraries/C and C++
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
Source1002: LICENSE.GPL-2.0
Source1003: LICENSE.LGPL-2.1
Source1004: LICENSE.Apache-2.0
Source1005: libmetis.manifest
Source1006: CXSparse.manifest

# ==========================================================
# BuildRequires
# specifies build-time dependencies for the package
# ==========================================================
BuildRequires:  cmake
BuildRequires:  lapack-devel
BuildRequires:  openblas-devel
%{?_toolchain:
%if %{toolchain_is clang}
BuildRequires:  libomp
%endif
}

Requires:   lapack
Requires:   SuiteSparse_config = %{version}

%description
A suite of sparse matrix algorithms

%package devel
Summary:    A collection of sparse matrix libraries
Requires:   %{name} = %{version}
Requires:   libmetis = 5.1.0
Requires:   CXSparse-devel = %{version}
Requires:   SuiteSparse_config-devel = %{version}

%description devel
%{name}-devel version %{version}

%package -n SuiteSparse_config
Summary:    SuiteSparse config library
License:    PD

%description -n SuiteSparse_config
SuiteSparse config library

%package -n SuiteSparse_config-devel
Summary:    SuiteSparse config library
License:    PD
Requires:   SuiteSparse_config = %{version}

%description -n SuiteSparse_config-devel
SuiteSparse config library


%package -n CXSparse
Summary:    CXSparse is a version of CSparse that operates on both real and complex matrices
License:    LGPL-2.1+
Requires:   SuiteSparse_config = %{version}

%description -n CXSparse
CXSparse is a version of CSparse that operates on both real and complex
matrices, using either int or SuiteSparse_long integers.  A SuiteSparse_long is
normally just a long on most platforms, but becomes __int64 on WIN64.  It now
includes a MATLAB interface, enabling the use of CXSparse functions on both
32-bit and 64-bit platforms

%package -n CXSparse-devel
Summary:    CXSparse is a version of CSparse that operates on both real and complex matrices
License:    LGPL-2.1+
Requires:   CXSparse = %{version}
Requires:   SuiteSparse_config-devel = %{version}

%description -n CXSparse-devel
CXSparse is a version of CSparse that operates on both real and complex matrices

%package -n libmetis
Summary:    Serial Graph Partitioning and Fill-reducing Matrix Ordering
Version:    5.1.0
Release:    0
License:    Apache-2.0

%description -n libmetis
METIS is a family of programs for partitioning unstructured graphs and hypergraph
and computing fill-reducing orderings of sparse matrices. The underlying algorithms
used by METIS are based on the state-of-the-art multilevel paradigm that has been
shown to produce high quality results and scale to very large problems.

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .
cp %{SOURCE1003} .
cp %{SOURCE1004} .
cp %{SOURCE1005} .
cp %{SOURCE1006} .

# ==========================================================
# build section
# how to actually build the software we are packaging
# ==========================================================
%build
%{make_build} library BLAS=-lblas

# ==========================================================
# install section
# how to actually build the software we are packaging
# ==========================================================
%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_datadir}/doc

INSTALL_LIB=%{buildroot}%{_libdir} \
INSTALL_INCLUDE=%{buildroot}%{_includedir} \
INSTALL_DOC=%{buildroot}%{_datadir}/doc \
RUNPATH=%{_libdir} \
%{__make} install

rm -f %{buildroot}%{_includedir}/metis.h

%remove_docs

%clean

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n SuiteSparse_config -p /sbin/ldconfig
%postun -n SuiteSparse_config -p /sbin/ldconfig

%post -n libmetis -p /sbin/ldconfig
%postun -n libmetis -p /sbin/ldconfig

%post -n CXSparse -p /sbin/ldconfig
%postun -n CXSparse -p /sbin/ldconfig
# ==========================================================
# files section
# The list of files that will be installed in the end
# user’s system.
# ==========================================================
%files
%license LICENSE.txt LICENSE.GPL-2.0 LICENSE.LGPL-2.1
%manifest %{name}.manifest
%exclude %{_libdir}/libsuitesparseconfig.so.*
%exclude %{_libdir}/libcxsparse.so.*
%{_libdir}/*.so.*

%files devel
%license LICENSE.txt LICENSE.GPL-2.0 LICENSE.LGPL-2.1
%manifest %{name}.manifest
%{_includedir}/*.h
%exclude %{_includedir}/cs.h
%exclude %{_includedir}/SuiteSparse_config.h
%{_includedir}/*.hpp
%exclude %{_libdir}/libmetis.so
%exclude %{_libdir}/libcxsparse.so
%exclude %{_libdir}/libsuitesparseconfig.so
%{_libdir}/*.so

%files -n SuiteSparse_config
# Public Domain License
%manifest %{name}.manifest
%{_libdir}/libsuitesparseconfig.so.*

%files -n SuiteSparse_config-devel
# Public Domain License
%manifest %{name}.manifest
%{_includedir}/SuiteSparse_config.h
%{_libdir}/libsuitesparseconfig.so

%files -n CXSparse
%license LICENSE.LGPL-2.1
%manifest CXSparse.manifest
%{_libdir}/libcxsparse.so.*

%files -n CXSparse-devel
%license LICENSE.LGPL-2.1
%manifest CXSparse.manifest
%{_includedir}/cs.h
%{_libdir}/libcxsparse.so

%files -n libmetis
%license LICENSE.Apache-2.0
%manifest libmetis.manifest
%{_libdir}/libmetis.so

