%define module_name	radio
%define name		hal-api-radio

### main package #########
Name:       %{name}
Summary:    %{name} interface
Version:    1.0.1
Release:    0
Group:      Development/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
Source2:    %{name}-haltests.manifest
Source3:    %{name}-manifest.xml

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(hal-api-common)
BuildRequires: pkgconfig(gmock)
BuildRequires: pkgconfig(capi-system-info)

%description
%{name} interface

### devel package #########
%package devel
Summary:	%{name} interface
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
%{name} Interface for product vendor developer

### test package #########
%package haltests
Summary: tests for %{name}
Requires: %{name} = %{version}

%description haltests
Haltests for %{name}

### build and install #########
%prep
%setup -q

cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_LIBDIR_PREFIX=%{_libdir}

%build
cp %{SOURCE1} .
cp %{SOURCE2} .
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
/usr/bin/hal-compatibility-checker --reset

%postun
/sbin/ldconfig
/usr/bin/hal-compatibility-checker --reset

### contain files to package #########
%files	-n %{name}
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/hal/*.so.*
%{_sysconfdir}/hal/%{name}-manifest.xml

%files	devel
%defattr(-,root,root,-)
%{_includedir}/hal/*.h
%{_libdir}/hal/*.so
%{_libdir}/pkgconfig/%{name}.pc

%files	haltests
%manifest %{name}-haltests.manifest
%{_bindir}/hal/radio-haltests
