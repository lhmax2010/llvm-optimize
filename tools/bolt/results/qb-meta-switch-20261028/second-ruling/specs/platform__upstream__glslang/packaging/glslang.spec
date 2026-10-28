Name:	    glslang
Version:    13.1.1
Release:    0
Summary:    Khronos reference front-end for GLSL and ESSL, and sample SPIR-V generator
Group:      Graphics & UI Framework/GL
License:    BSD-2-Clause
Source:	    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

BuildRequires:  cmake
BuildRequires:	pkg-config
BuildRequires:  libtool
BuildRequires:  bison
BuildRequires:  python3

%description
Khronos reference front-end for GLSL and ESSL, and sample SPIR-V generator

%package devel
Summary:    Khronos reference front-end for GLSL and ESSL, and sample SPIR-V generator
Group:		Graphics & UI Framework/GL

%description devel
Khronos reference front-end for GLSL and ESSL, and sample SPIR-V generator

%prep
%setup -q

%build
cp %{SOURCE1001} .
export CXXFLAGS="$CXXFLAGS -w -fPIE -Wno-psabi"
export LDFLAGS="$LDFLAGS -pie"
cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=ON -DENABLE_OPT=OFF \
      -DCMAKE_INSTALL_LIBDIR=%{_libdir} -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} -DCMAKE_INSTALL_DATADIR=%{_datadir} \
      -DCMAKE_INSTALL_BINDIR=%{_bindir} -DCMAKE_INSTALL_PREFIX=""
make

%install
rm -rf %{buildroot}
mkdir -p build
cp -a glslang/libglslang* build/
cp -a glslang/OSDependent/Unix/libOSDependent.a build/
cp -a SPIRV/libSPVRemapper.* build/
cp -a SPIRV/libSPIRV.* build/

%make_install

cp -a build/* %{buildroot}%{_libdir}/

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/glslang*
%{_bindir}/spirv-remap
%{_libdir}/libglslang*
%{_libdir}/libOSDependent.*
%{_libdir}/libSPVRemapper.*
%{_libdir}/libSPIRV.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/libglslang*
%{_libdir}/libOSDependent.*
%{_libdir}/libSPVRemapper.*
%{_libdir}/libSPIRV.*
%{_libdir}/cmake/*
