Name: nfc-plugin-emul
Summary: NFC emul plugin
Version: 0.0.26
Release: 0
Group: Network & Connectivity/NFC
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
BuildRequires: cmake
BuildRequires: pkgconfig(hal-rootstrap)

%description
NFC Plugin Emul

%prep
%setup -q
cp %{SOURCE1001} ./%{name}.manifest

%build
%cmake . -DCMAKE_VERBOSE_MAKEFILE=OFF \
         -DHAL_PATH=%{_hal_libdir} \
         -DHAL_LICENSE_PATH=%{_hal_licensedir}
make %{?_smp_mflags}

%install
%make_install

%files
%manifest %{name}.manifest
%{_hal_libdir}/*.so*
/hal/lib/udev/rules.d/98-%{name}.rules
%license %{_hal_licensedir}/LICENSE.APLv2
