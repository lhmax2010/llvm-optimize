%if 0%{?debug:1}
%define debug_package %{nil}
%define __debug_install_post %{nil}
%endif

Name:       espp-service
Summary:    ESPP service package which contains client lib. and daemon binary
Version:    0.3.21
Release:    0
Group:      Multimedia/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
Source2:    %{name}.service
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: meson
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(json-glib-1.0)
BuildRequires: pkgconfig(esplusplayer)
%if "%{use_tizen_60}" != "1"
BuildRequires: pkgconfig(libtbm)
BuildRequires: pkgconfig(capi-media-image-util)
%endif
%if "%{use_service_app}" == "1"
BuildRequires: pkgconfig(capi-appfw-service-application)
BuildRequires: pkgconfig(capi-appfw-application)
%endif

%description
ESPP service package contains daemon binary which uses esplusplayer to render audio/video buffers and it's client library

%package client
Summary:    ESPP service client library
Group:      Multimedia/Libraries

%description client
ESPP service client library used by applications that request to render audio/video buffers to ESPP service daemon

%package client-devel
Summary:    ESPP service client development header and library
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description client-devel
ESPP service client development header and library

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1} %{SOURCE2} .

%define _bin_dir %{_bindir}

%build
meson setup --auto-features=disabled \
  --prefix=/usr \
  --libdir=%{_libdir} \
  --datadir=%{_datadir} \
%if "%{use_tizen_60}" == "1"
  -Dtizen-60=true \
%else
  -Dtizen-60=false \
%endif
  -Dsock-path=/tmp/espp_service.sock \
%if "%{use_service_app}" == "1"
  -Dservice-app=true \
%else
  -Dservice-app=false \
%endif
  -D_bindir=%{_bin_dir} \
%if "%{asan}" != "1"
%ifnarch x86_64
  --werror \
%endif
%endif
  build

ninja -C build

%install
rm -rf %{buildroot}
export DESTDIR=%{buildroot}
ninja -C build install

mkdir -p %{buildroot}%{_unitdir}/
install -m0644 %{SOURCE2} %{buildroot}%{_unitdir}/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bin_dir}/espp-service
%{_unitdir}/espp-service.service
%license LICENSE.APLv2

%files client
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/*.so*
%exclude %{_libdir}/debug/*
%license LICENSE.APLv2

%files client-devel
%manifest %{name}.manifest
%{_libdir}/*.so
%{_libdir}/pkgconfig/espp-service*.pc
%{_includedir}/*.h

