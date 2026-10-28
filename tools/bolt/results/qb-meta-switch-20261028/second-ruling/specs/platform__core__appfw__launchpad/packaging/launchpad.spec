Name:       launchpad
Summary:    Launchpad for launching applications
Version:    0.51.7
Release:    1
Group:      Application Framework/Daemons
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source101:  launchpad-process-pool.service
Source102:  launchpad-process-pool.socket
Source1001: %{name}.manifest
Source1002: lib%{name}.manifest
Source1003: %{name}-loader.manifest
Source1004: app-defined-loader.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(buxton2)
BuildRequires:  pkgconfig(capi-system-resource)
BuildRequires:  pkgconfig(cynara-uid)
BuildRequires:  pkgconfig(dali2-adaptor)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(dlog-redirect-stdout)
BuildRequires:  pkgconfig(ecore)
BuildRequires:  pkgconfig(elementary)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(iniparser)
BuildRequires:  pkgconfig(libcap)
%if "%{?dev_wos}" != "1"
BuildRequires: pkgconfig(libsmack)
%endif
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(parcel)
BuildRequires:  pkgconfig(pkgmgr-installer)
BuildRequires:  pkgconfig(security-manager)
BuildRequires:  pkgconfig(tanchor-runtime)
BuildRequires:  pkgconfig(tizen-shared-queue)
BuildRequires:  pkgconfig(ttrace)
BuildRequires:  pkgconfig(vconf)

BuildRequires:  dali2-integration-devel
BuildRequires:  dali2-adaptor-integration-devel

Requires(post): /sbin/ldconfig
Requires(post): /usr/bin/systemctl
Requires(postun): /sbin/ldconfig
Requires(postun): /usr/bin/systemctl
Requires(preun): /usr/bin/systemctl
Requires(posttrans): /usr/bin/echo
Requires(posttrans): /usr/bin/sed

Provides: app-launchpad

%define tizen_feature_priority_change 0
%ifarch armv7l i686 i586
%define tizen_arch32 1
%else
%define tizen_arch32 0
%endif

%ifarch x86_64 i686 i586
%define tizen_emulator 1
%else
%define tizen_emulator 0
%endif

%if "%{?_prelink_enable}" == "y"
%define tizen_feature_prelink 1
%else
%define tizen_feature_prelink 0
%endif

%global real_crate_name rust_lux
%global rustc_edition 2021

%description
Launchpad for launching applications

%package devel
Summary:    Launchpad for launching applications (devel)
Group:      Development/Libraries
Requires:   liblaunchpad = %{version}-%{release}

%description devel
Launchpad for launching applications (devel)

%package -n launchpad-loader
Summary:    Launchpad-Loader for launching applications
Group:      Application Framework/Application Launcher

%description -n launchpad-loader
Launchpad-Loader for launching applications

%package -n app-defined-loader
Summary:    App-Defined-Loader for launching applications
Group:      Application Framework/Application Launcher

%description -n app-defined-loader
App-Defined-Loader for launching applications

%package -n liblaunchpad
Summary:    Launchpad library
Group:      Development/Libraries

%description -n liblaunchpad
Launchpad library

%package -n liblaunchpad-devel
Summary:    Launchpad library (devel)
Group:      Development/Libraries
Requires:   liblaunchpad = %{version}-%{release}

%description -n liblaunchpad-devel
Launchpad library (devel)

%package unittests
Summary:    %{name} unittests binary

%description unittests
unittests binary

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .
cp %{SOURCE1003} .
cp %{SOURCE1004} .

%build
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif
%if 0%{?tizen_feature_priority_change}
_TIZEN_FEATURE_PRIORITY_CHANGE=ON
%endif
%if 0%{?tizen_arch32}
_TIZEN_FEATURE_SET_PERSONALITY_32=ON
%else
_TIZEN_FEATURE_LOADER_ARCH64=ON
%endif
%if 0%{?tizen_feature_prelink}
_TIZEN_FEATURE_PRELINK=ON
%endif

