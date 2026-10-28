%define         soname 0

Name:           openfst
VCS:            platform/upstream/openfst#4e7400ad975d0a1461887357dd558806d67c9a81
Version:        1.8.4
Release:        1.1
Summary:        Weighted finite-state transducer library
License:        Apache-2.0
Group:          Development/Tools/Other
Url:            http://www.openfst.org/
Source0:        %{name}-%{version}.tar.gz
Source1:        LICENSE.APACHE2.0
Source2:        Add-pie-compile-option.patch
Source1001:     openfst.manifest

BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(zlib)
BuildRequires:  python-devel

%description
OpenFst is a library for constructing, combining, optimizing and
searching weighted finite-state transducers (FSTs).

%package devel
Summary:        Development files for OpenFst
License:        Apache-2.0
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}-%{release}

%description devel
OpenFst is a library for constructing, combining, optimizing and
searching weighted finite-state transducers (FSTs).

%package tools
Summary:        Command-line tools for working with FSTs
Group:          Development/Tools/Other
Requires:       %{name} = %{version}-%{release}

%description tools
OpenFst is a library for constructing, combining, optimizing and
searching weighted finite-state transducers (FSTs).

This package contains command-line tools that give access to OpenFst
functionality.

%prep
%setup -q
cp %{SOURCE1} .
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE2}

%build
export CXXFLAGS="$CXXFLAGS -fPIC"
autoreconf -fi
%configure
%{__make} %{?_smp_mflags}

%install
%{__make} install DESTDIR=%{buildroot}

find  %{buildroot}%{_libdir} -name '*.la' -delete

%remove_docs

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest openfst.manifest
%license LICENSE.APACHE2.0
%{_libdir}/*.so.*

%files devel
%manifest openfst.manifest
%license LICENSE.APACHE2.0
%{_includedir}/fst
%{_libdir}/*.so

%files tools
%manifest openfst.manifest
%license LICENSE.APACHE2.0
%{_bindir}/*
