#sbs-git:slp/sdk/default-fonts-fc-sdk default-fonts-fc-sdk 0.0.2 8414dbd3e62b6f7a864ba031e043dd7604b3d86d
Name:       default-fonts-fc-sdk
Summary:    Font configuration package for SDK
Version:    0.0.5
Release:    1
Group:      TO_BE/FILLED_IN
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: packaging/default-fonts-fc-sdk.manifest
BuildRequires:  pkgconfig(libtzplatform-config)

%description
Font configuration package for SDK
This package is maintained by SDK team

%prep
%setup -q

%build
cp %{SOURCE1001} .

%install
export FONT_CONF_FILE_1="99-tizen.conf"
export FONT_CONF_FILE_2="98-tizen-alias.conf"

## TZ_SYS_RO_ETC: /etc, TZ_SYS_ETC: /opt/etc/
rm -rf %{buildroot}
mkdir -p %{buildroot}%{TZ_SYS_RO_ETC}/fonts/conf.d/
mkdir -p %{buildroot}%{TZ_SYS_ETC}/fonts/conf.avail/ && cp -a sdk_fonts_fc/* %{buildroot}%{TZ_SYS_ETC}/fonts/conf.avail/
ln -s %{TZ_SYS_ETC}/fonts/conf.avail/$FONT_CONF_FILE_1 %{buildroot}%{TZ_SYS_RO_ETC}/fonts/conf.d/$FONT_CONF_FILE_1
ln -s %{TZ_SYS_ETC}/fonts/conf.avail/$FONT_CONF_FILE_2 %{buildroot}%{TZ_SYS_RO_ETC}/fonts/conf.d/$FONT_CONF_FILE_2

%post
chown root:users %{TZ_SYS_ETC}/fonts/conf.avail/*.conf
chmod 664 %{TZ_SYS_ETC}/fonts/conf.avail/*.conf
chsmack -a '*' %{TZ_SYS_ETC}/fonts/conf.avail/*.conf

%files
%manifest default-fonts-fc-sdk.manifest
%defattr(-,root,root,-)
%{TZ_SYS_ETC}/fonts/conf.avail/*.conf
%{TZ_SYS_RO_ETC}/fonts/conf.d/*.conf
%exclude %{TZ_SYS_RO_ETC}/fonts/conf.d/documentation.list
