Name:           npth
Version:        1.8
Release:        1
Summary:        The New GNU Portable Threads library
License:        LGPL-2.1-or-later
URL:            https://git.gnupg.org/cgi-bin/gitweb.cgi?p=npth.git
Source0:        %{name}-%{version}.tar.bz2
Source1001:     %{name}.manifest

%description
nPth is a non-preemptive threads implementation using an API very similar
to the one known from GNU Pth. It has been designed as a replacement of
GNU Pth for non-ancient operating systems. In contrast to GNU Pth is is
based on the system's standard threads implementation. Thus nPth allows
the use of libraries which are not compatible to GNU Pth.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup
cp %{SOURCE1001} .

%build
%configure --disable-static
%{__make} %{?_smp_mflags}

%install
%make_install
find %{buildroot} -name '*.la' -delete -print

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING.LIB
%{_libdir}/lib%{name}.so.*

%files devel
%manifest %{name}.manifest
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/lib%{name}.so
%{_includedir}/%{name}.h
%{_datadir}/aclocal/%{name}.m4
%{_libdir}/pkgconfig/%{name}.pc
