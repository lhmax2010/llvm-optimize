Name:       libmm-player
Summary:    Multimedia Framework Player Library
Version:    1.1.16
Release:    0
Group:      Multimedia/Libraries
License:    Apache-2.0
URL:        http://source.tizen.org
Source0:    %{name}-%{version}.tar.gz
Source1001:     libmm-player.manifest
Requires(post):  /sbin/ldconfig
Requires(postun):  /sbin/ldconfig
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(mm-common)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(gstreamer-app-1.0)
BuildRequires:  pkgconfig(mmutil-common)
BuildRequires:  pkgconfig(iniparser)
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(capi-media-tool)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(resource-manager)
BuildRequires:  pkgconfig(resource-center-api)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(storage)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(capi-media-sound-manager)
BuildRequires:  pkgconfig(libtbm)
%if "%{gtests}" == "1"
BuildRequires:  pkgconfig(gmock)
%endif

%description
Multimedia Framework Player Library files.

%package devel
Summary:    Multimedia Framework Player Library (DEV)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Multimedia Framework Player Library files (DEV).

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="$CFLAGS -Wall -DTIZEN_DEBUG -D_FILE_OFFSET_BITS=64 -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\" -DEXPORT_API=\"__attribute__((visibility(\\\"default\\\")))\" "
export CFLAGS="$CFLAGS -DPATH_LIBDIR=\\\"%{_libdir}\\\""

%if %{with x}
export CFLAGS="$CFLAGS -DHAVE_X11"
%endif

LDFLAGS="$LDFLAGS -Wl,--rpath=%{_prefix}/lib -Wl,--hash-style=both -Wl,--as-needed"; export LDFLAGS

%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

./autogen.sh
# always enable sdk build. This option should go away
#CFLAGS=$CFLAGS LDFLAGS=$LDFLAGS ./configure --enable-sdk --prefix=%{_prefix} --disable-static
%configure \
%if "%{gtests}" == "1"
--enable-tests \
%endif
--enable-rm-common \
--disable-static

#%__make -j1
make %{?jobs:-j%jobs}

%install
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%if "%{gtests}" == "1"
%{_bindir}/gtest-libmm-player
%endif

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/mmf/*.h
%{_libdir}/pkgconfig/*
