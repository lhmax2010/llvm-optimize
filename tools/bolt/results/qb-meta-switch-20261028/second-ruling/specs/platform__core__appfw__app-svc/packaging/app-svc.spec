%bcond_with x
%bcond_with wayland

Name:       app-svc
Summary:    Application Service
Version:    0.1.57
Release:    0
Group:      Application Framework/Service
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: app-svc.manifest
Source1002: app-svc-tests.manifest

Requires(post):     /sbin/ldconfig
Requires(postun):   /sbin/ldconfig

BuildRequires: cmake

BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(ecore)
%if %{with x}
BuildRequires:      pkgconfig(ecore-x)
%endif

%description
Application Service

%package devel
Summary:    App svc
Group:      Development/Application Framework
Requires:   %{name} = %{version}-%{release}
%description devel
%devel_desc

%package tests
Summary:    tests for App svc
Requires:   %{name} = %{version}

%description tests
tests for App svc

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .

%build
%cmake . \
%if %{with wayland} && !%{with x}
-Dwith_wayland=TRUE
%else
-Dwith_x=TRUE
%endif

%__make %{?jobs:-j%jobs}

%install
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/libappsvc.so.0
%{_libdir}/libappsvc.so.0.1.0

%files devel
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_libdir}/pkgconfig/appsvc.pc
%{_libdir}/libappsvc.so
%{_includedir}/appsvc/*.h

%files tests
%manifest %{name}-tests.manifest
%{_bindir}/appsvc_test
