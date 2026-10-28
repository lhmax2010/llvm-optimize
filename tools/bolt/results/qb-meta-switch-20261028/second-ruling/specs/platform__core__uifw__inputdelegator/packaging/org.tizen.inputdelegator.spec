Name: org.tizen.inputdelegator
Summary: Input Delegator Application
Version: 0.11.8
Release: 1
Group: Applications
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz

%define enable_log_manager 1

BuildRequires: cmake
BuildRequires: gettext-tools
BuildRequires: pkgconfig(libtzplatform-config)

BuildRequires:  pkgconfig(capi-appfw-app-control)
BuildRequires:  pkgconfig(capi-appfw-preference)
BuildRequires:  pkgconfig(capi-content-media-content)
BuildRequires:  pkgconfig(capi-media-recorder)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(dali2-ui-foundation)
BuildRequires:  pkgconfig(dali2-ui-components)
BuildRequires:  pkgconfig(dali2-core)
BuildRequires:  pkgconfig(dali2-adaptor)
BuildRequires:  dali2-adaptor-integration-devel
BuildRequires:  pkgconfig(storage)
BuildRequires:  pkgconfig(stt)
BuildRequires:  dali2-integration-devel

%description
Input Delegator Application

%prep
%setup -q

%build
export CFLAGS_BASE="${CFLAGS} -DTIZEN_DEBUG_ENABLE -fvisibility=hidden"
export CXXFLAGS_BASE="${CXXFLAGS} -DTIZEN_DEBUG_ENABLE -std=c++17 -fvisibility-inlines-hidden"
export FFLAGS="${FFLAGS} -DTIZEN_DEBUG_ENABLE"

rm -rf CMakeFiles
rm -rf CMakeCache.txt

export CFLAGS="${CFLAGS_BASE}";
export CXXFLAGS="${CXXFLAGS_BASE}";
%cmake . -DTARGET=common \
        -DTZ_SYS_RO_APP=%TZ_SYS_RO_APP \
        -DTZ_SYS_RO_PACKAGES=%TZ_SYS_RO_PACKAGES

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

%make_install

%find_lang inputdelegator

%files -f inputdelegator.lang
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{TZ_SYS_RO_PACKAGES}/%{name}.xml
%{TZ_SYS_RO_APP}/org.tizen.inputdelegator/bin/inputdelegator
%{TZ_SYS_RO_APP}/org.tizen.inputdelegator/res/images
%license LICENSE
