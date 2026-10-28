%define module_name	sensor
%define name		hal-api-sensor
%define devel_name	hal-api-sensor-devel

### main package #########
Name:       %{name}
Summary:    %{name} interface
Version:    0.0.1
Release:    1
Group:      System/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
Source2:    %{devel_name}.manifest
Source3:    %{name}-manifest.xml

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gmock)
BuildRequires: pkgconfig(hal-api-common)
BuildRequires: pkgconfig(capi-system-info)

%description
%{name} interface

### devel package #########
%package -n	%{devel_name}
Summary:	%{name} interface
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n	%{devel_name}
%{name} Interface for product vendor developer

### hal test package ########
%package haltests
Summary:	Sensor HAL(Hardware Abstraction Layer) Test Cases
Requires:	%{name} = %{version}-%{release}

%description haltests
Sensor HAL(Hardware Abstraction Layer) Test Cases

### build and install #########
%prep
%setup -q


%build
cp %{SOURCE1} .
cp %{SOURCE2} .
cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_LIBDIR_PREFIX=%{_libdir} \
	-DHALTEST=on
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/hal
cp %{SOURCE3} %{buildroot}%{_sysconfdir}/hal/
%make_install

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

### contain files to package #########
%files	-n %{name}
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/hal/*.so*
%{_sysconfdir}/hal/%{name}-manifest.xml

%files	-n %{devel_name}
%defattr(-,root,root,-)
%manifest %{devel_name}.manifest
%license LICENSE
%{_includedir}/hal/*.h
%{_libdir}/pkgconfig/%{name}.pc

%files haltests
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/hal/sensor-haltests
