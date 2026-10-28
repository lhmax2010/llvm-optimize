Name:       spirv-headers
Version:    1.5.5
Release:    0
Summary:    Khronos SPIRV Headers
Group:      Graphics & UI Framework/GL
License:    MIT
Source:     %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

BuildRequires:  cmake
BuildRequires:  pkg-config
BuildRequires:  libtool

%define BUILD_TYPE Debug

%description
Khronos SPIRV Headers

%package devel
Summary:    Khronos SPIRV Headers
Group:      System/Libraries

%description devel
Khronos SPIRV Headers

%prep
%setup -q

%build
cp %{SOURCE1001} .

# build SPIRV headers
mkdir build
cd build
cmake ..
cmake --build . 
cd ..

%install
rm -rf %{buildroot}
# release pkg
mkdir -p  %{buildroot}%{_includedir}/
mkdir -p  %{buildroot}%{_datadir}/cmake/SPIRV-Headers/
cp -Rf  include/spirv %{buildroot}%{_includedir}/
cp -rf build/generated/* %{buildroot}%{_datadir}/cmake/SPIRV-Headers
#cp -rf build/CMakeFiles/Export/share/cmake/SPIRV-Headers/* %{buildroot}%{_datadir}/cmake/SPIRV-Headers
find build/CMakeFiles/Export/ -name 'SPIRV-Headers*.cmake' -exec cp {} %{buildroot}%{_datadir}/cmake/SPIRV-Headers \;
# devel pkg
cp -rf  include/* %{buildroot}%{_includedir}/

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_includedir}/spirv/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/spirv/*
%{_datadir}/cmake/*

