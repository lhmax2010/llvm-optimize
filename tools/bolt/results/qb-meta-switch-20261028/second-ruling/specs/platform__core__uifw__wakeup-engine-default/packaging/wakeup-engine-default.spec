Name:       wakeup-engine-default
Summary:    Default wakeup engine for multi-assistant-service
Version:    0.2.5
Release:    1
Group:      Graphics & UI Framework/Voice Framework
License:    Flora-1.1
Source0:    %{name}-%{version}.tar.gz
BuildRequires: cmake
BuildRequires: pkgconfig(libtzplatform-config)
%description
wakeup-engine-default is the library of reference wakeup-engine.

%prep
%setup -q

%build
%define _app_home_dir   %{TZ_SYS_RO_APP}/%{name}
%define _app_bin_dir    %{_app_home_dir}/bin
%define _app_lib_dir    %{_app_home_dir}/lib
%define _app_res_dir    %{_app_home_dir}/shared/res
%define _app_shared_dir    %{_app_home_dir}/shared

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
cmake . -DCMAKE_INSTALL_PREFIX=/usr -DFULLVER=%{version} -DMAJORVER=${MAJORVER}

make %{?jobs:-j%jobs}
%install
rm -rf %{buildroot}

%make_install

%post

%postun

%files
%{_app_res_dir}/*
%{TZ_SYS_RO_PACKAGES}/wakeup-engine-default.xml
/usr/share/multiassistant/engines/wakeup-engine-default/libwakeup-engine.so
%manifest wakeup-engine-default.manifest
%license LICENSE.Flora
