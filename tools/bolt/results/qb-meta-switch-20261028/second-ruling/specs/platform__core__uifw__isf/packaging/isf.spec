%global __provides_exclude_from ^(.*\\.(wearable|tv|mobile|ivi))$

%bcond_with wayland

# BUILD_TCORE_ENABLE: 0 (default) = EFL, 1 = Tcore (disable EFL dependencies).
# Example: gbs build ... --define "BUILD_TCORE_ENABLE 1"
%{!?BUILD_TCORE_ENABLE:%global BUILD_TCORE_ENABLE 0}
%if "%{BUILD_TCORE_ENABLE}" != "0" && "%{BUILD_TCORE_ENABLE}" != "1"
%{error:BUILD_TCORE_ENABLE must be 0 or 1}
%endif

Name:       isf
Summary:    Input Service Framework
Version:    11.1.36
Release:    1
Group:      Graphics & UI Framework/Input
License:    LGPL-2.1+
Source0:    %{name}-%{version}.tar.gz
Source100:  %{name}.conf
Source200:  engine-loader.service
Source300:  org.tizen.engine-loader.service
Source400:  engine-loader.conf
BuildRequires:  gettext-tools
BuildRequires:  pkgconfig(dali2-adaptor)
BuildRequires:  dali2-adaptor-integration-devel
BuildRequires:  pkgconfig(dali2-ui-foundation)
BuildRequires:  pkgconfig(dali2-ui-components)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(xkbcommon) >= 0.3.0
BuildRequires:  pkgconfig(text-client)
BuildRequires:  pkgconfig(input-method-client)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(capi-appfw-app-control)
BuildRequires:  pkgconfig(capi-appfw-app-common)
BuildRequires:  pkgconfig(capi-appfw-service-application)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-creds-socket)
BuildRequires:  pkgconfig(cynara-session)
BuildRequires:  pkgconfig(capi-appfw-package-manager)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(capi-system-resource)
BuildRequires:  pkgconfig(capi-appfw-preference)
BuildRequires:  pkgconfig(capi-appfw-app-manager)
BuildRequires:  pkgconfig(tizen-core)
BuildRequires:  pkgconfig(tizen-core-wl)
BuildRequires:  pkgconfig(tizen-core-imf)
%if "%{BUILD_TCORE_ENABLE}" == "0"
BuildRequires:  pkgconfig(ecore-wl2)
BuildRequires:  pkgconfig(eina)
BuildRequires:  pkgconfig(ecore)
BuildRequires:  pkgconfig(evas)
BuildRequires:  pkgconfig(ecore-imf)
BuildRequires:  pkgconfig(ecore-input)
BuildRequires:  pkgconfig(ecore-evas)
BuildRequires:  pkgconfig(ecore-ipc)
BuildRequires:  pkgconfig(edje)
%endif
%if "%{BUILD_TCORE_ENABLE}" == "0"
Requires:       isf-ecore-imf-immodule = %{version}-%{release}
%endif
Requires(postun): /sbin/ldconfig

%description
Input Service Framewok (ISF) is an input method (IM) platform, and it has been derived from SCIM.


%package devel
Summary:    ISF header files
Requires:   %{name} = %{version}-%{release}
Requires:   pkgconfig(tizen-core-imf)

%description devel
This package contains ISF header files for ISE development.

%package -n isf-ecore-imf-immodule
Summary: Wayland input method module for ISF
Group: Graphics & UI Framework/Input
License: LGPL-2.1+
Requires: %{name} = %{version}-%{release}
Requires: ecore-imf

%description -n isf-ecore-imf-immodule
Wayland input method module for Ecore IMF.

%package -n isf-i18n
Summary: Internationalization files for ISF
Group: Graphics & UI Framework/Input
License: LGPL-2.1+
Requires: %{name} = %{version}-%{release}

%description -n isf-i18n
Internationalization files for Input Service Framework (ISF)

%package -n ise-engine-loader
Summary: ISE engine loader
Group: Graphics & UI Framework/Input
License: LGPL-2.1+
Requires: %{name} = %{version}-%{release}

%description -n ise-engine-loader
ISE Engine loader

%package -n isf-tests
Summary: ISF demo and test tools
Group: Graphics & UI Framework/Input
License: LGPL-2.1+
Requires: %{name} = %{version}-%{release}

%description -n isf-tests
This package contains the ISF demo application (isf-demo-dali)
and unit test binary (isf-tests) for testing the Input Service
Framework.

%prep
%setup -q
cp %{SOURCE300} .

%build
CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%if %{with wayland}
CFLAGS="$CFLAGS -DWAYLAND"
CXXFLAGS="$CXXFLAGS -DWAYLAND"
%endif

%{?_toolchain:
%if %{toolchain_is clang}
CFLAGS="$CFLAGS -Wno-error=return-type-c-linkage"
CXXFLAGS="$CXXFLAGS -Wno-error=return-type-c-linkage"
%endif
}

