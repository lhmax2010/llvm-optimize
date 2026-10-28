%{!?build_type:%global build_type RELEASE}

Name:    privilege-info
Summary: Privilege Information
Version: 0.0.9
Release: 1
Group:   Security/API
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz

Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires: cmake
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(security-privilege-manager)
%if "%{build_type}" == "COVERAGE"
BuildRequires: lcov
%endif

%description
Provides Privilege Information(Privilege Info) API

%package -n privilege-info-devel
Summary: Privilege Info API (Development)
Group:   Security/Development
Requires: %{name} = %{version}-%{release}

%description -n privilege-info-devel
The Privilege Info API provides functions to get privilege information (Development)

%package -n privilege-info-tests
Summary: Privilege Info TC
Group:   Security/Testing
Requires: %{name} = %{version}-%{release}

%description -n privilege-info-tests
Privilege Info API Internal Test

%if "%{build_type}" == "COVERAGE"

%package -n privilege-info-coverage
Summary: Privilege Info code coverage data
Group:   Security/Testing
Requires: privilege-info-tests = %{version}-%{release}
Requires: privilege-info-debugsource = %{version}-%{release}
Requires: lcov
Requires: gcc

%description -n privilege-info-coverage
Privilege Info code coverage data

%endif

%prep
%setup -q

%build

%global coverage_dir %{_datadir}/privilege-info-coverage

%cmake . -DCMAKE_BUILD_TYPE=%{build_type} -DCOVERAGE_DIR=%{coverage_dir}

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -n privilege-info -p /sbin/ldconfig
%postun -n privilege-info -p /sbin/ldconfig

%files -n privilege-info
%license LICENSE.Apache-2.0
%manifest packaging/privilege-info.manifest
%{_libdir}/libprivilege-info.so.*

%files -n privilege-info-devel
%manifest packaging/privilege-info.manifest
%{_libdir}/libprivilege-info.so
%{_includedir}/privilege_information.h
%{_libdir}/pkgconfig/privilege-info.pc

%files -n privilege-info-tests
%manifest packaging/privilege-info.manifest
%{_bindir}/privilege-info-tests

%if "%{build_type}" == "COVERAGE"

%files -n privilege-info-coverage
%manifest packaging/privilege-info.manifest
%{_bindir}/privilege-info-coverage.sh
%coverage_dir

%endif
