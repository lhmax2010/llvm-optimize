Name:       connectedhomeip
Summary:    Project Connected Home over IP
Version:    0.0.1
Release:    1
Group:      Network & Connectivity/Other
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
Source2:    %{name}.pc

BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(dns_sd)

BuildRequires: python3
BuildRequires: gn
BuildRequires: ninja
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Project Connected Home over IP is a new Working Group within the Zigbee Alliance.
This Working Group plans to develop and promote the adoption of a new, royalty-free
connectivity standard to increase compatibility among smart home products, with security as a fundamental design tenet

%package devel
Summary: Connected Home over IP for development
Requires: %{name} = %{version}-%{release}

%description devel
This package is for CHIP development

%package test
Summary: Connected Home over IP Test applications
Requires: %{name} = %{version}-%{release}

%description test
This package is for CHIP test applications

%prep
%setup -q
chmod 644 %{SOURCE0}
cp %{SOURCE1} ./%{name}.manifest
cp %{SOURCE2} ./%{name}.pc

%build
#gn gen out/host --args='is_debug=true target_os="linux" current_cpu="arm"'
#ninja -C out/host

%install
# ninja install

# install libraries
mkdir -p %{buildroot}%{_libdir}/chip/
find ./out/host/lib -name "*.a" -exec cp '{}' %{buildroot}%{_libdir}/chip/ \;

cd out/host/obj
find ./ -type d -exec mkdir -p %{buildroot}%{_libdir}/chip/{} \;
find ./ -name "*.a" -exec cp '{}' %{buildroot}%{_libdir}/chip/{} \;
cd -

# install header files
mkdir -p %{buildroot}%{_includedir}/chip/
find ./ -type d -exec mkdir -p %{buildroot}%{_includedir}/chip/{} \;
find ./ -name "*.h" -exec cp '{}' %{buildroot}%{_includedir}/chip/{} \;
find ./ -name "*.hpp" -exec cp '{}' %{buildroot}%{_includedir}/chip/{} \;

# install examples
mkdir -p %{buildroot}%{_bindir}

cp out/host/chip-tool %{buildroot}%{_bindir}/
cp out/host/chip-lighting-app %{buildroot}%{_bindir}/
#cp out/host/chip-all-clusters-app %{buildroot}%{_bindir}/
cp out/host/chip-shell %{buildroot}%{_bindir}/

# install pkg-config file
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cp %{name}.pc %{buildroot}%{_libdir}/pkgconfig 

%post

%files
%manifest %{name}.manifest
%license LICENSE

%files devel
%manifest %{name}.manifest
%{_includedir}/chip/*
%{_libdir}/chip/*
%{_libdir}/pkgconfig/*.pc

%files test
%manifest %{name}.manifest
%{_bindir}/chip-tool
%{_bindir}/chip-lighting-app
#%{_bindir}/chip-all-clusters-app
%{_bindir}/chip-shell
