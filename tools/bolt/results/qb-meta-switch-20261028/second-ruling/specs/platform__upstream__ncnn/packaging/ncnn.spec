%define		builddir	build
%define		upstream_release_version	20240102

###########################################################################
# Package and sub-package definitions
Name:		ncnn
Summary:	A high-performance neural network inference framework optimized for the mobile platform
Version:	%{upstream_release_version}
Release:	1e88fb8
Group:		Machine Learning/ML Framework
Packager:	Wook Song <wook16.song@samsung.com>
License:	BSD-3-Clause
Source0:	%{name}-%{version}.tar
Source1001:	%{name}.manifest

## Define build requirements ##
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: protobuf-lite-devel
BuildRequires: opencv-devel
BuildRequires: vulkan-loader-devel

## Define Packages ##
%description
ncnn is a high-performance neural network inference computing framework
optimized for mobile platforms. ncnn is deeply considerate about deployment
and uses on mobile phones from the beginning of design. ncnn does not have
third party dependencies. It is cross-platform, and runs faster than all known
open source frameworks on mobile phone cpu. Developers can easily deploy deep
learning algorithm models to the mobile platform by using efficient ncnn
implementation, create intelligent APPs, and bring the artificial intelligence
to your fingertips. ncnn is currently being used in many Tencent applications,
such as QQ, Qzone, WeChat, Pitu and so on.

%package devel
Summary:	Development package for the ncnn framework
%description devel
Development package for the ncnn framework.
This contains corresponding header files and static archives.

%package tools
Summary:	Binary package for tools included in the ncnn framework
%description tools
This is a binary package that provides tools and model converters included in
the ncnn framework.

%package examples
Summary:	Binary package for native examples
%description examples
This is a binary package that contains native examples developed based on
the APIs of the ncnn framework.

%prep
rm -rf ./%{builddir}
%setup -q
cp %{SOURCE1001} .

%build
CXXFLAGS=`echo -std=c++11 -fno-builtin $CXXFLAGS`
%define cmake_common_options -DNCNN_VERSION=%{upstream_release_version}-%{release} -DCMAKE_BUILD_TYPE=release -DNCNN_SHARED_LIB=ON -G Ninja
%ifnarch aarch64 i586 x86_64
%define cmake_arch_options -DNCNN_ENABLE_LTO=OFF
%else
%define cmake_arch_options -DNCNN_ENABLE_LTO=ON
%endif
%ifarch %arm
%{?asan:/usr/bin/gcc-unforce-options}
%endif

mkdir -p %{builddir}
pushd %{builddir}
cmake .. %{cmake_common_options} %{cmake_arch_options}
cmake --build .
popd

%install
pushd %{builddir}
DESTDIR=%{buildroot} cmake --install . --prefix %{_prefix}
install -p -m 755 benchmark/benchncnn %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_bindir}/ncnn_examples
find examples -type f -executable -exec install -p -m 755 {} %{buildroot}%{_bindir}/ncnn_examples \;
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE.txt
%{_libdir}/*.so.*
%{_bindir}/benchncnn

%files devel
%defattr(-,root,root,-)
%{_includedir}/ncnn/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/ncnn/*.cmake
%{_libdir}/*.so

%files tools
%{_bindir}/ncnn2mem
%{_bindir}/ncnnmerge
%{_bindir}/ncnnoptimize
%{_bindir}/caffe2ncnn
%{_bindir}/darknet2ncnn
%{_bindir}/mxnet2ncnn
%{_bindir}/ncnn2int8
%{_bindir}/ncnn2table
%{_bindir}/onnx2ncnn

%files examples
%{_bindir}/ncnn_examples/*
