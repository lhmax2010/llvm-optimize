Name:       org.tizen.vc-engine-default
Summary:    Voice control default engine service app
Version:    1.90.1
Release:    1
Group:      Graphics & UI Framework/Voice Framework
License:    Flora-1.1 and Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

Autoreq:  no
BuildRequires:  cmake
BuildRequires:  pkgconfig(libtzplatform-config)
Requires:  appcore-agent
Requires:  aul
Requires:  bundle
Requires:  capi-appfw-app-common
Requires:  capi-appfw-app-control
Requires:  capi-base-common
Requires:  dbus-libs
Requires:  dlog
Requires:  ecore-core
Requires:  efl
Requires:  eina
Requires:  eo
Requires:  glibc
Requires:  libglib
Requires:  xdgmime
Requires:  voice-control
Requires:  vconf
Requires:  capi-machine-learning-inference

%description
Description: Voice control default engine service app

%prep
%setup -q
cp %{SOURCE1001} .

cat LICENSE LICENSE.APLv2 > LICENSE.merge
cp LICENSE.merge LICENSE
rm LICENSE.merge

%define APP_PREFIX %{TZ_SYS_RO_APP}/%{name}
%define MANIFESTDIR %{TZ_SYS_RO_PACKAGES}

cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DLIBDIR=%{_libdir} -DTZ_SYS_RO_SHARE=%TZ_SYS_RO_SHARE \
	-DAPP_INSTALL_PREFIX=%{APP_PREFIX} -DAPP_MANIFESTDIR=%{MANIFESTDIR}

%build
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%post
/sbin/ldconfig
exit 0

%postun
/sbin/ldconfig
exit 0

%files
%license LICENSE
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{APP_PREFIX}/bin/*
%{MANIFESTDIR}/org.tizen.vc-engine-default.xml
%ifarch %{arm} aarch64 # arm armv7l
%ifnarch riscv64
%{APP_PREFIX}/lib/*
%endif
%{APP_PREFIX}/shared/res/*
%else
%{TZ_SYS_RO_SHARE}/voice/vc/engine_data/*
%endif
#%{TZ_SYS_RO_SHARE}/voice/vc/1.0/engine/lib*.so

