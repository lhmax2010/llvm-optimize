%define module_name	location
%define name		hal-api-%{module_name}
%define devel_name	hal-api-%{module_name}-devel

### main package #########
Name:       %{name}
Summary:    %{name} interface
Version:    0.0.2
Release:    1
Group:      Development/Libraries
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

%description
%{name} interface package for product vendor developer

### devel package #########
%package -n	%{devel_name}
Summary:	%{name} interface
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n	%{devel_name}
%{name} Interface development package for product vendor developer

### build and install #########
%prep
%setup -q

cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_LIBDIR_PREFIX=%{_libdir}/

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
%{_libdir}/hal/*.so*
%{_sysconfdir}/hal/%{name}-manifest.xml

%files	-n %{devel_name}
%defattr(-,root,root,-)
%manifest %{devel_name}.manifest
%license LICENSE
%{_includedir}/hal/*.h
%{_libdir}/pkgconfig/%{name}.pc
