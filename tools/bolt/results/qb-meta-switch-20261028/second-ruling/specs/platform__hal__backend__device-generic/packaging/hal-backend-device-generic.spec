Name:       hal-backend-device-generic
Summary:    Generic device HAL backend drivers for all normal targets
Version:    0.0.1
Release:    0
Group:      System/Hardware Adaptation
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  cmake
BuildRequires:  pkgconfig(hal-rootstrap)

%description
Generic device HAL backend drivers for all normal targets

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

# Reboot register storage
mkdir -p %{buildroot}%{_hal_sysconfdir}/reboot
touch %{buildroot}%{_hal_sysconfdir}/reboot/register_storage

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%manifest %{name}.manifest
%{_hal_licensedir}/%{name}/LICENSE.Apache-2.0
%{_hal_sysconfdir}/reboot/register_storage
