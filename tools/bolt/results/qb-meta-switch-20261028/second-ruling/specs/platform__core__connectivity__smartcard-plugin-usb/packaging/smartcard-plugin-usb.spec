Name:             smartcard-plugin-usb
Summary:          Smartcard plugin usb
Version:          0.0.1
Release:          0
Group:            Network & Connectivity/Smartcard
License:          Apache-2.0
Source0:          %{name}-%{version}.tar.gz
BuildRequires:    cmake
BuildRequires:    pkgconfig(glib-2.0)
BuildRequires:    pkgconfig(dlog)
BuildRequires:    pkgconfig(smartcard-service-common)
BuildRequires:    pkgconfig(libpcsclite)
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig


%description
Smartcard Service plugin usb

%prep
%setup -q

%build
cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} \
%ifarch aarch64 x86_64 riscv64
	 -DTIZEN_ARCH_64=1 \
%endif

%install
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE.APLv2
%defattr(-,root,root,-)
%{_libdir}/se/lib*.so
