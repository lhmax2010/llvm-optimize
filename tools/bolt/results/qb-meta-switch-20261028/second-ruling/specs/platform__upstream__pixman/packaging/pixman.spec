Name:           pixman
Version:        0.38.4
Release:        0
License:        MIT
Summary:        Pixel manipulation library
Url:            http://cairographics.org/releases/%{name}-%{version}.tar.gz
Group:          System/Libraries
Source:         %{name}-%{version}.tar.gz
Source1:        baselibs.conf
Source1001:     pixman.manifest
BuildRequires:  pkgconfig(libpng)

%description
The pixel-manipulation library for X and cairo.

%package devel
Summary:        Development components for the pixman library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
The pixel-manipulation library for X and cairo.

Development components for the pixman library.

%prep
%setup -q
cp %{SOURCE1001} .

%build

export CFLAGS="$CFLAGS -w"
%{?_toolchain:
%if %{toolchain_is clang}
export CFLAGS="$CFLAGS -fno-integrated-as"
%endif
}
%reconfigure --disable-arm-iwmmxt
make %{?_smp_mflags}

%install
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/libpixman-1*.so.*

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%dir %{_includedir}/pixman-1
%{_includedir}/pixman-1/pixman.h
%{_includedir}/pixman-1/pixman-version.h
%{_libdir}/libpixman-1*.so
%{_libdir}/pkgconfig/pixman-1.pc

