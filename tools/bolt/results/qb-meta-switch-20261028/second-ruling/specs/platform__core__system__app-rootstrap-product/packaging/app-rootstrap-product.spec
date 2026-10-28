Name:		app-rootstrap-product
Summary:	Package for product rootstrap configuration
Version:	10.0.0
Release:	1
License:	Apache-2.0
Source0:	%{name}-%{version}.tar.gz
AutoReqProv:    no

%define PRODUCT_CONFIG_PATH	%{_datadir}/app-rootstrap-product

BuildRequires:	pkgconfig(app-rootstrap)
BuildRequires:	tizen-platform-config
BuildRequires:	pkgconfig(libtzplatform-config)
BuildRequires:	tizen-platform-config-product
BuildRequires:	tizen-platform-config-tools

Requires:	pkgconfig(app-rootstrap)
Requires(post):	pkgconfig(libtzplatform-config)
Requires(post):	tizen-platform-config

%description
Package that updates /etc/tizen-platform.conf with product version from tizen-platform-config-product

### app-rootstrap-product-devel
%package devel
Summary:        Development files for app-rootstrap-product
Group:          Development/Tools
AutoReqProv:    no
Provides:       pkgconfig(app-rootstrap-product)
Requires:       %{name} = %{version}-%{release}

%description devel
Development files for app-rootstrap-product including pkgconfig file.

%prep
%setup -q

%build
cp /etc/tizen-platform.product tizen-platform.conf
tzplatform-tool rpm tizen-platform.conf | grep -v TZ_USER_ > macros.tizen-platform

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{PRODUCT_CONFIG_PATH}/rpm
cp tizen-platform.conf %{buildroot}%{PRODUCT_CONFIG_PATH}/tizen-platform.conf
cp macros.tizen-platform %{buildroot}%{PRODUCT_CONFIG_PATH}/rpm/macros.tizen-platform

# Install dummy pkgconfig file for devel
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cp packaging/app-rootstrap-product.pc %{buildroot}%{_libdir}/pkgconfig/

%post
# Replace /etc/tizen-platform.conf (installed by app-rootstrap-devel)
# Update /etc/tizen-platform.conf with product version
if [ -f %{PRODUCT_CONFIG_PATH}/tizen-platform.conf ]; then
    cp -f %{PRODUCT_CONFIG_PATH}/tizen-platform.conf /etc/tizen-platform.conf
fi
if [ -f %{PRODUCT_CONFIG_PATH}/rpm/macros.tizen-platform ]; then
    cp -f %{PRODUCT_CONFIG_PATH}/rpm/macros.tizen-platform /etc/rpm/macros.tizen-platform
fi

%files
%defattr(-,root,root,-)
%{PRODUCT_CONFIG_PATH}/tizen-platform.conf
%{PRODUCT_CONFIG_PATH}/rpm/macros.tizen-platform


%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/app-rootstrap-product.pc
