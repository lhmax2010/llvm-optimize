Summary: Simple DirectMedia Layer
Name: SDL2
Version: 2.0.14
Release: 2
Source: http://www.libsdl.org/release/%{name}-%{version}.tar.gz
URL: http://www.libsdl.org/
License: Zlib and SGI-B-2.0
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
Prefix: %{_prefix}
%ifos linux
Provides: libSDL2-2.0.so.0
%endif

%define _unpackaged_files_terminate_build 0
%define __defattr %defattr(-,root,root)
%define __soext so
%define __version 2.0.14

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-egl-tizen)
BuildRequires:  pkgconfig(text-client)
BuildRequires:  pkgconfig(tizen-extension-client)
BuildRequires:  pkgconfig(tizen-remote-surface-client)
BuildRequires:  pkgconfig(wayland-tbm-client)
Requires:       libwayland-extension-client
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(ecore-ipc)
BuildRequires:  binutils-devel
BuildRequires:  which
BuildRequires:  autoconf
BuildRequires:  pkgconfig(ecore)
BuildRequires:  pkgconfig(ecore-wl2)
BuildRequires:  pkgconfig(appcore-common)
BuildRequires:  pkgconfig(capi-system-system-settings)
BuildRequires:  pkgconfig(capi-appfw-app-control)
BuildRequires:  pkgconfig(capi-appfw-app-common)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(ecore-imf)
BuildRequires:  pkgconfig(ecore-input)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  terminfo-base-mini

BuildRequires:  pkgconfig(appcore-ui)

%description
This is the Simple DirectMedia Layer, a generic API that provides low
level access to audio, keyboard, mouse, and display framebuffer across
multiple platforms.

%package devel
Summary: Libraries, includes and more to develop SDL applications.
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
This is the Simple DirectMedia Layer, a generic API that provides low
level access to audio, keyboard, mouse, and display framebuffer across
multiple platforms.

This is the libraries, include files and other resources you can use
to develop SDL applications.


%package -n SDL2_ttf
Summary: Libraries, includes and more to develop SDL applications.
Group: Development/Libraries
Version: 2.0.14
Release: 1
%description -n SDL2_ttf
This library allows you to use TrueType fonts to render text in SDL applications.
%package -n SDL2_ttf-devel
Summary: Libraries, includes and more to develop SDL applications.
Group: Development/Libraries
Version: 2.0.14
Release: 1
Requires: SDL2_ttf
Requires: SDL2-devel
%description -n SDL2_ttf-devel
This library allows you to use TrueType fonts to render text in SDL applications.
%prep
%setup -q

%build

#make %{?_smp_mflgs}
BUILD_PATH=$RPM_BUILD_DIR/%{name}-%{__version}

