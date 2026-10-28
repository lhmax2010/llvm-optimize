Name:           libthai
Version:        0.1.18
Release:        0
License:        LGPL-2.1+
Summary:        Thai Language Support Routines
Url:            http://linux.thai.net/plone/TLWG/libthai/
Group:          System/Libraries
Source:         %{name}-%{version}.tar.gz
Source99:       baselibs.conf
Source1001: 	libthai.manifest
BuildRequires:  pkgconfig(datrie-0.2)
BuildRequires:  pkg-config
Requires:       libthai-data >= %{version}

%description
LibThai is a set of Thai language support routines aimed to ease
developers' tasks to incorporate Thai language support in their
applications. It includes important Thai-specific functions, such as
word breaking, input and output methods, and basic character and string
support.

%package data
Summary:        Thai Language Support Routines - Data files
Group:          System/Libraries

%description data
LibThai is a set of Thai language support routines aimed to ease
developers' tasks to incorporate Thai language support in their
applications. It includes important Thai-specific functions, such as
word breaking, input and output methods, and basic character and string
support.

This package contains the data files for libthai.

%package devel
Summary:        Thai Language Support Routines (development files)
Group:          Development/Languages/C and C++
Requires:       libthai = %{version}

%description devel
LibThai is a set of Thai language support routines aimed to ease
developers' tasks to incorporate Thai language support in their
applications. It includes important Thai-specific functions, such as
word breaking, input and output methods, and basic character and string
support.

This package contains headers and libraries required for developing
software using libthai.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%configure --disable-static --with-pic
make %{?_smp_mflags}

%install
%make_install


%post  -p /sbin/ldconfig

%postun  -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING
%defattr(-,root,root)
%{_libdir}/libthai.so.*

%files data
%manifest %{name}.manifest
%defattr(-, root, root)
%{_datadir}/libthai/

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_includedir}/thai/
%{_libdir}/libthai.so
%{_libdir}/pkgconfig/*.pc

%changelog
