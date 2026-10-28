%define debug_package %{nil}

Name:       media-config
Summary:    Multimedia Framework system configuration package
Version:    0.7.2
Release:    0
Group:      Multimedia/Configuration
License:    LGPL-2.1 and Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Requires: sed

%description
Multimedia Framework system configuration package including ini, conf and etc files.


%ifarch %arm aarch64 riscv64
%ifarch %arm aarch64

%package target-rpi3
Summary: Multimedia Framework system configuration package for rpi3
Group: Multimedia/Configuration
License: LGPL-2.1 and Apache-2.0

%description target-rpi3
Multimedia Framework system configuration package including ini, conf and etc files for rpi3 target.


%package target-c4
Summary: Multimedia Framework system configuration package for ODROID-C4
Group: Multimedia/Configuration
License: LGPL-2.1 and Apache-2.0

%description target-c4
Multimedia Framework system configuration package including ini, conf and etc files for ODROID-C4


%package target-vim3
Summary: Multimedia Framework system configuration package for VIM3
Group: Multimedia/Configuration
License: LGPL-2.1 and Apache-2.0

%description target-vim3
Multimedia Framework system configuration package including ini, conf and etc files for VIM3

%package target-sm8750
Summary: Multimedia Framework system configuration package for SM8750
Group: Multimedia/Configuration
License: LGPL-2.1 and Apache-2.0

%description target-sm8750
Multimedia Framework system configuration package including ini, conf and etc files for SM8750

%endif

%package generic
Summary: Multimedia Framework system configuration package for generic
Group: Multimedia/Configuration
License: LGPL-2.1 and Apache-2.0

%description generic
Multimedia Framework system configuration package including ini, conf and etc files for generic


%package target-vf2
Summary: Multimedia Framework system configuration package for vf2
Group: Multimedia/Configuration
License: LGPL-2.1 and Apache-2.0

%description target-vf2
Multimedia Framework system configuration package including ini, conf and etc files for vf2 target.


%package target-bpif3
Summary: Multimedia Framework system configuration package for BPI-F3
Group: Multimedia/Configuration
License: LGPL-2.1 and Apache-2.0

%description target-bpif3
Multimedia Framework system configuration package including ini, conf and etc files for BPI-F3 target.

%else

%package simulator
Summary: Multimedia Framework system configuration package for simulator
Group: Multimedia/Configuration
License: LGPL-2.1 and Apache-2.0

%description simulator
Multimedia Framework system configuration package including ini, conf and etc files for simulator.

%endif


%prep
%setup -q -n %{name}-%{version}


%build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_hal_datadir}


%ifarch %arm aarch64 riscv64
%ifarch %arm aarch64