%if "%{asan}" == "1"
%restore_fcommon
LDFLAGS+=" -lasan -ldl "
%endif
%ifos linux
chmod +x configure
CFLAGS="$RPM_OPT_FLAGS" %configure --prefix=%{prefix} --disable-video-directfb --disable-video-wayland --enable-video-tizen %{?asan:--disable-assembly}
autoreconf -fi
libtoolize --force
make %{?_smp_mflgs}
rm -rf build-scripts/ltmain.sh
#########
mkdir -p $BUILD_PATH/usr/include/SDL2
mkdir -p $BUILD_PATH/usr/lib/pkgconfig
export PKG_CONFIG_PATH=$BUILD_PATH/usr/lib/pkgconfig
cp -f $BUILD_PATH/include/* $BUILD_PATH/usr/include/SDL2 
cp -f $BUILD_PATH/sdl2.pc $BUILD_PATH/usr/lib/pkgconfig
cp -f $BUILD_PATH/build/.libs/lib*.%{__soext} $BUILD_PATH/usr/lib
cp -f $BUILD_PATH/build/.libs/libSDL2main.a $BUILD_PATH/usr/lib
#########
cd extension/SDL2_ttf-2.0.14
libtoolize --force
chmod +x autogen.sh
./autogen.sh
chmod +x configure
CPPFLAGS="-I$BUILD_PATH/usr/include/SDL2" 
LDFLAGS="-L$BUILD_PATH/usr/lib" 
LIBS="-lSDL2 -lSDL2main"
CFLAGS="$RPM_OPT_FLAGS -I$BUILD_PATH/usr/include/SDL2" %configure --prefix=%{prefix}
rm -rf ltmain.sh

make %{?_smp_mflgs}
%else
%configure %{?asan:--disable-assembly}
%endif
#make

%install
rm -rf $RPM_BUILD_ROOT
%ifos linux
mkdir -p %{buildroot}%{_sysconfdir}/profile.d/
sed -i -e 's|@LIBDIR@|%{_libdir}|g' script/SDL.sh
cp -f script/SDL.sh %{buildroot}/%{_sysconfdir}/profile.d/

make install prefix=$RPM_BUILD_ROOT%{prefix} \
             bindir=$RPM_BUILD_ROOT%{_bindir} \
             libdir=$RPM_BUILD_ROOT%{_libdir} \
             includedir=$RPM_BUILD_ROOT%{_includedir} \
             datadir=$RPM_BUILD_ROOT%{_datadir} \
             mandir=$RPM_BUILD_ROOT%{_mandir}
cd extension/SDL2_ttf-2.0.14
make install prefix=$RPM_BUILD_ROOT%{prefix} \
             bindir=$RPM_BUILD_ROOT%{_bindir} \
             libdir=$RPM_BUILD_ROOT%{_libdir} \
             includedir=$RPM_BUILD_ROOT%{_includedir} \
%else
%makeinstall
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%manifest SDL2.manifest
%{__defattr}
%license COPYING.txt
#%doc README*.txt COPYING.txt CREDITS.txt BUGS.txt
%{_libdir}/lib*.%{__soext}.*
%exclude %{_libdir}/libSDL2_ttf*
%{_sysconfdir}/profile.d/SDL.sh

%files devel
%{__defattr}
#%doc docs/README*.md
%{_bindir}/*-config
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/lib*.%{__soext}
%{_includedir}/*/*.h
%{_libdir}/cmake/*
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/*
%exclude %{_includedir}/SDL2/SDL_ttf.h
%exclude %{_libdir}/libSDL2_ttf*
%exclude %{_libdir}/pkgconfig/SDL2_ttf.pc
%files -n SDL2_ttf
%defattr(-,root,root)
#%doc README CHANGES COPYING
%{_libdir}/libSDL2_ttf*.so.*
%{_libdir}/libSDL2_ttf*.so
%files -n SDL2_ttf-devel
%defattr(-,root,root)
#%doc README CHANGES COPYING
%{_libdir}/libSDL2_ttf.la
%{_libdir}/libSDL2_ttf.a
%{_libdir}/libSDL2_ttf*.so
%{_libdir}/pkgconfig/SDL2_ttf.pc
%{_includedir}/*/SDL_ttf.h

%changelog
* Thu Jun 04 2015 Ryan C. Gordon <icculus@icculus.org>
- Fixed README paths.

* Sun Dec 07 2014 Simone Contini <s.contini@oltrelinux.com>
- Fixed changelog date issue and docs filenames

* Sun Jan 22 2012 Sam Lantinga <slouken@libsdl.org>
- Updated for SDL 2.0

* Tue May 16 2006 Sam Lantinga <slouken@libsdl.org>
- Removed support for Darwin, due to build problems on ps2linux

* Sat Jan 03 2004 Anders Bjorklund <afb@algonet.se>
- Added support for Darwin, updated spec file

* Wed Jan 19 2000 Sam Lantinga <slouken@libsdl.org>
- Re-integrated spec file into SDL distribution
- 'name' and 'version' come from configure
- Some of the documentation is devel specific
- Removed SMP support from %build - it doesn't work with libtool anyway

* Tue Jan 18 2000 Hakan Tandogan <hakan@iconsult.com>
- Hacked Mandrake sdl spec to build 1.1

* Sun Dec 19 1999 John Buswell <johnb@mandrakesoft.com>
- Build Release

* Sat Dec 18 1999 John Buswell <johnb@mandrakesoft.com>
- Add symlink for libSDL-1.0.so.0 required by sdlbomber
- Added docs

* Thu Dec 09 1999 Lenny Cartier <lenny@mandrakesoft.com>
- v 1.0.0

* Mon Nov  1 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- First spec file for Mandrake distribution.

# end of file
