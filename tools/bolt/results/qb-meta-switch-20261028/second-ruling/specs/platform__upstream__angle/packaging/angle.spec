Name:       angle
Summary:    angle
Version:    2.1
Release:    1
Group:      System/Libraries
License:    BSD License
Source0:    %{name}-%{version}.tar
Source1001:	%name.manifest

%define ANGLE_DIR %{_libdir}/driver

%ifarch armv7l aarch64
%define _build_enable 1
%endif

%ifarch armv7l
%define _angle_target_cpu arm
%define _angle_arm_ver 7
%define _angle_arm_arch armv7-a
%endif
%ifarch aarch64
%define _angle_target_cpu arm64
%define _angle_arm_ver 8
%define _angle_arm_arch armv8-a
%endif


%if 0%{?_build_enable}

BuildRequires:  cmake
BuildRequires:  ninja
BuildRequires:  python3
BuildRequires:  llvm
BuildRequires:  libllvm
BuildRequires:  clang
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  glibc
BuildRequires:  binutils
BuildRequires:  binutils-gold
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gthread-2.0)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  spirv-headers
BuildRequires:  pkgconfig(SPIRV-Tools)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  glslang-devel
BuildRequires:  spirv-tools
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(jsoncpp)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  abseil-cpp
BuildRequires:  python

%endif

%description
Almost Native Graphics Layer Engine from Google


%debug_package


%prep
%if 0%{?_build_enable}

%setup -q
cp %{SOURCE1001} .

%endif

%build
%if 0%{?_build_enable}
./gn gen out/Debug --args='target_os="linux" target_cpu="%{_angle_target_cpu}" arm_version="%{_angle_arm_ver}" arm_float_abi="softfp" arm_arch="%{_angle_arm_arch}" is_debug=false angle_use_wayland=true angle_use_tbm=true angle_use_gbm=false angle_enable_vulkan=true angle_enable_swiftshader=false use_libpci=false angle_use_x11=false target_sysroot = "/" angle_enable_wgpu=false ozone_platform_x11=false use_goma=false is_component_build=false angle_enable_trace=false angle_enable_trace_events=false  angle_assert_always_on=false angle_enable_vulkan_gpu_trace_events=false angle_use_custom_libvulkan=false angle_build_vulkan_system_info=false angle_debug_layers_enabled=false angle_enable_vulkan_validation_layers=false enable_dsyms=true symbol_level=2 strip_debug_info=false use_dwarf5=false use_ozone=false angle_enable_commit_id=false use_custom_libcxx=false is_clang=false treat_warnings_as_errors=false angle_enable_perf_counter_output=false build_angle_deqp_tests=false angle_has_histograms=false angle_has_astc_encoder=false'
ninja -C out/Debug -j4 -v

%endif


%install
%if 0%{?_build_enable}

mkdir -p "%{buildroot}"%{ANGLE_DIR}
install out/Debug/lib*.so "%{buildroot}"%{ANGLE_DIR}
ln -sf libEGL_angle.so                               %{buildroot}%{ANGLE_DIR}/libEGL.so
ln -sf libGLESv2_angle.so                            %{buildroot}%{ANGLE_DIR}/libGLESv2.so
ln -sf libGLESv1_CM_angle.so                         %{buildroot}%{ANGLE_DIR}/libGLESv1_CM.so

%endif

#cp -R --parents $(find out/Debug/obj -name '*.dwo') "%{buildroot}"%{ANGLE_DIR}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%if 0%{?_build_enable}

%manifest %{name}.manifest
%{ANGLE_DIR}/*

%endif



