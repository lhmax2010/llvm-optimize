Name:	    vulkan-headers
Version:    1.3.296
Release:    0
License:    Apache-2.0
Summary:    Vulkan Header files and API registry
Group:      Graphics & UI Framework/GL
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

BuildRequires:  cmake
BuildRequires:  ninja

%description
Vulkan Header files and API registry

%prep
%setup -q
cp %{SOURCE1001} .


%build
cmake -G Ninja .
ninja

%install
rm -rf %{buildroot}
mkdir -p "%{buildroot}"%{_includedir}/vulkan
mkdir -p "%{buildroot}"%{_includedir}/vk_video
mkdir -p "%{buildroot}"%{_datadir}/vulkan/registry/
mkdir -p %{buildroot}/usr/local/share/cmake/VulkanHeaders/
cp -ar include/* "%{buildroot}"%{_includedir}/
cp -ar registry/* "%{buildroot}"%{_datadir}/vulkan/registry/
cp -a generated/* "%{buildroot}"/usr/local/share/cmake/VulkanHeaders/
find CMakeFiles/Export/ -name 'VulkanHeaders*.cmake' -exec cp {} %{buildroot}/usr/local/share/cmake/VulkanHeaders/ \;

%files
%manifest %{name}.manifest
%license LICENSES
%defattr(-,root,root,-)
%{_includedir}/vulkan/*
%{_includedir}/vk_video/*
%{_datadir}/vulkan/registry/
/usr/local/share/cmake/*

