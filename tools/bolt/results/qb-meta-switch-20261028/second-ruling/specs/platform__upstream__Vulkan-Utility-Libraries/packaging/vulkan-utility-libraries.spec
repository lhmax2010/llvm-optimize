Name:	 vulkan-utility-libraries
Version: 1.3.296
Release: 0
Summary: Vulkan utility libraries
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
BuildRequires:  spirv-headers

%define BUILD_TYPE Debug

%description
This repo was created to share code across various Vulkan repositories, 
solving long standing issues for Vulkan SDK developers and users.

%prep
%setup -q

%build
cp %{SOURCE1001} .
export CFLAGS="-O0 -w -Wno-psabi -fvisibility=default"
export CXXFLAGS="-O0 -w -Wno-psabi -fvisibility=default"
cmake -S . -B build/ -D CMAKE_BUILD_TYPE=%{BUILD_TYPE} -D CMAKE_INSTALL_PREFIX="/usr" -D BUILD_SHARED_LIBS=OFF
cmake --build build --config %{BUILD_TYPE}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_includedir}/vulkan
mkdir -p %{buildroot}%{_libdir}/cmake
cd build
make DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSES
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*
