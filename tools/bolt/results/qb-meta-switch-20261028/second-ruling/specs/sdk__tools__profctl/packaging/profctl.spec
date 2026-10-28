%{!?buildtype: %define buildtype Release}

Name:       profctl
Summary:    Utility to control profiling applications
Version:    1.0.0
Release:    1
Group:      Development/Toolchain
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1000: profctl.manifest

BuildRequires: cmake

AutoReqProv: no

%define sdk_install_prefix /home/owner/share/tmp/sdk_tools/%{name}

%description
Utility to control profiling applications

%prep
%setup -q
cp %{SOURCE1000} .

%build

cmake \
	-DCMAKE_INSTALL_PREFIX=%{sdk_install_prefix} \
	-DBINDIR=. \
	-DCMAKE_BUILD_TYPE=%{buildtype}
make %{?jobs:-j%jobs} VERBOSE=1

%install
rm -rf %{buildroot}
%make_install
touch %{buildroot}%{sdk_install_prefix}/version-%{version}-%{release}

%files
%manifest profctl.manifest
%{sdk_install_prefix}/*