mkdir -p %{buildroot}%{_hal_licensedir}/%{name}-target-rpi3
cp LICENSE.APLv2.0 %{buildroot}%{_hal_licensedir}/%{name}-target-rpi3
cp LICENSE.LGPLv2.1 %{buildroot}%{_hal_licensedir}/%{name}-target-rpi3
mkdir -p %{buildroot}%{_hal_datadir}/%{name}-target-rpi3
cp -arf %{name}-target-rpi3/* %{buildroot}%{_hal_datadir}/%{name}-target-rpi3

mkdir -p %{buildroot}%{_hal_licensedir}/%{name}-target-c4
cp LICENSE.APLv2.0 %{buildroot}%{_hal_licensedir}/%{name}-target-c4
cp LICENSE.LGPLv2.1 %{buildroot}%{_hal_licensedir}/%{name}-target-c4
mkdir -p %{buildroot}%{_hal_datadir}/%{name}-target-c4
cp -arf %{name}-target-c4/* %{buildroot}%{_hal_datadir}/%{name}-target-c4

mkdir -p %{buildroot}%{_hal_licensedir}/%{name}-target-vim3
cp LICENSE.APLv2.0 %{buildroot}%{_hal_licensedir}/%{name}-target-vim3
cp LICENSE.LGPLv2.1 %{buildroot}%{_hal_licensedir}/%{name}-target-vim3
mkdir -p %{buildroot}%{_hal_datadir}/%{name}-target-vim3
cp -arf %{name}-target-vim3/* %{buildroot}%{_hal_datadir}/%{name}-target-vim3

mkdir -p %{buildroot}%{_hal_licensedir}/%{name}-target-sm8750
cp LICENSE.APLv2.0 %{buildroot}%{_hal_licensedir}/%{name}-target-sm8750
cp LICENSE.LGPLv2.1 %{buildroot}%{_hal_licensedir}/%{name}-target-sm8750
mkdir -p %{buildroot}%{_hal_datadir}/%{name}-target-sm8750
cp -arf %{name}-target-sm8750/* %{buildroot}%{_hal_datadir}/%{name}-target-sm8750

%endif

mkdir -p %{buildroot}%{_hal_licensedir}/%{name}-generic
cp LICENSE.APLv2.0 %{buildroot}%{_hal_licensedir}/%{name}-generic
cp LICENSE.LGPLv2.1 %{buildroot}%{_hal_licensedir}/%{name}-generic
mkdir -p %{buildroot}%{_hal_datadir}/%{name}-generic
cp -arf %{name}-generic/* %{buildroot}%{_hal_datadir}/%{name}-generic

mkdir -p %{buildroot}%{_hal_licensedir}/%{name}-target-vf2
cp LICENSE.APLv2.0 %{buildroot}%{_hal_licensedir}/%{name}-target-vf2
cp LICENSE.LGPLv2.1 %{buildroot}%{_hal_licensedir}/%{name}-target-vf2
mkdir -p %{buildroot}%{_hal_datadir}/%{name}-target-vf2
cp -arf %{name}-target-vf2/* %{buildroot}%{_hal_datadir}/%{name}-target-vf2

mkdir -p %{buildroot}%{_hal_licensedir}/%{name}-target-bpif3
cp LICENSE.APLv2.0 %{buildroot}%{_hal_licensedir}/%{name}-target-bpif3
cp LICENSE.LGPLv2.1 %{buildroot}%{_hal_licensedir}/%{name}-target-bpif3
mkdir -p %{buildroot}%{_hal_datadir}/%{name}-target-bpif3
cp -arf %{name}-target-bpif3/* %{buildroot}%{_hal_datadir}/%{name}-target-bpif3

%else

mkdir -p %{buildroot}%{_hal_licensedir}/%{name}-simulator
cp LICENSE.APLv2.0 %{buildroot}%{_hal_licensedir}/%{name}-simulator
cp LICENSE.LGPLv2.1 %{buildroot}%{_hal_licensedir}/%{name}-simulator
mkdir -p %{buildroot}%{_hal_datadir}/%{name}-simulator
cp -arf %{name}-simulator/* %{buildroot}%{_hal_datadir}/%{name}-simulator

%endif

%ifarch %arm aarch64 riscv64
%ifarch %arm aarch64

%post target-rpi3
cp -arf %{_hal_datadir}/%{name}-target-rpi3/* /
rm -rf %{_hal_datadir}/%{name}-target-rpi3

%post target-c4
cp -arf %{_hal_datadir}/%{name}-target-c4/* /
rm -rf %{_hal_datadir}/%{name}-target-c4

%post target-vim3
cp -arf %{_hal_datadir}/%{name}-target-vim3/* /
rm -rf %{_hal_datadir}/%{name}-target-vim3

%post target-sm8750
cp -arf %{_hal_datadir}/%{name}-target-sm8750/* /
rm -rf %{_hal_datadir}/%{name}-target-sm8750

%endif

%post generic
cp -arf %{_hal_datadir}/%{name}-generic/* /
rm -rf %{_hal_datadir}/%{name}-generic

%post target-vf2
cp -arf %{_hal_datadir}/%{name}-target-vf2/* /
rm -rf %{_hal_datadir}/%{name}-target-vf2

%post target-bpif3
cp -arf %{_hal_datadir}/%{name}-target-bpif3/* /
rm -rf %{_hal_datadir}/%{name}-target-bpif3

%else

%post simulator
cp -arf %{_hal_datadir}/%{name}-simulator/* /
rm -rf %{_hal_datadir}/%{name}-simulator

%endif


%postun


%ifarch %arm aarch64 riscv64
%ifarch %arm aarch64

%files target-rpi3
%manifest %{name}-target-rpi3.manifest
%{_hal_licensedir}/%{name}-target-rpi3/*
%defattr(-,root,root,-)
%{_hal_datadir}/%{name}-target-rpi3%{_hal_sysconfdir}/asound.conf
%{_hal_datadir}/%{name}-target-rpi3%{_hal_sysconfdir}/pulse/*
%{_hal_datadir}/%{name}-target-rpi3%{_hal_sysconfdir}/murphy/*
%{_hal_datadir}/%{name}-target-rpi3%{_hal_sysconfdir}/multimedia/*.ini
%{_hal_datadir}/%{name}-target-rpi3%{_hal_sysconfdir}/inference/*.ini
%{_hal_datadir}/%{name}-target-rpi3%{_hal_sysconfdir}/vision/depth/*.ini
%{_hal_datadir}/%{name}-target-rpi3%{_hal_sysconfdir}/multimedia/*.conf
%{_hal_datadir}/%{name}-target-rpi3%{_hal_sysconfdir}/multimedia/*.xml
%{_hal_datadir}/%{name}-target-rpi3%{_hal_sysconfdir}/xdg/gstomx.conf
%{_hal_datadir}/%{name}-target-rpi3%{_hal_datadir}/pulseaudio/alsa-mixer/paths/*.conf
%{_hal_datadir}/%{name}-target-rpi3%{_hal_datadir}/pulseaudio/alsa-mixer/paths/*.common
%{_hal_datadir}/%{name}-target-rpi3%{_hal_datadir}/pulseaudio/alsa-mixer/profile-sets/*.conf
%{_hal_datadir}/%{name}-target-rpi3%{_hal_datadir}/pipewire.conf.d/*.conf

%files target-c4
%manifest %{name}-target-c4.manifest
%{_hal_licensedir}/%{name}-target-c4/*
%defattr(-,root,root,-)
%{_hal_datadir}/%{name}-target-c4%{_hal_sysconfdir}/asound.conf
%{_hal_datadir}/%{name}-target-c4%{_hal_sysconfdir}/pulse/*
%{_hal_datadir}/%{name}-target-c4%{_hal_sysconfdir}/murphy/*
%{_hal_datadir}/%{name}-target-c4%{_hal_sysconfdir}/multimedia/*.ini
%{_hal_datadir}/%{name}-target-c4%{_hal_sysconfdir}/inference/*.ini
%{_hal_datadir}/%{name}-target-c4%{_hal_sysconfdir}/vision/depth/*.ini
%{_hal_datadir}/%{name}-target-c4%{_hal_sysconfdir}/multimedia/*.conf
%{_hal_datadir}/%{name}-target-c4%{_hal_sysconfdir}/multimedia/*.xml
%{_hal_datadir}/%{name}-target-c4%{_hal_sysconfdir}/xdg/gstomx.conf
%{_hal_datadir}/%{name}-target-c4%{_hal_datadir}/pulseaudio/alsa-mixer/paths/*.conf
%{_hal_datadir}/%{name}-target-c4%{_hal_datadir}/pulseaudio/alsa-mixer/paths/*.common
%{_hal_datadir}/%{name}-target-c4%{_hal_datadir}/pulseaudio/alsa-mixer/profile-sets/*.conf

%files target-vim3
%manifest %{name}-target-vim3.manifest
%{_hal_licensedir}/%{name}-target-vim3/*
%defattr(-,root,root,-)
%{_hal_datadir}/%{name}-target-vim3%{_hal_sysconfdir}/asound.conf
%{_hal_datadir}/%{name}-target-vim3%{_hal_sysconfdir}/pulse/*
%{_hal_datadir}/%{name}-target-vim3%{_hal_sysconfdir}/murphy/*
%{_hal_datadir}/%{name}-target-vim3%{_hal_sysconfdir}/multimedia/*.ini
%{_hal_datadir}/%{name}-target-vim3%{_hal_sysconfdir}/inference/*.ini
%{_hal_datadir}/%{name}-target-vim3%{_hal_sysconfdir}/vision/depth/*.ini
%{_hal_datadir}/%{name}-target-vim3%{_hal_sysconfdir}/multimedia/*.conf
%{_hal_datadir}/%{name}-target-vim3%{_hal_sysconfdir}/multimedia/*.xml
%{_hal_datadir}/%{name}-target-vim3%{_hal_sysconfdir}/xdg/gstomx.conf
%{_hal_datadir}/%{name}-target-vim3%{_hal_datadir}/pulseaudio/alsa-mixer/paths/*.conf
%{_hal_datadir}/%{name}-target-vim3%{_hal_datadir}/pulseaudio/alsa-mixer/paths/*.common
%{_hal_datadir}/%{name}-target-vim3%{_hal_datadir}/pulseaudio/alsa-mixer/profile-sets/*.conf

%files target-sm8750
%manifest %{name}-target-sm8750.manifest
%{_hal_licensedir}/%{name}-target-sm8750/*
%defattr(-,root,root,-)
%{_hal_datadir}/%{name}-target-sm8750%{_hal_sysconfdir}/asound.conf
%{_hal_datadir}/%{name}-target-sm8750%{_hal_sysconfdir}/pulse/*
%{_hal_datadir}/%{name}-target-sm8750%{_hal_sysconfdir}/murphy/*
%{_hal_datadir}/%{name}-target-sm8750%{_hal_sysconfdir}/multimedia/*.ini
%{_hal_datadir}/%{name}-target-sm8750%{_hal_sysconfdir}/inference/*.ini
%{_hal_datadir}/%{name}-target-sm8750%{_hal_sysconfdir}/multimedia/*.conf
%{_hal_datadir}/%{name}-target-sm8750%{_hal_sysconfdir}/xdg/gstomx.conf
%{_hal_datadir}/%{name}-target-sm8750%{_hal_datadir}/pulseaudio/alsa-mixer/paths/*.conf
%{_hal_datadir}/%{name}-target-sm8750%{_hal_datadir}/pulseaudio/alsa-mixer/paths/*.common
%{_hal_datadir}/%{name}-target-sm8750%{_hal_datadir}/pulseaudio/alsa-mixer/profile-sets/*.conf

%endif

%files generic
%manifest %{name}-generic.manifest
%{_hal_licensedir}/%{name}-generic/*
%defattr(-,root,root,-)
%{_hal_datadir}/%{name}-generic%{_hal_sysconfdir}/asound.conf
%{_hal_datadir}/%{name}-generic%{_hal_sysconfdir}/pulse/*
%{_hal_datadir}/%{name}-generic%{_hal_sysconfdir}/murphy/*
%{_hal_datadir}/%{name}-generic%{_hal_sysconfdir}/multimedia/*.ini
%{_hal_datadir}/%{name}-generic%{_hal_sysconfdir}/inference/*.ini
%{_hal_datadir}/%{name}-generic%{_hal_sysconfdir}/vision/depth/*.ini
%{_hal_datadir}/%{name}-generic%{_hal_sysconfdir}/multimedia/*.conf
%{_hal_datadir}/%{name}-generic%{_hal_sysconfdir}/multimedia/*.json
%{_hal_datadir}/%{name}-generic%{_hal_sysconfdir}/multimedia/*.xml
%{_hal_datadir}/%{name}-generic%{_hal_sysconfdir}/xdg/gstomx.conf
%{_hal_datadir}/%{name}-generic%{_hal_datadir}/pulseaudio/alsa-mixer/paths/*.conf
%{_hal_datadir}/%{name}-generic%{_hal_datadir}/pulseaudio/alsa-mixer/paths/*.common
%{_hal_datadir}/%{name}-generic%{_hal_datadir}/pulseaudio/alsa-mixer/profile-sets/*.conf

%files target-vf2
%manifest %{name}-target-vf2.manifest
%{_hal_licensedir}/%{name}-target-vf2/*
%defattr(-,root,root,-)
%{_hal_datadir}/%{name}-target-vf2%{_hal_sysconfdir}/asound.conf
%{_hal_datadir}/%{name}-target-vf2%{_hal_sysconfdir}/pulse/*
%{_hal_datadir}/%{name}-target-vf2%{_hal_sysconfdir}/murphy/*
%{_hal_datadir}/%{name}-target-vf2%{_hal_sysconfdir}/multimedia/*.ini
%{_hal_datadir}/%{name}-target-vf2%{_hal_sysconfdir}/inference/*.ini
%{_hal_datadir}/%{name}-target-vf2%{_hal_sysconfdir}/vision/depth/*.ini
%{_hal_datadir}/%{name}-target-vf2%{_hal_sysconfdir}/multimedia/*.conf
%{_hal_datadir}/%{name}-target-vf2%{_hal_sysconfdir}/multimedia/*.json
%{_hal_datadir}/%{name}-target-vf2%{_hal_sysconfdir}/multimedia/*.xml
%{_hal_datadir}/%{name}-target-vf2%{_hal_sysconfdir}/xdg/gstomx.conf
%{_hal_datadir}/%{name}-target-vf2%{_hal_datadir}/pulseaudio/alsa-mixer/paths/*.conf
%{_hal_datadir}/%{name}-target-vf2%{_hal_datadir}/pulseaudio/alsa-mixer/paths/*.common
%{_hal_datadir}/%{name}-target-vf2%{_hal_datadir}/pulseaudio/alsa-mixer/profile-sets/*.conf

%files target-bpif3
%manifest %{name}-target-bpif3.manifest
%{_hal_licensedir}/%{name}-target-bpif3/*
%defattr(-,root,root,-)
%{_hal_datadir}/%{name}-target-bpif3%{_hal_sysconfdir}/asound.conf
%{_hal_datadir}/%{name}-target-bpif3%{_hal_sysconfdir}/pulse/*
%{_hal_datadir}/%{name}-target-bpif3%{_hal_sysconfdir}/murphy/*
%{_hal_datadir}/%{name}-target-bpif3%{_hal_sysconfdir}/multimedia/*.ini
%{_hal_datadir}/%{name}-target-bpif3%{_hal_sysconfdir}/inference/*.ini
%{_hal_datadir}/%{name}-target-bpif3%{_hal_sysconfdir}/vision/depth/*.ini
%{_hal_datadir}/%{name}-target-bpif3%{_hal_sysconfdir}/multimedia/*.conf
%{_hal_datadir}/%{name}-target-bpif3%{_hal_sysconfdir}/multimedia/*.json
%{_hal_datadir}/%{name}-target-bpif3%{_hal_sysconfdir}/multimedia/*.xml
%{_hal_datadir}/%{name}-target-bpif3%{_hal_sysconfdir}/xdg/gstomx.conf
%{_hal_datadir}/%{name}-target-bpif3%{_hal_datadir}/pulseaudio/alsa-mixer/paths/*.conf
%{_hal_datadir}/%{name}-target-bpif3%{_hal_datadir}/pulseaudio/alsa-mixer/paths/*.common
%{_hal_datadir}/%{name}-target-bpif3%{_hal_datadir}/pulseaudio/alsa-mixer/profile-sets/*.conf

%else

%files simulator
%manifest %{name}-simulator.manifest
%{_hal_licensedir}/%{name}-simulator/*
%defattr(-,root,root,-)
%{_hal_datadir}/%{name}-simulator%{_hal_sysconfdir}/asound.conf
%{_hal_datadir}/%{name}-simulator%{_hal_sysconfdir}/pulse/*
%{_hal_datadir}/%{name}-simulator%{_hal_sysconfdir}/murphy/*
%{_hal_datadir}/%{name}-simulator%{_hal_sysconfdir}/multimedia/*.ini
%{_hal_datadir}/%{name}-simulator%{_hal_sysconfdir}/inference/*.ini
%{_hal_datadir}/%{name}-simulator%{_hal_sysconfdir}/vision/depth/*.ini
%{_hal_datadir}/%{name}-simulator%{_hal_sysconfdir}/multimedia/*.conf
%{_hal_datadir}/%{name}-simulator%{_hal_sysconfdir}/multimedia/*.json
%{_hal_datadir}/%{name}-simulator%{_hal_sysconfdir}/multimedia/*.xml
%{_hal_datadir}/%{name}-simulator%{_hal_datadir}/pulseaudio/alsa-mixer/paths/*.conf
%{_hal_datadir}/%{name}-simulator%{_hal_datadir}/pulseaudio/alsa-mixer/paths/*.common
%{_hal_datadir}/%{name}-simulator%{_hal_datadir}/pulseaudio/alsa-mixer/profile-sets/*.conf

%endif

