Name:       hal-backend-device-vim3
Summary:    Device HAL backend drivers for vim3 targets
Version:    0.0.1
Release:    0
Group:      System/Hardware Adaptation
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
ExclusiveArch:  %{arm} aarch64
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  cmake
BuildRequires:  pkgconfig(hal-rootstrap)

%description
Device HAL backend drivers for Amlogic vim3 targets

%prep
%setup -q
cp %{SOURCE1} .

%build
%cmake . -DENABLE_DLOG=on \
	-DHAL_LICENSE_DIR=%{_hal_licensedir} \
	-DHAL_LIB_DIR=%{_hal_libdir}

make %{?jobs:-j%jobs}

%install
%make_install

# install conf files
mkdir -p %{buildroot}%{_hal_sysconfdir}/deviced
install -m 644 conf/*.conf %{buildroot}%{_hal_sysconfdir}/deviced

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%{_hal_libdir}/*.so*
%manifest %{name}.manifest
%{_hal_licensedir}/%{name}/LICENSE.Apache-2.0
%{_hal_sysconfdir}/deviced/*
