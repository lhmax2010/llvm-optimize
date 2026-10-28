Name:       alsa-ucm-data-rpi3
Summary:    ALSA UCM data pkg for rpi3
Version:    0.0.1
Release:    1
License:    Apache-2.0
BuildArch:  noarch
Source0:    %{name}-%{version}.tar.gz

%description
ALSA UCM data for rpi3

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/hal/share/alsa/ucm
mkdir -p %{buildroot}%{_hal_licensedir}/%{name}
cp -a bcm2835 %{buildroot}%{_hal_datadir}/alsa/ucm
cp LICENSE.Apache-2.0 %{buildroot}%{_hal_licensedir}/%{name}

%post

%files
%manifest alsa-ucm-conf-rpi3.manifest
%{_hal_datadir}/alsa/ucm/bcm2835/*
%{_hal_licensedir}/%{name}/LICENSE.Apache-2.0
