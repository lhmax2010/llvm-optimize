Name:	 vulkan-tools
Version: 1.3.296
Release: 0
Summary: Vulkan tools
Group:   Graphics & UI Framework/GL
License: Apache-2.0
Source:     %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

BuildRequires:  cmake
BuildRequires:  pkg-config
BuildRequires:  libtool
BuildRequires:  python3
BuildRequires:  glslang
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols)

%define BUILD_TYPE Debug
%ifarch aarch64 riscv64 x86_64
%define __libdir lib64
%endif
%ifarch armv7l
%define __libdir lib
%endif

%description
This project provides the Khronos Vulkan Tools.

%prep
%setup -q

%build
cp %{SOURCE1001} .
export CFLAGS="$CFLAGS -w"
cd scripts/volk/
cmake . -Bbuild -DVOLK_INSTALL=ON
make -C build
find build/CMakeFiles/Export/ -name 'volk*.cmake' -exec cp {} build/ \;
cd ../../
mkdir include
mkdir %{__libdir}
cp scripts/volk/build/libvolk.a %{__libdir}
cp scripts/volk/volk.* include
cmake -DCMAKE_BUILD_TYPE=%{BUILD_TYPE} -Dvolk_DIR="./scripts/volk/build"\
      -DBUILD_WSI_XLIB_SUPPORT=OFF -DBUILD_WSI_XCB_SUPPORT=OFF -DBUILD_WSI_WAYLAND_SUPPORT=ON \
      -DCUBE_WSI_SELECTION=WAYLAND \
      -DCMAKE_INSTALL_LIBDIR=%{_libdir} -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
      -DCMAKE_INSTALL_DATADIR=%{_datadir} -DCMAKE_INSTALL_BINDIR=%{_bindir} .
make -j6

%install
rm -rf %{buildroot}
%make_install

%remove_docs

%files
%manifest %{name}.manifest
%license LICENSE.txt
%defattr(-,root,root,-)
%{_bindir}/*
