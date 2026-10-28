Name:       org.tizen.inputmethod-setting
Summary:    Input Method Setting Service
Version:    0.11.4
Release:    1
Group:      Graphics & UI Framework/Input
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(capi-appfw-service-application)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(isf)

%description
Input Method Setting Service for ISF

%prep
%setup -q -n %{name}-%{version}

%build
export CFLAGS="$CFLAGS -DTIZEN_ENGINEER_MODE -DTIZEN_DEBUG_ENABLE -fvisibility=hidden -Werror"
export CXXFLAGS="$CXXFLAGS -DTIZEN_ENGINEER_MODE -DTIZEN_DEBUG_ENABLE -fvisibility=hidden -fvisibility-inlines-hidden -Werror"
export FFLAGS="$FFLAGS -DTIZEN_ENGINEER_MODE -DTIZEN_DEBUG_ENABLE"

%define _pkg_dir %{TZ_SYS_RO_APP}/org.tizen.inputmethod-setting

cmake . -DINSTALL_PREFIX=%{_pkg_dir} -DTZ_SYS_RO_PACKAGES=%TZ_SYS_RO_PACKAGES
make %{?jobs:-j%jobs}

%install
%make_install

%define tizen_sign 1
%define tizen_sign_base %{_pkg_dir}
%define tizen_sign_level platform
%define tizen_author_sign 1
%define tizen_dist_sign 1

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bindir}/inputmethod-setting
%{_pkg_dir}/bin/inputmethod-setting
%{TZ_SYS_RO_PACKAGES}/%{name}.xml
%license LICENSE
