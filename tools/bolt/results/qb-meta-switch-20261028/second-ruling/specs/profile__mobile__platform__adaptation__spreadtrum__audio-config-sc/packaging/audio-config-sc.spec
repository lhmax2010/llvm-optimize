Name:       audio-config-sc
Summary:    audio configuration files
Version:    0.1.17
Release:    0
Group:      TO_BE/FILLED_IN
License:    Apache-2.0
BuildArch:  noarch
Source0:    audio-config-sc-%{version}.tar.gz
Requires(post): coreutils

%description
audio configuration files for spreadtrum devices such as ucm files.

%package TM1-sc7730
Summary: audio configuration files for TM1-sc7730
Group: TO_BE/FILLED_IN
License:    Apache-2.0

%description TM1-sc7730
audio configuration files for TM1-sc7730

%prep
%setup -q -n %{name}-%{version}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_hal_datadir}/alsa/ucm/TM1-sc7730
mkdir -p %{buildroot}%{_hal_licensedir}/%{name}
mkdir -p %{buildroot}/usr/etc
mkdir -p %{buildroot}/opt/system
mkdir -p %{buildroot}/opt/etc/dump.d/module.d

cp -arf Z3-3G-sc7730/ucm/* %{buildroot}/hal/share/alsa/ucm/TM1-sc7730
cp LICENSE %{buildroot}%{_hal_licensedir}/%{name}
cp -arf Z3-3G-sc7730/audio_para/audio_para %{buildroot}/usr/etc/audio_para.tm1
cp -arf Z3-3G-sc7730/audio_para/audio_para %{buildroot}/opt/system/audio_para.tm1
cp -arf Z3-3G-sc7730/vbc_eq/vbc_eq %{buildroot}/opt/system/vbc_eq
cp -a util/regdump_sprd_audio.sh %{buildroot}/opt/etc/dump.d/module.d/

%pre TM1-sc7730
UCM_PATH=/hal/share/alsa/ucm
rm -rf $UCM_PATH/*
rm -rf /usr/etc/audio_para*
rm -rf /opt/system/audio_para*
rm -rf /lib/firmware/vbc_eq

%post TM1-sc7730
UCM_PATH=/hal/share/alsa/ucm
ln -s $UCM_PATH/TM1-sc7730 $UCM_PATH/sprdphone
ln -s /usr/etc/audio_para.tm1 /usr/etc/audio_para
ln -s /opt/system/audio_para.tm1 /opt/system/audio_para
ln -s /opt/system/vbc_eq /lib/firmware/vbc_eq

%files TM1-sc7730
%manifest audio-config-sc.manifest
%defattr(-,root,root,-)
%{_hal_licensedir}/%{name}/LICENSE
%{_hal_datadir}/alsa/ucm/TM1-sc7730/*
/usr/etc/audio_para.tm1
/opt/system/audio_para.tm1
/opt/system/vbc_eq
/opt/etc/dump.d/module.d/regdump_sprd_audio.sh
