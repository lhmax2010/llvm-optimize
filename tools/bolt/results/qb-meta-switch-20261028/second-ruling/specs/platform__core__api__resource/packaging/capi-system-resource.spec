Name:       capi-system-resource
Summary:    API library for system resource management and optimization
Version:    1.0.0
Release:    0
Group:      System/API
License:    MIT
Source0:    %{name}-%{version}.tar.gz
Source1:    capi-system-resource.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(dlog)
Requires: %{name}-isu

%global build_test_package %{?test_build_on:%test_build_on}%{!?test_build_on:0}

%description
API library for system resource management and optimization

%package devel
Summary:  API library for system resource management and optimization (Devel)
Group:    System/Development
Requires: %{name} = %{version}-%{release}

%description devel
API library for system resource management and optimization (Devel)
%devel_desc

%package plugin
Summary:  API plugin library for system resource management and optimization
Requires: %{name} = %{version}-%{release}

%description plugin
API plugin library

%if %{build_test_package}
%package test
Summary:  API test for system resource management and optimization
Group:    System/Development
BuildRequires:  pkgconfig(glib-2.0)
Requires: %{name} = %{version}-%{release}

%description test
%endif


%isu_package

%prep
%setup -q

%build
cp %{SOURCE1} .
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%cmake . -DMAJORVER=${MAJORVER} \
	     -DFULLVER=%{version}   \
%if %{build_test_package}
		 -DTEST_BUILD_ON=ON  \
%endif
		 -DPLUGIN_PATH=%{_libdir}



%__make %{?jobs:-j%jobs}

%install
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE.MIT
%{_libdir}/libcapi-system-resource.so.*

%files devel
%manifest %{name}.manifest
%license LICENSE.MIT
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-system-resource.so
%{_includedir}/system/*.h
%{_includedir}/system/private/*.h

%files plugin
%manifest %{name}.manifest
%license LICENSE.MIT
%{_libdir}/libcapi-system-resource-plugin.so*

%if %{build_test_package}
%files test
%manifest %{name}.manifest
%license LICENSE.MIT
%{_bindir}/capi-system-resource-test
%{_bindir}/system-resource-test-service
%{_unitdir}/system-resource-test-service.service
%{_unitdir}/multi-user.target.wants/system-resource-test-service.service
%endif
