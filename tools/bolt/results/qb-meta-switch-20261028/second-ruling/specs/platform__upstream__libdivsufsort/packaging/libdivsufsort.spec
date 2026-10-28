Name:		libdivsufsort
Summary:	Suffix Array Construction Algorithm Library
Version:	2.0.2
Release:	1
Group:		System
License:	MIT
Source0:	%{name}-%{version}.tar.gz

BuildRequires:	cmake

%description
libdivsufsort is a software library that implements a lightweight suffix array construction algorithm.

%package devel
Summary:	libdivsufsort for (devel)

%description devel
libdivsufsort library package for (devel)

%prep
%setup -q

%build
%cmake .
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%files
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/libdivsufsort.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/libdivsufsort.so
%{_libdir}/pkgconfig/libdivsufsort.pc
