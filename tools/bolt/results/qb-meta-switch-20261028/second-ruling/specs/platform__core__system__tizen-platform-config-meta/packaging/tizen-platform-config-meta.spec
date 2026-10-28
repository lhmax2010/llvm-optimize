Name:           tizen-platform-config-meta
Version:        1.2
Release:        0
Summary:        Tizen Platform Configuration Meta data
License:        MIT
Url:            http://www.tizen.org
Group:          System/Configuration
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}-rpmlintrc
Source2:        %{name}.manifest
Source3:        tizen-platform.meta
Source4:        tizen-platform.product
Source5:        tizen-platform-config-product.manifest

# the main package only contains a config file but other dependent packages
# will contain binary. So, we can't build a noarch package and have to avoid
# a rpmlint warning using a filter in xxx-rpmlintrc

%description
Tizen Platform Configuration Meta data - variables definitions

%package -n tizen-platform-config-product
Summary:    Tizen Platform Configuration Product data
License:    MIT
Group:      System/Configuration
Requires: tizen-platform-config

%description -n tizen-platform-config-product
Tizen Platform Configuration Product data

%prep
%setup -q
cp %{SOURCE2} .
cp %{SOURCE5} .

%install
mkdir -p %{buildroot}%{_sysconfdir}
cp %{SOURCE3} %{buildroot}%{_sysconfdir}/tizen-platform.meta
cp %{SOURCE4} %{buildroot}%{_sysconfdir}/tizen-platform.product

%post -n tizen-platform-config-product

cp %{_sysconfdir}/tizen-platform.product %{_sysconfdir}/tizen-platform.conf

%files
%manifest %{name}.manifest
%license LICENSE.MIT
%attr(644, root, root) %{_sysconfdir}/tizen-platform.meta

%files -n tizen-platform-config-product
%manifest tizen-platform-config-product.manifest
%license LICENSE.MIT
%attr(644, root, root) %{_sysconfdir}/tizen-platform.product
