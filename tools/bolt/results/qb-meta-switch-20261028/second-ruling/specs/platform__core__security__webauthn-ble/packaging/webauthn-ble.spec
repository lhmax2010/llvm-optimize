%{!?build_type:%global build_type RELEASE}

%global version_major   1
%global version_minor   0
%global version_patch   8
%global version_release 1

Name:    webauthn-ble
Summary: Adaptation Layer of Web Authentication Service for BLE Authenticator
Version: %{version_major}.%{version_minor}.%{version_patch}
Release: %{version_release}
Group:   Security/Authentication
License: Apache-2.0 AND MIT
Source0: %{name}-%{version}.tar.gz

Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires: cmake
BuildRequires: python
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(webauthn-hal) >= 1.0.1
BuildRequires: pkgconfig(libwebsockets)
BuildRequires: pkgconfig(capi-network-bluetooth)
BuildRequires: pkgconfig(glib-2.0)

%if 0%{?tizen_version_major} < 8
BuildRequires: pkgconfig(openssl1.1)
%else
BuildRequires: pkgconfig(openssl3)
%endif

Requires: webauthn >= 1.0.1

%description
Adaptation Layer of Web Authentication Service for BLE Authenticator

%package unit-tests
Summary:    Adaptation Layer of Web Authentication Service for BLE Authenticator (unit test)
License:    Apache-2.0
Group:      Security/Development
BuildRequires: pkgconfig(gtest)
Requires:      %{name} = %{version}-%{release}

%description unit-tests
Adaptation Layer of Web Authentication Service for BLE Authenticator (unit test)

%package manual-tests
Summary:    Adaptation Layer of Web Authentication Service for BLE Authenticator (manual test)
License:    Apache-2.0
Group:      Security/Development
BuildRequires: pkgconfig(capi-media-vision)
Requires:      %{name} = %{version}-%{release}
Requires:      webauthn-manual-tests

%description manual-tests
Adaptation Layer of Web Authentication Service for BLE Authenticator (manual test)
The webauthn-manual-tests required to use webauthn-image-viewer

%if "%build_type" == "COVERAGE"
%package coverage
Summary:    Adaptation Layer of Web Authentication Service for BLE Authenticator (code coverage data)
License:    Apache-2.0
Group:      Security/Development
BuildRequires: lcov
Requires:   %{name}-unit-tests = %{version}-%{release}
Requires:   %{name}-debugsource = %{version}-%{release}
Requires:   lcov
Requires:   gcc

%description coverage
Adaptation Layer of Web Authentication Service for BLE Authenticator (code coverage data)
%endif

%prep
%setup -q

%global coverage_dir %{_datadir}/%{name}-coverage

%build
%{?asan:
export CXXFLAGS+=" -Wno-maybe-uninitialized"
}
%cmake . -DCMAKE_BUILD_TYPE=%{build_type} \
         -DPROJECT_NAME=%name \
         -DVERSION_MAJOR=%version_major \
         -DVERSION_MINOR=%version_minor \
         -DVERSION_PATCH=%version_patch \
         -DBIN_DIR=%{_bindir} \
         -DCOVERAGE_DIR=%{coverage_dir} \
%if "%_repository" == "emulator"
         -DEMULATOR_BUILD=1 \
%endif
         -DTIZEN_VERSION=%{?tizen_version_major}%{!?tizen_version_major:100}

make %{?jobs:-j%jobs}

%install
%make_install
cp -a srcs/tinycbor/LICENSE LICENSE.TINYCBOR
# ln -sr would suffice, but ln does not support -r option on Tizen 7.0 :(
%{__python} -c 'import os; \
        import sys; \
        src = sys.argv[1]; \
        dest = sys.argv[2]; \
        dir = os.path.dirname(dest); \
        src = os.path.relpath(src, dir); \
        os.symlink(src, dest)' \
    '%{buildroot}/%{_libdir}/lib%{name}.so' \
    '%{buildroot}/%{WEBAUTHN_HYBRID_PLUGIN_SO_PATH}'

%files
%manifest %{name}.manifest
%license LICENSE
%license LICENSE.TINYCBOR
%{_libdir}/lib%{name}.so*
%{WEBAUTHN_HYBRID_PLUGIN_SO_PATH}

%files -n %{name}-unit-tests
%manifest %{name}-unit-tests.manifest
%license LICENSE
%{_bindir}/%{name}-unit-tests

%files -n %{name}-manual-tests
%manifest %{name}-manual-tests.manifest
%license LICENSE
%{_bindir}/%{name}-manual-tests
%{_bindir}/%{name}-manual-tunnel-tests
%{_bindir}/%{name}-manual-tunnel-tests.sh

%if "%build_type" == "COVERAGE"
%files -n %{name}-coverage
%{_bindir}/%{name}-coverage.sh
%coverage_dir
%endif
