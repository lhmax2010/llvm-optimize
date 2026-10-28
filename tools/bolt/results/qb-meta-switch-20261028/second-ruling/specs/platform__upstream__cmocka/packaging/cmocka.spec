Name:           cmocka
Version:        1.1.8
Release:        1
Summary:        Library for testing and mocking C code
License:        Apache-2.0
URL:            https://cmocka.org/
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.manifest

BuildRequires:  cmake

%description
Framework for writing and using C mock functions on a variety of
platforms. CMocka provides a simple and elegant way to test C code
with support for mock objects and test fixtures.

%package devel
Summary:        Development files for cmocka
Requires:       %{name} = %{version}

%description devel
Development files for cmocka, including headers and CMake configuration
files needed to build applications that use cmocka.

%prep
%setup -q
cp %{SOURCE1} .

%build
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DLIB_INSTALL_DIR=%{_libdir} \
      -DCMAKE_EXE_LINKER_FLAGS="-Wl,-z,relro,-z,now" \
      -DCMAKE_SHARED_LINKER_FLAGS="-Wl,-z,relro,-z,now" \
      ../
%__make %{?_smp_mflags}

%install
cd build
%make_install

%{remove_docs}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING
%{_libdir}/libcmocka.so.*

%files devel
%manifest %{name}.manifest
%{_includedir}/cmocka.h
%{_includedir}/cmocka_pbc.h
%{_libdir}/libcmocka.so
%{_libdir}/pkgconfig/cmocka.pc
%{_libdir}/cmake/cmocka/cmocka-*.cmake

%changelog
