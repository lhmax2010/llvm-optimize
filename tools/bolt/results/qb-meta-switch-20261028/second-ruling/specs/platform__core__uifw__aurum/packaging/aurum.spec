Name:           aurum
Version:        1.0.29
Release:        1
License:        Apache-2.0 and MIT
Summary:        Automation framework for Ui testing
Group:          UI Framework
Source:         %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  meson
BuildRequires:  pkgconfig(grpc)
BuildRequires:  pkgconfig(grpc++)

Requires:       at-spi2-core
BuildRequires:  at-spi2-core-devel

BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(tizen-core)
BuildRequires:  pkgconfig(tizen-core-wl)
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  pkgconfig(gmock)

BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(capi-appfw-package-manager)
BuildRequires: pkgconfig(capi-appfw-app-control)
BuildRequires: pkgconfig(capi-appfw-app-manager)
BuildRequires: pkgconfig(capi-appfw-service-application)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(capi-system-device)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(capi-system-system-settings)
BuildRequires: pkgconfig(capi-base-utils-i18n)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(zlib)

%if 0%{?gendoc:1}
BuildRequires:  doxygen
%endif

BuildRequires:  hash-signer
%if 0%{?sec_product_feature_profile_wearable}
Requires(post): signing-client
%endif

%description
aurum is a project for testing ui.
it provides interfaces through gRPC protocol.

%package devel
Summary: devel package for libaurum

%description devel
devel package for libaurum

%package bootstrap
Summary: bootstrap
License: Apache-2.0
Requires: %{name} = %{version}-%{release}
Requires: libgrpc

%description bootstrap
gRPC Server

%if 0%{?gendoc:1}
%package docs
Summary: documentation
License: Apache-2.0
Requires: %{name} = %{version}-%{release}
Requires: libgrpc

%description docs
documentations for aurum
%endif

%prep
%setup -q
cp %{SOURCE1001} .

%if "%{asan}" == "1"
%restore_fcommon
%else
export LDFLAGS="$LDFLAGS -Wl,-z,relro -Wl,-z,now -Wl,-z,noexecstack"
%endif

%if "%{build_uidump}" == "1"
%define BUILD_UIDUMP true
%else
%define BUILD_UIDUMP false
%endif

%if 0%{?gendoc:1}
%define TIZEN_GEN_DOC true
%else
%define TIZEN_GEN_DOC false
%endif

meson \
    --prefix /usr \
    --libdir %{_libdir} \
    -Dcpp_std=c++17 \
    -Dtizen=true \
    -Denable_documentation=%{TIZEN_GEN_DOC} \
    -Dtzapp_path=%{TZ_SYS_RO_APP} \
    -Dtzpackage_path=%{TZ_SYS_RO_PACKAGES} \
    -Dbuild_c_bindings=true \
    -Dbuild_uidump=%{BUILD_UIDUMP} \
    gbsbuild 2>&1 | sed \
        -e 's%^.*: error: .*$%\x1b[37;41m&\x1b[m%' \
        -e 's%^.*: warning: .*$%\x1b[30;43m&\x1b[m%'

%build

ninja \
    -C gbsbuild \
    -j %(echo "`/usr/bin/getconf _NPROCESSORS_ONLN`") \
    -v \
    all 2>&1 | sed \
        -e 's%^.*: error: .*$%\x1b[37;41m&\x1b[m%' \
        -e 's%^.*: warning: .*$%\x1b[30;43m&\x1b[m%'

#Enable below test if needed
#meson test \
#    -C gbsbuild \
#    -v

%install

%define tizen_sign 1
%define tizen_sign_base /usr/apps/org.tizen.aurum-bootstrap
%define tizen_sign_level platform
%define tizen_author_sign 1
%define tizen_dist_sign 1

export DESTDIR=%{buildroot}
ninja -C gbsbuild install

%post
sbin/ldconfig
%if "%{build_uidump}" == "1"
# aurum-uidump runs from a shell (not the app framework), so without this it
# inherits the caller's User::Shell label and is denied inputgenerator. Give it
# an exec-transition to System::Privileged (the label the privileged daemons
# run as) so it can read the a11y tree AND inject input. No-op if not built.
[ -x %{_bindir}/aurum-uidump ] && chsmack -e "System::Privileged" %{_bindir}/aurum-uidump >/dev/null 2>&1 || :
%endif

%postun
sbin/ldconfig

%post bootstrap
%if 0%{?sec_product_feature_profile_wearable}
echo "signing %{TZ_SYS_RO_APP}/org.tizen.aurum-bootstrap"
/usr/bin/signing-client/hash-signer-client.sh -a -d -p platform %{TZ_SYS_RO_APP}/org.tizen.aurum-bootstrap
%endif

%postun bootstrap
/sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{_libdir}/libaurum.so
%{_libdir}/libaurum.so.*
%{_libdir}/libpugixml.so
%{_libdir}/libpugixml.so.*
%{_libdir}/libaurumsharp.so
%{_libdir}/libaurumsharp.so.*
#%{_bindir}/test_c_bindings
#%{_bindir}/test_dbus_performance
%if "%{build_uidump}" == "1"
%{_bindir}/aurum-uidump
%endif

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{_includedir}/*
%{_libdir}/libaurum.so
%{_libdir}/libpugixml.so
%{_libdir}/libaurumsharp.so
%{_libdir}/pkgconfig/*

%files bootstrap
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{TZ_SYS_RO_PACKAGES}/org.tizen.aurum-bootstrap.xml
%{TZ_SYS_RO_APP}/org.tizen.aurum-bootstrap/*

%if 0%{?gendoc:1}
%files docs
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{_datadir}/doc/aurum/
%endif
