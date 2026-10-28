Name:           libwbxml2
Version:        0.11.10
Release:        1
License:        LGPL-2.1+
Summary:        WBXML parser and compiler library
Url:            https://github.com/libwbxml/libwbxml
Group:          System/Libraries
Source:         libwbxml-%{version}.tar.bz2
Source1:        Add-pie-compile-option.patch
Source1001: 	libwbxml2.manifest
Source1002: 	COPYING.LGPLv2.1
Source1003: 	COPYING.GPLv2

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(pkg-config)
BuildRequires:  pkgconfig(popt)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libxml-2.0)

%description
wbxml2 is a library that includes a WBXML parser and a WBXML compiler.
Unlike wbxml, it does not depend on libxml2 but on expat, making it
faster and more portable. WBXML Library contains a library and its
associated tools to Parse, Encode and Handle WBXML documents. The WBXML
(Wireless Binary XML) format is a binary representation of XML, and it
has been defined by the Wap Forum.

%package -n wbxml2-tools
License:        GPL-2.0+
Summary:        Tools for libwbxml2
Group:          System/Utilities
Requires:       pkgconfig(libxml-2.0)
Requires:       %{name} = %{version}

%description -n wbxml2-tools
wbxml2 is a library that includes a WBXML parser and a WBXML compiler.
Unlike wbxml, it does not depend on libxml2 but on expat, making it
faster and more portable. WBXML Library contains a library and its
associated tools to Parse, Encode and Handle WBXML documents. The WBXML
(Wireless Binary XML) format is a binary representation of XML, and it
has been defined by the Wap Forum.

%package devel
License:        LGPL-2.1+
Summary:        WBXML parser and compiler library
Group:          System/Development
Requires:       glibc-devel
Requires:       libwbxml2 = %{version}
Requires:       pkgconfig(expat)
Requires:       pkgconfig(libxml-2.0)

%description devel
wbxml2 is a library that includes a WBXML parser and a WBXML compiler.
Unlike wbxml, it does not depend on libxml2 but on expat, making it
faster and more portable. WBXML Library contains a library and its
associated tools to Parse, Encode and Handle WBXML documents. The WBXML
(Wireless Binary XML) format is a binary representation of XML, and it
has been defined by the Wap Forum.

%prep
%setup -q -n libwbxml-%{version}
%__patch -p1 < %{SOURCE1}
cp %{SOURCE1001} .
cp %{SOURCE1002} .
cp %{SOURCE1003} .

%build
mkdir build
cd build
CFLAGS="%{optflags}" \
CXXFLAGS="%{optflags}" \
%cmake \
        -DCMAKE_BUILD_TYPE=None \
        -DENABLE_INSTALL_DOC:BOOL=OFF \
         %{_builddir}/libwbxml-%{version}
%__make %{?_smp_mflags} VERBOSE=1
cd -

%install
cd build
%make_install
cd -

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING.LGPLv2.1
%{_libdir}/libwbxml2.so.1*

%files devel
%manifest %{name}.manifest
%license COPYING.LGPLv2.1
%{_libdir}/pkgconfig/libwbxml2.pc
%{_libdir}/libwbxml2.so
%{_includedir}/libwbxml-1.1/wbxml
%{_libdir}/cmake/libwbxml2/*

%files -n wbxml2-tools
%manifest %{name}.manifest
%license COPYING.GPLv2
%{_bindir}/wbxml2xml
%{_bindir}/xml2wbxml

%changelog
