Name:       usb-modeswitch
Summary:    USB Modeswitch gets mobile broadband cards in operational mode
Version:    2.2.6
Release:    2
Group:      System/Tools
License:    GPL-2.0
URL:        http://www.draisberghof.de/usb_modeswitch/
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  pkgconfig(libusb-1.0)
Requires:       usb-modeswitch-data

%if "%{_with_emulator}" == "1"
ExcludeArch: %{arm} %ix86 x86_64
%endif

%description
USB Modeswitch brings up your datacard into operational mode. When plugged
in they identify themselves as cdrom and present some non-Linux compatible
installation files. This tool deactivates this cdrom-devices and enables
the real communication device. It supports most devices built and
sold by Huawei, T-Mobile, Vodafone, Option, ZTE, Novatel.

%prep
%setup -q

%build
CFLAGS+=" -DTIZEN_MOD -fPIE"
LDFLAGS+=" -pie"
cd jim
./configure
make %{?_smp_mflags}
cd ..
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}/etc
mkdir -p %{buildroot}/usr/sbin
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/etc/udev
mkdir -p %{buildroot}/etc/udev/rules.d
mkdir -p %{buildroot}/usr/share/license

cp usb_modeswitch %{buildroot}/usr/sbin/usb_modeswitch
chmod 700 %{buildroot}/usr/sbin/usb_modeswitch
sed -i 's/tclsh/jimsh/g' usb_modeswitch_dispatcher
cp usb_modeswitch_dispatcher %{buildroot}/usr/sbin/usb_modeswitch_dispatcher
chmod 700 %{buildroot}/usr/sbin/usb_modeswitch_dispatcher
cp jim/jimsh %{buildroot}/usr/bin/jimsh
chmod 700 %{buildroot}/usr/bin/jimsh
cp usb_modeswitch.conf %{buildroot}/etc/usb_modeswitch.conf
chmod 700 %{buildroot}/etc/usb_modeswitch.conf
# original script
cp usb_modeswitch.sh %{buildroot}/etc/udev/usb_modeswitch.sh
chmod 700  %{buildroot}/etc/udev/usb_modeswitch.sh
# wrapper script
cp usb_modeswitch_wrapper.sh %{buildroot}/etc/udev/usb_modeswitch
chmod 700  %{buildroot}/etc/udev/usb_modeswitch
cat LICENSE > %{buildroot}/usr/share/license/%{name}

%files
%manifest usb_modeswitch.manifest
%defattr(-,root,root,-)
%{_bindir}/jimsh
/usr/sbin/usb_modeswitch
/usr/sbin/usb_modeswitch_dispatcher
/etc/udev/usb_modeswitch
/etc/udev/usb_modeswitch.sh
/etc/usb_modeswitch.conf
/usr/share/license/%{name}
