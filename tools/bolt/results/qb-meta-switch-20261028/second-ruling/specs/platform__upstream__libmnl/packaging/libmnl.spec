Name:           libmnl
Summary:        Minimalistic Netlink communication library
License:        LGPL-2.1+
Group:          Productivity/Networking/Security
Version:        1.0.3
Release:        0
Url:            http://netfilter.org/projects/libmnl/

#Git-Clone:	git://git.netfilter.org/libmnl
Source:         ftp://ftp.netfilter.org/pub/libmnl/%name-%version.tar.bz2
Source2:        baselibs.conf
Source1001: 	libmnl.manifest
BuildRequires:  libtool
BuildRequires:  pkgconfig >= 0.21

%description
libmnl is a minimalistic user-space library oriented to Netlink
developers. There are a lot of common tasks in parsing, validating,
constructing of both the Netlink header and TLVs that are repetitive
and easy to get wrong. This library aims to provide simple helpers
that allows you to re-use code and to avoid re-inventing the wheel.

%package devel
Requires:       %name = %version
Summary:        Development files for libmnl
Group:          Development/Libraries/C and C++

%description devel
libmnl is a minimalistic user-space library oriented to Netlink
developers. There are a lot of common tasks in parsing, validating,
constructing of both the Netlink header and TLVs that are repetitive
and easy to get wrong. This library aims to provide simple helpers
that allows you to re-use code and to avoid re-inventing the wheel.

%prep
%setup -q
cp %{SOURCE1001} .

%build
if [ ! -e configure ]; then
	autoreconf -fi;
fi;
%configure --includedir=%_includedir/%name-%version
make %{?_smp_mflags}

%install
%make_install

%post  -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING
%defattr(-,root,root)
%_libdir/libmnl.so.0*

%files -n %name-devel
%manifest %{name}.manifest
%defattr(-,root,root)
%_includedir/libmnl*
%_libdir/libmnl.so
%_libdir/pkgconfig/libmnl.pc

%changelog
