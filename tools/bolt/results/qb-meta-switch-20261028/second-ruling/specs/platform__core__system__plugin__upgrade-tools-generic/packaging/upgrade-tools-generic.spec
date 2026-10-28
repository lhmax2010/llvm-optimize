%define install_path %{name}
%define install_path_boot_rpi4 %{name}-boot-rpi4
%define install_path_platform %{name}-platform
%define config_path_rpi4 mk_delta/rpi4/cfg
%define config_path_platform mk_delta/platform/cfg
%define scripts_path scripts

Name:           upgrade-tools-generic
Version:        1.0.0
Release:        0
License:        Apache-2.0
Summary:        Template generic config for delta building
Group:          Development/System
Source0:        %{name}-%{version}.tar.gz

Source1001:     %{name}.manifest

BuildRequires:  cmake

%description
This is a dummy package


%package        boot-rpi4
Summary:        Delta config for boot image of rpi4
%description    boot-rpi4
Delta config for boot image of rpi4

%package        platform
Summary:        Delta config for platform image
%description    platform
Delta config for platform image

%prep
%setup -q
%cmake . -DCMAKE_C_COMPILER=%__cc -DCMAKE_CXX_COMPILER=%__cxx

%build
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

# upgrade-tools-generic
mkdir -p %{buildroot}/%{install_path}
mkdir -p %{buildroot}/%{install_path}/%{config_path_rpi4}
mkdir -p %{buildroot}/%{install_path}/%{scripts_path}
cat $(find configs -name 'delta.cfg') > %{buildroot}/%{install_path}/%{config_path_rpi4}/delta.cfg
cp scripts/* %{buildroot}/%{install_path}/%{scripts_path}/.

# upgrade-tools-generic-boot-rpi4
mkdir -p %{buildroot}/%{install_path_boot_rpi4}
mkdir -p %{buildroot}/%{install_path_boot_rpi4}/%{config_path_rpi4}
mkdir -p %{buildroot}/%{install_path_boot_rpi4}/%{scripts_path}
cp ./configs/rpi4/boot/delta.cfg %{buildroot}/%{install_path_boot_rpi4}/%{config_path_rpi4}/.
cp scripts/* %{buildroot}/%{install_path_boot_rpi4}/%{scripts_path}/.

# upgrade-tools-generic-platform
mkdir -p %{buildroot}/%{install_path_platform}
mkdir -p %{buildroot}/%{install_path_platform}/%{config_path_platform}
mkdir -p %{buildroot}/%{install_path_platform}/%{scripts_path}
cp ./configs/rpi4/platform/delta.cfg %{buildroot}/%{install_path_platform}/%{config_path_platform}/.
cp scripts/* %{buildroot}/%{install_path_platform}/%{scripts_path}/.

%files
/%{install_path}/*

%files          boot-rpi4
/%{install_path_boot_rpi4}/*

%files          platform
/%{install_path_platform}/*
