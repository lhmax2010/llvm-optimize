Name:      dbus-tools
Summary:   A set of tools for working with D-Bus
Version:   0.1
Release:   1
License:   Apache-2.0, MIT
Requires:  libxslt-tools cynara
Source:    %{name}-%{version}.tar.gz
Source101: dbus-tools.manifest
BuildArch: noarch
BuildRequires: autoconf

%description
This package provides a set of tools for working with D-Bus.
It includes:
dbuspolicy-checker: a light-weight checker for D-Bus policy files.
It checks syntax and semantics, looking for common errors.

%prep
%setup -q
cp %{SOURCE101} .

%build
pushd policychecker
autoconf
%configure
popd

%install
%make_install

%clean

%files
%manifest dbus-tools.manifest
%license LICENSE.APACHE2.0 LICENSE.MIT
%{_bindir}/dbuspolicy-checker
%{_datadir}/dbus-tools/policychecker/*
