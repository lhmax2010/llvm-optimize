Name:    ot-br-posix
Summary: OpenThread Border Router
Version: 1.2.0
Release: 0
Group:    Network & Connectivity/Common
License: BSD-3-Clause License
Source0: %{name}-%{version}.tar.gz
Source1: otbr-agent.service
Source2: io.openthread.BorderRouter.wpan0.service
Source1001: %{name}.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(dns_sd)
BuildRequires:  ninja

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
OpenThread Border Router daemon and OTBR controller

%prep
%setup -q
cp %{SOURCE1001} .

%ifarch %{arm}
export ARCH=arm
%else
export ARCH=i586
%endif

%build
builddir="${OT_CMAKE_BUILD_DIR:-build}"
echo $builddir

%install
# install binaries and libraries
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}

cp build/src/agent/otbr-agent %{buildroot}%{_bindir}/
cp build/third_party/openthread/repo/src/posix/ot-ctl %{buildroot}%{_bindir}/

find ./build/ -type d -exec mkdir -p %{buildroot}%{_libdir}/{} \;
find ./build/ -name "*.a" -exec cp '{}' %{buildroot}%{_libdir}/ \;

find ./build/ -type d -exec mkdir -p %{buildroot}%{_includedir}/{} \;
find ./build/ -name "*.h" -exec cp '{}' %{buildroot}%{_includedir}/{} \;
find ./build/ -name "*.hpp" -exec cp '{}' %{buildroot}%{_includedir}/{} \;

mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
cp otbr-agent.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/otbr-agent.conf
mkdir -p %{buildroot}%{_unitdir}
cp %{SOURCE1} %{buildroot}%{_unitdir}/otbr-agent.service
mkdir -p %{buildroot}%{_datadir}/dbus-1/system-services/
cp %{SOURCE2} %{buildroot}%{_datadir}/dbus-1/system-services/io.openthread.BorderRouter.wpan0.service

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_unitdir}/otbr-agent.service
%{_datadir}/dbus-1/system-services/io.openthread.BorderRouter.wpan0.service
%attr(644,root,root) %{_sysconfdir}/dbus-1/system.d/otbr-agent.conf
%{_bindir}/ot-ctl
%{_bindir}/otbr-agent
%{_libdir}/*.a
%exclude %{_includedir}/*
