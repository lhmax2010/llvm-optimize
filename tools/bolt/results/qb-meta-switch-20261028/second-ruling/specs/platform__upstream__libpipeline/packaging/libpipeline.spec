Name:           libpipeline
Version:        1.5.8
Release:        0
License:        GPL-3.0+
Summary:        A pipeline manipulation library
Url:            http://www.nongnu.org/libpipeline/
Group:          System/Libraries
Source:         %{name}-%{version}.tar.gz
Source1001: 	libpipeline.manifest
Source1002: 	disable_man_page.patch
BuildRequires:  automake
BuildRequires:  autoconf

%description
libpipeline is a C library for setting up and running pipelines of
processes, without needing to involve shell command-line parsing which
is often error-prone and insecure. This alleviates programmers of the
need to laboriously construct pipelines using lower-level primitives
such as fork(2) and execve(2).

%package devel
Summary:        A pipeline manipulation library
Group:          Development/Libraries
Requires:       %{name} = %{version}
Provides:       pkgconfig(%{name}) = %{version}

%description devel
libpipeline is a C library for setting up and running pipelines of
processes, without needing to involve shell command-line parsing which
is often error-prone and insecure. This alleviates programmers of the
need to laboriously construct pipelines using lower-level primitives
such as fork(2) and execve(2).

%prep
%setup -q
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE1002}

%build
autoreconf -fi
%configure			\
  --enable-shared		\
  --enable-threads=posix	\
  --disable-rpath		\
  --enable-socketpair-pipe	\
  --with-pic=yes		\
  --with-gnu-ld
make %{?_smp_mflags}

%install
%make_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license  COPYING
%defattr(-,root,root,0755)
%{_libdir}/libpipeline.so.*

%files devel
%manifest %{name}.manifest
%license  COPYING
%defattr(-,root,root,0755)
%{_libdir}/libpipeline.so
%{_libdir}/pkgconfig/libpipeline.pc
%{_includedir}/pipeline.h
