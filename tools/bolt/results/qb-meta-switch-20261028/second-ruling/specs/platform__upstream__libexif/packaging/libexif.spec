Name:           libexif
Version:        0.6.22
Release:        0
License:        LGPL-2.1
Summary:        An EXIF Tag Parsing Library for Digital Cameras
Url:            https://libexif.github.io
Group:          System/Libraries
Source:         %{name}-%{version}.tar.bz2
Requires(post):  /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

%define debug_package_requires %{name} = %{version}-%{release}

%description
This library is used to parse EXIF information from JPEGs created by
digital cameras.

%package devel
Summary:        An EXIF Tag Parsing Library for Digital Cameras (Development files)
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}

%description devel
This library is used to parse EXIF information from JPEGs created by
digital cameras.

%prep
%setup -q

%build
sh ./autogen.sh
%configure --with-pic \
	--disable-static \
	--disable-docs

make %{?jobs:-j%jobs}

%install
%make_install
#%find_lang %{name}-12

%post  -p /sbin/ldconfig

%postun  -p /sbin/ldconfig

#%files -f %{name}-12.lang
%files
%manifest %{name}.manifest
%license COPYING
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/libexif
%{_libdir}/*.so
%{_libdir}/pkgconfig/libexif.pc

