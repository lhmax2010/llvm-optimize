Name:           hal-backend-config-rubikpi3
Summary:        Platform Extension configuration for QCS6490 & QCS5430
Group  :        System/Hardware Adaptation
Version:        1.0
Release:        0
ExclusiveArch:  aarch64
License:        Apache-2.0
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.manifest

AutoReqProv:    no

%description
Platform Extension configuration for QCS6490 (Rubik Pi 3) & QCS5430 (RB3 Gen2 Lite)

%prep
%setup -q
cp %{SOURCE1} .

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/hal

# Copy all regular files to /hal
cp -a hal/* %{buildroot}/hal

# hal-backend-config-rubikpi3 symlinks
mkdir -p %{buildroot}/hal/lib/systemd/system/multi-user.target.wants
mkdir -p %{buildroot}/hal/lib/systemd/system/local-fs.target.wants

ln -sf "../adsprpcd.service" "%{buildroot}/hal/lib/systemd/system/multi-user.target.wants/adsprpcd.service"
ln -sf "../cdsprpcd.service" "%{buildroot}/hal/lib/systemd/system/multi-user.target.wants/cdsprpcd.service"
ln -sf "../pd-mapper.service" "%{buildroot}/hal/lib/systemd/system/multi-user.target.wants/pd-mapper.service"
ln -sf "../property-vault.service" "%{buildroot}/hal/lib/systemd/system/local-fs.target.wants/property-vault.service"
ln -sf "../qrtr-ns.service" "%{buildroot}/hal/lib/systemd/system/multi-user.target.wants/qrtr-ns.service"

# Licenses
mkdir -p %{buildroot}/%{_hal_licensedir}/%{name}
cp LICENSE %{buildroot}/%{_hal_licensedir}/%{name}

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_hal_licensedir}/%{name}/LICENSE
/hal/etc/dl.conf.d/*
/hal/etc/platform-extension/*
/hal/lib/systemd/system/*
/hal/etc/udev/rules.d/kgsl.rules
