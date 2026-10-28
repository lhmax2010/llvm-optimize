%define EGL_PACKAGE 1

Name:		wayland
Version:	1.23.1
Release:	0
Summary:	Wayland Compositor Infrastructure
License:	MIT
Group:		Graphics & UI Framework/Wayland Window System
URL:		http://wayland.freedesktop.org/

#Git-Clone:	git://anongit.freedesktop.org/wayland/wayland
#Git-Web:	http://cgit.freedesktop.org/wayland/wayland/
Source:		%name-%version.tar.xz
Source1001:	%name.manifest
BuildRequires:	meson
BuildRequires:	autoconf >= 2.64, automake >= 1.11
BuildRequires:	libtool >= 2.2
BuildRequires:	pkgconfig
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  expat-devel
BuildRequires:  pkgconfig(libxml-2.0)

%description
Wayland is a protocol for a compositor to talk to its clients as well
as a C library implementation of that protocol. The compositor can be
a standalone display server running on Linux kernel modesetting and
evdev input devices, an X application, or a wayland client itself.
The clients can be traditional applications, X servers (rootless or
fullscreen) or other display servers.

%package -n libwayland-client
Group:		Graphics & UI Framework/Wayland Window System
Summary:	Wayland core client library

%description -n libwayland-client
Wayland is a protocol for a compositor to talk to its clients as well
as a C library implementation of that protocol. The compositor can be
a standalone display server running on Linux kernel modesetting and
evdev input devices, an X application, or a wayland client itself.
The clients can be traditional applications, X servers (rootless or
fullscreen) or other display servers.

%package -n libwayland-cursor
Group:		Graphics & UI Framework/Wayland Window System
Summary:	Wayland cursor library

%description -n libwayland-cursor
The purpose of this library is to be the equivalent of libXcursor in
the X world. This library is compatible with X cursor themes and
loads them directly into an shm pool making it easy for the clients
to get buffer for each cursor image.

%package -n libwayland-server
Group:		Graphics & UI Framework/Wayland Window System
Summary:	Wayland core server library

%description -n libwayland-server
Wayland is a protocol for a compositor to talk to its clients as well
as a C library implementation of that protocol. The compositor can be
a standalone display server running on Linux kernel modesetting and
evdev input devices, an X application, or a wayland client itself.
The clients can be traditional applications, X servers (rootless or
fullscreen) or other display servers.

%if "%{EGL_PACKAGE}" == "1"
%package -n libwayland-egl
Group:		Graphics & UI Framework/Wayland Window System
Summary:	Wayland egl library

%description -n libwayland-egl
The purpose of this library is to support wayland-egl frontend APIs and
make the backend for each target.
%endif

%package devel
Summary:	Development files for the Wayland Compositor Infrastructure
Group:		Graphics & UI Framework/Development
Requires:	libwayland-client = %version
Requires:	libwayland-cursor = %version
Requires:	libwayland-server = %version
%if "%{EGL_PACKAGE}" == "1"
Requires:	libwayland-egl = %version
%endif

%description devel
Wayland is a protocol for a compositor to talk to its clients as well
as a C library implementation of that protocol. The compositor can be
a standalone display server running on Linux kernel modesetting and
evdev input devices, an X application, or a wayland client itself.
The clients can be traditional applications, X servers (rootless or
fullscreen) or other display servers.

This package contains all necessary include files and libraries needed
to develop applications that require these.

%prep
%setup -q
cp %{SOURCE1001} .

%build
EGLLIB="no"
%if "%{EGL_PACKAGE}" == "1"
EGLLIB="yes"
%endif
meson setup \
          --prefix /usr \
          --libdir %{_libdir} \
          --bindir %{_bindir} \
          builddir
ninja -C builddir all

%install
export DESTDIR=%{buildroot}
ninja -C builddir install

%post -n libwayland-client -p /sbin/ldconfig
%postun -n libwayland-client -p /sbin/ldconfig
%post -n libwayland-cursor -p /sbin/ldconfig
%postun -n libwayland-cursor -p /sbin/ldconfig
%post -n libwayland-server -p /sbin/ldconfig
%postun -n libwayland-server -p /sbin/ldconfig
%if "%{EGL_PACKAGE}" == "1"
%post -n libwayland-egl -p /sbin/ldconfig
%postun -n libwayland-egl -p /sbin/ldconfig
%endif

%files -n libwayland-client
%manifest %{name}.manifest
%license COPYING
%defattr(-,root,root)
%_libdir/libwayland-client.so.0*

%files -n libwayland-cursor
%manifest %{name}.manifest
%license COPYING
%defattr(-,root,root)
%_libdir/libwayland-cursor.so.0*

%files -n libwayland-server
%manifest %{name}.manifest
%license COPYING
%defattr(-,root,root)
%_libdir/libwayland-server.so.0*

%if "%{EGL_PACKAGE}" == "1"
%files -n libwayland-egl
%manifest %{name}.manifest
%license COPYING
%defattr(-,root,root)
%_libdir/libwayland-egl.so.1*
%endif

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%_bindir/wayland-scanner
%_includedir/wayland-*.h
%_libdir/libwayland-*.so
%_libdir/pkgconfig/wayland-*.pc
%_datadir/wayland/wayland*
%_datadir/aclocal
%doc README.md

%changelog
