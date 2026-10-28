%define lname libcms2
Name:           lcms2
Summary:        Little CMS Engine - A color managment library and tools
License:        MIT
Group:          Graphics/Libraries
Url:            http://www.littlecms.com/
Version:        2.16
Release:        0
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  pkg-config
BuildRequires:  zlib-devel
Source0:        http://sourceforge.net/projects/lcms/files/lcms/%{version}/%{name}-%{version}.tar.gz
Source1001: 	lcms2.manifest

%description
Littlecms is a small speed optimized color management engine.
Little CMS intends to be a small-footprint color management engine
with a special focus on accuracy and performance. It uses the International
Color Consortium standard (ICC), which is the modern standard when
regarding to color management. The ICC specification is widely used and is
referred to in many International and other de-facto standards.

%package -n libcms2
Summary:        Libraries for the Little CMS Engine
Group:          Graphics/Libraries

%description -n libcms2
Little CMS Engine - A color managment library and tools.

%package -n liblcms2-devel
Summary:        Include Files and Libraries Mandatory for Development
Group:          Development/Libraries
Requires:       libcms2 = %{version}
Requires:       glibc-devel

%description -n liblcms2-devel
This package contains all necessary include files and libraries needed
to develop applications that require these.

%prep
%setup -q
cp %{SOURCE1001} .

chmod a-x doc/* LICENSE AUTHORS

%build
%configure --without-threads
make %{?_smp_flags}

%install
%make_install

%post -n libcms2 -p /sbin/ldconfig

%postun -n libcms2 -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license LICENSE
%{_bindir}/*

%files -n libcms2
%manifest %{name}.manifest
%defattr(-,root,root)
%license LICENSE
%{_libdir}/liblcms2.so.2*

%files -n liblcms2-devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%docs_package
