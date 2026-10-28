%define version 1.1.0
%define release 1

Name:       hal-backend-power-generic 
Summary:    Power HAL for standard linux interface
Version:    %{version}
Release:    %{release}
Group:      System/Hardware Adaptation
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest

Requires(post): /sbin/ldconfig
Requires(post): /bin/systemctl
Requires(post): security-config
Requires(postun): /sbin/ldconfig
Requires(postun): /bin/systemctl
BuildRequires:  cmake
BuildRequires:  pkgconfig(hal-rootstrap)

%description
PASS standard hal

%prep
%setup -q
cp %{SOURCE1} .

%build
%cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_HAL_LIBDIR_PREFIX=%{_hal_libdir} \
	-DCMAKE_HAL_LICENSEDIR_PREFIX=%{_hal_licensedir} \

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

%make_install

%post
/sbin/ldconfig
systemd-tmpfiles /hal/lib/tmpfiles.d/pass-hal.conf --create
if [ -f %{_unitdir}/pass.service ]; then
	systemctl try-restart pass.service
fi

%postun
/sbin/ldconfig
if [ -f %{_unitdir}/pass.service ]; then
	systemctl try-restart pass.service
fi

%files
%manifest %{name}.manifest
%{_hal_licensedir}/%{name}/LICENSE
%{_hal_libdir}/*.so
/hal/lib/tmpfiles.d/pass-hal.conf
