Name:       opencl-headers
Version:    v2022.01.04
Release:    0
Summary:    Khronos OpenCL Headers
Group:      Graphics & OpenCL
License:    Apache License 2.0
Source:     %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

BuildRequires:  cmake
BuildRequires:  pkg-config


%define BUILD_TYPE Debug

%description
Khronos OpenCL Headers

%package devel
Summary:    Khronos OpenCL Headers
Group:      System/Libraries

%description devel
Khronos OpenCL Headers

%prep
%setup -q

%build
cp %{SOURCE1001} .

# build OpenCL headers
%cmake .  -DDOCUMENTATION_FORMAT=man \
          -DCMAKE_C_FLAGS="%{optflags} -fPIC" \
          -DCMAKE_EXE_LINKER_FLAGS=" -pie"
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
%make_install DESTDIR=%{buildroot}

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_includedir}/CL/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/CL/*

%define _unpackaged_files_terminate_build 0
