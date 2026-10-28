%define _manifestdir %{TZ_SYS_RW_PACKAGES}
%define _desktop_icondir %{TZ_SYS_SHARE}/icons/default/small

%define crosswalk_extensions tizen-extensions-crosswalk
%define crosswalk_extensions_path %{_libdir}/%{crosswalk_extensions}
%define webapi_tools /usr/include/webapi-plugins/tools

Name:       cordova-api
Version:    0.18
Release:    0
License:    Apache-2.0 and BSD-3-Clause and MIT
Group:      Development/Libraries
Summary:    Cordova API using Tizen plugins
Source0:    %{name}-%{version}.tar.gz

BuildRequires: ninja
BuildRequires: python
BuildRequires: pkgconfig(webapi-plugins)
BuildRequires: pkgconfig(icu-i18n)
BuildRequires: pkgconfig(vconf)

%description
Cordova API using Tizen plugins.

%prep
%setup -q

%build

export GYP_GENERATORS='ninja'
GYP_OPTIONS="--depth=. -Dtizen=1 -Dextension_build_type=Debug -Dextension_host_os=%{tizen_profile_name}"
GYP_OPTIONS="$GYP_OPTIONS -Ddisplay_type=x11"
GYP_OPTIONS="$GYP_OPTIONS -Dcrosswalk_extensions_path=%{crosswalk_extensions_path}"
GYP_OPTIONS="$GYP_OPTIONS -Dversion=%{version}"

%{webapi_tools}/gyp/gyp $GYP_OPTIONS src/cordova-api.gyp

ninja -C out/Default %{?_smp_mflags}

%install

# Extensions.
mkdir -p %{buildroot}%{crosswalk_extensions_path}
install -p -m 644 out/Default/libtizen*.so %{buildroot}%{crosswalk_extensions_path}

# execute desc_gentool
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%{buildroot}%{crosswalk_extensions_path} %{webapi_tools}/desc_gentool \
    %{crosswalk_extensions_path} \
    %{buildroot}%{crosswalk_extensions_path} > cordova-api.json

# temporary plugins description for lazy loading
install -p -m 644 cordova-api.json %{buildroot}%{crosswalk_extensions_path}/cordova-api.json

%files
%{crosswalk_extensions_path}/libtizen*.so
%{crosswalk_extensions_path}/cordova-api.json
%manifest cordova-api.manifest
%license LICENSE LICENSE.BSD-3-Clause LICENSE.MIT NOTICE
