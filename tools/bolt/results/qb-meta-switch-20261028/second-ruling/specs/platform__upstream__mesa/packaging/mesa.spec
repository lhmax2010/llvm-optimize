Name:           mesa
Version:        24.3.4
Release:        0
License:        MIT and Apache-2.0 and SGI Free Software License B v2.0 and BSD-3-Clause
Summary:        System for rendering interactive 3-D graphics
Url:            http://www.mesa3d.org
Group:          Graphics & UI Framework/Hardware Adaptation
Source:         %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest
Source1002:     99-GPU-Acceleration.rules


Requires:       libtpl-egl
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(libdrm) >= 2.4.75
BuildRequires:  pkgconfig(libudev) > 150
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(tpl-egl)
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  pkgconfig(libtdm)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  meson
BuildRequires:  python3
BuildRequires:  python3-mako
BuildRequires:  python3-packaging
BuildRequires:  python3-PyYAML
BuildRequires:  pkgconfig(ttrace)
%ifarch x86_64 %ix86
BuildRequires:  pkgconfig(libdrm_intel) >= 2.4.24
%endif

%define enable_driver() %{expand:%%{?!enable_%{1}: %%global enable_%{1} 1}}

%define append_drivers() %{?gallium_drivers: %global gallium_drivers %{expand:%{gallium_drivers}},%{expand:%{1}}}\
						 %{?!gallium_drivers: %global gallium_drivers %{expand:%{1}}}

%define enable_gallium_driver() \
	%append_drivers %{1} \
	%enable_driver %{1}

%enable_driver gbm

%ifarch %ix86 x86_64
%enable_gallium_driver i915
%enable_gallium_driver softpipe
%enable_gallium_driver virgl

%define vulkan_drivers ""
%define dri_drivers ""

%else
%define USE_VULKAN 1
%define VULKAN_DRIVER broadcom

%if %{USE_VULKAN} == 1
%enable_driver vulkan
%endif

%enable_gallium_driver softpipe
%enable_gallium_driver vc4
%enable_gallium_driver v3d
%enable_gallium_driver virgl

%define vulkan_drivers "%{?enable_vulkan:%{VULKAN_DRIVER}}"
%define dri_drivers "auto"
%endif

%description
Mesa is a 3-D graphics library with an API which is very similar to
that of OpenGL.* To the extent that Mesa utilizes the OpenGL command
syntax or state machine, it is being used with authorization from
Silicon Graphics, Inc.(SGI). However, the author does not possess an
OpenGL license from SGI, and makes no claim that Mesa is in any way a
compatible replacement for OpenGL or associated with SGI. Those who
want a licensed implementation of OpenGL should contact a licensed
vendor.

Please do not refer to the library as MesaGL (for legal reasons). It's
just Mesa or The Mesa 3-D graphics library.

* OpenGL is a trademark of Silicon Graphics Incorporated.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .
cp %{SOURCE1002} .

%build
%{?asan:/usr/bin/gcc-unforce-options}
mkdir build

meson setup --prefix %{_hal_prefix} build/ \
        -Dc_link_args="-lttrace" \
        -Dcpp_link_args="-lttrace" \
        -Dlibdir=%{_hal_libdir} \
        -Dgallium-va=disabled \
        -Dgallium-vdpau=disabled \
        -Dgallium-xa=disabled \
        -Dglx=disabled \
        -Ddraw-use-llvm=false \
        -Dllvm=disabled \
        -Dgbm=%{?enable_gbm:enabled}%{?!enable_gbm:disabled} \
        -Dplatforms="tizen" \
        -Dgallium-drivers=%{gallium_drivers} \
        -Dvulkan-drivers=%{vulkan_drivers}

ninja -C build/

%install
DESTDIR=%{buildroot} ninja -C build/ install
mkdir -p %{buildroot}%{_hal_libdir}/driver
mkdir -p %{buildroot}%{_hal_libdir}/dri
mkdir -p %{buildroot}%{_hal_prefix}/share/vulkan/icd.d

cp -a %{buildroot}%{_hal_libdir}/libEGL* %{buildroot}%{_hal_libdir}/driver/
cp -a %{buildroot}%{_hal_libdir}/libGLES* %{buildroot}%{_hal_libdir}/driver/

mkdir -p %{buildroot}%{_hal_libdir}/udev/rules.d
cp 99-GPU-Acceleration.rules %{buildroot}%{_hal_libdir}/udev/rules.d

mkdir -p %{buildroot}%{_hal_prefix}/share/licenses/%{name}
cp -r licenses/* %{buildroot}%{_hal_prefix}/share/licenses/%{name}/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%define _unpackaged_files_terminate_build 0
%manifest %{name}.manifest
%defattr(-,root,root)
%{_hal_prefix}/share/licenses/%{name}/*
%{_hal_libdir}/libglapi*
%{_hal_libdir}/libgallium*.so
%{_hal_libdir}/driver/*

%if %{expand:%{?enable_gbm:1}%{?!enable_gbm:0}}
%{_hal_libdir}/gbm/dri_gbm.so
%endif

%if "%{USE_VULKAN}" == "1"
%{_hal_libdir}/libvulkan_%{VULKAN_DRIVER}.so
%{_hal_prefix}/share/vulkan/icd.d/*
%endif
%{_hal_libdir}/udev/rules.d/99-GPU-Acceleration.rules
