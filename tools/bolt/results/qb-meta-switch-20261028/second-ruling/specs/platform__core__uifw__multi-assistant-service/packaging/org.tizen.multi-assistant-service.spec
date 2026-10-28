Name:		org.tizen.multi-assistant-service
Summary:	Multi assistant service
Version:	0.3.43
Release:	1
Group:		Graphics & UI Framework/Voice Framework
License:	Flora-1.1 and MIT
Source:		%{name}-%{version}.tar.gz
Source1001:	%{name}.manifest

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires: pkgconfig(capi-appfw-package-manager)
BuildRequires: pkgconfig(capi-appfw-service-application)
BuildRequires: pkgconfig(capi-appfw-preference)
BuildRequires: pkgconfig(capi-media-audio-io)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(ecore)
BuildRequires: pkgconfig(capi-message-port)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(multi-assistant)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(pkgmgr-info)
BuildRequires: pkgconfig(jsoncpp)
BuildRequires: boost-devel
%if %{defined _test_type}
BuildRequires:  gtest-devel
%endif
BuildRequires: boost-system
BuildRequires: boost-thread
BuildRequires: cmake


%description
org.tizen.multi-assistant-service (application)

%define _usrdir	/usr
#%define _appdir	%{_usrdir}/apps/org.tizen.multi-assistant-service/
%define _appdir	%{TZ_SYS_RO_APP}/%{name}
%define _appbindir %{_appdir}/bin/

%prep
%setup -q
cp %{SOURCE1001} .

cat LICENSE.Flora LICENSE.MIT > LICENSE.merge
cp LICENSE.merge LICENSE
rm LICENSE.merge

%build
LDFLAGS="$LDFLAGS -Wl,-z -Wl,nodelete"
%if 0%{?sec_build_binary_debug_enable}
	export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
	export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
	export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif

export CFLAGS+=" -Wno-format-truncation -Wno-stringop-truncation -Wno-format-overflow -Wno-stringop-overflow"
export CXXFLAGS+=" -Wno-format-truncation -Wno-stringop-truncation -Wno-format-overflow -Wno-stringop-overflow"

export LDFLAGS
%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_appdir} \
	-DTZ_SYS_RO_SHARE=%TZ_SYS_RO_SHARE \
%if %{defined _test_type}
	-DTEST_TYPE="%{_test_type}" \
%else
	-DTEST_TYPE="none" \
%endif
%if "%{?profile}" == "tv"
	-DUSE_TRUSTED_MESSAGE_PORT="1" \
%else
	-DUSE_TRUSTED_MESSAGE_PORT="0" \
%endif

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

%make_install
%if "%{?profile}" == "tv"
install -m 0644 signatures/tv/author-signature.xml "%{buildroot}"/%{TZ_SYS_RO_APP}/%{name}
install -m 0644 signatures/tv/signature1.xml "%{buildroot}"%{TZ_SYS_RO_APP}/%{name}
%endif

%check
%if "%{_ctest_enable}" == "true"
ctest --output-on-failure %{?_smp_mflags}
%endif

%post
mkdir -p %{_appbindir}
mkdir -p %{_libdir}/multiassistant/ma/1.0/engine

/sbin/ldconfig
exit 0

%postun
/sbin/ldconfig
exit 0

# INITIALIZE VCONF ------------------------------------------------------------

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
/usr/share/packages/org.tizen.multi-assistant-service.xml
%{TZ_SYS_RO_SHARE}/multiassistant/libma-dependency-default.so
%{TZ_SYS_RO_APP}/%{name}/*
#%{_appdir}/lib/*
%{_appdir}/bin/*
#%defattr(-,app,app,-)
#%{_appbindir}/org.tizen.multi-assistant-service
%license LICENSE
