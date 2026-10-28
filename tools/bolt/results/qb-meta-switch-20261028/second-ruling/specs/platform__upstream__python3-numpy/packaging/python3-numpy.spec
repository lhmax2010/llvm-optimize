Name:           python3-numpy
Version:        2.4.1
Release:        0
Summary:        NumPy array processing for numbers, strings, records and objects
License:        BSD-3-Clause
Group:          Development/Libraries/Python3
Url:            http://www.numpy.org/
Source0:        %{name}-%{version}.tar.gz
Source1001:	    %{name}.manifest

BuildRequires:  blas-devel
BuildRequires:  gcc-fortran
BuildRequires:  lapack-devel
BuildRequires:  unzip
BuildRequires:  openblas-devel
BuildRequires:  meson
BuildRequires:  ninja
BuildRequires:  cmake
BuildRequires:  patchelf

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3
BuildRequires:  python3-build
BuildRequires:  python3-flit_core
BuildRequires:  python3-pip
BuildRequires:  python3-cython
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-meson-python
BuildRequires:  python3-pyproject-metadata
BuildRequires:  python3-cython

BuildRequires:  python3-hatchling
BuildRequires:  python3-pathspec
BuildRequires:  python3-pluggy

%{?_toolchain:
%if %{toolchain_is clang}
BuildRequires:	compiler-rt
%endif
}

%description
NumPy is a general-purpose array-processing package designed to
efficiently manipulate large multi-dimensional arrays of arbitrary
records without sacrificing too much speed for small multi-dimensional
arrays.  NumPy is built on the Numeric code base and adds features
introduced by numarray as well as an extended C-API and the ability to
create arrays of arbitrary type which also makes NumPy suitable for
interfacing with general-purpose data-base applications.

There are also basic facilities for discrete fourier transform,
basic linear algebra and random number generation.

%package devel
Summary:        Development files for numpy applications
Group:          Development/Libraries/Python3
Requires:       %{name} = %{version}
Requires:       blas-devel
BuildRequires:  gcc-fortran
Requires:       lapack-devel
Requires:       python3-devel
Requires:       openblas-devel

%description devel
This package contains files for developing applications using numpy.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="%{optflags} -fno-strict-aliasing"
%{_bindir}/python3 -m build -n --wheel

%install
# https://github.com/numpy/numpy/issues/16005
# if the CFLAGS is not set the same as the build section, the build will be performed again during installation.
export CFLAGS="%{optflags} -fno-strict-aliasing"
%{_bindir}/python3 -m pip install --root %{buildroot} ./dist/numpy-%{version}*.whl

%remove_docs

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE.txt
%{_bindir}/*
%{python3_sitearch}/numpy/*
%{python3_sitearch}/numpy-%{version}.dist-info/*

%exclude %{python3_sitearch}/numpy/f2py/tests/src/array_from_pyobj/*.c
%exclude %{python3_sitearch}/numpy/_core/tests/examples/limited_api/*.c
%exclude %{python3_sitearch}/numpy/_core/include/numpy/*.c
%exclude %{python3_sitearch}/numpy/f2py/src/*.h
%exclude %{python3_sitearch}/numpy/_core/include/numpy/*.h

%files devel
%license LICENSE.txt
%{python3_sitearch}/numpy/f2py/tests/src/array_from_pyobj/*.c
%{python3_sitearch}/numpy/_core/tests/examples/limited_api/*.c
%{python3_sitearch}/numpy/_core/include/numpy/*.c
%{python3_sitearch}/numpy/f2py/src/*.h
%{python3_sitearch}/numpy/_core/include/numpy/*.h

%{python3_sitearch}/numpy/_core/lib/libnpymath.a
%{python3_sitearch}/numpy/random/lib/libnpyrandom.a


%changelog
