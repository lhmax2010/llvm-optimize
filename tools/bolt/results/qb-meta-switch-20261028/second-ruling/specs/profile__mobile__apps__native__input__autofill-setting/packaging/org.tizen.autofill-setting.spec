Name:       org.tizen.autofill-setting
Summary:    Autofill Setting Application
Version:    0.11.2
Release:    1
Group:      Graphics & UI Framework/Input
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  gettext-tools
BuildRequires:  cmake
BuildRequires:  pkgconfig(capi-appfw-service-application)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(capi-ui-autofill-manager)
BuildRequires:  pkgconfig(capi-appfw-package-manager)
BuildRequires:  pkgconfig(capi-appfw-app-manager)

%description
Autofill Setting Application

%package -n org.tizen.autofill-setting-mobile
Summary:    Compatibility package for image generation
Group:      Graphics & UI Framework/Input
License:    Apache-2.0

%description -n org.tizen.autofill-setting-mobile
Compatibility package retained for image generation. It contains only
the license file.

%prep
%setup -q -n %{name}-%{version}

%build
CFLAGS="$CFLAGS -D_MOBILE";
CXXFLAGS="$CXXFLAGS -D_MOBILE";

export CFLAGS="$CFLAGS -DTIZEN_ENGINEER_MODE -DTIZEN_DEBUG_ENABLE -fvisibility=hidden -Werror"
export CXXFLAGS="$CXXFLAGS -DTIZEN_ENGINEER_MODE -DTIZEN_DEBUG_ENABLE -fvisibility=hidden -fvisibility-inlines-hidden -Werror"
export FFLAGS="$FFLAGS -DTIZEN_ENGINEER_MODE -DTIZEN_DEBUG_ENABLE"

export CFLAGSBASE="$CFLAGS"
export CXXFLAGSBASE="$CXXFLAGS"

rm -rf CMakeFiles
rm -rf CMakeCache.txt

%cmake . -DTZ_SYS_RO_APP=%TZ_SYS_RO_APP \
         -DTZ_SYS_RO_PACKAGES=%TZ_SYS_RO_PACKAGES \
         -DTZ_SYS_RO_ICONS=%TZ_SYS_RO_ICONS
make %{?jobs:-j%jobs}

%post
mkdir -p %{TZ_SYS_RO_APP}/%{name}/bin
mkdir -p %{TZ_SYS_RO_APP}/%{name}/res

%install
rm -rf %{buildroot}

%make_install

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{TZ_SYS_RO_APP}/%{name}/bin/autofill-setting
%{TZ_SYS_RO_APP}/%{name}/res/*
%{TZ_SYS_RO_PACKAGES}/%{name}.xml
%license LICENSE

%files -n org.tizen.autofill-setting-mobile
%defattr(-,root,root,-)
%license LICENSE
