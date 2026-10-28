%define debug_package %{nil}

Name:       snpe
Summary:    snpe dummy package
Version:    1.53.2
Release:    1
Group:      Machine Learning/ML Framework
Packager:   Sangjung Woo <sangjung.woo@samsung.com>
License:    BSD-2-Clause
ExclusiveArch:  %{arm} aarch64
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  cmake

%description
The Snapdragon Neural Processing Engine (SNPE) is a Qualcomm Snapdragon software
accelerated runtime for the execution of deep neural networks. Because of
the license issue, the header and binary files of SNPE cannot be opened in public.

To support the NNStreamer filter for SNPE on both In-House build infra and those
of the public, this repo generates a snpe-devel.rpm package, which contains
the snpe-dummy.pc file. In the case of the dummy SNPE package, nnstreamer-snpe rpm
is created but contains no files.

%prep
%setup -q

%build
mkdir -p build
pushd build
%cmake .. \
    -DCMAKE_INSTALL_PREFIX=%{_prefix}
make %{?jobs:-j%jobs}
popd

%install
rm -rf %{buildroot}
pushd build
%make_install
popd

%package -n snpe-devel
Summary: development package for snpe-dummy
%description -n snpe-devel
This package in public Tizen.org is DUMMY (no contents) to keep the build system
running w/o actual SNPE packages.

%files -n snpe-devel
%{_libdir}/pkgconfig/snpe-dummy.pc
