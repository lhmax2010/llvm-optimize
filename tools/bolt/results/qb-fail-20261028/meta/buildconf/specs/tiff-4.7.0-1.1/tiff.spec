Name:           tiff
VCS:            platform/upstream/tiff#13ae957bd0dcf493b026da4afeeac5eab9f89537
Version:        4.7.0
Release:        1.1
License:        libtiff
Summary:        Tools for Converting from and to the Tiff Format
Url:            https://gitlab.com/libtiff/libtiff
Group:          Productivity/Graphics/Convertors
Source:         tiff-%{version}.tar.bz2
Source3:        baselibs.conf
Source1001: 	tiff.manifest
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  libjpeg-devel
BuildRequires:  libtool
BuildRequires:  lzma-devel
BuildRequires:  pkg-config
BuildRequires:  pkgconfig(zlib)
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
This package contains the library and support programs for the TIFF
image format.

%package -n libtiff
Summary:        The Tiff Library (with JPEG and compression support)
Group:          System/Libraries

%description -n libtiff
This package includes the tiff libraries. To link a program with
libtiff, you will have to add -ljpeg and -lz to include the necessary
libjpeg and libz in the linking process.

%package -n libtiff-devel
Summary:        Development Tools for Programs which will use the libtiff Library
Group:          Development/Libraries/C and C++
Requires:       glibc-devel
Requires:       libstdc++-devel
Requires:       libtiff = %{version}

%description -n libtiff-devel
This package contains the header files and static libraries for
developing programs which will manipulate TIFF format image files using
the libtiff library.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%cmake . -Dtiff-tools=OFF -Dtiff-tests=OFF -Dtiff-contrib=OFF
make %{?_smp_mflags}

%install
%make_install

%docs_package

%post -n libtiff -p /sbin/ldconfig

%postun -n libtiff -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license LICENSE.md

%files -n libtiff
%manifest %{name}.manifest
%license LICENSE.md
%{_libdir}/*.so.*

%files -n libtiff-devel
%manifest %{name}.manifest
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/%{name}/*.cmake

