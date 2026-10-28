%bcond_with utest
%bcond_with utest_gcov

#TPL VERSION MACROS
%define TPL_VERSION_MAJOR	1
%define TPL_VERSION_MINOR	13
%define TPL_VERSION_PATCH	5
%define TPL_VERSION			%{TPL_VERSION_MAJOR}.%{TPL_VERSION_MINOR}.%{TPL_VERSION_PATCH}

#TPL WINDOW SYSTEM DEFINITION
%define TPL_WINSYS	WL

#TPL FEATURE OPTION
%define ENABLE_TTRACE				1
%define ENABLE_DLOG					1
%define ENABLE_DEFAULT_LOG			0
%define ENABLE_DEFAULT_DUMP			0
%define ENABLE_OBJECT_HASH_CHECK	1
%define ENABLE_WORKER_TEST_ONLY		0
%define ENABLE_DEFAULT_WL_THREAD	0
%define ENABLE_TIZEN_FEATURE		1

#TPL INSTALL OPTION
%define ENABLE_TPL_TEST			0
%define ENABLE_TPL_TEST_GCOV	0

#WAYLAND-EGL-TIZEN VERSION MACROS
%define WL_EGL_TIZEN_VERSION_MAJOR	1
%define WL_EGL_TIZEN_VERSION_MINOR	1
%define WL_EGL_TIZEN_VERSION_PATCH	1
%define WL_EGL_TIZEN_VERSION		%{WL_EGL_TIZEN_VERSION_MAJOR}.%{WL_EGL_TIZEN_VERSION_MINOR}.%{WL_EGL_TIZEN_VERSION_PATCH}

#TPL WINDOW SYSTEM CHECK
%if "%{TPL_WINSYS}" != "DRI2" && "%{TPL_WINSYS}" != "DRI3" && "%{TPL_WINSYS}" != "WL"
BuildRequires:		ERROR(No_window_system_designated)
%endif

Name:		libtpl-egl
Version:	%{TPL_VERSION}
Release:	0
%if "%{TPL_WINSYS}" == "DRI2"
Summary:	Tizen Porting Layer for EGL (DRI2 backend)
%endif
%if "%{TPL_WINSYS}" == "DRI3"
Summary:	Tizen Porting Layer for EGL (DRI3 backend)
%endif
%if "%{TPL_WINSYS}" == "WL"
Summary:	Tizen Porting Layer for EGL (Wayland backend)
%endif
Group: Graphics & UI Framework/GL
License:	MIT
Source:		%{name}-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:	pkg-config
BuildRequires:	pkgconfig(libtbm)

%if "%{TPL_WINSYS}" == "DRI2" || "%{TPL_WINSYS}" == "DRI3"
BuildRequires:	pkgconfig(libdri2)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(x11-xcb)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(xcb-dri3)
BuildRequires:	pkgconfig(xcb-sync)
BuildRequires:	pkgconfig(xcb-present)
BuildRequires:	pkgconfig(xshmfence)
BuildRequires:	pkgconfig(libdrm)
%endif

%if "%{TPL_WINSYS}" == "WL"
BuildRequires:  libtool
BuildRequires:	pkgconfig(libtdm-client)
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(wayland-server)
BuildRequires:	pkgconfig(wayland-egl)
BuildRequires:	pkgconfig(wayland-egl-backend)
BuildRequires:	pkgconfig(wayland-tbm-client)
BuildRequires:	pkgconfig(wayland-tbm-server)
BuildRequires:	pkgconfig(glib-2.0)
%if "%{ENABLE_TIZEN_FEATURE}" == "1"
BuildRequires:	pkgconfig(tizen-surface-client)
BuildRequires:  pkgconfig(presentation-time-client)
BuildRequires:  pkgconfig(linux-explicit-synchronization-unstable-v1-client)
%endif

%endif

%if "%{ENABLE_TTRACE}" == "1"
BuildRequires: pkgconfig(ttrace)
%endif

%if "%{ENABLE_DLOG}" == "1"
BuildRequires:	pkgconfig(dlog)
%endif

%global TZ_SYS_RO_SHARE  %{?TZ_SYS_RO_SHARE:%TZ_SYS_RO_SHARE}%{!?TZ_SYS_RO_SHARE:/usr/share}

%description
Tizen Porting Layer (a.k.a TPL) is a linkage between the underlying window
system and the EGL porting layer.

