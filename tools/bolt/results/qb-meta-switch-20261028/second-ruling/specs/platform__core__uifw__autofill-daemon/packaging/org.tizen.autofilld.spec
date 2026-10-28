Name:       org.tizen.autofilld
Summary:    Autofill Daemon
Version:    1.11.3
Release:    1
Group:      Graphics & UI Framework/Input
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  tidl
BuildRequires:  gawk
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(rpc-port)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(capi-appfw-service-application)
BuildRequires:  pkgconfig(capi-appfw-preference)
BuildRequires:  pkgconfig(capi-appfw-app-manager)
BuildRequires:  pkgconfig(tizen-core)

%if "%{?profile}" == "tv"
  %define __hash_signing 0
%else
  %define __hash_signing 1
%endif

%if 0%{?__hash_signing}
BuildRequires:  hash-signer
%if 0%{?sec_product_feature_profile_wearable}
Requires(post): signing-client
%endif
%endif

%description
Autofill Daemon


%prep
%setup -q

tidlc -s -l C -i tidl/autofill.tidl -o autofill_stub
mv autofill_stub.h ./src/
mv autofill_stub.c ./src/

tidlc -p -l C -i tidl/autofill_service.tidl -o autofill_service_proxy
mv autofill_service_proxy.h ./src/
mv autofill_service_proxy.c ./src/

tidlc -s -l C -i tidl/autofill_manager.tidl -o autofill_manager_stub
mv autofill_manager_stub.h ./src/
mv autofill_manager_stub.c ./src/


%build
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE -fvisibility=hidden -Werror"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE -fvisibility=hidden -Werror"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE -fvisibility=hidden"

rm -rf CMakeFiles
rm -rf CMakeCache.txt
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DTZ_SYS_RO_APP=%TZ_SYS_RO_APP -DTZ_SYS_RO_PACKAGES=%TZ_SYS_RO_PACKAGES

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%if 0%{?__hash_signing}
%define tizen_sign 1
%define tizen_sign_base /usr/apps/%{name}
%define tizen_sign_level platform
%define tizen_author_sign 1
%define tizen_dist_sign 1
%else
  install -m 0644 sign/tv/author-signature.xml "%{buildroot}"/%{TZ_SYS_RO_APP}/%{name}
  install -m 0644 sign/tv/signature1.xml "%{buildroot}"%{TZ_SYS_RO_APP}/%{name}
%endif

%post
%if 0%{?sec_product_feature_profile_wearable}
/usr/bin/signing-client/hash-signer-client.sh -a -d -p platform %{TZ_SYS_RO_APP}/%{name}
%endif

%files
%manifest %{name}.manifest
%license LICENSE
%{TZ_SYS_RO_PACKAGES}/%{name}.xml
%{TZ_SYS_RO_APP}/%{name}/*