%if 0%{?tizen_emulator}
HW_LOADER_THREADS=7
%else
HW_LOADER_THREADS=8
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake -DVERSION=%{version} \
	-DMAJORVER=${MAJORVER} \
	-DHW_LOADER_THREADS=${HW_LOADER_THREADS} \
	-D_TIZEN_FEATURE_PRIORITY_CHANGE:BOOL=${_TIZEN_FEATURE_PRIORITY_CHANGE} \
	-D_TIZEN_FEATURE_SET_PERSONALITY_32:BOOL=${_TIZEN_FEATURE_SET_PERSONALITY_32} \
	-D_TIZEN_FEATURE_PRELINK:BOOL=${_TIZEN_FEATURE_PRELINK} \
	-D_TIZEN_FEATURE_LOADER_ARCH64:BOOL=${_TIZEN_FEATURE_LOADER_ARCH64} \
%if 0%{?asan} != 1
	-DASAN_ENABLED=FALSE \
%else
	-DASAN_ENABLED=TRUE \
%endif
	-DTIZEN_FEATURE_SMACK_DISABLE:BOOL=%{?dev_wos:ON}%{!?dev_wos:OFF} \
	.
%__make %{?_smp_mflags}

%check
export LD_LIBRARY_PATH="../../src/lib/launchpad-common/:../../src/lib/launchpad-core"
ctest --verbose %{?_smp_mflags}

%install
rm -rf %{buildroot}

%make_install
mkdir -p %{buildroot}%{_userunitdir}/basic.target.wants
mkdir -p %{buildroot}%{_userunitdir}/sockets.target.wants
install -m 0644 %SOURCE101 %{buildroot}%{_userunitdir}/launchpad-process-pool.service
install -m 0644 %SOURCE102 %{buildroot}%{_userunitdir}/launchpad-process-pool.socket
ln -sf ../launchpad-process-pool.socket %{buildroot}%{_userunitdir}/sockets.target.wants/launchpad-process-pool.socket
ln -sf ../launchpad-process-pool.service %{buildroot}%{_userunitdir}/basic.target.wants/launchpad-process-pool.service

%post
ln -sf /usr/bin/false /usr/bin/process-pool

%posttrans
if [ -f %{_unitdir_user}/enlightenment-user.service ]; then
  echo "enlightenment-user.service exists";
else
  echo "enlightenment-user.service does not exist";
  sed -i 's/Requires=enlightenment-user.service//' %{_unitdir_user}/launchpad-process-pool.service;
  sed -i 's/After=enlightenment-user.service//' %{_unitdir_user}/launchpad-process-pool.service;
fi

%files
%manifest launchpad.manifest
%license LICENSE
%{_prefix}/share/aul/default.debugger
%{_userunitdir}/launchpad-process-pool.service
%{_userunitdir}/launchpad-process-pool.socket
%{_userunitdir}/sockets.target.wants/launchpad-process-pool.socket
%{_userunitdir}/basic.target.wants/launchpad-process-pool.service
%{_bindir}/launchpad-process-pool
%{_prefix}/share/aul/launchpad.conf
%{_sysconfdir}/package-manager/parserlib/liblaunchpad-parser.so
%{_datadir}/parser-plugins/*
%attr(0644,root,root) %{_libdir}/liblaunchpad-common.so.*
%attr(0644,root,root) %{_libdir}/liblaunchpad-core.so.*

%files devel
%{_includedir}/launchpad/*.h
%{_includedir}/launchpad-common/*.hh
%{_includedir}/launchpad-core/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/launchpad.pc
%attr(0644,root,root) %{_libdir}/liblaunchpad-common.so
%{_libdir}/pkgconfig/liblaunchpad-common.pc
%attr(0644,root,root) %{_libdir}/liblaunchpad-core.so
%{_libdir}/pkgconfig/liblaunchpad-core.pc

%files -n launchpad-loader
%manifest launchpad-loader.manifest
%license LICENSE
%{_bindir}/launchpad-loader

%files -n app-defined-loader
%manifest app-defined-loader.manifest
%license LICENSE
%{_prefix}/share/aul/app-defined-loader.conf
%{_bindir}/app-defined-loader

%files -n liblaunchpad
%manifest liblaunchpad.manifest
%license LICENSE
%attr(0644,root,root) %{_libdir}/liblaunchpad.so.*
%attr(0644,root,root) %{_libdir}/liblaunchpad-hydra.so.*

%files -n liblaunchpad-devel
%{_includedir}/launchpad/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/liblaunchpad.pc
%{_libdir}/pkgconfig/liblaunchpad-hydra.pc

%files unittests
%{_bindir}/launchpad-process-pool-unittest
