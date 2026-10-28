%define name		hal-api-hdcp

### main package #########
Name:       %{name}
Summary:    %{name} interface
Version:    2.0.0
Release:    0
Group:      Development/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}-manifest.xml
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(hal-api-common)
BuildRequires: pkgconfig(gmock)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: tidl
BuildRequires: pkgconfig(rpc-port)
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(capi-appfw-app-common)
BuildRequires: pkgconfig(capi-appfw-app-manager)
BuildRequires: pkgconfig(capi-appfw-package-manager)

%description
%{name} interface package for product vendor developer


### devel package #########
%package    devel
Summary:    %{name} interface
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
%{name} interface development package for product vendor developer

### test package #########
%package haltests
Summary: tests for %{name}
Requires: %{name} = %{version}

%description haltests
Haltests for %{name}


### build and install #########
%prep
%setup -q

mkdir -p ./src/generated
(cd src/generated && tidlc -p -l C -i ../../include/hal_hdcp_ipc_2.tidl -o hal_hdcp_proxy_2)

mkdir -p ./src/service_plugin/generated
(cd src/service_plugin/generated && tidlc -s -l C -i ../../../include/hal_hdcp_ipc_2.tidl -o hal_hdcp_stub_2)

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%cmake . \
        -DCMAKE_C_COMPILER=%__cc -DCMAKE_CXX_COMPILER=%__cxx \
        -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \
        -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_LIBDIR_PREFIX=%{_libdir}

%build
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/hal
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/hal/
%make_install

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
/usr/bin/hal-compatibility-checker --reset

%postun
/sbin/ldconfig
/usr/bin/hal-compatibility-checker --reset

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/hal/*.so.*
%{_libdir}/hal/libhal-backend-service-hdcp.so
%{_sysconfdir}/hal/%{name}-manifest.xml

%files devel
%defattr(-,root,root,-)
%{_includedir}/hal/*.h
%{_libdir}/hal/libhal-api-*.so
%{_libdir}/pkgconfig/*.pc

%files haltests
%manifest %{name}-haltests.manifest
%{_bindir}/hal/hdcp-haltests
