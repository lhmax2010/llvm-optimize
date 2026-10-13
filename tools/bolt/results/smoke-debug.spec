Name: bolt-smoke-d
Version: 1
Release: 1
Summary: Full strip BOLT selector smoke fixture
License: Apache-2.0
Group: Development/Tools
Source0: clang-22
Source1: control
Source2: control.c
%description
BOLT selector qualification fixture only.
%debug_package

%prep
mkdir -p %{_builddir}
cp %{SOURCE2} %{_builddir}/control.c
%build
%install
set -x
mkdir -p %{buildroot}/usr/bin
install -m 0755 %{SOURCE0} %{buildroot}/usr/bin/clang-22
install -m 0755 %{SOURCE1} %{buildroot}/usr/bin/bolt-control
%files
%defattr(-,root,root,-)
/usr/bin/clang-22
/usr/bin/bolt-control
