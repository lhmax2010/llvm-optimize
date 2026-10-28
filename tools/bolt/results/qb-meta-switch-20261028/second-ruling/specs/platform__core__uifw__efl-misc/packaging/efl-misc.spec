%bcond_with wayland

Name:       efl-misc
Summary:    Elementary config files
Version:    0.1.34
Release:    0
Provides:   efl-misc = %{version}-%{release}
Group:      Graphics & UI Framework/Development
License:    Apache-2.0
BuildArch:  noarch
Source0:    %{name}-%{version}.tar.gz
Source1001: efl-misc.manifest
BuildRequires: eet-tools

%define upgrade_script_path /usr/share/upgrade/scripts

%description
Elementary configuration files

%package -n efl-misc-profile_common
Summary: Elementary config files
License: Apache-2.0

%description -n efl-misc-profile_common
Elementary configuration files for common profile.

%prep
%setup -q
cp %{SOURCE1001} .


%build
make

%install
make install prefix=%{_prefix} DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{upgrade_script_path}
cp -f scripts/500.efl-misc.sh %{buildroot}%{upgrade_script_path}


%post -n efl-misc-profile_common
f="/etc/profile.d/efl_common.sh"
%if %{with wayland}
grep --silent ELM_ENGINE "$f" \
    || printf "\nELM_ENGINE=wayland_shm\n[ ! -d /dev/dri ] || ELM_ENGINE=wayland_egl\nexport ELM_ENGINE" >> "$f"
%else
grep --silent ELM_ENGINE "$f" \
    || printf "\nexport ELM_ENGINE=gl" >> "$f"
%endif


%files -n efl-misc-profile_common
%defattr(-,root,root,-)
%license COPYING
%{_sysconfdir}/profile.d/efl_common.sh
%{_datadir}/elementary/config/common
%manifest %{name}.manifest
%{upgrade_script_path}/500.efl-misc.sh
