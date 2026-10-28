# to build examples
%define enable_examples 0

Name:		wayland-extension
Version:	1.3.88
Release:	0
Summary:	Wayland extenstion protocols that add functionality not available in the Wayland core protocol
License:	MIT
Group:		Graphics & UI Framework/Wayland Window System
URL:		http://www.tizen.org/
Source:		%name-%version.tar.xz
Source1001:	%name.manifest
BuildRequires:	autoconf >= 2.64, automake >= 1.11
BuildRequires:	libtool >= 2.2
BuildRequires:	pkgconfig
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(gmock)

# requires to build examples
%if "%{enable_examples}" == "1"
BuildRequires:  pkgconfig(evas)
BuildRequires:  pkgconfig(ecore)
BuildRequires:  pkgconfig(ecore-wl2)
BuildRequires:  pkgconfig(elementary)
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  pkgconfig(wayland-tbm-client)
# NB: It causes a circular dependency, however we have no choice
#     but to use the elm to build examples.
BuildRequires:  wayland-extension-client-devel
%endif

%description
wayland-extension contains Wayland protocols that add functionality not available in the Wayland core protocol.

%package -n libwayland-extension-client
Group:		Graphics & UI Framework/Wayland Window System
Summary:	Wayland Extension client library
Requires:   libwayland-client

%description -n libwayland-extension-client
wayland-extension is a protocol for tizen window system.

%package -n libwayland-extension-server
Group:		Graphics & UI Framework/Wayland Window System
Summary:	Wayland Extension server library
Requires:   libwayland-server

%description -n libwayland-extension-server
wayland-extension is a protocol for tizen window system.

%package -n wayland-extension-client-devel
Summary:	Client development files for the Wayland Extension Protocol
Group:		Graphics & UI Framework/Development
Requires:	libwayland-extension-client = %version

%description -n wayland-extension-client-devel
wayland-extension is a protocol for tizen window system.

This package contains all necessary include files and libraries needed
to develop applications that require these.

%package -n wayland-extension-server-devel
Summary:	Server development files for the Wayland Extension Protocol
Group:		Graphics & UI Framework/Development
Requires:	libwayland-extension-server = %version

%description -n wayland-extension-server-devel
wayland-extension is a protocol for tizen window system.

This package contains all necessary include files and libraries needed
to develop a compositor that require these.

%package -n wayland-protocols
Summary:	Wayland upstream protocols
Group:		Graphics & UI Framework/Development
Requires:   libwayland-client

%description -n wayland-protocols
wayland-protocols contains Wayland upstream protocols that add functionality not available in the Wayland core protocol

%package -n libwayland-extension-unittests
Summary: Unit test cases for the libwayland-extension
Group:   Graphics & UI Framework/Development
Requires:   libwayland-client
Requires:   libwayland-server

%description -n libwayland-extension-unittests
Unit test cases for the libwayland-extension

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="$CFLAGS -Wall -Werror"
%if "%{enable_examples}" == "1"
   export CFLAGS="$CFLAGS -DEFL_BETA_API_SUPPORT "
   %reconfigure --disable-static --enable-build-examples LIBDIR=%{_libdir}
%else
   %reconfigure --disable-static LIBDIR=%{_libdir}
%endif
make %{?_smp_mflags}

%install
%make_install

%post -n libwayland-extension-client -p /sbin/ldconfig
%postun -n libwayland-extension-client -p /sbin/ldconfig
%post -n libwayland-extension-server -p /sbin/ldconfig
%postun -n libwayland-extension-server -p /sbin/ldconfig

%files -n libwayland-extension-client
%manifest %{name}.manifest
%license COPYING
%defattr(-,root,root)
%_libdir/*-client.so.0*
%if "%{enable_examples}" == "1"
%{_bindir}/*
%endif

%files -n libwayland-extension-server
%manifest %{name}.manifest
%license COPYING
%defattr(-,root,root)
%_libdir/*-server.so.0*

%files -n wayland-extension-client-devel
%manifest %{name}.manifest
%defattr(-,root,root)
%_includedir/wayland-extension/wayland-extension-version.h
%_includedir/wayland-extension/*-client-protocol.h
%_libdir/*-client.so
%_libdir/pkgconfig/*-client.pc

%files -n wayland-extension-server-devel
%manifest %{name}.manifest
%defattr(-,root,root)
%_includedir/wayland-extension/wayland-extension-version.h
%_includedir/wayland-extension/*-server-protocol.h
%_libdir/*-server.so
%_libdir/pkgconfig/*-server.pc

%files -n wayland-protocols
%manifest %{name}.manifest
%license COPYING
%defattr(-,root,root)
%_datadir/wayland-extension/protocol/tizen/*
%_datadir/wayland-extension/protocol/stable/*
%_datadir/wayland-extension/protocol/staging/*
%_datadir/wayland-extension/protocol/unstable/*
%_libdir/pkgconfig/wayland-protocols.pc

%files -n libwayland-extension-unittests
%defattr(-,root,root,-)
%{_bindir}/libwayland-extension-unittests

%changelog
