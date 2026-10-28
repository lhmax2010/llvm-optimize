Name:		vulkan-wsi-layer
Version:	1.0.5
Release:	0
Summary:	Vulkan WSI (Window System Integration) Layer for Tizen
License:	MIT
Group:		Graphics & UI Framework/Hardware Adaptation

Source:		%{name}-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires: autoconf > 2.64
BuildRequires: automake >= 1.11
BuildRequires: libtool >= 2.2

BuildRequires: cmake
BuildRequires: pkgconfig(tpl-egl)
BuildRequires: pkgconfig(libtbm)
BuildRequires: pkgconfig(libtdm)
BuildRequires: pkgconfig(vulkan)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(wayland-server)
BuildRequires: pkgconfig(wayland-protocols)
BuildRequires: pkgconfig(libtbm)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(dlog)
BuildRequires: vulkan-headers


#%define _unpackaged_files_terminate_build 0
%global TZ_SYS_RO_SHARE  %{?TZ_SYS_RO_SHARE:%TZ_SYS_RO_SHARE}%{!?TZ_SYS_RO_SHARE:/usr/share}

%description
Vulkan WSI (Window System Integration) Layer for Tizen


%prep
%setup -q
cp %{SOURCE1001} .

%build
%if %{defined _toolchain}
%if %{toolchain_is clang}
export CXXFLAGS="$CXXFLAGS -Wno-error=cast-function-type-strict"
%endif
%endif
cmake . -Bbuild                     \
        -DCMAKE_INSTALL_PREFIX=/usr \
        -DBUILD_WSI_TIZEN=ON        \
	-DBUILD_WSI_IMAGE_COMPRESSION_CONTROL_SWAPCHAIN=ON

make -C build

%install
mkdir -p %{buildroot}/usr/local/etc/vulkan/implicit_layer.d/
cp build/VkLayer_window_system_integration.json  %{buildroot}/usr/local/etc/vulkan/implicit_layer.d/
cp build/libVkLayer_window_system_integration.so %{buildroot}/usr/local/etc/vulkan/implicit_layer.d/

%files -n %{name}
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
/usr/local/etc/vulkan/implicit_layer.d/*

