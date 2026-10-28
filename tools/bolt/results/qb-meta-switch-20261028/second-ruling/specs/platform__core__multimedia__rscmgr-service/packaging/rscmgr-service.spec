Name: rscmgr-service
Summary: Daemon for resource manager
Version: 0.1
Release: 15
Group:   Multimedia/Libraries
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz
Source1: rscmgr-service.service
Source2: rscmgr-msgq.service
Source3: rscmgr-service-asan.conf
Source4: rscmgr-service.conf
BuildRequires: cmake >= 2.8.12
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(resource-information)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: python
BuildRequires: python-xml
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(ttrace)
BuildRequires: pkgconfig(wayland-client)
Requires: security-config

%description
This package provides service for vconf key usage

%package devel
Summary: The development package for daemon
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The development package for vconf daemon

%prep
%setup -q

%build
export CFLAGS="$CFLAGS %{?_vd_cflags}"
export CXXFLAGS="$CXXFLAGS %{?__vd_cxxflags}"
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
cmake . \
     -DPACKAGE_NAME=%{name} \
     -DINCLUDEDIR=%{_includedir} \
     -DVERSION=%{version} \
     -DBINDIR=%{TZ_SYS_BIN} \
     -DMAJORVERSION=%{MAJORVER} \
     -DLIBDIR=%{_libdir}
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install
mkdir -p %{buildroot}%{_unitdir}/basic.target.wants
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
cp %SOURCE4 %{buildroot}%{_sysconfdir}/dbus-1/system.d

install -m 0644 %SOURCE2 %{buildroot}%{_unitdir}/rscmgr-msgq.service
%install_service basic.target.wants rscmgr-msgq.service
ln -sf ../rscmgr-msgq.service %{buildroot}%{_unitdir}/basic.target.wants/

install -m 0644 %SOURCE1 %{buildroot}%{_unitdir}/%{name}.service
%install_service basic.target.wants %{name}.service
ln -sf ../rscmgr-msgq.service %{buildroot}%{_unitdir}/basic.target.wants/

%if "%{asan}" == "1"
mkdir -p %{buildroot}%{_unitdir}/%{name}.service.d
install -m 644 %SOURCE3 %{buildroot}%{_unitdir}/%{name}.service.d/%{name}-asan.conf
%endif
cp %SOURCE4 %{buildroot}%{_sysconfdir}/dbus-1/system.d

%clean
rm -rf %{buildroot}

%files
%manifest %{name}.manifest
%license LICENSE.APLv2
%{TZ_SYS_BIN}/gen_rm_msgq
%{TZ_SYS_BIN}/%{name}
%{_unitdir}/rscmgr-msgq.service
%{_unitdir}/basic.target.wants/rscmgr-msgq.service
%{_unitdir}/%{name}.service
%{_unitdir}/basic.target.wants/%{name}.service
%if "%{asan}" == "1"
%{_unitdir}/%{name}.service.d/%{name}-asan.conf
%endif
%{_sysconfdir}/dbus-1/system.d/%{name}.conf

%files devel
