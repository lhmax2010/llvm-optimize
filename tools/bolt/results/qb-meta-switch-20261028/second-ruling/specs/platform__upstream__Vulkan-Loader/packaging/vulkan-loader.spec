Name:	    vulkan-loader
Version:    1.3.296
Release:    0
Summary:    Vulkan ICD loader
Group:      Graphics & UI Framework/GL
License:    Apache-2.0
Source:		%{name}-%{version}.tar.gz
Source1001: %{name}.manifest

BuildRequires:  cmake
BuildRequires:  python3
BuildRequires:  vulkan-headers = %{version}
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(dlog)

%define BUILD_TYPE Debug

%description
This project provides the Khronos Vulkan ICD.

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
export CFLAGS="$CFLAGS -w"
cmake -DCMAKE_BUILD_TYPE=%{BUILD_TYPE} -DBUILD_TESTS=OFF -DTIZEN_PLATFORM=ON \
      -DBUILD_WSI_XLIB_SUPPORT=OFF -DBUILD_WSI_XCB_SUPPORT=OFF -DBUILD_WSI_WAYLAND_SUPPORT=ON \
      -DCMAKE_INSTALL_LIBDIR=%{_libdir} -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} -DCMAKE_INSTALL_DATADIR=%{_datadir}
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/vulkan/{explicit,implicit}_layer.d/ \
%{buildroot}%{_datadir}/vulkan/{explicit,implicit}_layer.d/ \
%{buildroot}{%{_sysconfdir},%{_datadir}}/vulkan/icd.d
%make_install

%remove_docs

%files
%manifest %{name}.manifest
%license LICENSE.txt
%defattr(-,root,root,-)
%dir %{_sysconfdir}/vulkan/
%dir %{_sysconfdir}/vulkan/explicit_layer.d/
%dir %{_sysconfdir}/vulkan/icd.d/
%dir %{_sysconfdir}/vulkan/implicit_layer.d/
%dir %{_datadir}/vulkan/
%dir %{_datadir}/vulkan/explicit_layer.d/
%dir %{_datadir}/vulkan/icd.d/
%dir %{_datadir}/vulkan/implicit_layer.d/
%{_libdir}/*.so.*

%files devel
%{_libdir}/pkgconfig/vulkan.pc
%{_libdir}/*.so
%{_libdir}/cmake/*
