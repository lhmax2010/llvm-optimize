Name:           libsolv
Version:        0.7.35
Release:        0
Url:            https://github.com/openSUSE/libsolv
License:        BSD-3-Clause
Source:         libsolv-%{version}.tar.bz2
Source10: 	    add_pie_compile_option.patch
Source1001: 	libsolv.manifest
Summary:        A new approach to package dependency solving
Group:          System/Package Management

BuildRequires:  db4-devel
BuildRequires:  expat-devel
BuildRequires:  fdupes
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  rpm-devel
BuildRequires:  zlib-devel

%bcond_without enable_static
%bcond_without perl_binding
%bcond_without python_binding

%if %{with perl_binding}
BuildRequires:  perl
BuildRequires:  swig
%endif
%if %{with python_binding}
%global python_sitearch %(python2 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(True);")
BuildRequires:  python-devel
BuildRequires:  swig
%endif

%description
A new approach to package dependency solving.

%package devel
Summary:        A new approach to package dependency solving
Group:          Development/Libraries
Requires:       libsolv-tools = %version
Requires:       libsolv = %version
Requires:       rpm-devel

%description devel
Development files for libsolv, a new approach to package dependency solving

%package tools
Summary:        A new approach to package dependency solving
Group:          Development/Libraries
Obsoletes:      satsolver-tools < 0.18
Provides:       satsolver-tools = 0.18
Requires:       gzip bzip2 coreutils findutils

%description tools
A new approach to package dependency solving.

%package -n python-solv
Requires:       python
Summary:        Python bindings for the libsolv library
Group:          Platfrom Development/Python

%description -n python-solv
Python bindings for sat solver.

%package -n perl-solv
Requires:       perl = %{perl_version}
Summary:        Perl bindings for the libsolv library
Group:          Platfrom Development/Perl

%description -n perl-solv
Perl bindings for sat solver.

%prep
%setup -n libsolv-%{version}
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE10}

%build
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$CFLAGS"

CMAKE_FLAGS=
CMAKE_FLAGS="-DSUSE=1"

cmake   $CMAKE_FLAGS \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DLIB=%{_lib} \
	-DCMAKE_VERBOSE_MAKEFILE=TRUE \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	%{?with_enable_static:-DENABLE_STATIC=1} \
	%{?with_perl_binding:-DENABLE_PERL=1} \
	%{?with_python_binding:-DENABLE_PYTHON=1} \
    -DENABLE_COMPLEX_DEPS=1 \
	-DUSE_VENDORDIRS=1 \
	-DCMAKE_SKIP_RPATH=1
make %{?jobs:-j %jobs}

%install
make DESTDIR=$RPM_BUILD_ROOT install
%if %{with python_binding}
cd $RPM_BUILD_ROOT/%{python_sitearch}
%{__python} %py_libdir/py_compile.py *.py
%{__python} -O %py_libdir/py_compile.py *.py
cd -
%endif
install -D -m0755 examples/repo2solv.sh %{buildroot}%{_bindir}

%remove_docs
# we want to leave the .a file untouched
export NO_BRP_STRIP_DEBUG=true

%post  -p /sbin/ldconfig

%postun  -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE.BSD
%{_libdir}/libsolv.so.*
%{_libdir}/libsolvext.so.*

%files tools
%manifest %{name}.manifest
%license LICENSE.BSD
%{_bindir}/solv
%{_bindir}/*

%files devel
%manifest %{name}.manifest
%license LICENSE.BSD
%{_libdir}/pkgconfig/libsolv.pc
%{_libdir}/pkgconfig/libsolvext.pc
%if %{with enable_static}
%{_libdir}/libsolv.a
%{_libdir}/libsolvext.a
%endif
%if !%{with disable_shared}
%{_libdir}/libsolv.so
%{_libdir}/libsolvext.so
%endif
%{_includedir}/solv
%{_bindir}/helix2solv
%{_datadir}/cmake/Modules/*

%if %{with perl_binding}
%files -n perl-solv
%manifest %{name}.manifest
%license LICENSE.BSD
%{perl_vendorarch}/*
%endif

%if %{with python_binding}
%files -n python-solv
%manifest %{name}.manifest
%license LICENSE.BSD
%{python_sitearch}/*
%endif
