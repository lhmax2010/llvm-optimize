Name:               hal-backend-device-emulator
Summary:            Device HAL backend drivers for emulator targets
Version:            0.0.21
Release:            1
Group:              SDK/Other
License:            Apache-2.0
Source0:            %{name}-%{version}.tar.gz
Source1:            %{name}.manifest
ExclusiveArch:      %{ix86} x86_64 aarch64 %{arm}
Requires(post):     /sbin/ldconfig
Requires(postun):   /sbin/ldconfig
BuildRequires:      cmake
BuildRequires:      pkgconfig(hal-rootstrap)

%description
Device HAL backend drivers for emulator targets

%prep
%setup -q
cp %{SOURCE1} .

%build
export LDFLAGS="$LDFLAGS -Wl,--rpath=%{_libdir} -Wl,--as-needed"
%cmake . -DENABLE_DLOG=on \
	-DHAL_LIB_DIR=%{_hal_libdir} \
	-DHAL_LICENSE_DIR=%{_hal_licensedir}

make

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
%{_hal_licensedir}/%{name}/LICENSE
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_hal_libdir}/*.so*
%{_hal_sysconfdir}/deviced/*
