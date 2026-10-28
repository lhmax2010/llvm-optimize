Name:           nvethernetrm
Version:        36.4.4
Release:        0
License:        GPL-2.0
Source0:        %{name}-%{version}.tar.xz
Source1:        %{name}.manifest
Summary:        NVIDIA Ethernet Resource Manager
Group:          System/Kernel
BuildArch:	noarch

%description
This is a dummy main package for nvethernetrm. The actual source code
is in the devel sub-package.

%package devel
License: GPL-2.0
Summary: Development sources for compiling the nvethernetrm driver
Group: System/Kernel
Provides: nvethernetrm-devel = %{version}-%{release}

%description devel
This package contains the source code for the nvethernetrm(NVIDIA Ethernet
Resource Manager) kernel module. These sources are specifically intended
to be copied into the linux-nv-oot directory and compiled as part of the
NVIDIA out-of-tree kernel module build process.

%prep
%setup -q
cp %{SOURCE1} .

%build
# There is no build process.

%install
mkdir -p %{buildroot}/boot/kernel/devel/nvethernetrm
cp -r * %{buildroot}/boot/kernel/devel/nvethernetrm/

%files
%manifest nvethernetrm.manifest
%license COPYING

%files devel
/boot/kernel/devel/nvethernetrm/
