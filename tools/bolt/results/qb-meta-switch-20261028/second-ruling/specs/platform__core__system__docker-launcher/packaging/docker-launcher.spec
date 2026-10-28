Name:       docker-launcher
Summary:    docker launcher
Version:    1.0.1
Release:    0
Group:      System/Docker Framework
License:    Apache-2.0
ExclusiveArch: armv7l aarch64
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
Source2:    %{name}.service

BuildRequires:  cmake
BuildRequires:  libcurl-devel
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  jsoncpp-devel
BuildRequires:  libblkid-devel
BuildRequires:  libmount-devel
BuildRequires:  libcap-devel
BuildRequires:  pkgconfig(libtzplatform-config)

# Ensure crash_worker user is available (created by security-config, package provides crash_worker-owned files)
Requires: security-config
Requires: jsoncpp

%description
docker launcher

%prep
%setup -q
chmod g-w %_sourcedir/*
cp %{SOURCE1} ./%{name}.manifest
cp %{SOURCE2} ./%{name}.service

%build
export LDFLAGS="$LDFLAGS -Wl,--as-needed"
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%cmake . \
	-DPLATFORM=tizen \
	-DMAJORVER=${MAJORVER}\
	-DFULLVER=%{version}\
	-DBIN_INSTALL_DIR:PATH=%{_bindir} \
	-DBUILD_UNITTEST=OFF \
	-DBUILD_COVERAGE=OFF

%__make %{?_smp_mflags}

%install
%make_install
mkdir -p %{buildroot}%{_unitdir}/multi-user.target.wants
install -m 0644 %{name}.service %{buildroot}%{_unitdir}/docker-launcher.service
ln -s ../%{name}.service %{buildroot}%{_unitdir}/multi-user.target.wants/

install -m 750 ./scripts/crash-forwarder.py %{buildroot}%{_bindir}/crash-forwarder
install -d %{buildroot}/usr/lib/sysctl.d
install -m 644 ./sysctl.d/99-docker-launcher.conf.in %{buildroot}/usr/lib/sysctl.d/99-docker-launcher.conf
install -d %{buildroot}%{TZ_SYS_DATA}/container

%post

%postun

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bindir}/docker-launcher*
%{_bindir}/dlauncher*
%license LICENSE
%{_unitdir}/%{name}.service
%{_unitdir}/multi-user.target.wants/%{name}.service
%attr(0750,root,crash_worker) %{_bindir}/crash-forwarder
/usr/lib/sysctl.d/99-docker-launcher.conf
%{_libdir}/pkgconfig/%{name}.pc
%attr(0750,system_fw,system_fw) %{TZ_SYS_DATA}/container
