%define libname libjson
%define libsoname %{libname}
Name:           json-c
Version:        0.18
Release:        0
Summary:        JSON implementation in C
License:        MIT
Group:          Development/Libraries/C and C++
Url:            https://github.com/json-c/json-c/wiki
#Git-Clone	git://github.com/json-c/json-c
Source0:        https://s3.amazonaws.com/json-c_releases/releases/%{name}-%{version}.tar.gz
Source1:        baselibs.conf
Source100:      Install_json_object_private.h_file.patch
Source101:      Disabled_arc4random.patch
Source1001:     json-c.manifest
BuildRequires:  libtool
BuildRequires:  cmake
BuildRequires:  pkgconfig

%description
JSON-C implements a reference counting object model that allows you to
easily construct JSON objects in C, output them as JSON formatted
strings and parse JSON formatted strings back into the C
representation of JSON objects.

%package -n %{libsoname}
Summary:        JSON-C shared library
Group:          System/Libraries

%description -n %{libsoname}
JSON-C implements a reference counting object model that allows you to
easily construct JSON objects in C, output them as JSON formatted
strings and parse JSON formatted strings back into the C
representation of JSON objects.

This package includes the JSON library.

%package -n %{libname}-devel
Summary:        Development headers and libraries for json-c
Group:          Development/Libraries/C and C++
Requires:       %{libsoname} = %{version}

%description -n %{libname}-devel
JSON-C implements a reference counting object model that allows you to
easily construct JSON objects in C, output them as JSON formatted
strings and parse JSON formatted strings back into the C
representation of JSON objects.

This package includes header files and scripts needed for developers
using the json-c library

%prep
%setup -q
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE100}
%{__patch} -p1 < %{SOURCE101}

%build
%{?asan: export VALGRIND=1}
%{?hwasan: export VALGRIND=1}
%{cmake} .
%{__make} %{?_smp_mflags}

%check
# %{__make} test

%install
DESTDIR=%{buildroot} %{__make} install

find %{buildroot} -type f -name "*.la" -delete -print
# create a compatibilty pkg-config file for software needing it
(cd %{buildroot}%{_libdir}/pkgconfig && ln -s json-c.pc json.pc)

# delete static file
rm -f %{buildroot}%{_libdir}/libjson-c.a

%remove_docs

%post -n %{libsoname} -p /sbin/ldconfig
%postun -n %{libsoname} -p /sbin/ldconfig

%files -n %{libsoname}
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/libjson-c.so.*
%license COPYING

%files -n %{libname}-devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/libjson-c.so
%{_includedir}/json-c
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/json-c/json-c-config.cmake
%{_libdir}/cmake/json-c/json-c-targets-debug.cmake
%{_libdir}/cmake/json-c/json-c-targets.cmake

%changelog