export GC_SECTIONS_FLAGS="-fdata-sections -ffunction-sections -Wl,--gc-sections"
CFLAGS="$CFLAGS -fvisibility=hidden ${GC_SECTIONS_FLAGS} -Werror"
CXXFLAGS="$CXXFLAGS -fvisibility=hidden -fvisibility-inlines-hidden ${GC_SECTIONS_FLAGS} -Werror"
export CFLAGS_BASIS="$CFLAGS"
export CXXFLAGS_BASIS="$CXXFLAGS"

%autogen
%configure --disable-static \
		--disable-tray-icon \
		--disable-filter-sctc \
%if "%{BUILD_TCORE_ENABLE}" == "1"
        --enable-tcore \
        --disable-efl-immodule \
        --disable-wayland-immodule \
        --disable-panel-efl \
%else
%if %{with wayland}
        --disable-efl-immodule \
%endif
%endif
		--disable-frontend-x11 \
		--disable-multiwindow-support \
		--disable-ime-embed-app \
		--with-ro-app-dir=%{TZ_SYS_RO_APP} \
		--with-ro-packages-dir=%{TZ_SYS_RO_PACKAGES} \
		--enable-remote-input
make %{?_smp_mflags}

%check
%if "%{BUILD_TCORE_ENABLE}" == "1"
# Skip make check when tcore backend is enabled (EFL-dependent tests excluded)
make check || true
%else
make check
%endif

%install
rm -rf %{buildroot}

%make_install
mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 0644 %SOURCE100 %{buildroot}%{_tmpfilesdir}/%{name}.conf

mkdir -p %{buildroot}/%{TZ_SYS_ETC}/dump.d/module.d
cp -af ism/dump/isf_log_dump.sh %{buildroot}/%{TZ_SYS_ETC}/dump.d/module.d
mkdir -p %{buildroot}/etc/scim/conf
mkdir -p %{buildroot}/usr/share/upgrade/scripts/

mkdir -p %{buildroot}%{_prefix}/lib/systemd/system
install -m 0644 %SOURCE200 %{buildroot}%{_unitdir}/engine-loader.service

mkdir -p %{buildroot}%{_datadir}/dbus-1/system-services
install -m 0644 %SOURCE300 %{buildroot}%{_datadir}/dbus-1/system-services/org.tizen.engine-loader.service

mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
install -m 0644 %SOURCE400 %{buildroot}%{_sysconfdir}/dbus-1/system.d/engine-loader.conf

%if "%{BUILD_TCORE_ENABLE}" == "0"
ln -sf %{_bindir}/isf %{buildroot}%{_bindir}/isf-panel-efl
%endif

%find_lang scim

cat scim.lang > isf.lang
%post
/sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%dir /etc/scim/conf
%attr(644,root,root) %{_sysconfdir}/profile.d/isf.sh
%{_sysconfdir}/scim/global
%{_sysconfdir}/scim/config
%{_datadir}/scim/icons/*
%if "%{BUILD_TCORE_ENABLE}" == "0"
%{_bindir}/isf
%{_bindir}/isf-panel-efl
%endif
%{_libdir}/tcore_imf/modules/*/*.so
%{_libdir}/scim-1.0/1.4.0/IMEngine/socket.so
%{_libdir}/scim-1.0/1.4.0/PanelAgent/*.so
%{_libdir}/scim-1.0/1.4.0/Config/simple.so
%{_libdir}/scim-1.0/1.4.0/Config/socket.so
%{_libdir}/scim-1.0/1.4.0/FrontEnd/*.so
%{_libdir}/scim-1.0/scim-helper-launcher
%{_libdir}/libscim-*.so.*
%{_libdir}/libisf-control.so.*
%{_libdir}/libscim_imengine.so.*
%license COPYING
%{TZ_SYS_ETC}/dump.d/module.d/*
%{_tmpfilesdir}/%{name}.conf

%if "%{BUILD_TCORE_ENABLE}" == "0"
%files -n isf-ecore-imf-immodule
%license COPYING
%defattr(-,root,root,-)
%{_libdir}/ecore_imf/modules/wayland/*/*.so
%endif

%files -n isf-i18n
%defattr(-,root,root,-)
%{_datadir}/locale/*/LC_MESSAGES/scim.mo

%files devel
%defattr(-,root,root,-)
%{_includedir}/scim-1.0/*
%{_libdir}/libscim-*.so
%{_includedir}/isf-control/*
%{_includedir}/scim_imengine/*
%{_libdir}/libisf-control.so
%{_libdir}/libscim_imengine.so
%{_libdir}/pkgconfig/isf.pc
%{_libdir}/pkgconfig/scim.pc
%{_libdir}/pkgconfig/isf-control.pc

%files -n ise-engine-loader
%manifest ise-engine-loader.manifest
%license engine-loader/LICENSE
%attr(0755,ui_fw,ui_fw) %{_bindir}/ise-engine-loader
%attr(0644,root,root) %{_unitdir}/engine-loader.service
%attr(0644,root,root) %{_datadir}/dbus-1/system-services/org.tizen.engine-loader.service
%config %{_sysconfdir}/dbus-1/system.d/engine-loader.conf

%files -n isf-tests
%manifest isf-tests.manifest
%license COPYING
%defattr(-,root,root,-)
%{_bindir}/isf-demo-dali
%{_bindir}/isf-tests
