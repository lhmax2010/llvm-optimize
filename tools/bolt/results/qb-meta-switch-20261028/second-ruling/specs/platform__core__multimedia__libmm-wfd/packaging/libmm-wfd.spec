Name:       libmm-wfd
Summary:    Multimedia Framework Wifi-Display Library
Version:    0.4.12
Release:    0
Group:      System/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Requires(post):  /sbin/ldconfig
Requires(postun):  /sbin/ldconfig
BuildRequires: pkgconfig(mm-common)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gstreamer-1.0)
BuildRequires: pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires: pkgconfig(gstreamer-video-1.0)
BuildRequires: pkgconfig(gstreamer-app-1.0)
BuildRequires: pkgconfig(iniparser)
BuildRequires: pkgconfig(capi-network-wifi-direct)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(libtbm)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(resource-manager)
BuildRequires: pkgconfig(resource-center-api)
BuildRequires: pkgconfig(mm-display-interface)
%if 0%{?gtests:1}
BuildRequires:  pkgconfig(gmock)
%endif

BuildRoot:  %{_tmppath}/%{name}-%{version}-build

%description
A Wfd library in Tizen native API

%package devel
Summary:    Multimedia Framework Wifi-Display Library (DEV)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development related files for a wfd library in Tizen native API

%package factory
Summary:    Multimedia Framework Wifi-Display Library (Factory)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
%description factory

%prep
%setup -q

%build
export CFLAGS="$CFLAGS -Wextra -Wno-array-bounds"
export CFLAGS="$CFLAGS -Wno-ignored-qualifiers -Wno-unused-parameter -Wshadow"
export CFLAGS="$CFLAGS -Wwrite-strings -Wswitch-default"
export CFLAGS="$CFLAGS -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""
./autogen.sh

CFLAGS="$CFLAGS -DMMFW_DEBUG_MODE -DEXPORT_API=\"__attribute__((visibility(\\\"default\\\")))\" "; export CFLAGS
LDFLAGS="$LDFLAGS -Wl,--rpath=%{_prefix}/lib -Wl,--hash-style=both -Wl,--as-needed"; export LDFLAGS

# always enable sdk build. This option should go away
#  --enable-wfd-sink-uibc
%configure \
%if 0%{?gtests:1}
--enable-tests \
%endif
--disable-static

# Call make instruction with smp support
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

%make_install
mkdir -p %{buildroot}/%{TZ_SYS_RO_SHARE}/dbus-1/services/

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%manifest libmm-wfd.manifest
%license LICENSE.APLv2.0
%if 0%{?gtests:1}
%{_bindir}/gtest-libmm-wfd
%endif

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/mmf/mm_wfd_sink.h
%{_includedir}/mmf/mm_wfd_sink_config.h
%{_includedir}/mmf/mm_wfd_sink_priv.h
%{_includedir}/mmf/mm_wfd_sink_dlog.h
%{_includedir}/mmf/mm_wfd_sink_util.h
%{_includedir}/mmf/mm_wfd_sink_ini.h
%{_includedir}/mmf/mm_wfd_sink_attrs.h
%{_includedir}/mmf/mm_wfd_sink_enum.h
%{_libdir}/pkgconfig/*

#%files factory
#%defattr(-,root,root,-)
#%{_includedir}/mmf/mm_player_factory.h
