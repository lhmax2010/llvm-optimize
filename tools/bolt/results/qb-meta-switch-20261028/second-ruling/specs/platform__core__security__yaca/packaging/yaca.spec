%{!?build_type:%define build_type RELEASE}

Name:               yaca
Version:            0.0.6
Release:            0
Source0:            %{name}-%{version}.tar.gz
License:            Apache-2.0
Group:              Security/Other
Summary:            Yet Another Crypto API
BuildRequires:      cmake
BuildRequires:      python3 >= 3.4
BuildRequires:      python3-setuptools
BuildRequires:      pkgconfig(capi-base-common)
BuildRequires:      pkgconfig(openssl3)
BuildRequires:      boost-devel
%if "%build_type" == "COVERAGE"
BuildRequires:      lcov
%endif
Requires(post):     /sbin/ldconfig
Requires(postun):   /sbin/ldconfig

%define _toolchain_override gcc

%global rw_app_dir          %{?TZ_SYS_RW_APP:%TZ_SYS_RW_APP}%{!?TZ_SYS_RW_APP:/opt/usr/apps}
%global yaca_tests          %rw_app_dir/yaca-tests

%description
The package provides Yet Another Crypto API.

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE
%manifest yaca.manifest
%{_libdir}/libyaca.so.0
%{_libdir}/libyaca.so.%{version}

%prep
%setup -q

%global coverage_dir %{_datadir}/yaca-coverage

%build
%cmake . \
        -DCMAKE_BUILD_TYPE=%{build_type} \
        -DCOVERAGE_DIR=%{coverage_dir} \
        -DYACA_TESTS=%yaca_tests

make -k %{?jobs:-j%jobs}

%install
%make_install
%py3_compile %{buildroot}/%{python3_sitelib}

%clean
rm -rf %{buildroot}

## Devel Package ##############################################################
%package devel
Summary:        Yet Another Crypto API development files
Group:          Security/Other
Requires:       yaca = %{version}-%{release}

%description devel
The package provides Yet Another Crypto API development files.

%files devel
%{_libdir}/libyaca.so
%{_includedir}/yaca
%{_libdir}/pkgconfig/yaca.pc

## Examples Package ###########################################################
%package examples
Summary:        Yet Another Crypto API example files
Group:          Security/Other
Requires:       yaca = %{version}-%{release}

%description examples
The package provides Yet Another Crypto API example files.

%files examples
%{_bindir}/yaca-example*
%{_datadir}/%{name}/examples

## Tests Package ##############################################################
%package tests
Summary:        Yet Another Crypto API tests
Group:          Security/Other
Requires:       yaca = %{version}-%{release}

%description tests
The package provides Yet Another Crypto API unit tests.

%files tests
%{_bindir}/yaca-unit-tests*
%yaca_tests/data/

## Python3 Package ############################################################
%package -n python3-yaca
Summary:        Yet Another Crypto API Python3 bindings
Group:          Security/Other
Requires:       yaca = %{version}-%{release}

%description -n python3-yaca
The package provides Yet Another Crypto API bindings for Python3.

%files -n python3-yaca
%{python3_sitelib}/%{name}

## Coverage Package ###########################################################
%if "%build_type" == "COVERAGE"
%package coverage
Summary:        Yet Another Crypto API code coverage data
Group:          Security/Other
Requires:       yaca-tests = %{version}-%{release}
Requires:       yaca-debugsource = %{version}-%{release}
Requires:       lcov
Requires:       gcc

%description coverage
Yet Another Crypto API code coverage data

%files coverage
%{_bindir}/yaca-coverage.sh
%coverage_dir
%endif
