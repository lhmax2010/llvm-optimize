Name:		usb-modeswitch-data
Summary:	USB Modeswitch gets mobile broadband cards in operational mode
Version:	20151101
Release:	2
Group:		System/Tools
License:	GPL-2.0
URL:		http://www.draisberghof.de/usb_modeswitch/
Source0:	%{name}-%{version}.tar.gz

%if "%{_with_emulator}" == "1"
ExcludeArch: %{arm} %ix86 x86_64
%endif

%description
This package contains the data files needed for usb_modeswitch to function.

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}/etc/udev
mkdir -p %{buildroot}/etc/udev/rules.d
mkdir -p %{buildroot}/usr/share/usb_modeswitch
mkdir -p %{buildroot}/usr/share/license

cp 40-usb_modeswitch.rules %{buildroot}/etc/udev/rules.d/40-usb_modeswitch.rules
chmod 644 %{buildroot}/etc/udev/rules.d/40-usb_modeswitch.rules
cp -rf  usb_modeswitch.d/* %{buildroot}/usr/share/usb_modeswitch/
chmod 777 %{buildroot}/usr/share/usb_modeswitch/
cat COPYING > %{buildroot}/usr/share/license/%{name}

%files
%defattr(-,root,root,-)
/etc/udev/rules.d/40-usb_modeswitch.rules
/usr/share/usb_modeswitch
/usr/share/license/%{name}
