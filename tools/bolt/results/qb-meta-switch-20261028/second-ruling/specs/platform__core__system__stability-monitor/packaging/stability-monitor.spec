Name:       stability-monitor
Version:    6.6.0
Release:    0
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.xz
Source1:    %{name}.manifest
Summary:    Stability monitoring daemon
Group:      System/Monitoring
BuildRequires: pkgconfig(json-c)
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(pkgmgr-info)
BuildRequires: pkgconfig(bugreport)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(libkmod)
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(diagnostics)

#Requires:   stability-monitor-kernel-module

%description
This package provides stability monitoring daemon.

%package tests
Summary:    Stability monitor tests/specification
Requires:   %{name} = %{version}

%description tests
Tests for stability monitoring tool

%prep
%setup -q
cp %{SOURCE1} ./%{name}.manifest

%build
make stability-monitor DEFAULT_CONFIG_FILE=%{_libdir}/stability-monitor/default.conf

make -C tests all

%install
make install INSTALL_PREFIX=%{buildroot}/%{_sbindir}
mkdir -p %{buildroot}/%{_libdir}/stability-monitor
cp config/default.conf %{buildroot}/%{_libdir}/stability-monitor/default.conf

mkdir -p %{buildroot}/%{_unitdir}/multi-user.target.wants
cp config/stability-monitor.service %{buildroot}/%{_unitdir}/stability-monitor.service
ln -s ../stability-monitor.service %{buildroot}/%{_unitdir}/multi-user.target.wants/stability-monitor.service

# install -D test-stability-fg-bg %{buildroot}%{_libexecdir}/stability-tests/test-stability-fg-bg
install -D tests/test-stability-cpu   %{buildroot}%{_libexecdir}/stability-tests/test-stability-cpu
install -D tests/test-stability-mem   %{buildroot}%{_libexecdir}/stability-tests/test-stability-mem
install -D tests/test-stability-io    %{buildroot}%{_libexecdir}/stability-tests/test-stability-io
install -D tests/test-stability-fd    %{buildroot}%{_libexecdir}/stability-tests/test-stability-fd

mkdir -p %{buildroot}/etc/stability-monitor.d
cp tests/config.json %{buildroot}/etc/stability-monitor.d/99-test-stability.conf

%files
%manifest %{name}.manifest
%license COPYING
%{_sbindir}/stability-monitor
%{_libdir}/stability-monitor/default.conf
%{_unitdir}/stability-monitor.service
%{_unitdir}/multi-user.target.wants/stability-monitor.service

%files tests
%manifest %{name}.manifest
# %{_libexecdir}/stability-tests/test-stability-fg-bg
%{_libexecdir}/stability-tests/test-stability-cpu
%{_libexecdir}/stability-tests/test-stability-mem
%{_libexecdir}/stability-tests/test-stability-io
%{_libexecdir}/stability-tests/test-stability-fd
/etc/stability-monitor.d/99-test-stability.conf
