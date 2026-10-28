Name:           opencl-icd-loader
Version:        v2022.01.04
Release:        0
License:        Apache License 2.0
Summary:        an Open Source alternative to vendor specific OpenCL ICD loaders.
Url:            https://github.com/OCL-dev/ocl-icd
Group:          Graphics & UI Framework/Hardware Adaptation
Source:         %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildRequires:  opencl-headers

%description
This repo contains the source code and tests for the Khronos official OpenCL ICD Loader.

%package devel
Summary:   Development files for OpenCL
Group:     Graphics
Requires:  %{name} = %{version}-%{release}

%description devel
This repo contains the source code and tests for the Khronos official OpenCL ICD Loader.

%prep
%setup -q -n %{name}-%{version}

%build
cp %{SOURCE1001} .
%{?asan:/usr/bin/gcc-unforce-options}
%cmake .
make %{?_smp_mflags}

%install
%make_install DESTDIR=%{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%define _unpackaged_files_terminate_build 0
%defattr(-,root,root)
%{_libdir}/libOpenCL*
%license LICENSE
%manifest %{name}.manifest

%files devel
%defattr(-,root,root,-)


