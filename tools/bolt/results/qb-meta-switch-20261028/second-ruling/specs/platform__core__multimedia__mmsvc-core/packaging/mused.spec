Name:       mused
Summary:    A multimedia daemon
Version:    0.6.1
Release:    0
Group:      System/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    muse-server.service
Source2:    gtest.input
Source3:    muse-server-vd_product_touch-interactive.service
Source4:    muse-server-vd_product_tv.service
Source5:    muse-server-vd_product_audio.service
Source6:    muse-server.socket
Source7:    muse-server.path
Source8:    muse-server-vd_product_ltv.service
Source9:    muse-server_touch-interactive.path
Source10:   muse-server.notstrip
BuildRequires: cmake
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(capi-system-runtime-info)
BuildRequires: pkgconfig(cynara-client)
BuildRequires: pkgconfig(cynara-creds-socket)
BuildRequires: pkgconfig(cynara-session)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gmodule-2.0)
BuildRequires: pkgconfig(gstreamer-1.0)
BuildRequires: pkgconfig(gstreamer-base-1.0)
BuildRequires: pkgconfig(iniparser)
BuildRequires: pkgconfig(json-c)
BuildRequires: pkgconfig(libtbm)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(mm-common)
BuildRequires: pkgconfig(capi-system-resource)
%if "%{tizen_profile_name}" == "tv"
BuildRequires: pkgconfig(libresourced)
BuildRequires: pkgconfig(lwipc)
BuildRequires: pkgconfig(ttrace)
%else
BuildRequires: pkgconfig(storage)
%endif
%if 0%{?gtests:1}
BuildRequires: pkgconfig(gmock)
%endif

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: security-config

%description


%package devel
Summary:  A Media Daemon library in Tizen (Development)
Group:    Multimedia/Service
Requires: %{name} = %{version}-%{release}
%description devel

%package isu
Summary: muse server ISU pacakge
Group:   Multimedia/Service
%description isu

%prep
%setup -q

%build
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
export CFLAGS="$CFLAGS -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""
export CXXFLAGS="$CXXFLAGS -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""

%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE -D_GNU_SOURCE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE -D_GNU_SOURCE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE -D_GNU_SOURCE"
%endif

%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage -DMUSE_GCOV_TEST "
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage -DMUSE_GCOV_TEST "
export LDFLAGS+=" -lgcov "
%endif

%if "%{tizen_profile_name}" != "tv"
export CFLAGS+=" -DMUSE_USE_POWER_OFF_STATE_CHANGE -DMUSE_USE_WATCHDOG -DMUSE_PUBLIC"
%endif

%cmake . -DCMAKE_INSTALL_PREFIX=/usr -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DLIBDIR=%{_libdir} -DTZ_SYS_DATA=%TZ_SYS_DATA \
%if "%{tizen_profile_name}" == "tv"
-DMUSE_REGISTER_VIP=1 -DMUSE_TTRACE_ENABLE=1 -DMUSE_LWIPC_ENABLE=1 -DMUSE_BOOST_ENABLE=1 \
%if ("%{sec_buildconf_optimized_memory}" == "1")
-DMUSE_LW=1
%endif
%else
-DMUSE_GTESTS_BUILD=%{?gtests:1}%{!?gtests:0} -DMUSE_STORAGE_ENABLE=1
%endif

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

%make_install

