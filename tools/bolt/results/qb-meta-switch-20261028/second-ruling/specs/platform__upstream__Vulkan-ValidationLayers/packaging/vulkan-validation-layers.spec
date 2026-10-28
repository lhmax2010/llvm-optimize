Name:       vulkan-validation-layers
Version:    1.3.296
Release:    0
Summary:    Vulkan validation layers
Group:      Graphics & UI Framework/GL
License:    Apache-2.0
Source:     %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

BuildRequires:  cmake
BuildRequires:  python3
BuildRequires:  vulkan-headers = %{version}
BuildRequires:  glslang-devel
BuildRequires:  pkgconfig(SPIRV-Tools) = 2024.4.1
BuildRequires:  spirv-tools
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  spirv-headers
BuildRequires:  spirv-headers-devel
BuildRequires:  vulkan-utility-libraries

%define BUILD_TYPE Debug

%description
This project provides the Vulkan validation layers.

%package        devel
Summary:        Development files for %{name}
Requires:       vulkan-headers

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
cp %{SOURCE1001} .
export CFLAGS="-O0 -w -Wno-psabi -Wl,--no-undefined"
export CXXFLAGS="-O0 -w -Wno-psabi -Wl,--no-undefined"
export LDFLAGS="-Wl,--no-as-needed -L/usr/lib -lpthread"
cmake -S . -DCMAKE_BUILD_TYPE=%{BUILD_TYPE} -DCMAKE_VERBOSE_MAKEFILE=ON \
      -DBUILD_WSI_XLIB_SUPPORT=OFF -DBUILD_WSI_XCB_SUPPORT=OFF -DBUILD_WSI_WAYLAND_SUPPORT=ON \
      -DGLSLANG_INSTALL_DIR=%{_bindir} -DSPIRV_HEADERS_INSTALL_DIR=%{_includedir}/spirv \
      -DVULKAN_HEADERS_INSTALL_DIR=/usr -DBUILD_TESTS=OFF -DUPDATE_DEPS=OFF \
      -DUSE_ROBIN_HOOD_HASHING=OFF -DVVL_CODEGEN=ON\
      -DCMAKE_INSTALL_LIBDIR=%{_libdir} -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir}/vulkan \
      -DCMAKE_INSTALL_DATADIR=%{_datadir} -DCMAKE_INSTALL_BINDIR=%{_bindir}
make -j8

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_includedir}/vulkan
%make_install
cp -a ./layers/vulkan/generated/*.h %{buildroot}%{_includedir}/vulkan
cp -a ./layers/lib*.a %{buildroot}/%{_libdir}
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE.txt
%defattr(-,root,root,-)
%{_includedir}/vulkan/*
%{_libdir}/lib*
/usr/share/vulkan/explicit_layer.d/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/vulkan/


