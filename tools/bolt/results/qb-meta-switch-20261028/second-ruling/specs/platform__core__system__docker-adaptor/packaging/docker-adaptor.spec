%define debug_package %{nil}

Name:       docker-adaptor
Summary:    Docker Adaptors for Tizen Container
Version:    1.0
Release:    0
Group:      Tools/Docker
License:    Apache-2.0
ExclusiveArch:  aarch64

BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: curl
BuildRequires: gawk

Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest

%define unpackdir source
%define pkgsdir packages
%define host_pkgsdir host_packages

%define container01 tizen-headed
%define container02 alpine

%description
Docker Adaptors for Containers

%package %{container01}
Summary:        Docker Adaptor for %{container01} Container
Group: Tools/Docker
License: Apache-2.0
Requires: docker-launcher

%description %{container01}
Docker Adaptors for %{container01} Container

%package %{container02}
Summary:        Docker Adaptor for %{container02} Container
Group: Tools/Docker
License: Apache-2.0
Requires: docker-launcher

%description %{container02}
Docker Adaptors for %{container02} Container

%prep
%setup -q
cp %{SOURCE1} ./%{name}.manifest

%install
install -d %{buildroot}%{TZ_SYS_DATA}/container
install -d %{buildroot}%{TZ_SYS_DATA}/container/list

for container in %{container01}; do
install -d %{buildroot}%{TZ_SYS_DATA}/container/$container
install -m 0644 ./container/$container/config-$container.json %{buildroot}%{TZ_SYS_DATA}/container/$container

install -d %{buildroot}%{TZ_SYS_DATA}/container/$container/configs
install -m 0644 ./container/$container/configs/* %{buildroot}%{TZ_SYS_DATA}/container/$container/configs
done

for container in %{container02}; do
install -d %{buildroot}%{TZ_SYS_DATA}/container/$container
install -m 0644 ./container/$container/config-$container.json %{buildroot}%{TZ_SYS_DATA}/container/$container

install -d %{buildroot}%{TZ_SYS_DATA}/container/$container/images
install -m 0644 ./container/$container/images/* %{buildroot}%{TZ_SYS_DATA}/container/$container/images

install -d %{buildroot}%{TZ_SYS_DATA}/container/$container/configs
install -m 0644 ./container/$container/configs/* %{buildroot}%{TZ_SYS_DATA}/container/$container/configs
done

%preun %{container01}
if [ -e %{TZ_SYS_DATA}/container/list/config-%{container01}.json ]; then
	mv -v %{TZ_SYS_DATA}/container/list/config-%{container01}.json %{TZ_SYS_DATA}/container/%{container01}/config-%{container01}.json
fi

%postun %{container01}
rm -rf %{TZ_SYS_DATA}/container/%{container01}

%files %{container01}
%manifest %{name}.manifest
%defattr(-,system_fw,system_fw,-)
%license LICENSE
%{TZ_SYS_DATA}/container/%{container01}

%post %{container02}
mv %{TZ_SYS_DATA}/container/%{container02}/config-%{container02}.json %{TZ_SYS_DATA}/container/list/config-%{container02}.json

%preun %{container02}
if [ -e %{TZ_SYS_DATA}/container/list/config-%{container02}.json ]; then
	mv %{TZ_SYS_DATA}/container/list/config-%{container02}.json %{TZ_SYS_DATA}/container/%{container02}/config-%{container02}.json
fi

%postun %{container02}
rm -rf %{TZ_SYS_DATA}/container/%{container02}

%files %{container02}
%manifest %{name}.manifest
%defattr(-,system_fw,system_fw,-)
%license LICENSE
%{TZ_SYS_DATA}/container/%{container02}
