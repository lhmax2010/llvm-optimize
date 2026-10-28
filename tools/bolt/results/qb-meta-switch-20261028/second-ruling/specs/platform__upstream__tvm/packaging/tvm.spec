Name:       tvm-runtime
Summary:    TVM Runtime Library
Version:    0.7.0
Release:    0
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: tvm.manifest

BuildRequires:  cmake

%description
Apache TVM is a compiler stack for deep learning systems. It is designed to close the gap between the productivity-focused deep learning frameworks, and the performance- and efficiency-focused hardware backends. TVM works with deep learning frameworks to provide end to end compilation to different backends.

%package devel
Summary:    develelopment package for TVM
Requires:   %{name} = %{version}-%{release}

%description devel
development package for tvm

%prep
%setup -q
cp %{SOURCE1001} .

%build
mkdir -p build
cp cmake/config.cmake build
pushd build
%{cmake} ..
%{__make} runtime %{?_smp_mflags}
popd

%install
mkdir -p %{buildroot}{%{_libdir},%{_includedir},%{_libdir}/pkgconfig}
cp -r build/libtvm_runtime.so %{buildroot}%{_libdir}
cp -r include/* %{buildroot}%{_includedir}
cp -r 3rdparty/dlpack/include/* %{buildroot}%{_includedir}
cp -r 3rdparty/dmlc-core/include/* %{buildroot}%{_includedir}
cp -r tvm_runtime.pc %{buildroot}%{_libdir}/pkgconfig

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest tvm.manifest
%defattr(-,root,root,-)
%{_libdir}/*.so

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/tvm_runtime.pc
%{_includedir}/*

