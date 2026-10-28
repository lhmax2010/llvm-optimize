Name:           python-numpy
Version:        1.16.6
Release:        0
Summary:        NumPy array processing for numbers, strings, records and objects
License:        BSD-3-Clause
Group:          Development/Libraries/Python
Url:            http://www.numpy.org/
Source0:        %{name}-%{version}.tar.gz
Source1001:	    %{name}.manifest
BuildRequires:  blas-devel
BuildRequires:  gcc-fortran
BuildRequires:  lapack-devel
BuildRequires:  unzip
BuildRequires:  python-cython
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  openblas-devel


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
Group:          Development/Libraries/Python
Requires:       %{name} = %{version}
Requires:       blas-devel
BuildRequires:  gcc-fortran
Requires:       lapack-devel
Requires:       python-devel
Requires:       openblas-devel


%description devel
This package contains files for developing applications using numpy.


%prep
%setup -q
cp %{SOURCE1001} .


%build
export CFLAGS="%{optflags} -fno-strict-aliasing -Wno-incompatible-pointer-types"
export G_SLICE=always-malloc
/usr/bin/python2 setup.py build


%install
/usr/bin/python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

# Remove testsuite from packaging
rm -rf %{buildroot}%{python_sitearch}/numpy/{,core,distutils,f2py,fft,lib,linalg,ma,matrixlib,oldnumeric,polynomial,random,testing}/tests

mkdir -p %{buildroot}%{_includedir}
pushd %{buildroot}%{_includedir}
ln -sf %{python_sitearch}/numpy/core/include/numpy numpy
popd

%post


%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license LICENSE.txt
%doc *.txt
%{_bindir}/f2py
%{_bindir}/f2py2*
%{python_sitearch}/numpy/
%{python_sitearch}/numpy-%{version}-py*.egg-info
%exclude %{python_sitearch}/numpy/*/*/*.c
%exclude %{python_sitearch}/numpy/*/*.h
%exclude %{python_sitearch}/numpy/*/*/*.h
%exclude %{python_sitearch}/numpy/*/*/*/*.h
%exclude %{python_sitearch}/numpy/core/lib/libnpymath.a


%files devel
%defattr(-,root,root)
%license LICENSE.txt
%doc README.md THANKS.txt
%{python_sitearch}/numpy/*/*/*.c
%{python_sitearch}/numpy/*/*.h
%{python_sitearch}/numpy/*/*/*.h
%{python_sitearch}/numpy/*/*/*/*.h
%{python_sitearch}/numpy/core/lib/libnpymath.a
%{_includedir}/numpy

%changelog