%if ("%{sec_buildconf_optimized_memory}" == "1")
mkdir -p %{buildroot}%{_unitdir}/sockets.target.wants
install -m 0644 %SOURCE6 %{buildroot}%{_unitdir}/muse-server.socket
%install_service sockets.target.wants muse-server.socket
install -m 0644 %SOURCE8 %{buildroot}%{_unitdir}/muse-server.service
%else
%if ("%{sec_buildconf_ir_touch_detection_support}" == "1")
mkdir -p %{buildroot}%{_unitdir}/sysinit.target.wants
install -m 0644 %SOURCE3 %{buildroot}%{_unitdir}/muse-server.service
%install_service sysinit.target.wants muse-server.service
install -m 0644 %SOURCE9 %{buildroot}%{_unitdir}/muse-server.path
%install_service paths.target.wants muse-server.path
%else
%if ("%{_vd_cfg_product_type}" == "AUDIO")
mkdir -p %{buildroot}%{_unitdir}/stater.target.wants
install -m 0644 %SOURCE5 %{buildroot}%{_unitdir}/muse-server.service
%install_service starter.target.wants muse-server.service
mkdir -p %{buildroot}%{TZ_SYS_RO_ETC}/notstrip/
install -m 0444 %SOURCE10 %{buildroot}%{TZ_SYS_RO_ETC}/notstrip/muse-server.notstrip
%else
%if ("%{_vd_cfg_product_type}" == "TV") || ("%{_vd_cfg_product_type}" == "LFD") || ("%{_vd_cfg_product_type}" == "HTV") || ("%{_vd_cfg_product_type}" == "AV") || ("%{_vd_cfg_product_type}" == "IWB") || ("%{_vd_cfg_product_type}" == "WALL")
mkdir -p %{buildroot}%{_unitdir}/basic.target.wants
install -m 0644 %SOURCE4 %{buildroot}%{_unitdir}/muse-server.service
%install_service basic.target.wants muse-server.service
mkdir -p %{buildroot}%{TZ_SYS_RO_ETC}/notstrip/
install -m 0444 %SOURCE10 %{buildroot}%{TZ_SYS_RO_ETC}/notstrip/muse-server.notstrip
%else
mkdir -p %{buildroot}%{_unitdir}/paths.target.wants
install -m 0644 %SOURCE1 %{buildroot}%{_unitdir}/muse-server.service
install -m 0644 %SOURCE7 %{buildroot}%{_unitdir}/muse-server.path
%install_service paths.target.wants muse-server.path

%endif
%endif
%endif
%endif

mkdir -p %{buildroot}/var/log/%{name}
mkdir -p %{buildroot}%{TZ_SYS_DATA}/%{name}

%if 0%{?gtests:1}
install -m 0644 %SOURCE2 %{buildroot}%{TZ_SYS_DATA}/%{name}/gtest.input
%endif

%post
/sbin/ldconfig

chown multimedia_fw:multimedia_fw %{TZ_SYS_DATA}/%{name}
chown multimedia_fw:multimedia_fw /var/log/%{name}
chsmack -a "System::Shared" %{TZ_SYS_DATA}/%{name}
chsmack -a "System::Shared" /var/log/%{name}

%postun -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%{_libdir}/libmuse-*.so.*
%license LICENSE.APLv2
%{_unitdir}/muse-server.service
%if ("%{sec_buildconf_optimized_memory}" == "1")
%{_unitdir}/muse-server.socket
%{_unitdir}/sockets.target.wants/muse-server.socket
%else
%if ("%{sec_buildconf_ir_touch_detection_support}" == "1")
%{_unitdir}/sysinit.target.wants/muse-server.service
%{_unitdir}/paths.target.wants/muse-server.path
%{_unitdir}/muse-server.path
%else
%if ("%{_vd_cfg_product_type}" == "AUDIO")
%{_unitdir}/starter.target.wants/muse-server.service
%attr(0444, root, root) %{TZ_SYS_RO_ETC}/notstrip/muse-server.notstrip
%else
%if ("%{_vd_cfg_product_type}" == "TV") || ("%{_vd_cfg_product_type}" == "LFD") || ("%{_vd_cfg_product_type}" == "HTV") || ("%{_vd_cfg_product_type}" == "AV") || ("%{_vd_cfg_product_type}" == "IWB") || ("%{_vd_cfg_product_type}" == "WALL")
%{_unitdir}/basic.target.wants/muse-server.service
%attr(0444, root, root) %{TZ_SYS_RO_ETC}/notstrip/muse-server.notstrip
%else
%{_unitdir}/paths.target.wants/muse-server.path
%{_unitdir}/muse-server.path
%endif
%endif
%endif
%endif

%{TZ_SYS_DATA}/%{name}
/var/log/%{name}
%{_bindir}/*

%if 0%{?gtests:1}
%{TZ_SYS_DATA}/%{name}/gtest.input
%{_bindir}/gtest-muse-server
%endif

%files devel
%{_includedir}/media/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so

%files isu
/etc/isu/muse-server/isu.cfg
/etc/isu/muse-server/system-services/muse-server.service
