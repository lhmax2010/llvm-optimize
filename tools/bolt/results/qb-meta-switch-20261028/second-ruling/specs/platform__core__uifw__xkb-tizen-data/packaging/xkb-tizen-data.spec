Name:          xkb-tizen-data
Version:       0.0.7
Release:       0
Provides:      xkb-tizen-data = %{version}-%{release}
BuildArch:     noarch
Summary:       Xkb data files
Group:         Graphics & UI Framework/Other
License:       MIT
Source0:       %{name}-%{version}.tar.gz
Source1001:    %{name}.manifest
BuildRequires: gawk
BuildRequires: grep
BuildRequires: sed
Requires: tizen-release
Requires(post): gawk
Requires(post): grep
Requires(post): sed

%{!?TZ_SYS_RO_SHARE: %global TZ_SYS_RO_SHARE /usr/share}
%global TZ_BUILD_CONF_FILE /etc/tizen-build.conf
%global KEYMAP_INSTALL_PATH %{TZ_SYS_RO_SHARE}/X11/xkb
%global LOCALE_INSTALL_PATH %{TZ_SYS_RO_SHARE}/X11/locale
%global LOCALE_LIGHT_INSTALL_PATH %{TZ_SYS_RO_SHARE}/X11/locale-light

%description
Data files for Xkb keymap

%prep
%setup -q
cp -a %{SOURCE1001} .

export TZ_SYS_RO_SHARE="%{TZ_SYS_RO_SHARE}"
./make_tizen_keysym.sh
echo %{KEYMAP_INSTALL_PATH}

%build
%autogen
%configure

make

%install
rm -rf %{buildroot}

# install service
%__mkdir_p %{buildroot}/%{KEYMAP_INSTALL_PATH}
%__mkdir_p %{buildroot}/%{LOCALE_INSTALL_PATH}
%__mkdir_p %{buildroot}/%{LOCALE_LIGHT_INSTALL_PATH}

%__cp -f xkb/tizen_key_layout.txt.* %{buildroot}/%{KEYMAP_INSTALL_PATH}/
%__cp -f xkb/xkb.rule.* %{buildroot}/%{KEYMAP_INSTALL_PATH}/
%__cp -rf locale/* %{buildroot}/%{LOCALE_INSTALL_PATH}/
%__cp -rf locale-light/* %{buildroot}/%{LOCALE_LIGHT_INSTALL_PATH}/

## tizen symbols
%__cp -f new_symbols.txt %{buildroot}/%{KEYMAP_INSTALL_PATH}/new_symbols.txt

%pre
if [ -e "%{KEYMAP_INSTALL_PATH}/tizen_key_layout.txt" ]; then
	rm %{KEYMAP_INSTALL_PATH}/tizen_key_layout.txt
fi
if [ -e "%{KEYMAP_INSTALL_PATH}/xkb.rule" ]; then
	rm %{KEYMAP_INSTALL_PATH}/xkb.rule
fi

%preun

%post
_tizen_build_profile=common

if [ "%{DEFINED_PROFILE}" = "%{""DEFINED_PROFILE""}" ]; then
	if [ -e %{TZ_BUILD_CONF_FILE} ]; then
		_tizen_build_profile=`grep "TZ_BUILD_PROFILE" %{TZ_BUILD_CONF_FILE} | awk -F '[=]' '{ print $2 }'`
	fi
else
	_tizen_build_profile=%{DEFINED_PROFILE}
fi

echo "${_tizen_build_profile}"

if [ -e %{KEYMAP_INSTALL_PATH}/tizen_key_layout.txt.${_tizen_build_profile} ]; then
	ln -s %{KEYMAP_INSTALL_PATH}/tizen_key_layout.txt.${_tizen_build_profile} %{KEYMAP_INSTALL_PATH}/tizen_key_layout.txt
fi

if [ -e %{KEYMAP_INSTALL_PATH}/xkb.rule.${_tizen_build_profile} ]; then
	ln -s %{KEYMAP_INSTALL_PATH}/xkb.rule.${_tizen_build_profile} %{KEYMAP_INSTALL_PATH}/xkb.rule
fi

%postun

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING
%{TZ_SYS_RO_SHARE}/X11/xkb/tizen_key_layout.txt*
%{TZ_SYS_RO_SHARE}/X11/xkb/xkb.rule*
%{TZ_SYS_RO_SHARE}/X11/xkb/new_symbols.txt
%{LOCALE_INSTALL_PATH}/*
%{LOCALE_LIGHT_INSTALL_PATH}/*
