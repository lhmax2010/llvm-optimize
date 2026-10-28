Name:       cbhm
Summary:    Clipboard History Manager
Version:    2.0.11
Release:    1
Group:      Graphics & UI Framework/Service
License:    Apache-2.0 and MIT
URL:        http://www.samsung.com/
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.service
Source2:    %{name}.path
Source1001: %{name}.manifest

BuildRequires: cmake
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(tizen-extension-client)
BuildRequires: pkgconfig(tizen-policy-ext-client)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(dlog)
Requires(post): /sbin/ldconfig, /usr/bin/systemctl
Requires(postun): /sbin/ldconfig, /usr/bin/systemctl

%description
Tizen Clipboard History Manager Service

%package devel
Summary:    Library for Tizen Clipboard History Manager (Development)
Group:      Graphics & UI Framework/Development
Requires:   %{name} = %{version}-%{release}

%description devel
Tizen Clipboard History Manager Service development kit

%prep
%setup -q
chmod g-w %{_sourcedir}/*
cp %{SOURCE1001} ./%{name}.manifest

%build
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CFLAGS="$CFLAGS -DEFL_BETA_API_SUPPORT"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"

%define _pkg_dir %{TZ_SYS_RO_APP}/org.tizen.%{name}

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
rm -rf CMakeFiles CMackCache.txt && %cmake . -DMAJORVER=${MAJORVER} \
		-DFULLVER=%{version} -DCMAKE_INSTALL_PREFIX=%{_pkg_dir} \
        -DBIN_INSTALL_DIR:PATH=%{_bindir} \

make %{?jobs:-j%jobs}

%install
%make_install

## systemd
mkdir -p %{buildroot}%{_unitdir_user}/paths.target.wants
install -m 0644 %SOURCE1 %{buildroot}%{_unitdir_user}/%{name}.service
install -m 0644 %SOURCE2 %{buildroot}%{_unitdir_user}/%{name}.path
ln -s ../%{name}.path %{buildroot}%{_unitdir_user}/paths.target.wants/%{name}.path

%post
systemctl daemon-reload
if [ "$1" = 1 ]; then
    systemctl restart %{name}.service
fi
/sbin/ldconfig

%postun
if [ "$1" = 0 ]; then
    systemctl stop %{name}.service
fi
systemctl daemon-reload
/sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_pkg_dir}/bin/%{name}-service
## systemd
%{_unitdir_user}/%{name}.service
%{_unitdir_user}/%{name}.path
%{_unitdir_user}/paths.target.wants/%{name}.path
%manifest %{name}.manifest
%license LICENSE.APLv2 LICENSE.MIT

%files devel
%defattr(-,root,root,-)