The following window systems are supported:
- X11 DRI2/DRI3
- Wayland

%package devel
Summary:	Development files for TPL
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the development libraries and header files needed by
the GPU Vendor DDK's EGL.

%if "%{TPL_WINSYS}" == "WL"
%package -n libwayland-egl-tizen
Version:	%{WL_EGL_TIZEN_VERSION}
Release:	0
Summary:    Wayland EGL TIZEN backend
BuildRequires:	pkgconfig(dlog)

%description -n libwayland-egl-tizen
This package provides tizen specific extension of wayland-egl.

%package -n libwayland-egl-tizen-devel
Version:	%{WL_EGL_TIZEN_VERSION}
Release:	0
Summary:    Development header files for wayland-egl tizen extensions.
Requires:	libwayland-egl libwayland-egl-tizen

%description -n libwayland-egl-tizen-devel
Development header files for wayland-egl tizen extensions.
%endif

%if %{with utest} || "%{ENABLE_TPL_TEST}" == "1"
%package    utest
Summary:    Unit test module of libtpl-egl
BuildRequires:  gtest-devel

%description utest
Unit test module of libtpl-egl (previously known as tpl-test)
%endif

%prep
%setup -q

%build
export TPL_VERSION_MAJOR=%{TPL_VERSION_MAJOR}
export TPL_VERSION_MINOR=%{TPL_VERSION_MINOR}
export TPL_VERSION_PATCH=%{TPL_VERSION_PATCH}

export WL_EGL_TIZEN_VERSION_MAJOR=%{WL_EGL_TIZEN_VERSION_MAJOR}
export WL_EGL_TIZEN_VERSION_MINOR=%{WL_EGL_TIZEN_VERSION_MINOR}
export WL_EGL_TIZEN_VERSION_PATCH=%{WL_EGL_TIZEN_VERSION_PATCH}

%reconfigure	\
%ifarch aarch64
	--with-arch=aarch64	\
%endif
%if "%{TPL_WINSYS}" == "WL"
	--with-wayland=yes	\
	--enable-wayland-thread=%{ENABLE_DEFAULT_WL_THREAD}	\
%endif
%if %{with utest} || "%{ENABLE_TPL_TEST}" == "1"
	--with-utest=yes	\
%if %{with utest_gcov} || "%{ENABLE_TPL_TEST_GCOV}" == "1"
	--enable-gcov=yes	\
%endif
%endif
	--enable-dlog=%{ENABLE_DLOG}							\
	--enable-dlog-default=%{ENABLE_DEFAULT_LOG}				\
	--enable-dump=%{ENABLE_DEFAULT_DUMP}					\
	--enable-object-hash-check=%{ENABLE_OBJECT_HASH_CHECK}	\
	--enable-ttrace=%{ENABLE_TTRACE}						\
	--enable-tizen-feature=%{ENABLE_TIZEN_FEATURE}			\
	LIBDIR=%{_libdir} \
	INCLUDEDIR=%{_includedir}

make %{?_smp_mflags}

%install
rm -fr %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%if "%{TPL_WINSYS}" == "WL"
%post	-n libwayland-egl-tizen -p /sbin/ldconfig
%postun	-n libwayland-egl-tizen -p /sbin/ldconfig
%endif

%files
%manifest packaging/libtpl-egl.manifest
%license COPYING
%defattr(-,root,root,-)
%{_libdir}/libtpl-egl.so.%{TPL_VERSION_MAJOR}
%{_libdir}/libtpl-egl.so.%{TPL_VERSION}

%files devel
%defattr(-,root,root,-)
%{_includedir}/tpl.h
%{_libdir}/pkgconfig/tpl-egl.pc
%{_libdir}/libtpl-egl.so

%if "%{TPL_WINSYS}" == "WL"
%files -n libwayland-egl-tizen
%manifest packaging/libwayland-egl-tizen.manifest
%license COPYING
%defattr(-,root,root,-)
%{_libdir}/libwayland-egl-tizen.so*

%files -n libwayland-egl-tizen-devel
%defattr(-,root,root,-)
%{_includedir}/wayland-egl-tizen.h
%{_libdir}/libwayland-egl-tizen.so
%{_libdir}/pkgconfig/wayland-egl-tizen.pc
%endif

%if %{with utest} || "%{ENABLE_TPL_TEST}" == "1"
%files utest
%defattr(-,root,root,-)
%{_bindir}/tpl-test
%endif
