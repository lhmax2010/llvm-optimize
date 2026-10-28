%define debug_package %{nil}

Name:		unified-model-config
Summary:	All Model configurations
Version:	11.0.0
Release:	0
Group:		System/Configuration
BuildArch:	noarch
License:	Apache-2.0
Source0:	%{name}-%{version}.tar.gz
Source1001:	%{name}.manifest

%description
Model configuration data package

%package -n model-config-generic
Summary:	A Model configuration
Provides:	model-config
%description -n model-config-generic
Model configuration data package

%package -n model-config-default
Summary:	Default Model configuration for IoT
Provides:	model-config
%description -n model-config-default
Model configuration data package main body having default values for Tizen IOT

%package -n model-config-generic-hal
Summary:	Model configuration for HAL Backend
Provides:	model-config
%description -n model-config-generic-hal
Model configuration data package for HAL Backend

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} ./%{name}.manifest

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/config

###### For generic & iot ######
cp -f generic/model-config.xml %{buildroot}%{_sysconfdir}/config/generic.xml
cp -f generic/model-config-iot.xml %{buildroot}%{_sysconfdir}/config/iot.xml

###### For generic hal ######
mkdir -p %{buildroot}%{_hal_sysconfdir}/config
cp -f generic/model-config-hal.xml %{buildroot}%{_hal_sysconfdir}/config/hal.xml

install -d %{buildroot}%{_hal_licensedir}/model-config-generic-hal/
install -m 664 LICENSE.Apache-2.0 %{buildroot}%{_hal_licensedir}/model-config-generic-hal/

install -d %{buildroot}%{_bindir}
install -m 755 scripts/model-config-cli %{buildroot}%{_bindir}


%post -n model-config-generic
ln -sf generic.xml %{_sysconfdir}/config/model-config.xml
%files -n model-config-generic
%manifest %{name}.manifest
%config %{_sysconfdir}/config/generic.xml
%{_bindir}/model-config-cli
%license LICENSE.Apache-2.0

%post -n model-config-default
ln -sf iot.xml %{_sysconfdir}/config/model-config.xml
%files -n model-config-default
%manifest %{name}.manifest
%config %{_sysconfdir}/config/iot.xml
%{_bindir}/model-config-cli
%license LICENSE.Apache-2.0

%post -n model-config-generic-hal
ln -sf hal.xml %{_hal_sysconfdir}/config/model-config.xml
%files -n model-config-generic-hal
%manifest %{name}.manifest
%config %{_hal_sysconfdir}/config/hal.xml
%{_hal_licensedir}/model-config-generic-hal/LICENSE.Apache-2.0
