Name:           libxml2
VCS:            platform/upstream/libxml2#3b75470643e5886ad743b77735f3f8cb58bfb3f6
Version:        2.15.1
Release:        1.13
Summary:        A Library to Manipulate XML Files
License:        MIT
URL:            http://xmlsoft.org
Source0:        ftp://xmlsoft.org/libxml2/%{name}-%{version}.tar.gz
Source1:        %{name}.manifest
Source2:        baselibs.conf
Source3:        Add_pie_compile_option.patch

BuildRequires:  cmake
BuildRequires:  pkg-config
BuildRequires:  readline-devel
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
BuildRequires:  gcc-c++

%description
The XML C library was initially developed for the GNOME project. It is
now used by many programs to load and save extensible data structures
or manipulate any kind of XML files.

This library implements a number of existing standards related to
markup languages, including the XML standard, name spaces in XML, XML
Base, RFC 2396, XPath, XPointer, HTML4, XInclude, SGML catalogs, and
XML catalogs. In most cases, libxml tries to implement the
specification in a rather strict way. To some extent, it provides
support for the following specifications, but does not claim to
implement them: DOM, FTP client, HTTP client, and SAX.

The library also supports RelaxNG. Support for W3C XML Schemas is in
progress.

%package tools
Summary:        Tools using libxml2
Requires:       %{name} = %{version}-%{release}

%description tools
This package contains xmllint, a very useful tool proving libxml's power.

%package devel
Summary:        Development files for libxml2
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-tools = %{version}-%{release}
Requires:       readline-devel
Requires:       xz-devel
Requires:       zlib-devel

%description devel
Development files and headers for libxml2.
This package contains libraries and header files for
developing applications that use libxml2.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1} .
%{__patch} -p1 < %{SOURCE3}

%build
export CFLAGS="$CFLAGS -fPIC"
export CXXFLAGS="$CXXFLAGS -fPIC"
%cmake . \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=ON \
    -DLIBXML2_WITH_PROGRAMS=ON \
    -DLIBXML2_WITH_TESTS=OFF \
    -DLIBXML2_WITH_PYTHON=OFF \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir}

%__make %{?_smp_mflags}

%install
%make_install DESTDIR=%{buildroot}

# Remove static libraries
find %{buildroot} -name "*.a" -delete
find %{buildroot} -name "*.la" -delete

# Remove documentation and man pages (Tizen policy)
rm -rf %{buildroot}%{_docdir}
rm -rf %{buildroot}%{_mandir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license Copyright
%{_libdir}/libxml2.so.*

%files tools
%manifest %{name}.manifest
%license Copyright
%{_bindir}/xmllint
%{_bindir}/xmlcatalog

%files devel
%manifest %{name}.manifest
%license Copyright
%{_bindir}/xml2-config
%{_includedir}/libxml2/
%{_libdir}/libxml2.so
%{_libdir}/pkgconfig/libxml-2.0.pc
%{_libdir}/cmake/libxml2/

