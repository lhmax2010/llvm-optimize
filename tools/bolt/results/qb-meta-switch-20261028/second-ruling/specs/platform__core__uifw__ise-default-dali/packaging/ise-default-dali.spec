# Unit and integration tests are enabled by default.  Disable with:
#   gbs build ... -- --without tests
#   rpmbuild --without tests ...
%bcond_without tests

Name:       ise-default-dali
Summary:    Tizen Dali Keyboard
Version:    0.3.9
Release:    1
Group:      UI Framework / Text Input
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gettext-tools
BuildRequires:  pkgconfig(capi-appfw-app-control)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(gio-2.0)
%if %{with tests}
BuildRequires:  pkgconfig(gtest)
%endif
BuildRequires:  pkgconfig(notification)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(stt)
BuildRequires:  pkgconfig(capi-appfw-preference)
%if %{with tests}
BuildRequires:  pkgconfig(capi-network-connection)
%endif
BuildRequires:  pkgconfig(capi-ui-inputmethod-core)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(dali2-ui-foundation)
BuildRequires:  pkgconfig(dali2-ui-components)
BuildRequires:  pkgconfig(dali2-core)
BuildRequires:  pkgconfig(dali2-adaptor)
BuildRequires:  dali2-adaptor-integration-devel
BuildRequires:  dali2-integration-devel
BuildRequires:  pkgconfig(libscl-ui-dali)

%description
This application is a Tizen reference Dali S/W keyboard

%if %{with tests}
%package test
Summary: Test executables for %{name}
Group: Development/Testing
Requires: %{name} = %{version}-%{release}

%description test
This package contains unit and integration test executables for %{name}.
%endif

%prep
%setup -q

%build
%cmake . -DTZ_SYS_RO_APP=%TZ_SYS_RO_APP \
         -DTZ_SYS_RO_PACKAGES=%TZ_SYS_RO_PACKAGES \
         %{?_with_tests:-DBUILD_TESTING=ON}
%__make %{?jobs:-j%jobs}

%if %{with tests}
%check
ctest --output-on-failure
%endif

%install
rm -rf %{buildroot}
%make_install

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{TZ_SYS_RO_APP}/%{name}/bin/%{name}
%{TZ_SYS_RO_APP}/%{name}/bin/%{name}-setting
%{TZ_SYS_RO_PACKAGES}/%{name}.xml
%config %{_sysconfdir}/ise-dali/conf/config.json
%{TZ_SYS_RO_APP}/%{name}/res/layout/common/*.xml
%{TZ_SYS_RO_APP}/%{name}/res/layout/common/image/*
%{TZ_SYS_RO_APP}/%{name}/res/locale/*
%license LICENSE

%if %{with tests}
%files test
%defattr(-,root,root,-)
%{_libexecdir}/%{name}/ise-default-dali-unit-test
%{_libexecdir}/%{name}/ise-default-dali-integration-test
%endif
