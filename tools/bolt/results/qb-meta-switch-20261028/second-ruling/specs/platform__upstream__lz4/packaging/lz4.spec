Name:       lz4
Summary:    LZ4 Extremely Fast Compression algorithm
Version:    1.10.0
Release:    1
Group:      System/Libraries
License:    BSD-2-Clause
Source0:    https://github.com/lz4/lz4/archive/v%{version}.tar.gz
Source1:    %{name}.manifest
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
LZ4 is lossless compression algorithm, providing compression speed > 500 MB/s
per core, scalable with multi-cores CPU. It features an extremely fast decoder,
with speed in multiple GB/s per core, typically reaching RAM speed limits on
multi-core systems.

%package bin
Summary:    LZ4 tools
Group:      Application/Text
License:    GPL-2.0
Requires:   %{name} = %{version}

%description bin
LZ4 is lossless compression algorithm. This package provides command line tools;
note that, unlike the main package, they are on a copyleft license.

%package devel
Summary:    Development files for the LZ4 library
Group:      Development/Libraries
Requires:   %{name} = %{version}

%description devel
LZ4 is lossless compression algorithm. This package provides the development
files for the library.

%prep
%setup -q
cp %{SOURCE1} .

%build
%__make BUILD_STATIC=0 %{?_smp_mflags}

%install
%__make install BUILD_STATIC=0 DESTDIR=%{?buildroot} PREFIX=/usr LIBDIR=%{_libdir} INSTALL="%{__install} -p"
rm %{?buildroot}%{_datadir}/man/man1/lz4.1
rm %{?buildroot}%{_datadir}/man/man1/lz4c.1
rm %{?buildroot}%{_datadir}/man/man1/lz4cat.1
rm %{?buildroot}%{_datadir}/man/man1/unlz4.1

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE.BSD-2-Clause
%{_libdir}/liblz4.so.*

%files bin
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE.GPL-2.0
%{_bindir}/lz4
%{_bindir}/lz4c
%{_bindir}/lz4cat
%{_bindir}/unlz4

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE.BSD-2-Clause
%{_includedir}/lz4.h
%{_includedir}/lz4frame.h
%{_includedir}/lz4hc.h
%{_libdir}/pkgconfig/liblz4.pc
%{_libdir}/liblz4.so
