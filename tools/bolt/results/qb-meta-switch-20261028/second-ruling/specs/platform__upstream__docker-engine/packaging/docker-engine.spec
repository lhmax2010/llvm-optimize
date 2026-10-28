Name: docker-engine
Version: 20.10.5
Release: 0
Summary: The open-source application container engine
Group: Tools/Docker

License: Apache-2.0
ExclusiveArch: armv7l aarch64 x86_64
Source0: %{name}-%{version}.tar.gz
Source1: %{name}.manifest

BuildRequires: pkgconfig(libtzplatform-config)

Requires(post): systemd
Requires(preun): systemd

%define unpackdir source

%description
Docker is an open source project to build, ship and run any application as a
lightweight container.

Docker containers are both hardware-agnostic and platform-agnostic. This means
they can run anywhere, from your laptop to the largest EC2 compute instance and
everything in between - and they don't require you to use a particular
language, framework or packaging system. That makes them great building blocks
for deploying and scaling web apps, databases, and backend services without
depending on a particular stack or provider.

Prebuilt binaries are download from https://download.docker.com/linux/static/stable


%prep
%setup -q

chmod g-w %_sourcedir/*
cp %{SOURCE1} ./%{name}.manifest

mkdir -p %{unpackdir}
tar -xvf prebuilt/docker-%{version}-%{_arch}.tgz -C %{unpackdir}
cp -f prebuilt/overlay/runc-%{_arch} %{unpackdir}/docker/runc

%install
# install binary
install -d %{buildroot}%{_bindir}
install -m 755 %{unpackdir}/docker/* %{buildroot}%{_bindir}
# prepare sysconf directories
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{TZ_SYS_ETC}/docker
ln -sf %{TZ_SYS_ETC}/docker %{buildroot}%{_sysconfdir}/docker
# install systemd services
install -d %{buildroot}%{_unitdir}
install -m 0644 systemd/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -m 0644 systemd/%{name}.socket %{buildroot}%{_unitdir}/%{name}.socket
%install_service sockets.target.wants %{name}.socket

%pre
getent group docker > /dev/null 2>&1 || %{_sbindir}/groupadd -r docker 2>&1 || :

%post
systemctl daemon-reload
systemctl restart %{name}.service

%preun
systemctl stop %{name}.service
systemctl daemon-reload

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE
%{_bindir}/*
%{_sysconfdir}/docker
%dir %{TZ_SYS_ETC}/docker
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.socket
%{_unitdir}/sockets.target.wants/%{name}.socket
